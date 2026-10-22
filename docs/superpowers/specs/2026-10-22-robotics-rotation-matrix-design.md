# 로보틱스 기초 4 — 회전행렬의 두 열

- 날짜: 2026-10-22
- 브랜치: `feat/robotics-rotation-matrix` (origin/main 기준. 기초 1–3은 모두 머지됐다)
- 산출물: 본편 `robotics-rotation-matrix.md`, 정적 SVG 4장, 조작 실험 1개(`rotation-lab.svg` + `rotation-matrix`)
- 독자: 기초 1에서 사용자가 확인한 «고교 수학을 잊은 독자»를 이어받는다. 이번 편도 사용자는 바로 작성을 요청했으므로(2026-10-22 "기초 4 드가자"), 독자와 목적을 다시 묻지 않고 시리즈의 확인값을 쓴다.
- 목적: 프로젝트의 기구학을 삼각함수·벡터부터 그림으로 공부하고 블로그로 정리한다(기초 1–3과 같음).

## 질문과 결론

막대가 원점에 붙어 있고, 막대에 달린 집게의 끝은 막대를 따라 3, 막대의 왼쪽으로 1인 자리에 있다. 막대를 $\theta$만큼 돌리면 집게 끝은 어디로 가는가?

- 막대에 붙은 두 축(막대 방향 $\mathbf e_x'$, 그 왼쪽 $\mathbf e_y'$)도 함께 돈다. 돌아간 두 축은 $\mathbf e_x'=(\cos\theta,\sin\theta)$, $\mathbf e_y'=(-\sin\theta,\cos\theta)$다.
- 막대에서 읽은 좌표 $(s_x,s_y)$는 돌려도 그대로이고, 돌아간 점은 $s_x\mathbf e_x'+s_y\mathbf e_y'$다.
- 두 축의 성분을 열로 나란히 적은 표가 회전행렬 $R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$이고, 행렬과 열벡터의 곱은 열을 성분만큼 더하는 계산으로 정한다. 시리즈 계획의 질문 «회전행렬의 숫자는 어디서 나오는가?»의 답은 «돌아간 두 축의 성분»이다.
- 거꾸로 고정 좌표에서 막대 좌표를 되찾을 때는 기초 3의 정사영을 쓴다: $s_x=\mathbf p\cdot\mathbf e_x'$, $s_y=\mathbf p\cdot\mathbf e_y'$. 이 표는 $R(\theta)$의 열을 행으로 놓은 것이고 $R(-\theta)$와 같다.
- 덤으로 각의 덧셈 공식이 나온다. 다음 글(평면 2관절 팔)의 두 번째 막대 방향 $\theta_1+\theta_2$를 성분으로 풀 때 쓴다.

기초 3의 «이어지는 글» callout이 예고한 내용(«돌아간 두 단위벡터의 실수배를 더해 얻는다», «두 쌍의 수가 회전행렬의 두 열이 되는 과정»)과 기초 3 본문 3절 끝의 약속(«축을 돌려 $\mathbf e_x$와 $\mathbf e_y$가 함께 돌아간 뒤에도 같은 방식으로 점을 나타낼 수 있는지는 다음 글에서 확인한다»)을 닫는다.

## 본문 순서

도입: 기초 2는 막대 끝점, 기초 3은 막대 둘을 이어 붙인 끝점을 구했다. 이번에는 막대에서 옆으로 비켜 난 점(집게 끝)이다. 막대는 길이 4이고 집게는 막대를 따라 3인 자리에서 옆으로 나온다. 극좌표로 풀면 집게 끝의 각 $\alpha$에 $\theta$를 더한 각의 코사인이 필요한데, 그 공식을 몰라도 되는 길을 간다.

1. **막대에 붙은 두 축** — 막대 방향 단위벡터 $\mathbf e_x'$와 그것을 반시계로 $90^\circ$ 돌린 $\mathbf e_y'$(막대가 가리키는 쪽을 앞으로 볼 때 왼쪽). $\theta=0$이면 $\mathbf e_x,\mathbf e_y$와 같다. 집게 끝 $P$는 $3\mathbf e_x'+1\mathbf e_y'$이고, 이 두 수 $(3,1)$을 막대 좌표 $(s_x,s_y)$라 부른다. 고정된 $x$, $y$축으로 읽은 좌표는 고정 좌표 $(p_x,p_y)$. 집게는 막대에 고정돼 있으므로 막대 좌표는 돌려도 그대로다. 교재는 둘을 local 좌표와 world 좌표라 부르고, 뒤의 글에서 다시 다룬다(이름만 소개). 질문을 «$\mathbf e_x'$, $\mathbf e_y'$의 고정 좌표는?»으로 바꾼다. 도판 `rod-frame.svg`.
2. **돌아간 두 축의 성분** — 전제: 원점 중심으로 그림 전체를 돌리면 이어 붙인 화살표는 이어 붙은 채, 실수배는 실수배인 채 돈다(기초 3 «그림자의 길이를 성분으로 계산하기» 첫째 단계에서 쓴 사실). $\mathbf e_x'$는 길이 1인 막대를 $\theta$ 돌린 끝점이라 기초 2에 따라 $(\cos\theta,\sin\theta)$. $90^\circ$ 규칙: $90^\circ$ 돌리면 $\mathbf e_x\to\mathbf e_y=(0,1)$, $\mathbf e_y\to(\cos180^\circ,\sin180^\circ)=(-1,0)$이므로 전제에 따라 $(a,b)=a\mathbf e_x+b\mathbf e_y\to a(0,1)+b(-1,0)=(-b,a)$. 예 $(3,1)\to(-1,3)$. $\mathbf e_y'$는 $\mathbf e_x'$를 $90^\circ$ 더 돌린 방향이라($\mathbf e_y$가 $\mathbf e_x$보다 $90^\circ$ 앞서 있고, 같은 원점을 중심으로 돌린 각은 더해진다) $(-\sin\theta,\cos\theta)$. 검산: 길이 1, $\mathbf e_x'\cdot\mathbf e_y'=0$. 예: $\cos\theta=0.6$, $\sin\theta=0.8$($\theta\approx53.13^\circ$, 기초 2의 $\operatorname{atan2}(4,3)$)이면 $(0.6,0.8)$, $(-0.8,0.6)$ — 기초 3의 $\mathbf u$와 나머지 $\mathbf r$이다. 도판 `quarter-turn.svg`, `turned-axes.svg`.
3. **돌아간 점은 두 축의 실수배를 더한 것이다** — 전제에 따라 $s_x\mathbf e_x+s_y\mathbf e_y$를 돌리면 $s_x\mathbf e_x'+s_y\mathbf e_y'$. 성분으로 $(s_x\cos\theta-s_y\sin\theta,\;s_x\sin\theta+s_y\cos\theta)$. 예 $3(0.6,0.8)+1(-0.8,0.6)=(1,3)$. $3\mathbf e_x'=(1.8,2.4)$는 기초 3의 수선의 발 $F$다. 길이 검산: 성분 식을 제곱해 더하면 엇갈린 항이 지워지고 $\cos^2\theta+\sin^2\theta=1$이 남아 $s_x^2+s_y^2$ — 모든 $\theta$, $s$에서 길이가 그대로다. 도판 `turned-point.svg`.
4. **두 열을 나란히 적으면 회전행렬이다** — 행렬(행·열), 열벡터(행렬 옆에서는 세로로 적되 같은 벡터), 행렬과 열벡터의 곱 $\begin{bmatrix}\mathbf c_1&\mathbf c_2\end{bmatrix}\begin{bmatrix}s_x\\s_y\end{bmatrix}=s_x\mathbf c_1+s_y\mathbf c_2$(정의). $R(\theta)$를 정하고 $\mathbf p=R(\theta)\,\mathbf s$. 첫째 열 = $R(\theta)\mathbf e_x$ = 돌아간 $x$축, 둘째 열 = 돌아간 $y$축. 행으로 읽기: 각 행과 열벡터의 내적이 고정 좌표 하나($p_x=\cos\theta\,s_x-\sin\theta\,s_y$). 같은 네 곱을 묶는 순서만 다르다. 예 $\begin{bmatrix}0.6&-0.8\\0.8&0.6\end{bmatrix}\begin{bmatrix}3\\1\end{bmatrix}=\begin{bmatrix}1\\3\end{bmatrix}$. $R(90^\circ)=\begin{bmatrix}0&-1\\1&0\end{bmatrix}$이 $90^\circ$ 규칙, $R(0^\circ)$는 점을 움직이지 않는다. 회전을 여러 번 잇는 공간 회전에서 이 표기가 필요해진다는 예고만 둔다(행렬끼리의 곱은 다루지 않는다).
5. **막대를 직접 돌려 보기** — 실험.
6. **거꾸로: 정사영으로 막대 좌표 되찾기** — 고정 좌표 $\mathbf p$를 알 때 막대 좌표를 구한다. $\mathbf e_x'$, $\mathbf e_y'$는 서로 수직인 단위벡터이므로 $\mathbf p\cdot\mathbf e_x'=s_x(\mathbf e_x'\cdot\mathbf e_x')+s_y(\mathbf e_y'\cdot\mathbf e_x')=s_x$. 내적이 덧셈과 실수배에 나뉘어 들어가는 성질은 성분 정의에서 바로 나온다(기초 3 첫째 단계의 «정사영 길이도 더해지고 실수배된다»와 같은 내용). $s_x=p_x\cos\theta+p_y\sin\theta$, $s_y=-p_x\sin\theta+p_y\cos\theta$. 예 $(1,3)\cdot(0.6,0.8)=3$, $(1,3)\cdot(-0.8,0.6)=1$ — 기초 3의 정사영 길이 3과 나머지 길이 1. 행렬로 쓰면 $R(\theta)$의 두 열이 두 행이 된 표이고, $\cos(-\theta)=\cos\theta$, $\sin(-\theta)=-\sin\theta$이므로 $R(-\theta)$와 같다(거꾸로 돌리기). 행과 열을 맞바꾼 행렬을 전치행렬 $R^{\mathsf T}$라 부른다(이름만 소개). 둘을 헷갈리면 점이 반대쪽으로 돈다.
7. **두 각의 합 공식** — 길이 1이고 각 $\alpha$인 화살표 $(\cos\alpha,\sin\alpha)$를 $\theta$ 돌리면 각 $\alpha+\theta$인 화살표다(전제). 3절의 식으로 돌린 성분과 비교해 $\cos(\alpha+\theta)=\cos\alpha\cos\theta-\sin\alpha\sin\theta$, $\sin(\alpha+\theta)=\sin\alpha\cos\theta+\cos\alpha\sin\theta$. 검산 $30^\circ+60^\circ$. 집게 예로 보면 $(1,3)$이 $(3,1)$의 각에 $\theta$를 더한 방향이다.
8. 핵심 정리 callout → 이어지는 글 callout(기초 5: 관절 두 개. 두 번째 막대는 첫 막대에 붙은 축으로 놓이므로 이 글의 회전행렬과 기초 3의 덧셈으로 손끝을 구한다. 미발행이라 링크 없음) → 참고 자료.

절 제목에 번호를 쓰지 않는다. `numbered: true`가 붙인다.

## 용어와 기호 도입 순서

- 기초 1–3의 표기를 이어 쓴다: 굵은 소문자 벡터, 성분 $(a_x,a_y)$, $\lVert\cdot\rVert$, $\mathbf e_x$, $\mathbf e_y$, 내적 $\cdot$. 각도는 기초 2의 약속(반시계가 양수, 대표 각도 $(-180^\circ,180^\circ]$)을 따른다.
- 막대 좌표 $(s_x,s_y)$, 고정 좌표 $(p_x,p_y)$, 막대의 두 축 $\mathbf e_x'$, $\mathbf e_y'$: 1절. 기호 $s$와 $p$는 이 분야 교재의 관례(local 점 $s$, world 점 $p$)를 따른다. $P$는 점 이름, $\mathbf s$, $\mathbf p$는 두 좌표를 성분으로 하는 벡터.
- 행렬, 행·열, 열벡터, 행렬과 열벡터의 곱, $R(\theta)$: 4절. 전치행렬: 6절(이름만).
- 열벡터 표기는 행렬 옆에서만 쓰고 본문은 괄호 표기를 유지한다(작성자 결정. 시리즈 메모의 미결정 항목 «점·벡터 표기»를 이 편에서는 «괄호 표기 + 행렬 옆 열벡터»로 처리한다. 열벡터와 괄호 표기가 같은 벡터라는 점을 본문에 적는다).

## 강한 주장과 증명 의무

| 주장 | 형태 | 의무 | 닫는 자리 |
|---|---|---|---|
| 모든 $\theta$에 대해 $\mathbf e_x'=(\cos\theta,\sin\theta)$ | 모든 …에 대해 | 완전성 | 2절. 기초 2의 정의(길이 1인 막대를 $\theta$ 돌린 끝점)가 모든 각도에서 성립 |
| 모든 $(a,b)$에 대해 $90^\circ$ 회전은 $(a,b)\to(-b,a)$ | 모든 …에 대해 | 완전성 | 2절. 전제 + $\mathbf e_x$, $\mathbf e_y$의 상(기초 2의 $90^\circ$, $180^\circ$ 끝점). 부호는 $a$, $b$의 부호와 무관하게 식이 처리한다 |
| 모든 $\theta$에 대해 $\mathbf e_y'=(-\sin\theta,\cos\theta)$ | 모든 …에 대해 | 완전성 | 2절. $\mathbf e_y'$는 $\mathbf e_x'$를 $90^\circ$ 돌린 화살표(같은 원점 중심 회전의 각은 더해진다) + $90^\circ$ 규칙 |
| 모든 $\mathbf s$, $\theta$에 대해 돌린 점 $=s_x\mathbf e_x'+s_y\mathbf e_y'$ | 모든 …에 대해 | 완전성 | 3절. 전제 |
| 모든 $\mathbf s$, $\theta$에 대해 길이가 그대로 | 모든 …에 대해 | 완전성 | 3절. 성분 계산 $(s_xc-s_ys)^2+(s_xs+s_yc)^2=(s_x^2+s_y^2)(c^2+s^2)$ |
| 열로 읽기와 행으로 읽기가 같은 값 | 모든 …에 대해 | 완전성 | 4절. 두 방법 모두 같은 네 곱 $\cos\theta\,s_x$, $-\sin\theta\,s_y$, $\sin\theta\,s_x$, $\cos\theta\,s_y$를 성분별로 더한다 |
| 모든 $\mathbf p$, $\theta$에 대해 $s_x=\mathbf p\cdot\mathbf e_x'$, $s_y=\mathbf p\cdot\mathbf e_y'$ | 모든 …에 대해 | 완전성 | 6절. $\mathbf p$는 3절에 따라 $s_x\mathbf e_x'+s_y\mathbf e_y'$이고, 내적의 분배(성분 정의) + 2절의 $\mathbf e_x'\cdot\mathbf e_x'=1$, $\mathbf e_y'\cdot\mathbf e_x'=0$ |
| 되찾는 표는 $R(-\theta)$와 같다 | 모든 …에 대해 | 완전성 | 6절. 성분 비교. $\cos(-\theta)=\cos\theta$(기초 3), $\sin(-\theta)=-\sin\theta$($x$축에 대해 뒤집으면 세로 좌표의 부호만 바뀐다) |
| 모든 $\alpha$, $\theta$에 대해 덧셈 공식 | 모든 …에 대해 | 완전성 | 7절. 3절의 식 + 전제(원점 중심으로 $\theta$ 돌리면 모든 방향의 각이 $\theta$만큼 는다) + 기초 2의 정의 |

전제는 하나다: 원점 중심 회전은 길이·각을 보존하고, 그림 전체를 함께 옮기므로 이어 붙인 모양과 실수배 관계를 유지한다(종이를 돌리는 것). 기초 3이 같은 전제를 썼고, 이 글도 증명하지 않고 전제로 밝힌다. 길이 보존은 3절에서 성분 계산으로 다시 확인한다.

퇴화 사례: $\mathbf s=\mathbf 0$이면 돌려도 원점. $\theta=0$이면 $R$은 점을 움직이지 않는다. 회전에는 영벡터의 방향 문제가 생기지 않는다(모든 식이 그대로 성립). 실험에서 막대 끝 손잡이를 원점으로 끌면 각을 정할 수 없어 현재 각을 유지한다(기초 2 실험과 같은 처리).

증명이 아닌 직관: `turned-axes.svg`의 두 직각삼각형(한쪽을 $90^\circ$ 돌리면 다른 쪽)은 직관이다. $\mathbf e_y'$의 증명은 $90^\circ$ 규칙으로 닫는다.

## 근거와 provenance

- 원문(사용자 제공 시리즈 계획, 2026-10-15 대화): 기초 4 «회전행렬의 숫자는 어디서 나오는가?», 조작 그림 «두 기준축을 회전시키고, 그 좌표가 행렬의 두 열이 되는 과정».
- 원문(사용자 제공 기구학 PPT): 1·4장(local 점 $(s_x,s_y)$를 $\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$로 돌리고 부품 원점을 더함, «첫 행은 세계 x, 둘째 행은 세계 y를 계산한다»), 3장(local frame의 세 축이 부품과 함께 돈다, local 좌표는 일정), 7장(초기 회전을 되돌리는 행렬 $\begin{bmatrix}\cos\theta_0&\sin\theta_0\\-\sin\theta_0&\cos\theta_0\end{bmatrix}$로 local 좌표를 구함), 24장(«각 행은 세계 x, y, z를 계산하고, 각 열은 local x, y, z의 기여를 나타낸다»). 이 글은 원점 이동($X$, $Y$를 더하는 부분)과 3차원 회전은 다루지 않는다(시리즈 경계: 기초 4 = 원점 중심 평면 회전, A1 = 이동과 local/world, A3 = 공간 회전. 기초 1 스펙 56행).
- 원문(사용자 제공 공학수학 선형대수 PDF, #243 대응표): 40쪽(열벡터와 $\mathbb R^m$의 벡터를 동일시), 41–42쪽(선형사상은 $L(\mathbf e_1),\dots,L(\mathbf e_n)$이 정하고, 그것을 늘어 쓴 행렬의 $j$번째 열이 $L(\mathbf e_j)$), 44쪽(원점 중심 $\theta$ 회전의 행렬, $L(\mathbf e_1)=(\cos\theta,\sin\theta)$, $L(\mathbf e_2)=(-\sin\theta,\cos\theta)$), 45–46쪽(행렬과 열벡터의 곱 = 열의 일차결합 = 성분 식), 49쪽(회전 두 번의 합성에서 덧셈 공식을 얻음). PDF는 선형사상을 성질로 정의하고 행렬을 그 표현으로 얻는다. 이 글은 «선형사상»이라는 이름 없이 회전의 전제(이어 붙인 모양과 실수배 유지)에서 출발하고, 덧셈 공식은 행렬의 곱 대신 한 점을 돌리는 계산으로 얻는다(입문 독자에 맞춘 작성자 결정). 행렬끼리의 곱, 일반 선형사상, 50쪽의 곱셈 성질은 쓰지 않는다.
- 승인된 추가: 위 계획을 입문 독자에게 맞춘 설명 전체. 집게 이야기와 예시 값(막대 좌표 $(3,1)$, $\cos\theta=0.6$·$\sin\theta=0.8$인 각, 결과 $(1,3)$, $90^\circ$ 예 $(-1,3)$), $90^\circ$ 규칙으로 $\mathbf e_y'$를 얻는 논증, 기초 3의 $F$·$\mathbf r$과 잇는 해석, 6절(되찾기)을 PPT 7장의 원점 이동 없는 경우로 가져온 구성, 7절(덧셈 공식)의 배치는 작성자 추가다. 6절과 7절은 원문(PPT 7장, PDF 49쪽)에 있는 내용이고, 기초 3의 정사영과 기초 5의 각 더하기를 잇기 위해 이 편에 둔다.
- 공개 대조(2026-10-22 확인): Margalit·Rabinoff, *Interactive Linear Algebra* §2.3 Matrix Equations(행렬과 벡터의 곱을 열의 일차결합으로 정의, row-column rule), §3.3 Linear Transformations(Subsection 3.3.3: 행렬의 열은 표준 단위벡터의 상 $T(\mathbf e_1),\dots,T(\mathbf e_n)$, 반시계 $\theta$ 회전의 행렬 $\begin{bmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{bmatrix}$). OpenStax *Algebra and Trigonometry 2e* §9.2 Sum and Difference Identities($\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta$, $\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta$).
- 비공개 원천의 존재와 경로를 게시 본문에 드러내지 않는다. 공개 문헌만 본문에 연결한다. «교재는 local 좌표와 world 좌표라 부른다»는 이 분야의 일반 용어 소개이고 비공개 원천을 가리키지 않는다.

## 계산 예시 (재계산용)

$c=\cos\theta$, $s=\sin\theta$로 줄여 쓴다.

| 입력 | 결과 |
|---|---|
| $c=0.6$, $s=0.8$ | $c^2+s^2=0.36+0.64=1$, $\theta=\operatorname{atan2}(0.8,0.6)\approx53.13^\circ$ ($0.927$ rad) |
| $\mathbf e_x'$, $\mathbf e_y'$ | $(0.6,0.8)$, $(-0.8,0.6)$. 내적 $-0.48+0.48=0$ |
| $90^\circ$: $(3,1)$ | $(-1,3)$ |
| $3\mathbf e_x'+1\mathbf e_y'$ | $(1.8-0.8,\;2.4+0.6)=(1,3)$. 길이 $\sqrt{10}$ 그대로 |
| 행으로: $0.6\cdot3+(-0.8)\cdot1$, $0.8\cdot3+0.6\cdot1$ | $1$, $3$ |
| $(1,3)\cdot(0.6,0.8)$, $(1,3)\cdot(-0.8,0.6)$ | $3$, $1$ |
| $R(-\theta)$ | $\begin{bmatrix}0.6&0.8\\-0.8&0.6\end{bmatrix}$ |
| 덧셈 공식 $\alpha=30^\circ$, $\theta=60^\circ$ | $\cos90^\circ=\tfrac{\sqrt3}{2}\cdot\tfrac12-\tfrac12\cdot\tfrac{\sqrt3}{2}=0$, $\sin90^\circ=\tfrac12\cdot\tfrac12+\tfrac{\sqrt3}{2}\cdot\tfrac{\sqrt3}{2}=1$ |
| $(3,1)$의 각 $\alpha$: $\cos\alpha=3/\sqrt{10}$, $\sin\alpha=1/\sqrt{10}$ | $\cos(\alpha+\theta)=(1.8-0.8)/\sqrt{10}=1/\sqrt{10}$, $\sin(\alpha+\theta)=(0.8\cdot3+0.6\cdot1)/\sqrt{10}=3/\sqrt{10}$ → $(1,3)/\sqrt{10}$ |
| 실험 처음 $\theta=30^\circ$, $\mathbf s=(3,1)$ | $\cos30^\circ\approx0.866$, $\sin30^\circ=0.5$, $\mathbf p\approx(2.598-0.5,\;1.5+0.866)=(2.098,\;2.366)$, 읽기 값 $(2.1,\;2.37)$ |

## 도판

`public/images/robotics-rotation-matrix/`. `docs/design/DIAGRAM_PALETTE.md`의 18색만 소문자로 쓴다. 모든 파일에 `width`·`height`·`viewBox`를 둔다. 내부 id는 `rrm-` 접두어.

색의 역할(작성자 결정): $\mathbf e_x$·$\mathbf e_x'$와 그 실수배는 앰버(`#fbbf24`), $\mathbf e_y$·$\mathbf e_y'$와 그 실수배는 초록(`#4ade80`). 기초 3의 `unit-axes.svg`(앰버 $\mathbf e_x$, 초록 $\mathbf e_y$)와 같은 뜻이다. 집게 끝 $P$와 원점에서 $P$로 가는 화살표는 파랑(`#93c5fd`, 주목). 막대는 `#1e293b` 면에 `#64748b` 테두리. 막대에 붙은 격자는 `#475569`(보조선, 뜻을 지지 않는다), 고정 축은 `#64748b`. 실험의 막대 끝 손잡이는 흰 마름모(`#e2e8f0`).

| 파일 | 내용 |
|---|---|
| `rod-frame.svg` | 두 칸. 돌리기 전: 막대가 $x$축 위, $\mathbf e_x'=\mathbf e_x$, $\mathbf e_y'=\mathbf e_y$, $P=3\mathbf e_x'+1\mathbf e_y'$. 돌린 뒤($c=0.6$, $s=0.8$): 막대·두 축·격자가 함께 돌고 $P$는 같은 막대 좌표 $(3,1)$ 자리 |
| `quarter-turn.svg` | $(3,1)=3\mathbf e_x+1\mathbf e_y$와 그것을 $90^\circ$ 돌린 $3(0,1)+1(-1,0)=(-1,3)$ |
| `turned-axes.svg` | $\mathbf e_x'$, $\mathbf e_y'$와 두 성분 삼각형. 다리에 $\cos\theta$, $\sin\theta$ |
| `turned-point.svg` | 돌린 격자 위에서 $3\mathbf e_x'$(앰버)를 따라 $(1.8,2.4)$, 이어 $\mathbf e_y'$(초록)를 따라 $(1,3)$. 고정 축 눈금으로 $(1,3)$을 읽을 수 있게 한다 |
| `rotation-lab.svg` | 실험 첫 화면 |

## 실험 `rotation-matrix`

기초 1–3의 실험 기반(파일명 `-lab.svg`, 루트 `data-lab`, 닫힌 등록부, 정적 SVG = 첫 화면, 손잡이 터치 처리, `pick-handle`, `data-marker`, 읽기 값의 `=`/`≈` 규칙)을 그대로 쓴다.

- 상태: 각 $\theta$(정수 도, $(-180^\circ,180^\circ]$, 기초 2 실험과 같은 감싸기)와 막대 좌표 $\mathbf s$(각 성분 $[-3,3]$, $0.5$ 단위). 처음은 $\theta=30^\circ$, $\mathbf s=(3,1)$. $c=0.6$인 각은 1° 단위로 고를 수 없다($53^\circ$이면 $\mathbf p\approx(1.01,3)$). 본문 질문에서 이 차이를 짚는다.
- $\mathbf s$를 $[-3,3]$으로 묶는 이유: $\lVert\mathbf p\rVert=\lVert\mathbf s\rVert\le3\sqrt2\approx4.24$라 $\pm4.5$ 그림 안에 머문다. 막대 길이는 4.
- 그리기: 막대·막대 격자·$\mathbf e_x'$·$\mathbf e_y'$·사슬($s_x\mathbf e_x'$ 앰버 점선, 이어 $s_y\mathbf e_y'$ 초록 점선)·$P$로 가는 파란 화살표·두 손잡이를 막대 좌표로 그린 묶음 하나에 넣고, 그 묶음에 `rotate(−θ, O)`만 건다. 그림을 통째로 돌린다는 본문의 전제를 그대로 그리는 방식이다. 고정 축과 눈금은 묶음 밖에 둔다. 격자는 그림 사각형으로 자른다(`clipPath`).
- 눈금 숫자는 그림 사각형 바깥 아래·왼쪽에 둔다. 돌아가는 막대와 화살표가 그림 안의 고정 글자를 지나기 때문이다. 같은 이유로 O와 축 글자는 그림 안에 두지 않고 범례에 적는다.
- 조작: 흰 마름모(막대 끝)를 끌면 $\theta$가 바뀐다(원점과의 $\operatorname{atan2}$, 포인터가 원점이면 유지). 막대 끝은 도는 손잡이라 잡은 자리를 픽셀 오프셋이 아니라 «누른 순간 막대 각 − 포인터 방향»의 각도로 기억한다(코드 리뷰, 2026-10-22: 픽셀 오프셋은 막대가 돌면 손가락 밑에서 밀리고 원점 판정을 O + 오프셋으로 옮겼다). 파란 점 $P$를 끌면 막대 좌표가 바뀐다: 포인터의 고정 좌표를 6절의 내적으로 막대 좌표로 바꾼 뒤 $0.5$ 단위(그린 격자의 반 칸)에 맞춘다. 손잡이가 겹치면 가까운 쪽(`pick-handle`). 키보드 경로는 $\theta$, $s_x$, $s_y$ range 입력 셋. 처음으로 버튼은 끌기 도중이면 끌기도 끝낸다.
- 행렬 표시: 그림 아래에 $R(\theta)\,\mathbf s\;[=|\approx]\;\mathbf p$를 숫자로 적는다. 첫째 열은 앰버, 둘째 열은 초록이라 두 열이 두 화살표와 같은 색이다. 정적 그림에도 남으므로 JavaScript 없이도 첫 화면의 행렬을 읽을 수 있다.
- 읽기 값: $\theta$와 라디안, 첫째 열 $\mathbf e_x'$, 둘째 열 $\mathbf e_y'$, 막대 좌표, $s_x\mathbf e_x'+s_y\mathbf e_y'$의 계산식과 고정 좌표, 길이. 식(행렬 표시, 계산식)은 보이는 수가 모두 정확할 때만 `=`로 잇고 하나라도 반올림했으면 `≈`(`src/labs/readout.mjs`).
- 라벨: 고정 범례. 사슬 조각과 $P$ 화살표는 길이 0이 될 수 있다. 파란 화살표의 화살촉은 손잡이 앞에서 멈추도록 당겨 그리므로 짧은 화살표에는 붙이지 않는다(기준은 SVG의 marker 크기에서 테스트가 확인).
- 검사: 입력이 만들 수 있는 상태 전체($360\times13^2=60{,}840$)를 훑는다. 모델의 식을 되풀이하지 않고, 정적 그림에서 읽은 기하(원점 위치, 단위 길이)와 묶음의 `rotate`를 직접 적용해 그린 $P$의 위치가 $s_x(\cos\theta,\sin\theta)+s_y(-\sin\theta,\cos\theta)$와 같은지, 그림 사각형 안인지, 길이가 같은지, 막대 좌표 되찾기가 원래 $\mathbf s$를 돌려주는지 확인한다. 끌기(막대 끝 → 각, $P$ → 돌린 격자에 맞춘 막대 좌표), 겹친 손잡이, 키보드 감싸기, 음수 0, 읽기 값의 등호 정직성, 정적 그림 = 첫 화면도 검사한다. 모델에 결함을 심는 변이 시험으로 검사의 힘을 확인한다.
- 자동 재생은 없다.

## 검증

- `npm run test:js`: 실험 모델(본문 예시 값, 상태 전체 검사, 드래그, 읽기 값), 정적 SVG = 첫 화면, 플러그인·로더 등록.
- `npm run build`(개발 서버가 떠 있으면 격리 복사본), `python .claude/review_post.py <글>`, `--gate`.
- 독립 L1–L7 리뷰와 `--finalize --strict`는 PR 완료 조건이다. 작성자의 자체 검증을 독립 리뷰로 기록하지 않는다.
- 브라우저 렌더, 실기기 터치, 인쇄는 작성자가 볼 수 없다. resvg 래스터로 근사 확인하고, 나머지는 사용자 확인 항목으로 넘긴다.
