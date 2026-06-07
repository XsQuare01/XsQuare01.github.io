import contextlib
import io
import unittest
import tempfile
from pathlib import Path
import review_post as rp


def write_post(path, body="본문", frontmatter=None):
    if frontmatter is None:
        frontmatter = (
            'title: "Fixture Post"\n'
            "date: 2026-06-07T09:00:00\n"
            'description: "충분히 긴 설명으로 테스트 fixture의 frontmatter 계약을 만족한다."\n'
            'tags: ["test"]\n'
            "category: algorithm\n"
            "difficulty: 입문\n"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter}---\n{body}\n", encoding="utf-8")
    return path


def write_svg(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def run_main(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = rp.main(argv)
    return rc, buf.getvalue()


def run_main_streams(argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        rc = rp.main(argv)
    return rc, stdout.getvalue(), stderr.getvalue()


def codes(findings):
    return {f.code for f in findings}


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


class TestCliContractsV2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._pub, self._posts = rp.PUBLIC_DIR, rp.POSTS_DIR
        rp.PUBLIC_DIR = self.root / "public"
        rp.POSTS_DIR = self.root / "posts"
        rp.PUBLIC_DIR.mkdir(parents=True)
        rp.POSTS_DIR.mkdir(parents=True)

    def tearDown(self):
        rp.PUBLIC_DIR, rp.POSTS_DIR = self._pub, self._posts
        self.tmp.cleanup()

    def test_json_flag_writes_schema_v2_to_stdout_only(self):
        post = write_post(self.root / "posts" / "clean.md")

        rc, stdout = run_main(["review_post.py", "--json", str(post)])

        self.assertEqual(rc, 0)
        self.assertTrue(stdout.lstrip().startswith("{"), stdout)
        self.assertNotIn("## 결정적 검사", stdout)
        self.assertIn('"schema_version": "review-report/v2"', stdout)
        self.assertIn('"target": "clean"', stdout)

    def test_strict_exit_code_zero_when_only_warnings_exist(self):
        post = write_post(self.root / "posts" / "warn-only.md", "[없음](/blog/missing-anchorless) 링크")

        rc, stdout = run_main(["review_post.py", "--strict", str(post)])

        self.assertEqual(rc, 0, stdout)
        self.assertNotIn("--strict", stdout)

    def test_strict_exit_code_one_when_required_findings_exist(self):
        post = write_post(self.root / "posts" / "red.md", "트리가 **DAG)**가 된다")

        rc, stdout = run_main(["review_post.py", "--strict", str(post)])

        self.assertEqual(rc, 1, stdout)

    def test_strict_exit_code_two_for_missing_input(self):
        missing = self.root / "posts" / "missing.md"

        rc, stdout = run_main(["review_post.py", "--strict", str(missing)])

        self.assertEqual(rc, 2, stdout)

    def test_write_reports_uses_output_dir_and_date_for_each_target(self):
        first = write_post(self.root / "posts" / "alpha.md", "본문")
        second = write_post(self.root / "posts" / "beta.md", "트리가 **DAG)**가 된다")
        output_dir = self.root / "reports"

        rc, stdout = run_main([
            "review_post.py",
            "--write-reports",
            "--output-dir",
            str(output_dir),
            "--date",
            "2026-06-07",
            str(first),
            str(second),
        ])

        self.assertEqual(rc, 0, stdout)
        alpha_report = output_dir / "2026-06-07-alpha.md"
        beta_report = output_dir / "2026-06-07-beta.md"
        self.assertTrue(alpha_report.exists(), stdout)
        self.assertTrue(beta_report.exists(), stdout)
        self.assertIn("alpha.md", alpha_report.read_text(encoding="utf-8"))
        self.assertIn("[D1]", beta_report.read_text(encoding="utf-8"))
        self.assertFalse((Path("docs") / "reviews" / "2026-06-07-alpha.md").exists())

    def test_strict_multi_target_writes_reports_before_returning_failure(self):
        clean = write_post(self.root / "posts" / "clean.md", "본문")
        red = write_post(self.root / "posts" / "red.md", "트리가 **DAG)**가 된다")
        output_dir = self.root / "reports"

        rc, stdout = run_main([
            "review_post.py",
            "--strict",
            "--write-reports",
            "--output-dir",
            str(output_dir),
            "--date",
            "2026-06-07",
            str(clean),
            str(red),
        ])

        self.assertEqual(rc, 1, stdout)
        self.assertTrue((output_dir / "2026-06-07-clean.md").exists(), stdout)
        self.assertTrue((output_dir / "2026-06-07-red.md").exists(), stdout)

    def test_json_keeps_stdout_machine_readable_and_errors_on_stderr(self):
        valid = write_post(self.root / "posts" / "valid.md", "본문")
        missing = self.root / "posts" / "missing.md"

        rc, stdout, stderr = run_main_streams(["review_post.py", "--json", str(missing), str(valid)])

        self.assertEqual(rc, 2)
        self.assertTrue(stdout.lstrip().startswith("{"), stdout)
        self.assertNotIn("입력 파일 처리 실패", stdout)
        self.assertIn("입력 파일 처리 실패", stderr)


class TestDeterministicValidatorsV2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self._pub, self._posts = rp.PUBLIC_DIR, rp.POSTS_DIR
        rp.PUBLIC_DIR = self.root / "public"
        rp.POSTS_DIR = self.root / "posts"
        rp.PUBLIC_DIR.mkdir(parents=True)
        rp.POSTS_DIR.mkdir(parents=True)

    def tearDown(self):
        rp.PUBLIC_DIR, rp.POSTS_DIR = self._pub, self._posts
        self.tmp.cleanup()

    def test_frontmatter_category_and_difficulty_enum(self):
        valid = TestFrontmatter.FULL.replace("category: algorithm", "category: cryptography").replace("difficulty: 입문", "difficulty: 심화")
        invalid = TestFrontmatter.FULL.replace("category: algorithm", "category: math").replace("difficulty: 입문", "difficulty: beginner")

        self.assertEqual(rp.check_frontmatter(valid), [])
        out = rp.check_frontmatter(invalid)
        messages = "\n".join(f.message for f in out)
        self.assertIn("category", messages)
        self.assertIn("difficulty", messages)
        self.assertIn("enum", messages)

    def test_display_math_placement_flags_text_sharing_delimiter_line(self):
        invalid = "문장과 $$x=1$$ display math가 한 줄에 있음"
        valid = "문장\n$$\nx=1\n$$\n끝\n$$y=2$$"

        self.assertIn("D11", codes(rp.check_math_block_lines(invalid, 1)))
        self.assertEqual(rp.check_math_block_lines(valid, 1), [])

    def test_final_callout_order_requires_key_before_next_post(self):
        invalid = (
            '<div class="callout">\n<div class="callout-title">다음 포스트</div>\n</div>\n'
            '<div class="callout callout-key">\n<div class="callout-title">핵심 정리</div>\n</div>'
        )
        valid = (
            '<div class="callout callout-key">\n<div class="callout-title">핵심 정리</div>\n</div>\n'
            '<div class="callout">\n<div class="callout-title">다음 포스트</div>\n</div>'
        )

        self.assertIn("D10", codes(rp.check_callout_order(invalid, 1)))
        self.assertEqual(rp.check_callout_order(valid, 1), [])

    def test_internal_link_anchor_validation_including_korean_heading_anchor(self):
        prim = write_post(
            self.root / "posts" / "prim.md",
            "## 정확성 증명\n본문\n## English Heading\n본문",
        )
        self.assertTrue(prim.exists())

        valid = "[Prim 증명](/blog/prim#정확성-증명) 링크와 [영문](/blog/prim#english-heading) 링크"
        missing_anchor = "[없는 앵커](/blog/prim#missing-anchor) 링크"

        self.assertEqual(rp.check_internal_links(valid, 1), [])
        out = rp.check_internal_links(missing_anchor, 1)
        self.assertIn("D6", codes(out))
        self.assertIn("missing anchor", "\n".join(f.message for f in out))

    def test_svg_text_baseline_flags_clipped_top_edge(self):
        bad_svg = self.root / "public" / "images" / "x" / "baseline-bad.svg"
        good_svg = self.root / "public" / "images" / "x" / "baseline-good.svg"
        write_svg(bad_svg, '<svg viewBox="0 0 100 20"><text x="5" y="0">Label</text></svg>')
        write_svg(good_svg, '<svg viewBox="0 0 100 20"><text x="5" y="15">Label</text></svg>')

        self.assertIn("D13", codes(rp.check_assets("![x](/images/x/baseline-bad.svg)", 1)))
        self.assertEqual(rp.check_assets("![x](/images/x/baseline-good.svg)", 1), [])


class TestReportSchemaV2(unittest.TestCase):
    def test_migrated_report_schema_preserves_placeholders(self):
        self.assertTrue(hasattr(rp, "migrate_legacy_finding"), "migrated report schema helper is missing")
        migrated = rp.migrate_legacy_finding("- [D7] — legacy message")

        self.assertEqual(migrated["schema_version"], "review-report/v2")
        self.assertEqual(migrated["source"], "MIGRATED")
        self.assertEqual(migrated["location"], "not-recorded")
        self.assertEqual(migrated["quote"], "not-recorded")
        self.assertEqual(migrated["gate_effect"], "warn")

    def test_json_schema_contains_required_finding_fields(self):
        self.assertTrue(hasattr(rp, "finding_to_report_v2"), "review-report/v2 finding serializer is missing")
        finding = rp.Finding(rp.REQUIRED, "D1", 7, "깨진 굵게")

        row = rp.finding_to_report_v2("sample.md", finding, quote="트리가 **DAG)**가")

        self.assertEqual(set(row), {
            "severity",
            "source",
            "rule_id",
            "location",
            "quote",
            "message",
            "recommendation",
            "gate_effect",
        })
        self.assertEqual(row["severity"], "🔴")
        self.assertEqual(row["source"], "D")
        self.assertEqual(row["rule_id"], "D1")
        self.assertEqual(row["location"], "sample.md:7")
        self.assertEqual(row["gate_effect"], "fail")


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
