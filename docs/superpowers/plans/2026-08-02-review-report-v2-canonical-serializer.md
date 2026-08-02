# review-report/v2 정본 Markdown serializer 통합 (#84) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `review-report/v2` Markdown의 구조·필드 순서·공백을 결정하는 단일 정본 serializer/parser/validator를 만들고, scaffold 경로·완료 경로·과거 보고서를 모두 그 계약 하나로 수렴시킨다.

**Architecture:** 새 모듈 `.claude/review_report.py`가 v2 계약의 유일한 소유자다. 직렬화(`serialize_report`), 파싱(`parse_report`), 검증(`validate_report`)을 한곳에 두고, `review_post.py`는 이 모듈을 import해서 쓰기만 한다. 보고서는 두 가지 유효 상태를 갖는다 — Python이 만드는 **scaffold**(결정적 finding만, finding 0건 허용)와 LLM 비평 추가 후 `--finalize`가 재직렬화한 **complete**(finding 1건 이상 필수). 과거 보고서는 일괄 재작성이 아니라 명시적 `--migrate` 경로로만 전환하며, 확보 불가능한 근거는 `not-recorded`로 정직하게 남긴다.

**Tech Stack:** Python 3.11 표준 라이브러리만 (외부 의존성 금지 — 기존 `review_post.py` 규약). 테스트는 `unittest` + `pytest` 러너.

## Global Constraints

- 표준 라이브러리 외 의존성 추가 금지. `review_post.py` docstring의 "표준 라이브러리만 사용한다" 규약을 유지한다.
- CLI 진입점은 `python .claude/review_post.py` 그대로 유지한다. 커맨드 파일(`.claude/commands/*.md`)이 이 경로를 호출한다.
- 정본 finding 필드는 정확히 8개이며 순서 고정: `severity`, `source`, `rule_id`, `location`, `quote`, `message`, `recommendation`, `gate_effect`.
- 정본 severity 값: `🔴`, `🟡`, `🟢`. source 값: `D`, `L`, `MIGRATED`. gate_effect 값: `fail`, `warn`, `info`.
- finding 정렬 순서: severity(`🔴`→`🟡`→`🟢`) → source(`D`→`L`→`MIGRATED`) → rule_id → file path → line.
- 근거 없는 값을 지어내지 않는다. 없으면 `not-recorded`.
- 같은 입력은 항상 바이트 단위로 같은 Markdown을 만든다(결정적 overwrite).
- 파일은 항상 개행 하나로 끝난다. 블록 사이 빈 줄은 정확히 하나.
- **비범위(이 플랜에서 건드리지 않는다):** L1–L7 루브릭 의미 변경(#87/#88), strict gate exit code 로직 변경(#85). Task 4의 `--finalize`는 요약 재계산까지만 하고 exit code 계약은 현행 유지한다.

---

## File Structure

| 파일 | 책임 |
|---|---|
| `.claude/review_report.py` (신규) | v2 계약의 유일한 소유자 — 상수, 직렬화, 파싱, 검증, 정렬, 요약 |
| `.claude/test_review_report.py` (신규) | 위 모듈의 단위 테스트 (round-trip, 결정성, 검증 오류) |
| `.claude/review_post.py` (수정) | 검사 로직 유지. 직렬화/정렬/요약은 새 모듈에 위임. `--finalize`·`--migrate` 추가 |
| `.claude/test_review_post.py` (수정) | scaffold 출력 형식 기대치 갱신. 기존 v2 스키마 테스트는 **수정하지 않는다**(수용 기준) |
| `docs/reviews/README.md` (수정) | 정본 순서·공백 정책·scaffold/complete 두 상태·마이그레이션 절차 문서화 |
| `.claude/commands/review-post.md` (수정) | `--finalize` 단계와 plain(굵게 없는) 필드 표기 규약 반영 |
| `.claude/commands/review-post-all.md` (수정) | 위와 동일 |
| `docs/reviews/*.md` (마이그레이션 대상 30개) | Task 5에서 `--migrate`로 전환 |

---

## 현재 상태 (측정값, 2026-08-02 main `e89ce33` 기준)

```
python -m pytest .claude/test_review_post.py -q
→ 30 failed, 57 passed
```

30개 실패 전부 `TestReportSchemaV2::test_all_existing_review_reports_conform_to_v2_schema` 하나의 subtest다. `docs/reviews/` 36개 보고서(README 제외) 중:

| 형식 | 개수 | 문제 |
|---|---|---|
| 정본 준수 (`## Findings` + plain 필드 + 헤더 5줄) | 6 | 통과 |
| 헤더 일부만 (`- target:` 처럼 `- ` 접두 포함) | 4 | `^target:` 정규식 불일치 |
| 굵게 필드 (`- **severity**: 🟡`) | 2 | 테스트 파서가 필드로 인식 못 함 → 빈 finding |
| 레거시 산문 불릿 (`- [L6] not-recorded · gate: info — …`) | 24 | 헤더·`## Findings`·필드 전부 없음 |

핵심: **`write_markdown_report()`는 테스트가 요구하는 형식을 한 번도 만든 적이 없다.** 현재 scaffold 출력은 `## 결정적 검사: <path>` + `- [D1] <loc>  <msg>` + `요약: …`뿐이고, 정본 헤더와 `## Findings`, `###` finding 블록은 사람이 손으로 붙여 왔다. 통과하는 6개는 LLM이 수동으로 정확히 맞춘 결과물이다. 이것이 #84가 말하는 "스키마 문서와 테스트가 주장하는 정본 계약 ↔ Python 생성기 ↔ 실제 저장 보고서" 3자 불일치다.

## 정본 Markdown 형식 (이 플랜이 확정하는 계약)

```
schema_version: review-report/v2
target: dp-3-traceback
generated_at: 2026-07-31
strict: false
sources: src/content/posts/dp-3-traceback.md
summary: 🔴 1 · 🟡 0 · 🟢 0

## Findings

### 🔴 [L7] src/content/posts/dp-3-traceback.md:106

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/dp-3-traceback.md:106
- quote: 복원은 `split` 표를 요구한다.
- message: 제시한 방법에서 `split`은 분할점을 상수 시간에 찾는 데 필요하지만, 복원 자체의 필수 조건은 아니다.
- recommendation: 주장을 한정하고, `m`과 `d`에서 `k`를 다시 계산할 수 있다고 설명한다.
- gate_effect: fail
```

기존 통과 보고서 6개와 호환되도록 헤더 5줄·`## Findings`·`###` 블록·plain 필드 표기를 그대로 따른다. `sources:`만 새로 추가하는 **선택 필드**다(scaffold는 항상 출력, validator는 없어도 통과). 이유: finding이 0건인 clean 포스트의 scaffold에도 검토 대상 경로가 남아야 하고(`test_write_reports_uses_output_dir_and_date_for_each_target`가 `alpha.md` 문자열 존재를 요구), #85의 gate가 대상 목록을 기계적으로 읽을 수 있어야 한다.

### 두 가지 유효 상태

| 상태 | 생성 주체 | finding 개수 | `summary` |
|---|---|---|---|
| **scaffold** | `--write-reports` | 0건 허용 | 결정적 finding만 집계 |
| **complete** | LLM이 `###` 블록 추가 후 `--finalize` | 1건 이상 필수 | 결정적 + LLM 전체 재집계 |

`docs/reviews/`에 최종 저장되는 것은 complete 상태다. scaffold는 중간 산출물이며, `--finalize`를 거치지 않은 보고서는 validator가 미완료로 표시한다.

---

### Task 1: 정본 상수·직렬화 모듈

**Files:**
- Create: `.claude/review_report.py`
- Test: `.claude/test_review_report.py`

**Interfaces:**
- Consumes: 없음 (최초 태스크)
- Produces:
  - `SCHEMA_VERSION: str`, `NOT_RECORDED: str`
  - `FINDING_FIELDS: tuple[str, ...]` (8개, 정본 순서)
  - `SEVERITY_VALUES`, `SOURCE_VALUES`, `GATE_EFFECT_VALUES: tuple[str, ...]`
  - `summary_counts(findings: list[dict]) -> dict[str, int]`
  - `format_summary(counts: dict[str, int]) -> str`
  - `finding_sort_key(finding: dict) -> tuple`
  - `serialize_finding(finding: dict) -> str`
  - `serialize_report(*, target, generated_at, strict, findings, sources=()) -> str`

- [ ] **Step 1: Write the failing test**

`.claude/test_review_report.py` 신규 생성:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_report.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'review_report'`

- [ ] **Step 3: Write minimal implementation**

`.claude/review_report.py` 신규 생성:

```python
#!/usr/bin/env python3
"""review-report/v2 정본 직렬화·파싱·검증. 표준 라이브러리만 사용한다.

Markdown 리포트의 구조와 필드 순서를 결정하는 유일한 모듈이다.
같은 입력은 항상 같은 Markdown을 만든다.
"""

SCHEMA_VERSION = "review-report/v2"
NOT_RECORDED = "not-recorded"
FINDINGS_HEADING = "## Findings"

FINDING_FIELDS = (
    "severity",
    "source",
    "rule_id",
    "location",
    "quote",
    "message",
    "recommendation",
    "gate_effect",
)
SEVERITY_VALUES = ("🔴", "🟡", "🟢")
SOURCE_VALUES = ("D", "L", "MIGRATED")
GATE_EFFECT_VALUES = ("fail", "warn", "info")

_SEVERITY_RANK = {value: i for i, value in enumerate(SEVERITY_VALUES)}
_SOURCE_RANK = {value: i for i, value in enumerate(SOURCE_VALUES)}


def _value(finding, field):
    raw = finding.get(field, "")
    text = str(raw).strip() if raw is not None else ""
    return text or NOT_RECORDED


def summary_counts(findings):
    counts = {severity: 0 for severity in SEVERITY_VALUES}
    for finding in findings:
        severity = _value(finding, "severity")
        if severity in counts:
            counts[severity] += 1
    return counts


def format_summary(counts):
    return " · ".join(f"{severity} {counts.get(severity, 0)}" for severity in SEVERITY_VALUES)


def finding_sort_key(finding):
    location = _value(finding, "location")
    file_part, line_part = location, 0
    if ":" in location:
        head, tail = location.rsplit(":", 1)
        if tail.isdigit():
            file_part, line_part = head, int(tail)
    return (
        _SEVERITY_RANK.get(_value(finding, "severity"), len(SEVERITY_VALUES)),
        _SOURCE_RANK.get(_value(finding, "source"), len(SOURCE_VALUES)),
        _value(finding, "rule_id"),
        file_part,
        line_part,
    )


def serialize_finding(finding):
    heading = "### {} [{}] {}".format(
        _value(finding, "severity"),
        _value(finding, "rule_id"),
        _value(finding, "location"),
    )
    lines = [heading, ""]
    lines += [f"- {field}: {_value(finding, field)}" for field in FINDING_FIELDS]
    return "\n".join(lines)


def serialize_report(*, target, generated_at, strict, findings, sources=()):
    rows = sorted(findings, key=finding_sort_key)
    header = [
        f"schema_version: {SCHEMA_VERSION}",
        f"target: {target or NOT_RECORDED}",
        f"generated_at: {generated_at or NOT_RECORDED}",
        f"strict: {_strict_text(strict)}",
    ]
    if sources:
        header.append("sources: " + ", ".join(sources))
    header.append(f"summary: {format_summary(summary_counts(rows))}")

    blocks = ["\n".join(header), FINDINGS_HEADING]
    blocks += [serialize_finding(row) for row in rows]
    return "\n\n".join(blocks) + "\n"


def _strict_text(strict):
    if isinstance(strict, bool):
        return "true" if strict else "false"
    text = str(strict).strip()
    return text or NOT_RECORDED
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_report.py -q`
Expected: PASS (8 tests)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_report.py .claude/test_review_report.py
git commit -m "feat(review): review-report/v2 정본 serializer 모듈 추가"
```

---

### Task 2: 정본 parser + validator (round-trip 보장)

**Files:**
- Modify: `.claude/review_report.py`
- Test: `.claude/test_review_report.py`

**Interfaces:**
- Consumes: Task 1의 `serialize_report`, `FINDING_FIELDS`, `SEVERITY_VALUES`, `SOURCE_VALUES`, `GATE_EFFECT_VALUES`, `summary_counts`, `format_summary`
- Produces:
  - `parse_report(text: str) -> dict` — `{"header": dict, "findings": list[dict]}`
  - `validate_report(text: str, *, state: str = "complete") -> list[str]` — 오류 메시지 목록, 빈 리스트면 유효. `state`는 `"scaffold"` 또는 `"complete"`

파서는 **굵게 표기(`- **severity**: …`)를 입력으로 허용**하되, serializer는 항상 plain으로만 출력한다. 이래야 Task 5에서 굵게 형식 보고서 2개를 근거 손실 없이 재포맷할 수 있다.

- [ ] **Step 1: Write the failing test**

`.claude/test_review_report.py`에 추가:

```python
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

    def test_reports_invalid_enum_values(self):
        text = rr.serialize_report(target="a", generated_at="2026-08-02",
                                   strict=False, findings=[finding()])
        broken = text.replace("- gate_effect: fail", "- gate_effect: explode")

        errors = rr.validate_report(broken)

        self.assertTrue(any("gate_effect" in e for e in errors), errors)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_report.py -q`
Expected: FAIL — `AttributeError: module 'review_report' has no attribute 'parse_report'`

- [ ] **Step 3: Write minimal implementation**

`.claude/review_report.py` 상단 import에 `import re`를 추가하고, 파일 끝에 이어붙인다:

```python
_HEADER_KEYS = ("schema_version", "target", "generated_at", "strict", "sources", "summary")
_HEADER_RE = re.compile(r"^(" + "|".join(_HEADER_KEYS) + r"): (.*)$")
_FIELD_RE = re.compile(
    r"^- \*{0,2}(" + "|".join(FINDING_FIELDS) + r")\*{0,2}: ?(.*)$"
)


def _clean_field_value(raw):
    text = raw.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        text = text[1:-1].strip()
    return text or NOT_RECORDED


def parse_report(text):
    header = {}
    findings = []
    current = None
    in_findings = False

    for line in text.splitlines():
        if not in_findings:
            match = _HEADER_RE.match(line)
            if match:
                key, value = match.group(1), match.group(2).strip()
                header[key] = [s.strip() for s in value.split(",") if s.strip()] \
                    if key == "sources" else value
                continue
            if line.strip() == FINDINGS_HEADING:
                in_findings = True
            continue

        if line.startswith("### "):
            if current:
                findings.append(current)
            current = {}
            continue
        if current is None:
            continue
        match = _FIELD_RE.match(line)
        if match:
            current[match.group(1)] = _clean_field_value(match.group(2))

    if current:
        findings.append(current)
    return {"header": header, "findings": findings}


def validate_report(text, *, state="complete"):
    errors = []
    parsed = parse_report(text)
    header, findings = parsed["header"], parsed["findings"]

    if header.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for key in ("target", "generated_at", "strict", "summary"):
        if not header.get(key):
            errors.append(f"missing required header field: {key}")
    if FINDINGS_HEADING not in text:
        errors.append(f"missing section: {FINDINGS_HEADING}")

    if state == "complete" and not findings:
        errors.append("complete report must contain at least one finding")

    for index, finding in enumerate(findings):
        missing = [f for f in FINDING_FIELDS if f not in finding]
        if missing:
            errors.append(f"finding #{index + 1} missing fields: {', '.join(missing)}")
            continue
        if finding["severity"] not in SEVERITY_VALUES:
            errors.append(f"finding #{index + 1} invalid severity: {finding['severity']}")
        if finding["source"] not in SOURCE_VALUES:
            errors.append(f"finding #{index + 1} invalid source: {finding['source']}")
        if finding["gate_effect"] not in GATE_EFFECT_VALUES:
            errors.append(f"finding #{index + 1} invalid gate_effect: {finding['gate_effect']}")

    expected = format_summary(summary_counts(findings))
    if header.get("summary") and header["summary"] != expected:
        errors.append(f"summary is stale: header={header['summary']} computed={expected}")

    return errors
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_report.py -q`
Expected: PASS (17 tests)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_report.py .claude/test_review_report.py
git commit -m "feat(review): v2 정본 parser·validator 추가 (round-trip 보장)"
```

---

### Task 3: scaffold writer를 정본 serializer로 교체

**Files:**
- Modify: `.claude/review_post.py:604-623` (`_summary`, `_finding_sort_key` 제거), `:626-689` (`report_to_json_v2`, `format_report`, `write_markdown_report`)
- Modify: `.claude/test_review_post.py:408-433` (`test_write_reports_uses_output_dir_and_date_for_each_target`)

**Interfaces:**
- Consumes: Task 1–2의 `review_report.serialize_report`, `finding_sort_key`, `summary_counts`, `format_summary`
- Produces:
  - `write_markdown_report(output_dir, report_date, path, findings, strict=False) -> Path` — 정본 scaffold를 쓴다 (`strict` 인자 추가)
  - `finding_to_report_v2`는 시그니처·반환 형태 그대로 유지 (기존 테스트가 의존)

`format_report()`는 **stdout 사람용 출력 전용**으로 남긴다(파일 출력과 분리). 파일은 오직 `serialize_report`만 만든다 — 이것이 "하나의 serializer만 v2 Markdown 구조와 필드 순서를 결정한다"는 완료 기준이다.

- [ ] **Step 1: Write the failing test**

`.claude/test_review_post.py`의 `test_write_reports_uses_output_dir_and_date_for_each_target`를 아래로 교체하고, 그 뒤에 새 테스트 두 개를 추가한다:

```python
    def test_write_reports_uses_output_dir_and_date_for_each_target(self):
        first = write_post(self.root / "posts" / "alpha.md", "본문")
        second = write_post(self.root / "posts" / "beta.md", "트리가 **DAG)**가 된다")
        output_dir = self.root / "reports"

        rc, stdout = run_main([
            "review_post.py", "--write-reports",
            "--output-dir", str(output_dir),
            "--date", "2026-06-07",
            str(first), str(second),
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
        self.assertIn("summary: 🔴 1 · 🟡 0 · 🟢 0", text)
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestCliContractsV2 -q`
Expected: FAIL — `test_scaffold_output_is_canonical_and_validates_as_scaffold`에서 첫 줄이 `## 결정적 검사: …`라 `schema_version: …`과 불일치

- [ ] **Step 3: Write minimal implementation**

`.claude/review_post.py`에서 `_summary`와 `_finding_sort_key` 정의(604–623행)를 삭제하고, import 블록(13행 `from pathlib import Path` 아래)에 추가:

```python
import review_report as rr
```

삭제한 두 함수 자리에 위임 래퍼를 둔다(기존 호출부 유지):

```python
def _summary(findings):
    return rr.summary_counts([{"severity": severity_icon(f.severity)} for f in findings])


def _finding_sort_key(row):
    return rr.finding_sort_key(row)
```

`write_markdown_report`를 교체한다:

```python
def write_markdown_report(output_dir, report_date, path, findings, strict=False):
    out_path = report_path_for(output_dir, report_date, path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [finding_to_report_v2(path, f) for f in findings]
    out_path.write_text(
        rr.serialize_report(
            target=Path(path).stem,
            generated_at=report_date,
            strict=strict,
            findings=rows,
            sources=[str(path)],
        ),
        encoding="utf-8",
    )
    return out_path
```

`main()`의 호출부(767행)를 `strict`를 넘기도록 고친다:

```python
                written_report_paths.append(
                    write_markdown_report(output_dir, report_date, p, findings, strict=opts["strict"])
                )
```

`report_to_json_v2`의 `generated_at`은 더 이상 무조건 `not-recorded`가 아니어야 한다 — Markdown과 같은 값을 쓴다. 시그니처에 `generated_at`을 추가한다:

```python
def report_to_json_v2(paths, results, strict=False, generated_at=rr.NOT_RECORDED):
```

그리고 본문의 `"generated_at": "not-recorded",`를 `"generated_at": generated_at,`으로 바꾼 뒤, `main()`의 호출부(775행)를 고친다:

```python
            print(json.dumps(
                report_to_json_v2(paths, results, strict=opts["strict"], generated_at=report_date),
                ensure_ascii=False, indent=2,
            ))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q`
Expected: `TestCliContractsV2`·`TestReportSchemaV2`의 JSON 테스트 전부 PASS. `test_all_existing_review_reports_conform_to_v2_schema`는 **여전히 30건 실패**(Task 5에서 해결). 그 외 실패는 0건이어야 한다.

확인 명령:

```bash
python -m pytest .claude/test_review_post.py -q 2>&1 | tail -3
```
Expected: `30 failed, 60 passed` (실패는 전부 기존 보고서 conformance subtest)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "refactor(review): scaffold 파일 출력을 정본 serializer로 일원화"
```

---

### Task 4: `--finalize` — LLM 행 추가 후 요약 재계산·재직렬화

**Files:**
- Modify: `.claude/review_post.py` (`parse_args`, `main`)
- Test: `.claude/test_review_post.py` (`TestCliContractsV2`에 추가)

**Interfaces:**
- Consumes: Task 2의 `rr.parse_report`, `rr.validate_report`, `rr.serialize_report`
- Produces: CLI 플래그 `--finalize <report.md> [...]`. exit `0` 정상, exit `2` 파싱·검증 실패. 품질 gate 판정은 하지 않는다(#85 범위).

- [ ] **Step 1: Write the failing test**

`.claude/test_review_post.py`의 `TestCliContractsV2`에 추가:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestCliContractsV2 -q`
Expected: FAIL — `--finalize`가 경로 인자로 취급되어 `review_file()`이 리포트 Markdown을 포스트로 읽고 rc가 어긋난다

- [ ] **Step 3: Write minimal implementation**

`parse_args`의 `opts` 초기값에 `"finalize": []`를 추가하고, 플래그 분기(`elif arg == "--write-reports":` 아래)에 추가한다:

```python
        elif arg == "--finalize":
            if i + 1 < len(args):
                opts["finalize"].append(args[i + 1])
                i += 1
            else:
                opts["errors"].append("--finalize requires a value")
```

`main()`에서 `paths` 검사 직전(740행 `paths = opts["paths"]` 위)에 finalize 분기를 넣는다:

```python
    if opts["finalize"]:
        return finalize_reports(opts["finalize"])
```

그리고 `main` 정의 위에 함수를 추가한다:

```python
def finalize_reports(report_paths):
    failed = False
    for report_path in report_paths:
        path = Path(report_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"리포트 읽기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue

        parsed = rr.parse_report(text)
        header = parsed["header"]
        canonical = rr.serialize_report(
            target=header.get("target", rr.NOT_RECORDED),
            generated_at=header.get("generated_at", rr.NOT_RECORDED),
            strict=header.get("strict", "false"),
            findings=parsed["findings"],
            sources=header.get("sources", []),
        )
        errors = rr.validate_report(canonical, state="complete")
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            failed = True
            continue

        try:
            path.write_text(canonical, encoding="utf-8")
        except OSError as e:
            print(f"리포트 쓰기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue
        print(f"정본화 완료: {path}")
    return 2 if failed else 0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q 2>&1 | tail -3`
Expected: `30 failed, 65 passed` (실패는 여전히 기존 보고서 conformance subtest만)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): --finalize로 LLM 행 추가 후 요약·정렬 재계산"
```

---

### Task 5: 과거 보고서 마이그레이션 (`--migrate`)

**Files:**
- Modify: `.claude/review_post.py` (`parse_args`, `main`, `migrate_legacy_finding` 인접)
- Modify: `docs/reviews/*.md` (비준수 30개)
- Test: `.claude/test_review_post.py` (새 클래스 `TestLegacyMigration`)

**Interfaces:**
- Consumes: Task 2의 `rr.parse_report`, `rr.serialize_report`, `rr.validate_report`; 기존 `migrate_legacy_finding`
- Produces: CLI 플래그 `--migrate <report.md> [...]`. exit `0`/`2`.

마이그레이션은 두 부류를 구분한다.

| 부류 | 대상 | 처리 |
|---|---|---|
| **A. 무손실 재포맷** | `###` 블록에 8개 필드가 이미 있는 보고서 (굵게 표기 포함, 헤더 누락 포함) — 12개 | 근거 그대로 보존하고 plain 표기·정본 헤더로 재직렬화. `source`는 원래 값 유지 |
| **B. 레거시 산문** | `- [L6] … · gate: info — …` 형태 불릿만 있는 보고서 — 24개 | 불릿마다 `migrate_legacy_finding()` 적용. `source: MIGRATED`, `location`/`quote`/`recommendation`은 `not-recorded` |

두 부류 모두 `generated_at`은 **파일명의 날짜**에서 가져온다(꾸며낸 값이 아니라 파일명이 이미 기록한 사실). `strict`는 알 수 없으므로 `not-recorded`. B 부류에는 헤더에 `migrated_from: legacy-prose`를 남겨 손실 있는 전환임을 투명하게 표시한다.

**severity 보존 주의:** 레거시 산문에서 심각도는 불릿 자체가 아니라 그 위의 섹션 제목(`🟢 참고 (9)`)과 불릿 안의 `· gate: info`에 실려 있다. `migrate_legacy_finding()`을 불릿 한 줄에만 적용하면 둘 다 놓쳐 기본값 🟡로 떨어지고, 🟢 참고 finding이 전부 🟡 권장으로 승격된다. 이는 근거 없는 심각도 변경이므로 반드시 섹션 제목과 인라인 `gate:`를 함께 읽는다. 우선순위는 인라인 `gate:` > 섹션 제목 > `migrate_legacy_finding()`의 문자열 휴리스틱이다.

실측(2026-08-02 main 기준)으로 두 신호가 레거시 불릿 전체를 덮는다.

```
총 레거시 불릿                48
  인라인 `· gate:` 보유       26   (info 24 · warn 2)
  섹션 제목 보유 파일          9   (🔴 필수 3 · 🟡 권장 7 · 🟢 참고 5 블록)
  두 신호가 모두 없는 파일      0   ← 휴리스틱 폴백이 실제로 쓰이는 경우 없음
```

검증 명령(마이그레이션 전에 다시 돌려 0이 유지되는지 확인한다):

```bash
for f in $(grep -rlE "^- \[(D[0-9]+|L[0-9]+)\] " docs/reviews/); do
  grep -qE "^(🔴|🟡|🟢) (필수|권장|참고) \([0-9]+\)$" "$f" || grep -qE "gate: (fail|warn|info)" "$f" || echo "$f"
done
```
Expected: 출력 없음

- [ ] **Step 1: Write the failing test**

`.claude/test_review_post.py` 끝(`TestStdoutEncoding` 앞)에 추가:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestLegacyMigration -q`
Expected: FAIL — `--migrate`가 미지원 플래그라 경로로 취급되고 rc/파일 내용이 어긋난다

- [ ] **Step 3: Write minimal implementation**

`parse_args`에 `"migrate": []`를 추가하고 `--finalize` 분기 옆에 같은 형태로 `--migrate` 분기를 넣는다. `main()`의 finalize 분기 아래에 추가:

```python
    if opts["migrate"]:
        return migrate_reports(opts["migrate"])
```

`migrate_legacy_finding` 아래에 헬퍼와 명령 구현을 추가한다:

```python
_REPORT_NAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
_LEGACY_BULLET_RE = re.compile(r"^- \[(D\d+|L\d+)\]\s")
_LEGACY_SECTION_RE = re.compile(r"^(🔴|🟡|🟢) (필수|권장|참고) \(\d+\)\s*$")
_LEGACY_GATE_RE = re.compile(r"gate:\s*(fail|warn|info)\b")
_SEVERITY_BY_GATE = {"fail": "🔴", "warn": "🟡", "info": "🟢"}
_GATE_BY_SEVERITY = {"🔴": "fail", "🟡": "warn", "🟢": "info"}


def report_identity(path):
    """파일명 `YYYY-MM-DD-<slug>.md`에서 날짜와 target을 읽는다."""
    match = _REPORT_NAME_RE.match(Path(path).stem)
    if not match:
        return rr.NOT_RECORDED, Path(path).stem
    return match.group(1), match.group(2)


def _legacy_rows(text):
    """레거시 산문 불릿을 v2 finding으로 옮긴다.

    심각도는 불릿 한 줄에만 있지 않다. 인라인 `gate:` 표시가 가장 정확하고,
    없으면 위쪽 섹션 제목(`🟢 참고 (9)`)이 그 불릿의 심각도다. 둘 다 없을 때만
    migrate_legacy_finding()의 문자열 휴리스틱에 맡긴다.
    """
    rows = []
    section_severity = None
    for line in text.splitlines():
        section = _LEGACY_SECTION_RE.match(line)
        if section:
            section_severity = section.group(1)
            continue
        if not _LEGACY_BULLET_RE.match(line):
            continue

        row = migrate_legacy_finding(line)
        row.pop("schema_version", None)
        gate = _LEGACY_GATE_RE.search(line)
        if gate:
            row["gate_effect"] = gate.group(1)
            row["severity"] = _SEVERITY_BY_GATE[gate.group(1)]
        elif section_severity:
            row["severity"] = section_severity
            row["gate_effect"] = _GATE_BY_SEVERITY[section_severity]
        rows.append(row)
    return rows


def migrate_reports(report_paths):
    failed = False
    for report_path in report_paths:
        path = Path(report_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"리포트 읽기 실패: {path}: {e}", file=sys.stderr)
            failed = True
            continue

        generated_at, target = report_identity(path)
        parsed = rr.parse_report(text)
        header = parsed["header"]
        complete = [f for f in parsed["findings"]
                    if all(field in f for field in rr.FINDING_FIELDS)]

        if complete:  # 부류 A: 근거를 그대로 보존한다
            findings, migrated_from = complete, None
        else:         # 부류 B: 손실 있는 전환임을 표시한다
            findings = _legacy_rows(text)
            migrated_from = "legacy-prose"

        if not findings:
            print(f"{path}: 마이그레이션할 finding이 없다", file=sys.stderr)
            failed = True
            continue

        canonical = rr.serialize_report(
            target=header.get("target") or target,
            generated_at=header.get("generated_at") or generated_at,
            strict=header.get("strict") or rr.NOT_RECORDED,
            findings=findings,
            sources=header.get("sources", []),
            migrated_from=migrated_from,
        )
        errors = rr.validate_report(canonical, state="complete")
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            failed = True
            continue

        path.write_text(canonical, encoding="utf-8")
        print(f"마이그레이션 완료: {path}")
    return 2 if failed else 0
```

`rr.serialize_report`에 `migrated_from` 선택 인자를 추가한다 (`.claude/review_report.py`):

```python
def serialize_report(*, target, generated_at, strict, findings, sources=(), migrated_from=None):
```

헤더 조립부에서 `sources` 추가 직후, `summary` 추가 직전에 넣는다:

```python
    if migrated_from:
        header.append(f"migrated_from: {migrated_from}")
```

그리고 `_HEADER_KEYS`에 `"migrated_from"`을 추가해 파서가 되읽을 수 있게 한다:

```python
_HEADER_KEYS = ("schema_version", "target", "generated_at", "strict",
                "sources", "migrated_from", "summary")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py::TestLegacyMigration .claude/test_review_report.py -q`
Expected: PASS

- [ ] **Step 5: 실제 보고서 30개 마이그레이션 실행**

먼저 비준수 목록을 확인한다:

```bash
python -m pytest .claude/test_review_post.py::TestReportSchemaV2::test_all_existing_review_reports_conform_to_v2_schema -q 2>&1 \
  | grep -oE "report='[^']+'" | sed "s/report='//;s/'//" | sort > /tmp/nonconforming.txt
wc -l /tmp/nonconforming.txt
```
Expected: 30

마이그레이션한다:

```bash
python .claude/review_post.py --migrate $(sed 's|^|docs/reviews/|' /tmp/nonconforming.txt | tr '\n' ' ')
```

- [ ] **Step 6: 사람 검수 — 근거가 날조되지 않았는지 확인**

```bash
git diff --stat docs/reviews/
git diff docs/reviews/2026-07-28-karatsuba.md   # 부류 A: quote/message가 그대로인지
git diff docs/reviews/2026-07-24-dp-1.md        # 부류 B: not-recorded 표시가 정직한지
grep -c "migrated_from: legacy-prose" docs/reviews/*.md | grep -v ":0" | wc -l
```

확인 사항:

1. 부류 A 보고서에서 `quote`·`message`·`recommendation` 문장이 한 글자도 바뀌지 않아야 한다.
2. 부류 B에서 원래 없던 `location`·`quote`가 생기면 안 된다.
3. **심각도 총계가 보존되어야 한다.** 마이그레이션 전후로 보고서별 🔴/🟡/🟢 개수가 같은지 기계적으로 대조한다.

```bash
# 마이그레이션 직전에 실행해 기준선을 남긴다
git stash list >/dev/null; for f in docs/reviews/*.md; do
  echo "$f $(git show HEAD:"$f" 2>/dev/null | grep -oE '요약: 🔴 [0-9]+ · 🟡 [0-9]+ · 🟢 [0-9]+' | tail -1)"
done > /tmp/severity-before.txt

# 마이그레이션 후
for f in docs/reviews/*.md; do
  echo "$f $(grep -oE '^summary: 🔴 [0-9]+ · 🟡 [0-9]+ · 🟢 [0-9]+' "$f" | sed 's/^summary: /요약: /')"
done > /tmp/severity-after.txt

diff /tmp/severity-before.txt /tmp/severity-after.txt
```

기존 `요약:` 줄이 있던 보고서는 새 `summary:` 줄과 개수가 같아야 한다. 하나라도 어긋나면 **중단하고 되돌린다**(`git checkout -- docs/reviews/`). 요약 줄이 아예 없던 보고서는 대조 대상이 아니므로 눈으로 확인한다.

- [ ] **Step 7: 전체 스위트가 초록인지 확인**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q 2>&1 | tail -3`
Expected: `0 failed` — 이 플랜의 핵심 수용 기준

- [ ] **Step 8: Commit**

```bash
git add .claude/review_post.py .claude/review_report.py .claude/test_review_post.py docs/reviews/
git commit -m "fix(review): 과거 보고서 30건을 review-report/v2 정본으로 마이그레이션"
```

---

### Task 6: 문서·커맨드 계약 동기화

**Files:**
- Modify: `docs/reviews/README.md:26-56` (v2 스키마 절)
- Modify: `.claude/commands/review-post.md:21-28, 59-68`
- Modify: `.claude/commands/review-post-all.md` (동일 절)
- Test: `.claude/test_review_post.py` (`TestReportSchemaV2::test_command_docs_include_required_storage_and_tool_contract` 확장)

**Interfaces:**
- Consumes: Task 3–5가 확정한 CLI 계약 (`--write-reports`, `--finalize`, `--migrate`)
- Produces: 없음 (문서)

**주의:** 이 태스크는 L1–L7 루브릭 문구를 건드리지 않는다. 루브릭 정본화는 #87 소관이다.

- [ ] **Step 1: Write the failing test**

`test_command_docs_include_required_storage_and_tool_contract`의 `required_terms`에 추가한다:

```python
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
```

그리고 `TestReportSchemaV2`에 README 계약 테스트를 추가한다:

```python
    def test_readme_documents_canonical_order_and_two_valid_states(self):
        text = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        for term in ("scaffold", "complete", "--finalize", "--migrate",
                     "migrated_from", "sources"):
            with self.subTest(term=term):
                self.assertIn(term, text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestReportSchemaV2 -q`
Expected: FAIL — README에 `scaffold`·`--finalize` 등이 없고, 커맨드 문서에 `--finalize`가 없다

- [ ] **Step 3: Write minimal implementation**

`docs/reviews/README.md`의 "## `review-report/v2` 스키마" 절(26–56행)을 아래로 교체한다:

```markdown
## `review-report/v2` 스키마

리포트는 다음 역할을 나눈다.

- Markdown: 기본 human output이다. 구조·필드 순서·공백은 `.claude/review_report.py`의 `serialize_report()`가 **단독으로** 결정한다. 손으로 형식을 맞추지 않는다.
- JSON: `--json`을 지정했을 때 stdout으로만 내보내는 machine-readable output이다. Markdown과 별도 산출물이지만 같은 필드 의미와 정렬 계약을 따른다.

### 최상위 필드 (이 순서로 출력한다)

| 필드 | 필수 | 값 |
|---|---|---|
| `schema_version` | 필수 | 항상 `review-report/v2` |
| `target` | 필수 | 리뷰 대상 slug 또는 `all` |
| `generated_at` | 필수 | 생성 날짜. 알 수 없으면 `not-recorded` |
| `strict` | 필수 | `true`, `false`, 또는 `not-recorded` |
| `sources` | 선택 | 검토한 포스트 경로 목록(쉼표 구분) |
| `migrated_from` | 선택 | 손실 있는 전환일 때만 `legacy-prose` |
| `summary` | 필수 | `🔴 n · 🟡 n · 🟢 n` — finding에서 계산한 값과 반드시 일치 |

헤더 다음에 빈 줄 하나, `## Findings`, 빈 줄 하나, 그리고 finding 블록이 온다.

### finding 필드 (이 순서로, 굵게 표기 없이 출력한다)

`severity` · `source` · `rule_id` · `location` · `quote` · `message` · `recommendation` · `gate_effect`

- `severity`: `🔴`, `🟡`, `🟢` 중 하나
- `source`: `D`, `L`, `MIGRATED` 중 하나
- `rule_id`: 예: `D1`, `L7`, `MIGRATED`
- `location`: `파일:줄` 형식. 알 수 없으면 `not-recorded`
- `quote`: 판단 근거가 되는 원문. 없으면 `not-recorded`
- `message`: 문제 설명
- `recommendation`: 권장 조치
- `gate_effect`: `fail`, `warn`, `info` 중 하나

각 finding은 `### <severity> [<rule_id>] <location>` 제목으로 시작한다.

정렬은 severity(`🔴`, `🟡`, `🟢`) → source(`D`, `L`, `MIGRATED`) → rule id → file path → line 순이며 항상 안정적이다. 블록 사이 빈 줄은 하나, 파일은 개행 하나로 끝난다. 같은 입력은 항상 같은 바이트를 만든다.

### 두 가지 유효 상태

| 상태 | 만드는 명령 | finding 개수 | 검증 |
|---|---|---|---|
| scaffold | `--write-reports` | 0건 허용 | `validate_report(text, state="scaffold")` |
| complete | LLM 행 추가 후 `--finalize` | 1건 이상 필수 | `validate_report(text, state="complete")` |

`docs/reviews/`에 남는 최종 산출물은 complete 상태다. `--finalize`는 finding을 정본 순서로 재정렬하고 `summary`를 다시 계산한다. 멱등이므로 여러 번 실행해도 결과가 같다.

### 마이그레이션

과거 보고서는 `python .claude/review_post.py --migrate <report.md>`로만 전환한다. 일괄 재작성은 하지 않는다.

- 8개 필드가 이미 있는 보고서는 근거를 그대로 보존하고 표기만 정본화한다. `source`는 원래 값을 유지한다.
- 산문 불릿만 있는 보고서는 `source: MIGRATED`로 전환하고, 확보할 수 없는 `location`·`quote`·`recommendation`은 `not-recorded`로 남긴다. 헤더에 `migrated_from: legacy-prose`를 붙여 손실 있는 전환임을 표시한다.
- `generated_at`은 파일명의 날짜에서 가져온다. 없는 근거를 새로 만들어 내지 않는다.

마이그레이션 placeholder는 기존 리포트에 증거가 없을 때만 `not-recorded`를 쓴다. 없는 quote, 위치, 생성 시각을 새로 꾸며내지 않는다.
```

`.claude/commands/review-post.md`의 1단계 절(21–28행) 끝에 한 줄 추가한다:

```markdown
- scaffold는 정본 헤더(`schema_version`·`target`·`generated_at`·`strict`·`sources`·`summary`)와 `## Findings` 섹션을 이미 포함한다. 헤더를 손으로 고치지 않는다.
```

같은 파일의 "## 저장 (문서화): 필수" 절 마지막 불릿 앞에 추가한다:

```markdown
- LLM 비평 행을 모두 추가한 뒤 `python .claude/review_post.py --finalize docs/reviews/<오늘 날짜>-<slug>.md`를 실행한다. 이 단계가 `summary`를 다시 계산하고 finding을 정본 순서로 재정렬한다. 건너뛰면 보고서가 미완료 상태로 남는다.
- finding 필드는 `- severity: 🔴`처럼 **굵게 표기 없이** 쓴다. `- **severity**:`는 정본 형식이 아니다.
```

`.claude/commands/review-post-all.md`의 "## 저장 (문서화): 필수" 절에도 같은 두 불릿을 추가한다(전체 리뷰 파일 경로는 `docs/reviews/<오늘 날짜>-all.md`).

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q 2>&1 | tail -3`
Expected: `0 failed`

- [ ] **Step 5: Commit**

```bash
git add docs/reviews/README.md .claude/commands/review-post.md .claude/commands/review-post-all.md .claude/test_review_post.py
git commit -m "docs(review): v2 정본 순서·두 유효 상태·마이그레이션 절차 문서화"
```

---

## 최종 검증

```bash
python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q
```
Expected: `0 failed` (기준선 30 failed → 0)

결정성 확인 — 같은 입력을 두 번 돌려 diff가 비어야 한다:

```bash
python .claude/review_post.py --write-reports --date 2026-08-02 src/content/posts/karatsuba.md
cp docs/reviews/2026-08-02-karatsuba.md /tmp/first.md
python .claude/review_post.py --write-reports --date 2026-08-02 src/content/posts/karatsuba.md
diff /tmp/first.md docs/reviews/2026-08-02-karatsuba.md && echo "결정적 overwrite OK"
git checkout -- docs/reviews/ 2>/dev/null; rm -f docs/reviews/2026-08-02-karatsuba.md
```

빌드 회귀 없음 확인:

```bash
npm run build
```

## 완료 기준 대조 (#84)

| 이슈 완료 기준 | 담당 태스크 |
|---|---|
| 하나의 serializer만 v2 Markdown 구조와 필드 순서를 결정한다 | Task 1, 3 (`write_markdown_report`가 `serialize_report`에만 의존) |
| deterministic·LLM·coverage row·final summary가 동일 계약으로 직렬화된다 | Task 1, 4 (coverage row도 `source: L`·`gate_effect: info`인 일반 finding) |
| 단일 포스트와 전체 포스트 경로가 같은 parser·validator를 통과한다 | Task 2, 6 (두 커맨드 모두 `--finalize` 경유) |
| scaffold 단계와 완료 보고서 단계의 유효 상태가 명시·검증된다 | Task 2 (`state="scaffold"` / `"complete"`), Task 6 (문서화) |
| 정본 출력의 순서·공백 정책이 안정적이며 같은 입력에 같은 결과 | Task 1 (결정성 테스트), 최종 검증 diff |
| 기존 보고서 처리 정책과 명시적 마이그레이션 절차가 문서화된다 | Task 5, 6 |

| 이슈 테스트 요구 | 담당 테스트 |
|---|---|
| scaffold-only 중간 상태 | `test_scaffold_output_is_canonical_and_validates_as_scaffold` |
| 완료된 보고서 | `test_finalize_recomputes_summary_from_all_findings` |
| 한 rule에 finding이 여러 개 | `test_findings_sorted_by_severity_then_source_then_rule` |
| evidence를 구할 수 없는 경우 | `test_class_b_legacy_prose_uses_migrated_source_and_placeholders`, `test_migration_never_invents_evidence` |
| 마이그레이션이 심각도를 바꾸지 않을 것 | `test_legacy_severity_comes_from_section_heading_not_default`, `test_inline_gate_marker_wins_over_section_heading`, Task 5 Step 6 총계 대조 |
| 전체 포스트 aggregate 보고서 | `test_multi_target_json_aggregate_uses_all_target_and_combines_findings` (기존), Task 5에서 `2026-06-04-all.md` 마이그레이션 |
| 같은 날짜 재실행 결정적 overwrite | `test_scaffold_rewrite_is_deterministic_for_same_input`, `test_finalize_is_idempotent`, `test_migration_is_idempotent` |

## 알려진 위험

- **부류 B 마이그레이션은 되돌릴 수 없는 정보 손실이 아니다** — git 히스토리에 원문이 남는다. 다만 Task 5 Step 6의 사람 검수를 건너뛰면 근거 날조를 놓칠 수 있다. 이 단계를 생략하지 않는다.
- **레거시 심각도는 불릿 밖에 있다.** 섹션 제목과 인라인 `gate:`를 읽지 않으면 🟢 참고가 조용히 🟡 권장으로 바뀐다. 이 플랜은 두 신호를 모두 읽도록 설계했고 실측상 폴백이 필요한 불릿은 0건이지만, 새 형식의 레거시 보고서가 나타나면 휴리스틱으로 떨어진다. Step 6의 심각도 총계 대조가 이를 잡는 안전망이다.
- **`sources:` 필드 신설**은 README 계약 변경이다. validator에서 선택 필드로 두었으므로 기존 통과 보고서 6개는 영향받지 않는다.
- **`report_to_json_v2`의 `generated_at`이 `not-recorded`에서 실제 날짜로 바뀐다.** JSON 소비자가 아직 없으므로 안전하지만, #85가 이 값을 읽게 되면 계약으로 굳는다.
- **`--finalize`를 커맨드 문서에만 적으면 LLM이 건너뛸 수 있다.** #85에서 strict gate가 미완료 보고서를 exit 2로 잡으면 구조적으로 강제된다. 그때까지는 문서 의존이다.
