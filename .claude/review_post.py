#!/usr/bin/env python3
"""블로그 포스트 결정적 리뷰 검사. 표준 라이브러리만 사용한다.

사용법: python review_post.py <파일.md> [<파일2.md> ...]
인자가 없으면 아무것도 출력하지 않고 0으로 종료한다.
"""
import sys
import re
import json
import xml.dom.minidom as minidom
from collections import namedtuple
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import review_report as rr

# ---- 심각도 ----
REQUIRED = "🔴 필수"
RECOMMENDED = "🟡 권장"
INFO = "🟢 참고"
SEVERITY_ORDER = [REQUIRED, RECOMMENDED, INFO]
SEVERITY_ICON = {
    REQUIRED: "🔴",
    RECOMMENDED: "🟡",
    INFO: "🟢",
}
GATE_EFFECT = {
    REQUIRED: "fail",
    RECOMMENDED: "warn",
    INFO: "info",
}

# ---- 임계치 ----
EMDASH_RATIO = 0.08
EMDASH_MIN = 6
BOLD_RATIO = 0.6
DESC_MIN = 40
DESC_MAX = 220

# ---- 경로 ----
REPO_ROOT = Path(__file__).resolve().parent.parent  # .claude/ 의 부모 = 레포 루트
PUBLIC_DIR = REPO_ROOT / "public"
POSTS_DIR = REPO_ROOT / "src" / "content" / "posts"

Finding = namedtuple("Finding", "severity code line message")

# 닫는 ** 앞이 구두점이고 바로 뒤가 글자/숫자/한글이면 굵게가 적용되지 않는다.
_CLOSE_PUNCT = ")].,!?:;'\"”’」』）}"
BROKEN_BOLD = re.compile(
    "[" + re.escape(_CLOSE_PUNCT) + r"]\*\*[0-9A-Za-z가-힣]"
)
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
REQUIRED_KEYS = ["title", "date", "description", "tags", "category", "difficulty"]
CANONICAL_CATEGORIES = {"theory", "cryptography", "algorithm", "os", "unity", "web-dev"}
CANONICAL_DIFFICULTIES = {"입문", "초급", "중급", "고급", "심화"}
_FM_KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
# ](/blog/<slug>) 또는 ](/blog/<slug>#anchor) 의 slug/anchor 추출
BLOG_LINK_RE = re.compile(r"\]\(/blog/([^)\s#]+)(?:#([^\)\s]+))?")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# D9 이모지 검사: 규칙은 ✅/❌ 같은 "이모지"를 금하고 O/X·텍스트를 쓰라는 것.
#   - U+1F000~1FAFF 이모지 블록은 모두 금지.
#   - 기본 표시가 이모지인 체크/엑스/경고/하트 기호를 명시적으로 금지.
#   - 단, 텍스트 표시 단순 기호 ✓(U+2713)·✗(U+2717)·✘는 허용한다(표·검증 표기에 정당하게 쓰임).
_BANNED_EMOJI = set("✅❌✔✖❎⚠☑❗❓❣❤➕➖➗") | {"️"}
# 말미 callout 구조 검사용
CALLOUT_OPEN_RE = re.compile(r'<div class="(callout[^"]*)">')
CALLOUT_TITLE_RE = re.compile(r'<div class="callout-title">(.*?)</div>')
# 번호가 붙은 시리즈 slug: <base>-<n>
SERIES_RE = re.compile(r"^(.*)-(\d+)$")


def split_frontmatter(text):
    """(frontmatter, body, body_start_line) 반환. body_start_line은 1-indexed."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm = "\n".join(lines[1:i])
                body = "\n".join(lines[i + 1:])
                return fm, body, i + 2
    return "", text, 1


# ---- 검사 stub (이후 태스크에서 구현) ----
def check_frontmatter(fm):
    out = []
    keys = {}
    for line in fm.split("\n"):
        m = _FM_KEY_RE.match(line)
        if m:
            keys[m.group(1)] = m.group(2)
    for k in REQUIRED_KEYS:
        if k not in keys:
            out.append(Finding(RECOMMENDED, "D7", None, f"frontmatter 누락: {k}"))
    if "description" in keys:
        desc = keys["description"].strip().strip('"').strip("'")
        if len(desc) < DESC_MIN:
            out.append(Finding(INFO, "D7", None, f"description 너무 짧음 ({len(desc)}자)"))
        elif len(desc) > DESC_MAX:
            out.append(Finding(INFO, "D7", None, f"description 너무 긺 ({len(desc)}자)"))
    if "category" in keys:
        category = _frontmatter_scalar(keys["category"])
        if category not in CANONICAL_CATEGORIES:
            allowed = ", ".join(sorted(CANONICAL_CATEGORIES))
            out.append(Finding(
                REQUIRED, "D7", None,
                f"frontmatter enum 불일치: category='{category}' — 허용값: {allowed}"
            ))
    if "difficulty" in keys:
        difficulty = _frontmatter_scalar(keys["difficulty"])
        if difficulty not in CANONICAL_DIFFICULTIES:
            allowed = ", ".join(sorted(CANONICAL_DIFFICULTIES))
            out.append(Finding(
                REQUIRED, "D7", None,
                f"frontmatter enum 불일치: difficulty='{difficulty}' — 허용값: {allowed}"
            ))
    return out


def _frontmatter_scalar(value):
    return value.strip().strip('"').strip("'")


def check_broken_bold(body, offset):
    out = []
    for i, line in enumerate(body.split("\n")):
        for m in BROKEN_BOLD.finditer(line):
            snippet = line[max(0, m.start() - 3):m.end()]
            out.append(Finding(
                REQUIRED, "D1", i + offset,
                f"깨진 굵게: '{snippet}' — 닫는 ** 앞 구두점 + 뒤 글자"
            ))
    return out


def _line_at(path, line):
    if not line:
        return "not-recorded"
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return "not-recorded"
    if 1 <= line <= len(lines):
        return lines[line - 1].strip() or "not-recorded"
    return "not-recorded"


def _sample_emdash_locations(path, body, offset, limit=3):
    if offset is None:
        return []
    samples = []
    for i, line in enumerate(body.split("\n")):
        if "—" in line:
            samples.append(f"{path}:{i + offset}")
            if len(samples) >= limit:
                break
    return samples


def check_emdash(body, path=None, offset=None):
    count = body.count("—")
    line_count = max(1, len(body.split("\n")))
    threshold = max(EMDASH_MIN, round(line_count * EMDASH_RATIO))
    if count > threshold:
        samples = _sample_emdash_locations(path, body, offset) if path else []
        sample_msg = f" 샘플 위치: {', '.join(samples)}" if samples else ""
        return [Finding(
            RECOMMENDED, "D2", None,
            f"줄표(—) {count}회 — 임계치({threshold}) 초과. AI 문체 신호{sample_msg}"
        )]
    return []


def check_emphasis(body):
    bold = len(BOLD_RE.findall(body))
    nonempty = max(1, len([ln for ln in body.split("\n") if ln.strip()]))
    if bold > nonempty * BOLD_RATIO:
        return [Finding(
            INFO, "D3", None,
            f"굵게 강조 {bold}회 (본문 {nonempty}줄) — 강조가 잦아 효과가 떨어질 수 있음"
        )]
    return []


def svg_error(path):
    """SVG가 well-formed면 None, 아니면 첫 줄 오류 메시지."""
    try:
        minidom.parse(str(path))
        return None
    except Exception as e:  # noqa: BLE001 - 파싱 실패 사유를 그대로 보고
        return str(e).splitlines()[0][:80]


def extract_svg_text_labels(path):
    """LLM 비교 보조용 SVG <text> 라벨 목록을 추출한다. 결정적 의미 비교는 하지 않는다."""
    try:
        doc = minidom.parse(str(path))
    except Exception:  # noqa: BLE001 - 호출자는 svg_error/svg_baseline_findings로 오류를 보고한다.
        return []
    labels = []
    for el in doc.getElementsByTagName("text"):
        text = "".join(
            node.data for node in el.childNodes
            if node.nodeType == node.TEXT_NODE
        ).strip()
        if text:
            labels.append(text)
    return labels


def svg_baseline_findings(path, url):
    """SVG 구조 기준선 검사. 색/품질/본문과의 의미 일치는 판단하지 않는다."""
    out = []
    try:
        doc = minidom.parse(str(path))
    except Exception as e:  # noqa: BLE001 - 파싱 실패 사유를 그대로 보고
        return [f"SVG 파싱 오류: {url} ({str(e).splitlines()[0][:80]})"]
    root = doc.documentElement
    if root is None or root.tagName != "svg":
        return [f"SVG 루트 오류: {url} (root <svg> 아님)"]
    view_box = root.getAttribute("viewBox").strip()
    if not view_box:
        out.append(f"SVG viewBox 누락: {url}")
    else:
        parts = [p for p in re.split(r"[ ,]+", view_box) if p]
        nums = [_fnum_str(p) for p in parts]
        if len(nums) != 4 or any(n is None for n in nums):
            out.append(f"SVG viewBox 형식 오류: {url} (viewBox='{view_box}')")
        else:
            _, _, width, height = nums
            if width < 0 or height < 0:
                out.append(f"SVG viewBox 크기 음수: {url} (viewBox='{view_box}')")
    if not root.getAttribute("width").strip() or not root.getAttribute("height").strip():
        out.append(f"SVG width/height 누락: {url}")
    return out


def check_assets(body, offset):
    out = []
    for i, line in enumerate(body.split("\n")):
        for m in IMG_RE.finditer(line):
            url = m.group(1).split()[0].strip()  # "(/path \"title\")" 의 title 제거
            if not url.startswith("/"):
                continue
            asset = PUBLIC_DIR / url.lstrip("/")
            if not asset.exists():
                out.append(Finding(REQUIRED, "D5", i + offset, f"에셋 없음: {url}"))
            elif url.lower().endswith(".svg"):
                baseline_errors = svg_baseline_findings(asset, url)
                if baseline_errors:
                    for err in baseline_errors:
                        out.append(Finding(REQUIRED, "D4", i + offset, err))
                    continue
                # D13: 명백한 세로 클리핑만 잡는다. ">25px 여백" 같은 작법 권고는
                # 기존 코퍼스가 대부분 따르지 않아(타이트한 푸터 관행) 결정적 검사로는 오탐이 된다.
                ext = svg_vertical_extent(asset)
                if ext:
                    vb_y, vb_h, mt, mb = ext
                    if mt < vb_y - 2:
                        out.append(Finding(
                            REQUIRED, "D13", i + offset,
                            f"SVG 세로 클리핑: 최상단 요소 y≈{mt:.0f}이 viewBox 시작 {vb_y:.0f}보다 위에 있어 잘림 — {url}"
                        ))
                    if mb > vb_y + vb_h + 2:
                        out.append(Finding(
                            REQUIRED, "D13", i + offset,
                            f"SVG 세로 클리핑: 최하단 요소 y≈{mb:.0f}이 viewBox 끝 {vb_y + vb_h:.0f}를 넘어 잘림 — {url}"
                        ))
    return out


def check_series_links(path, body):
    """D12 — 번호 시리즈(<base>-<n>)는 인접 편 포스트가 존재하면 본문에서 /blog/로 상호 링크한다."""
    out = []
    slug = Path(path).stem
    m = SERIES_RE.match(slug)
    if not m:
        return out
    base, n = m.group(1), int(m.group(2))
    linked = {bm.group(1) for bm in BLOG_LINK_RE.finditer(body)}
    for adj, label in ((n - 1, "이전"), (n + 1, "다음")):
        if adj < 1:
            continue
        sib = f"{base}-{adj}"
        if (POSTS_DIR / f"{sib}.md").exists() and sib not in linked:
            out.append(Finding(
                RECOMMENDED, "D12", None,
                f"시리즈 {label} 편 링크 누락: /blog/{sib}(`{sib}.md` 존재)을 본문에서 참조하지 않음"
            ))
    return out


def _fnum(el, name, default=None):
    v = el.getAttribute(name)
    if not v:
        return default
    try:
        return float(re.sub(r"[^0-9.\-]", "", v))
    except ValueError:
        return default


def svg_vertical_extent(path):
    """(viewBox y, 높이, 요소 최상단 y, 최하단 y)를 반환. 구하지 못하거나 transform이 있으면 None.

    transform이 있으면 좌표 보정이 어려워 오탐 위험이 커지므로 검사를 건너뛴다.
    """
    try:
        doc = minidom.parse(str(path))
    except Exception:  # noqa: BLE001
        return None
    svgs = doc.getElementsByTagName("svg")
    if not svgs:
        return None
    root = svgs[0]
    vb_y = 0.0
    vb_h = None
    vb = root.getAttribute("viewBox").strip()
    if vb:
        parts = re.split(r"[ ,]+", vb)
        if len(parts) == 4:
            parsed_y = _fnum_str(parts[1])
            if parsed_y is not None:
                vb_y = parsed_y
            vb_h = _fnum_str(parts[3])
    if vb_h is None:
        vb_h = _fnum(root, "height")
    if vb_h is None:
        return None
    min_top = None
    max_bottom = 0.0
    for el in doc.getElementsByTagName("*"):
        if el.getAttribute("transform"):
            return None  # 변환 좌표계 — 안전하게 검사 생략
        tag = el.tagName
        t = None
        b = None
        if tag == "text":
            # 텍스트는 베이스라인(y) 기준. 베이스라인이 캔버스를 벗어나야 실제 클리핑이다.
            # (베이스라인이 모서리에 걸친 정도는 어센더가 위로 그려져 시각적으로 멀쩡함)
            y = _fnum(el, "y")
            if y is not None:
                font_size = _fnum(el, "font-size", 16)
                t = y - font_size
                b = y
        elif tag == "rect":
            y, h = _fnum(el, "y"), _fnum(el, "height")
            if y is not None and h is not None:
                t = y
                b = y + h
        elif tag == "circle":
            cy, r = _fnum(el, "cy"), _fnum(el, "r")
            if cy is not None and r is not None:
                t = cy - r
                b = cy + r
        elif tag == "ellipse":
            cy, ry = _fnum(el, "cy"), _fnum(el, "ry")
            if cy is not None and ry is not None:
                t = cy - ry
                b = cy + ry
        elif tag == "line":
            ys = [v for v in (_fnum(el, "y1"), _fnum(el, "y2")) if v is not None]
            if ys:
                t = min(ys)
                b = max(ys)
        if t is not None and (min_top is None or t < min_top):
            min_top = t
        if b is not None and b > max_bottom:
            max_bottom = b
    if min_top is None:
        min_top = vb_y
    return vb_y, vb_h, min_top, max_bottom


def _fnum_str(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def markdown_heading_slug(text):
    """Astro/GitHub 계열 heading slug에 맞춘 간단한 Unicode 보존 정규화."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\{#[-\w가-힣]+\}\s*$", "", text)
    text = text.strip().lower()
    chars = []
    prev_sep = False
    for ch in text:
        if ch.isalnum():
            chars.append(ch)
            prev_sep = False
        elif ch.isspace() or ch in "-_":
            if chars and not prev_sep:
                chars.append("-")
                prev_sep = True
        else:
            continue
    return "".join(chars).strip("-")


def post_heading_slugs(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError:
        return set()
    _, body, _ = split_frontmatter(text)
    slugs = set()
    for _, line in iter_body_lines(body, 1):
        m = HEADING_RE.match(line)
        if m:
            slug = markdown_heading_slug(m.group(2))
            if slug:
                slugs.add(slug)
    return slugs


def check_internal_links(body, offset):
    out = []
    for i, line in enumerate(body.split("\n")):
        for m in BLOG_LINK_RE.finditer(line):
            slug = m.group(1)
            anchor = unquote(m.group(2) or "")
            target = POSTS_DIR / f"{slug}.md"
            if not target.exists():
                out.append(Finding(
                    REQUIRED, "D6", i + offset,
                    f"내부 링크 대상 없음: /blog/{slug}"
                ))
            elif anchor and anchor not in post_heading_slugs(target):
                out.append(Finding(
                    RECOMMENDED, "D6", i + offset,
                    f"내부 링크 앵커 없음: /blog/{slug}#{anchor} — target={target} anchor={anchor}"
                ))
    return out


def check_math_delims(body):
    stripped = _FENCE_RE.sub("", body)
    stripped = _INLINE_CODE_RE.sub("", stripped)
    stripped = stripped.replace(r"\$", "")  # 이스케이프된 달러는 제외
    out = []
    block = stripped.count("$$")
    if block % 2 != 0:
        out.append(Finding(RECOMMENDED, "D8", None, f"$$ 블록 구분자 짝이 안 맞음 ({block}개)"))
    inline = stripped.replace("$$", "").count("$")
    if inline % 2 != 0:
        out.append(Finding(RECOMMENDED, "D8", None, f"$ 인라인 수식 구분자 짝이 안 맞음 ({inline}개)"))
    return out


def iter_body_lines(body, offset):
    """(줄번호, 줄) 산출. ``` 코드펜스 내부는 건너뛴다. 줄번호는 1-indexed."""
    in_fence = False
    for i, line in enumerate(body.split("\n")):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield i + offset, line


def check_emoji(body, offset):
    """D9 — ✅/❌ 등 이모지 금지(O/X·텍스트 사용). 영구 규칙. 줄당 한 번 보고."""
    out = []
    for lineno, line in iter_body_lines(body, offset):
        found = []
        for ch in line:
            if ch == "️":  # 이형 선택자(U+FE0F) 단독은 표기에서 제외
                continue
            if (0x1F000 <= ord(ch) <= 0x1FAFF) or ch in _BANNED_EMOJI:
                if ch not in found:
                    found.append(ch)
        if found:
            chars = " ".join(f"'{c}'" for c in found)
            out.append(Finding(
                REQUIRED, "D9", lineno,
                f"이모지 사용: {chars} — ✅/❌ 등 이모지 대신 O/X·텍스트로"
            ))
    return out


def check_callout_order(body, offset):
    """D10 — 말미 callout 순서: '핵심 정리'(callout-key)가 '다음 포스트'보다 앞에 와야 한다."""
    callouts = []
    titles = list(CALLOUT_TITLE_RE.finditer(body))
    for om in CALLOUT_OPEN_RE.finditer(body):
        title = ""
        for tm in titles:
            if tm.start() > om.start():
                title = tm.group(1).strip()
                break
        lineno = body[:om.start()].count("\n") + offset
        callouts.append((lineno, om.group(1), title))
    key_pos = next((i for i, (_, c, _) in enumerate(callouts) if "callout-key" in c), None)
    next_pos = next((i for i, (_, _, t) in enumerate(callouts) if t == "다음 포스트"), None)
    if next_pos is not None and (key_pos is None or key_pos > next_pos):
        return [Finding(
            RECOMMENDED, "D10", callouts[next_pos][0],
            "callout 순서: '핵심 정리'(callout-key)가 '다음 포스트'보다 앞에 와야 함"
        )]
    return []


def check_math_block_lines(body, offset):
    """D11 — display 수식의 `$$`는 자체 줄에 둔다(텍스트와 같은 줄 금지). KaTeX display 인식용."""
    out = []
    for lineno, line in iter_body_lines(body, offset):
        line_without_code = _INLINE_CODE_RE.sub("", line)
        if "$$" not in line_without_code:
            continue
        s = line_without_code.strip()
        if s == "$$":
            continue  # 구분자만 단독으로 있는 줄 — OK
        out.append(Finding(
            REQUIRED, "D11", lineno,
            "`$$`가 텍스트와 같은 줄에 있음 — display 수식은 `$$`를 자체 줄에 둘 것"
        ))
    return out


def review_file(path):
    text = Path(path).read_text(encoding="utf-8")
    fm, body, offset = split_frontmatter(text)
    findings = []
    findings += check_frontmatter(fm)
    findings += check_broken_bold(body, offset)
    findings += check_emdash(body, path, offset)
    findings += check_emphasis(body)
    findings += check_assets(body, offset)
    findings += check_internal_links(body, offset)
    findings += check_series_links(path, body)
    findings += check_math_delims(body)
    findings += check_emoji(body, offset)
    findings += check_callout_order(body, offset)
    findings += check_math_block_lines(body, offset)
    return findings


def _location(path, finding):
    if finding.line:
        return f"{path}:{finding.line}"
    if finding.code == "D2" and "샘플 위치:" in finding.message:
        return finding.message.split("샘플 위치:", 1)[1].strip()
    return "not-recorded"


def _recommendation(finding):
    if "—" in finding.message:
        parts = finding.message.rsplit("—", 1)
        if len(parts) == 2 and parts[1].strip():
            return parts[1].strip()
    return "메시지에 따라 원문을 검토하고 필요한 경우 수정"


def severity_icon(severity):
    return SEVERITY_ICON.get(severity, str(severity).split()[0])


def gate_effect(severity):
    return GATE_EFFECT.get(severity, "warn")


def finding_to_report_v2(path, finding, quote=None):
    return {
        "severity": severity_icon(finding.severity),
        "source": "D",
        "rule_id": finding.code,
        "location": _location(path, finding),
        "quote": quote if quote is not None else _line_at(path, finding.line),
        "message": finding.message,
        "recommendation": _recommendation(finding),
        "gate_effect": gate_effect(finding.severity),
    }


def migrate_legacy_finding(text):
    m = re.search(r"\[(D\d+|L\d+)\]", text)
    rule_id = m.group(1) if m else "MIGRATED"
    severity = "🟡"
    effect = "warn"
    if "🔴" in text or "필수" in text:
        severity, effect = "🔴", "fail"
    elif "🟢" in text or "참고" in text:
        severity, effect = "🟢", "info"
    return {
        "schema_version": "review-report/v2",
        "severity": severity,
        "source": "MIGRATED",
        "rule_id": rule_id,
        "location": "not-recorded",
        "quote": "not-recorded",
        "message": text.strip(),
        "recommendation": "not-recorded",
        "gate_effect": effect,
    }


_REPORT_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
_LEGACY_BULLET_RE = re.compile(r"^- \[(D\d+|L\d+)\]\s+(.*)$")
_LEGACY_SECTION_RE = re.compile(r"^(🔴|🟡|🟢) (필수|권장|참고) \(\d+\)\s*$")
_LEGACY_SUBFIELD_RE = re.compile(r"^\s+- (quote|message|recommendation|location):\s*(.*)$")
_LEGACY_GATE_SPLIT_RE = re.compile(
    r"^(?P<loc>.*?)\s*·\s*gate:\s*(?P<gate>fail|warn|info)\b\s*(?:—\s*(?P<msg>.*))?$"
)
_HEADING_PREFIX_RE = re.compile(r"^(🔴|🟡|🟢)\s+\[(D\d+|L\d+)\]\s*(.*)$")
# 원본이 스스로 밝힌 심각도 총계. `요약(결정적):`처럼 일부만 센 줄은 제외한다.
_DECLARED_SUMMARY_RE = re.compile(
    r"^(?:요약|summary): (🔴 \d+ · 🟡 \d+ · 🟢 \d+)\s*$", re.MULTILINE
)
_SEVERITY_BY_GATE = {"fail": "🔴", "warn": "🟡", "info": "🟢"}
_GATE_BY_SEVERITY = {"🔴": "fail", "🟡": "warn", "🟢": "info"}


def report_identity(path):
    """파일명 `YYYY-MM-DD-<slug>.md`에서 날짜와 target을 읽는다."""
    match = _REPORT_NAME_RE.match(Path(path).stem)
    if not match:
        return rr.NOT_RECORDED, Path(path).stem
    return match.group(1), match.group(2)


def _split_legacy_bullet(rest):
    """`<위치> · gate: <효력> — <설명>` 꼴을 위치·효력·설명으로 가른다."""
    match = _LEGACY_GATE_SPLIT_RE.match(rest)
    if not match:
        return None, None, rest.strip()
    location = match.group("loc").strip().strip("`")
    return (location or None), match.group("gate"), (match.group("msg") or "").strip()


def heading_title(heading, location, rule_id):
    """`### ` 제목에서 위치 표기를 뺀 사람이 쓴 요약만 남긴다.

    제목이 `<심각도> [<규칙>] <위치>`뿐이면 살릴 요약이 없으므로 빈 문자열이다.
    """
    match = _HEADING_PREFIX_RE.match(heading or "")
    body = match.group(3).strip() if match else (heading or "").strip()
    if match and match.group(2) != rule_id:
        body = (heading or "").strip()
    if location and body.startswith(location):
        body = body[len(location):]
    return body.strip().lstrip("—-:").strip()


def _merge_title_into_message(row):
    """정본 헤딩에는 자리가 없는 설명형 제목을 message 앞으로 옮긴다."""
    title = heading_title(row.pop("_heading", ""), row.get("location"), row.get("rule_id"))
    message = (row.get("message") or "").strip()
    if title and title not in message:
        row["message"] = f"{title} — {message}" if message else title
    return row


def _legacy_rows(text):
    """레거시 산문 불릿을 v2 finding으로 옮긴다.

    심각도는 불릿 한 줄에만 있지 않다. 인라인 `gate:` 표시가 가장 정확하고,
    없으면 위쪽 섹션 제목(`🟢 참고 (9)`)이 그 불릿의 심각도다. 둘 다 없을 때만
    migrate_legacy_finding()의 문자열 휴리스틱에 맡긴다.

    불릿에 박힌 위치와 들여쓴 하위 `- quote:`/`- message:` 줄도 되살린다.
    확보할 수 있는 근거를 not-recorded로 버리지 않기 위해서다.
    """
    lines = text.splitlines()
    rows = []
    section_severity = None
    i = 0
    while i < len(lines):
        line = lines[i]
        section = _LEGACY_SECTION_RE.match(line)
        if section:
            section_severity = section.group(1)
            i += 1
            continue
        bullet = _LEGACY_BULLET_RE.match(line)
        if not bullet:
            i += 1
            continue

        rule_id, rest = bullet.group(1), bullet.group(2)
        location, gate, message = _split_legacy_bullet(rest)
        row = {
            "source": "MIGRATED",
            "rule_id": rule_id,
            "location": location or rr.NOT_RECORDED,
            "quote": rr.NOT_RECORDED,
            "message": message or rr.NOT_RECORDED,
            "recommendation": rr.NOT_RECORDED,
        }

        i += 1
        while i < len(lines):
            sub = _LEGACY_SUBFIELD_RE.match(lines[i])
            if not sub:
                break
            row[sub.group(1)] = sub.group(2).strip() or rr.NOT_RECORDED
            i += 1

        if gate:
            row["severity"], row["gate_effect"] = _SEVERITY_BY_GATE[gate], gate
        elif section_severity:
            row["severity"] = section_severity
            row["gate_effect"] = _GATE_BY_SEVERITY[section_severity]
        else:
            fallback = migrate_legacy_finding(line)
            row["severity"], row["gate_effect"] = fallback["severity"], fallback["gate_effect"]
        rows.append(row)
    return rows


def migrate_reports(report_paths):
    """과거 리포트를 v2 정본으로 전환한다. 없는 근거는 만들어 내지 않는다."""
    failed = False
    for report_path in report_paths:
        path = Path(report_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"리포트 읽기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue

        generated_at, target = report_identity(path)
        parsed = rr.parse_report(text)
        header = parsed["header"]
        complete = [f for f in parsed["findings"]
                    if all(field in f for field in rr.FINDING_FIELDS)]

        if complete:  # 부류 A: 근거를 그대로 보존한다
            findings = [_merge_title_into_message(f) for f in complete]
            migrated_from = None
        else:         # 부류 B: 손실 있는 전환임을 표시한다
            findings = _legacy_rows(text)
            migrated_from = "legacy-prose"

        if not findings:
            print(f"{path}: 마이그레이션할 finding이 없다", file=sys.stderr)
            failed = True
            continue

        # 과거 리포트는 손으로 쓴 형식이 제각각이라, 파서가 한 종류를 놓치면
        # finding이 조용히 사라진다. 원본이 밝힌 총계와 대조해 확인되지 않으면
        # 쓰지 않는다. 확인할 수 없는 전환은 하지 않는 편이 낫다.
        declared = _DECLARED_SUMMARY_RE.findall(text)
        computed = rr.format_summary(rr.summary_counts(findings))
        if not declared:
            print(f"{path}: 원본에 대조할 심각도 총계가 없어 전환하지 않는다", file=sys.stderr)
            failed = True
            continue
        if declared[-1] != computed:
            print(
                f"{path}: 심각도 총계 불일치 — 원본 [{declared[-1]}] 전환 [{computed}]. "
                "형식을 놓쳐 finding이 사라졌을 수 있어 전환하지 않는다",
                file=sys.stderr,
            )
            failed = True
            continue

        canonical = rr.serialize_report(
            target=header.get("target") or target,
            generated_at=header.get("generated_at") or generated_at,
            strict=header.get("strict") or rr.NOT_RECORDED,
            findings=findings,
            sources=header.get("sources", []),
            # 이미 전환된 리포트를 다시 돌려도 손실 표시가 사라지지 않아야 한다.
            migrated_from=migrated_from or header.get("migrated_from"),
        )
        errors = rr.validate_report(canonical, state="complete")
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            failed = True
            continue

        path.write_text(canonical, encoding="utf-8")
        print(f"마이그레이션 완료: {path}")
    return 2 if failed else 0


def _summary(findings):
    return rr.summary_counts([{"severity": severity_icon(f.severity)} for f in findings])


def _finding_sort_key(row):
    return rr.finding_sort_key(row)


def report_to_json_v2(paths, results, strict=False, generated_at=rr.NOT_RECORDED):
    posts = []
    all_findings = []
    all_rows = []
    for path, findings in results:
        rows = [finding_to_report_v2(path, f) for f in findings]
        rows.sort(key=_finding_sort_key)
        posts.append({
            "schema_version": "review-report/v2",
            "target": Path(path).stem,
            "generated_at": generated_at,
            "strict": strict,
            "summary": _summary(findings),
            "findings": rows,
        })
        all_findings.extend(findings)
        all_rows.extend(rows)
    all_rows.sort(key=_finding_sort_key)
    return {
        "schema_version": "review-report/v2",
        "posts": posts,
        "findings": all_rows,
        "aggregate": {
            "target": "all" if len(paths) != 1 else Path(paths[0]).stem,
            "summary": _summary(all_findings),
        },
    }


def format_report(path, findings):
    out = [f"## 결정적 검사: {path}"]
    if not findings:
        out.append("발견 사항 없음 ✅")
        return "\n".join(out)
    by_sev = {s: [f for f in findings if f.severity == s] for s in SEVERITY_ORDER}
    for s in SEVERITY_ORDER:
        fs = sorted(
            by_sev[s],
            key=lambda f: _finding_sort_key(finding_to_report_v2(path, f)),
        )
        if not fs:
            continue
        out.append(f"\n{s} ({len(fs)})")
        for f in fs:
            loc = _location(path, f)
            out.append(f"- [{f.code}] {loc}  {f.message}")
    summary = " · ".join(f"{s.split()[0]} {len(by_sev[s])}" for s in SEVERITY_ORDER)
    out.append("\n요약: " + summary)
    return "\n".join(out)


def has_required_findings(findings):
    return any(f.severity == REQUIRED for f in findings)


def report_path_for(output_dir, report_date, path):
    return Path(output_dir) / f"{report_date}-{Path(path).stem}.md"


def write_markdown_report(output_dir, report_date, path, findings, strict=False):
    out_path = report_path_for(output_dir, report_date, path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [finding_to_report_v2(path, f) for f in findings]
    out_path.write_text(
        rr.serialize_report(
            target=Path(path).stem,
            generated_at=report_date,
            strict=strict,
            findings=rows,
            sources=[str(path)],
        ),
        encoding="utf-8",
    )
    return out_path


def parse_args(argv):
    opts = {
        "json": False,
        "strict": False,
        "write_reports": False,
        "finalize": [],
        "migrate": [],
        "output_dir": None,
        "date": None,
        "paths": [],
        "errors": [],
    }
    args = list(argv[1:])
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--json":
            opts["json"] = True
        elif arg == "--strict":
            opts["strict"] = True
        elif arg == "--write-reports":
            opts["write_reports"] = True
        elif arg == "--finalize":
            if i + 1 < len(args):
                opts["finalize"].append(args[i + 1])
                i += 1
            else:
                opts["errors"].append("--finalize requires a value")
        elif arg == "--migrate":
            if i + 1 < len(args):
                opts["migrate"].append(args[i + 1])
                i += 1
            else:
                opts["errors"].append("--migrate requires a value")
        elif arg == "--output-dir":
            if i + 1 < len(args):
                opts["output_dir"] = args[i + 1]
                i += 1
            else:
                opts["errors"].append("--output-dir requires a value")
        elif arg == "--date":
            if i + 1 < len(args):
                opts["date"] = args[i + 1]
                i += 1
            else:
                opts["errors"].append("--date requires a value")
        else:
            opts["paths"].append(arg)
        i += 1
    return opts


def finalize_reports(report_paths):
    """LLM 비평 행이 추가된 리포트를 정본 형식으로 다시 직렬화한다.

    요약을 finding에서 다시 계산하고 정본 순서로 재정렬한다. 멱등이다.
    품질 gate 판정은 하지 않는다.
    """
    failed = False
    for report_path in report_paths:
        path = Path(report_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"리포트 읽기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue

        parsed = rr.parse_report(text)
        header = parsed["header"]
        canonical = rr.serialize_report(
            target=header.get("target", rr.NOT_RECORDED),
            generated_at=header.get("generated_at", rr.NOT_RECORDED),
            strict=header.get("strict", "false"),
            findings=parsed["findings"],
            sources=header.get("sources", []),
        )
        errors = rr.validate_report(canonical, state="complete")
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            failed = True
            continue

        try:
            path.write_text(canonical, encoding="utf-8")
        except OSError as e:
            print(f"리포트 쓰기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue
        print(f"정본화 완료: {path}")
    return 2 if failed else 0


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    opts = parse_args(argv)
    if opts["errors"]:
        for error in opts["errors"]:
            print(error, file=sys.stderr)
        return 2
    if opts["finalize"]:
        return finalize_reports(opts["finalize"])
    if opts["migrate"]:
        return migrate_reports(opts["migrate"])
    paths = opts["paths"]
    if not paths:
        return 0
    output_dir = opts["output_dir"] or "docs/reviews"
    report_date = opts["date"] or date.today().isoformat()
    reports = []
    written_report_paths = []
    results = []
    infra_failed = False
    required_failed = False
    for p in paths:
        try:
            findings = review_file(p)
        except OSError as e:
            infra_failed = True
            print(f"입력 파일 처리 실패: {p}: {e}", file=sys.stderr)
            if not opts["json"]:
                reports.append(f"## 결정적 검사: {p}\n파일을 읽을 수 없음")
            continue
        results.append((p, findings))
        if has_required_findings(findings):
            required_failed = True
        if not opts["json"]:
            report = format_report(p, findings)
            reports.append(report)
        if opts["write_reports"]:
            try:
                written_report_paths.append(
                    write_markdown_report(output_dir, report_date, p, findings, strict=opts["strict"])
                )
            except OSError as e:
                infra_failed = True
                print(f"리포트 쓰기 실패: {p}: {e}", file=sys.stderr)
    if opts["json"]:
        for path in written_report_paths:
            print(f"리포트 저장: {path}", file=sys.stderr)
        try:
            print(json.dumps(
                report_to_json_v2(paths, results, strict=opts["strict"], generated_at=report_date),
                ensure_ascii=False, indent=2,
            ))
        except (TypeError, ValueError) as e:
            print(f"JSON 렌더링 실패: {e}", file=sys.stderr)
            return 2
    else:
        reports.extend(f"리포트 저장: {path}" for path in written_report_paths)
        print("\n\n".join(reports))
    if infra_failed:
        return 2
    if opts["strict"] and required_failed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
