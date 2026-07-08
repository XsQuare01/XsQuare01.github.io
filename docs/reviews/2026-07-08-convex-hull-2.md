## 결정적 검사: src/content/posts/convex-hull-2.md
발견 사항 없음 ✅

## LLM 비평

### 🟡 [L7] src/content/posts/convex-hull-2.md:120

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-2.md:120
- quote: `정렬할 양수 $v_1, \cdots, v_N$이 있다고 하자.`
- message: 이어지는 126행의 “모든 각도는 ... 서로 겹치지 않는다”는 결론은 입력값이 서로 다를 때만 성립한다. 중복 양수가 있으면 같은 각도와 같은 원 위의 점으로 매핑되므로, 정렬 하한 환원의 전제가 본문에 빠져 있다.
- recommendation: 하한 환원을 시작할 때 “서로 다른 양수”를 정렬한다고 명시하라. 비교 정렬 하한은 서로 다른 키의 순열에 대해서도 성립하므로 증명의 힘은 약해지지 않는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-2.md:123

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-2.md:123
- quote: `$v_i \;\mapsto\; \theta_i = \frac{v_i}{M+1} \cdot 2\pi \;\mapsto\; \left(r\cos\theta_i,\; r\sin\theta_i\right)$`
- message: 본문은 143행에서 “좌표에 대한 대수적 연산·비교만 허용하는 모델”을 전제한다고 설명하지만, 환원 자체는 좌표 생성에 삼각함수 $\cos, \sin$을 사용한다. 계산 모델을 엄밀히 읽으면 하한 증명의 전처리가 모델 밖 연산에 의존하는 것처럼 보인다.
- recommendation: 원 위 환원이 직관적 설명임을 명시하거나, 서로 다른 양수 $v_i$를 $(v_i, v_i^2)$처럼 엄밀한 볼록 곡선 위 점으로 보내는 대수적 환원으로 바꾸라.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-2.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-2.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목·섹션·이미지 alt에 줄표가 쓰였지만 구조 표지 용도이며, 본문 문체에서 줄표 남발·경구식 마무리·과한 비유가 두드러지지 않는다.
- recommendation: 현재처럼 ~다 평서체와 설명 중심 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-2.md

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-2.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. Package Wrapping의 반복 낭비에서 각도 정렬, 스택 scan, 정렬 하한으로 넘어가는 설명 흐름이 자연스럽다.
- recommendation: 현재 흐름을 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-2.md

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-2.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 점, 껍질, 각도 정렬, CCW, push/pop, 환원 등의 용어 사용이 일관된다.
- recommendation: 현재 용어 체계를 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/convex-hull-2.md:39

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/convex-hull-2.md:39
- quote: `![각도 정렬 — 최하단 점 Y를 기준으로, 수평선에서 반시계 방향으로 훑으며 만나는 순서대로 점에 번호를 매긴다.](/images/convex-hull-2/angle-sort.svg)`
- message: 검토 완료, 이슈 없음. `angle-sort.svg`, `scan-push.svg`, `scan-pop.svg`, `scan-result.svg`, `lower-bound.svg`의 레이블·점 번호·push/pop 설명이 본문 설명과 일치한다.
- recommendation: 현재 SVG와 본문 연결을 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-2.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-2.md:2
- quote: `title: "볼록 껍질 ② — Graham Scan과 정렬 하한"`
- message: 검토 완료, 이슈 없음. 제목과 description이 실제 본문 범위인 Graham Scan, $O(N \log N)$ 복잡도, 정렬 하한을 대표한다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 다만 현재 환경에는 `notion-search`/`notion-fetch` 도구나 로컬 Notion 원문이 없어 원문 대조는 수행하지 못했다. 저장소의 현재 글 구조와 논지를 기준으로만 검토했다.
- recommendation: 원문 충실성까지 gate로 삼아야 한다면 해당 Notion 원문을 제공하거나 Notion 조회 도구를 연결한 뒤 재검토한다.
- gate_effect: info

요약: 🔴 0 · 🟡 2 · 🟢 6

## 반영 결과 (2026-07-08, 2차)

- [L7:120] "정렬할 양수" → "**서로 다른** 양수"로 전제 명시. 값이 겹치면 같은 점으로 매핑된다는 이유와, 서로 다른 키로 한정해도 비교 정렬 하한이 성립한다는 근거를 본문에 추가.
- [L7:123] 계산 모델 callout에 보강 문단 추가: $\cos$/$\sin$은 그림을 위한 선택이며, 엄밀하게는 포물선 위의 점 $(v_i, v_i^2)$으로 보내는 대수적 변환으로 같은 논증이 성립함을 명시. 원 그림(노션 원본 방식)은 직관용으로 유지.
- 반영 후 결정적 검사 "발견 사항 없음 ✅", `npm run build` 통과 (103 pages).
