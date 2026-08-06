schema_version: review-report/v2
target: maximum-subarray
generated_at: 2026-08-06
strict: true
sources: src/content/posts/maximum-subarray.md
summary: 🔴 0 · 🟡 2 · 🟢 6

## Findings

### 🟡 [L2] src/content/posts/maximum-subarray.md:180

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray.md:180
- quote: 위 코드의 `best` 변수가 바로 이 값을 들고 다닌다.
- message: `best` 가 $k_1, \dots, k_{i-1}$ 의 최댓값과 같은 것은 $i$ 번째 반복에 들어서는 순간뿐이다. 반복 안에서 `best = max(best, k)` 를 지나고 나면 $k_i$ 까지 반영되어 $\max(k_1, \dots, k_i)$ 가 된다. 시점을 밝히지 않으면 "$a_i$ 를 포함하지 않는 최선"이 코드의 `best` 와 항상 같은 값이라고 읽힌다.
- recommendation: 시점을 문장에 넣는다. "반복에 들어설 때 `best` 가 이 값이고, `k` 를 갱신한 뒤에는 $k_i$ 까지 반영한다"처럼 두 상태를 나눠 적는다.
- gate_effect: warn

### 🟡 [L2] src/content/posts/maximum-subarray.md:182

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray.md:182
- quote: 부분 문제를 "$a_1 \dots a_i$ 안에서의 답"으로 잡으면 이렇게 되지 않는다.
- message: 바로 앞 절이 두 값의 범위를 "$a_1 \dots a_i$ 안에서"로 못박아 놓고, 이 문장은 같은 표현의 부분 문제로는 안 된다고 말한다. 앞뒤가 모순처럼 읽힌다. 실제로 안 되는 것은 접두 구간의 답을 **하나의 값으로만** 들고 갈 때이고, 앞 절은 그 값을 포함·미포함 둘로 쪼갰기 때문에 성립한다. 그 차이가 문장에 드러나지 않는다.
- recommendation: "하나로만 잡으면"처럼 한정을 넣고, 앞 절이 값을 둘로 나눈 이유가 바로 이것임을 한 문장으로 이어 붙인다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 문두 접속어가 거의 없고 어체는 ~다 평서체로 통일된다. 줄표는 제목과 링크 표기에만 쓰인다. 1차 검토에서 지적한 경구식 마무리 중복은 반영되어, 같은 꼴의 마무리는 마치며 한 곳에만 남았다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L3] src/content/posts/maximum-subarray.md:29

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray.md:29
- quote: 아래에서는 연속 부분배열을 짧게 구간이라고도 부른다.
- message: 검토 완료, 이슈 없음. 1차 검토의 용어 혼용 지적이 반영되어, 정의 절에서 "연속 부분배열"과 "구간"을 한 번 묶는다. $k_i$, $P_j$, $x$ 의 뜻이 글 전체에서 일관되고 추가 설명 편과도 같다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L4] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. problem.svg 의 원소값과 두 합(7, 9), prefix-sum.svg 의 $P_0 \dots P_8 = 0, 3, -2, 0, 4, 2, 5, -1, 7$ 과 $P_5 - P_2 = 4$, kadane-scan.svg 의 $k$ 행 $3, 0, 2, 6, 4, 7, 1, 9$ 및 $i = 2$ 의 끊김 표시가 모두 본문과 일치한다. 세 도판이 같은 열 좌표계를 써서 장면이 이어진다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목의 "자리마다 최선 하나만 들고 간다"가 글의 중심 주장과 맞고, description 이 세 복잡도와 빈 배열 허용 여부라는 두 축을 모두 담는다.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray.md:44

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray.md:44
- quote: N + (N-1) + \cdots + 1 = \frac{N(N+1)}{2}
- message: 검토 완료, 이슈 없음. 노션 원문 「Maximum Subarray」와 대조했다. 원문의 여섯 줄기(문제, $O(N^3)$, $O(N^2)$, Idea 1·2·3)를 모두 담았고 노트 밖 확장은 "더 나가면"에서 명시한다. 원문이 부분배열 개수를 $N(N-1)/2$ 로 적은 것은 $N(N+1)/2$ 로 바로잡았다. 원문 자신의 두 셈법을 그대로 따라가도 $N(N+1)/2$ 가 나오므로 논증 구조는 보존한 사실 정정이며, 근거는 스펙에 기록되어 있다.
- recommendation: 조치 불필요. 정정 사실을 PR 본문에도 한 줄 적어 두면 추적이 쉬워진다.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 부분배열 개수 $N(N+1)/2$ 를 두 셈법으로 각각 확인했고 $N = 8$ 에서 36이 맞다. 복잡도는 후보 수 $\Theta(N^2)$ 에 후보당 비용을 곱한 값과 일치하며 공간도 $O(N)$·$O(1)$ 로 맞다. 허용 정의의 $k$ 수열 $3, 0, 2, 6, 4, 7, 1, 9$ 와 비허용 정의의 $3, -2, 2, 6, 4, 7, 1, 9$ 를 손으로 돌려 둘 다 답 9 를 얻었고, $[-3, -1, -2]$ 의 0 과 $-1$ 도 확인했다. 두 종류로 나누는 사례 분류가 빠짐·겹침 없이 닫히고, 1차 검토에서 지적한 범위 미한정도 접두 구간 명시로 해소되었다.
- recommendation: 조치 불필요.
- gate_effect: info

## 후속 처리

1차 검토(같은 날, 반영 전)에서 🔴 1 · 🟡 3 이 나왔고 모두 반영한 뒤 이 리포트로 다시 판정했다. 1차 지적과 처리는 아래와 같다.

- 🔴 [L7] :176 "$a_i$ 를 포함하지 않는 부분배열 중 최선"에 범위 한정이 없어 문장 그대로는 거짓이었다. $a_i$ 오른쪽에 통째로 놓인 구간도 후보에 들어가기 때문이다. → 두 불릿 모두 "$a_1 \dots a_i$ 안에서"로 접두 구간을 명시하고 앞 문장에도 같은 한정을 넣었다.
- 🟡 [L2] :113 $k_0$ 이 정의 없이 등장 → 식 뒤에 기저의 뜻을 한 문장으로 붙였다.
- 🟡 [L3] :116 "연속 부분배열"과 "구간" 혼용 → 정의 절에서 두 말을 묶었다.
- 🟡 [L1] :180 경구식 마무리가 두 절 연속 반복 → "부분 문제를 어떻게 정의하느냐가 점화식의 난이도를 정한다." 를 삭제했다.

이 리포트의 🟡 2건도 판정 후 곧바로 반영했다.

- 🟡 [L2] :180 `best` 의 시점 → "반복에 들어설 때"와 "`k` 갱신 뒤"를 나눠 적도록 고쳤다.
- 🟡 [L2] :182 앞 절과 모순처럼 읽히는 문장 → "하나로만 잡으면"으로 한정하고, 값을 둘로 나눈 이유를 잇는 문장을 붙였다.

재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py` 두 편 모두 `발견 사항 없음 ✅`. 예시 수치($P$, $k$, 정답 9, 36개)와 SVG 5장은 처음부터 끝까지 변경하지 않았다.
