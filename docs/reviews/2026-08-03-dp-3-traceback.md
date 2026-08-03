schema_version: review-report/v2
target: dp-3-traceback
generated_at: 2026-08-03
strict: true
sources: src/content/posts/dp-3-traceback.md
summary: 🔴 0 · 🟡 0 · 🟢 7

## Findings

### 🟢 [L1] src/content/posts/dp-3-traceback.md:1-118

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/dp-3-traceback.md:1-118
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/dp-3-traceback.md:1-118

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/dp-3-traceback.md:1-118
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/dp-3-traceback.md:1-118

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/dp-3-traceback.md:1-118
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] public/images/dp-3/traceback.svg:1-60

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/dp-3/traceback.svg:1-60
- quote: "split[1][3] = 1 / split[2][3] = 2"
- message: 참조 SVG 하나를 본문과 대조했다. `traceback.svg`의 분할점 표 값이 본문 56행의 $split[1][3] = 1$, $split[2][3] = 2$와 같고, 파스 트리도 루트 `[1,3] k=1`에서 잎 `M₁`과 내부 노드 `[2,3] k=2`로 갈린 뒤 `M₂`·`M₃`로 내려가는 모양이라 본문 60-63행의 재귀 전개와 정확히 대응한다. 범례의 "내부 노드 = 마지막 곱"도 29행의 "그 $k$가 곧 $[i,j]$를 감싸는 가장 바깥 괄호의 자리"라는 설명과 맞는다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/dp-3-traceback.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/dp-3-traceback.md:2-4
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] docs/superpowers/specs/2026-07-31-dp-3-traceback-design.md:5

- severity: 🟢
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-07-31-dp-3-traceback-design.md:5
- quote: "소스: 노션 밖 확장(강의 노트에 없음). 기반은 [dp-3](/blog/dp-3)(구간 DP / 행렬 곱셈 순서)."
- message: 노션 강의 노트에 분할점 기록과 괄호화 복원은 없다. 이 글은 dp-3의 "더 나가면"이 예고한 확장이고, 스펙 5행이 노션 밖 확장임을 명시하며 형제 선례로 `dp-2-traceback`을 지정해 구조와 목소리를 잇도록 했다. 본문 11행도 "이 글은 강의 노트 밖 확장으로"라고 스스로 범위를 밝혀 독자가 원문 밖임을 알 수 있다. 원문에 없는 내용을 원문의 것처럼 제시한 곳이 없고, dp-3 본편에서 가져온 값($d = [3,2,4,2]$, 최소 비용 28, $split$ 값)도 본편과 어긋나지 않는다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/dp-3-traceback.md:56-108

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/dp-3-traceback.md:56-108
- quote: not-recorded
- message: 값과 논증을 모두 검산했다. $d = [3,2,4,2]$에서 $M_1$은 $3 \times 2$, $M_2$는 $2 \times 4$, $M_3$은 $4 \times 2$다. $(M_1(M_2M_3))$의 비용은 $2 \cdot 4 \cdot 2 = 16$에 $3 \cdot 2 \cdot 2 = 12$를 더한 28이고, $((M_1M_2)M_3)$은 $3 \cdot 2 \cdot 4 = 24$에 $3 \cdot 4 \cdot 2 = 24$를 더한 48이다. 따라서 최소는 28, $split[1][3] = 1$이 맞고 본문 65행의 결론과 일치한다. 조각 A의 `<` 비교가 동점에서 가장 작은 $k$를 남긴다는 설명도 $k$가 오름차순으로 도는 루프와 맞고, 106행이 `<=`로 바꾸면 다른 괄호화가 남는다는 점, 그리고 "유일한 정답이 있어서 특정 $k$가 남는 게 아니다"라는 단서까지 정확하다. 앞선 리포트(2026-07-31)가 지적한 "복원은 `split` 표를 요구한다"는 과한 주장은 이미 한정돼 있다. 108행은 `split`이 분할점을 $O(1)$에 주지만 필수 조건은 아니라고 밝히고, `m`과 `d`만으로 $m[i][k] + m[k+1][j] + d_{i-1}d_k d_j = m[i][j]$인 $k$를 구간마다 $O(n)$에 다시 찾을 수 있다고 대안을 제시한 뒤, $O(n^2)$ 저장이 하한이 아니라 시간·공간 절충이라고 정정했다. 재탐색 비용도 실제로 구간 $[i,j]$에서 $k$를 $i$부터 $j-1$까지 훑어 $O(j-i)$이므로 맞다. 파스 트리가 잎 $n$개·내부 노드 $n-1$개의 완전 이진 트리라는 서술도 옳다.
- recommendation: not-recorded
- gate_effect: info
