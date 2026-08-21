schema_version: review-report/v2
target: convex-hull-2
generated_at: 2026-08-21
strict: true
sources: src/content/posts/convex-hull-2.md
summary: 🔴 0 · 🟡 2 · 🟢 6

## Findings

### 🟡 [L3] src/content/posts/convex-hull-2.md:76

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-2.md:76
- quote: 1편의 세 가정에 더해 점이 **3개 이상**이라고 둔다.
- message: 27행에서 이미 N>=3을 포함한 네 가지 가정을 상속한다고 밝혔는데, 여기서 다시 “세 가정에 더해”라고 쓰면 글 안의 가정 수와 맞지 않는다.
- recommendation: 네 가지 가정이라고 일관되게 부르거나, 여기서는 개수를 다시 세지 않도록 바꿔라.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-2.md:167

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-2.md:167
- quote: 껍질 출력에서 각도가 가장 작은 점을 찾아 거기서부터 순서대로 읽기만 하면 정렬이 끝난다.
- message: 출력 계약은 둘레를 도는 순서만 보장할 뿐 CCW 방향을 고정하지 않으므로, 시계방향 껍질이면 내림차순으로 읽히게 된다.
- recommendation: 방향을 확인해 필요하면 뒤집거나, CCW 출력 계약을 명시하라.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-2.md:10

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-2.md:10
- quote: > [1편](/blog/convex-hull-1)의 Package Wrapping은 껍질 점 하나를 확정할 때마다 남은 점 전체를 다시 훑는다.
- message: 검토 완료, 이슈 없음. 문체가 설명 중심이고 과장된 AI 신호나 지나친 수사 없이 차분하게 유지된다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-2.md:25

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-2.md:25
- quote: ## 되짚어보기 — Package Wrapping의 한계
- message: 검토 완료, 이슈 없음. 반복 탐색에서 정렬, 스캔, 하한 논증으로 이어지는 흐름이 분명하다.
- recommendation: 현재 흐름을 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/convex-hull-2.md:63

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/convex-hull-2.md:63
- quote: ![그레이엄 스캔 — 좌회전이면 push, 우회전이면 pop하며 스택이 볼록 껍질을 만들어 간다](/images/convex-hull-2/scan-steps.svg)
- message: 검토 완료, 이슈 없음. 참조한 세 SVG가 모두 본문과 맞물리며, `scan-steps.svg`는 Y, 1-7, 5의 pop, 최종 스택 순서를 그대로 담고 있고 복잡도 설명도 104행의 문단과 일치한다.
- recommendation: 현재 도판과 본문 대응을 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-2.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-2.md:2
- quote: title: "볼록 껍질 ② — Graham Scan과 정렬 하한"
- message: 검토 완료, 이슈 없음. 제목과 description이 Graham Scan과 정렬 하한 논증을 잘 대표한다.
- recommendation: 현재 메타데이터를 유지한다.
- gate_effect: info

### 🟢 [L6] docs/superpowers/specs/2026-07-08-convex-hull-2-design.md:26

- severity: 🟢
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-07-08-convex-hull-2-design.md:26
- quote: ## 본문 구성
- message: verified fidelity — the approved design spec was actually compared and the core structure, algorithm, proof flow, and SVG consolidation preserve the approved scope.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-2.md:104

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-2.md:104
- quote: **복잡도.**
- message: 검토 완료, 이슈 없음. 스캔의 상각 분석, O(N log N), 서로 다른 키로의 환원, 포물선 대체 논증이 모두 타당하다.
- recommendation: 현재 조건을 유지한다.
- gate_effect: info
