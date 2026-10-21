schema_version: review-report/v2
target: robotics-vector-projection
generated_at: 2026-10-21
strict: true
sources: src/content/posts/robotics-vector-projection.md
summary: 🔴 0 · 🟡 6 · 🟢 9

## Findings

### 🟡 [L2] src/content/posts/robotics-vector-projection.md:105

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-vector-projection.md:105
- quote: $\mathbf a$를 원점에서 그리고, 그 끝점에서 $\ell$에 내린 수선의 발을 $F$라 한다.
- message: 정사영의 정의 전체가 "수선의 발"이라는 용어에 기대는데, 본문은 이 말을 설명하지 않는다. 기초 1·2에는 "수선을 내리면"까지만 나오고 "수선의 발"은 처음 나온다. 고교 수학을 잊은 독자에게 이 용어는 자명하지 않다.
- recommendation: 처음 쓰는 자리에 짧은 풀이를 붙인다. 예: "끝점에서 $\ell$에 수직으로 그은 선이 $\ell$과 만나는 점, 곧 수선의 발을 $F$라 한다."
- gate_effect: warn

### 🟡 [L3] src/content/posts/robotics-vector-projection.md:167

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/robotics-vector-projection.md:167
- quote: $\mathbf a$에서 정사영을 빼고 남은 부분을 $\mathbf r$이라 하자.
- message: 같은 $\mathbf r$을 "남은 부분"(109행 캡션, 167·206행), "ℓ에 수직인 부분"(181행), "나머지"(165행 절 제목, 183·197·199행, shadow.svg와 projection-lab.svg 범례)로 섞어 부른다. 스펙의 용어표는 7절 용어를 "나머지 $\mathbf r$"로 정했다. 그런데 본문은 "나머지"를 용어로 소개하지 않은 채 절 제목에서 먼저 쓴다. 같은 도판(shadow.svg)을 두고 캡션은 "남은 부분", 범례는 "나머지"라고 부른다.
- recommendation: 167행을 "정사영을 빼고 남은 부분을 **나머지**라 부르고 $\mathbf r$로 쓰자"로 바꾸고, 그 뒤로는 "나머지"로 통일한다(109행 캡션과 206행 callout 포함).
- gate_effect: warn

### 🟡 [L4] public/images/robotics-vector-projection/multiples.svg:8

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-vector-projection/multiples.svg:8
- quote: |<tspan font-weight="bold">a</tspan>|
- message: 본문은 벡터의 길이를 $\lVert\mathbf a\rVert$로 쓴다(기초 1과 같다). 57행은 바로 앞에서 $|k|$를 "수 $k$에서 부호를 뗀 크기"라고 정의했다. 그런데 바로 뒤의 도판 오른쪽 열(8·12·16·20행)은 "|a|", "2|a|", "0.5|a|", "|a|, 반대 방향"으로 같은 막대 기호를 벡터 길이에 쓴다. 54행 식 $|k|\,\lVert\mathbf a\rVert$와 나란히 읽으면 한 기호가 두 뜻이 된다. 실험 읽기 값의 이름도 같은 문제를 안고 있다(src/labs/vector-sum.js:33의 "|a| + |b|"·"|a + b|", src/labs/vector-projection.js:36의 "u = D / |D|"·"|a| cos φ"). 이 글의 SVG와 실험에서만 생기는 어긋남이다.
- recommendation: multiples.svg의 네 레이블을 ‖a‖, 2‖a‖, 0.5‖a‖, ‖a‖로 바꾼다. 실험 읽기 값의 이름도 ‖·‖로 맞추되, 실험 코드 리뷰 범위와 함께 처리한다.
- gate_effect: warn

### 🟡 [L4] public/images/robotics-vector-projection/projection-lab.svg:40

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-vector-projection/projection-lab.svg:40
- quote: a · u = 3 · 정사영 (1.8, 2.4)
- message: 141행은 "이 계산을 두 벡터의 내적이라 부르고 가운뎃점으로 쓴다"고 정의한다. 그런데 이 요약 줄은 같은 가운뎃점을 내적 기호로도 쓰고 항목 구분자로도 쓴다. 입문 독자는 "3 · 정사영 (1.8, 2.4)"을 3과 정사영의 곱이나 내적으로 읽을 수 있다. sum-lab.svg:38의 "a + b = (4, 3) · 길이 5"도 같은 구분자를 쓴다.
- recommendation: 구분자를 쉼표나 줄바꿈으로 바꾼다(예: "a · u = 3, 정사영 (1.8, 2.4)", "a + b = (4, 3), 길이 5"). 실험 코드가 요약 문자열을 만들므로(vector-projection.js:77, vector-sum.js:68) 정적 SVG와 함께 고친다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-vector-projection.md:117

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-vector-projection.md:117
- quote: $\varphi$의 크기가 $90^\circ$보다 작으면 $s>0$, $90^\circ$이면 $s=0$, $90^\circ$보다 크면 $s<0$이다.
- message: 111행은 φ를 "$\mathbf u$에서 $\mathbf a$까지 잰 각"이라고만 정의하고, 어느 범위에서 값을 고르는지는 정하지 않는다. 범위가 없으면 이 부호 판정은 틀릴 수 있다. φ=300°는 "크기가 90°보다 큰" 각이지만 cos 300°=0.5>0이다. 163행의 "단위원 위에서 가로 좌표가 0인 곳은 $\pm90^\circ$뿐"도 270°를 빼지 못하므로, "내적이 0일 때, 그리고 그때에만 수직"이라는 필요충분 증명이 범위를 전제로 깔고 있다. 스펙 54행은 "(−180°,180°]에서"라고 범위를 적었는데 본문에는 이 말이 빠졌다. 기초 2(이 브랜치 판)에서는 이 범위가 atan2가 돌려주는 값의 범위로만 나온다. 일반 각도의 대표값으로 쓰겠다는 약속은 아직 병합되지 않은 #246에만 있다. 둘째 단계의 "$-\alpha$" 논증은 반시계 방향을 양수로 재는 약속에 기대는데, 본문은 이 약속도 다시 밝히지 않는다. $s=\lVert\mathbf a\rVert\cos\varphi$ 식은 어떤 대표값을 골라도 맞는다. 문제가 되는 곳은 부호를 판정하는 문장과 "±90°뿐"이라는 문장이다.
- recommendation: 111행 정의를 "$\mathbf u$에서 $\mathbf a$까지 반시계 방향을 양수로 잰 각을 $\varphi$라 하고, $-180^\circ$보다 크고 $180^\circ$ 이하인 값으로 고른다"로 고친다. 163행에는 "이 범위에서"를 넣는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-vector-projection.md:129

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-vector-projection.md:129
- quote: $\mathbf e_y$와 $\mathbf u$도 서로에게서 잰 각이 부호만 다르므로, $\mathbf e_y$를 $\mathbf u$ 방향으로 정사영한 길이는 $\mathbf u$의 세로 성분 $u_y$다.
- message: 내적 공식의 둘째 항 $a_yu_y$는 이 한 문장에만 기댄다. $\mathbf e_x$ 경우는 각(−α, α), 짝수성 $\cos(-\alpha)=\cos\alpha$, "$\cos\alpha$=$\mathbf u$를 x축에 정사영한 길이=$u_x$"라는 연결을 하나씩 적었다. $\mathbf e_y$ 경우에는 두 각의 값($\mathbf u$→$\mathbf e_y$는 90°−α, $\mathbf e_y$→$\mathbf u$는 α−90°)이 없다. "$\mathbf u$를 $\mathbf e_y$ 방향으로 정사영한 길이는 $u_y$"(121행의 결과를 $\mathbf u$에 쓴 것)라는 연결 고리도 없다. 논증은 옳다($\mathbf u$=(0.6,0.8)이면 cos 36.87°=0.8=$u_y$). 다만 고교 수학을 잊은 독자가 빈 단계를 스스로 채워야 한다. 129행은 문장 여덟 개가 한 문단에 몰려 있어 이 압축이 더 눈에 띈다.
- recommendation: $\mathbf e_y$ 경우를 따로 한 문단으로 뺀다. 예: "$\mathbf e_y$는 $x$축에서 $90^\circ$ 돈 방향이므로 $\mathbf u$에서 $\mathbf e_y$까지 잰 각은 $90^\circ-\alpha$, $\mathbf e_y$에서 $\mathbf u$까지 잰 각은 $\alpha-90^\circ$다. 두 각의 코사인은 같고, $\mathbf u$를 $\mathbf e_y$ 방향으로 정사영한 길이는 앞 절에 따라 $u_y$다."
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-vector-projection.md:69

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-vector-projection.md:69
- quote: 이 식이 «끝점 좌표에서 시작점 좌표를 뺀다»는 규칙이다.
- message: 블로그 글 가운데 겹화살괄호 «»를 쓴 곳은 이 한 군데뿐이다. 기초 1은 같은 쓰임에 “ ”를 쓴다(“오른쪽으로 3, 위로 4”). 이것 말고는 문체가 깨끗하다. 문두 접속어는 "이제·또·먼저" 세 번뿐이고 모두 전환에 필요하다. 줄표는 제목에만 있고, 경구식 마무리나 과한 비유는 없다. '것'은 2회, '-들'은 1회("앞 글들처럼")만 나온다.
- recommendation: “끝점 좌표에서 시작점 좌표를 뺀다”로 바꿔 시리즈와 맞춘다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-vector-projection.md:89

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-vector-projection.md:89
- quote: 축을 돌리면 $\mathbf e_x$와 $\mathbf e_y$도 함께 돌지만, 두 단위벡터의 실수배를 더한다는 모양은 그대로 남는다.
- message: 돌린 두 단위벡터로도 모든 벡터를 나타낼 수 있다는, 근거 없는 일반 주장이 본문에 단정문으로 들어가 있다. "모양"이 무엇을 가리키는지도 흐리다. 다음 글의 주제를 예고하는 문장이다.
- recommendation: 예고임을 드러낸다. 예: "축을 돌려도 돌아간 두 단위벡터의 실수배를 더해 점을 나타낼 수 있는지는 다음 글에서 확인한다." 아니면 이 문장을 "이어지는 글" callout으로 옮긴다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-vector-projection.md:129

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-vector-projection.md:129
- quote: **둘째, 길이 1인 두 화살표는 서로에게 같은 길이의 그림자를 드리운다.**
- message: 스펙의 용어 약속("그림자"는 직관 설명에만 쓰고 정의는 수선의 발로)과 달리, 증명 단계의 굵은 명제에 일상어 "그림자"가 들어갔다. 바로 뒤 본문은 "정사영한 길이"로 적는다. 첫째 단계 제목은 "정사영의 길이도"로 적었으므로 두 단계 제목의 말도 어긋난다.
- recommendation: "둘째, 길이 1인 두 화살표는 서로의 방향으로 같은 길이만큼 정사영된다"처럼 정사영 용어로 쓴다. 도판 제목의 "그림자"는 직관용이므로 그대로 둬도 된다.
- gate_effect: info

### 🟢 [L4] public/images/robotics-vector-projection/shadow-signs.svg:4

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/robotics-vector-projection/shadow-signs.svg:4
- quote: φ에 따라 정사영의 부호가 바뀐다
- message: 본문은 정사영을 화살표 $\overrightarrow{OF}$로, 부호가 있는 값을 "정사영의 길이 $s$"로 나눠 정의한다(105·107행). 도판 제목은 부호를 화살표에 붙였다. 캡션(119행)은 "정사영의 길이 s가 양수"로 바르게 적었다.
- recommendation: 제목을 "φ에 따라 정사영 길이 s의 부호가 바뀐다"로 고친다.
- gate_effect: info

### 🟢 [L4] src/content/posts/robotics-vector-projection.md:197

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/robotics-vector-projection.md:197
- quote: 그다음 $\mathbf a$를 직선 위에 올려 보자.
- message: 정적 SVG 8장의 좌표를 모두 다시 계산했고 본문과 캡션에 맞는다. sum (3,1)/(1,2)/(4,3), 점선 평행사변형, multiples (4,2)/(1,0.5)/(−2,−1), unit-axes, shadow F(1.8,2.4)·r(−0.8,0.6)·φ호 18.43°, shadow-signs 50°/90°/140°의 s 값, mutual-shadow α=40°·cos 40° 두 그림자·20° 이등분선, 두 실험 첫 화면이 모두 일치했다. 실험 안내도 스펙 범위 안에서 해 볼 수 있다. 실험 1에서 $\mathbf b$=(1.5,0.5) 또는 (3,1)이면 합 (6,2)가 ±6 판 안에 있고, $-\mathbf a$=(−3,−1)도 입력 범위 안이다. 실험 2에서 $D$=(3,−1)이면 정사영이 사라진다. 남은 지적은 사소한 세 가지다. ① 이 문장은 $D$가 처음 자리일 때($\mathbf a$=(1.5,2))나 수직 자리일 때($\mathbf a$=(3,−1))만 0.5 격자로 해 볼 수 있다. 앞 단계에서 $D$를 (3.5,4) 같은 곳에 두면 원점 말고는 직선 위의 격자점이 없다. ② 93행은 보라 마름모 손잡이를 "보라 점"이라 부르고, 195행은 흰 마름모를 "흰 마름모 $D$"라 부른다. 정적 그림에는 "D" 레이블이 없다. ③ 실험의 φ 읽기 값은 0°–180°의 크기로 나오는데(모델 주석), 본문의 φ는 부호가 있는 각이라고 독자에게 알리지 않는다. 렌더는 resvg 근사로만 봤고 브라우저에서는 관측하지 않았다.
- recommendation: "예를 들어 $D$를 처음 자리에 두고 $\mathbf a$를 (1.5, 2)로"처럼 해 볼 수 있는 예를 준다. 93행을 "보라 마름모"로 바꾸거나 두 손잡이의 이름을 같은 방식으로 맞춘다. "읽기 값의 φ는 부호를 뗀 크기로 보인다"는 구절을 하나 보탠다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-vector-projection.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-vector-projection.md:2
- quote: title: "벡터의 덧셈과 정사영 — 화살표를 잇고 한 방향에 그림자 내리기"
- message: 제목과 description은 덧셈, 실수배, 정사영, 내적, 수직인 나머지를 잘 대표하고 시리즈의 제목 형식과도 맞다. 사소한 어긋남이 둘 있다. 부제의 "한 방향에"는 절 제목과 shadow.svg 제목의 "한 방향으로"와 조사가 다르다. description의 "길이 1인 방향 u"는 방향에 길이를 붙인 표현이다. 본문은 "길이 1인 벡터 u"라고 쓴다.
- recommendation: 부제를 "한 방향으로 그림자 내리기"로 맞추고, description을 "길이 1인 벡터 u의 방향으로 내린 정사영의 길이는…"으로 고친다.
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-vector-projection.md:183

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-vector-projection.md:183
- quote: 레일을 따라서만 움직이게 만든 관절은 이 나머지가 0이 되도록 부품을 묶는다.
- message: approved extension. 승인 자료(스펙의 본문 순서·증명 의무 표·provenance)와 비공개 추출본을 직접 대조했다. 기구학 슬라이드 4장은 "부품 원점의 세계 위치 + 회전한 local 점"으로 덧셈을 쓴다. 12장의 축 이동량 s=u_x(p_x2−p_x1)+u_y(p_y2−p_y1)와 "법선 방향 이동만 막는" n·Δ=0, 27장의 "두 투영이 0이면 축 방향에만 남는다"는 레일 해석에 그대로 쓰였다. 선형대수 PDF 2–5·20·133–134·137·149–151쪽의 내용(덧셈·상수배, 표준 내적, ‖ca‖=|c|‖a‖, 정사영과 수직성, 가장 가까운 점)도 확인했다. 글은 스펙의 9절 순서와 주장을 그대로 따른다. 기하에서 성분 공식을 유도하는 순서, 예시 값, 회전 논증은 provenance에 작성자 추가로 밝혀져 있다. 슬라이드 12의 상대 회전 구속(θ2−θ1−δ=0)은 생략했다. 스펙에 "관절 구속식은 다루지 않는다"고 범위가 적혀 있고 글이 이와 모순되지 않는다. 본문에는 비공개 원천을 가리키는 서술이 없다(강의·노트·PPT·PDF·원문을 grep해 0건). 공개 참고 자료 두 곳의 설명이 실제 OpenStax §2.1과 §2.3 내용과 맞는다는 것도 확인했다. 다만 사용자의 2026-10-15 시리즈 계획 원문은 스펙 인용으로만 봤다.
- recommendation: 현재 범위를 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-vector-projection.md:127

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-vector-projection.md:127
- quote: 두 화살표를 이어 붙인 그림을 통째로 돌리면 이어 붙인 모양도 그대로 돌아가므로, 돌린 그림에서도 $\mathbf a+\mathbf b$는 돌린 $\mathbf a$와 돌린 $\mathbf b$를 이어 붙인 화살표다.
- message: 덧셈과 실수배에 대한 성질(정사영 길이가 더해지고 실수배된다)은 닫혔다. 실수배 쪽(길이 비율과 같은/반대 방향 보존)과 셋째 단계의 조합도 옳다. 다만 덧셈 쪽에는 핵심 전제가 하나 숨어 있다. "$\mathbf a$의 머리에 붙인 $\mathbf b$를 돌린 화살표가 원점에서 그린 $\mathbf b$를 돌린 화살표와 같은 벡터"라는 사실이다. 111행에 적은 보존 목록(길이·각도·수직)에서 이 사실을 끌어내는 연결이 본문에 없다. 스펙이 이 전제를 받아들였으므로 증명이 빠진 것은 아니고, 전제를 명시하면 좋은 수준이다.
- recommendation: 한 구절을 보탠다. 예: "돌리면 모든 화살표가 같은 각만큼 돌므로, 평행이동한 두 화살표는 돌린 뒤에도 평행이동한 관계, 곧 같은 벡터다."
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-vector-projection.md:206

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-vector-projection.md:206
- quote: 영벡터가 아닌 두 벡터는 내적이 0일 때에만 수직이다.
- message: 본문 163행은 필요충분 조건("0일 때, 그리고 그때에만")을 증명했다. 핵심 정리의 "0일 때에만"은 글자 그대로 읽으면 "수직이면 내적 0"이라는 한 방향만 말한다. 요약이 증명한 것보다 약하다.
- recommendation: "영벡터가 아닌 두 벡터는 내적이 0일 때, 그리고 그때에만 수직이다"로 본문과 맞춘다.
- gate_effect: info

## 후속 처리

2026-10-21, 작성자가 같은 세션에서 반영했다. 위 finding의 줄 번호는 리뷰 시점의 글을 가리킨다. 반영한 뒤 확인한 결과는 다음과 같다.

- 결정적 검사: 지적 0건
- `npm run test:js`: 68/68
- 빌드: dev 서버를 피해 격리된 복사본에서 실행. 151쪽 생성, 본문 검사 통과, KaTeX 오류 0

### 글 리뷰 반영

- 🟡 [L7] 117행: φ를 "u에서 a까지 반시계 방향을 양수로 잰 각"으로 정의했다. 같은 방향의 각은 360°씩 다른 여러 값이 있어도 cos는 같다는 점을 밝혔다. 부호를 따질 때는 (−180°, 180°]의 값을 고른다고 적었다. 163행의 "±90°뿐"도 그 범위 안의 말로 고쳤다.
- 🟡 [L7] 129행: $\mathbf e_y$ 경우를 따로 한 문단으로 뺐다. 두 각 90°−α와 α−90°, 그리고 "u를 $\mathbf e_y$ 방향으로 정사영한 길이 = $u_y$"(앞 절의 축 방향 결과)라는 연결을 적었다.
- 🟡 [L4] multiples.svg: 길이 레이블 네 개를 ‖a‖로 바꿨다. 실험 읽기 값의 이름도 ‖a‖ + ‖b‖, ‖a + b‖, u = D / ‖D‖, ‖a‖ cos φ로 바꿨다.
- 🟡 [L4] 두 실험의 요약 줄: 구분자를 가운뎃점 대신 쉼표로 바꿨다. 런타임 문자열, 정적 SVG, 테스트를 함께 고쳤다.
- 🟡 [L2] 105행: "끝점에서 ℓ에 수직으로 그은 선이 ℓ과 만나는 점을 F라 한다. 이 점을 수선의 발이라고 부른다"로 풀었다.
- 🟡 [L3] 167행: "**나머지**라 부르고 r로 쓰자"로 용어를 들였다. 109행 캡션, 181행, 핵심 정리, description을 "나머지"로 맞췄다.
- 🟢 [L7] 127행: 돌린 뒤에도 평행이동한 두 화살표는 같은 벡터라는 전제를 한 문장으로 적었다.
- 🟢 [L7] 206행: 핵심 정리를 "내적이 0일 때, 그리고 그때에만 수직이다"로 본문에 맞췄다.
- 🟢 [L2] 89행: 다음 글의 예고로 바꿨다("같은 방식으로 점을 나타낼 수 있는지는 다음 글에서 확인한다").
- 🟢 [L4] 197행: 해 볼 수 있는 예를 넣었다($D$를 (3,4)로 되돌리고 $\mathbf a$를 (1.5, 2)로). 실험 1에도 (1.5, 0.5)를 넣었다. 손잡이 이름을 "보라 마름모"로 맞췄고, 읽기 값의 φ가 부호를 뗀 크기라는 구절을 더했다.
- 🟢 [L4] shadow-signs.svg: 제목을 "φ에 따라 s의 부호가 바뀐다"로 바꿨다. "정사영 길이 s의"까지 넣으면 폭 400을 넘어서 줄였다. s는 캡션이 정사영의 길이로 정의한다.
- 🟢 [L3] 129행: 둘째 단계 제목을 "서로의 방향으로 같은 길이만큼 정사영된다"로 바꿨다.
- 🟢 [L1] 69행: «»를 “ ”로 바꿨다.
- 🟢 [L5] 2·4행: 부제를 "한 방향으로"로 바꿨다. description은 "길이 1인 벡터 u의 방향으로"와 "그 나머지는"으로 고쳤다.

### 실험 코드 리뷰 반영

같은 브랜치의 실험 코드를 별도 리뷰어가 검토했다(🔴 0, 🟡 7, 🟢 7). 리뷰어는 상태 전체 스윕, DOM 스텁 마운트, 변이 시험을 썼다. 반영한 내용은 다음과 같다.

- u 화살표가 O 글자를 지났다(7,098상태). 오른쪽이 O 라벨을 지나면 왼쪽 법선 쪽에 그린다.
- 방향키로 D가 0을 건너지 못했다. 원점에 닿으면 같은 방향으로 한 칸 더 간다.
- 끌기에서 D가 한 박자 늦었다. 끌기는 두 좌표를 한꺼번에 적용하고, 합친 결과가 원점일 때만 거부한다.
- 겹친 손잡이는 맨 위의 것만 잡혔다. 포인터에서 가장 가까운 손잡이를 고르는 공용 함수를 더했다. 거리가 같으면 선택된 쪽을 고른다.
- a와 b가 같은 방향이면 흰 합 화살표가 묻혔다. 합을 6px로 굵게 아래에 깔고 화살촉을 16px로 키웠다.
- 직각 표시가 a 점에 가려졌다. 임계를 14px에서 18px로 올렸다.
- 모델 식을 되풀이하던 검사를 그림에서 읽은 기하로 바꿨다.
  - 평행사변형의 마주 보는 변
  - 직각 표시 두 다리의 방향과 길이, 손잡이에 가리지 않음
  - u의 평행·간격·방향, O 라벨과 눈금 숫자 회피
  - φ의 범위, 화살촉 규칙
  - marker 크기와 `HEAD_MIN`의 관계(SVG에서 읽음)
- 🟢 일부도 반영했다.
  - 런타임이 화살촉 참조를 `data-marker`에서 읽는다.
  - s≈0일 때 다리 방향이 뒤집히지 않도록 허용 오차를 두었다.
  - 입력 이름("성분", "좌표")을 정리하고, 손잡이 링 반지름을 기존 실험과 같은 17로 맞췄다.

리뷰어의 변이 목록을 새 코드의 고정점에 맞게 옮겼다. 새 동작(쪽 고르기, 0 건너기, 대각선 끌기)에 대한 변이도 더해 27개를 다시 돌렸고, 모두 테스트가 잡았다. 처음 돌렸을 때는 두 개가 살아남았다. 하나는 대각선 끌기를 한 축씩 적용하는 변이이고, 다른 하나는 발 F를 반올림하지 않는 변이다. 이 둘을 잡는 검사를 더했다. 바뀐 규칙 두 가지(겹치는 손잡이, `data-marker`)는 `docs/design/SVG_LABS.md`에 적었다. 실험 동작 변경은 스펙의 실험 절에도 반영했다.

브라우저 렌더, 실기기 터치, 인쇄는 작성자도 두 리뷰어도 보지 못했다. 그림은 resvg 래스터로만 근사 확인했다.
