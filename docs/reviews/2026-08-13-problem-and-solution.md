schema_version: review-report/v2
target: problem-and-solution
generated_at: 2026-08-13
strict: true
sources: src/content/posts/problem-and-solution.md
summary: 🔴 0 · 🟡 0 · 🟢 11

## Findings

### 🟢 [L1] src/content/posts/problem-and-solution.md:120

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/problem-and-solution.md:120
- quote: 답이 yes인 입력들을 모아놓은 집합이 곧 Problem이다.
- message: 정의를 짧은 평서문으로 제시하며 과한 수사나 반복적인 문두 접속어 없이 읽힌다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/problem-and-solution.md:126

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/problem-and-solution.md:126
- quote: Language에 속하는 문자열은 답이 yes인 입력이다. 예시를 통해 이해해보자.
- message: 판정 문제에서 언어로, 문자열과 문제의 기수로, 튜링 머신의 수로 이어지는 큰 설명 순서는 명확하다. 기술적 전제가 빠진 환원 설명은 L7에 별도로 기록했다.
- recommendation: 현재 정의와 기수 비교의 전개 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/problem-and-solution.md:218

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/problem-and-solution.md:218
- quote: 이것이 Church's Thesis의 핵심 주장이다.
- message: 반영. 'Church's Thesis'와 'Church-Turing Thesis'를 'Church-Turing 논제'로 통일하고 Thesis의 역어를 '명제'에서 '논제'로 바꿨다. 뒷절의 '어떤 컴퓨터로도 풀 수 없다'도 논제를 전제로 한 진술임을 드러냈다.
- recommendation: 글 전체에서 "Church-Turing 논제"로 통일한다.
- gate_effect: info

### 🟢 [L4] public/images/problem-and-solution/problem-transform.svg:3

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/problem-and-solution/problem-transform.svg:3
- quote: Shortest Path — Decision Problem으로의 환원
- message: SVG를 독립 렌더링해 확인했다. Decision 문제에서 Binary Search를 거쳐 길이 문제로, Edge 제거를 거쳐 경로 문제로 향하는 두 화살표와 각 입력·출력 레이블이 본문 48~67행의 설명과 일치하며, 레이블 잘림도 없다.
- recommendation: 현재 도식의 대응 관계를 유지하되 환원의 성립 조건은 본문에서 L7 권고대로 보완한다.
- gate_effect: info

### 🟢 [L4] public/images/problem-and-solution/problem-vs-solution.svg:4

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/problem-and-solution/problem-vs-solution.svg:4
- quote: Problems vs Solutions — 크기 비교
- message: SVG를 독립 렌더링해 확인했다. Problems의 $|2^{\Sigma^*}|=|\mathbb{R}|=\mathfrak c$와 Solutions의 $|\mathbb{N}|=\aleph_0$ 레이블은 본문 224~239행의 기수 비교와 일치하며, 모든 텍스트가 viewBox 안에 표시된다.
- recommendation: 현재 도식을 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/problem-and-solution.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/problem-and-solution.md:2
- quote: title: "Problem & Solution — Complexity Theory의 수학적 정의"
- message: 제목과 description이 판정 문제, 언어, 튜링 머신, 계산 불가능한 문제의 기수 비교라는 실제 범위를 대표한다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/problem-and-solution.md:10

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/problem-and-solution.md:10
- quote: 이 글에서는 그 수학적 정의를 따라가며, 풀 수 있는 문제보다 풀 수 없는 문제가 압도적으로 많다는 사실을 확인한다.
- message: problem-and-solution의 직접 원천 자료에는 접근할 수 없어 저장소의 현재 글을 기준으로 검토했다. Notion을 확인했다고 가정하지 않았으며, 원천 대비 누락이나 자의적 추가 여부는 판정할 수 없다.
- recommendation: 직접 원천 자료가 확보되면 정의, 환원 예시, Church-Turing 논제 부분을 우선 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/problem-and-solution.md:35

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/problem-and-solution.md:35
- quote: Complexity Theory에서는 모든 문제를 Decision Problem으로 다룬다. 이유는 두 가지다.
- message: 반영. '모든 문제를 Decision Problem으로 다룬다'와 'Decision Problem만으로 모든 문제를 해결할 수 있다'를 '주로 판정 문제를 연구하며, 자연스러운 탐색·최적화 문제 상당수가 대응하는 판정판과 다항 시간 관계를 갖는다'로 한정했다. 예시가 최단 경로의 자기 환원성(self-reducibility)임을 명시하고, 이 논증이 쓴 구조(임계값 단조성, 간선을 지워도 같은 꼴로 남음, 정수 인코딩)를 밝히면서 판정 문제 중심의 연구가 정리가 아니라 대상 선택 방식임을 '보인 것과 보이지 않은 것' 상자로 갈랐다. 간선 제거 절차가 실제로 최단 경로만 남기는 이유도 증명을 붙였다.
- recommendation: 주장을 "복잡도 이론에서는 주로 판정 문제를 연구하며, 많은 자연스러운 탐색·최적화 문제는 적절한 판정판과 다항 시간 관계를 갖는다"로 한정하고 이 예시가 최단 경로의 자기 환원임을 명시한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/problem-and-solution.md:61

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/problem-and-solution.md:61
- quote: Binary Search로 가능하다. $L$의 범위를 최솟값(edge 최소 길이)과 최댓값(모든 edge의 합)으로 잡고, 중간값에 대해 Decision 문제를 반복 호출하면 최단 거리 $L$을 구할 수 있다.
- message: 반영. 판정 문제를 '길이 L 이하인 경로가 존재하는가'로 정의하고, 이하라는 부등호가 단조성을 준다는 점을 밝혔다. 비음수 정수 가중치·S≠E·도달 가능이라는 전제를 상자로 선언하고 각 조건이 하는 일(상한 성립, 유한 종료, 답의 정의)을 적었다. 실수 가중치의 정밀도 문제와 음수 가중치의 범위 이탈도 언급했다. 하한을 0으로 잡고 상한을 가중치 합 W로 두어 호출 횟수가 O(log W)이며 이것이 입력 길이의 다항식임을 보였다. 도판의 판정 카드에도 질문을 적어 넣었다.
- recommendation: 비음수 정수 가중치와 도달 가능한 서로 다른 두 정점을 전제로 선언하고, 판정 문제를 "길이 $L$ 이하인 경로가 존재하는가"로 정의한다. 더 일반적인 가중치를 다룬다면 정밀도와 탐색 구간을 별도로 설명한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/problem-and-solution.md:152

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/problem-and-solution.md:152
- quote: 길이에 따라 자연수 번호를 붙일 수 있으므로, $|\Sigma^*| = |\mathbb{N}|$ — 가산 무한이다.
- message: 유한하고 비어 있지 않은 알파벳에서 유한 문자열 집합은 가산 무한이고, 그 멱집합은 연속체 기수이며, 유한하게 기술되는 튜링 머신의 집합은 가산이라는 기수 비교는 맞다. 따라서 결정 가능한 언어는 전체 언어보다 기수상 작다는 중심 결론도 성립한다.
- recommendation: 기수 비교와 중심 결론은 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/problem-and-solution.md:242

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/problem-and-solution.md:242
- quote: 이 단순한 Rule 하나만으로도 모든 계산이 가능하며, 이것이 Church's Thesis의 핵심 주장이다.
- message: 반영. '이 단순한 Rule 하나만으로도 모든 계산이 가능하며'를 지우고, 규칙 하나는 한 걸음만 하며 계산을 수행하는 것은 규칙들의 유한 집합임을 적었다. 전이 규칙 형식도 오른쪽 이동 고정에서 D ∈ {L, R}로 고쳤다. Church-Turing 논제는 '효과적으로 계산 가능한 함수 = 튜링 머신으로 계산 가능한 함수'로 따로 정의하고, 논제인 이유(한쪽이 직관적 개념이라 증명 대상이 못 됨)와 여러 계산 모델의 일치라는 근거를 적었다. 물리적 기계에 대한 주장과 혼동되지 않도록 경계도 달았다.
- recommendation: 212~216행은 전이 규칙 한 개의 형식 예시라고 설명하고, 계산은 이런 규칙의 유한 집합으로 수행한다고 고친다. Church-Turing 논제의 내용은 효과적 계산 가능성과 튜링 계산 가능성의 일치로 따로 정의한다.
- gate_effect: info
