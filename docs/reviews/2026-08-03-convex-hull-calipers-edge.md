schema_version: review-report/v2
target: convex-hull-calipers-edge
generated_at: 2026-08-03
strict: true
sources: src/content/posts/convex-hull-calipers-edge.md
summary: 🔴 0 · 🟡 1 · 🟢 6

## Findings

### 🟡 [L7] src/content/posts/convex-hull-calipers-edge.md:121

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-calipers-edge.md:121
- quote: "이 루프는 모든 대척점 쌍을 **빠짐없이** 훑는다."
- message: 앞선 리포트(2026-07-15)가 지적한 "중복 없이 딱 한 번씩"이라는 과한 주장은 이미 철회돼 있다. 122행이 중복 제거는 범위 밖이라고 못박고, 121행도 "딱 한 번씩 내지는 않는다"로 정직하게 낮췄다. 다만 같은 문장에 남은 "빠짐없이"는 여전히 완전성 주장인데, 근거가 예시 수준에 머문다. 66행의 회전 지지선 논증은 **지름**이 어떤 변의 끝점과 최원 꼭짓점 쌍으로 반드시 나타난다는 것까지만 보이고, 80-82행의 세 항목은 변–변 동률 한 각도에서 네 조합이 어디서 나오는지를 직사각형으로 예시한다. 일반 볼록 껍질에서 모든 대척점 쌍이 이 루프와 동률 분기로 남김없이 등장한다는 논증은 없다. 122행이 완전 순회·종료 규칙을 범위 밖으로 미루면서 "열거가 빠짐없다는 것까지만 짚는다"고 적어, 빠짐없음은 이 글이 보인 것처럼 읽힌다.
- recommendation: "빠짐없이"를 "직사각형 예시에서 보듯 변–변 동률의 네 조합이 모두 등장한다" 정도로 한정하거나, 각 각도의 대척점 쌍이 그 각도에서 지지선에 닿는 변·꼭짓점 조합으로 남김없이 대응된다는 한 줄 논증을 덧붙여 주장과 근거의 폭을 맞춘다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-calipers-edge.md:1-139

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-calipers-edge.md:1-139
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-calipers-edge.md:1-139

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-calipers-edge.md:1-139
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-calipers-edge.md:1-139

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-calipers-edge.md:1-139
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-calipers-edge/parallel-pairs.svg:1-40

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-calipers-edge/parallel-pairs.svg:1-40
- quote: "뼈대가 기록 — (i, j), (ni, j) / 동률 분기로 추가 — (i, j+1) / 다음 변에서 나옴 — (ni, j+1)"
- message: 참조 SVG 두 개를 본문과 대조했다. `parallel-pairs.svg`의 세 레이블이 본문 80-82행의 세 항목과 그대로 대응하고, 어느 쌍을 뼈대가 잡고 어느 쌍을 분기로 채우는지가 코드 110행·115행의 두 `report` 호출과 일치한다. `contact-types.svg`의 "1개 → 2개 → 4개(2×2)" 증가도 본문 37-39행의 세 유형 서술과 같다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-calipers-edge.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-calipers-edge.md:2-4
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] docs/superpowers/specs/2026-07-15-convex-hull-calipers-edge-design.md:5

- severity: 🟢
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-07-15-convex-hull-calipers-edge-design.md:5
- quote: "원본 자료: 노션 `Convex hull 2` 노트의 Farthest Point 섹션(엣지 케이스 상세는 노션에 없어 표준 알고리즘 지식 — Toussaint 1983, Preparata–Shamos — 으로 보강. 승인된 확장)"
- message: 노션 원문(🎿 Convex hull 2)의 Farthest Point 절과 대조했다. 원문은 평행 지지선을 0도에서 180도까지 돌리며 대척점 쌍을 훑는다는 것, 가장 먼 두 점이 반드시 껍질 꼭짓점이라는 것, 전체 $O(N \log N)$까지만 다루고 평행한 변이 만드는 동률은 언급하지 않는다. 이 글이 채우는 동률 분기와 열거 문제는 원문 밖 확장이고, 스펙 5행이 그 사실과 근거 문헌을 미리 밝혀 두었다. 본문 10행도 5편이 무엇을 미뤘는지 밝히며 시작해 원문 범위를 넘어선다는 점이 독자에게 드러난다. 원문의 주장을 왜곡하거나 누락한 곳은 없다.
- recommendation: not-recorded
- gate_effect: info
