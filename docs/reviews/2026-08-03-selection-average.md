schema_version: review-report/v2
target: selection-average
generated_at: 2026-08-03
strict: true
sources: src/content/posts/selection-average.md
summary: 🔴 0 · 🟡 2 · 🟢 5

## Findings

### 🟡 [L5] src/content/posts/selection-average.md:7

- severity: 🟡
- source: L
- rule_id: L5
- location: src/content/posts/selection-average.md:7
- quote: "difficulty: 고급"
- message: 난이도 표기가 스펙과 다르고 시리즈 안에서 뒤집혀 있다. `docs/superpowers/specs/2026-06-29-selection-design.md:31`은 이 글을 심화로 지정했는데 실제 frontmatter는 고급이다. `src/content/config.ts:13`의 순서가 입문·초급·중급·고급·심화이므로, 본편 `selection.md`(심화)보다 이 글이 한 단계 쉬운 것으로 표시된다. 이 글은 본편이 "대부분 $O(n)$"으로 넘어간 자리를 기댓값 점화식과 귀납법으로 채우는 확장이라 본편보다 쉽다고 보기 어렵다. 같은 시리즈의 `selection-why-five.md`도 같은 값이라 두 확장 글이 함께 어긋나 있다.
- recommendation: 두 추가 설명 글을 심화로 올리거나, 5단계 재조정(#24) 이후 기준이 바뀐 것이라면 스펙의 난이도 항목을 현재 기준으로 갱신해 한쪽으로 맞춘다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/selection-average.md:32

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/selection-average.md:32
- quote: "대칭성에 의해 두 반쪽을 합산하면 $E(\lfloor n/2 \rfloor), E(\lfloor n/2 \rfloor+1), \ldots, E(n-1)$이 각각 **두 번씩** 나타난다."
- message: 합을 절반 구간으로 줄이는 단계에 전제 하나가 빠져 있고 표현 하나가 과하다. 첫째, `max(E(i-1), E(n-i))`를 `E(max(i-1, n-i))`로 바꾸려면 $E$가 단조 증가해야 하는데 그 가정이 어디에도 없다. 본문은 "$i$가 $n/2$를 넘으면 $E(i-1)$이 더 크고"라고 곧장 단정하는데, 이는 $E$의 단조성을 이미 쓰고 있는 서술이다. 둘째, "각각 두 번씩 나타난다"는 짝수 $n$에서만 정확하다. $n=5$로 확인하면 max 값의 다중집합이 $E(4), E(3), E(2), E(3), E(4)$이라 $E(\lfloor 5/2 \rfloor) = E(2)$는 한 번만 나온다. 결론이 부등식이라 상계는 그대로 성립하지만, 등식처럼 읽히는 서술이 뒤따르는 부등호와 어긋난다.
- recommendation: $E$가 단조 증가한다는 전제를 한 줄로 밝히고(비용 함수의 정의에서 따라온다), "각각 두 번씩"을 "많아야 두 번씩"으로 고쳐 뒤의 부등호와 맞춘다. 홀수 $n$에서 가운데 항이 한 번만 나온다는 점을 괄호로 덧붙이면 충분하다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/selection-average.md:1-89

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/selection-average.md:1-89
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/selection-average.md:1-89

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/selection-average.md:1-89
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/selection-average.md:1-89

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/selection-average.md:1-89
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] src/content/posts/selection-average.md:1-89

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/selection-average.md:1-89
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 이 글은 SVG를 참조하지 않는다. 수식과 산문만으로 논증이 닫히므로 대조할 그림이 없다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] src/content/posts/selection-average.md:10

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/selection-average.md:10
- quote: "본문은 quickselect를 소개하면서 \"대부분 $O(n)$\"이라는 말로 평균을 넘어갔다."
- message: 노션 원문(🛹 Selection Problem)과 대조했다. 원문은 quickselect의 최선 `S(n) = n + S(n/2) = O(n)`과 최악 `S(n) = n + S(n-1) = O(n^2)`만 다루고 "이렇게만 해도 '대부분' O(n)에 되지만, worst case가 남아있기에 불안하다"로 넘어간다. 기댓값 점화식, max 항, 귀납법 상계 $E(n) \le 4n$은 원문에 없는 확장이다. 이 글은 첫 문단에서 원문의 그 표현을 그대로 인용하며 빈칸을 채운다고 밝히고, `docs/superpowers/specs/2026-06-29-selection-design.md:30-37`이 확장 범위를 미리 기록해 두었다. 원문에 없는 주장을 원문의 것처럼 제시한 곳은 없고, 원문의 핵심인 한쪽만 재귀한다는 점과 최악이 $O(n^2)$로 남는다는 점도 누락 없이 유지된다.
- recommendation: not-recorded
- gate_effect: info
