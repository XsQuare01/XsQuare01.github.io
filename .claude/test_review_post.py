import unittest
import tempfile
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
