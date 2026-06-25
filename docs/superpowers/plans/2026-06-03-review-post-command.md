# `/review-post` 리뷰 커맨드 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 블로그 포스트의 내용·문체·SVG를 점검하는 온디맨드 리뷰 도구(`/review-post`, `/review-post-all`)를 만든다.

**Architecture:** 결정적 검사는 표준 라이브러리만 쓰는 Python 스크립트(`.claude/review_post.py`)가 담당하고, LLM 비평과 오케스트레이션은 두 개의 슬래시 커맨드(`.claude/commands/review-post.md`, `review-post-all.md`)가 담당한다. 커맨드가 스크립트를 호출해 결정적 결과를 받고, 본문·SVG를 읽어 비평을 더해 하나의 리포트로 출력한다.

**Tech Stack:** Python 3 표준 라이브러리(`re`, `pathlib`, `xml.dom.minidom`, `unittest`), Claude Code 프로젝트 슬래시 커맨드(마크다운). 외부 패키지 없음.

설계서: `docs/superpowers/specs/2026-06-03-review-post-command-design.md`

**테스트 실행 규약:** 테스트는 `.claude/test_review_post.py`에 두고 `python .claude/test_review_post.py -v`로 실행한다(레포 루트에서 실행 시 `.claude/`가 `sys.path[0]`이 되어 `import review_post`가 동작한다).

**스펙과의 차이 1건:** D6(내부 링크·앵커) 중 **앵커(`#...`) 검증은 v1에서 제외**한다. 사이트의 한글 제목 → heading id 슬러그 규칙이 렌더 결과로 확정되지 않아 거짓 양성 위험이 크다. v1은 `/blog/<slug>` 링크 대상 존재만 검사하고, 앵커 검증은 향후 확장으로 남긴다.

---

### Task 1: 스크립트 골격 (상수·frontmatter 분리·Finding·리포트·stub)

모듈이 처음부터 import 가능하도록, 모든 검사 함수를 `[]` 반환 stub으로 먼저 둔다. 이후 태스크에서 stub을 실제 구현으로 교체한다.

**Files:**
- Create: `.claude/review_post.py`
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 작성**

`.claude/test_review_post.py`:

```python
import unittest
import review_post as rp


class TestSkeleton(unittest.TestCase):
    def test_split_frontmatter(self):
        text = "---\ntitle: A\n---\n본문 첫 줄\n둘째 줄\n"
        fm, body, offset = rp.split_frontmatter(text)
        self.assertIn("title: A", fm)
        self.assertTrue(body.startswith("본문 첫 줄"))
        self.assertEqual(offset, 4)  # 본문 첫 줄은 원본 4번째 줄

    def test_split_frontmatter_none(self):
        fm, body, offset = rp.split_frontmatter("프론트매터 없음\n둘째")
        self.assertEqual(fm, "")
        self.assertEqual(offset, 1)

    def test_main_no_args_returns_zero(self):
        self.assertEqual(rp.main(["review_post.py"]), 0)

    def test_format_report_empty(self):
        report = rp.format_report("x.md", [])
        self.assertIn("발견 사항 없음", report)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'review_post'`

- [ ] **Step 3: 골격 구현**

`.claude/review_post.py`:

```python
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
    return []


def check_broken_bold(body, offset):
    return []


def check_emdash(body):
    return []


def check_emphasis(body):
    return []


def check_assets(body, offset):
    return []


def check_internal_links(body, offset):
    return []


def check_math_delims(body):
    return []


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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (4 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): 리뷰 스크립트 골격 + frontmatter 분리·리포트"
```

---

### Task 2: D1 깨진 굵게 검사

**Files:**
- Modify: `.claude/review_post.py` (`check_broken_bold` stub 교체, 상수 추가)
- Test: `.claude/test_review_post.py` (테스트 추가)

- [ ] **Step 1: 실패하는 테스트 추가**

`.claude/test_review_post.py`의 `if __name__` 위에 클래스 추가:

```python
class TestBrokenBold(unittest.TestCase):
    def test_detects_punct_then_bold_then_letter(self):
        body = "트리가 아니라 **DAG(방향)**가 된다"
        out = rp.check_broken_bold(body, 1)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D1")
        self.assertEqual(out[0].severity, rp.REQUIRED)

    def test_ok_when_space_after(self):
        body = "**DAG(방향)** 가 된다"
        self.assertEqual(rp.check_broken_bold(body, 1), [])

    def test_ok_plain_intraword(self):
        # 구두점 없이 글자만 붙은 경우는 CommonMark에서 정상 렌더 → 잡지 않음
        body = "도출된 정리는 **참**이다."
        self.assertEqual(rp.check_broken_bold(body, 1), [])

    def test_line_number_uses_offset(self):
        body = "첫 줄\n트리가 **DAG)**가"
        out = rp.check_broken_bold(body, 10)  # 본문이 원본 10번째 줄부터
        self.assertEqual(out[0].line, 11)
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_detects_...`에서 `len(out) == 0`

- [ ] **Step 3: 구현 (stub 교체 + 상수 추가)**

`review_post.py`의 `# ---- 경로 ----` 블록 아래에 추가:

```python
# 닫는 ** 앞이 구두점이고 바로 뒤가 글자/숫자/한글이면 굵게가 적용되지 않는다.
_CLOSE_PUNCT = ")].,!?:;'\"”’」』）}"
BROKEN_BOLD = re.compile(
    "[" + re.escape(_CLOSE_PUNCT) + r"]\*\*[0-9A-Za-z가-힣]"
)
```

`check_broken_bold` stub을 교체:

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (8 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D1 깨진 굵게 패턴 검사"
```

---

### Task 3: D2 줄표 남발 + D3 강조 과다

**Files:**
- Modify: `.claude/review_post.py` (`check_emdash`, `check_emphasis` stub 교체, 상수 추가)
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 추가**

```python
class TestStyleDensity(unittest.TestCase):
    def test_emdash_over_threshold(self):
        body = "\n".join(["줄 — 표"] * 10)  # 10개 줄표, 10줄
        out = rp.check_emdash(body)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D2")
        self.assertEqual(out[0].severity, rp.RECOMMENDED)

    def test_emdash_under_threshold(self):
        body = "줄표 하나 — 끝\n" + "보통 줄\n" * 50
        self.assertEqual(rp.check_emdash(body), [])

    def test_emphasis_dense(self):
        body = "\n".join(["**굵게**"] * 10)  # 10줄 모두 굵게
        out = rp.check_emphasis(body)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D3")
        self.assertEqual(out[0].severity, rp.INFO)

    def test_emphasis_sparse(self):
        body = "보통 문장\n" * 20 + "**한 번**만 강조\n"
        self.assertEqual(rp.check_emphasis(body), [])
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_emdash_over_threshold`에서 빈 리스트

- [ ] **Step 3: 구현**

`review_post.py` 상수 영역(`BROKEN_BOLD` 아래)에 추가:

```python
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*")
```

`check_emdash`, `check_emphasis` stub 교체:

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (12 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D2 줄표 남발·D3 강조 과다 검사"
```

---

### Task 4: D7 frontmatter 검사

**Files:**
- Modify: `.claude/review_post.py` (`check_frontmatter` stub 교체, 상수 추가)
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 추가**

```python
class TestFrontmatter(unittest.TestCase):
    FULL = (
        'title: "글 제목"\n'
        "date: 2026-06-03T09:00:00\n"
        'description: "' + ("설명 " * 15).strip() + '"\n'
        'tags: ["A"]\n'
        "category: algorithm\n"
        "difficulty: 입문\n"
    )

    def test_all_present(self):
        self.assertEqual(rp.check_frontmatter(self.FULL), [])

    def test_missing_key(self):
        fm = self.FULL.replace("category: algorithm\n", "")
        out = rp.check_frontmatter(fm)
        codes = [(f.code, f.message) for f in out]
        self.assertTrue(any("category" in m for _, m in codes))
        self.assertTrue(all(f.code == "D7" for f in out))

    def test_short_description(self):
        fm = self.FULL.replace(("설명 " * 15).strip(), "짧음")
        out = rp.check_frontmatter(fm)
        self.assertTrue(any("짧음" in f.message or "짧" in f.message for f in out))
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_missing_key`에서 빈 리스트

- [ ] **Step 3: 구현**

`review_post.py` 상수 영역에 추가:

```python
REQUIRED_KEYS = ["title", "date", "description", "tags", "category", "difficulty"]
_FM_KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")
```

`check_frontmatter` stub 교체:

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (15 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D7 frontmatter 누락·description 길이 검사"
```

---

### Task 5: D8 수식 구분자 짝 검사

**Files:**
- Modify: `.claude/review_post.py` (`check_math_delims` stub 교체, 상수 추가)
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 추가**

```python
class TestMathDelims(unittest.TestCase):
    def test_balanced(self):
        body = "인라인 $a+b$ 와 블록\n$$\nx=1\n$$\n끝"
        self.assertEqual(rp.check_math_delims(body), [])

    def test_odd_inline(self):
        body = "여기 $a+b 가 안 닫힘"
        out = rp.check_math_delims(body)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D8")

    def test_ignores_code_block(self):
        body = "```bash\necho $HOME $PATH\n```\n본문 $x$ 정상"
        self.assertEqual(rp.check_math_delims(body), [])

    def test_ignores_inline_code(self):
        body = "`$5` 와 `$10` 은 코드\n수식 $y$ 정상"
        self.assertEqual(rp.check_math_delims(body), [])
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_odd_inline`에서 빈 리스트

- [ ] **Step 3: 구현**

`review_post.py` 상수 영역에 추가:

```python
_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
```

`check_math_delims` stub 교체:

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (19 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D8 수식 구분자 짝 검사"
```

---

### Task 6: D4 SVG 유효성 + D5 에셋 경로 검사

파일시스템에 의존하므로, 테스트는 `rp.PUBLIC_DIR`를 임시 디렉터리로 바꿔치기한다.

**Files:**
- Modify: `.claude/review_post.py` (`check_assets` stub 교체, `svg_error`·`IMG_RE` 추가)
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 추가**

파일 상단 import에 `import tempfile`, `from pathlib import Path`를 추가하고(이미 unittest만 있으면 추가), 클래스 추가:

```python
import tempfile
from pathlib import Path


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._orig = rp.PUBLIC_DIR
        rp.PUBLIC_DIR = Path(self.tmp.name)

    def tearDown(self):
        rp.PUBLIC_DIR = self._orig
        self.tmp.cleanup()

    def _write(self, rel, content):
        p = Path(self.tmp.name) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    def test_missing_asset(self):
        body = "![alt](/images/x/none.svg)"
        out = rp.check_assets(body, 1)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D5")
        self.assertEqual(out[0].severity, rp.REQUIRED)

    def test_valid_svg(self):
        self._write("images/x/ok.svg", "<svg><rect/></svg>")
        body = "![alt](/images/x/ok.svg)"
        self.assertEqual(rp.check_assets(body, 1), [])

    def test_broken_svg(self):
        self._write("images/x/bad.svg", "<svg><rect></svg>")  # 닫히지 않은 태그
        body = "![alt](/images/x/bad.svg)"
        out = rp.check_assets(body, 1)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D4")

    def test_external_url_ignored(self):
        body = "![alt](https://example.com/a.png)"
        self.assertEqual(rp.check_assets(body, 1), [])
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_missing_asset`에서 빈 리스트

- [ ] **Step 3: 구현**

`review_post.py` 상수 영역에 추가:

```python
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
```

`svg_error` 함수와 `check_assets` 구현(stub 교체):

```python
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
    return out
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (23 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D4 SVG 유효성·D5 에셋 경로 검사"
```

---

### Task 7: D6 내부 링크 대상 존재 검사

**Files:**
- Modify: `.claude/review_post.py` (`check_internal_links` stub 교체, `BLOG_LINK_RE` 추가)
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: 실패하는 테스트 추가**

```python
class TestInternalLinks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._orig = rp.POSTS_DIR
        rp.POSTS_DIR = Path(self.tmp.name)
        (Path(self.tmp.name) / "prim.md").write_text("x", encoding="utf-8")

    def tearDown(self):
        rp.POSTS_DIR = self._orig
        self.tmp.cleanup()

    def test_existing_link_ok(self):
        body = "자세한 건 [Prim](/blog/prim) 참고"
        self.assertEqual(rp.check_internal_links(body, 1), [])

    def test_missing_link(self):
        body = "[없는 글](/blog/does-not-exist) 링크"
        out = rp.check_internal_links(body, 1)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].code, "D6")
        self.assertEqual(out[0].severity, rp.RECOMMENDED)

    def test_link_with_anchor_strips_anchor(self):
        # 앵커가 붙어도 slug(prim)만 보고 존재 판정 (앵커 자체는 v1에서 검증 안 함)
        body = "[Prim 증명](/blog/prim#정확성-증명)"
        self.assertEqual(rp.check_internal_links(body, 1), [])
```

- [ ] **Step 2: 실패 확인**

Run: `python .claude/test_review_post.py -v`
Expected: FAIL — `test_missing_link`에서 빈 리스트

- [ ] **Step 3: 구현**

`review_post.py` 상수 영역에 추가:

```python
# ](/blog/<slug>) 또는 ](/blog/<slug>#anchor) 의 slug 추출
BLOG_LINK_RE = re.compile(r"\]\(/blog/([^)\s#]+)")
```

`check_internal_links` stub 교체:

```python
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
```

- [ ] **Step 4: 통과 확인**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (27 tests)

- [ ] **Step 5: 커밋**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): D6 내부 링크 대상 존재 검사"
```

---

### Task 8: 통합 — review_file·format_report 다중 이슈 검증

모든 검사가 `review_file`을 통해 함께 동작하고 리포트가 심각도별로 묶이는지 확인한다.

**Files:**
- Test: `.claude/test_review_post.py` (통합 테스트 추가)
- (구현 변경 없음 — 골격의 `review_file`/`format_report`가 이미 모든 검사를 호출함)

- [ ] **Step 1: 통합 테스트 추가**

```python
class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._pub, self._posts = rp.PUBLIC_DIR, rp.POSTS_DIR
        rp.PUBLIC_DIR = self.root / "public"
        rp.POSTS_DIR = self.root / "posts"
        rp.POSTS_DIR.mkdir(parents=True)

    def tearDown(self):
        rp.PUBLIC_DIR, rp.POSTS_DIR = self._pub, self._posts
        self.tmp.cleanup()

    def test_multiple_issues_grouped(self):
        post = self.root / "posts" / "sample.md"
        post.write_text(
            "---\ntitle: T\n---\n"
            "트리가 **DAG)**가 된다\n"          # D1 (🔴)
            "![x](/images/none.svg)\n"           # D5 (🔴)
            "[없음](/blog/nope) 링크\n",          # D6 (🟡)
            encoding="utf-8",
        )
        findings = rp.review_file(str(post))
        codes = sorted({f.code for f in findings})
        self.assertEqual(codes, ["D1", "D5", "D6", "D7"])  # D7: tags 등 누락
        report = rp.format_report(str(post), findings)
        self.assertIn("🔴 필수", report)
        self.assertIn("🟡 권장", report)
        self.assertIn("요약:", report)
```

- [ ] **Step 2: 실행 (바로 통과해야 함)**

Run: `python .claude/test_review_post.py -v`
Expected: PASS (28 tests). 만약 실패하면 `review_file`이 해당 검사를 호출하는지 확인.

- [ ] **Step 3: 커밋**

```bash
git add .claude/test_review_post.py
git commit -m "test(review): 다중 이슈 통합 검증"
```

---

### Task 9: `/review-post` 슬래시 커맨드

**Files:**
- Create: `.claude/commands/review-post.md`

- [ ] **Step 1: 커맨드 파일 작성**

`.claude/commands/review-post.md`:

```markdown
---
description: main 대비 변경된 블로그 포스트의 내용·문체·SVG를 리뷰 (인자로 slug 지정 가능)
allowed-tools: Bash(git diff:*), Bash(python .claude/review_post.py:*), Read, Grep
---

# 블로그 포스트 리뷰 (변경분)

## 대상 선정
- 인자(`$ARGUMENTS`)가 있으면 `src/content/posts/<인자>.md` 하나만 대상으로 한다.
- 인자가 없으면 아래 두 결과를 합쳐 `src/content/posts/*.md`만 추린다.
  - `git diff --name-only main...HEAD`
  - `git diff --name-only`  (워킹트리 변경분)
- 대상이 하나도 없으면 "main 대비 변경된 포스트가 없습니다"라고 알리고 종료한다.

## 1단계 — 결정적 검사
대상 파일 경로들을 인자로 다음을 실행하고, 출력을 리포트에 그대로 포함한다.

`python .claude/review_post.py <대상 파일들>`

## 2단계 — LLM 비평
각 대상 포스트의 본문과, 본문이 참조하는 모든 SVG(`/images/...svg`)를 Read로 읽고 아래를 점검한다. 문제는 가능한 한 **파일:줄 위치와 인용 문장**으로 구체적으로 지적한다.

- **L1 문체(AI 신호):** 줄표(—) 남발, 경구식 섹션 마무리, 과한 비유·수사("형제처럼", "두 얼굴" 류), 대칭 문장 반복, 과한 굵게/기울임. → 줄표는 마침표·접속사로, 비유는 평이하게 고치라고 제안. 어체는 ~다 평서체 유지.
- **L2 설명 흐름·명료성:** 논리 도약, 빠진 전제, 너무 길어 끊어야 할 문장.
- **L3 용어·어체 일관성:** 같은 개념을 다른 말로 섞어 쓰는지(예: 노드/정점, 엣지/간선), 어체 통일.
- **L4 SVG ↔ 본문 일치:** SVG의 레이블·수치·캡션이 본문 예제/주장과 맞는지(예: 그래프 가중치, 거리 값).
- **L5 제목·description 적합성:** 제목과 frontmatter description이 실제 내용을 잘 대표하는지.

## 출력 형식
포스트별로 묶어, 결정적 검사 결과와 LLM 비평을 합친다. 각 항목은 심각도(🔴 필수 / 🟡 권장 / 🟢 참고)와 출처 코드(`[Dn]` 결정적 / `[Ln]` 비평), 그리고 `파일:줄` 위치를 붙인다. 마지막에 `요약: 🔴 n · 🟡 n · 🟢 n`.

**자동 수정은 하지 않는다.** 지적과 권고만 제시한다.
```

- [ ] **Step 2: 결정적 스크립트가 실제 포스트에서 도는지 확인**

Run: `python .claude/review_post.py src/content/posts/dijkstra-2.md`
Expected: `## 결정적 검사: ...` 리포트 출력. 현재 dijkstra-2는 정리된 상태이므로 🔴(D1/D4/D5) 0건이어야 한다.

- [ ] **Step 3: 커밋**

```bash
git add .claude/commands/review-post.md
git commit -m "feat(review): /review-post 슬래시 커맨드"
```

---

### Task 10: `/review-post-all` 슬래시 커맨드

**Files:**
- Create: `.claude/commands/review-post-all.md`

- [ ] **Step 1: 커맨드 파일 작성**

`.claude/commands/review-post-all.md`:

```markdown
---
description: 모든 블로그 포스트의 내용·문체·SVG를 리뷰
allowed-tools: Bash(python .claude/review_post.py:*), Read, Grep, Glob
---

# 블로그 포스트 리뷰 (전체)

## 대상 선정
`src/content/posts/*.md` 전체를 대상으로 한다. 글 수가 많으면 결정적 검사 리포트를 먼저 보이고, LLM 비평은 🔴/🟡가 있는 포스트부터 우선 다룬다.

## 1단계 — 결정적 검사
모든 대상 파일 경로를 인자로 다음을 실행하고, 출력을 리포트에 그대로 포함한다.

`python .claude/review_post.py src/content/posts/*.md`

## 2단계 — LLM 비평
각 포스트와 참조 SVG를 읽고, `/review-post` 커맨드와 **동일한 루브릭(L1~L5)** 으로 점검한다. (문체 AI 신호, 설명 흐름, 용어·어체 일관성, SVG↔본문 일치, 제목·description 적합성)

## 출력 형식
`/review-post`와 동일하다. 포스트별로 심각도·출처 코드·위치를 붙이고, 전체 요약을 마지막에 둔다. 자동 수정은 하지 않는다.
```

- [ ] **Step 2: 전체 실행이 도는지 확인**

Run: `python .claude/review_post.py src/content/posts/*.md`
Expected: 여러 포스트에 대한 결정적 검사 리포트가 차례로 출력된다(오류 없이 완주).

- [ ] **Step 3: 커밋**

```bash
git add .claude/commands/review-post-all.md
git commit -m "feat(review): /review-post-all 슬래시 커맨드"
```

---

### Task 11: 실제 포스트 검증 + 마무리

알려진 사례로 스크립트의 정확성을 점검한다.

**Files:**
- (코드 변경 없음 — 검증 전용. 문제 발견 시 해당 검사 태스크로 돌아가 수정)

- [ ] **Step 1: 깨진 굵게 회귀 확인 (현재는 0건이어야 함)**

Run: `python .claude/review_post.py src/content/posts/dijkstra-1.md src/content/posts/dijkstra-2.md`
Expected: 두 글 모두 D1(깨진 굵게) 0건. (이전 세션에서 `)**글자` 버그를 모두 수정했으므로.)

- [ ] **Step 2: 일부러 깨뜨린 임시 파일로 발화 확인**

```bash
printf '%s\n' '---' 'title: T' '---' '트리가 **DAG)**가 된다' '![x](/images/none.svg)' '수식 $a+b 안 닫힘' > /tmp/broken-post.md
python .claude/review_post.py /tmp/broken-post.md
```
Expected: D1(🔴), D5(🔴), D8(🟡), D7(🟡: tags/category 등 누락)이 리포트에 나타난다.

- [ ] **Step 3: 전체 테스트 최종 실행**

Run: `python .claude/test_review_post.py -v`
Expected: 전체 PASS (28 tests).

- [ ] **Step 4: 임시 파일 정리**

```bash
rm -f /tmp/broken-post.md
```

- [ ] **Step 5: 검증 사실을 설계서/계획에 반영할 게 있으면 메모 후 커밋 (없으면 생략)**

검증 중 임계치·정규식 조정이 필요했다면 해당 태스크에서 이미 수정·커밋됐을 것이다. 추가 변경이 없다면 이 태스크는 커밋 없이 종료한다.

---

## Self-Review (계획 작성자 체크)

- **스펙 커버리지:** 결정적 D1~D8 → Task 2/3/4/5/6/7(D6 앵커는 의도적 제외, 상단 명시). LLM L1~L5 → Task 9/10 커맨드 루브릭. 두 진입점(`/review-post`, `/review-post-all`) → Task 9/10. 출력 포맷(심각도·`[Dn/Ln]`·위치·요약) → Task 1 `format_report` + 커맨드. 검증 방법(스펙 §7) → Task 11.
- **플레이스홀더:** 모든 코드 스텝에 실제 코드 포함. TBD/TODO 없음.
- **타입·이름 일관성:** `Finding(severity, code, line, message)`, `check_*` 함수명, `PUBLIC_DIR`/`POSTS_DIR`/`REPO_ROOT`, 심각도 상수 `REQUIRED/RECOMMENDED/INFO`가 전 태스크에서 일관되게 사용됨. `review_file`이 7개 검사 함수를 모두 호출(Task 1에서 확정, 이후 stub만 교체).
