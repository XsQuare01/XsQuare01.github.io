import contextlib
import io
import json
import os
import re
import unittest
import tempfile
from pathlib import Path
from unittest import mock
import review_post as rp
import review_report as rr


REPO_ROOT = Path(__file__).resolve().parent.parent
REVIEW_REPORT_DIR = REPO_ROOT / rp.DEFAULT_REPORTS_DIR
COMMAND_DIR = REPO_ROOT / ".claude" / "commands"
# 스키마 상수는 정본 모듈에서 가져온다. 사본을 두면 갈라져도 테스트가 통과한다(#100).
REQUIRED_REPORT_FIELDS = set(rr.FINDING_FIELDS)
SEVERITY_VALUES = set(rr.SEVERITY_VALUES)
SOURCE_VALUES = set(rr.SOURCE_VALUES)
GATE_EFFECT_VALUES = set(rr.GATE_EFFECT_VALUES)


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


# 기준일과 면제 판정은 production과 같은 것을 쓴다. 테스트가 사본을 들면 계약이
# 갈라져도 초록으로 남는다(#100).
CANONICAL_FROM = rp.CANONICAL_CONTRACT_FROM
report_must_conform = rp.report_under_canonical_contract


def stored_reports():
    return sorted(p for p in REVIEW_REPORT_DIR.glob("*.md") if p.name != "README.md")


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

    def _gate_report(self, findings, name="2026-08-02-gate.md"):
        import review_report as rr

        report = self.root / "reports" / name
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            rr.serialize_report(target="gate", generated_at="2026-08-02",
                                strict=True, findings=findings),
            encoding="utf-8",
        )
        return report

    def _coverage(self, rule_ids=("L1", "L2", "L3", "L4", "L5", "L6", "L7")):
        return [{
            "severity": "🟢", "source": "L", "rule_id": rule_id,
            "location": "not-recorded", "quote": "not-recorded",
            "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
            "gate_effect": "info",
        } for rule_id in rule_ids]

    def _problem(self, severity, source, rule_id, gate_effect):
        return {
            "severity": severity, "source": source, "rule_id": rule_id,
            "location": "src/content/posts/gate.md:12", "quote": "인용",
            "message": "문제 설명", "recommendation": "권장 조치",
            "gate_effect": gate_effect,
        }

    def test_strict_gate_fails_on_deterministic_red(self):
        report = self._gate_report(
            self._coverage() + [self._problem("🔴", "D", "D1", "fail")])

        rc, _ = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 1)

    def test_strict_gate_fails_on_llm_red(self):
        report = self._gate_report(
            self._coverage() + [self._problem("🔴", "L", "L7", "fail")])

        rc, _ = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 1)

    def test_strict_gate_fails_when_red_and_yellow_mixed(self):
        report = self._gate_report(self._coverage() + [
            self._problem("🔴", "L", "L7", "fail"),
            self._problem("🟡", "L", "L1", "warn"),
        ])

        rc, _ = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 1)

    def test_strict_gate_passes_on_yellow_only(self):
        report = self._gate_report(
            self._coverage() + [self._problem("🟡", "L", "L1", "warn")])

        rc, stdout = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 0, stdout)

    def test_strict_gate_passes_when_only_coverage_rows_exist(self):
        report = self._gate_report(self._coverage())

        rc, stdout = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 0, stdout)

    def test_strict_gate_returns_two_on_malformed_llm_output(self):
        report = self._gate_report(self._coverage())
        broken = report.read_text(encoding="utf-8").replace(
            "- gate_effect: info", "- gate_effect: explode", 1)
        report.write_text(broken, encoding="utf-8")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("gate_effect", stderr)

    def test_strict_gate_returns_two_when_llm_phase_missing(self):
        report = self._gate_report([self._problem("🟡", "D", "D3", "warn")])

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("L1", stderr)

    def test_strict_gate_returns_two_when_one_category_missing(self):
        report = self._gate_report(
            self._coverage(("L1", "L2", "L3", "L4", "L5", "L7")))

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("L6", stderr)

    def test_strict_gate_cannot_be_bypassed_by_downgrading_gate_effect(self):
        """🔴인데 gate_effect: info로 적어 게이트를 빠져나갈 수 없다."""
        report = self._gate_report(self._coverage())
        sneaky = report.read_text(encoding="utf-8").replace(
            "- severity: 🟢\n- source: L\n- rule_id: L1",
            "- severity: 🔴\n- source: L\n- rule_id: L1", 1)
        report.write_text(sneaky, encoding="utf-8")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("severity", stderr)

    def test_strict_gate_writes_report_before_returning_failure(self):
        report = self._gate_report(
            self._coverage() + [self._problem("🔴", "L", "L7", "fail")])

        rc, _ = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 1)
        text = report.read_text(encoding="utf-8")
        self.assertIn("summary: 🔴 1 · 🟡 0 · 🟢 7", text)
        self.assertIn("strict: true", text)

    def test_report_summary_and_exit_code_come_from_same_aggregation(self):
        import review_report as rr

        report = self._gate_report(self._coverage() + [
            self._problem("🔴", "D", "D1", "fail"),
            self._problem("🔴", "L", "L7", "fail"),
            self._problem("🟡", "L", "L1", "warn"),
        ])

        rc, _ = run_main(["review_post.py", "--finalize", "--strict", str(report)])

        parsed = rr.parse_report(report.read_text(encoding="utf-8"))
        failing = [f for f in parsed["findings"] if f["gate_effect"] == "fail"]
        self.assertEqual(rc, 1 if failing else 0)
        self.assertEqual(parsed["header"]["summary"], "🔴 2 · 🟡 1 · 🟢 7")

    def test_finalize_without_strict_still_returns_zero_on_red(self):
        """게이트 판정은 --strict를 붙였을 때만 한다."""
        report = self._gate_report(
            self._coverage() + [self._problem("🔴", "L", "L7", "fail")])

        rc, _ = run_main(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 0)

    def _post_coverage(self, post, rule_ids=("L1", "L2", "L3", "L4", "L5", "L6", "L7")):
        """`-all` 리포트용 coverage row. 어느 포스트를 덮었는지 location으로 밝힌다."""
        return [{
            "severity": "🟢", "source": "L", "rule_id": rule_id,
            "location": f"src/content/posts/{post}.md:1-100", "quote": "not-recorded",
            "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
            "gate_effect": "info",
        } for rule_id in rule_ids]

    def test_all_report_fails_when_one_post_has_no_coverage(self):
        """포스트가 여럿이면 한 포스트의 coverage가 나머지를 대신할 수 없다."""
        report = self._gate_report(
            self._post_coverage("alpha")
            + [self._problem("🟡", "D", "D3", "warn") | {
                "location": "src/content/posts/beta.md:12"}],
            name="2026-08-02-all.md",
        )

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("beta.md", stderr)

    def test_all_report_passes_when_every_post_is_covered(self):
        report = self._gate_report(
            self._post_coverage("alpha") + self._post_coverage("beta"),
            name="2026-08-02-all.md",
        )

        rc, stdout, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 0, stdout + stderr)

    def test_all_report_names_only_the_uncovered_categories(self):
        report = self._gate_report(
            self._post_coverage("alpha")
            + self._post_coverage("beta", ("L1", "L2", "L3", "L4", "L5", "L7")),
            name="2026-08-02-all.md",
        )

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("beta.md", stderr)
        self.assertIn("L6", stderr)
        self.assertNotIn("alpha.md", stderr)

    def test_gate_reports_missing_field_instead_of_crashing(self):
        """필드가 빠진 finding은 크래시가 아니라 인프라 실패(2)로 끊는다.

        exit 1은 품질 실패 코드다. 크래시가 1로 새어 나가면 CI가 둘을 구분할 수 없다.
        """
        report = self._gate_report(
            self._coverage() + [self._problem("🔴", "L", "L7", "fail")])
        broken = report.read_text(encoding="utf-8").replace(
            "- location: src/content/posts/gate.md:12\n", "", 1)
        report.write_text(broken, encoding="utf-8")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("location", stderr)
        self.assertNotIn("Traceback", stderr)

    def test_gate_rejects_heading_and_field_severity_mismatch(self):
        """제목 🔴 · 필드 🟢는 정본화로 덮지 않고 거부한다."""
        report = self._gate_report(self._coverage())
        sneaky = report.read_text(encoding="utf-8").replace(
            "### 🟢 [L1] not-recorded", "### 🔴 [L7] not-recorded", 1)
        report.write_text(sneaky, encoding="utf-8")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("제목", stderr)
        self.assertIn("### 🔴 [L7] not-recorded",
                      report.read_text(encoding="utf-8"))

    def test_coverage_gap_still_canonicalizes_the_report(self):
        """게이트가 실패해도 정본화는 끝낸다. 근거가 남아야 하기 때문이다."""
        report = self._gate_report(
            self._coverage(("L1", "L2", "L3", "L4", "L5", "L7")))
        stale = report.read_text(encoding="utf-8").replace(
            "summary: 🔴 0 · 🟡 0 · 🟢 6", "summary: 🔴 9 · 🟡 9 · 🟢 9", 1)
        report.write_text(stale, encoding="utf-8")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("L6", stderr)
        self.assertIn("summary: 🔴 0 · 🟡 0 · 🟢 6",
                      report.read_text(encoding="utf-8"))

    def test_finalize_and_migrate_together_is_an_input_error(self):
        """두 모드를 함께 주어 migrate의 거부를 우회할 수 없다."""
        report = self._gate_report(self._coverage())
        before = report.read_text(encoding="utf-8")

        rc, _, stderr = run_main_streams([
            "review_post.py", "--finalize", "--migrate", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("--migrate", stderr)
        self.assertEqual(report.read_text(encoding="utf-8"), before)

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

    def test_reports_under_canonical_contract_conform_to_v2_schema(self):
        """저장 리포트 검사는 정본 validator와 정본 직렬화 하나로만 한다(#100).

        테스트가 자체 parser와 enum 사본으로 검사하면, production이 놓치는 위반을
        테스트도 같이 놓친다. 실제로 사본 parser는 백틱을 무조건 벗겨 `` `A` / `B` ``를
        깨뜨렸는데, 그 손실이 정확히 #103에서 드러났다.
        """
        reports = stored_reports()
        self.assertTrue(reports, "expected at least one stored review report")
        checked = [path for path in reports if report_must_conform(path)]
        self.assertTrue(checked, "expected at least one report under the canonical contract")

        for report in checked:
            with self.subTest(report=report.name):
                text = report.read_text(encoding="utf-8")

                self.assertEqual(rr.validate_report(text, state="complete"), [], report.name)
                self.assertEqual(text, rp.canonical_form(rr.parse_report(text)),
                                 f"{report.name}: 정본 바이트와 다르다")

    def test_legacy_exemption_is_explicit_and_documented(self):
        """면제 대상은 조용히 빠지지 않고 목록과 문서로 남아야 한다."""
        exempt = [p.name for p in stored_reports() if not report_must_conform(p)]
        readme = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        self.assertIn(CANONICAL_FROM, readme,
                      "README가 정본 강제 기준일을 밝혀야 한다")
        for name in exempt:
            with self.subTest(report=name):
                self.assertLess(name[:10], CANONICAL_FROM,
                                "기준일 이후 리포트는 면제될 수 없다")

    def test_readme_documents_strict_gate_contract(self):
        text = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        for term in ("--finalize --strict", "exit code `1`", "exit code `2`",
                     "L1–L7", "coverage 누락",
                     # 게이트를 우회할 수 있던 경로들. 계약을 문서에 고정해 둔다.
                     "판정 단위는 포스트다", "검증 → 저장 → 판정",
                     "`--finalize`와 `--migrate`는 함께 쓸 수 없다"):
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_command_docs_require_strict_as_the_final_step(self):
        """`--strict`를 빼는 것이 기본 경로면 게이트를 안 돌리는 우회가 남는다."""
        for command_name in ("review-post.md", "review-post-all.md"):
            with self.subTest(command=command_name):
                text = (COMMAND_DIR / command_name).read_text(encoding="utf-8")
                self.assertIn("--finalize --strict docs/reviews/", text)
                self.assertIn("리뷰 종료 조건", text)

    def test_readme_documents_canonical_order_and_two_valid_states(self):
        text = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        for term in ("scaffold", "complete", "--finalize", "--migrate",
                     "migrated_from", "sources"):
            with self.subTest(term=term):
                self.assertIn(term, text)

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
            "--finalize",
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


class TestStoredReportValidation(unittest.TestCase):
    """저장 리포트 검사는 정본 validator 하나로 한다(#100).

    아래 위반은 전부 예전 검사(테스트 전용 parser + enum 사본)를 통과했다.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.canonical = rr.serialize_report(
            target="alpha", generated_at="2026-08-05", strict=False,
            findings=[{
                "severity": "🟡", "source": "L", "rule_id": "L1",
                "location": "src/content/posts/alpha.md:12", "quote": "인용",
                "message": "문제", "recommendation": "권고", "gate_effect": "warn",
            }],
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_canonical_report_passes(self):
        self.assertEqual(rr.validate_report(self.canonical), [])

    def test_unknown_state_is_a_caller_bug_not_a_finding(self):
        """오타 난 state를 오류 목록에 담으면 호출자가 데이터 결함으로 읽고 넘어간다."""
        with self.assertRaises(ValueError):
            rr.validate_report(self.canonical, state="scaffolding")
        for state in rr.REPORT_STATES:
            with self.subTest(state=state):
                rr.validate_report(self.canonical, state=state)

    def test_invalid_strict_value_is_rejected(self):
        text = self.canonical.replace("strict: false", "strict: banana")

        errors = rr.validate_report(text)

        self.assertTrue(any("strict" in e for e in errors), errors)

    def test_schema_version_must_be_the_first_line(self):
        text = "# 리뷰 리포트\n\n" + self.canonical

        errors = rr.validate_report(text)

        self.assertTrue(any("first line" in e for e in errors), errors)

    def test_stale_summary_is_rejected(self):
        text = self.canonical.replace("summary: 🔴 0 · 🟡 1 · 🟢 0",
                                      "summary: 🔴 0 · 🟡 9 · 🟢 0")

        errors = rr.validate_report(text)

        self.assertTrue(any("stale" in e for e in errors), errors)

    def test_non_canonical_order_and_spacing_are_caught_by_byte_equality(self):
        """정렬·공백은 validator가 아니라 정본 바이트 비교가 잡는다."""
        two_blank_lines = self.canonical.replace("## Findings\n\n", "## Findings\n\n\n")
        reordered = rr.serialize_report(
            target="alpha", generated_at="2026-08-05", strict=False,
            findings=[
                {"severity": "🟢", "source": "L", "rule_id": "L2",
                 "location": "a.md:2", "quote": "q", "message": "m",
                 "recommendation": "r", "gate_effect": "info"},
                {"severity": "🔴", "source": "L", "rule_id": "L1",
                 "location": "a.md:1", "quote": "q", "message": "m",
                 "recommendation": "r", "gate_effect": "fail"},
            ],
        ).replace("### 🔴 [L1] a.md:1", "### PLACEHOLDER")  # 순서만 흔든다
        swapped = reordered.replace("### 🟢 [L2] a.md:2", "### 🔴 [L1] a.md:1")
        swapped = swapped.replace("### PLACEHOLDER", "### 🟢 [L2] a.md:2")

        for name, text in (("빈 줄 두 개", two_blank_lines), ("정렬 어긋남", swapped)):
            with self.subTest(case=name):
                self.assertNotEqual(text, rp.canonical_form(rr.parse_report(text)))

    def test_gate_rejects_a_stored_report_with_an_invalid_strict_value(self):
        """validator가 좁아진 만큼 게이트도 함께 좁아져야 한다."""
        reports = self.root / "reviews"
        reports.mkdir()
        (reports / "2026-08-05-alpha.md").write_text(
            self.canonical.replace("strict: false", "strict: banana"), encoding="utf-8")

        rc, _, stderr = run_main_streams([
            "review_post.py", "--gate", "--reports-dir", str(reports),
        ])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("strict", stderr)

    def test_finalize_refuses_a_section_the_canonical_form_cannot_hold(self):
        report = self.root / "2026-08-05-alpha.md"
        report.write_text(self.canonical + "\n## 검증 로그\n\n- 빌드 성공\n", encoding="utf-8")
        original = report.read_bytes()

        rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("검증 로그", stderr)
        self.assertEqual(report.read_bytes(), original)

    def test_finalize_refuses_progress_sections_that_hold_prose(self):
        """진행용 제목은 전환의 입력이지 정본의 일부가 아니다.

        `--migrate`가 허용하는 목록을 정본화가 함께 쓰면, 그 제목 아래 산문이
        성공 코드와 함께 사라진다.
        """
        for section in ("## 결정적 검사", "## LLM 비평", "# 리뷰 리포트"):
            with self.subTest(section=section):
                report = self.root / "2026-08-05-alpha.md"
                report.write_text(
                    f"{self.canonical}\n{section}\n\n보존해야 할 산문\n", encoding="utf-8")
                original = report.read_bytes()

                rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

                self.assertEqual(rc, 2, stderr)
                self.assertIn(section.lstrip("# "), stderr)
                self.assertEqual(report.read_bytes(), original)
                self.assertIn("보존해야 할 산문", report.read_text(encoding="utf-8"))

    def test_migrate_still_accepts_progress_sections(self):
        """정본화가 좁아진 것이 전환까지 막으면 과거 리포트를 옮길 수 없다."""
        report = self.root / "2026-07-20-alpha.md"
        report.write_text(
            "## 결정적 검사: src/content/posts/alpha.md\n발견 사항 없음 ✅\n\n"
            "## LLM 비평\n\n### 🟡 [L1] src/content/posts/alpha.md:12\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L1\n"
            "- location: src/content/posts/alpha.md:12\n"
            "- quote: 인용\n- message: 문제\n- recommendation: 권고\n- gate_effect: warn\n\n"
            "요약: 🔴 0 · 🟡 1 · 🟢 0\n", encoding="utf-8")

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stderr)
        self.assertEqual(rr.validate_report(report.read_text(encoding="utf-8")), [])

    def test_finalize_refuses_an_invalid_strict_value_even_with_strict_flag(self):
        """`--strict`가 strict 값을 덮어쓰므로, 원본을 먼저 보지 않으면 결함이 지워진다."""
        report = self.root / "2026-08-05-alpha.md"
        for argv in (["--finalize"], ["--finalize", "--strict"]):
            with self.subTest(argv=" ".join(argv)):
                report.write_text(self.canonical.replace("strict: false", "strict: banana"),
                                  encoding="utf-8")
                original = report.read_bytes()

                rc, _, stderr = run_main_streams(["review_post.py", *argv, str(report)])

                self.assertEqual(rc, 2, stderr)
                self.assertIn("strict", stderr)
                self.assertEqual(report.read_bytes(), original)

    def test_finalize_refuses_a_buried_schema_declaration(self):
        """serializer가 선언을 첫 줄로 옮기므로, 원본을 먼저 보지 않으면 위반이 정규화된다."""
        report = self.root / "2026-08-05-alpha.md"
        report.write_text("리포트 머리말\n\n" + self.canonical, encoding="utf-8")
        original = report.read_bytes()

        rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("first line", stderr)
        self.assertEqual(report.read_bytes(), original)

    def test_commands_do_not_ask_for_a_progress_section(self):
        """커맨드가 만들라고 한 섹션을 정본화가 거부하면 계약이 서로 어긋난다."""
        for name in ("review-post.md", "review-post-all.md"):
            with self.subTest(command=name):
                text = (COMMAND_DIR / name).read_text(encoding="utf-8")

                self.assertNotIn("리포트의 결정적 검사 섹션에 그대로 포함한다", text)
                self.assertIn("산문 섹션을 만들지 않는다", text)

    def test_no_second_report_parser_lives_in_the_tests(self):
        """테스트가 자체 parser를 다시 들이면 계약이 조용히 갈라진다."""
        source = Path(__file__).read_text(encoding="utf-8")

        # 이 파일 자신에 걸리지 않도록 조각으로 나눠 찾는다.
        self.assertNotIn("def " + "parse_report_findings", source)
        self.assertIs(report_must_conform, rp.report_under_canonical_contract)
        self.assertEqual(REQUIRED_REPORT_FIELDS, set(rr.FINDING_FIELDS))
        self.assertEqual(CANONICAL_FROM, rp.CANONICAL_CONTRACT_FROM)


class TestLlmRubricSingleSource(unittest.TestCase):
    """L1–L7 루브릭은 정본 하나만 둔다(#87).

    두 커맨드가 문구를 각자 들고 있으면 갈라진다. 실제로 `/review-post-all`의 L1은
    `docs/writing-rules.md` 참조와 강박 금지 단서를 빠뜨린 채 오래 유지됐다.
    """

    RUBRIC = REPO_ROOT / "docs" / "review-rubric.md"
    COMMANDS = ("review-post.md", "review-post-all.md")

    def _rubric_text(self):
        return self.RUBRIC.read_text(encoding="utf-8")

    def _command_text(self, name):
        return (COMMAND_DIR / name).read_text(encoding="utf-8")

    def _critique_section(self, text):
        return text.split("## 2단계: LLM 비평", 1)[1].split("\n## ", 1)[0]

    def test_canonical_rubric_defines_exactly_l1_to_l7(self):
        text = self._rubric_text()

        defined = re.findall(r"(?m)^- \*\*(L[1-7]) ", text)
        self.assertEqual(defined, ["L1", "L2", "L3", "L4", "L5", "L6", "L7"])
        self.assertNotIn("**L8", text)

    def test_canonical_rubric_l1_keeps_the_writing_guide_and_anti_compulsion(self):
        l1 = self._rubric_text().split("- **L1 ", 1)[1].split("\n- **L2", 1)[0]

        for term in ("docs/writing-rules.md", "바른 문장 쓰기", "강박 금지",
                     "논리 전환에 꼭 필요한 접속어"):
            with self.subTest(term=term):
                self.assertIn(term, l1)

    def test_both_commands_point_at_the_canonical_rubric(self):
        for name in self.COMMANDS:
            with self.subTest(command=name):
                text = self._command_text(name)
                self.assertIn("docs/review-rubric.md", text)

    def test_neither_command_redefines_the_rubric(self):
        """정본을 두고도 문구를 복제하면 다시 갈라진다."""
        for name in self.COMMANDS:
            with self.subTest(command=name):
                text = self._command_text(name)
                inlined = re.findall(r"(?m)^- \*\*(L[1-7]) ", text)
                self.assertEqual(inlined, [], f"{name}에 루브릭 문구가 복제돼 있다")

    def test_both_commands_share_one_critique_section(self):
        sections = [self._critique_section(self._command_text(n)) for n in self.COMMANDS]

        self.assertEqual(sections[0], sections[1])

    def test_coverage_constant_matches_the_canonical_rubric(self):
        defined = tuple(re.findall(r"(?m)^- \*\*(L[1-7]) ", self._rubric_text()))

        self.assertEqual(rp.REQUIRED_LLM_RULES, defined)

    def _l6_section(self):
        return self._rubric_text().split("- **L6 ", 1)[1].split("\n- **L7", 1)[0]

    def test_canonical_rubric_defines_four_l6_states(self):
        """L6는 네 상태로 기록한다(#88).

        원문 접근 실패를 검증 통과와 같은 색으로 보고하면 판정 의미가 흔들린다.
        2026-08-13 전수 리뷰는 대조 실패를 59개 글 전부 🟢으로 적었다.
        """
        l6 = self._l6_section()

        for state in ("verified fidelity", "approved extension",
                      "source unavailable", "actual mismatch"):
            with self.subTest(state=state):
                self.assertIn(state, l6)

    def test_canonical_rubric_maps_l6_states_to_severity(self):
        """상태만 있고 severity가 없으면 리뷰마다 색이 갈린다."""
        l6 = self._l6_section()

        rows = {
            "verified fidelity": ("🟢", "info"),
            "approved extension": ("🟢", "info"),
            "source unavailable": ("🟡", "warn"),
        }
        for state, (severity, gate_effect) in rows.items():
            with self.subTest(state=state):
                row = next(line for line in l6.splitlines() if state in line)
                self.assertIn(severity, row)
                self.assertIn(gate_effect, row)

        mismatch_rows = [line for line in l6.splitlines() if "actual mismatch" in line]
        self.assertEqual(len(mismatch_rows), 2, "국소와 핵심 불일치를 나눠 적는다")
        self.assertTrue(any("🔴" in row and "fail" in row for row in mismatch_rows))
        self.assertTrue(any("🟡" in row and "warn" in row for row in mismatch_rows))

    def test_canonical_rubric_forbids_reporting_missing_source_as_verified(self):
        l6 = self._l6_section()

        for term in ("`message` 맨 앞", "미완료",
                     "추가 자체를 불일치로 판정하지 않는다"):
            with self.subTest(term=term):
                self.assertIn(term, l6)

    def test_both_commands_declare_the_l6_coverage_exception(self):
        """coverage row를 🟢으로 고정한 규정과 L6 WARN이 충돌한다(#88).

        L6는 원문 대조가 안 되면 '이슈 없음'이 아니라 '검증 미완료'다.
        """
        for name in self.COMMANDS:
            with self.subTest(command=name):
                text = self._command_text(name)
                self.assertIn("L6는 이 고정에서 예외다", text)
                self.assertIn("source unavailable", text)
                self.assertIn("docs/review-rubric.md", text)

    def test_readme_documents_l6_severity_and_reporting_examples(self):
        readme = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        self.assertIn("#### L6 상태가 severity를 정한다", readme)
        for term in ("source unavailable", "verified fidelity",
                     "gate_effect: warn", "2026-08-18"):
            with self.subTest(term=term):
                self.assertIn(term, readme)

    V1_SPEC = (REPO_ROOT / "docs" / "superpowers" / "specs"
               / "2026-06-03-review-post-command-design.md")

    def test_superseded_v1_spec_is_marked_historical(self):
        """v1 설계서는 L1–L5만 정의하고 수학 정확성을 판정하지 않는다고 적었다.

        현재 L7과 정면으로 어긋나므로, 그 문서를 현재 계약으로 읽으면 안 된다는
        표시와 정본 링크가 문서 안에 있어야 한다.
        """
        text = self.V1_SPEC.read_text(encoding="utf-8")

        head = text.split("\n## ", 1)[0]
        self.assertIn("docs/review-rubric.md", head)
        for term in ("v1", "기록"):
            with self.subTest(term=term):
                self.assertIn(term, head)

    def test_readme_does_not_present_the_v1_spec_as_the_current_design(self):
        text = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        self.assertNotIn("자세한 설계는 `docs/superpowers/specs/2026-06-03", text)
        self.assertIn("docs/review-rubric.md", text)

    def test_readme_category_labels_match_the_canonical_rubric(self):
        """범주 이름을 README가 따로 적어 두면 정본과 갈라진다."""
        rubric = self._rubric_text()
        readme = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        for match in re.finditer(r"(?m)^- \*\*(L[1-7]) ([^:*]+):\*\*", rubric):
            rule_id, label = match.group(1), match.group(2).strip()
            with self.subTest(rule=rule_id):
                if rule_id in readme and f"{rule_id} " in readme:
                    self.assertIn(f"{rule_id} {label}", readme,
                                  f"README의 {rule_id} 이름이 정본과 다르다")

    def test_command_specific_output_differences_are_preserved(self):
        """루브릭을 합치면서 편별·집계 출력 차이를 지우지 않는다."""
        single = self._command_text("review-post.md")
        aggregate = self._command_text("review-post-all.md")

        self.assertIn("<오늘 날짜>-<slug>.md", single)
        self.assertNotIn("aggregate summary", single)
        self.assertIn("<오늘 날짜>-all.md", aggregate)
        self.assertIn("aggregate summary", aggregate)


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

    def _write(self, name, text, summary=None):
        """리포트 fixture를 쓴다.

        --migrate는 원본이 밝힌 심각도 총계와 대조되지 않으면 전환하지 않으므로,
        요약 줄이 없는 fixture에는 기대 총계를 붙여 준다.
        """
        if summary is not None:
            text = f"{text}\n요약: {summary}\n"
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
        ), summary="🔴 0 · 🟡 1 · 🟢 0")

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
        ), summary="🔴 0 · 🟡 0 · 🟢 1")

        run_main(["review_post.py", "--migrate", str(report)])

        text = report.read_text(encoding="utf-8")
        self.assertIn("- severity: 🟢", text)
        self.assertIn("- gate_effect: info", text)
        self.assertIn("summary: 🔴 0 · 🟡 0 · 🟢 1", text)

    def test_report_without_findings_heading_still_migrates(self):
        import review_report as rr

        report = self._write("2026-07-30-dp-3.md", (
            "## 결정적 검사: src/content/posts/dp-3.md\n발견 사항 없음 ✅\n\n"
            "## LLM 비평: src/content/posts/dp-3.md\n\n"
            "### 🟡 [L2] src/content/posts/dp-3.md:19\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L2\n"
            "- location: src/content/posts/dp-3.md:19\n"
            "- quote: `(더 나가면) 복원, 복잡도`\n"
            "- message: 개요 항목이 본문 구성과 어긋난다\n"
            "- recommendation: 항목을 나눈다\n- gate_effect: warn\n"
        ), summary="🔴 0 · 🟡 1 · 🟢 0")

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text), [])
        self.assertIn("## Findings", text)
        self.assertIn("- source: L", text)
        self.assertNotIn("migrated_from:", text)

    def test_descriptive_heading_is_preserved_in_message(self):
        report = self._write("2026-07-30-dp-3.md", (
            "### 🟡 [L2] 개요의 항목 구분이 실제 본문 구성과 어긋남\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L2\n"
            "- location: src/content/posts/dp-3.md:19\n"
            "- quote: `복원, 복잡도`\n"
            "- message: 복잡도는 독립된 절에서 다룬다\n"
            "- recommendation: 항목을 나눈다\n- gate_effect: warn\n"
        ), summary="🔴 0 · 🟡 1 · 🟢 0")

        run_main(["review_post.py", "--migrate", str(report)])

        text = report.read_text(encoding="utf-8")
        self.assertIn("개요의 항목 구분이 실제 본문 구성과 어긋남", text)
        self.assertIn("복잡도는 독립된 절에서 다룬다", text)
        self.assertIn("### 🟡 [L2] src/content/posts/dp-3.md:19", text)

    def test_heading_that_only_repeats_location_adds_no_title(self):
        report = self._write("2026-06-27-quicksort.md", (
            "### 🔴 [L7] src/content/posts/quicksort.md:42\n\n"
            "- severity: 🔴\n- source: L\n- rule_id: L7\n"
            "- location: src/content/posts/quicksort.md:42\n"
            "- quote: `while (i <= j) {`\n"
            "- message: 분할 코드가 멈추지 않을 수 있다\n"
            "- recommendation: 전제를 명시한다\n- gate_effect: fail\n"
        ), summary="🔴 1 · 🟡 0 · 🟢 0")

        run_main(["review_post.py", "--migrate", str(report)])

        self.assertIn("- message: 분할 코드가 멈추지 않을 수 있다",
                      report.read_text(encoding="utf-8"))

    def test_legacy_bullet_location_and_subfields_are_recovered(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n"
            "- [L7] src/content/posts/dp-1.md:88 · gate: info\n"
            "  - quote: \"$2^{n/2-1} \\le F(n) < 2^n$\"\n"
            "  - message: 지수 범위 증명 검증. 상한 F(n)≤2F(n-1)\n"
        ), summary="🔴 0 · 🟡 0 · 🟢 1")

        run_main(["review_post.py", "--migrate", str(report)])

        text = report.read_text(encoding="utf-8")
        self.assertIn("- location: src/content/posts/dp-1.md:88", text)
        self.assertIn("$2^{n/2-1} \\le F(n) < 2^n$", text)
        self.assertIn("- message: 지수 범위 증명 검증. 상한 F(n)≤2F(n-1)", text)
        self.assertNotIn("- location: not-recorded", text)

    def test_legacy_message_drops_redundant_bullet_prefix(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n"
            "- [L2] not-recorded · gate: info — 흐름 검토 완료, 이슈 없음.\n"
        ), summary="🔴 0 · 🟡 0 · 🟢 1")

        run_main(["review_post.py", "--migrate", str(report)])

        self.assertIn("- message: 흐름 검토 완료, 이슈 없음.",
                      report.read_text(encoding="utf-8"))

    def test_bullet_heading_with_indented_fields_is_class_a(self):
        import review_report as rr

        report = self._write("2026-07-01-closest-pair-2.md", (
            "## 결정적 검사: src/content/posts/closest-pair-2.md\n발견 사항 없음 ✅\n\n"
            "## LLM 비평\n\n"
            "- 🟡 [L7] src/content/posts/closest-pair-2.md:95\n"
            "  - severity: 🟡\n  - source: L\n  - rule_id: L7\n"
            "  - location: src/content/posts/closest-pair-2.md:95\n"
            "  - quote: \"// 두 점 사이 거리의 제곱\"\n"
            "  - message: signed overflow가 날 수 있다\n"
            "  - recommendation: 입력 범위를 명시한다\n"
            "  - gate_effect: warn\n"
        ), summary="🔴 0 · 🟡 1 · 🟢 0")

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        text = report.read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text), [])
        self.assertIn("- source: L", text)
        self.assertNotIn("- source: MIGRATED", text)
        self.assertNotIn("migrated_from:", text)
        self.assertIn("- message: signed overflow가 날 수 있다", text)
        self.assertIn("- quote: \"// 두 점 사이 거리의 제곱\"", text)

    def test_migration_never_invents_evidence(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n"
        ), summary="🔴 0 · 🟡 0 · 🟢 1")

        run_main(["review_post.py", "--migrate", str(report)])

        parsed_text = report.read_text(encoding="utf-8")
        self.assertNotIn("src/content/posts/dp-1.md:", parsed_text)

    def test_migration_is_idempotent(self):
        report = self._write("2026-07-24-dp-1.md", (
            "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n"
        ), summary="🔴 0 · 🟡 0 · 🟢 1")

        run_main(["review_post.py", "--migrate", str(report)])
        first = report.read_text(encoding="utf-8")
        run_main(["review_post.py", "--migrate", str(report)])
        second = report.read_text(encoding="utf-8")

        self.assertEqual(first, second)

    def test_refuses_to_write_when_severity_totals_disagree(self):
        """파서가 형식을 놓쳐 finding이 사라지면 원본을 건드리지 않는다."""
        original = (
            "🟢 참고 (3)\n\n- [L6] not-recorded · gate: info — 대조했다.\n\n"
            "요약: 🔴 0 · 🟡 0 · 🟢 3\n"
        )
        report = self._write("2026-07-24-dp-1.md", original)

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("심각도 총계 불일치", stderr)
        self.assertEqual(report.read_text(encoding="utf-8"), original)

    def test_refuses_to_write_when_source_declares_no_totals(self):
        original = "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n"
        report = self._write("2026-07-24-dp-1.md", original)

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2)
        self.assertIn("대조할 심각도 총계가 없어", stderr)
        self.assertEqual(report.read_text(encoding="utf-8"), original)

    def test_partial_deterministic_summary_line_is_not_used_for_comparison(self):
        """`요약(결정적):`은 일부만 센 줄이라 대조 기준이 아니다."""
        report = self._write("2026-07-03-closest-pair-3.md", (
            "요약(결정적): 🔴 1 · 🟡 0 · 🟢 0\n\n"
            "🟢 참고 (1)\n\n- [L6] not-recorded · gate: info — 대조했다.\n\n"
            "요약: 🔴 0 · 🟡 0 · 🟢 1\n"
        ))

        rc, stdout = run_main(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stdout)
        self.assertIn("summary: 🔴 0 · 🟡 0 · 🟢 1",
                      report.read_text(encoding="utf-8"))

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


CANONICAL_WITH_AUDIT = (
    "schema_version: review-report/v2\n"
    "target: dp-2\n"
    "generated_at: 2026-07-28\n"
    "strict: not-recorded\n"
    "summary: 🔴 0 · 🟡 1 · 🟢 0\n"
    "\n"
    "## Findings\n"
    "\n"
    "### 🟡 [L7] src/content/posts/dp-2.md:91\n"
    "\n"
    "- severity: 🟡\n"
    "- source: L\n"
    "- rule_id: L7\n"
    "- location: src/content/posts/dp-2.md:91\n"
    "- quote: `S(0)` / `S(1)`\n"
    "- message: 기저 문구가 점화식 범위와 어긋난다\n"
    "- recommendation: 기저를 직접 정하고 점화식은 n≥2부터 적용한다\n"
    "- gate_effect: warn\n"
    "\n"
    "## 후속 처리\n"
    "\n"
    "- 🟡 [L7] 기저 문구(dp-2:91) → 커밋 `69ec1f0`에서 정정. **반영 완료**.\n"
    "- 재검증: `npm run build` 성공(106 pages).\n"
)

# PR #97이 감사 섹션을 지운 리포트. 복구했으니 다시 사라지면 안 된다(#103).
REPORTS_WITH_AUDIT_SECTION = (
    "2026-06-25-divide-and-conquer.md",
    "2026-06-27-quicksort.md",
    "2026-07-08-convex-hull-2.md",
    "2026-07-09-convex-hull-3.md",
    "2026-07-10-convex-hull-bst-tangent.md",
    "2026-07-13-convex-hull-4.md",
    "2026-07-15-convex-hull-5.md",
    "2026-07-23-matrix-strassen-why-seven.md",
    "2026-07-24-dp-1.md",
    "2026-07-28-dp-2.md",
    "2026-07-30-dp-3.md",
)


class TestEvidenceFidelity(unittest.TestCase):
    """정본화가 근거를 바꾸지 않는다는 계약(#103)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, text):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    # ---- code span ----

    def test_multiple_code_spans_survive_parsing(self):
        """감싼 백틱 한 쌍만 벗기면 여러 code span이 뒤집힌 스팬 하나로 깨진다."""
        import review_report as rr

        raw = "`int matrixChain(const vector<int>& d, int n)` / `d[i-1]*d[k]*d[j]`"
        parsed = rr.parse_report(
            "## Findings\n\n### 🟡 [L7] a.md:1\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n- location: a.md:1\n"
            f"- quote: {raw}\n- message: m\n- recommendation: r\n- gate_effect: warn\n"
        )

        self.assertEqual(parsed["findings"][0]["quote"], raw)

    def test_single_code_span_is_still_unwrapped(self):
        import review_report as rr

        parsed = rr.parse_report(
            "## Findings\n\n### 🟡 [L7] a.md:1\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n- location: `a.md:1`\n"
            "- quote: `트리가 **DAG)**가`\n- message: m\n"
            "- recommendation: r\n- gate_effect: warn\n"
        )

        self.assertEqual(parsed["findings"][0]["quote"], "트리가 **DAG)**가")
        self.assertEqual(parsed["findings"][0]["location"], "a.md:1")

    def test_awkward_values_round_trip_byte_identically(self):
        """백틱이 섞인 값이 정본화를 반복해도 바이트가 그대로여야 한다.

        값 전체를 감싼 백틱 한 쌍은 표기 정규화로 한 번 벗겨진다(`location`이 그
        대상이다). 그 뒤로는 손대지 않는다. 정규화가 매 실행마다 값을 깎으면
        리포트를 다시 돌릴 때마다 근거가 조금씩 사라진다.
        """
        import review_report as rr

        def canonicalize(value):
            findings = value if isinstance(value, list) else [{
                "severity": "🟡", "source": "L", "rule_id": "L7",
                "location": "a.md:1", "quote": value, "message": value,
                "recommendation": "r", "gate_effect": "warn",
            }]
            return rr.serialize_report(target="t", generated_at="2026-08-04",
                                       strict=False, findings=findings)

        for value in (
            "`A` / `B`",
            "`int f(vector<int>& d)` / `d[i-1]*d[k]*d[j]`",
            "표기 `M_i`와 `M[i,j]`를 구분한다",
            "백틱 ` 하나만 있다",
            "`$M[1,3]=\\min(28,48)=28$`",
        ):
            with self.subTest(value=value):
                once = canonicalize(value)
                parsed = rr.parse_report(once)
                twice = canonicalize(parsed["findings"])

                self.assertEqual(rr.parse_report(twice), parsed)
                self.assertEqual(canonicalize(rr.parse_report(twice)["findings"]), twice)
                self.assertEqual(rr.verify_round_trip(twice, parsed["findings"]), [])

    # ---- audit 섹션 ----

    def test_audit_section_round_trips_byte_identically(self):
        import review_report as rr

        parsed = rr.parse_report(CANONICAL_WITH_AUDIT)
        rebuilt = rr.serialize_report(
            target=parsed["header"]["target"],
            generated_at=parsed["header"]["generated_at"],
            strict=parsed["header"]["strict"],
            findings=parsed["findings"],
            audit=parsed["audit"],
        )

        self.assertEqual(rebuilt, CANONICAL_WITH_AUDIT)

    def test_audit_section_bullets_are_not_read_as_findings(self):
        """감사 섹션의 `- 🟡 [L7] …` 불릿은 finding 제목 꼴이다. finding으로 세면 안 된다."""
        import review_report as rr

        parsed = rr.parse_report(CANONICAL_WITH_AUDIT)

        self.assertEqual(len(parsed["findings"]), 1)
        self.assertEqual(rr.validate_report(CANONICAL_WITH_AUDIT), [])

    def test_validate_rejects_a_finding_below_the_audit_section(self):
        """감사 섹션 뒤 finding은 파서가 읽지 않으므로 조용히 사라진다."""
        import review_report as rr

        text = CANONICAL_WITH_AUDIT + (
            "\n### 🔴 [L1] a.md:3\n\n"
            "- severity: 🔴\n- source: L\n- rule_id: L1\n- location: a.md:3\n"
            "- quote: q\n- message: m\n- recommendation: r\n- gate_effect: fail\n"
        )

        errors = rr.validate_report(text)

        self.assertTrue(errors)
        self.assertTrue(any("감사 섹션" in e for e in errors), errors)

    # ---- multiline 값 ----

    def _report_with_continuation(self, continuation):
        return (
            "## Findings\n\n### 🟡 [L7] a.md:1\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n- location: a.md:1\n"
            "- quote: q\n"
            "- message: 첫 줄이다\n"
            f"{continuation}\n"
            "- recommendation: r\n- gate_effect: warn\n"
        )

    def test_multiline_field_value_is_reported_not_truncated(self):
        """모양으로 걸러 내면 걸러진 모양만 조용히 사라진다. 들여쓴 줄은 다 잡는다."""
        import review_report as rr

        for continuation in (
            "  둘째 줄은 조용히 사라진다",
            "  - 중첩된 근거",           # 중첩 목록
            "  1. 번호 붙인 근거",
            "  | 셀 | 셀 |",            # 들여쓴 표
            "  # 들여쓴 제목처럼 보이는 줄",
            "\t탭으로 들여쓴 줄",
        ):
            with self.subTest(continuation=continuation):
                text = self._report_with_continuation(continuation)
                parsed = rr.parse_report(text)

                errors = rr.validate_source_findings(parsed["findings"])

                self.assertTrue(any("여러 줄" in e for e in errors), errors)
                self.assertNotIn(continuation.strip(), rr.serialize_report(
                    target="t", generated_at="2026-08-04", strict=False,
                    findings=parsed["findings"],
                ), "정본에 담기지 않는 내용이면 검증에서 막아야 한다")

    def test_migrate_refuses_a_nested_bullet_inside_a_field(self):
        report = self._write("2026-07-20-alpha.md", (
            "## LLM 비평: src/content/posts/alpha.md\n\n"
            + self._report_with_continuation("  - 중첩된 근거")
            + "\n요약: 🔴 0 · 🟡 1 · 🟢 0\n"
        ))
        original = report.read_bytes()

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("여러 줄", stderr)
        self.assertEqual(report.read_bytes(), original)

    # ---- round-trip 검증 헬퍼 ----

    def test_round_trip_check_catches_a_changed_field_value(self):
        import review_report as rr

        parsed = rr.parse_report(CANONICAL_WITH_AUDIT)
        tampered = [dict(parsed["findings"][0], quote="다른 인용")]

        errors = rr.verify_round_trip(CANONICAL_WITH_AUDIT, tampered, parsed["audit"])

        self.assertTrue(any("quote" in e for e in errors), errors)

    def test_round_trip_check_catches_a_dropped_audit_section(self):
        import review_report as rr

        parsed = rr.parse_report(CANONICAL_WITH_AUDIT)
        without_audit = CANONICAL_WITH_AUDIT.split("\n## 후속 처리", 1)[0] + "\n"

        errors = rr.verify_round_trip(without_audit, parsed["findings"], parsed["audit"])

        self.assertTrue(any("후속 처리" in e or "감사 섹션" in e for e in errors), errors)

    # ---- migrate / finalize ----

    def test_finalize_preserves_the_audit_section(self):
        report = self._write("2026-07-28-dp-2.md", CANONICAL_WITH_AUDIT)

        rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 0, stderr)
        self.assertEqual(report.read_text(encoding="utf-8"), CANONICAL_WITH_AUDIT)

    def test_migrate_preserves_the_audit_section_and_code_spans(self):
        import review_report as rr

        report = self._write("2026-07-30-dp-3.md", (
            "## LLM 비평: src/content/posts/dp-3.md\n\n"
            "### 🟡 [L7] 비용 자료형의 유효 범위가 제시되지 않음\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n"
            "- location: src/content/posts/dp-3.md:103\n"
            "- quote: `int matrixChain(const vector<int>& d, int n)` / `d[i-1]*d[k]*d[j]`\n"
            "- message: int로 계산한다\n- recommendation: long long을 쓴다\n"
            "- gate_effect: warn\n\n"
            "요약: 🔴 0 · 🟡 1 · 🟢 0\n\n"
            "## 후속 처리\n\n"
            "- 🟡 [L7] 자료형 → `long long`으로 바꿈. **반영 완료**.\n"
        ))

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 0, stderr)
        text = report.read_text(encoding="utf-8")
        self.assertEqual(rr.validate_report(text), [])
        self.assertIn("## 후속 처리", text)
        self.assertIn("- 🟡 [L7] 자료형 → `long long`으로 바꿈. **반영 완료**.", text)
        self.assertIn(
            "- quote: `int matrixChain(const vector<int>& d, int n)` / `d[i-1]*d[k]*d[j]`",
            text,
        )
        self.assertEqual(len(rr.parse_report(text)["findings"]), 1)

    def test_migrate_refuses_when_an_unknown_section_would_be_dropped(self):
        report = self._write("2026-07-20-alpha.md", (
            "## LLM 비평: src/content/posts/alpha.md\n\n"
            "### 🟡 [L7] alpha\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n- location: alpha.md:1\n"
            "- quote: q\n- message: m\n- recommendation: r\n- gate_effect: warn\n\n"
            "요약: 🔴 0 · 🟡 1 · 🟢 0\n\n"
            "## 검증 로그\n\n"
            "- 빌드 성공을 여기에 적었다.\n"
        ))
        original = report.read_bytes()

        rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("검증 로그", stderr)
        self.assertEqual(report.read_bytes(), original)

    def test_migrate_refuses_when_the_round_trip_loses_a_field(self):
        """무손실을 증명할 수 없으면 쓰지 않는다."""
        import review_report as rr

        report = self._write("2026-07-20-alpha.md", (
            "## LLM 비평: src/content/posts/alpha.md\n\n"
            "### 🟡 [L7] alpha\n\n"
            "- severity: 🟡\n- source: L\n- rule_id: L7\n- location: alpha.md:1\n"
            "- quote: 인용이다\n- message: m\n- recommendation: r\n- gate_effect: warn\n\n"
            "요약: 🔴 0 · 🟡 1 · 🟢 0\n"
        ))
        original = report.read_bytes()
        real_serialize = rr.serialize_report

        def lossy_serialize(**kwargs):
            findings = [dict(f, quote="not-recorded") for f in kwargs.pop("findings")]
            return real_serialize(findings=findings, **kwargs)

        with mock.patch.object(rr, "serialize_report", lossy_serialize):
            rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("quote", stderr)
        self.assertEqual(report.read_bytes(), original)

    # ---- 실제 손상 사례 회귀 ----

    def test_readme_documents_the_evidence_contract(self):
        text = (REPO_ROOT / "docs" / "reviews" / "README.md").read_text(encoding="utf-8")
        for term in (
            "### 감사 섹션",
            "## 후속 처리",
            "## 반영 상태",
            "## 반영 결과",
            "한 쌍뿐일 때만",
            "한 줄에 담는다",
        ):
            self.assertIn(term, text)

    def test_audit_headings_in_the_readme_match_the_parser(self):
        """문서와 파서가 갈라지면 문서에 적힌 제목이 조용히 사라진다."""
        import review_report as rr

        text = (REPO_ROOT / "docs" / "reviews" / "README.md").read_text(encoding="utf-8")
        section = text.split("### 감사 섹션", 1)[1].split("\n### ", 1)[0]
        documented = {m for m in re.findall(r"`## ([^`]+)`", section)}

        self.assertEqual(documented, set(rr.AUDIT_HEADINGS))

    def test_repository_reports_keep_their_audit_sections(self):
        reports = REPO_ROOT / "docs" / "reviews"
        for name in REPORTS_WITH_AUDIT_SECTION:
            with self.subTest(report=name):
                text = (reports / name).read_text(encoding="utf-8")
                self.assertRegex(
                    text, r"(?m)^## (후속 처리|반영 상태|반영 결과)",
                    f"{name}: 감사 섹션이 없다. PR #97에서 지워진 기록을 복구했으니 유지해야 한다",
                )

    def test_repository_dp_3_report_keeps_both_code_spans(self):
        text = (REPO_ROOT / "docs" / "reviews" / "2026-07-30-dp-3.md").read_text(encoding="utf-8")

        self.assertIn(
            "- quote: `int matrixChain(const vector<int>& d, int n)` / `d[i-1]*d[k]*d[j]`",
            text,
        )
        self.assertIn(
            "- quote: `① 3·2·4 = 24` / `② 3·4·2 = 24` / `24 + 24 = 48` / `16 + 12 = 28`",
            text,
        )


class TestLlmCoverage(unittest.TestCase):
    def _rows(self, rule_ids, source="L"):
        return [{
            "severity": "🟢", "source": source, "rule_id": rule_id,
            "location": "not-recorded", "quote": "not-recorded",
            "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
            "gate_effect": "info",
        } for rule_id in rule_ids]

    def test_full_l1_to_l7_coverage_has_no_gaps(self):
        rows = self._rows(["L1", "L2", "L3", "L4", "L5", "L6", "L7"])

        self.assertEqual(rp.missing_llm_coverage(rows), [])

    def test_reports_each_missing_category(self):
        rows = self._rows(["L1", "L2", "L4", "L7"])

        self.assertEqual(rp.missing_llm_coverage(rows), ["L3", "L5", "L6"])

    def test_deterministic_only_report_is_missing_every_category(self):
        rows = [{
            "severity": "🔴", "source": "D", "rule_id": "D1",
            "location": "a.md:7", "quote": "q", "message": "m",
            "recommendation": "r", "gate_effect": "fail",
        }]

        self.assertEqual(
            rp.missing_llm_coverage(rows),
            ["L1", "L2", "L3", "L4", "L5", "L6", "L7"],
        )

    def test_migrated_rows_do_not_count_as_llm_coverage(self):
        rows = self._rows(["L1", "L2", "L3", "L4", "L5", "L6", "L7"], source="MIGRATED")

        self.assertEqual(
            rp.missing_llm_coverage(rows),
            ["L1", "L2", "L3", "L4", "L5", "L6", "L7"],
        )

    def _post_rows(self, post, rule_ids=("L1", "L2", "L3", "L4", "L5", "L6", "L7")):
        rows = self._rows(rule_ids)
        for row in rows:
            row["location"] = f"src/content/posts/{post}.md:1-100"
        return rows

    def test_single_target_report_is_checked_report_wide(self):
        """포스트가 하나면 coverage row에 위치가 없어도 리포트 전체로 본다."""
        rows = self._rows(["L1", "L2", "L3", "L4", "L5", "L6", "L7"])
        rows.append({
            "severity": "🟡", "source": "D", "rule_id": "D3",
            "location": "src/content/posts/only.md:12", "quote": "q",
            "message": "m", "recommendation": "r", "gate_effect": "warn",
        })

        self.assertEqual(rp.missing_llm_coverage_by_target(rows), {})

    def test_multi_target_report_is_checked_per_post(self):
        rows = self._post_rows("alpha") + self._post_rows("beta", ("L1", "L2"))

        self.assertEqual(
            rp.missing_llm_coverage_by_target(rows),
            {"src/content/posts/beta.md": ["L3", "L4", "L5", "L6", "L7"]},
        )

    def test_post_without_any_llm_row_is_reported(self):
        rows = self._post_rows("alpha")
        rows.append({
            "severity": "🔴", "source": "D", "rule_id": "D1",
            "location": "src/content/posts/beta.md:7", "quote": "q",
            "message": "m", "recommendation": "r", "gate_effect": "fail",
        })

        self.assertEqual(
            list(rp.missing_llm_coverage_by_target(rows)),
            ["src/content/posts/beta.md"],
        )

    def test_svg_location_is_not_a_coverage_target(self):
        """L4는 SVG 경로를 가리킬 수 있다. SVG는 포스트가 아니므로 대상이 아니다."""
        rows = self._post_rows("alpha")
        rows[3]["location"] = "public/images/alpha/figure.svg:3"

        self.assertEqual(rp.missing_llm_coverage_by_target(rows), {})


class TestRepositoryGate(unittest.TestCase):
    """대상별 최신 리포트만 보는 읽기 전용 게이트."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def _report(self, name, findings, strict=True, target=None, migrated_from=None):
        import review_report as rr

        path = self.root / name
        path.write_text(
            rr.serialize_report(
                target=target or name[11:-3], generated_at=name[:10],
                strict=strict, findings=findings, migrated_from=migrated_from),
            encoding="utf-8",
        )
        return path

    def _coverage(self, slug, rule_ids=("L1", "L2", "L3", "L4", "L5", "L6", "L7")):
        return [{
            "severity": "🟢", "source": "L", "rule_id": rule_id,
            "location": f"src/content/posts/{slug}.md:1-100", "quote": "not-recorded",
            "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
            "gate_effect": "info",
        } for rule_id in rule_ids]

    def _red(self, slug):
        return {
            "severity": "🔴", "source": "L", "rule_id": "L7",
            "location": f"src/content/posts/{slug}.md:12", "quote": "인용",
            "message": "문제", "recommendation": "조치", "gate_effect": "fail",
        }

    def test_superseded_red_report_does_not_fail_the_gate(self):
        """과거 스냅샷의 🔴은 더 최신 리뷰가 초록이면 게이트를 막지 않는다."""
        self._report("2026-08-01-alpha.md", self._coverage("alpha") + [self._red("alpha")])
        self._report("2026-08-03-alpha.md", self._coverage("alpha"))

        rc, stdout, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 0, stdout + stderr)

    def test_latest_report_with_red_fails_the_gate(self):
        self._report("2026-08-01-alpha.md", self._coverage("alpha"))
        self._report("2026-08-03-alpha.md", self._coverage("alpha") + [self._red("alpha")])

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 1)
        self.assertIn("2026-08-03-alpha.md", stderr)

    def test_legacy_report_is_skipped_and_reported(self):
        """기준일 이전의 비정본 리포트는 면제하되 조용히 넘기지 않는다."""
        (self.root / "2026-06-01-legacy.md").write_text(
            "# 리뷰 리포트: legacy\n\n- [L7] 뭔가 문제\n", encoding="utf-8")

        rc, stdout, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 0, stderr)
        self.assertIn("2026-06-01-legacy.md", stdout + stderr)

    def test_v2_declaring_report_before_cutoff_is_still_enforced(self):
        """정본을 선언한 리포트는 기준일 이전이어도 되돌아갈 수 없다."""
        self._report("2026-06-01-beta.md", self._coverage("beta") + [self._red("beta")])

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 1)
        self.assertIn("2026-06-01-beta.md", stderr)

    def test_report_that_was_not_finalized_is_an_infra_failure(self):
        """summary가 낡은 리포트는 --finalize를 돌리지 않은 것이므로 exit 2다."""
        path = self._report("2026-08-03-alpha.md", self._coverage("alpha"))
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "summary: 🔴 0 · 🟡 0 · 🟢 7", "summary: 🔴 0 · 🟡 0 · 🟢 3"),
            encoding="utf-8",
        )

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 2)
        self.assertIn("정본", stderr)

    def test_missing_coverage_in_latest_report_is_an_infra_failure(self):
        self._report("2026-08-03-alpha.md",
                     self._coverage("alpha", ("L1", "L2", "L3", "L4", "L5", "L7")))

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 2)
        self.assertIn("L6", stderr)

    def test_missing_reports_directory_is_an_infra_failure(self):
        """경로를 잘못 적으면 CI가 아무것도 검사하지 않고 초록이 된다."""
        rc, stdout, stderr = run_main_streams([
            "review_post.py", "--gate", "--reports-dir", str(self.root / "없는경로"),
        ])

        self.assertEqual(rc, 2, stdout)
        self.assertIn("없는경로", stderr)

    def test_empty_reports_directory_is_an_infra_failure(self):
        """검사한 리포트가 0개면 게이트는 아무것도 보장하지 못한다. 통과로 읽히면 안 된다."""
        (self.root / "README.md").write_text("문서다\n", encoding="utf-8")

        rc, stdout, stderr = run_main_streams([
            "review_post.py", "--gate", "--reports-dir", str(self.root),
        ])

        self.assertEqual(rc, 2, stdout)
        self.assertIn("리포트", stderr)

    def test_gate_never_writes_to_reports(self):
        path = self._report("2026-08-03-alpha.md", self._coverage("alpha"))
        before = path.read_bytes()

        run_main_streams(["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(path.read_bytes(), before)

    def test_migrated_from_survives_finalize_and_the_gate(self):
        """provenance 헤더가 정본화에서 사라지면 게이트가 정본이 아니라고 판정한다."""
        path = self._report("2026-08-03-alpha.md", self._coverage("alpha"),
                            strict=False, migrated_from="legacy-prose")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--finalize", "--strict", str(path)])
        self.assertEqual(rc, 0, stderr)
        self.assertIn("migrated_from: legacy-prose", path.read_text(encoding="utf-8"))

        rc, stdout, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])
        self.assertEqual(rc, 0, stdout + stderr)

    def _migrated_rows(self, slug, severity="🟢", gate_effect="info"):
        return [{
            "severity": severity, "source": "MIGRATED", "rule_id": "L7",
            "location": f"src/content/posts/{slug}.md:9", "quote": "not-recorded",
            "message": "전환된 지적", "recommendation": "not-recorded",
            "gate_effect": gate_effect,
        }]

    def test_migrated_report_is_exempt_from_the_coverage_requirement(self):
        """레거시 전환분에는 L 비평 행이 없다. coverage를 요구하면 재리뷰를 강제한다."""
        self._report("2026-08-03-alpha.md", self._migrated_rows("alpha"),
                     strict=False, migrated_from="legacy-prose")

        rc, stdout, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 0, stdout + stderr)

    def test_migrated_report_is_not_exempt_from_the_red_check(self):
        """coverage만 면제한다. 🔴는 전환분에서도 게이트를 막는다."""
        self._report("2026-08-03-alpha.md",
                     self._migrated_rows("alpha", severity="🔴", gate_effect="fail"),
                     strict=False, migrated_from="legacy-prose")

        rc, _, stderr = run_main_streams(
            ["review_post.py", "--gate", "--reports-dir", str(self.root)])

        self.assertEqual(rc, 1)
        self.assertIn("2026-08-03-alpha.md", stderr)

    def test_gate_passes_on_the_repository_reports(self):
        """저장소의 실제 리포트에 게이트를 걸어 둔다. 🔴가 들어오면 여기서 먼저 깨진다."""
        rc, stdout, stderr = run_main_streams([
            "review_post.py", "--gate", "--reports-dir", str(REVIEW_REPORT_DIR),
        ])

        self.assertEqual(rc, 0, stdout + stderr)


class TestGateIsWiredIntoCI(unittest.TestCase):
    """게이트가 실행되는 곳이 없으면 신호가 아무것도 막지 못한다(#99)."""

    def _workflow_texts(self):
        workflows = REPO_ROOT / ".github" / "workflows"
        return {p.name: p.read_text(encoding="utf-8") for p in workflows.glob("*.yml")}

    def test_some_workflow_runs_the_gate(self):
        texts = self._workflow_texts()

        running = [name for name, text in texts.items() if "--gate" in text]
        self.assertTrue(running, f"워크플로 어디에도 --gate가 없다: {sorted(texts)}")

    def test_deploy_is_blocked_by_the_gate(self):
        text = self._workflow_texts().get("deploy.yml", "")

        self.assertIn("--gate", text, "배포 워크플로가 게이트를 통과하지 않는다")
        self.assertLess(text.index("--gate"), text.index("npm run build"),
                        "게이트는 빌드 전에 돌아야 한다")

    def test_pull_requests_run_the_gate(self):
        wired = [text for text in self._workflow_texts().values()
                 if "--gate" in text and "pull_request" in text]

        self.assertTrue(wired, "PR에서 게이트를 돌리는 워크플로가 없다")

    def test_package_json_exposes_the_gate_locally(self):
        package = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))

        scripts = package.get("scripts", {})
        self.assertTrue(any("--gate" in command for command in scripts.values()),
                        f"package.json에 게이트 실행 스크립트가 없다: {sorted(scripts)}")


class TestUnknownFlags(unittest.TestCase):
    """모르는 옵션은 경로가 아니라 오류다. 쓰기 전에 거부한다."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _report(self):
        path = self.root / "2026-08-05-alpha.md"
        path.write_text(rr.serialize_report(
            target="alpha", generated_at="2026-08-05", strict=False,
            findings=[{
                "severity": "🟢", "source": "L", "rule_id": rule,
                "location": "src/content/posts/alpha.md:1", "quote": "not-recorded",
                "message": "검토 완료, 이슈 없음", "recommendation": "not-recorded",
                "gate_effect": "info",
            } for rule in rp.REQUIRED_LLM_RULES],
        ), encoding="utf-8")
        return path

    def test_mistyped_strict_does_not_finalize_without_judging(self):
        """`--strcit`가 경로로 먹히면, 실패 코드와 함께 판정 없는 정본화가 일어난다."""
        report = self._report()
        before = report.read_bytes()

        rc, stdout, stderr = run_main_streams([
            "review_post.py", "--finalize", "--strcit", str(report),
        ])

        self.assertEqual(rc, 2, stdout)
        self.assertIn("--strcit", stderr)
        self.assertNotIn("정본화 완료", stdout)
        self.assertEqual(report.read_bytes(), before)

    def test_mistyped_gate_says_which_option_is_wrong(self):
        rc, _, stderr = run_main_streams(["review_post.py", "--gates"])

        self.assertEqual(rc, 2)
        self.assertIn("--gates", stderr)
        self.assertNotIn("No such file", stderr)

    def test_known_options_still_work(self):
        report = self._report()

        rc, stdout, _ = run_main_streams([
            "review_post.py", "--finalize", "--strict", str(report),
        ])

        self.assertEqual(rc, 0, stdout)


class TestGateEffectSingleSource(unittest.TestCase):
    def test_severity_to_gate_effect_has_one_definition(self):
        """대응이 갈라지면 validator가 migrate 산출물을 거부한다. 사본을 두지 않는다."""
        import review_report as rr

        self.assertIs(rp._GATE_BY_SEVERITY, rr.CANONICAL_GATE_EFFECT)
        self.assertEqual(
            rp._SEVERITY_BY_GATE,
            {gate: severity for severity, gate in rr.CANONICAL_GATE_EFFECT.items()},
        )
        self.assertEqual(
            rp.GATE_EFFECT,
            {label: rr.CANONICAL_GATE_EFFECT[icon]
             for label, icon in rp.SEVERITY_ICON.items()},
        )


class _HalfWriter:
    """받은 텍스트의 절반만 쓰고 실패하는 파일 핸들. 부분 쓰기를 주입한다."""

    def __init__(self, handle):
        self._handle = handle

    def write(self, text):
        self._handle.write(text[: len(text) // 2])
        raise OSError(28, "No space left on device")

    def flush(self):
        self._handle.flush()

    def fileno(self):
        return self._handle.fileno()

    def close(self):
        self._handle.close()

    @property
    def closed(self):
        return self._handle.closed


_REAL_FDOPEN = os.fdopen
_REAL_MKSTEMP = tempfile.mkstemp


def _half_writing_fdopen(*args, **kwargs):
    return _HalfWriter(_REAL_FDOPEN(*args, **kwargs))


def _recording_fdopen(handles):
    def fdopen(*args, **kwargs):
        handle = _REAL_FDOPEN(*args, **kwargs)
        handles.append(handle)
        return handle

    return fdopen


def _recording_mkstemp(descriptors):
    def mkstemp(*args, **kwargs):
        fd, name = _REAL_MKSTEMP(*args, **kwargs)
        descriptors.append(fd)
        return fd, name

    return mkstemp


def _failing_replace(exc, only=None):
    """`os.replace` 실패를 주입한다. only를 주면 그 경로에서만 실패한다."""
    real = os.replace

    def replace(src, dst, **kwargs):
        if only is None or str(dst).endswith(only):
            raise exc
        return real(src, dst, **kwargs)

    return replace


class TestAtomicReportWrite(unittest.TestCase):
    """리포트 교체는 파일별로 원자적이다. 실패하면 원본이 그대로 남아야 한다(#101)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _names(self, directory=None):
        return sorted(p.name for p in (directory or self.root).iterdir())

    def _v2_report(self, name="2026-08-02-alpha.md", target="alpha"):
        import review_report as rr

        report = self.root / name
        report.write_text(rr.serialize_report(
            target=target, generated_at="2026-08-02", strict=False,
            findings=[{
                "severity": "🟡", "source": "L", "rule_id": "L1",
                "location": f"src/content/posts/{target}.md:12",
                "quote": "줄표가 남발된다", "message": "줄표 남발",
                "recommendation": "마침표로 끊는다", "gate_effect": "warn",
            }],
            sources=[f"src/content/posts/{target}.md"],
        ), encoding="utf-8")
        return report

    def _legacy_report(self, name="2026-07-24-legacy.md"):
        report = self.root / name
        report.write_text(
            "🟢 참고 (1)\n\n"
            "- [L6] not-recorded · gate: info — 노션 원본과 대조했다.\n\n"
            "요약: 🔴 0 · 🟡 0 · 🟢 1\n",
            encoding="utf-8",
        )
        return report

    def test_atomic_write_replaces_content_and_leaves_no_temp_file(self):
        target = self.root / "report.md"
        target.write_text("옛 내용\n", encoding="utf-8")

        rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(target.read_text(encoding="utf-8"), "새 내용\n")
        self.assertEqual(self._names(), ["report.md"])

    def test_atomic_write_matches_path_write_text_bytes(self):
        """줄 끝 처리가 달라지면 정본화만 해도 저장소 전체 diff가 생긴다."""
        text = "첫 줄\n둘째 줄\n"
        expected = self.root / "expected.md"
        expected.write_text(text, encoding="utf-8")
        actual = self.root / "actual.md"

        rp.atomic_write_text(actual, text)

        self.assertEqual(actual.read_bytes(), expected.read_bytes())

    def test_atomic_write_keeps_the_line_endings_of_the_replaced_file(self):
        """저장소 리포트는 LF와 CRLF가 섞여 있다. 정본화가 줄 끝을 뒤집으면 전체 diff가 난다."""
        for name, ending in (("lf.md", b"\n"), ("crlf.md", b"\r\n")):
            with self.subTest(ending=ending):
                target = self.root / name
                target.write_bytes("옛 내용".encode("utf-8") + ending)

                rp.atomic_write_text(target, "첫 줄\n둘째 줄\n")

                data = target.read_bytes()
                self.assertEqual(data.count(b"\r\n"), 2 if ending == b"\r\n" else 0, name)
                self.assertEqual(data.count(b"\n"), 2, name)

    def test_atomic_write_keeps_the_permissions_of_the_replaced_file(self):
        """임시 파일은 0600으로 생긴다. 그대로 교체하면 리포트 권한이 좁아진다."""
        target = self.root / "report.md"
        target.write_text("옛 내용\n", encoding="utf-8")
        before = target.stat().st_mode & 0o777

        rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(target.stat().st_mode & 0o777, before)

    def test_atomic_write_keeps_the_target_intact_when_the_write_fails(self):
        target = self.root / "report.md"
        target.write_text("원본 근거\n", encoding="utf-8")
        original = target.read_bytes()

        with mock.patch("os.fdopen", _half_writing_fdopen):
            with self.assertRaises(OSError):
                rp.atomic_write_text(target, "새 내용이 아주 길어서 절반만 써진다\n")

        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(self._names(), ["report.md"])

    def test_atomic_write_keeps_the_target_intact_when_replace_fails(self):
        target = self.root / "report.md"
        target.write_text("원본 근거\n", encoding="utf-8")
        original = target.read_bytes()

        with mock.patch("os.replace", _failing_replace(OSError(13, "Permission denied"))):
            with self.assertRaises(OSError):
                rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(self._names(), ["report.md"])

    def test_atomic_write_cleans_up_when_interrupted(self):
        """프로세스 중단(KeyboardInterrupt)은 Exception이 아니다. 임시 파일이 남으면 안 된다."""
        target = self.root / "report.md"
        target.write_text("원본 근거\n", encoding="utf-8")

        with mock.patch("os.replace", _failing_replace(KeyboardInterrupt())):
            with self.assertRaises(KeyboardInterrupt):
                rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(target.read_text(encoding="utf-8"), "원본 근거\n")
        self.assertEqual(self._names(), ["report.md"])

    def test_atomic_write_closes_the_handle_when_interrupted_before_replace(self):
        """임시 파일을 지우려면 먼저 닫아야 한다. 열린 파일은 Windows에서 지워지지 않는다."""
        target = self.root / "report.md"
        target.write_text("원본 근거\n", encoding="utf-8")
        handles = []

        with mock.patch("os.fdopen", _recording_fdopen(handles)), \
             mock.patch("os.chmod", side_effect=KeyboardInterrupt()):
            with self.assertRaises(KeyboardInterrupt):
                rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(len(handles), 1, "임시 파일 핸들이 열리지 않았다")
        self.assertTrue(handles[0].closed, "중단 뒤에도 임시 파일 핸들이 열려 있다")
        self.assertEqual(target.read_text(encoding="utf-8"), "원본 근거\n")
        self.assertEqual(self._names(), ["report.md"])

    def test_atomic_write_closes_the_descriptor_when_the_handle_cannot_be_opened(self):
        """os.fdopen이 실패하면 raw descriptor 소유권이 아직 우리에게 있다."""
        target = self.root / "report.md"
        target.write_text("원본 근거\n", encoding="utf-8")
        descriptors, closed = [], []
        real_close = os.close

        def recording_close(fd):
            closed.append(fd)
            return real_close(fd)

        with mock.patch("tempfile.mkstemp", _recording_mkstemp(descriptors)), \
             mock.patch("os.fdopen", side_effect=KeyboardInterrupt()), \
             mock.patch("os.close", recording_close):
            with self.assertRaises(KeyboardInterrupt):
                rp.atomic_write_text(target, "새 내용\n")

        self.assertEqual(len(descriptors), 1, "임시 파일이 만들어지지 않았다")
        self.assertIn(descriptors[0], closed, "raw descriptor가 닫히지 않았다")
        self.assertEqual(target.read_text(encoding="utf-8"), "원본 근거\n")
        self.assertEqual(self._names(), ["report.md"])

    def test_finalize_keeps_the_original_when_the_replacement_fails(self):
        report = self._v2_report()
        original = report.read_bytes()

        with mock.patch("os.replace", _failing_replace(OSError(28, "No space left on device"))):
            rc, _, stderr = run_main_streams(["review_post.py", "--finalize", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("쓰기 실패", stderr)
        self.assertEqual(report.read_bytes(), original)
        self.assertEqual(self._names(), [report.name])

    def test_migrate_keeps_the_original_when_the_replacement_fails(self):
        report = self._legacy_report()
        original = report.read_bytes()

        with mock.patch("os.replace", _failing_replace(OSError(28, "No space left on device"))):
            rc, _, stderr = run_main_streams(["review_post.py", "--migrate", str(report)])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("쓰기 실패", stderr)
        self.assertEqual(report.read_bytes(), original)
        self.assertEqual(self._names(), [report.name])

    def test_batch_finalize_applies_per_file_and_names_the_failing_file(self):
        """정책은 파일별 원자성이다. batch all-or-nothing이 아니므로 성공분은 남는다."""
        first = self._v2_report("2026-08-02-alpha.md", "alpha")
        second = self._v2_report("2026-08-02-beta.md", "beta")
        # 요약을 지워 두면 정본화가 실제로 일어났는지 내용으로 확인할 수 있다.
        for report in (first, second):
            report.write_text(
                report.read_text(encoding="utf-8").replace("summary: 🔴 0 · 🟡 1 · 🟢 0",
                                                           "summary: 🔴 9 · 🟡 9 · 🟢 9"),
                encoding="utf-8",
            )
        stale = second.read_bytes()

        with mock.patch("os.replace",
                        _failing_replace(OSError(28, "No space left"), only="beta.md")):
            rc, _, stderr = run_main_streams([
                "review_post.py", "--finalize", str(first), str(second),
            ])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("summary: 🔴 0 · 🟡 1 · 🟢 0", first.read_text(encoding="utf-8"))
        self.assertEqual(second.read_bytes(), stale)
        self.assertIn(second.name, stderr)
        self.assertEqual(self._names(), [first.name, second.name])

    def test_scaffold_write_leaves_no_temp_file_when_replace_fails(self):
        post = self.root / "posts" / "alpha.md"
        post.parent.mkdir(parents=True, exist_ok=True)
        post.write_text("---\ntitle: T\n---\n본문이다.\n", encoding="utf-8")
        output_dir = self.root / "reports"

        with mock.patch("os.replace", _failing_replace(OSError(28, "No space left"))):
            rc, _, stderr = run_main_streams([
                "review_post.py", "--write-reports", "--output-dir", str(output_dir),
                "--date", "2026-08-04", str(post),
            ])

        self.assertEqual(rc, 2, stderr)
        self.assertIn("쓰기 실패", stderr)
        self.assertEqual(self._names(output_dir), [])

    def test_readme_documents_the_write_policy(self):
        text = (REPO_ROOT / "docs" / "reviews" / "README.md").read_text(encoding="utf-8")
        for term in ("os.replace", "임시 파일", "파일별 원자성", "byte-identical"):
            self.assertIn(term, text)


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
