schema_version: review-report/v2
target: maximum-subarray-why-extend
generated_at: 2026-08-08
strict: true
sources: src/content/posts/maximum-subarray-why-extend.md
summary: 🔴 0 · 🟡 2 · 🟢 6

## Findings

### 🟡 [L4] public/images/maximum-subarray-why-extend/prefix-min.svg:10

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/maximum-subarray-why-extend/prefix-min.svg:10
- quote: <text x="430" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">누적합 꺾은선에서 낙차가 가장 큰 구간</text>
- message: SVG의 수치와 방향은 $P_2=-2$에서 $P_8=7$로 9만큼 올라가는 모습을 정확히 그리지만, 제목과 주석은 이를 낙차라고 부른다. 아래 골짜기에서 위 봉우리로 향하는 변화이므로 상승폭이라는 뜻과 반대다.
- recommendation: SVG 제목과 주석, 본문 89행과 91행의 낙차를 상승폭이나 증가량으로 바꿔 화살표 방향과 뜻을 맞춘다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/maximum-subarray-why-extend.md:158

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray-why-extend.md:158
- quote: 앞 절의 증명이 말해 주는 것은 두 코드가 매 자리에서 같은 값 $P_j - m_j = k_j$ 를 얻는다는 사실이지, 구현이 같다는 뜻이 아니다.
- message: 제시된 코드는 `m`을 갱신하기 전에 `p - m`을 계산하므로 반복 $j$에서 실제로 평가하는 값은 $P_j-m_{j-1}$이다. 예시의 $j=2$에서는 코드는 $-2$를 평가하지만 $P_2-m_2=k_2=0$이다. `best`가 이미 0 이상이라 최종 답은 올바르지만, 코드가 매 자리에서 등식의 값을 얻는다는 설명은 156행의 올바른 갱신 순서 설명과 모순된다.
- recommendation: 두 수학적 풀이가 매 자리에서 같은 값을 정의한다고 한정하고, 이 구현은 갱신 순서 때문에 그 값을 매번 직접 계산하지 않아도 전역 최댓값만 올바르게 유지한다고 구분한다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/maximum-subarray-why-extend.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray-why-extend.md:11
- quote: 이 글은 강의 노트 밖 확장으로, 그 갱신에 손해가 없는 이유를 증명하고 누적합 관점의 다른 풀이와 이어 붙인다.
- message: 검토 완료, 이슈 없음. 평서체가 유지되고 문두 접속어, 과한 수사, 대칭 문장, 강조 표현이 남용되지 않는다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L2] src/content/posts/maximum-subarray-why-extend.md:51

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray-why-extend.md:51
- quote: 증명. 세 단계로 나눠 본다. 후보를 짝짓고, 짝의 합을 비교하고, 최댓값을 옮긴다.
- message: 검토 완료, 이슈 없음. 정의, 후보 대응, 최댓값 보존, 누적합 해석, 구현 순으로 전제가 도입되며 핵심 추론의 연결이 드러난다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L3] src/content/posts/maximum-subarray-why-extend.md:23

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray-why-extend.md:23
- quote: 기호는 본편 그대로다. 배열은 $a_1, \dots, a_N$, 누적합은 $P_0 = 0$, $P_j = a_1 + \cdots + a_j$, 그리고 $k_i$ 는 $a_1 \dots a_i$ 의 뒷조각 중 최대 합이다.
- message: 검토 완료, 이슈 없음. 배열, 누적합, 뒷조각, 후보 집합의 용어와 기호가 글 전체에서 같은 뜻으로 쓰이고 어체도 통일되어 있다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L4] public/images/maximum-subarray-why-extend/extend.svg:13

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/maximum-subarray-why-extend/extend.svg:13
- quote: <text x="430" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">a₆ 을 포함하는 후보는 a₁ … a₅ 의 뒷조각과 1:1로 대응한다</text>
- message: 검토 완료, 이슈 없음. 여섯 후보의 대응, 각 합에 3을 더한 값, 최댓값 4에서 7로의 이동이 본문 44행부터 63행의 정의와 계산에 모두 맞는다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray-why-extend.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray-why-extend.md:2
- quote: title: "추가 설명 — 왜 이어 붙이는 것이 최선인가"
- message: 검토 완료, 이슈 없음. 제목은 중심 증명을, description은 후보 대응과 누적합 풀이의 동치까지 실제 범위에 맞게 요약한다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray-why-extend.md:11

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray-why-extend.md:11
- quote: 이 글은 강의 노트 밖 확장으로, 그 갱신에 손해가 없는 이유를 증명하고 누적합 관점의 다른 풀이와 이어 붙인다.
- message: 검토 완료, 이슈 없음. 현재 환경에서는 Notion 원문 자체를 가져올 수 없었다. 저장소의 provenance 기록은 원문의 두 미해결 질문과 Idea 3을 특정하고, 후보의 1:1 대응 증명, Idea 3의 정당성, 두 풀이의 동치, 단일 훑기 코드를 승인된 추가로 분류한다. 본문도 노트 밖 확장임을 명시해 추가 내용을 원문으로 오인하게 하지 않는다.
- recommendation: 조치 없음. 추후 원문 접근이 가능해지면 직접 대조한다.
- gate_effect: info

## 후속 처리

🟡 2건을 모두 반영했다. 판정은 2026-08-08 시점 근거로 그대로 남긴다.

- 🟡 [L4] `prefix-min.svg:10` 방향과 어긋난 "낙차" → **반영 완료**. 화살표가 골짜기 $P_2 = -2$ 에서 봉우리 $P_8 = 7$ 로 올라가므로 "낙차"를 "상승폭"으로 바꿨다. 리뷰가 지목한 SVG 제목(`:10`)과 주석(`:49`) 외에, 같은 말을 쓰던 본문 89·91행과 마치며의 166행까지 함께 고쳤다. 골짜기·봉우리 비유는 방향과 맞으므로 그대로 뒀다.
- 🟡 [L7] `:158` 코드가 자리마다 $P_j - m_j$ 를 얻는다는 서술 → **반영 완료**. 두 **풀이**가 자리마다 같은 값을 정의한다는 진술과, 두 **코드**가 그 값을 매번 계산한다는 진술을 갈랐다. 이 구현이 $j$ 번째 반복에서 읽는 값은 $P_j - m_{j-1}$ 이며, 예시의 $j = 2$ 에서 코드가 읽는 값은 $-2$ 이고 $k_2 = 0$ 이라 자리마다의 값은 다르다는 점, 일치하는 것은 `best` 가 유지하는 전체 최댓값이라는 점을 적었다. 156행의 갱신 순서 설명과 모순되지 않는다.

### 리포트 이후의 별도 수정 — 인덱스 기호 통일

리뷰 반영과 무관하게, 리포트 작성 이후 인덱스 기호를 통일했다. 리뷰가 지적한 사항이 아니라 읽힘 개선이므로 여기 따로 적는다.

$i$ 가 절마다 다른 뜻으로 쓰이고 있었다. 「이어 붙이기」에서는 현재 자리($S_i$, $k_i + x$)였고, 「누적합으로 다시 보기」부터는 잘라내는 지점이 되면서 현재 자리가 $j$ 로 넘어갔다. 「두 풀이는 같다」의 $k_j = \max_{0 \le i \le j}(P_j - P_i)$ 는 두 뜻을 한 식에 함께 놓아 충돌이 가장 크게 드러나는 자리였다. **$j$ 는 지금 보고 있는 자리, $s$ 는 앞에서 잘라낸 자리**로 글 전체에 고정했다.

본편은 자리를 $i$ 로 적고 구간합을 $a_i + \cdots + a_j = P_j - P_{i-1}$ 로 적으므로, 이 글은 본편과 글자가 달라진다. "기호는 본편 그대로다"라는 기존 문장이 사실과 어긋나게 되므로 기호 문단을 다시 써서 두 글의 차이와 그 이유를 명시했다. 정의·논증·수치는 바꾸지 않았고 글자만 바꿨다.

이 수정으로 위 🟢 [L3] finding이 인용한 23행이 다시 쓰였다. 해당 판정은 수정 전 본문에 대한 것이므로, **L3(용어·기호 일관성)는 재리뷰 대상이다.** 본편과의 기호 차이가 시리즈 일관성 측면에서 받아들일 만한지도 함께 판정이 필요하다.

### 리포트 이후의 별도 수정 — 원문 언급 삭제

정본 가이드에 새로 명시한 「원문을 본문에서 드러내지 않는다」를 적용했다. 네 곳에서 귀속을 걷고 내용은 살렸다.

- `:11` "이 글은 강의 노트 밖 확장으로" → 삭제. 뒤따르는 "그 갱신에 손해가 없는 이유를 증명하고…"가 글의 범위를 이미 말한다.
- `:63` "원문 노트는 이 사실을 …로 적었다. 같은 말이다." → "같은 사실을 …로 적을 수도 있다." 대체 표현과 뒤이은 논증은 그대로다.
- `:89` "원문 노트가 …라고 남긴 방법인데" → "이 방법이 정말 답을 내는지는 의심스러울 수 있는데". 의심을 독자의 것으로 돌렸고 근거를 가리키는 구조는 유지했다.
- `:143` "원문 노트는 …라고 적었다" → "누적합 풀이를 식 그대로 옮기면 … 배열을 세 번 훑는다." 세 번 훑는다는 사실이 본문 서술로 남았다.

이 수정으로 위 🟢 [L6] finding이 인용한 11행이 바뀌었다. **L6(원문 충실성)는 재리뷰 대상이다.** 확장 경계 표시를 본문에서 걷어낸 뒤에도 추가 내용을 원문으로 오인할 여지가 없는지 판정이 필요하다. provenance 기록은 이 리포트와 포스트별 스펙에 남아 있다.

반영 후 검증: 코드를 예시 배열 $[3, -5, 2, 4, -2, 3, -6, 8]$ 로 추적해 $j$ 마다 읽는 값 $3, -2, 2, 6, 4, 7, 1, 9$ 와 $P_j - m_j = k_j$ 인 $3, 0, 2, 6, 4, 7, 1, 9$ 가 $j = 2$ 에서만 갈리고 `best` 는 두 경우 모두 9로 끝남을 확인했다. `npm run build` 성공. 증명 구조와 복잡도 주장은 바꾸지 않았다.
