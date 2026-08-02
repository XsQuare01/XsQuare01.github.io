import unittest

import review_report as rr


def finding(**overrides):
    base = {
        "severity": "🔴",
        "source": "D",
        "rule_id": "D1",
        "location": "src/content/posts/a.md:7",
        "quote": "트리가 **DAG)**가",
        "message": "깨진 굵게",
        "recommendation": "닫는 별표 앞 구두점을 옮긴다",
        "gate_effect": "fail",
    }
    base.update(overrides)
    return base


class TestSerializeFinding(unittest.TestCase):
    def test_emits_eight_fields_in_canonical_order_without_bold(self):
        block = rr.serialize_finding(finding())

        self.assertEqual(block.splitlines(), [
            "### 🔴 [D1] src/content/posts/a.md:7",
            "",
            "- severity: 🔴",
            "- source: D",
            "- rule_id: D1",
            "- location: src/content/posts/a.md:7",
            "- quote: 트리가 **DAG)**가",
            "- message: 깨진 굵게",
            "- recommendation: 닫는 별표 앞 구두점을 옮긴다",
            "- gate_effect: fail",
        ])

    def test_missing_field_becomes_not_recorded_not_omitted(self):
        block = rr.serialize_finding(finding(quote=""))

        self.assertIn("- quote: not-recorded", block)


class TestSummary(unittest.TestCase):
    def test_counts_every_severity_even_when_zero(self):
        counts = rr.summary_counts([finding(), finding(severity="🟡")])

        self.assertEqual(counts, {"🔴": 1, "🟡": 1, "🟢": 0})

    def test_format_summary_matches_schema_line(self):
        line = rr.format_summary({"🔴": 1, "🟡": 4, "🟢": 4})

        self.assertEqual(line, "🔴 1 · 🟡 4 · 🟢 4")


class TestSerializeReport(unittest.TestCase):
    def test_header_field_order_and_trailing_newline(self):
        text = rr.serialize_report(
            target="a",
            generated_at="2026-08-02",
            strict=False,
            findings=[finding()],
            sources=["src/content/posts/a.md"],
        )

        self.assertEqual(text.splitlines()[:6], [
            "schema_version: review-report/v2",
            "target: a",
            "generated_at: 2026-08-02",
            "strict: false",
            "sources: src/content/posts/a.md",
            "summary: 🔴 1 · 🟡 0 · 🟢 0",
        ])
        self.assertIn("\n## Findings\n", text)
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))

    def test_findings_sorted_by_severity_then_source_then_rule(self):
        text = rr.serialize_report(
            target="a", generated_at="2026-08-02", strict=False,
            findings=[
                finding(severity="🟢", source="L", rule_id="L2", gate_effect="info"),
                finding(severity="🔴", source="L", rule_id="L7", gate_effect="fail"),
                finding(severity="🔴", source="D", rule_id="D1", gate_effect="fail"),
            ],
        )

        self.assertEqual(
            [l for l in text.splitlines() if l.startswith("### ")],
            [
                "### 🔴 [D1] src/content/posts/a.md:7",
                "### 🔴 [L7] src/content/posts/a.md:7",
                "### 🟢 [L2] src/content/posts/a.md:7",
            ],
        )

    def test_same_input_produces_identical_bytes(self):
        kwargs = dict(target="a", generated_at="2026-08-02", strict=True,
                      findings=[finding(), finding(severity="🟡", gate_effect="warn")])

        self.assertEqual(rr.serialize_report(**kwargs), rr.serialize_report(**kwargs))

    def test_zero_findings_still_emits_findings_heading_and_summary(self):
        text = rr.serialize_report(target="clean", generated_at="2026-08-02",
                                   strict=False, findings=[])

        self.assertIn("summary: 🔴 0 · 🟡 0 · 🟢 0", text)
        self.assertIn("## Findings", text)


class TestParseReport(unittest.TestCase):
    def test_round_trip_is_byte_identical(self):
        original = rr.serialize_report(
            target="a", generated_at="2026-08-02", strict=False,
            findings=[finding(), finding(severity="🟡", rule_id="L1",
                                         source="L", gate_effect="warn")],
            sources=["src/content/posts/a.md"],
        )

        parsed = rr.parse_report(original)
        again = rr.serialize_report(
            target=parsed["header"]["target"],
            generated_at=parsed["header"]["generated_at"],
            strict=parsed["header"]["strict"],
            findings=parsed["findings"],
            sources=parsed["header"].get("sources", []),
        )

        self.assertEqual(original, again)

    def test_accepts_bold_field_markup_on_input(self):
        text = (
            "schema_version: review-report/v2\n"
            "target: a\ngenerated_at: 2026-07-28\nstrict: false\n"
            "summary: 🔴 0 · 🟡 1 · 🟢 0\n\n"
            "## Findings\n\n"
            "### 🟡 [L4] src/content/posts/a.md:73\n\n"
            "- **severity**: 🟡\n"
            "- **source**: L\n"
            "- **rule_id**: L4\n"
            "- **location**: `src/content/posts/a.md:73`\n"
            "- **quote**: \"겹치지 않고\"\n"
            "- **message**: 본문과 SVG가 어긋난다\n"
            "- **recommendation**: 문장을 고친다\n"
            "- **gate_effect**: warn\n"
        )

        parsed = rr.parse_report(text)

        self.assertEqual(len(parsed["findings"]), 1)
        self.assertEqual(parsed["findings"][0]["severity"], "🟡")
        self.assertEqual(parsed["findings"][0]["location"], "src/content/posts/a.md:73")
        self.assertEqual(parsed["findings"][0]["gate_effect"], "warn")

    def test_legacy_prose_report_parses_to_zero_findings(self):
        text = (
            "## 결정적 검사: src/content/posts/dp-1.md\n발견 사항 없음 ✅\n\n"
            "🟢 참고 (1)\n\n"
            "- [L6] not-recorded · gate: info — 노션 원본과 대조했다.\n\n"
            "요약: 🔴 0 · 🟡 0 · 🟢 1\n"
        )

        parsed = rr.parse_report(text)

        self.assertEqual(parsed["findings"], [])
        self.assertEqual(parsed["header"], {})


class TestValidateReport(unittest.TestCase):
    def test_canonical_complete_report_has_no_errors(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[finding()])

        self.assertEqual(rr.validate_report(text), [])

    def test_complete_state_rejects_zero_findings(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[])

        errors = rr.validate_report(text, state="complete")

        self.assertTrue(any("finding" in e for e in errors), errors)

    def test_scaffold_state_allows_zero_findings(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[])

        self.assertEqual(rr.validate_report(text, state="scaffold"), [])

    def test_reports_missing_header_fields(self):
        errors = rr.validate_report("## Findings\n", state="scaffold")

        self.assertTrue(any("schema_version" in e for e in errors), errors)
        self.assertTrue(any("target" in e for e in errors), errors)

    def test_reports_stale_summary_line(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[finding()])
        stale = text.replace("summary: 🔴 1 · 🟡 0 · 🟢 0",
                             "summary: 🔴 0 · 🟡 0 · 🟢 0")

        errors = rr.validate_report(stale)

        self.assertTrue(any("summary" in e for e in errors), errors)

    def test_rejects_severity_and_gate_effect_mismatch(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[finding()])
        sneaky = text.replace("- gate_effect: fail", "- gate_effect: info")

        errors = rr.validate_report(sneaky)

        self.assertTrue(any("gate_effect" in e and "severity" in e for e in errors), errors)

    def test_accepts_canonical_severity_gate_pairs(self):
        findings = [
            finding(severity="🔴", gate_effect="fail"),
            finding(severity="🟡", rule_id="L1", source="L", gate_effect="warn"),
            finding(severity="🟢", rule_id="L2", source="L", gate_effect="info"),
        ]
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=findings)

        self.assertEqual(rr.validate_report(text), [])

    def test_reports_invalid_enum_values(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[finding()])
        broken = text.replace("- gate_effect: fail", "- gate_effect: explode")

        errors = rr.validate_report(broken)

        self.assertTrue(any("gate_effect" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
