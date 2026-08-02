schema_version: review-report/v2
target: karatsuba
generated_at: 2026-07-28
strict: not-recorded
summary: 🔴 0 · 🟡 3 · 🟢 8

## Findings

### 🟡 [L4] src/content/posts/karatsuba.md:73

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/karatsuba.md:73
- quote: "이 자리 이동이 있어야 세 조각이 서로 겹치지 않고 하나의 수로 합쳐진다."
- message: 본문과 SVG의 자릿수 겹침 설명이 반대다 — 세 항은 서로 다른 자릿수만 차지하는 것이 아니라 겹치는 자릿수끼리 더해진다. `public/images/karatsuba/split-and-recombine.svg:40-50`도 이를 그대로 그린다. 눈금에서 첫째 막대는 4m부터 2m, 가운데 막대는 3m부터 m, 셋째 막대는 2m부터 0까지이므로 첫째와 가운데는 3m부터 2m에서, 가운데와 셋째는 2m부터 m에서 겹친다. 자리 이동의 역할은 겹침 제거가 아니라 각 항을 올바른 자릿수에 맞추는 것이다. 이 문장 외의 SVG 식, 이동량, 네 곱, 점화식과 복잡도 표시는 본문과 일치한다.
- recommendation: "서로 겹치지 않고"를 "서로 다른 위치에 맞춰지고, 겹치는 자릿수끼리 더해져"처럼 고쳐 자리 정렬과 덧셈을 정확히 구분한다.
- gate_effect: warn

### 🟡 [L6] src/content/posts/karatsuba.md:1

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/karatsuba.md:1
- quote: not-recorded
- message: Notion 원문 대조를 검증할 수 없다 — 이 보고서에서 확인할 수 있는 증거만으로는 Notion 원문을 가져왔거나 원문과 현재 글을 대조했다고 검증할 수 없다. 따라서 원문의 구조, 논증 흐름, 의도한 주장에 대한 충실성 비교는 완료되지 않았다.
- recommendation: `notion-search`와 `notion-fetch`를 실제로 사용할 수 있고 검색 및 조회 결과가 감사 가능한 환경에서 원문 비교를 다시 수행한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/karatsuba.md:213

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/karatsuba.md:213
- quote: "각 호출이 절반 크기의 재귀" / `BigInt P3 = karatsuba(x1 + x2, y1 + y2);`
- message: 올림 분리 설명이 의사코드에 반영되지 않았다 — 197행은 합에서 넘친 올림 자리를 따로 떼어 재귀 입력을 m자리로 유지한다고 설명한다. 그러나 216행의 의사코드는 합을 그대로 넘기므로 두 합은 각각 m+1자리가 될 수 있다. 알고리즘과 최종 점근 복잡도는 옳지만, 제시된 코드만으로는 모든 호출이 정확히 절반 크기라는 213행의 주석과 점화식 `3T(n/2)`의 엄밀한 전제가 충족되지 않는다.
- recommendation: 의사코드에 올림 분리와 선형 시간 보정을 표시하거나, 주석을 "두 호출은 절반 크기이고 합 호출은 최대 m+1자리"로 고친 뒤 완화된 점화식도 같은 점근 복잡도를 갖는다고 설명한다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/karatsuba.md:27

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/karatsuba.md:27
- quote: "무엇을 \"곱셈 한 번\"으로 세는가"
- message: 검토 완료, 이슈 없음. `docs/writing-rules.md`의 접속어, 보조 용언, 불필요한 수식어, 지시어, 중복, 의존 명사, 복수 표지, 관형격 조사 항목을 문맥에 따라 확인했다. 지정된 문두 접속어는 0회였고, 강조와 긴 줄표는 개념 대비나 목록 구분에 제한적으로 쓰였다. 짧은 질문과 평서문이 섞여 리듬이 자연스럽고 과형식화나 기계적 문장 패턴도 두드러지지 않는다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L1] src/content/posts/karatsuba.md:288

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/karatsuba.md:288
- quote: "분할 정복에서 재귀 가지의 수는 그만큼 무겁다."
- message: 마무리 문장이 행렬 곱셈 글과 동일한 후렴이다 — 마치며의 마지막 문장이 `matrix-multiplication.md`의 마무리 문장과 완전히 같다. 의도된 후렴(refrain)으로 두 글의 짝을 강조하지만 다소 경구식으로 닫힌다.
- recommendation: 의도된 대구라면 그대로 두어도 무방하다. 반복이 부담스러우면 카라츠바 문맥에 맞춰 한 번 변주하는 선택지도 있다.
- gate_effect: info

### 🟢 [L2] src/content/posts/karatsuba.md:27

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/karatsuba.md:27
- quote: "무엇을 \"곱셈 한 번\"으로 세는가"
- message: 검토 완료, 이슈 없음. 비용 단위 정의, 네 곱을 쓰는 순진한 분할, 가운데 항만 얻으면 된다는 관찰, 세 곱 항등식, 복잡도, 자릿수 예외, 진법 일반화, Strassen 대응 순으로 전개된다. 각 절이 앞 절에서 생긴 질문에 답하며, 카라츠바 항등식을 도입하기 전에 필요한 전개식과 목표값을 충분히 제시한다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L2] src/content/posts/karatsuba.md:197

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/karatsuba.md:197
- quote: "떼어 낸 몫은 $\Theta(n)$ 짜리 보정 덧셈으로 처리되므로"
- message: 넘친 올림 자리를 "몫"이라 부른다 — 떼어 내는 값은 $x_1+x_2$ 가 $m$ 자리를 넘길 때의 올림(carry) 성분이지 나눗셈의 몫이 아니다. 바로 앞 문장의 "넘친 올림 자리"와 용어가 어긋난다.
- recommendation: "떼어 낸 올림 자리" 또는 "떼어 낸 자리 넘침"으로 바꿔 앞 문장과 맞춘다.
- gate_effect: info

### 🟢 [L3] src/content/posts/karatsuba.md:224

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/karatsuba.md:224
- quote: "나머지 덧셈·뺄셈과 자리 밀기는 Θ(n) 으로 점화식의 상수항에 흡수된다."
- message: 점화식의 비재귀 항을 상수항으로 부른다 — `Θ(n)`은 n에 따라 증가하므로 상수항이 아니다. 같은 글의 83행은 이를 "덧셈 항", 176행은 조립 비용으로 정확히 설명한다. 수학적 결론에는 영향이 없지만 용어가 앞선 설명과 어긋난다. 그 밖의 "초등학교식", "자리 곱셈", "나이브", "순진한 분할" 표기는 각 대상을 구분하며 일관되게 쓰였다.
- recommendation: "점화식의 Θ(n) 항" 또는 "점화식의 비재귀 항"으로 바꾼다.
- gate_effect: info

### 🟢 [L4] public/images/karatsuba/four-vs-three.svg:4

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/karatsuba/four-vs-three.svg:4
- quote: "곱셈 한 번이 재귀 가지 하나"
- message: 검토 완료, 이슈 없음. 네 곱과 세 곱의 레이블, 재귀 가지 수, 입력 크기, 가운데 항 복원식, 두 점화식, `log₂4 = 2`, `log₂3 = 1.585…`, 최종 복잡도가 모두 본문과 일치한다. `public/images/karatsuba/split-and-recombine.svg`도 위 L4 문장 불일치를 제외하면 분할식, 각 이동량, 눈금, 네 곱과 복잡도 값이 정확하다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L5] src/content/posts/karatsuba.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/karatsuba.md:2
- quote: "n자리 두 수를 곱하는 데 정의대로면 Θ(n²)이 든다."
- message: 검토 완료, 이슈 없음. 제목은 카라츠바가 이차 시간보다 빠른 정수 곱셈을 보인다는 중심 주장을 담는다. description은 순진한 곱셈, 네 갈래 분할의 한계, 세 곱 축소, `Θ(n^1.585)`, Strassen과의 구조적 대응을 실제 본문 순서대로 요약한다. `difficulty: 중급`도 점화식과 마스터 정리를 다루는 깊이에 맞는다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L7] src/content/posts/karatsuba.md:122

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/karatsuba.md:122
- quote: P_3 - P_1 - P_2 = x_1y_2 + x_2y_1
- message: 검토 완료, 이슈 없음. 위 의사코드 표기 문제를 제외한 수식과 수치를 독립적으로 검산했다. 카라츠바 항등식과 재조립식이 성립한다. 마스터 정리에서 `4T(n/2)+Θ(n)=Θ(n²)`이고 `3T(n/2)+Θ(n)=Θ(n^{log₂3})`이며, `log₂3=1.5849625… > 1`이라 선형 조립 비용이 흡수된다. 1024자리 예시는 `1024²=1,048,576`, `3¹⁰=59,049`, 비율 `17.7577…`로 "열여덟 배 가까이"와 맞는다. `2^1.585≈3`, `log₃5≈1.46497`, 비트와 십진 자리의 환산 계수 `log₁₀2≈0.30103`도 정확하다.
- recommendation: 조치 없음.
- gate_effect: info
