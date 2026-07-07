## 결정적 검사: src/content/posts/convex-hull-1.md
발견 사항 없음 ✅

## LLM 비평

- 🔴 [L4] public/images/convex-hull-1/wrapping-full.svg:24
  - severity: 🔴
  - source: L
  - rule_id: L4
  - location: public/images/convex-hull-1/wrapping-full.svg:24
  - quote: "<line x1=\"330\" y1=\"382\" x2=\"145\" y2=\"338\" marker-end=\"url(#f-g)\"/>"
  - message: 본문과 코드는 현재 선분의 왼쪽에 모든 점을 두는 방향으로 다음 점을 고르는 설명인데, 전체 흐름 SVG의 첫 화살표는 최하단 시작점에서 왼쪽 위 점으로 향한다. 이 방향에서는 나머지 점들이 시각적으로 선분의 오른쪽에 놓여, 본문·코드의 방향 규약과 반대로 보인다.
  - recommendation: `wrapping-full.svg`의 순회 방향을 본문·코드와 맞추거나, 본문에서 SVG가 반대 방향 순회를 예시한다고 명확히 설명한다.
  - gate_effect: fail

- 🔴 [L7] src/content/posts/convex-hull-1.md:33
  - severity: 🔴
  - source: L
  - rule_id: L7
  - location: src/content/posts/convex-hull-1.md:33
  - quote: "오목한 부분이 있으면 그 안으로 파고든 만큼 넓이·둘레를 더 줄일 수 있으므로, \"가장 작은\"과 \"볼록\"은 사실상 같은 것을 요구한다."
  - message: 볼록 껍질은 점들을 포함하는 가장 작은 볼록 집합/다각형이지, 볼록 조건 없이 가장 작은 다각형과 같은 문제가 아니다. 또한 오목하게 파고들면 넓이는 줄 수 있지만, 해당 오목 경로를 직선 현으로 대체할 때보다 둘레는 보통 삼각부등식 때문에 늘어난다.
  - recommendation: "볼록 조건을 먼저 고정한 뒤 그 안에서 가장 작은 다각형을 찾는다"고 분리해 설명하고, 오목 부분이 둘레까지 줄인다는 문장은 삭제하거나 넓이와 둘레를 구분한다.
  - gate_effect: fail

- 🟡 [L7] src/content/posts/convex-hull-1.md:75
  - severity: 🟡
  - source: L
  - rule_id: L7
  - location: src/content/posts/convex-hull-1.md:75
  - quote: "$A \to B$의 기울기 $m_{AB}$보다 $B \to C$의 기울기 $m_{BC}$가 더 크면(더 가파르게 위로 꺾이면) 왼쪽으로 도는 것이다."
  - message: 기울기 비교 직관은 분모의 부호와 x좌표 순서가 통제될 때만 안전하다. 현재 가정은 x좌표가 서로 다르다는 것뿐이라, 분모를 곱할 때 부등호 방향이 바뀔 수 있고 "기울기가 더 크면 좌회전"도 일반 명제로는 성립하지 않는다.
  - recommendation: 기울기 비교는 제한된 배치에서의 직관이라고 밝히고, 일반 판정은 바로 외적/행렬식 부호로 유도한다.
  - gate_effect: warn

- 🟡 [L7] src/content/posts/convex-hull-1.md:111
  - severity: 🟡
  - source: L
  - rule_id: L7
  - location: src/content/posts/convex-hull-1.md:111
  - quote: "좌표가 크면 곱셈 오버플로를 막기 위해 `long long`을 쓴다."
  - message: `long long`은 좌표 범위가 충분히 작다는 전제가 있을 때만 CCW 곱셈 overflow를 막는다. 임의의 큰 정수 좌표라면 `(b.x - a.x) * (c.y - a.y)` 자체가 signed overflow를 낼 수 있다.
  - recommendation: `long long`으로 안전한 좌표 범위를 명시하거나, 범위를 일반화하려면 `__int128`로 곱셈을 수행한다고 설명한다.
  - gate_effect: warn

- 🟢 [L1] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L1
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 현재의 ~다 평서체와 강조 빈도를 유지한다.
  - gate_effect: info

- 🟢 [L2] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L2
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 정의, 가정, 브루트포스, CCW, Package Wrapping으로 이어지는 큰 흐름은 유지한다. 위 L7 지적처럼 수학적으로 부정확한 문장만 분리해 고친다.
  - gate_effect: info

- 🟢 [L3] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L3
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 볼록 껍질, 볼록/오목, 변/선분, CCW, Package Wrapping 용어를 현재처럼 일관되게 유지한다.
  - gate_effect: info

- 🟢 [L5] src/content/posts/convex-hull-1.md:2
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: src/content/posts/convex-hull-1.md:2
  - quote: "볼록 껍질 ① — 정의, CCW, 그리고 Package Wrapping"
  - message: 검토 완료, 이슈 없음
  - recommendation: 제목과 description이 실제 범위인 볼록 껍질 정의, CCW, Package Wrapping을 잘 대표한다.
  - gate_effect: info

- 🟢 [L6] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L6
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 현재 세션에서 notion-search/notion-fetch 도구가 제공되지 않아 노션 원문 대조는 수행하지 못했다.
  - recommendation: 원문 충실성 확인이 필요하면 Notion MCP가 연결된 환경에서 재검토한다.
  - gate_effect: info

요약: 🔴 2 · 🟡 2 · 🟢 5
