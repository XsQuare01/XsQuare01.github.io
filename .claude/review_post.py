#!/usr/bin/env python3
"""블로그 포스트 결정적 리뷰 검사. 표준 라이브러리만 사용한다.

사용법: python review_post.py <파일.md> [<파일2.md> ...]
인자가 없으면 아무것도 출력하지 않고 0으로 종료한다.
"""
import sys
import re
import xml.dom.minidom as minidom
from collections import namedtuple
from pathlib import Path

# ---- 심각도 ----
REQUIRED = "🔴 필수"
RECOMMENDED = "🟡 권장"
INFO = "🟢 참고"
SEVERITY_ORDER = [REQUIRED, RECOMMENDED, INFO]

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


def check_emdash(body):
    count = body.count("—")
    line_count = max(1, len(body.split("\n")))
    threshold = max(EMDASH_MIN, round(line_count * EMDASH_RATIO))
    if count > threshold:
        return [Finding(
            RECOMMENDED, "D2", None,
            f"줄표(—) {count}회 — 임계치({threshold}) 초과. AI 문체 신호"
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


def check_assets(body, offset):
    return []


def check_internal_links(body, offset):
    return []


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


def review_file(path):
    text = Path(path).read_text(encoding="utf-8")
    fm, body, offset = split_frontmatter(text)
    findings = []
    findings += check_frontmatter(fm)
    findings += check_broken_bold(body, offset)
    findings += check_emdash(body)
    findings += check_emphasis(body)
    findings += check_assets(body, offset)
    findings += check_internal_links(body, offset)
    findings += check_math_delims(body)
    return findings


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
            loc = f"L{f.line}" if f.line else "—"
            out.append(f"- [{f.code}] {loc}  {f.message}")
    summary = " · ".join(f"{s.split()[0]} {len(by_sev[s])}" for s in SEVERITY_ORDER)
    out.append("\n요약: " + summary)
    return "\n".join(out)


def main(argv):
    paths = argv[1:]
    if not paths:
        return 0
    reports = []
    for p in paths:
        try:
            findings = review_file(p)
        except FileNotFoundError:
            reports.append(f"## 결정적 검사: {p}\n파일을 찾을 수 없음")
            continue
        reports.append(format_report(p, findings))
    print("\n\n".join(reports))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
