schema_version: review-report/v2
target: all-pairs-shortest-path
generated_at: 2026-08-13
strict: true
sources: src/content/posts/all-pairs-shortest-path.md
summary: 🔴 0 · 🟡 0 · 🟢 7

## Findings

### 🟢 [L1] src/content/posts/all-pairs-shortest-path.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/all-pairs-shortest-path.md:11
- quote: 이번엔 시작점을 고르지 않는다. 모든 쌍이다. 답이 하나가 아니라 $N^2$개다.
- message: 검토 완료, 이슈 없음
- recommendation: 현재의 ~다 평서체와 절제된 강조를 유지한다. 문두 접속어, 줄표식 수사, 중복 표현도 문맥상 문제될 정도로 반복되지 않는다.
- gate_effect: info

### 🟢 [L2] src/content/posts/all-pairs-shortest-path.md:75

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/all-pairs-shortest-path.md:75
- quote: 지나갈 수 있는 노드를 제한한다
- message: 검토 완료, 이슈 없음
- recommendation: 문제 정의, 다익스트라 기준선, 경유 노드 제한, 손계산, 점화식 증명, 의사코드 순서가 전제를 단계적으로 쌓으므로 현재 흐름을 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/all-pairs-shortest-path.md:81

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/all-pairs-shortest-path.md:81
- quote: $D^k[i][j]$를 "$i$에서 $j$로 가되 **중간에 거치는 노드**가 모두 $\{1,\dots,k\}$ 안에 있는 길 중 최단 거리"로 정의한다.
- message: 검토 완료, 이슈 없음
- recommendation: 노드, 간선, 길, 최단 거리, 중간 노드와 $D^k[i][j]$ 표기가 글 전체에서 같은 뜻으로 유지되므로 현재 용어를 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/all-pairs-shortest-path.md:37

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/all-pairs-shortest-path.md:37
- quote: `problem.svg`, `k-meaning.svg`, `simulation.svg`, `recurrence.svg`
- message: 검토 완료, 이슈 없음
- recommendation: 네 SVG를 각각 렌더링해 확인했다. `problem.svg`의 간선 1, 5, 7, 1, 10과 4×4 빈 행렬, `k-meaning.svg`의 허용 집합, `simulation.svg`의 k=0,1,2 행렬과 갱신값, `recurrence.svg`의 두 항과 min 연결이 본문과 일치하며 레이블, 값, 연결선, 강조, 캡션에 잘림이 없다.
- gate_effect: info

### 🟢 [L5] src/content/posts/all-pairs-shortest-path.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/all-pairs-shortest-path.md:2
- quote: title: "모든 쌍 최단 거리 — 다익스트라 N번과 플로이드·워셜"
- message: 검토 완료, 이슈 없음
- recommendation: 제목은 기준선과 중심 알고리즘을 함께 드러내고 description은 경유 집합, 점화식, 양방향 증명까지 실제 본문 범위를 정확히 요약하므로 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/all-pairs-shortest-path.md:25

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/all-pairs-shortest-path.md:25
- quote: 무엇을 구하는가
- message: 검토 완료, 이슈 없음
- recommendation: 직접 Notion 비교는 현재 접근 수단이 없어 불가능하다. 매핑된 설계 스펙 `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md`와 대조하면 문제 정의, 기준선, 경유 제약, 시뮬레이션, 점화식 증명, 의사코드의 핵심 줄기와 승인된 예시 및 유일성 약화가 보존되어 있으므로 현 상태를 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/all-pairs-shortest-path.md:243

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/all-pairs-shortest-path.md:243
- quote: `INF`에 거는 조건은 하나다. 실제로 존재하는 어떤 길의 길이보다도 커야 한다.
- message: 반영 완료. 원래 문장은 `INF`가 존재하는 모든 길보다 커야 한다고 적어, 사이클을 반복하면 길이가 무한히 커지는 경우를 배제하지 못했다. 표에 담기는 값이 최단 거리뿐임을 짚고, 비음수 가중치에서 최단 거리가 간선을 많아야 N-1개 쓰므로 (N-1)W_max를 넘지 않는다는 하한 근거를 적었다. 덧셈 오버플로 조건도 함께 명시했다. 실제로 더해지는 두 값은 최단 거리이므로 합이 2(N-1)W_max 아래이고, `INF`와 이 합이 함께 자료형에 들어가면 된다. 점화식, 정리, 의사코드, 복잡도 판정은 손대지 않았다.
- recommendation: `INF`는 도달 가능한 최단 거리의 상한보다 크고 `D[k - 1][i][k] + D[k - 1][k][j]`가 자료형 범위 안에 남도록 정한다고 고친다. 예를 들어 가중치 상한이 `W_MAX`이고 비음수 그래프라면 단순 최단 경로가 최대 `N-1`개 간선을 쓰므로 `(N-1)W_MAX`보다 큰 값을 택하되 덧셈 오버플로도 함께 막는 조건을 명시한다.
- gate_effect: info

## 반영 결과 — #128 INF 조건 (2026-08-13)

- 🟡 `:243` `INF`의 sentinel 조건 — **반영 완료**. 「존재하는 어떤 길보다 크다」는 유한한 정수로 만족할 수 없는 조건이다. 사이클을 반복한 길의 길이에 상한이 없기 때문이다. 표에 담기는 값이 최단 거리뿐이라는 점을 짚고, 하한을 $(N-1)W_{\max}$로 좁혔다.
- 리뷰가 함께 지적한 덧셈 오버플로 조건을 같은 문단에 적었다. 실제로 더해지는 두 값이 모두 최단 거리이므로 합은 $2(N-1)W_{\max}$ 아래이며, `INF`와 이 합이 함께 자료형에 들어가면 된다.
- 판정을 바꾸는 수정은 없다. 점화식, 정리 1과 증명, 손계산 예시, 의사코드, $O(N^3)$ 판정은 그대로다.
- 재검증: `python .claude/review_post.py src/content/posts/all-pairs-shortest-path.md` 발견 사항 없음, `npm run build` 성공, 발행본 raw `$` 0개.
