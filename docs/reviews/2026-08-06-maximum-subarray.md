schema_version: review-report/v2
target: maximum-subarray
generated_at: 2026-08-06
strict: true
sources: src/content/posts/maximum-subarray.md
summary: 🔴 0 · 🟡 0 · 🟢 7

## Findings

### 🟢 [L1] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 문두 접속어가 거의 없고 어체는 ~다 평서체로 통일된다. 줄표는 제목과 링크 표기에만 쓰인다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L2] src/content/posts/maximum-subarray.md:36

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray.md:36
- quote: 8만 따로 떼어 $[8]$ 을 고를 수는 있다. 앞의 $2 + 4$ 와 8을 **한 구간에 함께** 담으려면 연속이라는 조건 때문에 두 음수를 반드시 지나가야 한다.
- message: 검토 완료, 이슈 없음. 직전 판정이 지적한 범위 누락이 해소되었다. $[8]$ 이 선택 가능하다는 사실과, 앞의 양수 구간을 함께 담을 때만 두 음수를 지나야 한다는 조건이 구분되어 있다. 절 사이 연결에도 도약이 없다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L3] src/content/posts/maximum-subarray.md:96

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray.md:96
- quote: 부분 문제는 "뒷조각"(suffix)으로 잡는다.
- message: 검토 완료, 이슈 없음. 새로 세운 "뒷조각"이 처음 쓰이는 자리에서 정의되고 영어 대응어도 함께 적혀 있다. 이후 정의 callout, 후보 분류, 비허용 정의, 포함·미포함 절, 마치며가 모두 같은 말을 쓰고 추가 설명 편의 기호 되짚기와도 일치한다. "연속 부분배열"과 "구간"을 묶는 안내도 정의 절에 남아 있다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L4] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. problem.svg 의 원소값과 두 합(7, 9), prefix-sum.svg 의 $P_0 \dots P_8 = 0, 3, -2, 0, 4, 2, 5, -1, 7$ 과 $P_5 - P_2 = 4$, kadane-scan.svg 의 $k$ 행 $3, 0, 2, 6, 4, 7, 1, 9$ 와 $i = 2$ 의 끊김 표시가 본문과 일치한다. kadane-scan.svg 의 부제도 본문의 새 정의에 맞춰 뒷조각 표현으로 고쳐졌다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목의 "자리마다 최선 하나만 들고 간다"가 글의 중심 주장과 맞고, description 이 세 복잡도와 빈 배열 허용 여부라는 두 축을 담는다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray.md:44

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray.md:44
- quote: N + (N-1) + \cdots + 1 = \frac{N(N+1)}{2}
- message: 검토 완료, 이슈 없음. 이 세션에서는 `notion-search`·`notion-fetch` 로 원문 「Maximum Subarray」(2026-08-06 조회)를 직접 가져와 대조했다. 직전 판정이 도구 부재로 대조하지 못했다고 적은 부분을 여기서 닫는다. 원문의 여섯 줄기(문제, $O(N^3)$, $O(N^2)$, Idea 1·2·3)를 모두 담았고 노트 밖 확장은 "더 나가면"에서 명시한다. 원문이 부분배열 개수를 $N(N-1)/2$ 로 적은 것은 $N(N+1)/2$ 로 바로잡았다. 원문 자신의 두 셈법을 따라가도 같은 값이 나오므로 논증 구조는 보존한 사실 정정이며 근거는 스펙에 있다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray.md:99

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray.md:99
- quote: $k_i$ = $a_1 \dots a_i$ 의 **뒷조각** 중 합의 최댓값 (빈 뒷조각 포함)
- message: 검토 완료, 이슈 없음. 직전 판정의 🔴, 곧 빈 배열이 "$a_i$ 에서 끝나는" 집합에 속하지 않아 정의가 자기모순이던 문제가 해소되었다. 빈 뒷조각은 실제로 뒷조각이므로 집합이 정합하고, 후보 분류의 두 갈래도 같은 집합 위에서 빠짐·겹침 없이 닫힌다. $k_0 = 0$ 도 빈 배열의 뒷조각이 빈 것 하나뿐이라는 사실에서 곧바로 나온다. 포함·미포함 해석에서 $k_i$ 가 정확히는 "포함하는 최선과 0 중 큰 쪽"이라는 차이도 본문이 밝힌다. 수치는 다시 검산했다. 부분배열 수 36, 전체 합 7, 최대 합 9, $P_0 \dots P_8$, 허용 정의 $k = 3, 0, 2, 6, 4, 7, 1, 9$, 비허용 정의 $k = 3, -2, 2, 6, 4, 7, 1, 9$, $[-3, -1, -2]$ 의 0 과 $-1$, 그리고 $O(N^3)$·$O(N^2)$·$O(N)$ 과 공간 $O(N)$·$O(1)$ 이 모두 맞다.
- recommendation: 조치 불필요.
- gate_effect: info

## 후속 처리

### 1차 판정 (같은 날, 초안 대상)

- 🔴 [L7] :176 "$a_i$ 를 포함하지 않는 부분배열 중 최선"에 범위 한정이 없어 문장 그대로는 거짓 → 두 항목을 접두 구간으로 한정했다.
- 🟡 [L2] :113 $k_0$ 이 정의 없이 등장 → 기저의 뜻을 한 문장으로 붙였다.
- 🟡 [L3] :116 "연속 부분배열"과 "구간" 혼용 → 정의 절에서 두 말을 묶었다.
- 🟡 [L1] :180 경구식 마무리 중복 → 한 문장을 삭제했다.

### 2차 판정

- 🟡 [L2] :180 `best` 의 시점 → "반복에 들어설 때"와 "`k` 갱신 뒤"를 나눠 적었다.
- 🟡 [L2] :182 앞 절과 모순처럼 읽히는 문장 → "하나로만 잡으면"으로 한정했다.

### 3차 판정 (독립 리뷰, 이 리포트가 대체함)

3차 판정의 finding 은 아래에 원문대로 옮긴다.

- 🔴 [L7] :99 `$k_i$ = $a_i$ **에서 끝나는** 부분배열의 합 중 최댓값 (빈 배열 허용)` — "빈 배열은 어떤 $a_i$에서도 끝나거나 $a_i$를 포함하지 않으므로 이 정의는 $k_i=0$인 상태와 모순되고, 103-108행의 후보 분류와 177-180행의 포함 여부 해석도 성립하지 않는다." 권고는 빈 배열 허용 상태를 suffix 기준으로 다시 정의하라는 것이었다. 나머지 수치와 복잡도는 독립 검산에서 모두 맞다고 확인되었다.
- 🟡 [L2] :36 `버리고 싶어도 연속이라는 조건 때문에 뒤의 8을 쓰려면 반드시 지나가야 한다.` — "부분배열 $[8]$도 가능하므로 8을 쓰기 위해 $-2$와 $-6$을 반드시 지나가야 한다는 설명은 범위가 빠져 있다."
- 🟢 6건(L1·L3·L4×3·L5)은 조치 없음. 🟢 [L6] 은 세션에 Notion 도구가 없어 원문 대조를 하지 못했다고 기록했다.

처리:

- 🔴 → 부분 문제를 "$a_1 \dots a_i$ 의 뒷조각(suffix), 빈 뒷조각 포함"으로 다시 정의했다. 정의 callout, 앞선 설명 문단, 후보 분류 두 갈래, 기저 $k_0$, 비허용 정의, 포함·미포함 절, 마치며를 모두 같은 정의에 맞췄다. 포함·미포함 절에는 $k_i$ 가 정확히는 "$a_i$ 를 포함하는 최선과 0 중 큰 쪽"이며 포함 후보가 모두 음수일 때만 갈린다는 단서를 넣었다. `kadane-scan.svg` 의 부제도 함께 고쳤다.
- 🟡 [L2] :36 → $[8]$ 을 따로 고를 수 있다는 사실을 먼저 밝히고, 두 음수를 지나야 하는 것은 앞의 $2 + 4$ 와 8을 한 구간에 함께 담을 때임을 조건으로 달았다.
- 🟢 [L6] → 이번 세션에는 Notion MCP 가 있어 원문을 직접 가져와 대조했고, 결과를 이 리포트의 L6 에 적었다.

### 판정 뒤 사용자 요청으로 고친 것

- "뒷조각"에 구체적인 설명이 필요하다는 지적 → 정의를 "$a_1 \dots a_i$ 에서 앞의 몇 개를 잘라내고 남은 조각"으로 풀어 쓰고 개수가 $i+1$ 개임을 밝힌 뒤, $i = 4$ 인 $[3, -5, 2, 4]$ 의 뒷조각 다섯 개를 잘라낸 개수·조각·합의 표로 열거해 최댓값 6이 $k_4$ 임을 보였다. 추가 설명 편의 기호 되짚기에도 한 문장 요약을 넣어 그 글만 읽어도 뜻이 통하게 했다.

재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py` 두 편 모두 `발견 사항 없음 ✅`, SVG 5장 파싱 정상. 새 표의 값 $4, 1, 6, 4, 0$ 을 직접 더해 확인했고 최댓값 6은 $k$ 수열의 $k_4$ 와 같다. 예시 수치($P$, $k$ 두 수열, 정답 9, 36개)는 네 차례 판정 내내 바뀌지 않았다.
