schema_version: review-report/v2
target: convex-hull-4
generated_at: 2026-07-13
strict: not-recorded
summary: 🔴 1 · 🟡 1 · 🟢 6

## Findings

### 🔴 [L7] src/content/posts/convex-hull-4.md:76

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-4.md:76
- quote: while (below(R[b], L[a], L[nextDown(a)])) { a = nextDown(a); moved = true; }
- message: `below(a, b, c)`가 70행에서 방향선 `a→b` 기준으로 정의됐는데, 왼쪽 후보 검사만 `R[b]→L[a]`로 뒤집혀 있다. 방향선 기준 아래쪽 판정은 끝점을 바꾸면 부호가 반대가 되므로, 하단 접선 워킹 의사코드가 본문 설명과 달라질 수 있다.
- recommendation: 왼쪽 후보도 같은 기준선 `L[a]→R[b]`에 대해 검사하도록 고치거나, `below`가 무방향 직선 기준이라는 별도 정의와 CCW 부호 변환을 명시한다.
- gate_effect: fail

### 🟡 [L7] src/content/posts/convex-hull-4.md:107

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-4.md:107
- quote: 먼저 왼쪽 껍질의 한 점 $a$를 고정하면, $a$에서 오른쪽 껍질로 긋는 접선의 접점은 하나로 정해진다.
- message: 외부 점에서 볼록 다각형으로 긋는 접선은 일반적으로 상·하 두 개다. 문맥상 특정 사슬 또는 특정 방향의 접선을 말하는 듯하지만, 이 문장만 보면 접점이 항상 하나라는 말로 읽힌다.
- recommendation: “상단 접선을 찾는다고 고정하면”, “하단 사슬에서 찾는 접점은”처럼 대상 접선과 사슬을 먼저 제한해 모호성을 줄인다.
- gate_effect: warn

### 🟢 [L1] not-recorded

- severity: 🟢
- source: L
- rule_id: L1
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: Korean declarative tone is consistent, and no actionable AI-style filler or register break was found.
- gate_effect: info

### 🟢 [L2] not-recorded

- severity: 🟢
- source: L
- rule_id: L2
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: The section order moves from split, merge by tangents, linear walking, recurrence, then faster tangent search without a blocking flow gap.
- gate_effect: info

### 🟢 [L3] not-recorded

- severity: 🟢
- source: L
- rule_id: L3
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: Terms such as upper hull, lower hull, 상단 공통 접선, 하단 공통 접선, merge, and CCW are used consistently for this post's register.
- gate_effect: info

### 🟢 [L4] not-recorded

- severity: 🟢
- source: L
- rule_id: L4
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: All four referenced SVGs were read. The split direction, highlighted tangent endpoints, walking arrows, binary-search labels, captions, and body claims match the prose aside from the separate L7 pseudocode issue.
- gate_effect: info

### 🟢 [L5] not-recorded

- severity: 🟢
- source: L
- rule_id: L5
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: The title and description match the actual scope: divide and conquer convex hull merging, common tangents, linear walking, binary-search tangent finding, and complexity limits.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: Notion tools are unavailable in this session, so original-source comparison could not be performed. The review only checks the repository version against its own prose, math, and SVGs.
- gate_effect: info
