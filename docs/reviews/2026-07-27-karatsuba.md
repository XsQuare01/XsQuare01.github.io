## 결정적 검사: src/content/posts/karatsuba.md
발견 사항 없음 ✅

---

## LLM 비평: src/content/posts/karatsuba.md

참조 SVG: `public/images/karatsuba/split-and-recombine.svg`, `public/images/karatsuba/four-vs-three.svg`

### 🟡 [L3] src/content/posts/karatsuba.md:280 — '초등학교식' / '초등학교 방식' 혼용

- **severity**: 🟡
- **source**: L
- **rule_id**: L3
- **location**: `src/content/posts/karatsuba.md:280`
- **quote**: "작은 수에서는 초등학교식이 빠르다. GMP 같은 다중 정밀도 라이브러리는 임계값(대략 수백~수천 비트) 아래에서 초등학교식을"
- **message**: 같은 알고리즘을 31행·94행에서는 "초등학교 방식", 280행에서는 "초등학교식"으로 부른다. `four-vs-three.svg`의 "초등학교식과 똑같다"까지 포함하면 두 표기가 본문과 그림에 섞여 있다.
- **recommendation**: 한쪽으로 통일한다. 짧고 반복해서 쓰기 좋은 "초등학교식"으로 모으고 31·94행을 고치는 편이 자연스럽다. 코드 주석(205행)은 규칙 대상이 아니므로 그대로 두어도 된다.
- **gate_effect**: warn

### 🟡 [L6] src/content/posts/karatsuba.md:1 — 노션 원본이 없는 글 (승인된 예외)

- **severity**: 🟡
- **source**: L
- **rule_id**: L6
- **location**: `src/content/posts/karatsuba.md:1`
- **quote**: not-recorded
- **message**: `notion-search`로 "카라츠바 / Karatsuba / 큰 수 곱셈 / n비트 곱셈"을 검색하고 `알고리즘 수업 정리` 하위를 확인한 결과, 카라츠바를 다룬 노션 페이지가 없다. `Matrix multiplication` 페이지는 나이브 → 분할 정복 8번 → Strassen 7번 → Recent Results로 끝나고, `Divide and Conquer` 페이지도 merge sort·heap sort·정렬 하한까지다. PS 하위 `문자열을 사용한 곱셈`은 초등학교식 $O(n^2)$ 구현이라 카라츠바가 아니다. 이 글은 전량 노션 밖 내용이다.
- **recommendation**: 사용자가 2026-07-27 대화에서 "이번에 예외로 써도 될 거 같아"라고 명시적으로 승인한 건이다. 조치는 필요 없고 기록만 남긴다. 향후 노션에 카라츠바 정리가 추가되면 본문과 대조해 한 번 맞춘다.
- **gate_effect**: warn

### 🟡 [L4] public/images/karatsuba/split-and-recombine.svg:60 — '제자리' 레이블 위치가 대상과 어긋난다

- **severity**: 🟡
- **source**: L
- **rule_id**: L4
- **location**: `public/images/karatsuba/split-and-recombine.svg:60`
- **quote**: `<text x="110" y="318" fill="#64748b" font-size="11">제자리</text>`
- **message**: 세 조각 행 중 앞의 두 행은 주석("·10²ᵐ (2m칸 위로)", "·10ᵐ (m칸 위로)")이 블록 **오른쪽**에 붙어 있는데, 셋째 행의 "제자리"만 x=110의 **왼쪽 빈 공간**에 있다. 같은 행이긴 하나 x₂y₂ 블록(x=430~750)과 320px 떨어져 있어, 무엇을 가리키는 말인지 즉시 읽히지 않는다.
- **recommendation**: 블록 오른쪽(x≈760)으로 옮겨 앞 두 행과 패턴을 맞춘다. 폭이 모자라면 "·10⁰ (제자리)" 대신 "제자리"만 두어도 754~790px에 들어간다.
- **gate_effect**: warn

### 🟢 [L7] src/content/posts/karatsuba.md:197 — 자릿수 어긋남 논거가 느슨하다

- **severity**: 🟢
- **source**: L
- **rule_id**: L7
- **location**: `src/content/posts/karatsuba.md:197`
- **quote**: "이 어긋남은 자리 하나에 그쳐 상수 배 안에 머물고, 점근 복잡도를 바꾸지 않는다."
- **message**: 결론은 옳다. 다만 근거 문장만 보면 "재귀 깊이마다 +1이 쌓이면 결국 커지지 않는가"라는 반문을 막지 못한다. 엄밀히는 점화식이 $T(n) = 2T(n/2) + T(n/2+1) + \Theta(n)$ 이 되고, 이 형태도 $\Theta(n^{\log_2 3})$ 으로 풀린다.
- **recommendation**: 실제 구현이 쓰는 처리를 한 줄 덧붙이면 반문이 닫힌다. 예: "$x_1+x_2$ 의 올림 비트를 따로 떼어 두면 재귀에 넘기는 값은 $m$ 자리로 유지되고, 떼어 낸 몫은 $\Theta(n)$ 짜리 보정 덧셈으로 흡수된다."
- **gate_effect**: info

### 🟢 [L4] public/images/karatsuba/four-vs-three.svg:70 — 박스 레이블과 P 기호가 그림 안에서 연결되지 않는다

- **severity**: 🟢
- **source**: L
- **rule_id**: L4
- **location**: `public/images/karatsuba/four-vs-three.svg:70`
- **quote**: `<text x="645" y="248" text-anchor="middle" fill="#fcd34d" font-size="11.5">가운데 항 = P₃ − P₁ − P₂  (곱셈 없이 뺄셈만)</text>`
- **message**: 세 박스는 x₁y₁ / x₂y₂ / (x₁+x₂)(y₁+y₂)로, 바로 아래 주석은 P₁·P₂·P₃로 적혀 있다. 순서는 본문 정의(정리 1)와 정확히 맞지만, 그림만 떼어 보면 어느 박스가 어느 P인지 대응이 드러나지 않는다.
- **recommendation**: 각 박스 레이블에 "P₁ = x₁y₁" 식으로 기호를 병기하거나, 박스 위에 작은 P₁/P₂/P₃ 캡션을 얹는다. 셋째 박스는 폭이 90px로 좁으니 위쪽 캡션 방식이 안전하다.
- **gate_effect**: info

### 🟢 [L3] src/content/posts/karatsuba.md:68 — '자리 곱셈' / '자리 곱' 혼용

- **severity**: 🟢
- **source**: L
- **rule_id**: L3
- **location**: `src/content/posts/karatsuba.md:68`
- **quote**: "자리 곱셈으로 세지 않는다" (68행) / "여기서는 자리 곱이 4번이라" (94행)
- **message**: 비용 단위를 31·37·68행에서는 "자리 곱셈", 94·191행에서는 "자리 곱"으로 부른다. 의미 혼동은 없다.
- **recommendation**: 단위를 처음 정의한 "자리 곱셈"으로 모으면 읽는 쪽이 같은 대상임을 다시 확인할 필요가 없다. 우선순위는 낮다.
- **gate_effect**: info

### 🟢 [L1] src/content/posts/karatsuba.md — 검토 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L1
- **location**: `src/content/posts/karatsuba.md`
- **quote**: not-recorded
- **message**: 검토 완료, 이슈 없음. 문두 접속어 0회(자매편 `matrix-multiplication.md`는 2회), 의존명사 '것' 3회(자매편 7회), 줄표 5회(자매편 5회)로 모두 기존 글 수준 이하다. 52행 "작은 곱들로"와 270행 "그 뒤의 기록들"은 자매편의 대응 표현을 그대로 따른 것이라 유지가 맞다. 경구식 마무리, 과한 비유, 대칭 문장 반복 없음. 어체는 ~다 평서체로 일관된다.
- **recommendation**: 조치 없음.
- **gate_effect**: info

### 🟢 [L2] src/content/posts/karatsuba.md — 검토 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L2
- **location**: `src/content/posts/karatsuba.md`
- **quote**: not-recorded
- **message**: 검토 완료, 이슈 없음. "무엇을 곱셈 한 번으로 세는가"로 비용 단위를 먼저 못 박고 → 4번 분할의 실패 → 필요한 값이 셋뿐이라는 관찰 → $(x_1+x_2)(y_1+y_2)$ 도입 순서로, 각 단계가 앞 단계의 결핍에서 나온다. 가운데 항의 $10^m$ 을 별도 경고 콜아웃으로 뽑은 처리가 흔한 오해를 앞서 막는다. 논리 도약이나 끊어야 할 장문 없음.
- **recommendation**: 조치 없음.
- **gate_effect**: info

### 🟢 [L5] src/content/posts/karatsuba.md:2 — 검토 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L5
- **location**: `src/content/posts/karatsuba.md:2`
- **quote**: "카라츠바 알고리즘 — n자리 곱셈은 n²보다 빠를 수 있다"
- **message**: 검토 완료, 이슈 없음. 제목이 글의 주장을 그대로 담고, description은 나이브 $\Theta(n^2)$ → 4번 분할 실패 → 3번 축소 → $\Theta(n^{1.585})$ 라는 실제 전개 순서와 일치한다. Strassen 대응을 언급해 시리즈 내 위치도 드러난다. `difficulty: 중급`은 본편과 같은 수준으로 적절하다.
- **recommendation**: 조치 없음.
- **gate_effect**: info

### 🟢 [L7] src/content/posts/karatsuba.md — 수치·복잡도 검산 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L7
- **location**: `src/content/posts/karatsuba.md`
- **quote**: not-recorded
- **message**: 검토 완료, 이슈 없음. 검산 내역 — 정리 1의 전개 $P_3-P_1-P_2 = x_1y_2+x_2y_1$ 성립 확인. $T(n)=4T(n/2)+\Theta(n) \Rightarrow \Theta(n^{\log_2 4})=\Theta(n^2)$, $T(n)=3T(n/2)+\Theta(n) \Rightarrow \Theta(n^{\log_2 3})$, $\log_2 3 = 1.58496\ldots$ 모두 맞다(마스터 정리 case 1, $\log_2 3 > 1$). 191행의 $n=1024$ 예시는 $1024^2 = 1{,}048{,}576 \approx 105$ 만, $3^{10} = 59{,}049$, 비 $17.76$ 배로 "열여덟 배 가까이"와 일치한다. Toom–3의 $\log_3 5 = 1.46497\ldots$, $n$ 비트 ↔ 자리 환산 계수 $\log_{10}2 = 0.30103$ 도 맞다. 연표(콜모고로프 1956 추측 / 1960 세미나·카라츠바 23세, Strassen 1969로 9년 차, Toom–Cook 1963, Schönhage–Strassen 1971, Harvey–van der Hoeven 2019)에 오류 없음.
- **recommendation**: 조치 없음.
- **gate_effect**: info

### 🟢 [L4] public/images/karatsuba/split-and-recombine.svg — 좌표·수치 대조 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L4
- **location**: `public/images/karatsuba/split-and-recombine.svg`
- **quote**: not-recorded
- **message**: 검토 완료, 이슈 없음(위 '제자리' 레이블 위치 건 제외). 눈금 4m~0을 640px에 균등 배치했을 때 $m$ = 160px이고, 세 블록의 실제 좌표가 자릿수 범위와 정확히 맞는다 — x₁y₁ 110~430 = [2m, 4m], 가운데 항 270~590 = [m, 3m], x₂y₂ 430~750 = [0, 2m]. 하단 결론 "T(n) = 4·T(n/2) + Θ(n) → Θ(n²)"가 본문 점화식과 일치한다.
- **recommendation**: 조치 없음.
- **gate_effect**: info

### 🟢 [L4] public/images/karatsuba/four-vs-three.svg — 본문 대조 완료, 이슈 없음

- **severity**: 🟢
- **source**: L
- **rule_id**: L4
- **location**: `public/images/karatsuba/four-vs-three.svg`
- **quote**: not-recorded
- **message**: 검토 완료, 이슈 없음(위 P 기호 병기 건 제외). 가지 수(4개/3개), 점화식, 지수(log₂4 = 2, log₂3 = 1.585…), 결과(Θ(n²), Θ(n¹·⁵⁸⁵))가 모두 본문과 일치한다. 좌우 대비 구도·색(적색 실패 / 녹색 성공)·위첨자 표기가 자매편 `seven-vs-eight.svg`의 규약을 따른다.
- **recommendation**: 조치 없음.
- **gate_effect**: info

---

요약: 🔴 0 · 🟡 3 · 🟢 8

---

## 후속 조치 (리뷰 이후 저자 패스에서 반영)

리뷰 자체는 수정하지 않았다. 아래는 리포트를 받은 뒤 같은 PR에서 적용한 내용이다.

| finding | 조치 |
|---|---|
| 🟡 L3 초등학교식 표기 | 31·94행을 "초등학교식"으로 통일. 코드 주석·SVG와 일치. |
| 🟡 L6 노션 원본 없음 | 조치 없음. 사용자 승인 예외로 기록만 유지. |
| 🟡 L4 '제자리' 레이블 | `split-and-recombine.svg` x=110 → x=764로 이동. 앞 두 행과 같이 블록 오른쪽에 붙였다. |
| 🟢 L7 자릿수 어긋남 | 197행에 올림 자리를 떼어 재귀를 $m$ 자리로 유지한다는 설명과, 보정 덧셈이 $\Theta(n)$ 항에 흡수된다는 근거를 추가. |
| 🟢 L4 P 기호 대응 | `four-vs-three.svg`의 주석을 P 기호 대신 실제 식 `(x₁+x₂)(y₁+y₂) − x₁y₁ − x₂y₂`로 바꿔 그림만으로 읽히게 했다. P₁~P₃ 캡션을 박스 위(y=174)에 얹는 안은 재귀 가지 선(y=142~180)과 겹쳐 폐기. |
| 🟢 L3 자리 곱셈 표기 | 94·191행을 "자리 곱셈"으로 통일. |
