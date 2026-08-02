# strict 모드 LLM finding 게이트 (#85) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** strict 실행의 최종 exit code를 deterministic 검사와 LLM 비평이 **모두 끝난 뒤 한 번만** 결정하게 만들어, 보고서에 남은 실패 finding과 프로세스 종료 상태가 어긋나지 않게 한다.

**Architecture:** #84가 만든 `--finalize`는 이미 완료 보고서를 파싱해 deterministic finding과 LLM finding을 한 자리에서 본다. 여기에 `--strict`를 결합해 최종 게이트로 쓴다. 재정렬·요약 재계산과 게이트 판정이 **같은 finding 목록**에서 나오므로 "보고서와 exit code가 같은 집계 결과에서 나온다"는 기준이 구조적으로 만족된다.

**Tech Stack:** Python 3.11 표준 라이브러리만. 테스트는 `unittest` + `pytest`.

## Global Constraints

- 표준 라이브러리 외 의존성 추가 금지.
- exit code 계약: `0` 통과 / `1` 품질 실패 / `2` 인프라·스키마·입력 실패.
- 🟡 finding은 경고이며 게이트를 실패시키지 않는다. `gate_effect: fail`만 실패로 이어진다.
- 게이트 판정과 보고서 직렬화는 반드시 같은 finding 목록에서 나온다.
- **비범위:** L1–L7 루브릭 의미 변경(#87·#88), Markdown 표현·마이그레이션 변경(#84에서 완료), 과거 보고서 재전환.

---

## 현재 상태

`review_post.py:1029`가 최종 판정 지점이다.

```python
if opts["strict"] and required_failed:   # required_failed는 결정적 검사만 본다
    return 1
```

Python 프로세스는 LLM 행이 추가되기 **전에** 종료한다. 그래서 보고서에 `gate_effect: fail`인 🔴 L7 finding이 남아 있어도 exit code는 0이다. 보고서는 실패인데 명령은 성공하므로 strict를 CI 게이트로 신뢰할 수 없다.

`--finalize`(#84)는 LLM 행이 다 붙은 완료 보고서를 파싱한다. 최종 판정을 내릴 지점은 여기다.

## 설계

```
python .claude/review_post.py --finalize --strict docs/reviews/2026-08-02-karatsuba.md
```

| exit | 조건 |
|---|---|
| `0` | `gate_effect: fail`인 finding 없음 |
| `1` | `gate_effect: fail`인 finding 하나 이상 (source가 D든 L이든) |
| `2` | 파싱 실패 · 스키마 위반 · 입력 오류 · severity↔gate_effect 불일치 · **LLM 단계 누락** |

**LLM 단계 누락 판정:** 두 리뷰 커맨드는 "문제가 없는 범주도 생략하지 말고 explicit coverage row를 남긴다"고 규정한다. 따라서 `source: L`인 finding의 `rule_id`가 L1–L7을 모두 덮지 않으면 비평이 끝나지 않은 것이다. 조용한 통과 대신 exit 2로 처리한다.

**severity↔gate_effect 대응 강제:** 정본 매핑은 🔴→`fail`, 🟡→`warn`, 🟢→`info`다. 이 대응을 검증하지 않으면 🔴 finding에 `gate_effect: info`를 적어 게이트를 우회할 수 있다. 저장된 보고서 전수 조사 결과 현재 불일치는 0건이므로 강제해도 기존 데이터가 깨지지 않는다.

**쓰기 순서:** 보고서를 먼저 쓰고 그 다음 판정한다. 기존 `test_strict_multi_target_writes_reports_before_returning_failure`가 정한 관례와 같다. 실패해도 보고서는 남아야 한다.

---

### Task 1: severity↔gate_effect 대응 검증

**Files:**
- Modify: `.claude/review_report.py` (`validate_report`)
- Test: `.claude/test_review_report.py`

**Interfaces:**
- Consumes: `SEVERITY_VALUES`, `GATE_EFFECT_VALUES`
- Produces: `CANONICAL_GATE_EFFECT: dict[str, str]` — 🔴→fail, 🟡→warn, 🟢→info

- [ ] **Step 1: Write the failing test**

`.claude/test_review_report.py`의 `TestValidateReport`에 추가:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_report.py -q`
Expected: FAIL — `test_rejects_severity_and_gate_effect_mismatch`가 빈 오류 목록을 받는다

- [ ] **Step 3: Write minimal implementation**

`.claude/review_report.py`의 `GATE_EFFECT_VALUES` 정의 아래에 추가:

```python
# 정본 대응. 이 대응을 검증하지 않으면 🔴 finding에 gate_effect: info를 적어
# 품질 게이트를 우회할 수 있다.
CANONICAL_GATE_EFFECT = {"🔴": "fail", "🟡": "warn", "🟢": "info"}
```

`validate_report`의 finding 루프에서 `gate_effect` 검사 뒤에 추가:

```python
        expected_gate = CANONICAL_GATE_EFFECT.get(finding["severity"])
        if expected_gate and finding["gate_effect"] != expected_gate:
            errors.append(
                f"finding #{index + 1} severity {finding['severity']}는 "
                f"gate_effect {expected_gate}여야 하는데 {finding['gate_effect']}다"
            )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_report.py .claude/test_review_post.py -q`
Expected: 전부 PASS (기존 99 + 신규 2)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_report.py .claude/test_review_report.py
git commit -m "feat(review): severity와 gate_effect 대응을 검증해 게이트 우회를 막는다"
```

---

### Task 2: LLM coverage 검사

**Files:**
- Modify: `.claude/review_post.py`
- Test: `.claude/test_review_post.py`

**Interfaces:**
- Consumes: 없음
- Produces:
  - `REQUIRED_LLM_RULES: tuple[str, ...]` — `("L1", …, "L7")`
  - `missing_llm_coverage(findings: list[dict]) -> list[str]` — 빠진 rule_id 목록, 빈 리스트면 완전

- [ ] **Step 1: Write the failing test**

`.claude/test_review_post.py`에 새 클래스를 `TestStdoutEncoding` 앞에 추가:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestLlmCoverage -q`
Expected: FAIL — `AttributeError: module 'review_post' has no attribute 'missing_llm_coverage'`

- [ ] **Step 3: Write minimal implementation**

`.claude/review_post.py`의 `finalize_reports` 정의 위에 추가:

```python
# 두 리뷰 커맨드는 문제가 없는 범주도 explicit coverage row로 남기도록 규정한다.
# 따라서 이 중 하나라도 비면 LLM 비평이 끝나지 않은 것이다.
REQUIRED_LLM_RULES = ("L1", "L2", "L3", "L4", "L5", "L6", "L7")


def missing_llm_coverage(findings):
    """LLM 비평이 덮지 않은 L 범주를 돌려준다. 빈 목록이면 전 범주가 덮였다."""
    covered = {f.get("rule_id") for f in findings if f.get("source") == "L"}
    return [rule for rule in REQUIRED_LLM_RULES if rule not in covered]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py::TestLlmCoverage -q`
Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "feat(review): LLM 비평 L1-L7 coverage 누락 검사 추가"
```

---

### Task 3: `--finalize --strict` 최종 게이트

**Files:**
- Modify: `.claude/review_post.py` (`finalize_reports`, `main`)
- Test: `.claude/test_review_post.py` (`TestCliContractsV2`)

**Interfaces:**
- Consumes: Task 1의 `validate_report` 대응 검증, Task 2의 `missing_llm_coverage`
- Produces: `finalize_reports(report_paths, strict=False) -> int` — exit code 0/1/2

이슈가 요구한 회귀 사례 일곱 가지를 그대로 테스트로 옮긴다.

- [ ] **Step 1: Write the failing test**

`.claude/test_review_post.py`의 `TestCliContractsV2`에 추가:

```python
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
            "### 🟢 [L1] not-recorded",
            "### 🔴 [L1] not-recorded", 1).replace(
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestCliContractsV2 -q`
Expected: FAIL — `--strict`가 붙어도 `finalize_reports`가 게이트를 보지 않아 red 사례가 0을 낸다

- [ ] **Step 3: Write minimal implementation**

`finalize_reports`를 아래로 교체한다.

```python
def finalize_reports(report_paths, strict=False):
    """LLM 비평 행이 추가된 리포트를 정본 형식으로 다시 직렬화한다.

    요약을 finding에서 다시 계산하고 정본 순서로 재정렬한다. 멱등이다.

    strict면 재직렬화에 쓴 바로 그 finding 목록으로 최종 품질 게이트를 판정한다.
    보고서에 남은 실패 finding과 exit code가 같은 집계에서 나오게 하기 위해서다.
    """
    infra_failed = False
    quality_failed = False
    for report_path in report_paths:
        path = Path(report_path)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as e:
            print(f"리포트 읽기 실패: {path}: {e}", file=sys.stderr)
            infra_failed = True
            continue

        parsed = rr.parse_report(text)
        header = parsed["header"]
        findings = parsed["findings"]
        canonical = rr.serialize_report(
            target=header.get("target", rr.NOT_RECORDED),
            generated_at=header.get("generated_at", rr.NOT_RECORDED),
            strict=True if strict else header.get("strict", "false"),
            findings=findings,
            sources=header.get("sources", []),
        )
        errors = rr.validate_report(canonical, state="complete")
        if errors:
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
            infra_failed = True
            continue

        if strict:
            missing = missing_llm_coverage(findings)
            if missing:
                print(
                    f"{path}: LLM 비평 coverage 누락 — {', '.join(missing)}. "
                    "비평 단계가 끝나지 않았으므로 품질 통과로 처리하지 않는다",
                    file=sys.stderr,
                )
                infra_failed = True
                continue

        try:
            path.write_text(canonical, encoding="utf-8")
        except OSError as e:
            print(f"리포트 쓰기 실패: {path}: {e}", file=sys.stderr)
            infra_failed = True
            continue
        print(f"정본화 완료: {path}")

        if strict:
            failing = [f for f in findings if f.get("gate_effect") == "fail"]
            if failing:
                quality_failed = True
                for f in failing:
                    print(
                        f"{path}: 품질 게이트 실패 — [{f['rule_id']}] {f['location']}",
                        file=sys.stderr,
                    )

    if infra_failed:
        return 2
    return 1 if quality_failed else 0
```

`main()`의 finalize 분기를 고친다.

```python
    if opts["finalize"]:
        return finalize_reports(opts["finalize"], strict=opts["strict"])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q`
Expected: 전부 PASS

- [ ] **Step 5: Commit**

```bash
git add .claude/review_post.py .claude/test_review_post.py
git commit -m "fix(review): strict 최종 판정을 LLM 비평까지 집계한 뒤 내린다"
```

---

### Task 4: 문서·커맨드 계약 동기화

**Files:**
- Modify: `docs/reviews/README.md` (Gate 계약 절)
- Modify: `.claude/commands/review-post.md`, `.claude/commands/review-post-all.md`
- Test: `.claude/test_review_post.py`

- [ ] **Step 1: Write the failing test**

`TestReportSchemaV2`에 추가:

```python
    def test_readme_documents_strict_gate_contract(self):
        text = (REVIEW_REPORT_DIR / "README.md").read_text(encoding="utf-8")

        for term in ("--finalize --strict", "exit code `1`", "exit code `2`",
                     "L1–L7", "coverage 누락"):
            with self.subTest(term=term):
                self.assertIn(term, text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest .claude/test_review_post.py::TestReportSchemaV2 -q`
Expected: FAIL — README에 `--finalize --strict`가 없다

- [ ] **Step 3: Write minimal implementation**

`docs/reviews/README.md`의 "## Gate 계약" 절을 아래로 교체한다.

```markdown
## Gate 계약

strict mode는 schema, 입력, deterministic 검사, LLM 비평 결과를 gate 판정에 맞춰 검증하는 모드다. 최종 판정은 두 단계가 **모두 끝난 뒤 한 번만** 내린다.

`python .claude/review_post.py --finalize --strict <report.md>`

- exit code `0`: 통과. `gate_effect: fail`인 finding이 없다.
- exit code `1`: 품질 실패. `gate_effect: fail`인 finding이 하나 이상 있다. 출처가 결정적 검사(`D`)든 LLM 비평(`L`)이든 같다.
- exit code `2`: infrastructure, schema, input 실패. 파싱 실패, 스키마 위반, severity와 gate_effect 불일치, LLM 비평 단계 누락을 포함한다.

`🟡` finding은 권장 사항이며 gate를 실패시키지 않는다. `🔴`만 quality gate 실패로 이어진다.

판정에 쓰는 finding 목록은 리포트를 직렬화할 때 쓴 목록과 같다. 보고서에 남은 실패 finding과 exit code가 어긋날 수 없다.

### severity와 gate_effect 대응

| severity | gate_effect |
|---|---|
| `🔴` | `fail` |
| `🟡` | `warn` |
| `🟢` | `info` |

이 대응은 검증 대상이다. `🔴` finding에 `gate_effect: info`를 적어 게이트를 우회할 수 없다. 어긋나면 exit code `2`다.

### LLM 비평 coverage 누락

두 리뷰 커맨드는 문제가 없는 범주도 생략하지 말고 explicit coverage row를 남기도록 규정한다. 따라서 `source: L`인 finding이 L1–L7을 모두 덮지 않으면 비평 단계가 끝나지 않은 것이다.

strict는 이를 품질 통과로 처리하지 않고 exit code `2`로 끝낸다. LLM 단계의 인프라 실패나 출력 계약 위반이 조용히 통과하는 것을 막기 위해서다. 누락된 범주는 stderr에 나열된다.

리포트는 판정 전에 먼저 저장한다. 게이트가 실패해도 근거가 남아야 하기 때문이다.
```

`.claude/commands/review-post.md`의 `--finalize` 불릿을 아래로 바꾼다.

```markdown
- 비평 행을 모두 추가한 뒤 `python .claude/review_post.py --finalize docs/reviews/<오늘 날짜>-<slug>.md`를 실행한다. 이 단계가 `summary`를 다시 계산하고 finding을 정본 순서로 재정렬한다. 건너뛰면 리포트가 미완료 상태로 남는다.
- 품질 게이트까지 확인하려면 `--strict`를 함께 준다. `gate_effect: fail`인 finding이 있으면 exit 1, L1–L7 coverage가 비면 exit 2다. 자세한 계약은 `docs/reviews/README.md`의 Gate 계약 절에 있다.
```

`.claude/commands/review-post-all.md`에도 같은 두 번째 불릿을 추가한다(경로는 `docs/reviews/<오늘 날짜>-all.md`).

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q`
Expected: 전부 PASS

- [ ] **Step 5: Commit**

```bash
git add docs/reviews/README.md .claude/commands/ .claude/test_review_post.py
git commit -m "docs(review): strict gate 계약과 coverage 누락 판정 문서화"
```

---

## 최종 검증

```bash
python -m pytest .claude/test_review_post.py .claude/test_review_report.py -q
npm run build
```

end-to-end 확인 — 실제 포스트로 scaffold를 만들고, LLM 행 없이 strict finalize를 돌리면 coverage 누락으로 2가 나와야 한다.

```bash
python .claude/review_post.py --write-reports --date 2026-08-02 src/content/posts/karatsuba.md
python .claude/review_post.py --finalize --strict docs/reviews/2026-08-02-karatsuba.md; echo "exit=$?"
rm -f docs/reviews/2026-08-02-karatsuba.md
```
Expected: `exit=2`, stderr에 `LLM 비평 coverage 누락 — L1, L2, L3, L4, L5, L6, L7`

## 완료 기준 대조 (#85)

| 이슈 완료 기준 | 담당 |
|---|---|
| strict 최종 판정이 deterministic·LLM 단계 완료 후 이뤄진다 | Task 3 (`--finalize --strict`) |
| `gate_effect: fail`인 🔴 LLM finding이 있으면 exit 1 | `test_strict_gate_fails_on_llm_red` |
| deterministic 빨간 finding도 exit 1 | `test_strict_gate_fails_on_deterministic_red` |
| 노랑만 있거나 finding 없으면 exit 0 | `test_strict_gate_passes_on_yellow_only`, `…only_coverage_rows_exist` |
| malformed·필수 단계 누락·인프라 실패는 exit 2 | `…malformed_llm_output`, `…llm_phase_missing`, `…one_category_missing` |
| 보고서 finding과 exit code가 같은 집계에서 나온다 | `test_report_summary_and_exit_code_come_from_same_aggregation` |

## 알려진 위험

- **`--strict`가 `--finalize` 없이 쓰이던 기존 경로는 그대로다.** `python review_post.py --strict <post.md>`는 여전히 결정적 검사만으로 판정한다. 이건 scaffold 단계의 조기 실패 검출로 유효하며, 최종 게이트는 `--finalize --strict`다. 두 경로의 역할 차이를 README에 적는다.
- **coverage 강제는 커맨드 문서의 규정에 의존한다.** 커맨드가 coverage row 규칙을 버리면 이 검사도 의미를 잃는다. #87이 루브릭 정본을 하나로 모으면 그 정본에서 목록을 끌어오는 편이 낫다.
- **`REQUIRED_LLM_RULES`가 코드에 하드코딩된다.** L 범주가 늘면 두 곳(커맨드 문서·이 상수)을 같이 고쳐야 한다. #87에서 정본화할 때 함께 정리한다.
