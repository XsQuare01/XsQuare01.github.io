# 증명 의무·원문 충실도(L6) 판정 지침 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 작성자 정본과 리뷰 루브릭에 증명 의무 판단 단위와 L6 네 상태를 세우고, 계약 테스트로 문서 표류를 막는다.

**Architecture:** 문서만 고친다. 작성자 지침은 `docs/writing-rules.md` 정본에, 리뷰어 판정 기준은 `docs/review-rubric.md`에 넣고 루브릭이 정본을 가리킨다. 새 LLM 범주를 만들지 않고 기존 L4를 넓혀 과거 리포트 coverage를 보존한다. 모든 문서 규약은 `.claude/test_review_post.py`의 기존 계약 테스트 패턴으로 붙잡는다.

**Tech Stack:** Markdown 문서, Python 3.12 `unittest`(+`subTest`), `python .claude/review_post.py --gate`

**Spec:** `docs/superpowers/specs/2026-08-18-proof-obligation-l6-guidance-design.md`

## Global Constraints

- 브랜치는 `docs/proof-obligation-l6-guidance`다. main에 직접 커밋하지 않는다.
- 커밋 메시지에 `Co-Authored-By` 트레일러를 넣지 않는다.
- `.claude/review_post.py` 본체와 `review-report/v2` 스키마를 수정하지 않는다.
- 새 LLM 범주를 만들지 않는다. 루브릭에 `**L8`이 등장하면 `test_canonical_rubric_defines_exactly_l1_to_l7`이 실패한다.
- 루브릭의 각 범주는 `- **L<n> <이름>:**` 형태의 최상위 불릿으로 남긴다. 이름에 `:`와 `*`를 쓰지 않는다(`test_readme_category_labels_match_the_canonical_rubric`의 정규식 `^- \*\*(L[1-7]) ([^:*]+):\*\*`).
- 두 커맨드의 `## 2단계: LLM 비평` 절은 바이트 단위로 같아야 한다(`test_both_commands_share_one_critique_section`). 이 절을 건드리지 않는다.
- 문장은 `~다` 평서체로 쓰고 문두 접속어를 최소화한다(`docs/writing-rules.md` 「바른 문장 쓰기」).
- 기준선: `python -m pytest .claude -q` → `207 passed, 130 subtests passed`. `python .claude/review_post.py --gate` → 대상 31개, 면제 4개, exit 0.
- 매 태스크 끝에서 `python -m pytest .claude -q`가 전부 통과해야 한다. 실패는 이번 변경 탓으로 본다.

---

### Task 1: L6 네 상태를 루브릭에 세운다

**Files:**
- Modify: `docs/review-rubric.md:13` (L6 불릿 한 줄을 상태 표로 교체)
- Test: `.claude/test_review_post.py` (`TestLlmRubricSingleSource` 클래스에 추가, 현재 1362행 `test_coverage_constant_matches_the_canonical_rubric` 뒤)

**Interfaces:**
- Consumes: 없음 (첫 태스크)
- Produces: 루브릭에 상태 이름 문자열 `verified fidelity`, `approved extension`, `source unavailable`, `actual mismatch`가 존재한다. Task 2가 커맨드 문서에서 이 표를 가리키고, Task 8이 완료기준 대조에 쓴다.

- [ ] **Step 1: 실패하는 계약 테스트를 쓴다**

`.claude/test_review_post.py`의 `TestLlmRubricSingleSource` 안, `test_coverage_constant_matches_the_canonical_rubric` 메서드 바로 뒤에 넣는다.

```python
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
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k l6_states -v`
Expected: FAIL — `AssertionError: 'verified fidelity' not found in ...`

- [ ] **Step 3: 루브릭의 L6 불릿을 상태 표로 교체한다**

`docs/review-rubric.md`의 L6 불릿(현재 13행 한 줄) 전체를 아래로 바꾼다. 불릿은 반드시 `- **L6 소스 자료 충실성:**`으로 시작해야 하고(이름 변경 금지 — README 색인과 대조된다), 표는 두 칸 들여쓰기로 불릿에 딸린다.

```markdown
- **L6 소스 자료 충실성:** 이 블로그 포스트는 사용자의 **노션** 자료를 바탕으로 쓴다(`AGENTS.md` 원문 보존 규칙과 `docs/writing-rules.md` 참조). 가능하면 해당 노션 페이지를 `notion-search`→`notion-fetch`로 가져와 대조한다. 판정은 아래 네 상태 가운데 하나를 골라 기록하며, 상태 이름을 `message` 맨 앞에 적는다. 상태가 severity를 정한다.

  | 상태 | 뜻 | severity | gate_effect |
  |---|---|---|---|
  | `verified fidelity` | 원문이나 승인된 자료를 실제로 대조해 구조, 핵심 주장, 논증 흐름, 의도가 보존됨을 확인했다 | 🟢 | info |
  | `approved extension` | 원문 밖 내용이 있으나 추가임이 provenance에 밝혀져 있고 승인된 스펙에 부합하며 원문의 의도와 논증을 훼손하지 않는다 | 🟢 | info |
  | `source unavailable` | 원문이나 승인된 자료에 접근할 수 없어 충실도를 검증하지 못했다 | 🟡 | warn |
  | `actual mismatch` — 국소 | 대조 가능한 자료와 사소한 표현 차이가 있다 | 🟡 | warn |
  | `actual mismatch` — 핵심 | 구조, 주장, 증명 흐름, 의도, 사실 관계를 바꾸는 불일치가 있다 | 🔴 | fail |

  세 규칙을 함께 지킨다. 원문 접근 실패를 `verified fidelity`로 적지 않는다. `source unavailable`은 그 자체로 문서 gate를 차단하지 않되 L6 검증을 **미완료**로 남긴다. 원문 밖 추가 자체를 불일치로 판정하지 않는다. 판정 대상은 투명성, 승인, 의도 보존 세 조건이다.
```

- [ ] **Step 4: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "l6_states or l6_states_to_severity or missing_source_as_verified" -v`
Expected: 3 passed

- [ ] **Step 5: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: `210 passed` 이상, 실패 0

- [ ] **Step 6: 커밋한다**

```bash
git add docs/review-rubric.md .claude/test_review_post.py
git commit -m "docs(review): L6를 네 상태로 나눠 severity를 고정한다 (#88)"
```

---

### Task 2: L6 coverage 예외를 커맨드와 README에 반영한다

**Files:**
- Modify: `.claude/commands/review-post.md` (`## 출력 형식` 절의 coverage row 문단 뒤)
- Modify: `.claude/commands/review-post-all.md` (같은 위치)
- Modify: `docs/reviews/README.md:207-215` (`### severity와 gate_effect 대응` 절 뒤에 새 소절), `docs/reviews/README.md:182-193` (면제 규칙 절 끝)
- Test: `.claude/test_review_post.py` (`TestLlmRubricSingleSource`, Task 1이 추가한 메서드 뒤)

**Interfaces:**
- Consumes: Task 1이 루브릭에 세운 상태 이름과 `docs/review-rubric.md`의 L6 표.
- Produces: 두 커맨드에 문자열 `L6는 이 고정에서 예외다`, README에 `#### L6 상태가 severity를 정한다` 소절이 있다.

- [ ] **Step 1: 실패하는 계약 테스트를 쓴다**

```python
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
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "l6_coverage_exception or l6_severity_and_reporting" -v`
Expected: FAIL — `AssertionError: 'L6는 이 고정에서 예외다' not found`

- [ ] **Step 3: 두 커맨드에 같은 문단을 넣는다**

`review-post.md`와 `review-post-all.md` 둘 다에서, `이 coverage row는 `severity: 🟢`, `source: L`, `gate_effect: info`를 쓴다.`로 끝나는 문단 **바로 뒤에** 아래 문단을 넣는다. 두 파일에 같은 문장을 쓴다.

```markdown
**L6는 이 고정에서 예외다.** L6 coverage row는 `docs/review-rubric.md`의 L6 상태 표가 정한 severity를 쓴다. 원문 대조에 실패한 상태를 `검토 완료, 이슈 없음`으로 적지 않고, 상태 이름 `source unavailable`과 검증하지 못한 이유를 `message`에 적으며 `severity: 🟡`, `gate_effect: warn`으로 기록한다. 대조를 실제로 마쳤을 때만 `verified fidelity` 또는 `approved extension`으로 적고 🟢을 쓴다.
```

`## 2단계: LLM 비평` 절은 건드리지 않는다. 두 커맨드의 그 절이 어긋나면 `test_both_commands_share_one_critique_section`이 실패한다.

- [ ] **Step 4: README에 severity 소절과 보고 예시를 넣는다**

`docs/reviews/README.md`의 `### severity와 gate_effect 대응` 절 끝(`어긋나면 exit code `2`다.` 문장 뒤)에 아래를 넣는다.

````markdown
#### L6 상태가 severity를 정한다

위 3단 매핑은 그대로다. L6만 판정 상태가 severity를 먼저 정하고, 그 severity가 매핑에 따라 `gate_effect`를 정한다. 원문 대조에 실패한 상태는 "이슈 없음"이 아니라 "검증 미완료"이므로 coverage row라도 🟢을 쓰지 않는다. 상태 목록과 매핑의 정본은 `docs/review-rubric.md`의 L6 절이다.

검증을 마치지 못한 경우.

```
### 🟡 [L6] src/content/posts/any-mst.md:1

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/any-mst.md:1
- quote: not-recorded
- message: source unavailable — 대조할 노션 원문이나 승인된 자료에 접근할 수 없어 충실도를 검증하지 못했다. 현재 저장소 글의 구조와 논지만 보존 기준으로 삼았다.
- recommendation: 원문 접근이 가능해지면 핵심 구조, 논증 흐름, 누락, 자의적 추가를 대조한다.
- gate_effect: warn
```

대조를 마친 경우.

```
### 🟢 [L6] src/content/posts/all-pairs-shortest-path.md:25

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/all-pairs-shortest-path.md:25
- quote: 무엇을 구하는가
- message: verified fidelity — 승인된 설계 스펙과 대조해 문제 정의, 경유 제약, 점화식 증명, 의사코드의 핵심 줄기가 보존됨을 확인했다.
- recommendation: not-recorded
- gate_effect: info
```
````

면제 규칙 절 끝(`🔴 판정은 면제하지 않는다.` 문장 뒤)에 한 줄을 넣는다.

```markdown
L6 상태 규약은 2026-08-18 이후 생성된 리포트에 적용한다. 그 이전 리포트의 L6 행을 고쳐 쓰지 않는다. 판정은 그 시점의 근거로 남기며, 소급 수정은 위 「감사 섹션」 규약과 어긋난다.
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "l6_coverage_exception or l6_severity_and_reporting" -v`
Expected: 2 passed

- [ ] **Step 6: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 7: 커밋한다**

```bash
git add .claude/commands/review-post.md .claude/commands/review-post-all.md docs/reviews/README.md .claude/test_review_post.py
git commit -m "docs(review): L6 coverage row를 상태별 severity로 가른다 (#88)"
```

---

### Task 3: L4를 표현 정렬로 넓힌다

**Files:**
- Modify: `docs/review-rubric.md:11` (L4 불릿)
- Modify: `docs/reviews/README.md:246` (검사 항목 요약의 L 목록)

**Interfaces:**
- Consumes: 없음
- Produces: 루브릭 L4 이름이 `표현 정렬 — SVG·의사코드·수식·계산 예시 ↔ 본문`이다. Task 6이 정본의 표현 정렬 모듈에서 이 범주를 가리킨다.

- [ ] **Step 1: 루브릭의 L4 불릿을 바꾼다**

기존 한 줄을 아래로 교체한다. 새 범주를 만들지 않으므로 `rule_id`는 `L4`로 유지되고 과거 리포트의 coverage row가 그대로 유효하다.

```markdown
- **L4 표현 정렬 — SVG·의사코드·수식·계산 예시 ↔ 본문:** 한 글 안의 여러 표현이 같은 전제, 같은 실행 순서, 같은 값, 같은 결론을 말하는지 대조한다. SVG의 레이블·수치·캡션이 본문 예제와 맞는지(예: 그래프 가중치, 거리 값), 의사코드의 분기와 순회 순서가 본문 설명과 같은지, 수식과 계산 예시의 값이 어긋나지 않는지 본다. 대조 절차는 `docs/writing-rules.md`의 「표현 정렬 모듈」이 정본이다.
```

- [ ] **Step 2: 기존 계약 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k readme_category_labels -v`
Expected: FAIL — `AssertionError: README의 L4 이름이 정본과 다르다`

이 실패가 이 태스크의 안전망이다. 루브릭만 고치고 색인을 잊는 경우를 잡는다.

- [ ] **Step 3: README의 검사 항목 색인을 맞춘다**

`docs/reviews/README.md`의 `LLM 비평(L):` 줄에서 `L4 SVG ↔ 본문 일치`를 `L4 표현 정렬 — SVG·의사코드·수식·계산 예시 ↔ 본문`으로 바꾼다. 다른 범주 이름은 건드리지 않는다.

- [ ] **Step 4: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k readme_category_labels -v`
Expected: PASS

- [ ] **Step 5: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 6: 커밋한다**

```bash
git add docs/review-rubric.md docs/reviews/README.md
git commit -m "docs(review): L4를 표현 정렬 범주로 넓힌다 (#88)"
```

---

### Task 4: 증명 의무 표와 증명 모듈을 정본에 넣고 L7을 넓힌다

**Files:**
- Modify: `docs/writing-rules.md:181-184` (증명 모듈)
- Modify: `docs/review-rubric.md:15` (L7 불릿)
- Test: `.claude/test_review_post.py` (`TestAuthoringGuideContracts` 클래스 끝)

**Interfaces:**
- Consumes: 없음
- Produces: 정본에 `###### 강한 주장과 증명 의무` 헤딩과 의무 이름 문자열(`완전성`, `건전성`, `유일성`, `존재성`, `최적성`, `종료성`)이 있다. Task 5의 사례 4와 Task 7의 2단계 항목이 이 표를 가리킨다.

- [ ] **Step 1: 실패하는 계약 테스트를 쓴다**

`.claude/test_review_post.py`의 `TestAuthoringGuideContracts` 클래스 맨 끝에 넣는다.

```python
    def test_canonical_guide_defines_proof_obligations_per_claim(self):
        """강한 주장이 만드는 의무를 이름으로 부르지 못하면 닫혔는지 판단할 수 없다(#88)."""
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")

        self.assertIn("###### 강한 주장과 증명 의무", text)
        for obligation in ("완전성", "건전성", "유일성", "존재성", "최적성", "종료성"):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, text)

    def test_canonical_guide_proof_module_covers_scope_and_degenerate_cases(self):
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        module = text.split("##### 증명 모듈", 1)[1].split("\n##### ", 1)[0]

        for term in ("적용 영역", "한정사", "MECE", "base", "step",
                     "퇴화 사례", "직관"):
            with self.subTest(term=term):
                self.assertIn(term, module)

    def test_canonical_rubric_l7_points_at_the_obligation_table(self):
        rubric = (REPO_ROOT / "docs" / "review-rubric.md").read_text(encoding="utf-8")
        l7 = rubric.split("- **L7 ", 1)[1]

        for term in ("비용 모델", "점화식", "증명 의무", "직관",
                     "docs/writing-rules.md"):
            with self.subTest(term=term):
                self.assertIn(term, l7)
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "proof_obligations_per_claim or proof_module_covers or l7_points_at" -v`
Expected: 3 failed

- [ ] **Step 3: 증명 모듈을 6항으로 늘리고 표를 붙인다**

`docs/writing-rules.md`의 `##### 증명 모듈` 블록 전체를 아래로 교체한다. 기존 두 항목을 맨 앞에 그대로 남긴다.

```markdown
##### 증명 모듈

- [ ] 증명할 명제, 전제, 사용한 정의와 정리, 각 추론 단계, 결론을 구분한다.
- [ ] 생략한 단계와 외부 정리의 출처를 표시해 리뷰어가 타당성을 판정할 수 있게 한다.
- [ ] 가정, 적용 영역, 사용한 기호의 정의를 증명 앞에 모은다. 적용 영역은 주장이 성립하는 입력과 조건의 범위다.
- [ ] 표기와 한정사가 문단, 수식, 의사코드 사이에서 같은 뜻으로 쓰이는지 문서 전체에서 대조한다.
- [ ] 경우 구분이 상호 배타적이고 전체를 포괄하는지(MECE) 확인하고, 귀납 논증은 base와 step을 나눠 각각 닫는다.
- [ ] 경계값, 빈 입력, 최소 크기, 중복값, 동일값처럼 그 문제의 퇴화 사례를 다루거나 다루지 않아도 되는 이유를 적는다.
- [ ] 직관 설명과 증명을 구분해 표시하고 직관을 증명 자리에 두지 않는다.
- [ ] 강한 주장마다 아래 표로 의무를 도출하고 각 의무를 닫은 위치를 리뷰 인계에 적는다.

###### 강한 주장과 증명 의무

강한 한정사는 그 자체로 증명 의무를 만든다. 주장을 약하게 고치는 것도 의무를 닫는 방법이다.

| 주장 형태 | 생기는 의무 | 닫는 방법 |
|---|---|---|
| 모든 …에 대해 성립한다 | 완전성 | 임의 원소를 잡아 논증하거나 구조적 귀납으로 전 범위를 덮는다 |
| …만이 / …인 경우에만 | 건전성과 역방향 | 양방향을 각각 증명하거나 필요조건과 충분조건을 나눠 적는다 |
| 유일하다 | 유일성 | 서로 다른 둘을 가정해 같음을 유도한다 |
| 존재한다 / 항상 찾는다 | 존재성 | 구성해 보이거나 비존재 가정에서 모순을 얻는다 |
| 정확히 한 번 …한다 | 존재성과 중복 배제 | 최소 한 번과 두 번 이상 불가를 각각 닫는다 |
| 최적이다 | 최적성 | 임의 해와 비교하거나 교환 논증으로 손실 없음을 보인다 |
| 종료한다 | 종료성 | 단계마다 감소하는 정수 척도를 제시한다 |
```

- [ ] **Step 4: 루브릭 L7을 넓힌다**

`docs/review-rubric.md`의 L7 불릿 한 줄을 아래로 교체한다. 이름 `논증·복잡도 정확성`은 바꾸지 않는다(README 색인과 대조된다).

```markdown
- **L7 논증·복잡도 정확성:** 수학·알고리즘 주장이 실제로 옳은지 따진다. ① 본문 예시가 주장한 값으로 실제 계산되는가(예: 총 이익, 거리), ② 시간·공간 복잡도 주장에 비용 모델(무엇을 1 연산으로 세는지, 입력 크기 기호, 계산 모델)이 밝혀져 있고 알고리즘과 맞는가, ③ 재귀 알고리즘은 점화식의 각 항과 기저 조건이 검증되었는가, ④ 강한 주장이 만든 증명 의무가 논증으로 닫혔는가 — 경우 구분이 빠짐·겹침 없이(MECE) 완결적인지, 귀납의 base·step이 닫히는지, 경계와 퇴화 사례를 다루는지 본다, ⑤ 직관 설명을 형식적 증명 자리에 세우지 않았는가. 주장 형태별 의무 목록은 `docs/writing-rules.md`의 「강한 주장과 증명 의무」가 정본이다.
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "proof_obligations_per_claim or proof_module_covers or l7_points_at" -v`
Expected: 3 passed

- [ ] **Step 6: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 7: 커밋한다**

```bash
git add docs/writing-rules.md docs/review-rubric.md .claude/test_review_post.py
git commit -m "docs(writing): 강한 주장이 만드는 증명 의무를 표로 세운다 (#88)"
```

---

### Task 5: 의무를 닫지 않은 진단 사례를 넣는다

**Files:**
- Modify: `docs/writing-rules.md:65` (`아래 세 사례는` → `아래 네 사례는`), `docs/writing-rules.md:121` (사례 3 뒤에 사례 4 삽입)
- Modify: `.claude/test_review_post.py:1477-1508` (`test_canonical_guide_has_three_annotated_examples_and_split_policy`)

**Interfaces:**
- Consumes: Task 4가 만든 「강한 주장과 증명 의무」 표.
- Produces: 정본의 진단 사례가 4개다. 주석 문자열 `**결함:**`, `**수정 후**`, `**개선 이유:**`가 각각 4번 등장한다.

- [ ] **Step 1: 기존 테스트를 4개 기준으로 고친다**

`test_canonical_guide_has_three_annotated_examples_and_split_policy`가 사례를 정확히 3개로 못 박고 있다. 이름과 기대값을 함께 바꾼다.

```python
    def test_canonical_guide_has_four_annotated_examples_and_split_policy(self):
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
            {"**결함:**": 4, "**수정 후**": 4, "**개선 이유:**": 4},
        )
        for term in (
            "개념 설명 문단",
            "증명 진행 문단",
            "코드 및 예시 설명 문단",
            "증명 의무를 닫지 않은 문단",
            "독립된 질문",
            "고정 템플릿을 요구하지 않는다",
        ):
            self.assertIn(term, text)
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k four_annotated_examples -v`
Expected: FAIL — `AssertionError: {'**결함:**': 3, ...} != {'**결함:**': 4, ...}`

- [ ] **Step 3: 사례 소개 문장의 수를 고친다**

`docs/writing-rules.md`의 `##### 진단용 전후 사례` 아래 문장에서 `아래 세 사례는`을 `아래 네 사례는`으로 바꾼다.

- [ ] **Step 4: 사례 4를 넣는다**

사례 3 블록이 끝나는 곳, `이 사례들은 독립적인 작성과 리뷰 판단을 돕는 진단 방향이다.`로 시작하는 문단 **앞에** 아래를 넣는다.

```markdown
###### 사례 4. 증명 의무를 닫지 않은 문단

**수정 전**

각 정점은 스택에 정확히 한 번 들어가므로 그레이엄 스캔의 스택 연산은 $O(n)$이다.

**결함:**

「정확히 한 번」은 최소 한 번 들어감과 두 번 이상 들어가지 않음을 함께 요구하는데 둘 다 논증하지 않았다. 무엇을 1 연산으로 세는지도 밝히지 않아 push와 pop을 합친 비용인지 알 수 없고, 정렬 비용이 이 주장에 포함되는지가 모호하다.

**수정 후**

각 정점은 정렬 순서대로 한 번씩 방문되므로 push는 정점마다 최소 한 번 일어난다. pop된 정점은 껍질 내부로 판정되어 이후 후보에서 제외되므로 다시 push되지 않는다. push 횟수는 정점마다 정확히 한 번이고 pop 횟수는 그보다 크지 않다. push와 pop을 각각 1 연산으로 세면 스택 연산의 총 횟수는 $2n$ 이하이므로 $O(n)$이다. 앞선 정렬 비용 $O(n\log n)$은 이 주장에 포함되지 않는다.

**개선 이유:**

「정확히 한 번」이 만든 두 의무를 각각 닫았다. 존재성은 정렬 순서 방문으로, 중복 배제는 pop된 정점이 후보에서 제외된다는 성질로 닫힌다. 무엇을 1 연산으로 세는지 비용 모델을 밝히고 정렬 비용을 분리해 주장의 적용 영역을 좁혔다. 논증의 타당성은 별도 검증 자료를 바탕으로 리뷰에서 확정한다.
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k four_annotated_examples -v`
Expected: PASS

- [ ] **Step 6: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 7: 커밋한다**

```bash
git add docs/writing-rules.md .claude/test_review_post.py
git commit -m "docs(writing): 의무를 닫지 않은 증명 문단을 진단 사례로 넣는다 (#88)"
```

---

### Task 6: 복잡도 모듈을 늘리고 표현 정렬 모듈을 만든다

**Files:**
- Modify: `docs/writing-rules.md:201-204` (복잡도 모듈), 그 뒤에 표현 정렬 모듈 삽입
- Test: `.claude/test_review_post.py` (`TestAuthoringGuideContracts` 끝)

**Interfaces:**
- Consumes: Task 3이 넓힌 L4 범주 이름.
- Produces: 정본에 `##### 표현 정렬 모듈` 헤딩과 문자열 `비재귀 작업`, `비용 모델`, `점화식`이 있다.

- [ ] **Step 1: 실패하는 계약 테스트를 쓴다**

```python
    def test_canonical_guide_complexity_module_defines_cost_model(self):
        """비용 모델 없이 Big-O를 단정하면 무엇을 세는지 검증할 수 없다(#88)."""
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        module = text.split("##### 복잡도 모듈", 1)[1].split("\n##### ", 1)[0]

        for term in ("비용 모델", "1 연산", "점화식", "기저 조건", "비재귀 작업"):
            with self.subTest(term=term):
                self.assertIn(term, module)

    def test_canonical_guide_has_a_representation_alignment_module(self):
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")

        self.assertIn("##### 표현 정렬 모듈", text)
        module = text.split("##### 표현 정렬 모듈", 1)[1].split("\n### ", 1)[0]
        for term in ("의사코드", "계산 예시", "SVG", "수식",
                     "N/A — 해당 요소 없음"):
            with self.subTest(term=term):
                self.assertIn(term, module)
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "complexity_module_defines or representation_alignment" -v`
Expected: 2 failed

- [ ] **Step 3: 복잡도 모듈에 3항을 더한다**

`##### 복잡도 모듈` 블록을 아래로 교체한다. 기존 두 항목을 앞에 남긴다.

```markdown
##### 복잡도 모듈

- [ ] 입력 크기와 계산 모델을 정의하고 시간 및 공간 복잡도의 유도 근거를 적는다.
- [ ] 최악, 평균, 상환 분석 중 어느 기준인지 밝히고 코드 설명과 일치하는지 확인할 자료를 준비한다.
- [ ] 비용 모델을 밝힌다. 무엇을 1 연산으로 세는지, 입력 크기 기호가 무엇인지, 어떤 계산 모델을 쓰는지 적는다.
- [ ] 재귀 알고리즘은 점화식의 각 항이 무엇을 세는지와 기저 조건을 검증한다.
- [ ] 재귀 호출 밖의 작업은 비재귀 작업으로 부르고 결합, 분할, 순회 중 무엇인지 밝힌다. 「나머지」나 「기타」처럼 모호한 이름을 쓰지 않는다.
```

- [ ] **Step 4: 표현 정렬 모듈을 만든다**

복잡도 모듈 블록 뒤, `### 5. 문장 퇴고` 앞에 넣는다.

```markdown
##### 표현 정렬 모듈

- [ ] 본문 설명, 수식, 의사코드, 계산 예시, SVG가 같은 전제, 같은 실행 순서, 같은 값, 같은 결론을 말하는지 대조한다.
- [ ] 한 표현을 고쳤으면 나머지 표현에 같은 수정이 필요한지 확인하고, 대조한 표현 목록을 리뷰 인계에 적는다.
- [ ] 그 글에 없는 표현은 `N/A — 해당 요소 없음`으로 남긴다.

리뷰는 이 대조 결과를 L4 표현 정렬 범주로 판정한다.
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "complexity_module_defines or representation_alignment" -v`
Expected: 2 passed

- [ ] **Step 6: 6단계 헤딩 순서가 깨지지 않았는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k six_stages_in_order -v`
Expected: PASS — 새 모듈이 `#####`이므로 `### N.` 단계 헤딩을 늘리지 않는다.

- [ ] **Step 7: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 8: 커밋한다**

```bash
git add docs/writing-rules.md .claude/test_review_post.py
git commit -m "docs(writing): 비용 모델 기준과 표현 정렬 모듈을 세운다 (#88)"
```

---

### Task 7: 주장 표식과 투명 확장 기준을 앞 단계에 넣는다

**Files:**
- Modify: `docs/writing-rules.md:40` (1단계 공통 필수, provenance 항목 뒤)
- Modify: `docs/writing-rules.md:48` (2단계 공통 필수, 첫 항목 뒤)
- Test: `.claude/test_review_post.py` (`TestAuthoringGuideContracts` 끝)

**Interfaces:**
- Consumes: Task 4가 만든 「강한 주장과 증명 의무」 표.
- Produces: 없음 (마지막 내용 태스크)

- [ ] **Step 1: 실패하는 계약 테스트를 쓴다**

```python
    def test_canonical_guide_marks_strong_claims_at_design_stage(self):
        """의무를 4단계에서 처음 발견하면 수정이 구조 변경이 된다(#88)."""
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        stage_two = text.split("### 2. 글 설계", 1)[1].split("\n### 3. ", 1)[0]

        for term in ("강한 한정사", "정확히 한 번", "증명 의무"):
            with self.subTest(term=term):
                self.assertIn(term, stage_two)

    def test_canonical_guide_allows_transparent_intent_preserving_extension(self):
        """추가를 일률적으로 금지하면 승인된 확장까지 불일치로 몰린다(#88)."""
        text = (REPO_ROOT / "docs" / "writing-rules.md").read_text(encoding="utf-8")
        stage_one = text.split("### 1. 원문 확인", 1)[1].split("\n### 2. ", 1)[0]

        self.assertIn("추가는 금지가 아니다", stage_one)
        for term in ("provenance", "승인", "의도"):
            with self.subTest(term=term):
                self.assertIn(term, stage_one)
```

- [ ] **Step 2: 테스트가 실패하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "strong_claims_at_design or transparent_intent" -v`
Expected: 2 failed

- [ ] **Step 3: 1단계에 투명 확장 기준을 넣는다**

`- [ ] 원문, 명시적으로 승인된 추가, 확인이 필요한 추가를 구분해 포스트별 스펙이나 작업 메모에 provenance를 기록한다.` 항목 **바로 뒤에** 넣는다.

```markdown
- [ ] **원문 밖 추가는 금지가 아니다.** 추가임을 provenance에 밝히고, 승인된 포스트별 스펙과 충돌하지 않고, 원문의 구조·논증 흐름·의도를 보존하면 허용한다. 세 조건 중 하나라도 지키지 못하면 승인을 받기 전까지 넣지 않는다.
```

- [ ] **Step 4: 2단계에 주장 표식 항목을 넣는다**

`- [ ] 글의 질문, 답, 답을 지지할 정의, 근거, 증명 순서를 먼저 세운다.` 항목 **바로 뒤에** 넣는다.

```markdown
- [ ] 핵심 주장에서 강한 한정사(모든, 유일한, 정확히 한 번, 항상, 최적)를 표시하고, 각 주장이 만드는 증명 의무를 4단계 「강한 주장과 증명 의무」 표로 도출해 적는다. 의무를 닫을 자리가 구조에 없으면 주장을 약하게 고치거나 그 논증을 담을 절을 만든다.
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `python -m pytest .claude/test_review_post.py -k "strong_claims_at_design or transparent_intent" -v`
Expected: 2 passed

- [ ] **Step 6: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0

- [ ] **Step 7: 커밋한다**

```bash
git add docs/writing-rules.md .claude/test_review_post.py
git commit -m "docs(writing): 설계 단계에서 강한 주장과 확장 기준을 정한다 (#88)"
```

---

### Task 8: 게이트와 완료기준을 대조한다

**Files:**
- Read: `docs/superpowers/specs/2026-08-18-proof-obligation-l6-guidance-design.md`
- 수정 없음. 검증과 증거 수집만 한다.

**Interfaces:**
- Consumes: Task 1~7의 모든 문서 변경
- Produces: PR 본문에 쓸 완료기준 대조표와 실행 증거

- [ ] **Step 1: 전체 테스트를 돌린다**

Run: `python -m pytest .claude -q`
Expected: 실패 0. 기준선 `207 passed`에 신규 12개가 더해져 `219 passed` 내외다. 정확한 수치를 기록한다.

- [ ] **Step 2: 저장소 게이트가 여전히 초록인지 확인한다**

Run: `python .claude/review_post.py --gate`
Expected: `게이트 대상 31개`, 면제 4개, exit 0. 문서 개정이 과거 리포트 판정을 깨지 않았다는 증거다.

exit 0이 아니면 멈추고 원인을 보고한다. 범주를 늘리지 않았으므로 coverage 실패는 나오지 않아야 한다.

- [ ] **Step 3: 계약 테스트가 실제로 문서를 붙잡는지 확인한다**

`docs/review-rubric.md`에서 `source unavailable` 행 한 줄을 임시로 지우고 테스트를 돌린다.

Run: `python -m pytest .claude/test_review_post.py -k l6 -v`
Expected: FAIL

확인 뒤 `git checkout docs/review-rubric.md`로 되돌린다. 되돌린 뒤 같은 명령이 PASS인지 다시 확인한다.

- [ ] **Step 4: 이슈 완료기준 6개를 대조한다**

각 기준에 대해 반영 위치를 아래 형식으로 적는다. 근거 없이 통과로 적지 않는다.

| 완료기준 | 반영 위치 |
|---|---|
| 증명 가정·적용 영역·표기와 한정사 일관성·MECE·base와 step·경계와 퇴화·직관과 증명 구분 | `docs/writing-rules.md` 증명 모듈 |
| 강한 주장별 증명 의무 식별·닫기 절차와 예시 | 같은 문서 「강한 주장과 증명 의무」 표, 진단 사례 4, 2단계 주장 표식 항목 |
| 비용 모델·점화식 검증·비재귀 작업 용어 | 같은 문서 복잡도 모듈 |
| 본문·수식·의사코드·worked example·SVG 정렬 체크리스트 | 같은 문서 표현 정렬 모듈, `docs/review-rubric.md` L4 |
| L6 네 상태와 severity·gate 동작, 미확인 사례 보고 예시 | `docs/review-rubric.md` L6, `docs/reviews/README.md` L6 소절 |
| 투명하고 의도 보존적인 확장 허용 기준 | `docs/writing-rules.md` 1단계, `docs/review-rubric.md` L6 `approved extension` |

- [ ] **Step 5: 변경 요약을 확인한다**

Run: `git diff --stat main...HEAD`
Expected: `docs/writing-rules.md`, `docs/review-rubric.md`, `docs/reviews/README.md`, `.claude/commands/review-post.md`, `.claude/commands/review-post-all.md`, `.claude/test_review_post.py`, 그리고 스펙·계획 문서 2개. `.claude/review_post.py`는 목록에 없어야 한다.

`review_post.py`가 목록에 있으면 범위를 벗어난 변경이다. 멈추고 보고한다.

- [ ] **Step 6: 사용자에게 결과를 보고한다**

테스트 수치, 게이트 exit code, 완료기준 대조표, `git diff --stat` 결과를 함께 보고한다. PR 생성은 사용자 승인 뒤에 한다.

---

## 검증 요약

| 명령 | 기대 |
|---|---|
| `python -m pytest .claude -q` | 실패 0 (기준선 207 + 신규 12 내외) |
| `python .claude/review_post.py --gate` | 대상 31개, 면제 4개, exit 0 |
| `git diff --stat main...HEAD` | `review_post.py` 미포함 |

## 범위 밖

- strict gate 또는 report serializer 구현. `review_post.py` 본체와 `review-report/v2` 스키마를 바꾸지 않는다.
- 과거 리포트 59개의 L6 finding 행 수정.
- 기존 블로그 글 재작성.
- 새 LLM 범주(L8) 신설.
- `docs/readability-guide.md` 개정.
