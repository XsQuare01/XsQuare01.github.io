schema_version: review-report/v2
target: maximum-subarray-why-extend
generated_at: 2026-08-06
strict: true
sources: src/content/posts/maximum-subarray-why-extend.md
summary: 🔴 0 · 🟡 4 · 🟢 4

## Findings

### 🟡 [L1] src/content/posts/maximum-subarray-why-extend.md:150

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray-why-extend.md:150
- quote: 서로 다른 두 관점에서 출발해 같은 자리에 도착하는 일은 흔하다. 도착점이 같다는 사실을 확인하고 나면, 둘 중 편한 쪽을 골라 쓰면 된다.
- message: 마무리가 글의 결론이 아니라 일반론으로 넘어간다. "~하는 일은 흔하다"는 이 글이 증명한 내용을 넘어서는 진술이고, 뒤 문장은 앞 문장을 다시 풀어 쓴 동어 반복에 가깝다. L1 이 지적하는 경구식 섹션 마무리에 해당한다.
- recommendation: 일반론 한 문장을 덜어내고, 두 관점이 같은 식으로 모인다는 이 글의 결과만 남긴다.
- gate_effect: warn

### 🟡 [L3] src/content/posts/maximum-subarray-why-extend.md:46

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray-why-extend.md:46
- quote: 마지막 원소 $x$ 를 떼어내면 $a_s, \dots, a_i$ 가 남는다. $s \le i$ 면 이것은 $S_i$ 의 원소다.
- message: "원소"가 한 문단 안에서 두 뜻으로 쓰인다. 앞의 "마지막 원소 $x$"는 배열의 원소이고, 뒤의 "$S_i$ 의 원소"는 집합의 원소, 즉 부분배열 하나다. 증명의 핵심이 두 집합 사이의 대응이라 이 자리에서 말이 겹치면 무엇과 무엇을 짝짓는지가 흐려진다.
- recommendation: 집합 쪽을 "후보"로 바꿔 "$S_i$ 의 후보다", "$S_i$ 의 후보 뒤에 $x$ 를 붙이면"처럼 쓴다. 도판이 이미 "후보"라는 말을 쓰고 있어 용어도 함께 맞는다.
- gate_effect: warn

### 🟡 [L3] src/content/posts/maximum-subarray-why-extend.md:48

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray-why-extend.md:48
- quote: 곧 $S_i$ 에서 합이 $s$ 인 원소에 대응하는 $T_{i+1}$ 의 원소는 합이 $s + x$ 다.
- message: 기호 $s$ 가 한 증명 안에서 두 뜻으로 쓰인다. 바로 앞 문단(46번 줄)에서 $s$ 는 부분배열의 시작 인덱스 $a_s, \dots, a_{i+1}$ 를 가리키는데, 여기서는 부분배열의 합을 가리킨다. 인덱스와 합은 값의 성질이 달라, 같은 글자를 쓰면 "$s$ 가 최대일 때"가 시작 인덱스의 최대인지 합의 최대인지 읽는 사람이 되짚어야 한다.
- recommendation: 합에는 다른 글자를 쓴다. 시작 인덱스로 이미 $s$ 를 썼으므로 합은 $t$ 처럼 겹치지 않는 기호로 둔다.
- gate_effect: warn

### 🟡 [L4] src/content/posts/maximum-subarray-why-extend.md:80

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray-why-extend.md:80
- quote: ![누적합 P₀부터 P₈까지의 꺾은선과 지금까지의 최소를 나타내는 계단선. P₂ = −2에서 P₈ = 7까지의 낙차 9가 답이다.](/images/maximum-subarray-why-extend/prefix-min.svg)
- message: 도판의 범례와 각주가 기호 $m_j$ 를 쓰는데, 본문에서 $m_j$ 는 다음 절 「두 풀이는 같다」에서야 정의된다. 이 절의 본문은 같은 값을 $\min_{0 \le i \le j} P_i$ 로만 적는다. 도판을 먼저 보는 독자는 정의되지 않은 기호를 만난다. 수치 자체는 본문과 일치한다.
- recommendation: 도판 캡션이나 앞 문단에서 "$m_j = \min_{0 \le i \le j} P_i$" 를 한 번 밝히거나, 도판의 범례를 $\min$ 표기로 바꾼다.
- gate_effect: warn

### 🟢 [L2] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 의심 제기, 대응 논증, 수치 확인, 다른 관점, 두 관점의 합류 순으로 이어지고 도약이 없다. 코드의 갱신 순서를 걱정할 수 있다는 지점을 본문이 먼저 짚고 답한다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목은 첫 절만 가리키지만 description 이 누적합 관점과 두 풀이의 동일성까지 밝혀, 둘을 합쳐 보면 글의 범위가 정확히 드러난다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 노션 원문 「Maximum Subarray」와 대조했다. 원문이 "이 부분에 대한 추가 설명이 있어야 이해하기 쉬워보임", "사실 이게 답이 되는지는 모르겠다", "총 3번을 탐색"이라고 남긴 세 지점을 각각 인용하고 답한다. 원문 표현을 바꾸지 않고 인용한 뒤 확장임을 밝혀 두었다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 대응 논증의 전사와 역이 서로의 역임을 확인했고, 논증의 결론과 수치는 옳다. 기호 $s$ 의 중복 사용은 별도 L3 finding 으로 따로 적었다. $S_5$ 의 여섯 후보 합 $0, -2, 2, 4, -1, 2$ 와 $+3$ 을 더한 $3, 1, 5, 7, 2, 5$ 를 직접 계산해 $k_5 = 4$, $k_6 = 7$ 과 맞췄다. 귀납 증명의 base($j = 0$)와 step 이 닫히고 $-\min(u, v) = \max(-u, -v)$ 변형도 옳다. $P_j - m_j$ 수열 $0, 3, 0, 2, 6, 4, 7, 1, 9$ 가 $k_0 \dots k_8$ 과 일치한다. `maxSubarrayPrefix` 를 예시 배열로 손으로 돌려 9를 얻었고, `m` 갱신 전에 `p - m` 을 읽는 순서가 안전하다는 본문의 근거도 성립한다.
- recommendation: 조치 불필요.
- gate_effect: info

## 후속 처리

- 🟡 [L3] :46 "원소"가 배열의 원소와 집합의 원소 두 뜻으로 쓰임 → 집합 쪽을 모두 "후보"로 바꿔 도판 용어와 맞췄다.
- 🟡 [L3] :48 기호 $s$ 가 시작 인덱스와 합 두 뜻으로 쓰임 → 합을 $t$ 로 바꿨다.
- 🟡 [L4] :80 도판 범례의 $m_j$ 가 본문 정의보다 먼저 등장 → 「누적합으로 다시 보기」 안에서 $m_j = \min_{0 \le i \le j} P_i$ 를 먼저 정의하고, 「두 풀이는 같다」의 증명은 그 정의를 다시 세우지 않고 이어받도록 고쳤다.
- 🟡 [L1] :150 마치며의 일반론 경구 → "자리마다 최선을 들고 가든 누적합의 낙차를 재든 매 자리에서 같은 값이 나온다"는 이 글의 결과 문장으로 교체했다.
- 🟢 4건(L2·L5·L6·L7)은 조치 없음.
- 재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py` 두 편 모두 `발견 사항 없음 ✅`. 증명 구조와 수치는 바꾸지 않았다.
