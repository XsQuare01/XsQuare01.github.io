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


if __name__ == "__main__":
    unittest.main()
