## 결정적 검사: src/content/posts/quicksort.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/quicksort.md

### 🔴 [L7] src/content/posts/quicksort.md:42

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/quicksort.md:42
- quote: `while (i <= j) {`
- message: 분할 코드가 pivot과 같은 값이 있는 입력에서 멈추지 않을 수 있다. 예를 들어 `[5, 5]`에서 `i == j == 1`이고 `a[i] == p`이면 43행의 `a[i] < p`와 44행의 `a[j] > p`가 모두 거짓이며, 45행의 `if (i < j)`도 거짓이라 포인터가 전혀 이동하지 않는다. 또한 57-60행의 “큰 값/작은 값만” 설명은 중복 원소가 없는 경우에만 맞는다.
- recommendation: 중복 원소를 배제한다는 전제를 명시하거나, 같은 값에서도 포인터가 진행되는 Hoare/Lomuto 계열 분할로 코드와 설명을 조정하라고 권한다.
- gate_effect: fail

### 🟡 [L2] src/content/posts/quicksort.md:181

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/quicksort.md:181
- quote: `같은 분모끼리 다시 묶으면 정리된다.`
- message: 175-188행의 텔레스코핑 설명은 결론인 `Θ(n log n)`에는 도달하지만, 178-185행의 급수 전개가 시작항·끝항을 어디까지 포함하는지 명확하지 않다. 특히 185행의 등호는 유한합의 마지막 `3/(n+1)` 같은 꼬리항과 초기값 처리를 생략해 독자가 “정확한 등식”으로 오해할 수 있다.
- recommendation: 해당 전개가 점근적 정리를 위한 근사·상수항 생략임을 식 바로 앞에서 밝히거나, 유한합의 범위와 남는 꼬리항을 한 줄 추가하라고 권한다.
- gate_effect: warn

### 🟡 [L4] public/images/quicksort/partition-pointers.svg:6

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/quicksort/partition-pointers.svg:6
- quote: `i는 큰 값에서, j는 작은 값에서 멈추고 두 값을 맞바꾼다`
- message: SVG의 일반 설명이 본문 코드와 완전히 일치하지 않는다. 본문 코드의 내부 반복문은 `a[i] < p` 동안 전진하고 `a[j] > p` 동안 후진하므로 실제 정지 조건은 각각 `p 이상`, `p 이하`다. SVG 예시의 8과 2 자체는 맞지만, 일반 레이블은 중복 원소가 있을 때 부정확하다.
- recommendation: SVG 레이블을 `i는 p 이상에서, j는 p 이하에서 멈춘다`처럼 바꾸거나, 그림과 본문 모두 “서로 다른 값만 있는 예시”라는 전제를 붙이라고 권한다.
- gate_effect: warn

### 🟢 [L1] not-recorded

- severity: 🟢
- source: L
- rule_id: L1
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 현재 문체는 전반적으로 `~다` 평서체를 유지하며, 줄표·비유·경구식 마무리가 리뷰 기준상 별도 수정이 필요할 정도로 반복되지는 않는다.
- gate_effect: info

### 🟢 [L3] not-recorded

- severity: 🟢
- source: L
- rule_id: L3
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: pivot, 분할, 기댓값, 조화수 등 핵심 용어 사용이 일관적이다.
- gate_effect: info

### 🟢 [L5] not-recorded

- severity: 🟢
- source: L
- rule_id: L5
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 제목과 description은 글의 실제 중심인 퀵 정렬의 평균 시간 분석과 분할 과정을 대표한다.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: Notion 원본 대조는 수행하지 못했다. 현재 실행 환경에는 `notion-search`와 `notion-fetch` 도구가 제공되지 않았고, 저장소 안에서도 대응되는 원본 자료를 확인하지 못했다.
- recommendation: Notion 원본을 확보할 수 있으면 원문의 핵심 구조·증명 흐름·주장 누락 여부를 별도로 재검토하라고 권한다.
- gate_effect: info

요약: 🔴 1 · 🟡 2 · 🟢 4

---

## 반영 결과 (2026-06-27)

| 항목 | 판단 | 조치 |
|---|---|---|
| 🔴 L7 (line 42) | 반영 | 중복 값 무한 루프 수정. 내부 조건을 비대칭(`a[i] < p` / `a[j] >= p`)으로 바꿔 `=p` 값에서도 포인터가 항상 진행하도록 보장. Python brute-force(값 0~3·크기 0~7 전 조합 + 무작위 2만 건)로 무한 루프·오정렬 0건 검증. 중복 처리 설명 한 문단 추가. |
| 🟡 L2 (line 181) | 반영 | 급수 정리 직전에 "유한합의 꼬리항 $\frac{3}{n+1}$과 초기값 $F(0)$는 상수·저차항이라 무시하며, 아래 등호는 지배항만 남긴 근사"임을 명시. |
| 🟡 L4 (SVG line 6) | 반영 | SVG 부제를 "i는 p 이상에서, j는 p 미만에서 멈추고 두 값을 맞바꾼다"로 정정해 중복 값에서도 정확하게. |
| 🟢 L1·L3·L5 | 정보 | 이슈 없음. 조치 불필요. |
| 🟢 L6 | 무효 | "Notion 대조 미수행" 지적은 본 세션에서 notion-fetch로 원본("⚡ Quick Sort", 154cb27e…)을 이미 대조했으므로 해당 없음. |

`npm run build` 재검증 통과 (81 페이지). 반영 후 🔴 0 · 🟡 0 · 🟢 4(+무효 1).
