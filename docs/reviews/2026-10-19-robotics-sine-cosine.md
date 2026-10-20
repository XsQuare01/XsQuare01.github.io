schema_version: review-report/v2
target: robotics-sine-cosine
generated_at: 2026-10-19
strict: true
sources: src/content/posts/robotics-sine-cosine.md
summary: 🔴 0 · 🟡 8 · 🟢 6

## Findings

### 🟡 [L1] src/content/posts/robotics-sine-cosine.md:43

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/robotics-sine-cosine.md:43
- quote: 곧 $\sin30^\circ=\tfrac12$이고, 피타고라스 정리로 밑변은 $\sqrt{1-\tfrac14}=\tfrac{\sqrt3}{2}\approx0.866$이다.
- message: 바꿔 말하기 표지 '곧'이 17·37·41(두 번)·43·85행에 여섯 번 나오고, 41행은 한 문단 안에서 두 번 쓴다. 43행의 '곧'은 문두 접속어 자리다. 청유형 보조 용언 '~해 보자'도 41·43·67·85·112(두 번)·120행에 일곱 번 반복된다. 정본 가이드의 문두 접속어 최소화·동어 중복·보조 용언 항목에 걸린다. 그 밖의 표지는 깨끗하다(줄표는 제목에만, '-들' 0회, 의존명사 '것' 0회, 굵게 6곳은 모두 용어 도입).
- recommendation: 43행은 "…맞은편 변이 정삼각형 한 변의 절반이므로 $\sin30^\circ=\tfrac12$이다."처럼 앞 문장에 잇고, 37행 "곧 앞 글의 위치벡터다"는 "앞 글에서 말한 위치벡터다", 41행 둘째 '곧'은 "예를 들어"로 바꿔 '곧'을 두세 번으로 줄인다. '~해 보자'는 실험 안내(112행)만 남기고 41·67·120행은 평서로 쓴다(예: "이 식이 모든 각도에서 맞는지 따진다").
- gate_effect: warn

### 🟡 [L3] src/content/posts/robotics-sine-cosine.md:120

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/robotics-sine-cosine.md:120
- quote: 앞 글의 변위 $(3,4)$를 끝점으로 놓으면 $L=5$다.
- message: 스펙 36행과 앞 글은 점의 두 수를 '좌표', 화살표의 두 수를 '성분'으로 갈라 쓰고, 앞 글의 논지가 바로 위치와 변위의 구분이다. "변위를 끝점으로 놓는다"는 변위(화살표)를 점처럼 다뤄 그 구분을 흐린다. 앞 글 43행의 연결("(0,0)에서 (3,4)로 향하는 화살표도 변위 (3,4)를 나타낸다")과 이 글 37행(위치벡터의 성분 = 끝점 좌표)을 거치면 같은 내용을 용어를 섞지 않고 말할 수 있다. 이 글의 나머지 용례(37·39·65·67·85·110·114행)는 좌표와 성분을 바르게 갈라 쓴다.
- recommendation: "앞 글의 변위 $(3,4)$를 원점에서 그리면 화살표의 끝점은 $(3,4)$이고, 길이는 $L=5$다."처럼 화살표를 원점에 놓는 단계를 밝힌다.
- gate_effect: warn

### 🟡 [L4] public/images/robotics-sine-cosine/quadrants.svg:20

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-sine-cosine/quadrants.svg:20
- quote: <text x="200" y="252" fill="#fbbf24" font-size="17" text-anchor="middle">−1</text> … <text x="217" y="251" fill="#e2e8f0" font-size="20" text-anchor="end">O</text>
- message: 원점 이름 "O"(20px, 오른쪽 끝 x=217)와 가로 성분 라벨 "−1"(17px, 가운데 x=200)이 거의 같은 기준선(251·252)에 놓인다. 일반 sans-serif 글리프 폭으로 환산하면 "O"는 대략 x 202–216, "−1"은 x 190–210을 차지해 가로로 6–8px, 세로로 y 240–251이 겹친다. "−1"의 '1'이 "O" 왼쪽에 파고들어 겹친 글자나 "−1O"로 보일 가능성이 높다. 앞 편 리뷰가 displacement-lab.svg에서 지적한 "−1O" 붙음과 같은 유형이다. 리뷰어는 브라우저로 보지 못했고 좌표와 글리프 폭 계산으로 판단했다. 글꼴에 따라 몇 px 달라져도 간격이 음수라 겹침은 남는다.
- recommendation: "−1"을 노란 선 위 삼각형 안쪽(예: x=200, y=222)으로 올린다. 그 자리는 막대(x=190–210에서 y≈161–195)와도 떨어져 있고, "O"는 다른 도판처럼 원점 왼쪽 아래에 그대로 둘 수 있다.
- gate_effect: warn

### 🟡 [L4] public/images/robotics-sine-cosine/unit-circle.svg:16

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-sine-cosine/unit-circle.svg:16
- quote: <text x="208" y="366">3π/2</text> … π/2 = 90°, π = 180°, 3π/2 = 270°
- message: 본문 17행은 아래쪽 방향을 "$\theta=-90^\circ$"로 정하고, 사분면 표(103행)와 atan2 범위(126행)도 −180°–180° 규약을 쓴다. 바로 다음 도판은 같은 아래쪽 자리를 3π/2 = 270°로 적는다. 270°와 −90°가 같은 방향이라는 설명은 106행(제3사분면)과 134행(233.13°)에서야 간접적으로 나와, 첫 도판에서 독자는 한 방향에 두 값이 붙는 이유를 알 수 없다. 스펙 74행이 0·π/2·π·3π/2 표시를 정했으므로 도판은 스펙대로지만 본문 규약과 어긋난다. 나머지 값은 맞다(원점 (200,215), 단위 130px에서 끝점 (312.6,150) = 130·(cos30°, sin30°), 호 끝 (232.9,196)은 반지름 38·30°).
- recommendation: 아래쪽 라벨을 "−π/2"로 바꾸고 캡션을 "π/2 = 90°, π = 180°, −π/2 = −90°"로 하거나, 3π/2를 유지한다면 캡션에 "3π/2 = 270°는 −90°와 같은 방향"을 덧붙인다. 스펙 74행도 함께 고친다.
- gate_effect: warn

### 🟡 [L6] src/content/posts/robotics-sine-cosine.md:25

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/robotics-sine-cosine.md:25
- quote: 이 글은 읽기 쉽게 도로 계산하고, 필요한 곳에 라디안을 함께 적는다.
- message: actual mismatch — 국소. 승인 자료(포스트 스펙, 기구학 PPT 1·4·19·20·36장, 앞 글)와 실제로 대조했다. 절 순서 1–7, 예시 값($L=2$, $30^\circ$·$120^\circ$·$-30^\circ$, $(3,4)$/$(-3,-4)$), 스펙 강한 주장 표의 네 의무, 원점 처리, PPT 19장의 $L_c\cos\alpha$·$L_c\sin\alpha$ 끝점 계산과 36장의 atan2(y값, x값)·사분면 설명이 본문과 맞고, 회전행렬을 다루지 않는 범위 축소도 스펙에 적혀 있다. 한 가지가 다르다. 스펙 32행은 "본문 계산은 도로 하고 라디안 대응값을 함께 적는다"고 정했고 계산표 64행은 $\operatorname{atan2}(4,3)\approx0.927$ rad를 적었는데, 본문은 25행의 $\pi/6$ 말고는 라디안 값을 쓰지 않는다(53.13°, 120°, −126.87° 모두 도만). 25행이 스스로 약속한 "필요한 곳에 라디안을 함께"도 지켜지지 않는다. PPT는 각을 모두 rad로 정의하므로(19장 α, 36장 α) 다음 편으로 넘어갈 때 필요한 연결이다.
- recommendation: 129행에 $\approx0.927$ rad와 $-126.87^\circ\approx-2.214$ rad를 덧붙이고, 88행의 $120^\circ$에 $2\pi/3$를 병기한다. 병기하지 않기로 했다면 25행의 약속을 지우고 스펙 32행을 고친다.
- gate_effect: warn

### 🟡 [L6] src/content/posts/robotics-sine-cosine.md:148

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/robotics-sine-cosine.md:148
- quote: 다음 글에서는 화살표 두 개를 더하는 방법과, 화살표 하나를 다른 방향으로 투영하는 방법을 다룬다.
- message: actual mismatch — 국소. 스펙 25행은 이어지는 글 callout을 "기초 3: 막대 끝에 막대를 하나 더 붙이면 두 변위를 어떻게 더하는가"로 정했다. 본문은 여기에 '투영'을 더해 다음 편 범위를 약속한다. 스펙이 provenance로 든 2026-10-15 시리즈 계획은 리뷰 자료에 없어 대조하지 못했고, 이 편 스펙에는 투영에 관한 기록이 없다. 승인만 빠진 추가로 본다. 글의 구조와 논증에는 영향이 없다.
- recommendation: 기초 3 범위에 투영이 확정됐다면 스펙 25행에 그 근거를 적고, 아니면 callout을 스펙 문구(두 변위를 더하는 방법)로 줄인다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-sine-cosine.md:122

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-sine-cosine.md:122
- quote: $x=L\cos\theta$와 $y=L\sin\theta$를 나누면 $\dfrac{y}{x}=\dfrac{\sin\theta}{\cos\theta}$이고 … 나눗셈을 하면 $x$와 $y$의 부호가 지워진다.
- message: y/x 단계에 부정확이 둘 있다. ① 나눗셈의 전제 $x\neq0$이 빠졌다. $\theta=\pm90^\circ$이면 $x=0$이라 $y/x$와 $\tan\theta$가 정의되지 않는다. 이는 $y/x$만으로 각을 정할 수 없는 둘째 이유이고 atan2가 필요한 이유이기도 하다. ② 126행 "부호가 지워진다"는 말 그대로는 틀린다. $y/x$의 부호는 $x$와 $y$의 부호가 같은지 다른지를 남긴다($-4/3$이면 제2 또는 제4사분면). 사라지는 것은 $(x,y)$와 정반대 방향의 $(-x,-y)$를 가르는 정보다. 122행의 반례 자체는 옳다($-4/-3=4/3$).
- recommendation: 122행을 "$x\neq0$일 때 … 나누면"으로 고치고 "$x=0$인 $\pm90^\circ$에서는 이 비가 정의되지 않는다"를 한 문장 더한다. 126행은 "나눗셈을 하면 $x$와 $y$의 부호를 함께 바꾼 점, 정반대 방향의 점과 구별이 사라진다"처럼 쓴다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-sine-cosine.md:136

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-sine-cosine.md:136
- quote: 프로그래밍 언어의 atan2는 이때도 0 같은 값을 돌려주지만, 그 값에 방향의 뜻은 없다.
- message: 결론(그 값에 방향의 뜻은 없다)은 옳지만 앞부분이 일반화되어 있다. C11 7.12.4.4는 두 인자가 모두 0이면 정의역 오류가 일어날 수 있다고 해 값 반환을 보장하지 않고, 반환 범위를 [−π, +π]로 적는다. IEC 60559 부록(F.10.1.4)과 JavaScript Math.atan2(ECMA-262)는 오류 없이 값을 주지만 부호 있는 0에 따라 atan2(+0,+0)=+0, atan2(+0,−0)=+π, atan2(−0,−0)=−π로 0이 아닌 ±180°가 나오기도 한다(리뷰에서 Python math.atan2로 0.0, π, −π를 확인). 같은 이유로 126행의 "−180°보다 크고"는 수학적 정의로는 맞지만 부동소수점에서는 atan2(−0, −1) = −π가 나온다. 입문 글의 핵심을 해치지 않는 국소 부정확이다.
- recommendation: "많은 언어의 atan2는 이때도 오류 없이 0이나 ±180° 같은 값을 돌려주지만, 그 값에 방향의 뜻은 없다."처럼 한정하거나 "어떤 값을 돌려주든 방향의 뜻은 없다"로 줄인다. 126행은 그대로 두되 필요하면 "수학적으로는"을 붙인다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-sine-cosine.md:134

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-sine-cosine.md:134
- quote: 앞의 실험에서 끝점을 끌면 실험도 이 함수로 각도를 다시 구한다.
- message: 한 문장에 '실험'이 두 번 나온다(동어 중복).
- recommendation: "앞의 실험도 끝점을 끌면 이 함수로 각도를 다시 구한다."
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-sine-cosine.md:116

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-sine-cosine.md:116
- quote: 앞 절의 $L=2$, $\theta=30^\circ$ 계산과 같은 값이다.
- message: $L=2$, $\theta=30^\circ$ 계산은 바로 앞 절(부호는 사분면이 정한다)이 아니라 두 절 앞의 「길이 L인 막대」(75–79행)에 있다. 그 밖의 흐름(도입 질문, 정의, 일반화와 증명, 부호, 실험, 역문제, 정리)은 스펙 순서대로이고 빠진 전제는 L7 행에 적은 것 말고는 없다.
- recommendation: "앞에서 구한 $L=2$, $\theta=30^\circ$의 끝점 $(\sqrt3,1)$과 같은 값이다."
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-sine-cosine.md:41

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-sine-cosine.md:41
- quote: 막대가 첫 번째 사분면, 곧 가로·세로 좌표가 모두 양수인 영역에 있으면
- message: 41행은 '첫 번째 사분면'이라 쓰고 정의(97행)와 표(101행)는 '제1사분면'이라 쓴다. 정의 전에 풀이를 붙여 먼저 쓴 것은 괜찮지만 이름이 다르다. 좌표/성분, 끝점, 막대, 단위원 같은 나머지 용어와 ~다 평서체는 글 전체와 앞 편에서 일관된다. 실험 UI 문구의 합쇼체는 앞 편 실험과 같은 관례다.
- recommendation: 41행을 "제1사분면"으로 맞춘다.
- gate_effect: info

### 🟢 [L4] public/images/robotics-sine-cosine/scale.svg:23

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/robotics-sine-cosine/scale.svg:23
- quote: U = (cos 30°, sin 30°) ≈ (0.87, 0.5)
- message: 도판 좌표를 각 원점과 단위로 환산해 본문과 대조했다. scale.svg(원점 (50,300), 140px): U (171.2,230) → (0.866, 0.5), P (292.5,160) → (1.732, 1). quadrants.svg(원점 (230,230), 60px): P (170,126.1) → (−1, 1.732), 호 끝 (213,200.6)은 반지름 34·120°, 네 모서리 부호 맞음. inverse.svg(원점 (200,230), 36px): (308,86) → (3,4), (92,374) → (−3,−4), 점선은 기울기 4/3으로 원점을 지남, 파란 호 끝 (224,198)은 반지름 40·53.13°, 노란 호 끝 (168.8,271.6)은 반지름 52·−126.87°(sweep 1, 시계 방향). rod-lab.svg는 모델 layout(initialState())를 손으로 계산해 끝점 (303.9,190), 단위원 점 (252,220), 호 끝 (231.2,232), 라벨 P(325,186)·θ(244,245)·L cos θ(252,294)·L sin θ(314,227)가 모두 일치했고, 요약 "(1.73, 1)"과 본문 116행도 맞는다(node --test test/rod-angle.test.mjs test/lab-loader.test.mjs 14/14 통과). 캡션과 alt의 색 설명(노란 실선 = 가로 성분, 초록 점선 = 세로 성분)도 다섯 도판 모두 맞다. 참고 두 가지: scale.svg는 0.87, 본문 46행은 0.866으로 반올림 자릿수가 다르다. inverse.svg의 "53.13°" 라벨(가운데 x=256) 왼쪽 아래 끝이 반지름 40 호(x≈233에서 y≈208)에 거의 닿는다. 리뷰어는 브라우저 렌더를 보지 못했다.
- recommendation: 반올림 자릿수를 한쪽으로 맞춘다. "53.13°" 라벨을 x=262 정도로 옮기면 호와 떨어진다. 다섯 도판을 브라우저에서 한 번 확인한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-sine-cosine.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-sine-cosine.md:2
- quote: 사인과 코사인 — 각도와 길이로 막대 끝을 찾기
- message: 검토 완료, 이슈 없음. 제목은 순방향 질문(각도·길이 → 끝점)을, description은 단위원 정의·일반식·atan2 역문제까지 본문 결론을 대표한다. 앞 편과 같은 「주제 — 질문」 형식이다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-sine-cosine.md:41

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-sine-cosine.md:41
- quote: 단위원 정의는 직각삼각형으로 그릴 수 없는 각도, 곧 $90^\circ$보다 큰 각과 음수 각에도 값을 준다.
- message: 리뷰에서 다시 계산했다. $\pi/6\approx0.5236$, $\sin30^\circ=\tfrac12$와 $\sqrt{1-\tfrac14}=\tfrac{\sqrt3}{2}\approx0.866$, $\tfrac34+\tfrac14=1$, $(\sqrt3,1)\approx(1.73,1)$, $120^\circ$($60^\circ$ 점 $(\tfrac12,\tfrac{\sqrt3}{2})$의 y축 반사 → $(-\tfrac12,\tfrac{\sqrt3}{2})$, $L=2$면 $(-1,\sqrt3)$), $-30^\circ$($(\sqrt3,-1)$), atan2 $53.1301^\circ$·$-126.8699^\circ$·$233.13^\circ$, $(3,4)$의 길이 5가 모두 맞다. $\cos^2\theta+\sin^2\theta=1$은 정의상 거리 1인 점에 앞 글의 길이 공식을 써서 모든 θ에 대해 닫힌다. 모든 θ에 대한 $(L\cos\theta,L\sin\theta)$ 논증(67–73행)도 닫혔다. 끝점을 반직선 OU 위·거리 L인 점으로 규정하고, 양수 L배가 두 좌표를 같은 비율로 늘리고 부호를 지켜 방향을 보존함을 들고, 거리 계산에 위 항등식을 쓰고, 반직선 위 거리 L인 점의 유일성으로 마무리한다. 사분면 표는 열린 구간 넷과 축 위 각(0°, ±90°, 180°)을 합쳐 (−180°, 180°]를 빠짐없이 겹침 없이 덮고, −180° 대신 180°를 쓴 경계가 atan2 범위와 맞는다. 참고 두 가지: ① 41행의 '곧' 목록은 직각삼각형 정의가 닿지 않는 각을 다 들지 못한다. 0°와 90°도 직각삼각형의 예각이 될 수 없고, 실험 질문(112행)의 답인 '가로 성분이 0이 되는 각'이 바로 90°다. ② 43행 "정삼각형을 반으로 자른 모양이라"는 근거 없이 단정한다. 같은 삼각형 둘을 맞붙이면 세 각이 60°인 정삼각형이 된다는 한 마디가 있으면 논증이 닫힌다.
- recommendation: 41행을 "직각삼각형으로 그릴 수 없는 각도, 예를 들어 $0^\circ$와 $90^\circ$, $90^\circ$보다 큰 각, 음수 각에도"로 넓힌다. 43행에 "같은 삼각형 두 개를 직각을 낀 긴 변끼리 맞붙이면 세 각이 모두 $60^\circ$인 정삼각형이 되므로" 같은 근거를 더한다.
- gate_effect: info

## 후속 처리

2026-10-19, 작성자가 같은 세션에서 반영했다. 커밋 전 작업 트리 변경이다. 반영 뒤 결정적 검사는 지적 0건, `npm run test:js`는 50/50이다. 빌드는 dev 서버를 피해 격리된 복사본에서 실행했고 150쪽 생성, 본문 검사를 통과했다.

- 🟡 [L1] 43행 외: 문두 자리의 '곧'을 없애고 '곧'은 3회로 줄였다. '~해 보자'는 실험 안내(112행)의 2회만 남기고 평서로 바꿨다.
- 🟡 [L3] 120행: "앞 글의 변위 (3,4)를 원점에서 그리면 화살표의 끝점은 (3,4)이고, 길이는 √(3²+4²)=5다"로 원점에 놓는 단계를 밝혔다.
- 🟡 [L4] quadrants.svg: "−1"을 노란 선 위 삼각형 안쪽(200, 222)으로 올려 "O"와 떨어뜨렸다.
- 🟡 [L4] unit-circle.svg: 아래쪽 표시를 "−π/2"로, 하단 문구를 "−π/2 = −90°"로 바꿨다. 스펙도 고쳤다.
- 🟡 [L6] 25행: 120°에 2π/3, atan2 결과에 0.927·−2.214 라디안을 병기했다. 스펙의 라디안 항목도 같은 목록으로 고쳤다.
- 🟡 [L6] 148행: 본문은 그대로 두고 스펙에 근거를 적었다. 「투영」은 사용자 제공 시리즈 계획(2026-10-15)의 기초 3 «벡터를 더하고 특정 방향으로 투영한다는 것은?»에서 왔다. 리뷰어가 받은 자료에 이 계획이 없어서 생긴 지적이다.
- 🟡 [L7] 122·126행: "x≠0일 때"와 "x=0인 ±90°에서는 이 비가 정의되지 않는다"를 넣었다. 126행은 "(x,y)와 (−x,−y)는 나눈 값이 같으므로, 나눗셈을 하면 정반대 방향의 두 점을 구별할 정보가 사라진다"로 고쳤다.
- 🟡 [L7] 136행: "0이나 ±180° 같은 값을 돌려주거나 오류로 처리하는데, 어느 쪽이든 그 값에 방향의 뜻은 없다"로 고쳤다.
- 🟢 [L7] 41·43행: 예각이 아닌 각도에 0°와 90°를 넣었다. 30° 논증에는 정삼각형의 대칭, 그리고 막대가 만드는 삼각형이 반쪽 삼각형과 같다는 연결을 더했다.
- 🟢 [L2] 116행, 🟢 [L3] 41행, 🟢 [L1] 134행: "「길이 L인 막대」 절에서 계산한", "제1사분면"으로 통일, "앞의 실험도 끝점을 끌면"으로 고쳤다.

같은 PR의 실험 코드 리뷰(별도 리뷰어)가 실험 라벨 겹침을 상태 전체 스윕(θ 1° × L 11단계)으로 찾았다. 이에 따라 다음을 바꿨다. 정적 도판 `rod-lab.svg`도 함께 바뀌었다.

- 움직이던 성분 라벨 "L cos θ"·"L sin θ"를 그림 아래 고정 범례로 바꿨다.
- P·θ 라벨은 눈금·축 글자·O·막대·성분·끝점·단위원 점을 장애물로 두고 빈자리를 고르게 했다. θ는 20° 미만이거나 자리가 없으면 숨긴다.
- 각도를 (−180°, 180°]로 감아, 드래그로 −180°가 나오던 문제를 없앴다.
- 상태 전체(3,960개)를 모델과 독립된 상자 계산으로 검사하는 테스트를 더했다.
- 등록부 테스트가 각 모듈의 `mount`까지 확인한다.

브라우저 렌더는 작성자도 리뷰어도 보지 못했다.
