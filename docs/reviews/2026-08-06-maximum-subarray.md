schema_version: review-report/v2
target: maximum-subarray
generated_at: 2026-08-06
strict: true
sources: src/content/posts/maximum-subarray.md
summary: 🔴 1 · 🟡 3 · 🟢 3

## Findings

### 🔴 [L7] src/content/posts/maximum-subarray.md:176

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray.md:176
- quote: $a_i$ 를 **포함하지 않는** 부분배열 중 최선
- message: 범위를 한정하지 않아 문장 그대로는 거짓이다. $a_i$ 를 포함하지 않는 부분배열에는 $a_i$ 오른쪽에 통째로 놓인 것도 들어간다. 예시 배열에서 $i = 2$ 로 잡으면 $a_3 \dots a_8$(합 9)이 $a_2$ 를 포함하지 않는 후보인데, 바로 다음 문장이 제시하는 값 $\max(k_1) = 3$ 은 그것을 세지 않는다. 뒤 문장의 "앞에서 이미 끝난"이 범위를 조용히 좁히고 있어, 앞의 불릿과 뒤의 값이 서로 다른 집합을 가리킨다.
- recommendation: 불릿을 "$a_1 \dots a_i$ 안에서 $a_i$ 를 포함하지 않는 부분배열 중 최선"처럼 접두 구간으로 한정한다. 두 값이 모두 접두 구간 기준이라는 점을 앞 불릿에도 명시해 뒤 문장과 범위를 맞춘다.
- gate_effect: fail

### 🟡 [L1] src/content/posts/maximum-subarray.md:180

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray.md:180
- quote: 부분 문제를 어떻게 정의하느냐가 점화식의 난이도를 정한다.
- message: 같은 꼴의 경구식 마무리가 두 절 연속으로 반복된다. 200번 줄도 "문제를 어떻게 쪼개느냐가 알고리즘을 정한다."로 끝나, "어떻게 ~냐가 ~을 정한다"라는 대칭 문장이 글의 마지막 두 마디를 차지한다. L1이 지적하는 경구식 섹션 마무리와 대칭 문장 반복에 함께 걸린다.
- recommendation: 둘 중 하나를 남긴다. 180번 줄은 앞 문장의 설명으로 흡수하고, 마무리 경구는 마치며에만 두는 편이 낫다.
- gate_effect: warn

### 🟡 [L2] src/content/posts/maximum-subarray.md:113

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray.md:113
- quote: k_0 = 0, \qquad k_{i+1} = \max(k_i + x,\; 0)
- message: $k_0$ 이 정의 없이 등장한다. 바로 앞의 callout은 $k_i$ 를 "$a_i$ 에서 끝나는 부분배열의 최댓값"으로 정의하는데 $a_0$ 은 없다. 독자가 기저를 스스로 유추해야 하고, 추가 설명 편의 귀납 증명이 이 $k_0 = 0$ 을 base case로 쓰기 때문에 빈틈이 그대로 이어진다.
- recommendation: 기저를 한 문장으로 붙인다. 예를 들어 "$k_0$ 은 배열이 시작하기 전 자리이므로 후보가 빈 배열뿐이고, 따라서 $k_0 = 0$ 이다"를 식 앞이나 뒤에 둔다.
- gate_effect: warn

### 🟡 [L3] src/content/posts/maximum-subarray.md:116

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray.md:116
- quote: $k_i + x$ 가 음수면 0을 고르는 편이 낫다. 여기서 구간이 한 번 끊긴다.
- message: 같은 대상을 "연속 부분배열"과 "구간" 두 이름으로 부른다. 본문은 첫 절에서 "연속 부분배열"을 정의어로 세워 놓고, 목차(16번 줄)와 description(4번 줄), 그리고 이 문장에서는 "구간"을 쓴다. 두 말이 같은 것을 가리킨다는 안내가 없다.
- recommendation: 정의 절에서 "이 글에서는 연속 부분배열을 짧게 구간이라고도 부른다"처럼 한 번 묶어 주거나, 본문 서술을 한쪽으로 통일한다.
- gate_effect: warn

### 🟢 [L4] src/content/posts/maximum-subarray.md

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/maximum-subarray.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. problem.svg 의 원소값과 두 합(7, 9), prefix-sum.svg 의 $P_0 \dots P_8 = 0, 3, -2, 0, 4, 2, 5, -1, 7$ 과 $P_5 - P_2 = 4$, kadane-scan.svg 의 $k$ 행 $3, 0, 2, 6, 4, 7, 1, 9$ 및 $i = 2$ 의 끊김 표시가 모두 본문과 일치한다.
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

### 🟢 [L6] src/content/posts/maximum-subarray.md:40

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray.md:40
- quote: N + (N-1) + \cdots + 1 = \frac{N(N+1)}{2}
- message: 노션 원문 「Maximum Subarray」와 대조했다. 원문의 여섯 줄기(문제, $O(N^3)$, $O(N^2)$, Idea 1·2·3)를 모두 담았고 노트 밖 확장은 "더 나가면"에서 명시한다. 다만 원문이 부분배열 개수를 $N(N-1)/2$ 로 적은 것을 이 글은 $N(N+1)/2$ 로 바로잡았다. 원문 자신의 두 셈법을 그대로 따라가도 $N(N+1)/2$ 가 나오므로 논증 구조는 보존한 사실 정정이다. 정정 근거는 스펙에 기록되어 있다.
- recommendation: 조치 불필요. 정정 사실이 스펙에만 남아 있으므로 PR 본문에서도 한 줄 언급해 두면 추적이 쉬워진다.
- gate_effect: info

## 후속 처리

- 🔴 [L7] :176 "$a_i$ 를 포함하지 않는 부분배열 중 최선"의 범위 미한정 → 두 불릿 모두 "$a_1 \dots a_i$ 안에서"로 접두 구간을 명시하고, 앞 문장에도 "두 값 모두 범위가 앞쪽 $a_1 \dots a_i$ 로 한정된다"를 넣어 뒤 문장의 값과 집합을 맞췄다.
- 🟡 [L2] :113 $k_0$ 이 정의 없이 등장 → 식 뒤에 "기저 $k_0$ 은 배열이 시작하기 전 자리다. 거기서 끝나는 부분배열은 빈 것 하나뿐이므로 $k_0 = 0$ 이다."를 추가했다.
- 🟡 [L3] :116 "연속 부분배열"과 "구간" 혼용 → 정의 문장 뒤에 "아래에서는 연속 부분배열을 짧게 구간이라고도 부른다"를 붙여 두 말을 묶었다.
- 🟡 [L1] :180 경구식 마무리 중복 → "부분 문제를 어떻게 정의하느냐가 점화식의 난이도를 정한다." 한 문장을 삭제하고, 같은 꼴의 마무리는 마치며에만 남겼다.
- 🟢 3건(L4·L5·L6)은 조치 없음.
- 재검증: `npm run build` 성공(135 페이지), `python .claude/review_post.py`는 두 편 모두 `발견 사항 없음 ✅`. 예시 수치($P$, $k$, 정답 9, 36개)와 SVG 5장은 변경하지 않았다.
- 게이트: 이 리포트는 반영 전 시점의 판정이라 🔴 1건이 그대로 남아 `--finalize --strict` 가 exit 1 이다. 위 반영 내용의 확정은 다음 날짜의 재리뷰 리포트로 닫는다.
