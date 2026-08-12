schema_version: review-report/v2
target: all-pairs-shortest-path
generated_at: 2026-08-12
strict: true
sources: src/content/posts/all-pairs-shortest-path.md
summary: 🔴 0 · 🟡 0 · 🟢 8

## Findings

### 🟢 [L1] src/content/posts/all-pairs-shortest-path.md:1

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/all-pairs-shortest-path.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/all-pairs-shortest-path.md:1

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/all-pairs-shortest-path.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/all-pairs-shortest-path.md:1

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/all-pairs-shortest-path.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] src/content/posts/all-pairs-shortest-path.md:35

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/all-pairs-shortest-path.md:35
- quote: problem.svg, k-meaning.svg, simulation.svg, recurrence.svg
- message: 검토 완료, 이슈 없음. problem.svg의 5개 간선과 가중치 및 빈 4×4 행렬, k-meaning.svg의 k=0·1·2 허용 노드 강조, simulation.svg의 세 행렬과 갱신 셀, recurrence.svg의 두 경우와 min 합류를 본문과 대조했다. XML의 레이블·선·경로·강조와 브라우저 렌더링 bounding box를 모두 확인했으며 잘림이나 수치 불일치가 없다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/all-pairs-shortest-path.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/all-pairs-shortest-path.md:2
- quote: 모든 쌍 최단 거리 — 다익스트라 N번과 플로이드·워셜
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] src/content/posts/all-pairs-shortest-path.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/all-pairs-shortest-path.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 직접 Notion 비교는 이용할 수 없었다. provenance 인계 문서 `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md`는 원문 자체가 아니라 범위 확인용으로만 사용했으며, 그 문서가 기록한 핵심 흐름, 승인된 4노드 예시와 SVG, 비음수 전제 및 유일성 약화 범위가 현재 글과 일치한다.
- recommendation: Notion 원문 접근이 가능해지면 핵심 구조, 증명 흐름, 누락 및 자의적 추가 여부를 직접 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/all-pairs-shortest-path.md:43

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/all-pairs-shortest-path.md:43
- quote: 다익스트라 한 번은 $O((M+N)\log N)$이다. 이를 $N$번 반복하니 전체는 $O(N(M+N)\log N)$이다.
- message: 검토 완료, 이슈 없음. 비음수 가중치 아래 사이클 제거 정리와 유한 단순 경로 모임에서의 최솟값 달성, k 통과 여부의 빠짐없고 겹치지 않는 분류, 양방향 후보 부등식, 동점 예시를 독립 확인했다. 간선 목록으로 D^0·D^1·D^2와 최종 행렬을 재계산했고 k=3·4의 무변화도 확인했다. 다익스트라 N회 시간 복잡도와 3차원 플로이드·워셜의 시간·공간 O(N^3)도 맞다. INF 구현 전제는 별도 L7 finding으로 기록했다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/all-pairs-shortest-path.md:189

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/all-pairs-shortest-path.md:189
- quote: `INF`에 거는 조건은 하나다. 실제로 존재하는 어떤 길의 길이보다도 커야 한다.
- message: 반영 후 재판정. 원래 문장은 `INF`를 "둘을 더해도 자료형을 넘지 않을 만큼 큰 값"으로 잡으라고 해 방향이 뒤집혀 있었고, 상충하는 두 조건 중 오버플로 쪽만 적어 sentinel 하한 조건을 빠뜨렸다. 의사코드에 한쪽이라도 `INF`면 덧셈을 건너뛰는 검사를 넣어 `INF`가 덧셈에 들어가는 경로 자체를 없앴고, 남는 조건은 "유한한 길의 길이보다 크다" 하나다. 본문이 그 하나만 말하므로 서술과 코드가 맞는다. 점화식과 증명은 그대로이며 검사는 반복당 상수 시간이라 $O(N^3)$ 판정도 그대로다.
- recommendation: 조치 없음. 후속 글이 같은 점화식을 다시 쓸 때는 검사를 생략했다는 사실을 밝혀 안전하지 않은 코드로 읽히지 않게 한다.
- gate_effect: info

## 반영 결과 (2026-08-12, 2차)

- 🔴 [L7] `all-pairs-shortest-path.md:189` `INF` 조건 서술이 뒤집혀 있고 조건 하나가 빠짐 — **반영 완료**. 의사코드 안쪽 문장을 `int viaK = INF;` + `D[k-1][i][k] != INF && D[k-1][k][j] != INF`일 때만 더하는 형태로 바꿔 `INF`가 덧셈에 들어가지 않게 했다. 이로써 `INF ≤ INT_MAX/2`(덧셈 안전)와 `INF > (N-1)·maxWeight`(없는 간선이 실제 길을 이기지 않음)라는 상충하는 두 조건 중 앞이 사라지고 뒤 하나만 남는다. 본문 :189를 그 하나만 말하도록 다시 썼다. 점화식·정리·증명은 손대지 않았다.
- 복잡도 서술 :212에 검사가 상수 시간이라는 한 절을 더하고, "세 개의 `for`와 `min` 하나가 전부다"를 코드에 보이는 형태에 맞춰 "세 개의 `for`와 비교 몇 줄"로 고쳤다. $O(N^3)$ 판정은 그대로다.
- 후속 글 정합성: `floyd-warshall-memory.md`의 두 의사코드는 검사를 생략하고, 생략 사실과 규칙이 그대로 필요하다는 점을 :32에서 한 번 밝힌다. 그 글의 주제가 메모리 축소라 층 인덱스 외의 군더더기를 코드에 넣지 않기로 했다.
- 재검증: `python .claude/review_post.py src/content/posts/all-pairs-shortest-path.md` 발견 사항 없음, `python .claude/review_post.py --gate` exit 0, `npm run build` 성공.
