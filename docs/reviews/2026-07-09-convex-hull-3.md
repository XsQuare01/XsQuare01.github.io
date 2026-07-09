## 결정적 검사: src/content/posts/convex-hull-3.md
발견 사항 없음 ✅

## LLM 비평

### 🔴 [L7] src/content/posts/convex-hull-3.md:73

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-3.md:73
- quote: `그래서 껍질 점을 **균형 이진 트리(balanced BST)** 에 y좌표 순으로 담는다.`
- message: upper/lower hull의 단조성은 x좌표 또는 사슬 순서에 대한 성질이다. y좌표 순 BST는 일반적으로 hull의 인접 관계를 보존하지 않으므로, 각 노드가 양옆 변을 함께 들고 접점을 이진 탐색한다는 설명과 전체 O(N log N) 결론의 핵심 전제가 성립하지 않는다. 같은 주장은 `public/images/convex-hull-3/bst-idea.svg:10`과 본문 요약 `src/content/posts/convex-hull-3.md:111`에도 반복된다.
- recommendation: `y좌표 순`을 `upper/lower 사슬을 x순 또는 hull-chain order로 저장`으로 고치고, SVG의 `y좌표 순으로 저장` 레이블도 함께 수정한다. 전체 O(N log N)은 올바른 사슬 순서 자료구조와 접선 판정이 전제될 때만 주장한다.
- gate_effect: fail

### 🟡 [L1] src/content/posts/convex-hull-3.md:10

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-3.md:10
- quote: `이번 편은 껍질을 **한 점씩 삼키며 키우는** Plane Sweeping과`
- message: `삼키며`라는 비유가 frontmatter description, 도입부, 본문 요약에서 반복되어 글의 기술 설명보다 수사적 인상이 앞선다.
- recommendation: `점을 x좌표 순서로 하나씩 추가하며 유지하는`처럼 평이한 설명으로 바꾸고, 같은 비유의 반복을 줄인다. 어체는 현재처럼 ~다 평서체를 유지한다.
- gate_effect: warn

### 🟡 [L2] src/content/posts/convex-hull-3.md:4

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-3.md:4
- quote: `점이 왼쪽부터 하나씩 도착하거나, 껍질을 다 구한 뒤에도 새 점이 계속 밀려온다면? Plane Sweeping은 점을 x좌표 순으로 삼키며 껍질을 키운다. 모든 껍질 점을 훑어 접선을 찾는 O(N²)에서 출발해, 껍질을 균형 이진 트리에 담아 접선을 이진 탐색으로 찾는 O(N log N)까지 내려간다. 나아가 완성된 껍질에 점이 추가될 때마다 고쳐 나가는 동적 볼록 껍질을 다룬다.`
- message: description이 질문, plane sweeping, O(N²), O(N log N), dynamic case를 한 번에 담아 길고 밀도가 높다. 검색 결과나 카드 UI에서 핵심이 흐려질 수 있다.
- recommendation: 핵심 주제를 1~2문장으로 줄이고, 세부 복잡도 전개는 본문에 맡긴다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-3.md:63

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-3.md:63
- quote: `새 점 $p$가 지금까지의 모든 점보다 위에 있으면 위쪽 접선이 따로 없이 $p$ 자신이 새로운 최상단이 되어 upper hull 한쪽을 통째로 새로 쓰고`
- message: 외부점에서 볼록다각형으로의 두 접선은 여전히 존재한다. `위쪽 접선이 따로 없다`는 표현은 특수한 갱신 범위가 커지는 상황을 접선 자체가 사라지는 것처럼 읽히게 한다.
- recommendation: `접선은 존재하지만, p가 새 극점이 되면서 upper hull의 큰 구간이 교체될 수 있다`처럼 표현을 완화한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-3.md:98

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-3.md:98
- quote: `$X$의 x좌표 위에 놓인 변을 upper hull에서 이진 탐색으로 찾아 $X$가 그 변보다 아래인지 CCW로 보고, lower hull에서도 같은 것을 본다.`
- message: upper/lower segment로 내부 판정하는 설명은 X.x가 현재 hull의 최좌/최우 x범위 안에 있을 때 자연스럽다. X.x가 범위 밖이면 해당 x좌표 위의 변이 없고 즉시 외부점이다.
- recommendation: 내부 판정 전에 `X.x가 [L.x, R.x] 밖이면 외부`라는 범위 조건을 추가한다.
- gate_effect: warn

### 🟢 [L3] src/content/posts/convex-hull-3.md:1

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-3.md:1
- quote: `not-recorded`
- message: 검토 완료, 이슈 없음. `upper/lower hull`, `Plane Sweeping`, `Dynamic Case`, `BST`, `접선`, `껍질` 용어가 본문 전반에서 대체로 일관되게 쓰인다.
- recommendation: 현재 용어 체계를 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/convex-hull-3.md:32

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/convex-hull-3.md:32
- quote: `![껍질을 반으로 나누기 — 최좌측 L과 최우측 R이 껍질을 upper hull(위)과 lower hull(아래) 두 사슬로 가른다.](/images/convex-hull-3/upper-lower.svg)`
- message: 검토 완료, 이슈 없음. 참조된 5개 SVG는 본문에서 설명하는 upper/lower 분할, sweep 접선, 갱신 결과, BST 아이디어, dynamic case의 역할과 대응된다. 단, BST 그림의 `y좌표 순` 정확성 문제는 L7 finding에서 별도로 지적했다.
- recommendation: L7 수정 시 `public/images/convex-hull-3/bst-idea.svg`의 레이블도 본문과 함께 고친다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-3.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-3.md:2
- quote: `title: "볼록 껍질 ③ — Plane Sweeping과 동적 갱신"`
- message: 검토 완료, 이슈 없음. 제목은 실제 본문 주제인 plane sweeping과 dynamic update를 대표한다. description은 길다는 L2 권고가 있지만, 다루는 범위 자체는 본문과 일치한다.
- recommendation: 제목은 유지하고, description은 L2 권고에 따라 압축을 검토한다.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: `not-recorded`
- message: 노션 원본 대조는 수행하지 못했다. 현재 세션에서 사용 가능한 MCP 리소스 목록에 notion-search/notion-fetch 도구가 없어 원본 페이지를 가져올 수 없었다.
- recommendation: 노션 원본 접근 도구가 연결된 환경에서 원문 대비 자의적 추가·핵심 누락 여부를 별도 확인한다.
- gate_effect: info

요약: 🔴 1 · 🟡 4 · 🟢 4

## 반영 결과 (2026-07-09, 2차)

- [🔴 L7] BST 키를 정정. upper/lower hull은 **x에 단조**이므로 "y좌표 순으로 담는다"는 프레이밍 오류였다. 본문을 "각 사슬(upper/lower)을 x좌표 순으로 담는다"로 고치고, "한 x에 점이 하나뿐이라 x-키 트리가 잘 정의된다"는 근거를 추가. 이진 탐색 방향 서술도 "위/아래" → "사슬 앞쪽/뒤쪽(작은/큰 x)"으로 수정. `bst-idea.svg`는 닫힌 다각형 대신 단조 사슬 하나(x순 1→5)를 보여주고 트리도 x순 in-order로 재구성. 이미지 alt·핵심 정리 요약도 함께 수정.
- [🟡 L1] "삼키며" 비유를 description·도입부·요약에서 제거하고 "x좌표 순으로 하나씩 더하며"로 평이화.
- [🟡 L2] description를 질문+4주제 나열에서 2문장으로 압축.
- [🟡 L7:63] "위쪽 접선이 따로 없이" → "접선 두 개는 언제나 존재하지만 갱신 범위가 커질 수 있다"로 완화(외부 점 접선 존재성 정확화).
- [🟡 L7:98] 내부 판정 전 "X.x가 [L_x, R_x] 밖이면 외부" 범위 조건 추가.
- [🟢 L6] 노션 원본 대조는 이번 리뷰 세션에서 도구 미연결로 미수행. 단, 직전 1차 리뷰에서 대화 내 fetch본으로 대조 완료(자의적 추가·핵심 누락 없음)했고, 이번 x-키 정정은 오히려 노션 원본(right hull+y)을 upper/lower로 재프레이밍하며 생긴 불일치를 바로잡은 것.
- 반영 후 결정적 검사 "발견 사항 없음 ✅", `npm run build` 통과 (104 pages).
