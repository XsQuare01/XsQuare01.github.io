## 결정적 검사: src/content/posts/convex-hull-bst-tangent.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/convex-hull-bst-tangent.md

### 🟡 [L1] src/content/posts/convex-hull-bst-tangent.md:25

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-bst-tangent.md:25
- quote: `## 다시, 무대 위로 올라와서,`
- message: 섹션 제목이 비유적이고 끝 쉼표로 마무리되어 학습 노트의 평서체 흐름보다 수사적으로 보인다.
- recommendation: `## 다시, 문제 설정으로`처럼 평이한 제목으로 바꾸고 끝 쉼표를 제거한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-bst-tangent.md:35

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-bst-tangent.md:35
- quote: `다행히 볼록성 덕분에 이 조건이 **국소 조건**으로 바뀐다.`
- message: 두 이웃이 직선 아래이면 사슬 전체가 아래라는 핵심 명제가 제시되지만, 왜 국소 조건이 전역 접선 조건을 보장하는지 설명이 짧다. 이 글의 핵심 정확성 근거라 독자가 논리 도약으로 느낄 수 있다.
- recommendation: 볼록 사슬에서 한 꼭짓점 양쪽 이웃이 후보 직선 아래이고 사슬이 위로 볼록하면, 사슬이 그 직선 위로 다시 올라가려면 인접 구간 중 하나에서 이미 위쪽 이웃이 생겨야 한다는 식의 한두 문장 증명을 추가한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-bst-tangent.md:66

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-bst-tangent.md:66
- quote: `매 단계 후보가 절반으로 줄고, 트리 높이가 $O(\log N)$이므로 접점도 $O(\log N)$에 나온다.`
- message: 균형 BST의 O(log N) 보장은 높이에서 나오며, 일반적인 균형 트리의 각 하강이 항상 후보 수를 정확히 절반으로 줄인다고 말하기는 어렵다. `절반` 표현은 그림의 직관으로는 좋지만 복잡도 논증으로는 과하게 강하다.
- recommendation: `정확히 절반`처럼 읽히지 않도록 `한쪽 서브트리를 버리고 균형 트리의 높이만큼만 내려간다`로 바꾸거나, 절반은 이상화된 직관이라고 분리해 설명한다.
- gate_effect: warn

### 🟢 [L2] not-recorded

- severity: 🟢
- source: L
- rule_id: L2
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 문제 설정 → 접점 조건 → 방향 판정 → 이진 탐색 → 코드의 전개가 읽는 순서대로 이어진다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] not-recorded

- severity: 🟢
- source: L
- rule_id: L3
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. x좌표 키, upper hull, lower hull, prev/next, left/right 자식의 구분이 일관되며 이전 y-key 혼동으로 되돌아가지 않는다.
- recommendation: 현재 용어 체계를 유지한다.
- gate_effect: info

### 🟢 [L4] not-recorded

- severity: 🟢
- source: L
- rule_id: L4
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. `tangent-condition.svg`, `direction-cases.svg`, `halving.svg`의 후보 번호, 위/아래 판정, 좌우 이동 레이블이 본문 설명과 대응한다.
- recommendation: 현재 SVG와 본문 연결을 유지한다.
- gate_effect: info

### 🟢 [L5] not-recorded

- severity: 🟢
- source: L
- rule_id: L5
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목과 description이 3편에서 미룬 균형 트리 접선 탐색의 방향 판정과 O(log N) 근거를 잘 대표한다.
- recommendation: 현재 frontmatter를 유지한다.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: Notion 원본 대조는 수행하지 못했다. 현재 세션에서 사용 가능한 MCP 리소스에 notion-search/notion-fetch가 없어 저장소의 관련 계획/스펙 문서와 이전 리뷰 맥락을 기준으로 검토했다.
- recommendation: Notion 원본 접근이 가능해지면, 원문의 right-hull/y-BST 설명이 현재 글의 upper/lower x-chain 설명으로 충실히 번역됐는지 별도로 대조한다.
- gate_effect: info

요약: 🔴 0 · 🟡 3 · 🟢 5

## 반영 결과 (2026-07-10, 2차)

- [L1:25] 섹션 제목은 사용자 확정에 따라 "다시, 무대 위로 올라와서," 유지(지적 무시하기로 결정).
- [L7:35] 국소 조건이 왜 전역 접선 조건을 보장하는지 보강. "직선 p–t가 t에서 사슬의 지지선이 되고, 위로 볼록한 사슬은 어떤 지지선도 넘지 않는다 → 다시 위로 솟으려면 볼록성에 어긋나는 꺾임이 필요"라는 한 문단 추가.
- [L7:66] "매 단계 정확히 절반" 표현 완화. "한쪽 서브트리 전체가 빠지고 트리 높이만큼 내려간다 → 균형 BST 높이 O(log N)에서 보장이 온다"로 바꾸고, 절반은 이상화된 직관으로 분리(괄호). 이미지 alt·핵심 정리·halving.svg 문구도 "절반" → "서브트리/높이"로 통일.
- 반영 후 결정적 검사 "발견 사항 없음 ✅", `npm run build` 통과 (105 pages).
