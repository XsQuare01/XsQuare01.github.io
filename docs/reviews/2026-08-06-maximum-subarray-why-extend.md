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
- message: 검토 완료, 이슈 없음. 문두 접속어가 거의 없고 어체가 통일된다. 줄표는 제목과 링크 표기에만 쓰인다. 마치며는 일반론이 아니라 이 글이 얻은 결과를 말한다.
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

### 🟢 [L3] src/content/posts/maximum-subarray-why-extend.md:23

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray-why-extend.md:23
- quote: 그리고 $k_i$ 는 $a_1 \dots a_i$ 의 뒷조각 중 최대 합이다. 빈 뒷조각을 후보에 넣는 정의를 계속 쓴다.
- message: 검토 완료, 이슈 없음. 기호 되짚기가 본편의 새 정의와 같은 말을 쓴다. 집합의 구성원은 "후보", 배열의 구성원은 "원소"로 갈라 쓰고, 시작 인덱스 $s$ 와 합 $t$ 도 겹치지 않는다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L4] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. extend.svg 의 여섯 쌍과 합($0, -2, 2, 4, -1, 2$ 와 $3, 1, 5, 7, 2, 5$), 강조한 최댓값 4·7 이 본문과 일치하고, 두 열 머리말도 본편의 뒷조각 정의에 맞춰 고쳐졌다. prefix-min.svg 의 $P$ 꼭짓점, 계단선, 낙차 9 도 맞다. 도판 범례의 $m_j$ 는 도판 앞 문단에서 먼저 정의된다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목은 첫 절을 가리키지만 description 이 누적합 관점과 두 풀이의 동일성까지 밝혀, 둘을 합쳐 보면 글의 범위가 드러난다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray-why-extend.md

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray-why-extend.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 이 세션에서는 `notion-search`·`notion-fetch` 로 원문 「Maximum Subarray」(2026-08-06 조회)를 직접 가져와 대조했다. 직전 판정이 도구 부재로 대조하지 못했다고 적은 부분을 여기서 닫는다. 원문이 "이 부분에 대한 추가 설명이 있어야 이해하기 쉬워보임", "사실 이게 답이 되는지는 모르겠다", "총 3번을 탐색"이라고 남긴 세 지점을 각각 인용하고 답하며, 원문 표현을 바꾸지 않고 인용한 뒤 노트 밖 확장임을 도입에서 밝힌다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray-why-extend.md:66

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray-why-extend.md:66
- quote: 비어 있지 않은 부분배열 하나는 $0 \le i < j \le N$ 인 쌍 $(i, j)$ 와 1:1로 대응한다.
- message: 검토 완료, 이슈 없음. 직전 판정이 지적한 두 가지가 해소되었다. 전단사는 이제 $i < j$ 인 쌍과 비어 있지 않은 부분배열 사이에서만 주장하고, $i = j$ 인 쌍은 값이 모두 0 이라 빈 배열 후보 하나를 더한 것과 같다고 따로 설명한다. 마지막 절도 두 코드가 같은 값을 얻을 뿐 상태와 갱신 순서는 다르다고 한정한다. 나머지 논증도 다시 확인했다. 대응 논증의 전사와 역이 서로의 역이고, $S_5$ 의 여섯 후보 합 $0, -2, 2, 4, -1, 2$ 에 $+3$ 을 더한 $3, 1, 5, 7, 2, 5$ 가 $k_5 = 4$, $k_6 = 7$ 과 맞는다. 귀납의 base 와 step 이 닫히고 $P_j - m_j$ 수열 $0, 3, 0, 2, 6, 4, 7, 1, 9$ 가 $k_0 \dots k_8$ 과 일치하며, `maxSubarrayPrefix` 를 손으로 돌려 9 를 얻었다.
- recommendation: 조치 불필요.
- gate_effect: info

## 후속 처리

### 1차 판정 (같은 날, 초안 대상)

- 🟡 [L3] :46 "원소"가 배열의 원소와 집합의 원소 두 뜻으로 쓰임 → 집합 쪽을 "후보"로 바꿨다.
- 🟡 [L3] :48 기호 $s$ 가 시작 인덱스와 합 두 뜻으로 쓰임 → 합을 $t$ 로 바꿨다.
- 🟡 [L4] :80 도판 범례의 $m_j$ 가 본문 정의보다 먼저 등장 → $m_j$ 를 도판 앞에서 정의했다.
- 🟡 [L1] :150 마치며의 일반론 경구 → 이 글의 결과 문장으로 교체했다.

### 2차 판정 (독립 리뷰, 이 리포트가 대체함)

2차 판정의 finding 은 아래에 원문대로 옮긴다.

- 🟡 [L7] :66 `부분배열 하나는 $0 \le i \le j \le N$ 인 쌍 $(i, j)$ 와 1:1로 대응한다. 두 경계를 고르는 것이 곧 부분배열을 고르는 것이고, $i = j$ 는 빈 배열이다.` — "서로 다른 $N+1$개의 $(i,i)$가 모두 같은 빈 배열을 나타내므로 전체 대응은 1:1이 아니다. 중복이 최댓값을 바꾸지 않아 뒤의 식과 알고리즘은 유효하지만, 제시한 전단사 근거는 그대로 성립하지 않는다."
- 🟡 [L7] :142 `본편의 카데인 코드와 나란히 놓으면 변수 이름만 다르다. 앞 절의 증명이 그 사실을 말해 준다.` — "두 코드는 같은 값을 구하지만 변수 이름만 다른 구현은 아니다."
- 🟢 6건(L1·L2·L3·L4×2·L5)은 조치 없음. 🟢 [L6] 은 세션에 Notion 도구가 없어 원문 대조를 하지 못했다고 기록했다.

처리:

- 🟡 [L7] :66 → 전단사 주장을 $i < j$ 와 비어 있지 않은 부분배열 사이로 좁히고, $i = j$ 인 쌍은 값이 모두 0 이라 후보로는 빈 배열 하나를 더한 것과 다르지 않다고 따로 적었다. 뒤따르는 $\max_{0 \le i \le j \le N}$ 식은 그대로 성립한다.
- 🟡 [L7] :142 → "변수 이름만 다르다"를 걷어내고, 카데인은 $k$ 하나를, 이 코드는 $p$ 와 $m$ 을 따로 굴린다는 차이를 밝힌 뒤 증명이 보장하는 것은 자리별 값의 일치뿐이라고 한정했다.
- 본편의 🔴 처리로 부분 문제 정의가 뒷조각 기준이 되어, 이 글의 기호 되짚기와 $S_i$·$T_{i+1}$ 정의, `extend.svg` 의 두 열 머리말도 같은 정의에 맞춰 고쳤다.
- 🟢 [L6] → 이번 세션에는 Notion MCP 가 있어 원문을 직접 가져와 대조했고, 결과를 이 리포트의 L6 에 적었다.

재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py` 두 편 모두 `발견 사항 없음 ✅`, SVG 파싱 정상. 증명의 결론과 수치는 세 차례 판정 내내 바뀌지 않았다.
