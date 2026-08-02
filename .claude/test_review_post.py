import contextlib
import io
import json
import re
import unittest
import tempfile
from pathlib import Path
import review_post as rp


REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEW_REPORT_DIR = REPO_ROOT / "docs" / "reviews"
COMMAND_DIR = REPO_ROOT / ".claude" / "commands"
REQUIRED_REPORT_FIELDS = {
    "severity",
    "source",
    "rule_id",
    "location",
    "quote",
    "message",
    "recommendation",
    "gate_effect",
}
SEVERITY_VALUES = {"🔴", "🟡", "🟢"}
SOURCE_VALUES = {"D", "L", "MIGRATED"}
GATE_EFFECT_VALUES = {"fail", "warn", "info"}


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


def assert_review_json_schema(testcase, payload, expected_post_count=None):
    testcase.assertEqual(payload["schema_version"], "review-report/v2")
    testcase.assertIn("posts", payload)
    testcase.assertIn("aggregate", payload)
    testcase.assertIn("findings", payload)
    testcase.assertIsInstance(payload["posts"], list)
    testcase.assertIsInstance(payload["findings"], list)
    if expected_post_count is not None:
        testcase.assertEqual(len(payload["posts"]), expected_post_count)

    for post in payload["posts"]:
        testcase.assertEqual(post["schema_version"], "review-report/v2")
        testcase.assertIn("target", post)
        testcase.assertIn("summary", post)
        testcase.assertIn("findings", post)
        testcase.assertIsInstance(post["findings"], list)
        for finding in post["findings"]:
            assert_finding_schema(testcase, finding)

    aggregate = payload["aggregate"]
    testcase.assertIn("target", aggregate)
    testcase.assertIn("summary", aggregate)
    testcase.assertEqual(set(aggregate["summary"]), {"🔴", "🟡", "🟢"})
    for finding in payload["findings"]:
        assert_finding_schema(testcase, finding)


def assert_finding_schema(testcase, finding):
    testcase.assertEqual(set(finding), REQUIRED_REPORT_FIELDS)
    testcase.assertIn(finding["severity"], SEVERITY_VALUES)
    testcase.assertIn(finding["source"], SOURCE_VALUES)
    testcase.assertTrue(finding["rule_id"], finding)
    testcase.assertTrue(finding["location"], finding)
    testcase.assertTrue(finding["quote"], finding)
    testcase.assertTrue(finding["message"], finding)
    testcase.assertTrue(finding["recommendation"], finding)
    testcase.assertIn(finding["gate_effect"], GATE_EFFECT_VALUES)


def parse_report_findings(markdown):
    findings = []
    current = None
    for line in markdown.splitlines():
        if line.startswith("### "):
            if current is not None:
                findings.append(current)
            current = {}
            continue
        if current is None or not line.startswith("- "):
            continue
        m = re.match(r"- (severity|source|rule_id|location|quote|message|recommendation|gate_effect):\s*(.*)$", line)
        if m:
            current[m.group(1)] = m.group(2).strip().strip("`")
    if current is not None:
        findings.append(current)
    return findings


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
        self._write("images/x/ok.svg", '<svg viewBox="0 0 10 10" width="10" height="10"><rect/></svg>')
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
        self.assertEqual(out[0].severity, rp.REQUIRED)
        self.assertIn("/blog/does-not-exist", out[0].message)

    def test_link_with_existing_anchor_ok(self):
        (Path(self.tmp.name) / "prim.md").write_text("## 정확성 증명\n", encoding="utf-8")
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
            "[없음](/blog/nope) 링크\n",          # D6 (🔴)
            encoding="utf-8",
        )
        findings = rp.review_file(str(post))
        codes = sorted({f.code for f in findings})
        self.assertEqual(codes, ["D1", "D5", "D6", "D7"])  # D7: tags 등 누락
        report = rp.format_report(str(post), findings)
        self.assertIn("🔴 필수", report)
        self.assertIn("🟡 권장", report)
        self.assertIn("요약:", report)

    def test_format_report_sorts_each_severity_group_by_stable_key(self):
        post = self.root / "posts" / "stable.md"
        findings = [
            rp.Finding(rp.INFO, "D3", None, "굵게 강조가 잦음"),
            rp.Finding(rp.REQUIRED, "D7", None, "frontmatter 누락: tags"),
            rp.Finding(rp.REQUIRED, "D1", 20, "깨진 굵게 늦은 줄"),
            rp.Finding(rp.REQUIRED, "D5", 4, "에셋 없음"),
            rp.Finding(rp.REQUIRED, "D1", 3, "깨진 굵게 이른 줄"),
            rp.Finding(rp.RECOMMENDED, "D2", None, "줄표 과다"),
        ]

        report = rp.format_report(str(post), findings)
        finding_lines = [line for line in report.splitlines() if line.startswith("- [")]

        self.assertEqual(
            [line.split("]", 1)[0] + "]" for line in finding_lines],
            ["- [D1]", "- [D1]", "- [D5]", "- [D7]", "- [D2]", "- [D3]"],
        )
        self.assertIn(f"{post}:3", finding_lines[0])
        self.assertIn(f"{post}:20", finding_lines[1])


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

    def test_strict_exit_code_one_when_missing_internal_slug_exists(self):
        post = write_post(self.root / "posts" / "missing-slug.md", "[없음](/blog/missing-anchorless) 링크")

        rc, stdout = run_main(["review_post.py", "--strict", str(post)])

        self.assertEqual(rc, 1, stdout)
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
        self.assertIn(str(alpha_report), stdout)
        self.assertIn(str(beta_report), stdout)
        self.assertFalse((Path("docs") / "reviews" / "2026-06-07-alpha.md").exists())

    def test_scaffold_output_is_canonical_and_validates_as_scaffold(self):
        import review_report as rr

        post = write_post(self.root / "posts" / "beta.md", "트리가 **DAG)**가 된다")
        output_dir = self.root / "reports"

        rc, _ = run_main([
            "review_post.py", "--write-reports",
            "--output-dir", str(output_dir),
            "--date", "2026-06-07", str(post),
        ])

        self.assertEqual(rc, 0)
        text = (output_dir / "2026-06-07-beta.md").read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text, state="scaffold"), [])
        self.assertEqual(text.splitlines()[0], "schema_version: review-report/v2")
        # 이 fixture는 D1(🔴 깨진 굵게)과 D3(🟢 굵게 강조 밀도)을 함께 낸다.
        self.assertIn("summary: 🔴 1 · 🟡 0 · 🟢 1", text)
        self.assertIn("- gate_effect: fail", text)
        self.assertNotIn("- **severity**:", text)

    def test_scaffold_rewrite_is_deterministic_for_same_input(self):
        post = write_post(self.root / "posts" / "beta.md", "트리가 **DAG)**가 된다")
        output_dir = self.root / "reports"
        argv = ["review_post.py", "--write-reports", "--output-dir", str(output_dir),
                "--date", "2026-06-07", str(post)]

        run_main(argv)
        first = (output_dir / "2026-06-07-beta.md").read_text(encoding="utf-8")
        run_main(argv)
        second = (output_dir / "2026-06-07-beta.md").read_text(encoding="utf-8")

        self.assertEqual(first, second)

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

    def _write_report_with_llm_rows(self):
        import review_report as rr

        report = self.root / "reports" / "2026-06-07-beta.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        scaffold = rr.serialize_report(
            target="beta", generated_at="2026-06-07", strict=False,
            findings=[{
                "severity": "🔴", "source": "D", "rule_id": "D1",
                "location": "src/content/posts/beta.md:7", "quote": "트리가 **DAG)**가",
                "message": "깨진 굵게", "recommendation": "구두점을 옮긴다",
                "gate_effect": "fail",
            }],
            sources=["src/content/posts/beta.md"],
        )
        llm_block = (
            "\n### 🟡 [L1] src/content/posts/beta.md:12\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L1\n"
            "- location: src/content/posts/beta.md:12\n"
            "- quote: 줄표가 남발된다\n- message: 줄표 남발\n"
            "- recommendation: 마침표로 끊는다\n- gate_effect: warn\n"
        )
        report.write_text(scaffold + llm_block, encoding="utf-8")
        return report

    def test_finalize_recomputes_summary_from_all_findings(self):
        report = self._write_report_with_llm_rows()

        rc, stdout = run_main(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertIn("summary: 🔴 1 · 🟡 1 · 🟢 0", text)

    def test_finalize_reorders_findings_canonically(self):
        report = self._write_report_with_llm_rows()

        run_main(["review_post.py", "--finalize", str(report)])

        headings = [l for l in report.read_text(encoding="utf-8").splitlines()
                    if l.startswith("### ")]
        self.assertEqual(headings, [
            "### 🔴 [D1] src/content/posts/beta.md:7",
            "### 🟡 [L1] src/content/posts/beta.md:12",
        ])

    def test_finalize_is_idempotent(self):
        report = self._write_report_with_llm_rows()

        run_main(["review_post.py", "--finalize", str(report)])
        first = report.read_text(encoding="utf-8")
        run_main(["review_post.py", "--finalize", str(report)])
        second = report.read_text(encoding="utf-8")

        self.assertEqual(first, second)

    def test_finalize_returns_two_when_report_has_no_findings(self):
        import review_report as rr

        report = self.root / "reports" / "2026-06-07-empty.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            rr.serialize_report(target="empty", generated_at="2026-06-07",
                                strict=False, findings=[]),
            encoding="utf-8",
        )

        rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("finding", stderr)

    def test_finalize_returns_two_for_missing_file(self):
        rc, _, stderr = run_main_streams([
            "review_post.py", "--finalize", str(self.root / "nope.md"),
        ])

        self.assertEqual(rc, 2)

    def test_json_keeps_stdout_machine_readable_and_errors_on_stderr(self):
        valid = write_post(self.root / "posts" / "valid.md", "본문")
        missing = self.root / "posts" / "missing.md"

        rc, stdout, stderr = run_main_streams(["review_post.py", "--json", str(missing), str(valid)])

        self.assertEqual(rc, 2)
        self.assertTrue(stdout.lstrip().startswith("{"), stdout)
        self.assertNotIn("입력 파일 처리 실패", stdout)
        self.assertIn("입력 파일 처리 실패", stderr)

    def test_json_write_reports_keeps_stdout_json_only_and_prints_paths_to_stderr(self):
        post = write_post(self.root / "posts" / "json-report.md", "본문")
        output_dir = self.root / "reports"

        rc, stdout, stderr = run_main_streams([
            "review_post.py",
            "--json",
            "--write-reports",
            "--output-dir",
            str(output_dir),
            "--date",
            "2026-06-07",
            str(post),
        ])

        self.assertEqual(rc, 0, stderr)
        payload = json.loads(stdout)
        assert_review_json_schema(self, payload, expected_post_count=1)
        report_path = output_dir / "2026-06-07-json-report.md"
        self.assertTrue(report_path.exists(), stderr)
        self.assertNotIn(str(report_path), stdout)
        self.assertIn(str(report_path), stderr)


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
        self.assertTrue(all(f.severity == rp.REQUIRED for f in out))

    def test_display_math_placement_flags_text_sharing_delimiter_line(self):
        invalid = "문장과 $$x=1$$ display math가 한 줄에 있음"
        valid = "문장\n$$\nx=1\n$$\n끝\n인라인 $x$ 정상"

        out = rp.check_math_block_lines(invalid, 1)
        self.assertIn("D11", codes(out))
        self.assertTrue(all(f.severity == rp.REQUIRED for f in out))
        self.assertEqual(rp.check_math_block_lines(valid, 1), [])

    def test_display_math_placement_ignores_code_fences_and_inline_code(self):
        body = "```md\n문장 $$x=1$$\n```\n인라인 코드 `$$x=1$$` 는 무시\n본문 $x$ 정상"

        self.assertEqual(rp.check_math_block_lines(body, 1), [])

    def test_final_callout_order_requires_key_before_next_post(self):
        invalid = (
            '<div class="callout">\n<div class="callout-title">다음 포스트</div>\n</div>\n'
            '<div class="callout callout-key">\n<div class="callout-title">핵심 정리</div>\n</div>'
        )
        valid = (
            '<div class="callout callout-key">\n<div class="callout-title">핵심 정리</div>\n</div>\n'
            '<div class="callout">\n<div class="callout-title">다음 포스트</div>\n</div>'
        )

        out = rp.check_callout_order(invalid, 1)
        self.assertIn("D10", codes(out))
        self.assertTrue(all(f.severity == rp.RECOMMENDED for f in out))
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
        self.assertEqual(out[0].severity, rp.RECOMMENDED)
        self.assertEqual(out[0].line, 1)
        self.assertIn("/blog/prim#missing-anchor", out[0].message)
        self.assertIn(str(self.root / "posts" / "prim.md"), out[0].message)
        self.assertIn("anchor=missing-anchor", out[0].message)

    def test_markdown_heading_slug_preserves_korean_and_normalizes_spacing(self):
        self.assertEqual(rp.markdown_heading_slug("정확성 증명"), "정확성-증명")
        self.assertEqual(rp.markdown_heading_slug("English Heading!"), "english-heading")

    def test_svg_text_baseline_flags_clipped_top_edge(self):
        bad_svg = self.root / "public" / "images" / "x" / "baseline-bad.svg"
        good_svg = self.root / "public" / "images" / "x" / "baseline-good.svg"
        write_svg(bad_svg, '<svg viewBox="0 0 100 20" width="100" height="20"><text x="5" y="0">Label</text></svg>')
        write_svg(good_svg, '<svg viewBox="0 0 100 20" width="100" height="20"><text x="5" y="15">Label</text></svg>')

        self.assertIn("D13", codes(rp.check_assets("![x](/images/x/baseline-bad.svg)", 1)))
        self.assertEqual(rp.check_assets("![x](/images/x/baseline-good.svg)", 1), [])

    def test_svg_structural_baseline_flags_viewbox_dimensions_and_root(self):
        missing_viewbox = self.root / "public" / "images" / "x" / "missing-viewbox.svg"
        missing_size = self.root / "public" / "images" / "x" / "missing-size.svg"
        negative_viewbox = self.root / "public" / "images" / "x" / "negative-viewbox.svg"
        wrong_root = self.root / "public" / "images" / "x" / "wrong-root.svg"
        write_svg(missing_viewbox, '<svg width="100" height="20"><text>Label</text></svg>')
        write_svg(missing_size, '<svg viewBox="0 0 100 20"><text>Label</text></svg>')
        write_svg(negative_viewbox, '<svg viewBox="0 0 -100 20" width="100" height="20"><text>Label</text></svg>')
        write_svg(wrong_root, '<html><svg viewBox="0 0 100 20" width="100" height="20"/></html>')

        messages = []
        for name in ("missing-viewbox", "missing-size", "negative-viewbox", "wrong-root"):
            out = rp.check_assets(f"![x](/images/x/{name}.svg)", 1)
            self.assertIn("D4", codes(out), name)
            messages.extend(f.message for f in out)
        joined = "\n".join(messages)
        self.assertIn("viewBox 누락", joined)
        self.assertIn("width/height 누락", joined)
        self.assertIn("viewBox 크기 음수", joined)
        self.assertIn("root <svg> 아님", joined)

    def test_svg_text_labels_extractable_for_llm_support(self):
        svg = self.root / "public" / "images" / "x" / "labels.svg"
        write_svg(svg, '<svg viewBox="0 0 100 20" width="100" height="20"><text>시작</text><text>End</text></svg>')

        self.assertEqual(rp.extract_svg_text_labels(svg), ["시작", "End"])


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

    def test_all_existing_review_reports_conform_to_v2_schema(self):
        reports = sorted(
            path for path in REVIEW_REPORT_DIR.glob("*.md")
            if path.name != "README.md"
        )
        self.assertTrue(reports, "expected at least one stored review report")

        for report in reports:
            with self.subTest(report=report.name):
                text = report.read_text(encoding="utf-8")
                self.assertIn("schema_version: review-report/v2", text)
                self.assertRegex(text, r"(?m)^target: .+", report.name)
                self.assertRegex(text, r"(?m)^generated_at: .+", report.name)
                self.assertRegex(text, r"(?m)^strict: .+", report.name)
                self.assertRegex(text, r"(?m)^summary: 🔴 \d+ · 🟡 \d+ · 🟢 \d+", report.name)
                self.assertIn("## Findings", text)
                findings = parse_report_findings(text)
                self.assertTrue(findings, f"{report.name} has no parsed findings")
                for finding in findings:
                    self.assertEqual(set(finding), REQUIRED_REPORT_FIELDS, finding)
                    self.assertIn(finding["severity"], SEVERITY_VALUES)
                    self.assertIn(finding["source"], SOURCE_VALUES)
                    self.assertIn(finding["gate_effect"], GATE_EFFECT_VALUES)

    def test_review_reports_readme_is_documentation_not_report_artifact(self):
        readme = REVIEW_REPORT_DIR / "README.md"

        self.assertTrue(readme.exists())
        self.assertEqual(
            [p.name for p in REVIEW_REPORT_DIR.glob("*.md") if p.name == "README.md"],
            ["README.md"],
        )
        self.assertNotIn("## Findings", readme.read_text(encoding="utf-8"))

    def test_generated_json_schema_contains_required_top_level_and_finding_fields(self):
        post = REPO_ROOT / "src" / "content" / "posts" / "dijkstra-2.md"

        rc, stdout = run_main(["review_post.py", "--json", str(post)])

        self.assertEqual(rc, 0, stdout)
        payload = json.loads(stdout)
        assert_review_json_schema(self, payload, expected_post_count=1)
        self.assertEqual(payload["aggregate"]["target"], "dijkstra-2")

    def test_multi_target_json_aggregate_uses_all_target_and_combines_findings(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            old_public, old_posts = rp.PUBLIC_DIR, rp.POSTS_DIR
            try:
                rp.PUBLIC_DIR = root / "public"
                rp.POSTS_DIR = root / "posts"
                rp.PUBLIC_DIR.mkdir(parents=True)
                rp.POSTS_DIR.mkdir(parents=True)
                clean = write_post(root / "posts" / "clean.md", "본문")
                red = write_post(root / "posts" / "red.md", "트리가 **DAG)**가 된다\n" + "보통 문장\n" * 4)

                rc, stdout = run_main(["review_post.py", "--json", str(clean), str(red)])
            finally:
                rp.PUBLIC_DIR, rp.POSTS_DIR = old_public, old_posts

        self.assertEqual(rc, 0, stdout)
        payload = json.loads(stdout)
        assert_review_json_schema(self, payload, expected_post_count=2)
        self.assertEqual(payload["aggregate"]["target"], "all")
        self.assertEqual(payload["aggregate"]["summary"], {"🔴": 1, "🟡": 0, "🟢": 0})
        self.assertEqual([post["target"] for post in payload["posts"]], ["clean", "red"])
        self.assertEqual(payload["posts"][0]["summary"], {"🔴": 0, "🟡": 0, "🟢": 0})
        self.assertEqual(payload["posts"][1]["summary"], {"🔴": 1, "🟡": 0, "🟢": 0})
        self.assertEqual([finding["rule_id"] for finding in payload["findings"]], ["D1"])

    def test_command_docs_include_required_storage_and_tool_contract(self):
        required_terms = [
            "allowed-tools: Write, Edit",
            "--write-reports",
            "docs/reviews/",
            "review-report/v2",
            "canonical fields",
            "Write/Edit",
            "저장",
            "검토 완료, 이슈 없음",
        ]

        for command_name in ("review-post.md", "review-post-all.md"):
            with self.subTest(command=command_name):
                text = (COMMAND_DIR / command_name).read_text(encoding="utf-8")
                for term in required_terms:
                    self.assertIn(term, text)
                for field in REQUIRED_REPORT_FIELDS:
                    self.assertIn(f"`{field}`", text)


class TestAuthoringGuideContracts(unittest.TestCase):
    def test_agents_and_review_commands_share_canonical_authority_and_ownership(self):
        agents_text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for term in (
            "`docs/writing-rules.md`",
            "핵심 줄기",
            "증명/논증 흐름",
            "의도한 주장",
        ):
            self.assertIn(term, agents_text)

        required_command_terms = (
            "## 작성 가이드와 책임 경계",
            "docs/writing-rules.md",
            "AGENTS.md",
            "작성자는 구조·문체·provenance 분류와 검증 근거 준비를 맡는다.",
            "리뷰어는 원문 충실성·사실 및 기술 정확성·증명 타당성을 판정한다.",
        )
        responsibility_sections = []
        for command_name in ("review-post.md", "review-post-all.md"):
            with self.subTest(command=command_name):
                text = (COMMAND_DIR / command_name).read_text(encoding="utf-8")
                for term in required_command_terms:
                    self.assertIn(term, text)
                section = text.split("## 작성 가이드와 책임 경계", 1)[1].split("\n## ", 1)[0]
                responsibility_sections.append(section)

        self.assertEqual(responsibility_sections[0], responsibility_sections[1])

    def test_canonical_guide_has_six_stages_in_order(self):
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        stage_headings = [
            "### 1. 원문 확인",
            "### 2. 글 설계",
            "### 3. 초안",
            "### 4. 기술 검증 준비",
            "### 5. 문장 퇴고",
            "### 6. 리뷰 인계",
        ]
        actual_stage_headings = []
        in_fence = False

        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            elif not in_fence and re.fullmatch(r"### [1-6]\. .+", line):
                actual_stage_headings.append(line)

        self.assertEqual(actual_stage_headings, stage_headings)

    def test_canonical_guide_preserves_sentence_rules_and_sources(self):
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        required_terms = [
            "접속어 최소화",
            "grep -oE",
            "George Orwell",
            "William Strunk Jr.",
            "William Zinsser",
            "Joan Didion",
            "Kurt Vonnegut",
        ]

        for term in required_terms:
            self.assertIn(term, text)

    def test_canonical_guide_has_three_annotated_examples_and_split_policy(self):
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        annotation_counts = {
            "**결함:**": 0,
            "**수정 후**": 0,
            "**개선 이유:**": 0,
        }
        in_fence = False

        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            elif not in_fence:
                for annotation in annotation_counts:
                    if line == annotation:
                        annotation_counts[annotation] += 1

        self.assertEqual(
            annotation_counts,
            {"**결함:**": 3, "**수정 후**": 3, "**개선 이유:**": 3},
        )
        for term in (
            "개념 설명 문단",
            "증명 진행 문단",
            "코드 및 예시 설명 문단",
            "독립된 질문",
            "고정 템플릿을 요구하지 않는다",
        ):
            self.assertIn(term, text)


class TestLegacyMigration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, text):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_class_a_bold_fields_are_reformatted_without_losing_evidence(self):
        import review_report as rr

        report = self._write("2026-07-28-karatsuba.md", (
            "## LLM 비평: src/content/posts/karatsuba.md\n\n"
            "## Findings\n\n"
            "### 🟡 [L4] src/content/posts/karatsuba.md:73\n\n"
            "- **severity**: 🟡\n- **source**: L\n- **rule_id**: L4\n"
            "- **location**: `src/content/posts/karatsuba.md:73`\n"
            "- **quote**: 서로 겹치지 않고\n"
            "- **message**: 본문과 SVG가 어긋난다\n"
            "- **recommendation**: 문장을 고친다\n"
            "- **gate_effect**: warn\n"
        ))

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text), [])
        self.assertIn("- source: L", text)
        self.assertNotIn("- **severity**:", text)
        self.assertIn("- quote: 서로 겹치지 않고", text)
        self.assertIn("generated_at: 2026-07-28", text)
        self.assertIn("target: karatsuba", text)
        self.assertNotIn("migrated_from:", text)

    def test_class_b_legacy_prose_uses_migrated_source_and_placeholders(self):
        import review_report as rr

        report = self._write("2026-07-24-dp-1.md", (
            "## 결정적 검사: src/content/posts/dp-1.md\n발견 사항 없음 ✅\n\n"
            "🟢 참고 (2)\n\n"
            "- [L6] not-recorded · gate: info — 노션 원본과 대조했다.\n"
            "- [L7] not-recorded · gate: info — 지수 범위 증명을 검증했다.\n\n"
            "요약: 🔴 0 · 🟡 0 · 🟢 2\n"
        ))

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text), [])
        self.assertIn("migrated_from: legacy-prose", text)
        self.assertIn("- source: MIGRATED", text)
        self.assertIn("- quote: not-recorded", text)
        self.assertIn("- location: not-recorded", text)
        self.assertIn("target: dp-1", text)
        self.assertIn("strict: not-recorded", text)
        parsed = rr.parse_report(text)
        self.assertEqual([f["rule_id"] for f in parsed["findings"]], ["L6", "L7"])

    def test_legacy_severity_comes_from_section_heading_not_default(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🔴 필수 (1)\n\n- [D7] frontmatter enum 불일치\n\n"
            "🟢 참고 (1)\n\n- [L6] 노션 원본과 대조했다.\n\n"
            "요약: 🔴 1 · 🟡 0 · 🟢 1\n"
        ))

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertIn("summary: 🔴 1 · 🟡 0 · 🟢 1", text)
        self.assertIn("### 🔴 [D7] not-recorded", text)
        self.assertIn("### 🟢 [L6] not-recorded", text)
        self.assertIn("- gate_effect: fail", text)
        self.assertIn("- gate_effect: info", text)

    def test_inline_gate_marker_wins_over_section_heading(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟡 권장 (1)\n\n- [L7] not-recorded · gate: info — 검증 기록이다.\n"
        ))

        run_main(["review_post.py", "--migrate", str(report)])

        text = report.read_text(encoding="utf-8")
        self.assertIn("- severity: 🟢", text)
        self.assertIn("- gate_effect: info", text)
        self.assertIn("summary: 🔴 0 · 🟡 0 · 🟢 1", text)

    def test_migration_never_invents_evidence(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n"
        ))

        run_main(["review_post.py", "--migrate", str(report)])

        parsed_text = report.read_text(encoding="utf-8")
        self.assertNotIn("src/content/posts/dp-1.md:", parsed_text)

    def test_migration_is_idempotent(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n"
        ))

        run_main(["review_post.py", "--migrate", str(report)])
        first = report.read_text(encoding="utf-8")
        run_main(["review_post.py", "--migrate", str(report)])
        second = report.read_text(encoding="utf-8")

        self.assertEqual(first, second)

    def test_already_canonical_report_is_left_byte_identical(self):
        import review_report as rr

        canonical = rr.serialize_report(
            target="a", generated_at="2026-08-02", strict=False,
            findings=[{
                "severity": "🟢", "source": "L", "rule_id": "L1",
                "location": "not-recorded", "quote": "not-recorded",
                "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
                "gate_effect": "info",
            }],
        )
        report = self._write("2026-08-02-a.md", canonical)

        run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(report.read_text(encoding="utf-8"), canonical)


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
