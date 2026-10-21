# 로보틱스 기초 3 — 벡터의 덧셈과 정사영

- 날짜: 2026-10-21
- 브랜치: `feat/robotics-vector-projection` (origin/main 기준. 기초 2의 추가 리뷰 반영은 #246으로 따로 올렸고, 이 브랜치는 기초 2 파일을 건드리지 않는다)
- 산출물: 본편 `robotics-vector-projection.md`, 정적 SVG 6장, 조작 실험 2개(`sum-lab.svg` + `vector-sum`, `projection-lab.svg` + `vector-projection`)
- 독자: 기초 1에서 사용자가 확인한 «고교 수학을 잊은 독자»를 이어받는다. 이번 편도 사용자는 바로 작성을 요청했으므로(2026-10-21 "'기초 3' 페이지 포스트 작성해줘"), 독자와 목적을 다시 묻지 않고 시리즈의 확인값을 쓴다.
- 목적: 프로젝트의 기구학을 삼각함수·벡터부터 그림으로 공부하고 블로그로 정리한다(기초 1·2와 같음).

## 질문과 결론

두 질문을 한 편에서 다룬다.

1. 막대 끝에 막대를 하나 더 붙이면 두 번째 막대의 끝점은 어디인가? 두 화살표를 이어 붙이면 끝점은 성분끼리 더한 $(a_x+b_x,\;a_y+b_y)$다.
2. 비스듬한 레일 방향 $\mathbf u$가 있을 때, 변위 $\mathbf a$는 레일을 따라 얼마나 간 것이고 레일에서 얼마나 벗어났는가? 레일 방향으로 내린 그림자(정사영)의 길이는 $\mathbf a\cdot\mathbf u=a_xu_x+a_yu_y=\lVert\mathbf a\rVert\cos\varphi$이고, 남은 부분 $\mathbf a-(\mathbf a\cdot\mathbf u)\mathbf u$는 레일에 수직이다.

기초 2의 «이어지는 글» callout이 첫 질문과 «화살표 하나를 다른 방향으로 투영하는 방법»을 예고했다.

## 본문 순서

도입: 기초 2가 남긴 질문(막대 끝에 막대를 하나 더 붙이면)과 레일 질문을 함께 세운다. 두 질문에 쓰는 연산이 벡터의 덧셈과 정사영이다.

1. **화살표를 이어 붙이면 더해진다** — $\mathbf a=(3,1)$의 머리에 $\mathbf b=(1,2)$의 꼬리를 놓으면 끝점은 $(4,3)$. 가로 이동끼리, 세로 이동끼리 더해지므로 $\mathbf a+\mathbf b=(a_x+b_x,\,a_y+b_y)$로 정의한다. 순서를 바꿔 $\mathbf b$ 다음 $\mathbf a$로 가도 끝점은 같다(성분마다 수의 덧셈 순서가 상관없음). 두 길이 평행사변형을 이루고 합은 그 대각선이다. 길이는 성분처럼 더해지지 않는다: $\lVert\mathbf a\rVert+\lVert\mathbf b\rVert=\sqrt{10}+\sqrt5\approx5.40$이지만 $\lVert\mathbf a+\mathbf b\rVert=5$. 기초 2의 막대로 돌아가 길이 2·30° 막대 끝에 위쪽을 향한 길이 1 막대를 붙이면 끝점은 $(\sqrt3,1)+(0,1)=(\sqrt3,2)$. 두 번째 막대의 각도도 같은 $x$축에서 잰다고 둔다(앞 막대에서 재는 관절 각은 뒤에서 다룬다). 도판 `sum.svg`.
2. **수를 곱하면 길이와 방향이 바뀐다** — 실수배 $k\mathbf a=(ka_x,\,ka_y)$. 길이는 $|k|\,\lVert\mathbf a\rVert$. $k>0$이면 같은 방향, $k<0$이면 정반대 방향, $k=0$이면 영벡터. 기초 2의 $(L\cos\theta,L\sin\theta)$는 단위원 위 점에 $L$을 곱한 실수배였다. 뺄셈 $\mathbf a-\mathbf b=\mathbf a+(-1)\mathbf b$. $\overrightarrow{OA}+\overrightarrow{AB}=\overrightarrow{OB}$이므로 $\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}$이고, 이것이 기초 1의 «끝점에서 시작점을 뺀다»다. 도판 `multiples.svg`.
3. **모든 벡터는 두 축 방향의 합이다** — 길이 1인 벡터를 단위벡터라 한다. $\mathbf e_x=(1,0)$, $\mathbf e_y=(0,1)$. $\mathbf a=a_x\mathbf e_x+a_y\mathbf e_y$. 성분은 «$\mathbf e_x$와 $\mathbf e_y$를 몇 배씩 더하는가»다. 기초 2의 끝점은 $L\cos\theta\,\mathbf e_x+L\sin\theta\,\mathbf e_y$. 도판 `unit-axes.svg`.
4. **화살표를 직접 더해 보기** — 실험 1.
5. **한 방향으로 그림자 내리기** — 레일 질문. 원점을 지나 $\mathbf u$ 방향으로 뻗은 직선 $\ell$에 $\mathbf a$의 끝점에서 수선을 내린 발 $F$. $\overrightarrow{OF}$가 $\mathbf a$의 $\mathbf u$ 방향 **정사영**이다. $\overrightarrow{OF}=s\,\mathbf u$로 쓸 때 $s$는 부호 있는 길이다. 그림 전체를 원점 중심으로 돌려 $\mathbf u$가 오른쪽을 향하게 하면 $\ell$은 가로축이 되고 $F$는 끝점의 가로 좌표 자리다. 기초 2에 따라 $s=\lVert\mathbf a\rVert\cos\varphi$($\varphi$는 $\mathbf u$에서 $\mathbf a$까지 잰 각). $|\varphi|<90^\circ$면 양수, $90^\circ$면 0, 더 크면 음수. $\mathbf u=\mathbf e_x$이면 $s=a_x$: 성분은 축 방향 정사영의 길이였다. 도판 `shadow.svg`, `shadow-signs.svg`.
6. **그림자의 길이를 성분으로 계산하기** — 세 단계. ① 그림자도 더해지고 실수배된다: 돌린 그림에서 $s$는 가로 성분이고, 그림을 통째로 돌려도 이어 붙인 모양은 유지되므로 1절의 «가로 이동끼리 더한다»가 그대로 성립한다. ② 단위벡터 둘은 서로에게 같은 길이의 그림자를 드리운다: $\mathbf e_x$의 $\mathbf u$ 방향 그림자는 $\cos(-\alpha)$, $\mathbf u$의 $\mathbf e_x$ 방향 그림자는 $\cos\alpha$이고, 두 값은 같다(기초 2의 $-30^\circ$처럼 $x$축에 대해 뒤집어도 가로 좌표는 그대로). 뒤의 것은 $\mathbf u$의 가로 성분 $u_x$다. 같은 이유로 $\mathbf e_y$의 그림자는 $u_y$. ③ $\mathbf a=a_x\mathbf e_x+a_y\mathbf e_y$이므로 $s=a_xu_x+a_yu_y$. 이 계산을 **내적** $\mathbf a\cdot\mathbf b=a_xb_x+a_yb_y$로 이름 붙인다. 예: $(1,3)\cdot(0.6,0.8)=3$. 일반 벡터 $\mathbf b=\lVert\mathbf b\rVert\mathbf u_b$에 대해 $\mathbf a\cdot\mathbf b=\lVert\mathbf a\rVert\lVert\mathbf b\rVert\cos\varphi$. 영벡터가 아닌 두 벡터는 내적이 0일 때, 그리고 그때에만 수직이다. $\mathbf a\cdot\mathbf a=\lVert\mathbf a\rVert^2$. 도판 `mutual-shadow.svg`.
7. **정사영과 나머지로 나누기** — $\mathbf r=\mathbf a-s\mathbf u$. $\mathbf r\cdot\mathbf u=\mathbf a\cdot\mathbf u-s(u_x^2+u_y^2)=0$이므로 $\mathbf r$은 $\mathbf u$에 수직이다. 예: $\mathbf r=(-0.8,0.6)$, 길이 1, $10=3^2+1^2$. 직선 위의 다른 점 $t\mathbf u$까지의 거리 제곱은 $(s-t)^2+\lVert\mathbf r\rVert^2$이라 $F$가 $\ell$ 위에서 $\mathbf a$의 끝점에 가장 가까운 유일한 점이다. 레일 질문의 답: 레일을 따라 3, 레일에서 벗어난 양 1. 레일을 따라 움직이는 관절은 이 나머지가 0이 되도록 묶는다(관절은 뒤에서 다룬다).
8. **정사영을 직접 바꿔 보기** — 실험 2.
9. 핵심 정리 callout → 이어지는 글 callout(기초 4: 막대를 돌리면 막대에 붙은 두 축 $\mathbf e_x,\mathbf e_y$도 함께 돈다. 3절의 구조로 돌아간 점을 구하고, 돌아간 두 축의 성분이 회전행렬의 두 열이 된다. 미발행이라 링크 없음) → 참고 자료.

절 제목에 번호를 쓰지 않는다. `numbered: true`가 붙인다.

## 용어와 기호 도입 순서

- 벡터는 굵은 소문자 $\mathbf a,\mathbf b,\mathbf u$. 성분은 $(a_x,a_y)$. 기초 1의 $\overrightarrow{AB}$, $\lVert\cdot\rVert$, 좌표/성분 구분을 그대로 쓴다.
- 덧셈과 평행사변형: 1절. 실수배·뺄셈: 2절. 고교 용어 «실수배»를 쓴다.
- 단위벡터, $\mathbf e_x,\mathbf e_y$: 3절.
- 정사영, 수선의 발 $F$, 부호 있는 길이 $s$, 각 $\varphi$: 5절. 일상어 «그림자»는 직관 설명에만 쓰고 정의는 수선의 발로 한다.
- 내적: 6절. 나머지 $\mathbf r$: 7절.
- 각도 범위와 부호는 기초 2의 약속을 따른다. $\varphi$의 부호는 $\cos$에 영향이 없으므로 실험의 읽기 값은 $0^\circ$–$180^\circ$의 크기로 보인다.

## 강한 주장과 증명 의무

| 주장 | 형태 | 의무 | 닫는 자리 |
|---|---|---|---|
| 모든 $\mathbf a,\mathbf b$에 대해 $\mathbf a+\mathbf b=\mathbf b+\mathbf a$ | 모든 …에 대해 | 완전성 | 1절. 성분마다 수의 덧셈은 순서와 무관하다 |
| 모든 $k$, $\mathbf a$에 대해 $\lVert k\mathbf a\rVert=|k|\lVert\mathbf a\rVert$ | 모든 …에 대해 | 완전성 | 2절. $\sqrt{k^2a_x^2+k^2a_y^2}=\sqrt{k^2}\sqrt{a_x^2+a_y^2}$, $\sqrt{k^2}=|k|$ |
| $k<0$이면 $k\mathbf a$는 $\mathbf a$와 정반대 방향 | 모든 …에 대해 | 완전성 | 2절. $k\mathbf a=|k|(-\mathbf a)$이고 $-\mathbf a$의 끝점 $(-a_x,-a_y)$는 원점에 대해 $\mathbf a$의 끝점 반대편(기초 2의 $(3,4)$/$(-3,-4)$) |
| 모든 벡터는 $a_x\mathbf e_x+a_y\mathbf e_y$ | 모든 …에 대해 | 완전성 | 3절. $a_x\mathbf e_x=(a_x,0)$, $a_y\mathbf e_y=(0,a_y)$의 합 |
| 모든 $\varphi$에 대해 $s=\lVert\mathbf a\rVert\cos\varphi$ | 모든 …에 대해 | 완전성 | 5절. 원점 중심 회전은 길이·각·수직을 보존한다는 사실(종이를 돌리는 것)을 전제로 두고, 돌린 그림에서 기초 2의 결론(모든 각도)을 쓴다 |
| 그림자는 더해지고 실수배된다 | 모든 …에 대해 | 완전성 | 6절 ①. 회전은 그림 전체를 함께 옮기므로 이어 붙인 모양과 실수배 관계가 유지된다 |
| 모든 $\mathbf a$와 단위벡터 $\mathbf u$에 대해 $s=a_xu_x+a_yu_y$ | 모든 …에 대해 | 완전성 | 6절 ①②③ |
| 영벡터가 아닌 두 벡터는 내적이 0일 때에만 수직 | …인 경우에만 | 필요충분 | 6절. $\mathbf a\cdot\mathbf b=\lVert\mathbf a\rVert\lVert\mathbf b\rVert\cos\varphi$, 길이가 양수이므로 $\cos\varphi=0$과 동치. $(-180^\circ,180^\circ]$에서 단위원의 가로 좌표가 0인 곳은 $\pm90^\circ$뿐 |
| $\mathbf r\perp\mathbf u$ | 모든 …에 대해 | 완전성 | 7절. 성분 계산 |
| $F$는 $\ell$ 위에서 가장 가까운 유일한 점 | 유일하다 / 최적이다 | 존재성·유일성 | 7절. $t=s$에서 거리 $\lVert\mathbf r\rVert$, $t\neq s$면 $(s-t)^2>0$이 더해져 더 멀다. 수직인 두 화살표를 이은 모양이 직각삼각형이라는 사실(피타고라스)을 쓴다 |
| 길이는 성분처럼 더해지지 않는다 | 반례 | 반례 하나 | 1절. $5\neq5.40$. «항상 합보다 짧다»(삼각부등식)는 주장하지 않는다 |

증명이 아닌 직관: «그림자», 평행사변형 그림, 단위벡터 둘의 거울 대칭 그림(`mutual-shadow.svg`)은 직관 설명이다. ②의 증명은 $\cos(-\alpha)=\cos\alpha$로 닫는다.

## 근거와 provenance

- 원문(사용자 제공 시리즈 계획, 2026-10-15 대화): 기초 3 «벡터를 더하고 특정 방향으로 투영한다는 것은?», 조작 그림 «화살표 합성, 길이 변경, 한 축으로의 정사영».
- 원문(사용자 제공 기구학 PPT): 4장(부품 원점의 세계 위치에 회전한 local 점을 더함: 벡터의 덧셈), 12장(평면 슬라이더: 단위 축 $\mathbf u$와의 곱 $s=u_x(p_{x2}-p_{x1})+u_y(p_{y2}-p_{y1})$이 축 방향 이동량, 단위 법선과의 곱이 0이라는 조건이 횡이동을 막음), 27장(두 단위 법선으로 투영해 0이면 축 방향에만 남음). 이 글은 관절 구속식은 다루지 않고, 레일 예시의 «축 방향 이동량»과 «벗어난 양» 해석만 가져온다.
- 원문(사용자 제공 공학수학 선형대수 PDF, #243 대응표): 2–5쪽(기하적 벡터, 덧셈·상수배와 성질, 좌표의 덧셈·상수배), 20쪽(일차결합), 133–134쪽(내적의 성질과 표준 내적), 137쪽($\lVert c\mathbf a\rVert=|c|\lVert\mathbf a\rVert$), 149–151쪽(정사영 $\operatorname{proj}_{\mathbf w}\mathbf v=\frac{\mathbf v\cdot\mathbf w}{\mathbf w\cdot\mathbf w}\mathbf w$, $\mathbf v-\mathbf p$의 수직성, 가장 가까운 점). PDF는 내적을 성질로 정의하고 표준 내적을 보기로 든다. 이 글은 정사영의 기하에서 출발해 성분 공식을 유도하는 순서를 쓴다(입문 독자에 맞춘 작성자 결정). 일차결합·부분공간·복소내적·코시–슈바르츠는 쓰지 않는다.
- 승인된 추가: 위 계획을 입문 독자에게 맞춘 설명 전체. 예시 값($\mathbf a=(3,1)$, $\mathbf b=(1,2)$, 실수배의 $(2,1)$, 정사영의 $(1,3)$과 $\mathbf u=(0.6,0.8)$, 수직 예 $(-4,3)$, 두 막대 $(\sqrt3,2)$), 레일 이야기, 회전 논증과 «서로에게 같은 그림자» 논증의 구성은 작성자 추가다.
- 공개 대조(2026-10-21 확인): OpenStax *Calculus Volume 3* §2.1 Vectors in the Plane(꼬리를 머리에 놓는 덧셈, 평행사변형 방법, $k\mathbf v$의 크기 $|k|$배와 $k<0$이면 반대 방향, 성분의 덧셈·실수배, $\mathbf i,\mathbf j$와 $\mathbf v=x\mathbf i+y\mathbf j$), §2.3 The Dot Product(성분 내적, $\mathbf u\cdot\mathbf v=\lVert\mathbf u\rVert\lVert\mathbf v\rVert\cos\theta$, 영벡터가 아닌 두 벡터는 내적이 0일 때에만 직교, scalar projection $\operatorname{comp}_{\mathbf u}\mathbf v$와 vector projection, $\mathbf q=\mathbf v-\mathbf p$가 $\mathbf p$에 직교).
- 비공개 원천의 존재와 경로를 게시 본문에 드러내지 않는다. 공개 문헌만 본문에 연결한다.

## 계산 예시 (재계산용)

| 입력 | 결과 |
|---|---|
| $(3,1)+(1,2)$ | $(4,3)$, 길이 5 |
| $\lVert(3,1)\rVert+\lVert(1,2)\rVert$ | $\sqrt{10}+\sqrt5\approx3.162+2.236=5.398\approx5.40$ |
| $(\sqrt3,1)+(0,1)$ | $(\sqrt3,2)\approx(1.73,2)$ |
| $2(2,1)$, $0.5(2,1)$, $-(2,1)$, $0(2,1)$ | $(4,2)$, $(1,0.5)$, $(-2,-1)$, $(0,0)$. 길이 $2\sqrt5$, $\sqrt5/2$, $\sqrt5$, 0 ($\sqrt5\approx2.236$) |
| $(3,1)=3\mathbf e_x+1\mathbf e_y$ | — |
| $\mathbf u=(3,4)/5$ | $(0.6,0.8)$, 길이 $\sqrt{0.36+0.64}=1$ |
| $(1,3)\cdot(0.6,0.8)$ | $0.6+2.4=3$ |
| 정사영 $3\mathbf u$ | $(1.8,2.4)$ |
| 나머지 $(1,3)-(1.8,2.4)$ | $(-0.8,0.6)$, 길이 1, $\mathbf r\cdot\mathbf u=-0.48+0.48=0$ |
| $\lVert(1,3)\rVert^2$ | $10=3^2+1^2$ |
| $\cos\varphi=3/\sqrt{10}$ | $\approx0.949$, $\varphi\approx18.43^\circ$ |
| $(-4,3)\cdot(3,4)$ | $-12+12=0$ (수직) |
| $(-3,1)\cdot(0.6,0.8)$ | $-1.8+0.8=-1$ (음수) |

## 도판

`public/images/robotics-vector-projection/`. `docs/design/DIAGRAM_PALETTE.md`의 18색만 소문자로 쓴다. 모든 파일에 `width`·`height`·`viewBox`를 둔다. 내부 id는 `rvp-` 접두어.

색의 역할(작성자 결정): $\mathbf a$는 파랑(`#93c5fd`, 주목). $\mathbf b$는 보라(`#a78bfa`): 두 화살표를 갈라야 하는데 앰버·초록은 기초 2부터 가로·세로 성분에 쓰고 있어서다. 합과 방향 $\mathbf u$는 흰색(`#e2e8f0`). 축 방향 성분과 정사영은 앰버(`#fbbf24`), 그에 수직인 성분과 나머지는 초록 점선(`#4ade80`). 정사영을 «$\mathbf u$를 가로축으로 돌린 그림의 가로 성분»으로 설명하므로 기초 2의 가로·세로 색과 뜻이 이어진다. 직선 $\ell$은 `#94a3b8` 점선(뜻을 지므로 `#475569`를 쓰지 않는다), 축 `#64748b`, 격자 `#475569`.

| 파일 | 내용 |
|---|---|
| `sum.svg` | $\mathbf a=(3,1)$ 다음 $\mathbf b=(1,2)$, 합 $(4,3)$. 순서를 바꾼 길을 점선으로 그려 평행사변형 |
| `multiples.svg` | $(2,1)$의 $2$배, $0.5$배, $-1$배, $0$배를 네 칸에. 각 칸에 기준 $\mathbf a$를 옅게 |
| `unit-axes.svg` | $\mathbf e_x$ 세 개(앰버)와 $\mathbf e_y$ 하나(초록)를 이어 $(3,1)$ |
| `shadow.svg` | $\mathbf a=(1,3)$, $\mathbf u=(0.6,0.8)$, $\ell$, 발 $F(1.8,2.4)$, 정사영, 나머지, 직각 표시, $\varphi$ |
| `shadow-signs.svg` | $\mathbf u$를 오른쪽으로 돌린 그림 세 칸: $\varphi=50^\circ,90^\circ,140^\circ$에서 $s>0$, $s=0$, $s<0$ |
| `mutual-shadow.svg` | $\mathbf e_x$와 $\mathbf u$(사이각 $40^\circ$)가 서로에게 드리운 길이 $\cos40^\circ$의 그림자, 두 직각삼각형이 사이각의 이등분선에 대해 거울 대칭 |
| `sum-lab.svg` | 실험 1 첫 화면 |
| `projection-lab.svg` | 실험 2 첫 화면 |

## 실험

기초 1·2의 실험 기반(파일명 `-lab.svg`, 루트 `data-lab`, 닫힌 등록부, 정적 SVG = 첫 화면, 손잡이 터치 처리)을 그대로 쓴다.

### `vector-sum`

- 상태: $\mathbf a$, $\mathbf b$의 성분, 각각 $[-3,3]$, $0.5$ 단위. 처음은 $\mathbf a=(3,1)$, $\mathbf b=(1,2)$.
- 조작: 파란 점($\mathbf a$의 끝)과 보라 마름모(이어 붙인 $\mathbf b$의 끝, 곧 합의 끝)를 끈다. 보라 마름모를 끌면 $\mathbf b$만 바뀌고, 파란 점을 끌면 $\mathbf a$가 바뀌며 $\mathbf b$는 그대로 따라온다. 키보드 경로는 기초 1처럼 대상 선택(a/b)과 $x$, $y$ range 입력. 처음으로 버튼.
- 표시: $\mathbf a$(파랑), 이어 붙인 $\mathbf b$(보라), 합(흰색, 6px로 굵게 아래에 깔고 화살촉도 16px로 키운다: $\mathbf a$와 $\mathbf b$가 같은 방향이면 그 위에 포개지므로 테두리로 보이게 한다. 코드 리뷰, 2026-10-21), 순서를 바꾼 길(같은 색 점선, 화살촉 없음). 읽기 값: $\mathbf a$, $\mathbf b$, $\mathbf a+\mathbf b$, $\lVert\mathbf a\rVert+\lVert\mathbf b\rVert$와 $\lVert\mathbf a+\mathbf b\rVert$.
- 라벨: 화살표 이름은 움직이는 라벨 대신 고정 범례로 둔다. 세 화살표 모두 영벡터가 될 수 있어 붙일 자리가 사라지기 때문이다(SVG_LABS 규약). 화살촉은 손잡이 앞에서 멈추도록 뒤로 당겨 그리므로, 화살촉이 꼬리를 넘는 짧은 화살표(26px 미만, 길이 0 포함)에는 붙이지 않는다. 그 값은 SVG의 marker 크기에서 테스트가 확인한다.

### `vector-projection`

- 상태: $\mathbf a$ 성분 $[-3,3]$, 방향 점 $D$ 성분 $[-4,4]$, 모두 $0.5$ 단위. $\mathbf u=D/\lVert D\rVert$. 처음은 $\mathbf a=(1,3)$, $D=(3,4)$라 $\mathbf u=(0.6,0.8)$이 정확히 나온다. 방향을 각도 입력 대신 격자점으로 받는 이유가 이것이다(각도를 1° 단위로 받으면 $53.13^\circ$를 고를 수 없다). $D$는 원점에 둘 수 없다(방향이 없다). 한 축씩 바꾸는 입력(방향키)이 원점에 닿으면 같은 방향으로 한 칸 더 가서 0을 건너고, 끌기는 두 좌표를 한꺼번에 적용해 합친 결과가 원점일 때만 거부한다(코드 리뷰, 2026-10-21: 거부만 하면 방향키가 ±0.5에서 멈추고 대각선 끌기가 한 박자 늦었다).
- $\mathbf a$를 $[-3,3]$으로 묶는 이유: $\lVert\mathbf a\rVert\le3\sqrt2\approx4.24$이므로 발 $F$가 반지름 $4.24$ 안에 머물러 $\pm4.5$ 그림 밖으로 나가지 않는다.
- 조작: 파란 점($\mathbf a$의 끝)과 흰 마름모($D$)를 끈다. 키보드 경로는 대상 선택과 $x$, $y$ range 입력. 처음으로 버튼.
- 표시: 직선 $\ell$(그림 사각형에 잘라 그림), 길이 1인 $\mathbf u$, $\mathbf a$, 정사영 $\overrightarrow{OF}$(앰버, 굵게), 나머지(초록 점선), $F$의 직각 표시(나머지가 18px보다 짧으면 숨김: 표시 9px과 $\mathbf a$ 손잡이 반지름 8px). $\mathbf u$는 정사영 위에 포개지지 않게 $\ell$ 옆 16px에 띄워 그리고, 오른쪽이 O 라벨을 지나면 왼쪽에 그린다. 읽기 값: $\mathbf a$, $\mathbf u$, $\mathbf a\cdot\mathbf u$의 성분 계산, $\lVert\mathbf a\rVert\cos\varphi$, 정사영, 나머지와 그 길이. $\mathbf a$가 영벡터면 $\varphi$는 «정할 수 없음».
- 라벨: 고정 범례. 정사영·나머지·$\mathbf a$ 모두 길이 0이 될 수 있다.

### 두 실험 공통

- 모델이 모든 좌표를 계산하고, 정적 SVG가 첫 화면과 같은지 테스트로 묶는다.
- 손잡이가 겹치면(영벡터 등) 맨 위에 그린 쪽이 아니라 포인터에서 가장 가까운 손잡이를 잡고, 같은 거리면 선택 상자에서 고른 쪽을 잡는다(`src/labs/pick-handle.mjs`).
- 런타임은 화살촉 참조를 `data-marker`에서 읽는다. 첫 화면의 `marker-end`에 기대면 첫 화면에 짧은 화살표가 있을 때 참조를 잃는다.
- 움직이는 라벨이 없으므로 라벨 겹침 스윕 대신, 입력이 만들 수 있는 상태 전체(실험 1: $13^4$, 실험 2: $13^2\times(17^2-1)$)를 훑는다. 모델의 식을 되풀이하지 않고 그림에서 읽은 기하로 독립 검사한다: 그린 요소가 그림 사각형 안에 있는지, 평행사변형의 마주 보는 변이 같은지, 화살촉 규칙, 실험 2에서 나머지가 $\mathbf u$에 수직이고 $\mathbf a=s\mathbf u+\mathbf r$인지, 직각 표시의 두 다리가 $\ell$을 따라 O 쪽과 나머지를 따라 $\mathbf a$ 쪽을 향하고 손잡이에 가리지 않는지, $\mathbf u$가 $\ell$과 평행하고 16px 떨어져 O 라벨과 눈금 숫자를 지나지 않는지. 모델에 결함을 하나씩 심어 테스트가 잡는지도 확인했다(27개 모두 잡힘, scratchpad의 변이 스크립트).
- 자동 재생은 없다.

## 검증

- `npm run test:js`: 두 실험 모델(본문 예시 값, 교환법칙, 실수배, 드래그, 상태 전체 검사), 정적 SVG = 첫 화면, 플러그인·로더 등록.
- `npm run build`(개발 서버가 떠 있으면 격리 복사본), `python .claude/review_post.py <글>`, `--gate`.
- 독립 L1–L7 리뷰와 `--finalize --strict`는 PR 완료 조건이다. 작성자의 자체 검증을 독립 리뷰로 기록하지 않는다.
- 브라우저 렌더, 실기기 터치, 인쇄는 작성자가 볼 수 없다. 사용자 확인 항목으로 넘긴다.
