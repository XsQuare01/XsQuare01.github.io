schema_version: review-report/v2
target: robotics-rotation-matrix
generated_at: 2026-10-22
strict: true
sources: src/content/posts/robotics-rotation-matrix.md
summary: 🔴 1 · 🟡 4 · 🟢 8

## Findings

### 🔴 [L4] src/content/posts/robotics-rotation-matrix.md:61

- severity: 🔴
- source: L
- rule_id: L4
- location: src/content/posts/robotics-rotation-matrix.md:61
- quote: 노란 성분 삼각형을 90° 돌리면 초록 성분 삼각형이 된다.
- message: 노란 삼각형의 꼭짓점은 O, (cos θ, 0), (cos θ, sin θ)다. 원점 중심으로 90° 돌리면 O, (0, cos θ), (−sin θ, cos θ)가 된다. 이때 직각은 y축 위의 (0, cos θ)에 오고, cos θ 변은 y축을 따라 서며, sin θ 변은 높이 cos θ에서 왼쪽으로 눕는다. 그런데 turned-axes.svg 7행의 초록 점선 `M230 300H94V198`은 O→(−sin θ, 0)→(−sin θ, cos θ)를 그린다. sin θ 변이 x축 위에 있고 직각은 (−sin θ, 0)에 있다. 두 삼각형은 빗변을 공유하는 합동이지만, 빗변을 축으로 뒤집은 관계이지 90° 회전 관계가 아니다. 캡션(61행), 본문 63행 "가로 변은 위로 서고 세로 변은 왼쪽으로 누워", SVG aria-label "두 성분 삼각형은 서로 90° 돌린 모양이다"가 모두 그림과 어긋난다. 증명은 90° 규칙으로 따로 닫혀 있어 수학 결론은 그대로다. 다만 직관 설명이 그림과 모순된다.
- recommendation: 본문을 살리고 그림을 고친다. 초록 경로를 `M230 300V198H94`로 바꾸고(y축을 따라 cos θ 올라간 뒤 왼쪽으로 sin θ), 초록 "cos θ" 라벨은 y축 옆 세로 변으로, "sin θ" 라벨은 높이 198의 가로 변 옆으로 옮긴다. 다른 방법은 그림을 그대로 두고 캡션·63행·aria-label에서 "90° 돌리면"을 빼는 것이다.
- gate_effect: fail

### 🟡 [L1] src/content/posts/robotics-rotation-matrix.md:65

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:65
- quote: $(1,3)$을 정사영하고 남은 나머지 $\mathbf r$
- message: '나머지'에 이미 '남은 부분'이라는 뜻이 있어 '남은 나머지'는 겹말이다. 앞 글은 '나머지'를 용어로 정의했다. 181행 "남은 나머지 $(-0.8,0.6)$은 $\mathbf e_y'$ 하나였다. 막대 좌표 $(3,1)$은 이 두 수다"도 같은 겹말이고, '이 두 수'가 3과 'e′_y 하나'에 숨은 1을 가리켜 지시 대상이 흐리다.
- recommendation: 65행은 "(1,3)을 정사영한 나머지 r"로 고친다. 181행은 "나머지 (−0.8, 0.6)은 e′_y의 1배였다. 막대 좌표 (3,1)은 정사영 길이 3과 이 1이다"처럼 고친다.
- gate_effect: warn

### 🟡 [L4] public/images/robotics-rotation-matrix/turned-point.svg:20

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-rotation-matrix/turned-point.svg:20
- quote: P′ = (1.8 − 0.8, 2.4 + 0.6) = (1, 3)
- message: 본문은 돌리기 전과 뒤의 집게 끝을 모두 P라고 부른다(19행, 157행). rod-frame.svg도 두 칸 모두 P이고, rotation-lab.svg 범례도 "P: 집게 끝"이다. turned-point.svg만 돌아간 집게 끝을 P′로 적어(20행 라벨, 27행 범례) 본문에 정의되지 않은 기호가 생긴다. e′_x, e′_y의 프라임('돌아간 축')과 겹쳐 P′가 다른 점이라는 오해도 줄 수 있다.
- recommendation: 라벨과 범례의 P′를 P로 바꾼다. 돌린 뒤의 점을 꼭 구분해야 한다면 본문에서 P′를 먼저 정의한다.
- gate_effect: warn

### 🟡 [L4] src/content/posts/robotics-rotation-matrix.md:11

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/robotics-rotation-matrix.md:11
- quote: 로봇 팔의 막대 끝에 집게가 달려 있다고 하자.
- message: 도판에서는 막대 길이가 4이고, 집게는 막대를 따라 3인 자리에서 옆으로 나온다. 막대는 집게 너머로 1만큼 더 뻗어 있다(rod-frame.svg 7–10행, turned-point.svg 10–13행, 실험 모델의 `ROD = 4`). 본문은 집게가 막대 '끝'에 달렸다고 하므로, 독자는 그림에서 막대 끝과 집게 위치가 왜 다른지 찾게 된다. 실험에서는 흰 마름모 '막대 끝'(157행)과 집게 끝 P가 따로 있어 이 구분과도 충돌한다.
- recommendation: "로봇 팔의 막대에 집게가 달려 있다고 하자"처럼 '끝'을 뺀다. 실험에서 막대 끝 손잡이와 P를 구별해야 하므로 그림보다 본문을 고치는 편이 낫다.
- gate_effect: warn

### 🟡 [L4] src/content/posts/robotics-rotation-matrix.md:157

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/robotics-rotation-matrix.md:157
- quote: 막대에 붙은 격자도 막대와 함께 돌고, 파란 점은 그 격자의 칸에 맞춰 움직인다.
- message: rotation-lab.svg 7행의 막대 격자 간격은 40px, 곧 1단위다. 모델은 막대 좌표를 0.5 단위로 맞춘다(rotation-matrix-model.mjs 7행 `step: 0.5`, `dragPoint`→`setCoords`→`snap`). 파란 점은 격자 교점뿐 아니라 칸 변의 중점과 칸 가운데에도 멈춘다. '격자의 칸에 맞춰'라는 설명과 실제 동작이 다르다. 코드로 판정했고 브라우저 동작은 관찰하지 못했다.
- recommendation: "파란 점은 그 격자의 반 칸(0.5) 단위로 움직인다"로 고친다. 다른 방법은 격자를 0.5 간격으로 그리는 것이다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:13

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:13
- quote: 그러려면 두 각을 더한 각의 코사인과 사인을 계산해야 한다. 이 글은 그 공식 없이 답을 구하고
- message: '그 공식'이 가리킬 대상이 앞 문장에 없다. 앞 문장은 '계산해야 한다'로 끝나고 공식을 말하지 않는다.
- recommendation: "그러려면 두 각을 더한 각의 코사인과 사인을 구하는 공식이 필요하다. 이 글은 그 공식 없이 …"로 고친다.
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:25

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:25
- quote: 로봇 공학 교재는 앞의 것을 local 좌표, 뒤의 것을 world 좌표라고 부르고, 이 시리즈도 뒤의 글에서 이 이름을 쓴다.
- message: 한 문장에 관형격 '의'와 의존명사 '것'이 몰렸다. '뒤의'도 두 가지 뜻(뒤에 적은 것, 뒤에 나올 글)으로 두 번 쓰였다.
- recommendation: "로봇 공학 교재는 막대 좌표를 local 좌표, 고정 좌표를 world 좌표라고 부르고, 이 시리즈도 이후 글에서 이 이름을 쓴다."로 고친다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-rotation-matrix.md:11

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-rotation-matrix.md:11
- quote: 막대가 오른쪽을 가리키면 집게 끝의 좌표는 $(3,1)$이다.
- message: 막대의 밑동(관절)이 원점에 있다는 전제가 글에 적혀 있지 않다. 좌표 (3,1)과 33행의 '원점을 중심으로 돌린다'는 전제는 막대가 원점에 붙어 있어야 성립한다. 시리즈 독자는 앞 글에서 이 전제를 이어받고 그림도 막대를 원점에서 그리지만, 첫 문단에 한 구절만 넣으면 이 도약이 사라진다.
- recommendation: "로봇 팔의 첫 관절이 원점에 있고, 그 관절에 붙은 막대에 집게가 달려 있다고 하자"처럼 쓴다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-rotation-matrix.md:53

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-rotation-matrix.md:53
- quote: $\mathbf e_x$를 $\theta$만큼 돌린 화살표가 $\mathbf e_x'$이므로 $\mathbf e_y'$는 $\mathbf e_x'$를 $90^\circ$ 돌린 화살표다.
- message: 논증은 순환이 아니다. 같은 원점을 중심으로 돌린 각은 더해지고 순서와 무관하다는 전제만 쓰고 덧셈정리는 쓰지 않는다. 다만 결론 'e′_y는 e′_x를 90° 돌린 화살표'는 17행의 정의와 같다. 3절(69행)과 131행에 필요한 사실은 오히려 출발점인 'e′_y는 e_y를 θ만큼 돌린 화살표'다. 독자에게는 정의를 다시 증명하는 것처럼 읽힐 수 있다. 문단 안에 '화살표'가 여섯 번 되풀이된다.
- recommendation: 논증 방향을 바꾼다. "1절에서 e′_y를 e′_x를 90° 돌린 단위벡터로 정했다. 처음의 e_y를 θ만큼 돌린 화살표도 이것과 같다. …θ 돌린 e_y는 e′_x를 90° 돌린 화살표, 곧 e′_y다." 이렇게 하면 이 문단이 '돌아간 e_y = 막대의 왼쪽 축'을 보인다는 역할이 드러난다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-rotation-matrix.md:53

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-rotation-matrix.md:53
- quote: $90^\circ$ 규칙을 $\mathbf e_x'=(\cos\theta,\sin\theta)$에 쓰면
- message: 46–49행에서 식을 얻을 때는 '90° 규칙'이라는 이름을 붙이지 않았는데, 53행에서 처음 그 이름을 쓴다. 이후 63·89·151행에서도 쓴다. 캡션 61행은 '성분 삼각형'이라고 하고 본문 63행은 'e′_x의 삼각형'이라고 해서 이름이 갈린다.
- recommendation: 49행 끝에 "이 식을 90° 규칙이라 부르자"를 넣는다. 삼각형 이름은 캡션과 본문 중 한쪽으로 통일한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-rotation-matrix.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-rotation-matrix.md:2
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 없음
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-rotation-matrix.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-rotation-matrix.md:1
- quote: not-recorded
- message: `approved extension` (국소·핵심 불일치 없음). 이 글에는 Notion 원문이 없다. 승인 자료(포스트별 스펙, 기구학 슬라이드 1·3·4·7·8·22–24, 선형대수 39–50쪽 추출본)와 실제로 대조했다. 원천의 핵심이 모두 보존됐다: local 좌표는 일정하고 축 방향만 바뀐다(슬라이드 3 ↔ 27행), R(θ)의 네 성분(슬라이드 1·4·8, 44쪽 ↔ 122행), '첫 행은 세계 x'라는 행 읽기(슬라이드 4 ↔ 133행), j번째 열은 e_j가 옮겨 간 자리(42쪽, 슬라이드 24 ↔ 131행), 열벡터와 괄호 표기의 동일시(40쪽 ↔ 107–111행), 곱 = 열의 일차결합 = 성분 식(45–46쪽 ↔ 113–139행), 초기 회전을 되돌리는 행렬과 원점 이동 제외(슬라이드 7 ↔ 186행), 회전 합성에서 덧셈정리(49쪽 ↔ 195–216행). 원천과 다른 선택('선형사상' 이름 없이 회전 전제에서 출발, 덧셈정리를 행렬곱 대신 화살표 하나를 돌려 얻음, 원점 이동과 3차원 제외, x축 색을 앰버로, 집게 예시 값을 기초 3의 F·r과 이음)은 모두 스펙 provenance에 작성자 추가로 밝혀져 있고 원천의 의도와 논증을 해치지 않는다. 스펙 7절이 계획한 '(1,3)이 (3,1)의 각에 θ를 더한 방향'이라는 확인은 본문에 없지만 승인된 추가 예시의 생략이라 판정에 영향이 없다. 시리즈 계획(2026-10-15 대화)은 스펙에 인용된 형태로만 확인했다. 본문에 비공개 원천을 드러내는 문장은 없다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-rotation-matrix.md:1

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-rotation-matrix.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 본문 계산값을 모두 재계산했다(3(0.6,0.8)+1(−0.8,0.6)=(1,3), e′x·e′y=0, 90° 회전 (3,1)→(−1,3), 행 계산 1·3, 되찾기 3·1, 길이 전개의 엇갈린 항 상쇄, 무작위 θ·s로 ‖Rs‖=‖s‖·Rᵀ(Rs)=s·R(−θ)=R(θ)ᵀ, 덧셈정리 30°+60°, atan2(4,3)=53.130°, 실험 첫 화면 p=(2.098, 2.366), θ=53°에서 p=(1.007, 2.998)). 강한 주장의 증명 의무(41·49·81·103·139·181·191·212행)가 모두 닫혀 있고, 회전 전제는 33행에 전제로 밝혔으며, 63행은 직관과 증명을 나눴고, 169행은 임의의 점에 막대 좌표가 있음을 −θ 되돌리기로 보인다. 순환 논증은 없다.
- recommendation: 없음
- gate_effect: info

## 후속 처리

2026-10-22, 작성자가 같은 세션에서 반영했다. 위 finding의 줄 번호는 리뷰 시점의 글을 가리킨다. 반영한 뒤 확인한 결과는 다음과 같다.

- 결정적 검사: 지적 0건
- `npm run test:js`: 79/79
- 빌드: dev 서버를 피해 격리된 복사본에서 실행. 153쪽 생성, 76개 글 본문 검사 통과, KaTeX 오류 0
- 이 리포트에는 🔴이 남아 있어 strict 게이트를 통과하지 않는다. 반영한 글을 다른 리뷰어가 다시 리뷰하고, 그 결과로 이 리포트를 갱신한다. 원래 판정은 이 판의 커밋에 남긴다.

### 글 리뷰 반영

- 🔴 [L4] 61행 turned-axes.svg: 초록 성분 삼각형을 노란 삼각형을 원점 중심으로 90° 돌린 모양으로 다시 그렸다. 경로는 O에서 y축을 따라 cos θ 올라간 뒤 왼쪽으로 sin θ 간다(`M230 300V198H94`). 초록 "cos θ"는 y축 위 세로 변 옆에, "sin θ"는 위쪽 가로 변 아래에 두었다. 캡션과 aria-label은 그대로 맞는 말이 되었다. 63행은 "가로 변은 y축을 따라 위로 서고 세로 변은 그 끝에서 왼쪽으로 눕는다. 그렇게 얻은 초록 성분 삼각형은 위로 cos θ, 왼쪽으로 sin θ 간 자리에서 끝나고, 그 자리가 e′_y의 끝점이다"로 그림에 맞췄다. resvg 래스터로 다시 그려 확인했다.
- 🟡 [L4] 11행: "로봇 팔의 첫 관절이 원점에 있고, 그 관절에 붙은 막대에 집게가 달려 있다고 하자"로 바꿨다. '막대 끝'을 빼고, 아래 🟢 [L2] 11행의 원점 전제도 함께 넣었다.
- 🟡 [L4] turned-point.svg: 라벨과 범례의 P′를 P로 바꿨다.
- 🟡 [L4] 157행: "파란 점은 그 격자의 반 칸(0.5) 단위로 움직인다"로 고쳤다. 모델 주석도 같은 뜻으로 고쳤다.
- 🟡 [L1] 65·181행: "정사영한 나머지 r"로 겹말을 걷었다. 181행은 "나머지 (−0.8, 0.6)은 e′_y의 1배였다. 막대 좌표 (3,1)은 그 정사영 길이 3과 이 1이다"로 지시 대상을 밝혔다.
- 🟢 [L2] 53행: 논증의 방향을 바꿨다. 1절의 정의(e′_x를 90° 돌린 단위벡터가 e′_y)를 먼저 밝히고, 처음의 e_y를 θ만큼 돌린 것이 그것과 같음을 보이는 문단으로 고쳤다. 같은 원점 중심 회전에서 각이 더해진다는 전제만 쓴다.
- 🟢 [L1] 13행: "구하는 공식이 필요하다"로 바꿔 '그 공식'의 대상을 세웠다.
- 🟢 [L1] 25행: "막대 좌표를 local 좌표, 고정 좌표를 world 좌표라고 부르고, 이 시리즈도 이후 글에서 이 이름을 쓴다"로 고쳤다.
- 🟢 [L3] 49·61·63행: 49행 끝에 "이 식을 90° 규칙이라 부르자"를 넣었다. 63행도 캡션처럼 "성분 삼각형"이라 부른다.
- 🟢 [L5]·[L6]·[L7]: 조치 없음.

### 실험 코드 리뷰 반영

같은 브랜치의 실험 코드를 별도 리뷰어가 검토했다(🔴 0, 🟡 1, 🟢 8). 리뷰어는 포인터 흐름 시뮬레이션(확대·평행이동한 CTM), linkedom 마운트, 변이 22개, 글꼴 메트릭 측정을 썼다. 반영한 내용은 다음과 같다.

- 🟡 본문의 "격자의 칸에 맞춰"가 0.5 단위 스냅과 달랐다. 위 157행 반영과 같다.
- 🟢 막대 끝을 잡은 오프셋을 고정 좌표의 픽셀 벡터로 두어, 막대가 돌면 손가락 밑에서 손잡이가 밀리고 원점 판정도 O + 오프셋 자리로 옮겨 갔다. 누른 순간 막대 각과 포인터 방향의 차이를 각도로 기억하고, 끄는 동안 포인터 방향에 그 차이를 더한다. 원점 판정은 포인터 자체로 한다. 테스트는 막대 끝에서 막대를 가로질러 20px 떨어진 곳(약 7°)을 잡고 원점 둘레로 100°, 170° 돌려 각이 같은 만큼 도는지와 180°를 넘어 감기는지 본다.
- 🟢 끌기 도중 "처음으로"를 누르면 드래그 상태가 남아, 다음 pointermove가 옛 잡기를 새 상태에 적용했다. 리셋이 포인터 캡처를 풀고 드래그를 끝낸다. 브라우저에서는 확인하지 못했다.
- 🟢 막대 끝의 선택용 좌표를 모든 각도에서 그린 위치(x·y)와 대조하지 않았다. 상태 전체 검사에 넣었다.
- 🟢 HEAD_MIN의 상한이 고정되지 않았다. 반 단위(20px) 화살표에는 촉이 없고 √0.5 단위(28px) 화살표에는 촉이 있다는 단언과, marker가 그 사이에 들어가는지를 SVG에서 읽는 단언을 더했다.
- 🟢 읽기 값이 반올림 범위 안에 있는지를 전 상태에서 보지 않았다. 행렬·막대 좌표·고정 좌표의 보인 수가 참값과 0.005 이내인지를 상태 전체에서 검사한다.
- 🟢 넓은 글꼴에서 행렬 괄호와 숫자가 붙을 수 있다. 행렬 왼괄호를 4px, 막대 좌표 왼괄호를 4px 왼쪽으로 옮겼다.
- 🟢 스크린 리더 요약에서 고정 좌표에만 ≈가 붙었다. 반올림한 쌍마다 ≈를 붙인다(정확한 쌍은 =).
- 🟢 θ 입력 양 끝의 감싸기와 `setAngle`의 `+ 0`: 리뷰어 판단대로 바꾸지 않았다.

변이 시험을 다시 돌렸다. 작성자 변이 21개에 리뷰어가 짚은 빈틈과 새 끌기 방식의 변이 5개를 더한 26개가 모두 잡힌다.
