schema_version: review-report/v2
target: scheduling-1
generated_at: 2026-08-13
strict: true
sources: src/content/posts/scheduling-1.md
summary: 🔴 0 · 🟡 0 · 🟢 11

## Findings

### 🟢 [D12] src/content/posts/scheduling-1.md:164

- severity: 🟢
- source: D
- rule_id: D12
- location: src/content/posts/scheduling-1.md:164
- quote: not-recorded
- message: 반영 완료. #178에서 '다음 포스트' 콜아웃을 마크다운 링크로 바꿔 /blog/scheduling-2를 실제로 걸었다. D12 규칙이 마크다운 링크 표기만 인식하므로 raw HTML의 a href로는 해소되지 않아 mst와 같은 콜아웃 패턴으로 통일했다. 현재 scheduling-1 재검사에서 발견 사항 없음.
- recommendation: 메시지에 따라 원문을 검토하고 필요한 경우 수정
- gate_effect: info

### 🟢 [L1] src/content/posts/scheduling-1.md:10

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/scheduling-1.md:10
- quote: 어떤 일을 골라 어떤 순서로 해야 이익의 합이 최대가 될까?
- message: 문제 제기에서 정의, 전략, 증명으로 곧바로 이어지며 과한 비유나 경구식 마무리 없이 평서체가 유지된다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/scheduling-1.md:71

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/scheduling-1.md:71
- quote: 증명의 핵심 도구는 **교환 논증(exchange argument)** 이다. "우리 알고리즘의 부분 답을, 어떤 최적해로 손해 없이 맞춰 갈 수 있다"는 것을 단계마다 보인다.
- message: 문제 정의와 예시 뒤에 greedy 규칙을 제시하고, 불변식, base, 겹치지 않는 step 경우로 최적성을 설명한 다음 복잡도로 넘어가는 흐름이 명확하다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/scheduling-1.md:2

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/scheduling-1.md:2
- quote: title: "데드라인 스케줄링 — 이익을 최대로 만드는 greedy 배치"
- message: 반영. greedy·Greedy·그리디가 섞여 있었다. 개념 글인 greedy.md가 제목부터 '그리디 알고리즘'이고 본문에서 '그리디'를 29회 쓰므로 그쪽으로 통일했다. 제목·description·머리말 콜아웃·절 제목·도판 alt·핵심 정리를 모두 '그리디'로 맞췄다. 태그 'Greedy'는 다른 글과 공유하는 라벨이라 두었다. 증명 절의 Invariant·Base·Step도 불변식·기초·귀납 단계로 옮겨 mst·prim과 표기를 맞췄다. 덧붙여 시리즈 다음 편 링크가 없어 D12가 남아 있었으므로 '다음 포스트' 콜아웃을 마크다운 링크로 바꿔 /blog/scheduling-2를 실제로 걸었다.
- recommendation: 고유한 영문 용어를 유지하려면 "greedy"로, 한국어 설명을 우선하려면 "그리디"로 한 가지 표기를 정해 제목, 소제목, 본문에서 통일한다.
- gate_effect: info

### 🟢 [L4] public/images/scheduling/timeline.svg:7

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/scheduling/timeline.svg:7
- quote: 할 일 {(2, 2), (1, 3), (1, 1)} — (이익 큰 순서로 배치)
- message: SVG를 독립 렌더링해 확인했다. 슬롯 1의 $(1,3)$, 슬롯 2의 $(2,2)$, 버린 $(1,1)$, 총 이익 5가 본문 37~42행과 61~63행에 일치한다. 시간축, 값, 상태 레이블은 모두 viewBox 안에 있고 잘림이 없다.
- recommendation: 현재 도식을 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/scheduling-1.md:4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/scheduling-1.md:4
- quote: description: "마감 기한과 이익이 있는 일들 중에서, 이익의 합을 최대로 만드는 일정을 짜는 문제를 다룬다. 이익이 큰 일부터 마감 기한에 가까운 자리에 넣는 greedy 전략을 세우고, 교환 논증으로 그 최적성을 증명한 뒤, 균형 트리로 O(N log N)까지 줄이는 방법을 살펴본다."
- message: 제목과 description이 문제 정의, greedy 선택, 교환 논증, $O(N\log N)$ 구현이라는 실제 본문 범위를 빠짐없이 대표한다.
- recommendation: 현재 제목과 description의 내용 범위를 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/scheduling-1.md:22

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/scheduling-1.md:22
- quote: ## 데드라인 스케줄링 문제
- message: 매핑된 스펙 `docs/superpowers/specs/2026-06-08-scheduling-1-post-design.md`는 문제, greedy 전략, 교환 논증, 성능이라는 provenance 인계 구조가 현재 글에 반영됐음을 보여 준다. 이 스펙은 직접 원문이 아니므로 내용 충실성의 독립 근거로 사용하지 않았고, Notion 원문 접근도 가정하지 않았다.
- recommendation: 직접 원천 자료가 확보되면 스펙의 인계 항목과 현재 본문을 원문에 다시 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/scheduling-1.md:42

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/scheduling-1.md:42
- quote: 가장 이익이 큰 $(1, 3)$ 을 시간 1에, $(2, 2)$ 를 시간 2에 넣으면 이익은 $3 + 2 = 5$.
- message: 세 작업의 모든 부분집합과 순서를 완전탐색해 최적 총이익 5와 배치 $(1,3),(2,2)$를 재현했다. 두 작업은 각각 슬롯 1과 2에서 마감을 지키고 $(1,1)$을 함께 넣을 수 없다.
- recommendation: 현재 예시 계산을 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/scheduling-1.md:45

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/scheduling-1.md:45
- quote: $S$ 의 $t$ 가 비어 있다면, $S$ 에 $J_{i+1}$ 을 추가하기만 해도 이익이 $P_{i+1} > 0$ 만큼 늘어난다.
- message: 반영. 문제 정의가 이익의 부호를 제한하지 않은 채 증명만 P > 0을 썼다. 정의에 P_i > 0을 전제로 명시하고, 그 전제가 무엇을 하는지 상자로 풀었다. P_i = 0이면 빈 슬롯에서의 모순 논법이 막히지만 '손해 없는 추가'로 바꾸면 결론이 유지되고, P_i < 0이면 '놓을 수 있으면 놓는다'는 선택 규칙 자체가 손해 보는 일을 배치하므로 P_i ≤ 0인 일을 제외하는 규칙이 필요하다는 점을 적었다. 증명 본문도 전제를 인용하는 형태로 고쳤다.
- recommendation: 모든 $P_i>0$을 문제 전제로 명시한다. 0 이익까지 허용하려면 빈 슬롯에는 $J_{i+1}$을 추가해도 최적성이 유지된다고 증명을 바꾸고, 음수 이익은 배치하지 않는 선택 규칙을 추가한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/scheduling-1.md:108

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/scheduling-1.md:108
- quote: 모든 경우에서, $J_{i+1}$ 까지 본 상태 $A_{i+1}$ 에 일치하는 최적해 $S$ 를 만들 수 있다.
- message: 이익이 양수라는 전제를 두면 base와 step이 닫힌다. 버리는 경우와 배치하는 경우가 전체를 덮고, 배치하는 경우는 $S$의 $J_{i+1}$ 포함 여부와 슬롯 상태로 겹치지 않게 나뉜다. 양의 이익 1~4, 작업 수 1~4의 67,332개 입력을 완전탐색해 greedy 이익이 최적 이익과 같음도 확인했다.
- recommendation: 교환 논증의 구조는 유지하고 L7 권고대로 이익 전제만 문제 정의에 연결한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/scheduling-1.md:138

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/scheduling-1.md:138
- quote: 일 $N$ 개 각각에 대해 $O(\log N)$ 작업을 하므로 전체 $O(N \log N)$. 정렬 비용 $O(N \log N)$ 과 합쳐도 차수는 그대로다.
- message: 배열로 각 마감부터 역방향 탐색하면 최악 $O(N^2)$이고, 사용 가능한 슬롯의 predecessor 질의와 삭제를 균형 이진 탐색 트리에서 각각 $O(\log N)$에 처리하면 정렬을 포함한 전체 시간이 $O(N\log N)$이라는 분석은 맞다.
- recommendation: 현재 복잡도 분석을 유지한다.
- gate_effect: info
