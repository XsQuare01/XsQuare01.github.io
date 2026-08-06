schema_version: review-report/v2
target: maximum-subarray-why-extend
generated_at: 2026-08-06
strict: true
sources: src/content/posts/maximum-subarray-why-extend.md
summary: 🔴 0 · 🟡 0 · 🟢 7

## Findings

### 🟢 [L1] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 문두 접속어가 거의 없고 어체가 통일된다. 줄표는 제목과 링크 표기에만 쓰인다. 1차 검토에서 지적한 마치며의 일반론 경구는 이 글의 결과를 말하는 문장으로 바뀌었다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L2] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 의심 제기, 대응 논증, 수치 확인, 다른 관점, 두 관점의 합류 순으로 이어지고 도약이 없다. 코드의 갱신 순서를 걱정할 수 있다는 지점을 본문이 먼저 짚고 답한다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L3] src/content/posts/maximum-subarray-why-extend.md:46

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray-why-extend.md:46
- quote: $s \le i$ 면 이것은 $S_i$ 의 후보다.
- message: 검토 완료, 이슈 없음. 1차 검토에서 지적한 두 가지가 반영되었다. 집합의 원소를 "후보"로 부르게 되어 배열의 원소와 겹치지 않고 도판 용어와도 맞는다. 시작 인덱스 $s$ 와 합을 나타내던 같은 글자도 분리되어, 합은 $t$ 로 쓴다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L4] src/content/posts/maximum-subarray-why-extend.md:80

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray-why-extend.md:80
- quote: 이 최솟값을 앞으로 $m_j = \min_{0 \le i \le j} P_i$ 로 줄여 쓴다.
- message: 검토 완료, 이슈 없음. extend.svg 의 여섯 쌍과 합($0, -2, 2, 4, -1, 2$ 와 $3, 1, 5, 7, 2, 5$), 강조한 최댓값 4·7 이 본문과 일치한다. prefix-min.svg 의 $P$ 꼭짓점과 계단선, 낙차 9 도 맞다. 1차 검토가 지적한 기호 순서 문제도 해소되어, 도판 범례의 $m_j$ 가 도판 앞 문단에서 먼저 정의된다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목은 첫 절을 가리키지만 description 이 누적합 관점과 두 풀이의 동일성까지 밝혀, 둘을 합쳐 보면 글의 범위가 정확히 드러난다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 노션 원문 「Maximum Subarray」와 대조했다. 원문이 "이 부분에 대한 추가 설명이 있어야 이해하기 쉬워보임", "사실 이게 답이 되는지는 모르겠다", "총 3번을 탐색"이라고 남긴 세 지점을 각각 인용하고 답한다. 원문 표현을 바꾸지 않고 인용한 뒤 노트 밖 확장임을 도입에서 밝힌다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 대응 논증의 전사와 역이 서로의 역임을 확인했고, $S_5$ 의 여섯 후보 합 $0, -2, 2, 4, -1, 2$ 와 $+3$ 을 더한 $3, 1, 5, 7, 2, 5$ 를 직접 계산해 $k_5 = 4$, $k_6 = 7$ 과 맞췄다. 귀납 증명의 base($j = 0$)와 step 이 닫히고 $-\min(u, v) = \max(-u, -v)$ 변형도 옳다. $P_j - m_j$ 수열 $0, 3, 0, 2, 6, 4, 7, 1, 9$ 가 $k_0 \dots k_8$ 과 일치한다. `maxSubarrayPrefix` 를 예시 배열로 손으로 돌려 9 를 얻었고, `m` 갱신 전에 `p - m` 을 읽는 순서가 안전하다는 본문의 근거도 성립한다. $i \le j$ 와 $i < j$ 가 빈 배열 허용 여부에 대응한다는 설명도 맞다.
- recommendation: 조치 불필요.
- gate_effect: info

## 후속 처리

1차 검토(같은 날, 반영 전)에서 🟡 4 가 나왔고 모두 반영한 뒤 이 리포트로 다시 판정했다. 1차 지적과 처리는 아래와 같다.

- 🟡 [L3] :46 "원소"가 배열의 원소와 집합의 원소 두 뜻으로 쓰임 → 집합 쪽을 모두 "후보"로 바꿔 도판 용어와 맞췄다.
- 🟡 [L3] :48 기호 $s$ 가 시작 인덱스와 합 두 뜻으로 쓰임 → 합을 $t$ 로 바꿨다.
- 🟡 [L4] :80 도판 범례의 $m_j$ 가 본문 정의보다 먼저 등장 → 「누적합으로 다시 보기」 안에서 $m_j$ 를 먼저 정의하고, 「두 풀이는 같다」의 증명은 그 정의를 다시 세우지 않고 이어받도록 고쳤다.
- 🟡 [L1] :150 마치며의 일반론 경구 → 두 풀이가 매 자리에서 같은 값을 낸다는 결과 문장으로 교체했다.

재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py` 두 편 모두 `발견 사항 없음 ✅`. 증명 구조와 수치, 도판 2장은 변경하지 않았다.
