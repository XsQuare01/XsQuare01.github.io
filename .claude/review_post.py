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
from pathlib import Path

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
_FM_KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
# ](/blog/<slug>) 또는 ](/blog/<slug>#anchor) 의 slug 추출
BLOG_LINK_RE = re.compile(r"\]\(/blog/([^)\s#]+)")

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
    return out


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
                err = svg_error(asset)
                if err:
                    out.append(Finding(REQUIRED, "D4", i + offset, f"SVG 파싱 오류: {url} ({err})"))
                    continue
                # D13: 명백한 세로 클리핑만 잡는다. ">25px 여백" 같은 작법 권고는
                # 기존 코퍼스가 대부분 따르지 않아(타이트한 푸터 관행) 결정적 검사로는 오탐이 된다.
                ext = svg_bottom_extent(asset)
                if ext:
                    vb_h, mb = ext
                    if mb > vb_h + 2:
                        out.append(Finding(
                            REQUIRED, "D13", i + offset,
                            f"SVG 세로 클리핑: 최하단 요소 y≈{mb:.0f}이 viewBox 높이 {vb_h:.0f}를 넘어 잘림 — {url}"
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


def svg_bottom_extent(path):
    """(viewBox 높이, 요소 최하단 y)를 반환. 구하지 못하거나 transform이 있으면 None.

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
    vb_h = None
    vb = root.getAttribute("viewBox").strip()
    if vb:
        parts = re.split(r"[ ,]+", vb)
        if len(parts) == 4:
            vb_h = _fnum_str(parts[3])
    if vb_h is None:
        vb_h = _fnum(root, "height")
    if vb_h is None:
        return None
    max_bottom = 0.0
    for el in doc.getElementsByTagName("*"):
        if el.getAttribute("transform"):
            return None  # 변환 좌표계 — 안전하게 검사 생략
        tag = el.tagName
        b = None
        if tag == "text":
            # 텍스트는 베이스라인(y) 기준. 베이스라인이 캔버스를 벗어나야 실제 클리핑이다.
            # (베이스라인이 모서리에 걸친 정도는 어센더가 위로 그려져 시각적으로 멀쩡함)
            b = _fnum(el, "y")
        elif tag == "rect":
            y, h = _fnum(el, "y"), _fnum(el, "height")
            if y is not None and h is not None:
                b = y + h
        elif tag == "circle":
            cy, r = _fnum(el, "cy"), _fnum(el, "r")
            if cy is not None and r is not None:
                b = cy + r
        elif tag == "ellipse":
            cy, ry = _fnum(el, "cy"), _fnum(el, "ry")
            if cy is not None and ry is not None:
                b = cy + ry
        elif tag == "line":
            ys = [v for v in (_fnum(el, "y1"), _fnum(el, "y2")) if v is not None]
            if ys:
                b = max(ys)
        if b is not None and b > max_bottom:
            max_bottom = b
    return vb_h, max_bottom


def _fnum_str(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def check_internal_links(body, offset):
    out = []
    for i, line in enumerate(body.split("\n")):
        for m in BLOG_LINK_RE.finditer(line):
            slug = m.group(1)
            if not (POSTS_DIR / f"{slug}.md").exists():
                out.append(Finding(
                    RECOMMENDED, "D6", i + offset,
                    f"내부 링크 대상 없음: /blog/{slug}"
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
            REQUIRED, "D10", callouts[next_pos][0],
            "callout 순서: '핵심 정리'(callout-key)가 '다음 포스트'보다 앞에 와야 함"
        )]
    return []


def check_math_block_lines(body, offset):
    """D11 — display 수식의 `$$`는 자체 줄에 둔다(텍스트와 같은 줄 금지). KaTeX display 인식용."""
    out = []
    for lineno, line in iter_body_lines(body, offset):
        if "$$" not in line:
            continue
        s = line.strip()
        if s == "$$":
            continue  # 구분자만 단독으로 있는 줄 — OK
        if s.startswith("$$") and s.endswith("$$") and s.count("$$") == 2:
            continue  # 한 줄짜리 $$...$$ 단독 — 허용
        out.append(Finding(
            RECOMMENDED, "D11", lineno,
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


def _summary(findings):
    return {severity_icon(s): len([f for f in findings if f.severity == s]) for s in SEVERITY_ORDER}


def _finding_sort_key(row):
    sev_order = {"🔴": 0, "🟡": 1, "🟢": 2}
    source_order = {"D": 0, "L": 1, "MIGRATED": 2}
    loc = row["location"]
    file_part, line_part = loc, 0
    if ":" in loc:
        file_part, maybe_line = loc.rsplit(":", 1)
        if maybe_line.isdigit():
            line_part = int(maybe_line)
    return (
        sev_order.get(row["severity"], 99),
        source_order.get(row["source"], 99),
        row["rule_id"],
        file_part,
        line_part,
    )


def report_to_json_v2(paths, results, strict=False):
    posts = []
    all_findings = []
    all_rows = []
    for path, findings in results:
        rows = [finding_to_report_v2(path, f) for f in findings]
        rows.sort(key=_finding_sort_key)
        posts.append({
            "schema_version": "review-report/v2",
            "target": Path(path).stem,
            "generated_at": "not-recorded",
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
        fs = by_sev[s]
        if not fs:
            continue
        out.append(f"\n{s} ({len(fs)})")
        for f in fs:
            loc = _location(path, f)
            out.append(f"- [{f.code}] {loc}  {f.message}")
    summary = " · ".join(f"{s.split()[0]} {len(by_sev[s])}" for s in SEVERITY_ORDER)
    out.append("\n요약: " + summary)
    return "\n".join(out)


def parse_args(argv):
    opts = {
        "json": False,
        "strict": False,
        "write_reports": False,
        "output_dir": None,
        "date": None,
        "paths": [],
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
        elif arg == "--output-dir":
            if i + 1 < len(args):
                opts["output_dir"] = args[i + 1]
                i += 1
        elif arg == "--date":
            if i + 1 < len(args):
                opts["date"] = args[i + 1]
                i += 1
        else:
            opts["paths"].append(arg)
        i += 1
    return opts


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    opts = parse_args(argv)
    paths = opts["paths"]
    if not paths:
        return 0
    reports = []
    results = []
    for p in paths:
        try:
            findings = review_file(p)
        except FileNotFoundError:
            reports.append(f"## 결정적 검사: {p}\n파일을 찾을 수 없음")
            continue
        results.append((p, findings))
        if not opts["json"]:
            reports.append(format_report(p, findings))
    if opts["json"]:
        print(json.dumps(report_to_json_v2(paths, results, strict=opts["strict"]), ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(reports))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
