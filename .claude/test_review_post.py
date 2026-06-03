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


class TestStdoutEncoding(unittest.TestCase):
    def test_main_emits_emoji_without_crash(self):
        import io
        import contextlib
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            post = Path(d) / "p.md"
            # 깨진 굵게(D1, 🔴) → 보고서에 이모지·줄표 포함
            post.write_text("---\ntitle: T\n---\n트리가 **DAG)**가 된다\n", encoding="utf-8")
            # cp949 콘솔을 흉내 낸 stdout (이모지/em-dash 인코딩 불가)
            buf = io.TextIOWrapper(io.BytesIO(), encoding="cp949")
            with contextlib.redirect_stdout(buf):
                rc = rp.main(["review_post.py", str(post)])
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
