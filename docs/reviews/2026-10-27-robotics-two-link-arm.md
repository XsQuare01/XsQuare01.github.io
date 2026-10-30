schema_version: review-report/v2
target: robotics-two-link-arm
generated_at: 2026-10-27
strict: true
sources: src/content/posts/robotics-two-link-arm.md
summary: 🔴 0 · 🟡 4 · 🟢 16

## Findings

### 🟡 [L2] src/content/posts/robotics-two-link-arm.md:63

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:63
- quote: 성분을 풀면 앞의 식과 같다. 다음 절은 이 읽기를 쓴다.
- message: 절을 가리키는 말이 한 칸씩 어긋난다. 「손끝의 위치」 바로 다음 절은 실험 절 「각도를 직접 바꿔 보기」이고, 이 읽기($\mathbf p=R(\theta_1)\mathbf s$)를 쓰는 곳은 그다음 절 「손끝까지의 거리는 둘째 관절이 정한다」다. 79행의 "앞 절의 둘째 읽기에서"도 같은 문제로, 79행의 앞 절은 실험 절이다. 절 번호를 따라가는 독자는 엉뚱한 절에 닿는다.
- recommendation: 63행은 "「손끝까지의 거리는 둘째 관절이 정한다」 절이 이 읽기를 쓴다"로, 79행은 "「손끝의 위치」 절의 둘째 읽기에서"처럼 절 이름으로 가리킨다.
- gate_effect: warn

### 🟡 [L3] src/content/posts/robotics-two-link-arm.md:11

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/robotics-two-link-arm.md:11
- quote: 원점에 고정된 어깨 관절이 첫 링크를 돌리고, 첫 링크 끝의 팔꿈치 관절이 둘째 링크를 돌린다.
- message: '링크'가 정의 없이 처음 나온다. 앞의 네 글에는 이 말이 한 번도 없고 같은 대상을 '막대'라 불렀다. 이 글은 두 말을 섞어 쓴다. 37행에는 "첫 링크에서 본 둘째 링크는 막대 방향에서 θ₂만큼 돈 … 막대다"가 있고, "막대 좌표"(37·57·63행)와 "첫 링크의 방향"(19행)이 함께 나온다. 고교 수학을 잊은 독자는 링크와 막대가 같은 대상인지 확인할 수 없다.
- recommendation: 11행에서 "관절과 관절, 또는 관절과 손끝을 잇는 막대를 **링크**라 한다"처럼 정의한다. 37행처럼 한 문장에 두 말이 섞인 곳은 역할을 나눠 쓴다. '막대 좌표'는 앞 글의 용어로 그대로 두어도 된다.
- gate_effect: warn

### 🟡 [L4] src/content/posts/robotics-two-link-arm.md:121

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/robotics-two-link-arm.md:121
- quote: 고리 밖의 빨간 점에는 손끝이 닿지 않는다.
- message: 본문과 그림이 서로 다른 점을 예로 든다. 바로 앞 119행은 닿지 않는 예로 $(3,1)$과 $(0.5,0)$을 드는데, reach.svg의 빨간 점 둘은 $(2.5,2)$($d\approx3.20$)와 $(0.5,0.5)$($d\approx0.71$)다(reach.svg 19–20행, 1단위 52px, 원점 (200,222)). 그림에 좌표 표시가 없어 직접 모순은 아니지만, 독자는 빨간 점을 본문의 두 점으로 읽기 쉽다. 다른 점(안쪽 $(2,1)$ "2개", 바깥 경계 $(-3,0)$ "1개", 안쪽 경계 $(0,-1)$ "1개", 팔의 끝점, 고리 반지름 1·3)은 맞다.
- recommendation: 빨간 점을 본문의 $(3,1)$과 $(0.5,0)$으로 옮기거나, 본문의 예를 그림의 점으로 바꾸거나, 그림 점에 좌표를 적는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-two-link-arm.md:131

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-two-link-arm.md:131
- quote: - 안쪽 경계($d=|L_1-L_2|>0$): $c=-1$, $\theta_2=180^\circ$. 팔을 완전히 접은 자세 하나다.
- message: 자세 개수를 나눈 네 경우가 전체를 덮지 못한다(MECE 아님). 이 줄은 $d>0$을 걸어 $L_1=L_2$, $T=O$인 퇴화 사례를 뺐는데, 그 사례를 받는 다섯째 경우가 없다. 117행은 "$\theta_1$이 무엇이든 손끝이 원점에 있다"고만 쓰고 "자세가 무수히 많다"는 결론을 적지 않는다. 승인 스펙은 이 결론을 질문과 결론 2번과 의무 표에 따로 세웠는데 본문에서 빠졌다. 그래서 핵심 정리의 "경계에는 한 자세가 있고"와 description의 "경계에서는 하나다"는 일반 $L_1$, $L_2$에 대해 말하면서 $L_1=L_2$일 때 틀린 문장이 된다. 같은 경우에 119행의 "작업 공간은 … 고리다"도 실제로는 원판이 된다. 예로 든 팔($2,1$)에는 영향이 없다.
- recommendation: 목록 끝에 "$L_1=L_2$이고 $T=O$($d=0$): $\theta_2=180^\circ$이고 $\theta_1$은 아무 값이나 된다. 자세가 무수히 많다."를 더한다. 119행에는 "($L_1=L_2$이면 안쪽 반지름이 0이라 원판)"을 덧붙인다. 핵심 정리와 description은 예외를 밝히거나 "$L_1\ne L_2$이면"을 단다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:21

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:21
- quote: 벡터의 덧셈 글에서 두 번째 막대의 각도를 $x$축에서 재면서 뒤로 미룬 방식이 이것이다.
- message: 수식어가 길게 겹쳐 무엇을 미뤘는지 바로 읽히지 않고, "x축에서 잰" 방식을 미룬 것으로 오독할 수 있다. 앞 글을 가리키는 내용 자체는 맞다(vector-projection.md 37행).
- recommendation: "벡터의 덧셈 글은 두 번째 막대의 각도를 x축에서 재고, 앞 막대를 기준으로 재는 방식을 뒤로 미뤘다. θ₂가 그 방식이다."
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:43

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:43
- quote: 첫 링크에서 $\theta_2$만큼 더 돌았으니 자연스러운 결과이고, 회전행렬로 계산해도 같은 답이 나온다.
- message: 바로 위 식이 이미 회전행렬로 계산한 결과라서 뒷부분은 같은 말을 되풀이한다.
- recommendation: "첫 링크에서 θ₂만큼 더 돌았으니 자연스러운 결과다."로 줄인다.
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:51

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:51
- quote: 벡터의 덧셈이 모두 모든 각도에서 성립하므로
- message: '모두 모든'이 붙어 있어 동어가 겹친다.
- recommendation: "…벡터의 덧셈은 어느 각도에서나 성립하므로"
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:117

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:117
- quote: 단위원과 세로선 $x=c$는 점 $(c,\sqrt{1-c^2})$에서 만나고, 그 점의 각을 $\theta_2$로 고르면 $\cos\theta_2=c$이고, 손끝까지의 거리는 $d$가 된다.
- message: 한 문장에 연결어미 '-고'가 세 번 이어지고(같은 문법 요소의 중복) 이 독자에게 길다. '세로선 x=c'라는 표기도 이 글에서 처음 나온다.
- recommendation: 두세 문장으로 나누고 "가로 좌표가 c인 점이 모인 세로선 x=c"처럼 표기를 풀어 준다.
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:134

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:134
- quote: 곧 회전행렬 글의 약 $53.13^\circ$만큼 돌리면
- message: 관형격 '의'가 어색하게 이어져 말 순서가 꼬였다. 내용은 맞다(rotation-matrix.md 65행).
- recommendation: "곧 회전행렬 글에서 본 약 53.13°만큼 돌리면"
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:13

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:13
- quote: 앞의 네 글이 이 질문에 필요한 재료를 마련했다.
- message: 11행은 질문 두 개를 세웠는데 "이 질문"은 단수다. '네 글'이라 해 놓고 링크는 셋만 달고 다음 문장은 "그 셋으로"라고 받아, 점과 벡터 글은 이름이 나오지 않는다.
- recommendation: "앞의 네 글이 두 질문에 필요한 재료를 마련했다"로 고치고, 점과 벡터 글을 한 마디 넣거나 "그 가운데 세 글로"라고 적는다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:99

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:99
- quote: 사인과 코사인 글에서 본 대로 $y$축에 대해 뒤집으면 가로 좌표의 부호만 바뀌어 $\cos(180^\circ-\theta_2)=-\cos\theta_2$이므로
- message: 사인과 코사인 글은 60°를 y축에 대해 뒤집으면 120°가 되는 예 하나만 보였고, "θ 자리를 y축에 대해 뒤집으면 180°−θ 자리"라는 일반형은 그 글에 없다. 곁가지 문단이라 증명에는 영향이 없다.
- recommendation: "θ₂ 자리를 y축에 대해 뒤집으면 180°−θ₂ 자리가 되고, 가로 좌표는 부호만 바뀐다"처럼 일반형을 한 마디 덧붙인다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:132

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:132
- quote: - 고리 바깥: 자세가 없다.
- message: 나머지 세 경우에는 부등식이 붙어 있는데 이 경우에만 없다. 독자는 '바깥'을 바깥 원 너머로만 읽고 안쪽 구멍($d<|L_1-L_2|$)이 빠졌다고 생각할 수 있다.
- recommendation: "- 고리 바깥($d<|L_1-L_2|$ 또는 $d>L_1+L_2$): 자세가 없다."
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:150

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:150
- quote: 읽기 값의 관절 각은 실험이 계산해 보여 주는 값이다.
- message: 이 문장을 왜 적었는지가 드러나지 않는다. 본문에 없는 계산식으로 구한 값이고 그 식은 뒤의 글에서 다룬다는 뜻으로 보이지만, 그 뜻이 문장에 나타나지 않는다.
- recommendation: "읽기 값의 관절 각은 실험이 계산한 값이고, 계산식은 뒤의 글에서 다룬다."
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:168

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:168
- quote: 이 글로 입문부를 마친다.
- message: '입문부'는 시리즈의 어느 글에서도 소개된 적이 없어, 독자는 몇 편이 입문부였는지 모른다.
- recommendation: "점과 벡터부터 이 글까지 다섯 편으로 입문 과정을 마친다"처럼 범위를 밝힌다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-two-link-arm.md:103

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-two-link-arm.md:103
- quote: 목표점 $T$까지의 거리를 $d=\lVert T\rVert$라 하자.
- message: 같은 거리를 ‖P‖(69행), ‖p‖(79행), d(89행)로 적고, 103행에서 d를 목표점의 거리로 다시 쓴다. 시리즈는 ‖·‖를 벡터에만 정의했는데 여기서는 점 P, T에 붙였다. 뜻은 통한다.
- recommendation: 처음 나오는 곳에서 "‖T‖는 원점에서 T까지의 거리, 곧 위치벡터의 길이"라고 밝히고, 103행에서 같은 글자 d를 다시 쓰는 이유를 드러낸다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-two-link-arm.md:150

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-two-link-arm.md:150
- quote: 아래 그림에서 흰 고리(목표점 $T$)를 끌거나
- message: 같은 문단에서 '고리'가 목표점 표시와 작업 공간("어두운 고리가 작업 공간이고")을 함께 가리킨다. 괄호와 색으로 구분은 된다.
- recommendation: 목표점 표시는 "흰 동그라미(목표점 T)"로 바꾸고 '고리'는 작업 공간에만 쓴다.
- gate_effect: info

### 🟢 [L4] public/images/robotics-two-link-arm/two-postures.svg:25

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/robotics-two-link-arm/two-postures.svg:25
- quote: 옅은 점선: O에서 2, T에서 1 떨어진 점들
- message: 범례를 두 조건을 함께 만족하는 점(팔꿈치 두 개)으로도 읽을 수 있다. 실제 옅은 점선은 O를 중심으로 반지름 2인 호(−8°~68°)와 T를 중심으로 반지름 1인 원, 두 곡선이다. 도형 자체(팔꿈치 (1.2,1.6)과 (2,0), 직선 OT의 기울기 1/2)는 정확하다.
- recommendation: "옅은 점선: O에서 2인 호와 T에서 1인 원"처럼 곡선 둘을 따로 적는다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-two-link-arm.md:4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-two-link-arm.md:4
- quote: 거꾸로 목표점에 손끝을 놓는 자세는 원점에서의 거리가 |L₁ − L₂| 이상 L₁ + L₂ 이하일 때만 있고, 그 안쪽에서는 둘, 경계에서는 하나다.
- message: 제목과 description은 글 내용(순기구학 공식, 닿는 조건, 자세의 수)을 잘 대표한다. 다만 '원점에서의 거리가'의 주어가 빠져 손끝의 거리인지 목표점의 거리인지 모호하고, '경계에서는 하나'에는 L7 지적의 퇴화 예외가 그대로 남아 있다.
- recommendation: "…자세는 목표점이 원점에서 |L₁ − L₂| 이상 L₁ + L₂ 이하로 떨어져 있을 때만 있고…"로 고치고, L7 수정에 맞춰 예외 처리도 함께 고친다.
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-two-link-arm.md:168

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-two-link-arm.md:168
- quote: 한 입력에 조립되는 모양이 둘이거나 아예 조립되지 않는 경우도 다시 나온다.
- message: `approved extension`. 승인 자료를 직접 대조했다. 스펙에 인용된 사용자 시리즈 계획의 기초 5 질문, 두 링크의 기여를 합산하는 조작 그림, "목표점을 먼저 지정하고 여러 자세나 닿지 않는 경우를 보여 주며 해법은 뒤로 미룬다"는 메모가 본문과 실험 2개, 146행에 반영돼 있다. kin.txt 추출본의 4장(local 점을 회전한 뒤 원점을 더함)은 원점이 O라 $\mathbf p=R(\theta_1)\mathbf s$로 들어갔고, 19–20장(두 조립 가지와 조립되지 않는 경우)은 이 이어지는 글 문장에서 예고로만 쓰였으며, 5–6장의 관절 구속식과 원점 이동은 스펙이 범위 밖이라고 밝혔다. 예시 값, 회전의 길이 보존으로 세운 거리 논증, 거울상 근거는 스펙 provenance에 작성자 추가로 적혀 있고 원천의 의도를 훼손하지 않는다. Notion 페이지는 없다. 본문에 비공개 원천을 가리키는 서술은 없다(검출 grep과 직접 읽기 모두 0건).
- recommendation: 없음
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-two-link-arm.md:1

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-two-link-arm.md:1
- quote: not-recorded
- message: 위 🟡 [L7] 외에는 이슈가 없다. 재계산: $(30^\circ,60^\circ)\to(\sqrt3,2)$, $d^2=5+4\cos\theta_2$(60°→7, 0°→9, 180°→1, 90°→5), distance.svg의 팔 넷의 손끝이 모두 $\sqrt7$, $T=(2,1)$에서 $c=0$·$\theta_1=53.1301^\circ$($\cos 0.6$, $\sin 0.8$)·$R(\theta_1)(2,-1)=(2,1)$·팔꿈치 $(1.2,1.6)$, $(2,0)$을 직선 OT에 대해 뒤집으면 $(1.2,1.6)$, $(3,1)$과 $(0.5,0)$은 닿지 않음. 손끝 식과 $d^2$의 전 각도 성립, 필요조건(코사인의 범위)과 충분조건($\theta_2$ 구성, 방향 맞추기, $d=0$은 $L_1=L_2$일 때만), $\theta_2$의 개수(단위원과 $x=c$의 교점)와 $d>0$일 때 $\theta_1$의 유일성이 닫혔다. 거울상은 직관과 짧은 근거로만 쓰였고 144행이 "개수의 근거는 앞의 코사인 논증"이라고 밝힌다. 앞 글 인용 13곳은 모두 해당 글에 실제로 있다. 참고 자료의 서술(Modern Robotics 6장 도입부의 식 (6.1), $L_1>L_2$일 때의 고리, 0·1·2개 해, lefty/righty와 elbow-up/down, OpenStax 10.2)도 정확하다.
- recommendation: 없음
- gate_effect: info

## 후속 처리

2026-10-27, 작성자가 같은 세션에서 반영했다. 위 finding의 줄 번호는 리뷰 시점의 글을 가리킨다. 반영한 뒤 확인한 결과는 다음과 같다.

- 결정적 검사: 지적 0건
- `npm run test:js`: 97/97
- 빌드: dev 서버를 피해 격리된 복사본에서 실행. 154쪽 생성, 77개 글 본문 검사 통과, KaTeX 오류 0
- 변이 시험: 작성자 변이 23개에 코드 리뷰가 짚은 빈틈 5개를 더한 28개가 모두 잡힌다.

### 글 리뷰 반영

- 🟡 [L7] 131행: 자세 목록 끝에 "$L_1=L_2$이고 $T=O$($d=0$): $\theta_2=180^\circ$이고 $\theta_1$은 아무 값이나 된다. 자세가 무수히 많다"를 더했다. 작업 공간 문장에 "$L_1=L_2$이면 안쪽 반지름이 0이라 구멍 없는 원판"을 덧붙였다. 핵심 정리는 "두 링크의 길이가 다르면 … 길이가 같으면 원점에서만 자세가 무수히 많다"로, description은 "두 링크의 길이가 다르면 그 안쪽에서는 둘, 경계에서는 하나"로 고쳤다.
- 🟡 [L2] 63·79행: 절 이름으로 가리킨다("「손끝까지의 거리는 둘째 관절이 정한다」 절이 이 읽기를 쓴다", "「손끝의 위치」 절의 둘째 읽기에서").
- 🟡 [L4] reach.svg: 빨간 점 둘을 $(3,1)$과 $(0,0.5)$로 옮겼다. 처음 제안한 $(0.5,0)$은 그림에서 자세 ①의 첫 링크($x$축 위)와 겹쳐 목표점이 팔 위에 놓인 것처럼 보여서, 같은 거리 0.5의 $(0,0.5)$를 골랐다. 본문의 예와 스펙 계산표도 $(0,0.5)$로 맞췄다. 라벨이 겹치지 않도록 "2개"·"없음" 자리를 옮기고 resvg로 확인했다.
- 🟡 [L3] 11·37행: 도입에 "관절과 관절, 또는 관절과 손끝을 잇는 막대를 **링크**라 한다"를 넣었다. 37행은 "첫 링크에서 보는 둘째 링크는 첫 링크의 방향에서 θ₂만큼 돈 길이 L₂인 막대"로 고쳤다.
- 🟢 [L4] two-postures.svg 범례: "옅은 점선: O에서 2인 호와 T에서 1인 원". 같은 그림의 자세 ② 범례 점선도 그림과 같은 "9 6" 무늬로 맞췄다(코드 리뷰 🟢4와 같은 문제).
- 🟢 [L3] 150행: "흰 동그라미(목표점 T)".
- 🟢 [L3] 103행: "원점에서 목표점 T까지의 거리, 곧 T의 위치벡터의 길이를 ‖T‖로 쓰자. 손끝이 T에 닿으면 손끝까지의 거리 d가 이 값과 같아야 하므로, 이 절에서는 d = ‖T‖로 둔다."
- 🟢 [L2] 99행: "단위원에서 θ₂ 자리를 y축에 대해 뒤집으면 180°−θ₂ 자리가 되고, 사인과 코사인 글의 60°와 120°처럼 가로 좌표는 부호만 바뀐다."
- 🟢 [L2] 132행: "고리 바깥($d<|L_1-L_2|$ 또는 $d>L_1+L_2$)".
- 🟢 [L2] 150행: "읽기 값의 관절 각은 실험이 계산한 값이고, 계산식은 뒤의 글에서 다룬다."
- 🟢 [L2] 13행: "두 질문에 필요한 재료"로 고치고 점과 벡터 글을 링크와 함께 넣었다. 다음 문장은 "그 재료로"로 받는다.
- 🟢 [L2] 168행: "점과 벡터 글부터 이 글까지 다섯 편으로 입문 과정을 마친다."
- 🟢 [L1] 21·43·51·117·134행: 권고대로 고쳤다. 117행은 세 문장으로 나누고 "가로 좌표가 c인 점을 모은 세로선 x=c"로 표기를 풀었다.
- 🟢 [L5] 4행: 위 L7 반영과 함께 "목표점이 원점에서 … 떨어져 있을 때만"으로 주어를 밝혔다.
- 🟢 [L6]·[L7] coverage: 조치 없음.

### 실험 코드 리뷰 반영

같은 브랜치의 두 실험을 별도 리뷰어가 검토했다(🔴 0, 🟡 3, 🟢 9). 리뷰어는 배율을 바꾼 포인터 시뮬레이션(손잡이당 64,896회 누름), linkedom 마운트, 변이 19개, resvg 래스터를 썼다. 반영한 내용은 다음과 같다.

- 🟡 닿지 않는 목표점에서 «cos θ₂ = … = 1.25»처럼 틀린 등식이 보였다. 읽기 칸 이름을 본문과 같은 «c = (d² − L₁² − L₂²) / (2L₁L₂), 닿으려면 cos θ₂ = c»로 바꾸고, 닿지 않으면 «(|c| > 1이라 그런 θ2가 없다)»를 덧붙인다.
- 🟡 순기구학 테스트가 그린 손잡이 위치를 보지 않아 «θ₂ < 0이면 마름모를 팔꿈치에 그림» 변이가 살아남았다. 상태 전체 검사에서 두 손잡이를 독립 식의 $E$·$P$와 대조한다.
- 🟡 역기구학 테스트의 꺾임 방향과 거울상 검사가 모델 값을 보아 «x < 0이면 두 자세를 맞바꿈», «y < 0이면 같은 팔을 두 번 그림» 변이가 살아남았다. 그린 링크에서 꺾임 방향(①은 반시계, ②는 시계, 경계는 곧거나 접힘)을 읽고, 그린 두 팔꿈치가 서로 다르며 픽셀 공간에서 직선 OT에 대한 거울상인지 본다.
- 🟢 180° 호의 방향을 검사하지 않았다. 대표 각도가 +180°이므로 반시계(flag 0)라고 단언한다.
- 🟢 중심 판정이 정확히 중심일 때만 동작해, 손끝을 끌며 E를 0.0025px 옆으로 지나가자 θ₂가 60 → 150 → −120으로 튀었다. 중심에서 6px 안이면 각을 유지한다. 실험 규약 문서의 해당 항목도 고쳤다.
- 🟢 스펙의 "호는 각이 작으면 그리지 않는다"를 코드에 맞춰 "0°일 때만"으로 고쳤다.
- 🟢 실험 2 범례의 자세 ② 점선 무늬를 실제 그림과 같은 "9 6"으로 맞췄다.
- 🟢 본문의 "흰 점선은 … 화살표 a+b"를 "흰 점선은 원점과 손끝을 잇는 a+b"로 고쳤다(그 선에는 화살촉이 없다).
- 🟢 단독 값 표기 헬퍼가 두 런타임에 중복되고 테스트가 없었다. `readout.mjs`의 `approx`로 옮기고 `test/readout.test.mjs`를 더했다. 실험 규약의 적용 범위를 «읽기 칸에 홀로 놓인 값»으로 좁히고, 요약 문장 속 «= (3, 1)»은 그대로 읽힌다고 적었다(회전행렬 실험의 요약은 바꾸지 않는다).
- 🟢 목표점이 x = −3.5에 오면 왼쪽 눈금 숫자를 가렸다. 목표점 범위를 [−3, 3]으로 줄였다. 이 범위로도 안쪽·두 경계·구멍·고리 바깥이 모두 나오는지 테스트가 확인한다.
- 🟢 두 모델에 중복된 좌표 상수(`UNIT`, `O`, `toSvg`, `fromSvg`)를 `two-link.mjs`로 모았다.
- 🟢 안쪽 경계의 접힌 자세가 헷갈릴 수 있다는 지적은 그대로 두었다. 팔꿈치 점과 읽기 값 «팔꿈치 (2, 0)»으로 구분된다.
