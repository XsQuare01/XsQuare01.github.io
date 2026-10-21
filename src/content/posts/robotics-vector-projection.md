---
title: "벡터의 덧셈과 정사영 — 화살표를 잇고 한 방향으로 그림자 내리기"
date: 2026-10-21T09:00:00+09:00
description: "화살표를 이어 붙이면 성분끼리 더해지고, 수를 곱하면 길이와 방향이 바뀐다. 길이 1인 벡터 u의 방향으로 내린 정사영의 길이는 내적 a·u로 계산하고, 그 나머지는 u에 수직이다."
tags: ["Robotics", "Kinematics", "Vector"]
category: robotics
difficulty: 입문
numbered: true
---

로봇 팔의 첫 막대 끝에 두 번째 막대가 붙어 있다고 하자. [앞 글](/blog/robotics-sine-cosine)에서는 원점에 붙은 막대 하나의 끝점을 각도와 길이로 구했다. 막대가 둘이면 두 번째 막대는 첫 막대의 끝점에서 다시 출발한다. 두 화살표를 이어 붙였을 때 끝점이 어디인지가 첫 번째 질문이다.

두 번째 질문은 방향 하나를 정해 놓고 화살표를 그 방향으로 읽는 일이다. 비스듬히 놓인 레일을 따라가야 할 로봇 손끝이 $(1,3)$만큼 움직였다고 하자. 레일을 따라서는 얼마나 갔고, 레일에서는 얼마나 벗어났을까? 이 글은 첫 질문에 벡터의 덧셈으로, 두 번째 질문에 정사영으로 답한다.

## 화살표를 이어 붙이면 더해진다

$\mathbf a=(3,1)$과 $\mathbf b=(1,2)$를 생각하자. 이 글은 벡터를 굵은 글자로 쓰고, 성분은 앞 글들처럼 괄호 안에 가로·세로 순으로 적는다. 원점에서 $\mathbf a$를 따라가면 $(3,1)$에 닿는다. 그 자리에 $\mathbf b$의 꼬리를 놓고 $\mathbf b$를 따라가면 가로로 1, 세로로 2를 더 가서 $(4,3)$에 닿는다.

가로 이동은 가로 이동끼리, 세로 이동은 세로 이동끼리 쌓인다. 가로로 3을 간 뒤 다시 1을 가면 모두 4를 간 셈이다. 두 벡터의 **합**은 이렇게 성분끼리 더해서 정한다.

$$
\mathbf a+\mathbf b=(a_x+b_x,\;a_y+b_y),\qquad (3,1)+(1,2)=(4,3).
$$

순서를 바꿔 $\mathbf b$를 먼저 가고 $\mathbf a$를 나중에 가도 끝점은 $(1+3,\;2+1)=(4,3)$이다. 성분마다 두 수를 더하는 순서는 결과를 바꾸지 않으므로, 어떤 두 벡터에서도 $\mathbf a+\mathbf b=\mathbf b+\mathbf a$다. 두 길을 함께 그리면 평행사변형이 되고, 합은 원점에서 출발하는 대각선이다. 마주 보는 변은 같은 화살표를 평행이동한 화살표라 같은 벡터를 나타낸다. [점과 벡터 글](/blog/robotics-points-vectors)에서 본 자유벡터의 성질이다.

![a (3, 1)의 머리에 b (1, 2)의 꼬리를 놓으면 끝점은 (4, 3)이다. 점선은 b를 먼저 가고 a를 나중에 간 길로, 같은 점에서 끝나며 두 길이 평행사변형을 이룬다.](/images/robotics-vector-projection/sum.svg)

길이는 성분처럼 더해지지 않는다. $\lVert\mathbf a\rVert=\sqrt{10}\approx3.16$, $\lVert\mathbf b\rVert=\sqrt5\approx2.24$라 두 길이의 합은 약 $5.40$인데, 합 $(4,3)$의 길이는 $\sqrt{4^2+3^2}=5$다. 점과 벡터 글에서 꺾인 경로의 길이와 직선거리가 달랐던 것과 같은 현상이다.

막대 두 개로 돌아가 보자. 길이 2인 첫 막대를 $30^\circ$ 돌리면 끝점은 $(\sqrt3,1)$이었다. 그 끝에 길이 1인 막대를 붙여 위쪽($90^\circ$)을 향하게 하면, 두 번째 막대가 만드는 변위는 $(\cos90^\circ,\sin90^\circ)=(0,1)$이다. 두 번째 막대의 끝점은 두 변위의 합이다.

$$
(\sqrt3,\;1)+(0,\;1)=(\sqrt3,\;2)\approx(1.73,\;2).
$$

여기서는 두 번째 막대의 각도도 같은 $x$축에서 쟀다. 실제 관절은 앞 막대를 기준으로 각도를 재는 경우가 많고, 그 방식은 뒤의 글에서 다룬다.

## 수를 곱하면 길이와 방향이 바뀐다

벡터에 수 $k$를 곱하는 **실수배**는 두 성분에 똑같이 $k$를 곱한다.

$$
k\mathbf a=(ka_x,\;ka_y).
$$

$\mathbf a=(2,1)$이면 $2\mathbf a=(4,2)$, $0.5\mathbf a=(1,0.5)$, $-\mathbf a=(-2,-1)$, $0\mathbf a=(0,0)$이다.

![(2, 1)에 2, 0.5, −1, 0을 곱한 화살표. 같은 방향으로 늘거나 줄고, −1을 곱하면 방향이 반대가 되며, 0을 곱하면 영벡터다.](/images/robotics-vector-projection/multiples.svg)

길이는 곱한 수의 크기만큼 변한다. 어떤 $k$와 $\mathbf a$에서도

$$
\lVert k\mathbf a\rVert=\sqrt{(ka_x)^2+(ka_y)^2}=\sqrt{k^2}\,\sqrt{a_x^2+a_y^2}=|k|\,\lVert\mathbf a\rVert
$$

이다. $|k|$는 $k$에서 부호를 뗀 크기이고, $\sqrt{k^2}=|k|$다.

방향은 $k$의 부호가 정한다. $k>0$이면 두 성분이 같은 비율로 늘거나 줄고 부호도 그대로라, 원점에서 본 방향이 $\mathbf a$와 같다. $k<0$이면 $k\mathbf a=|k|(-\mathbf a)$이고, $-\mathbf a$의 끝점 $(-a_x,-a_y)$는 원점을 사이에 두고 $\mathbf a$의 끝점 반대편에 있다. 앞 글의 $(3,4)$와 $(-3,-4)$가 그런 짝이었다. $k=0$이면 영벡터가 되어 방향이 없다.

앞 글의 끝점 $(L\cos\theta,L\sin\theta)$도 실수배였다. 단위원 위의 점 $(\cos\theta,\sin\theta)$에 양수 $L$을 곱했으므로 방향은 그대로이고 길이만 $L$배가 된다.

뺄셈은 $-1$배를 더하는 계산으로 정한다. $\mathbf a-\mathbf b=\mathbf a+(-1)\mathbf b$다. 점과 벡터 글의 공식도 여기서 다시 나온다. 원점에서 점 $A$로 간 뒤 $A$에서 $B$로 가면 $B$에 닿으므로 $\overrightarrow{OA}+\overrightarrow{AB}=\overrightarrow{OB}$이고, 양변에서 $\overrightarrow{OA}$를 빼면

$$
\overrightarrow{AB}=\overrightarrow{OB}-\overrightarrow{OA}=(b_x-a_x,\;b_y-a_y)
$$

다. 위치벡터의 성분은 점의 좌표와 같은 수이므로, 이 식이 “끝점 좌표에서 시작점 좌표를 뺀다”는 규칙이다.

## 모든 벡터는 두 축 방향의 합이다

길이가 1인 벡터를 **단위벡터**라고 한다. $x$축과 $y$축의 양의 방향을 가리키는 두 단위벡터를

$$
\mathbf e_x=(1,0),\qquad \mathbf e_y=(0,1)
$$

로 쓰자. 실수배로 $a_x\mathbf e_x=(a_x,0)$, $a_y\mathbf e_y=(0,a_y)$이고, 둘을 더하면 $(a_x,a_y)$다. 어떤 벡터든

$$
\mathbf a=a_x\mathbf e_x+a_y\mathbf e_y
$$

로 쓸 수 있다. 성분은 $\mathbf e_x$와 $\mathbf e_y$를 각각 몇 배 해서 더하는지를 적은 수다. $(3,1)$은 $\mathbf e_x$ 세 개와 $\mathbf e_y$ 하나를 이어 붙인 화살표다.

![(3, 1)은 노란 e_x 세 개와 초록 e_y 하나를 이어 붙인 화살표다.](/images/robotics-vector-projection/unit-axes.svg)

앞 글의 막대 끝점은 $L\cos\theta\,\mathbf e_x+L\sin\theta\,\mathbf e_y$다. 가로 성분과 세로 성분이 두 단위벡터에 곱하는 수였다. 축을 돌려 $\mathbf e_x$와 $\mathbf e_y$가 함께 돌아간 뒤에도 같은 방식으로 점을 나타낼 수 있는지는 다음 글에서 확인한다.

## 화살표를 직접 더해 보기

아래 그림에서 파란 점을 끌면 $\mathbf a$가, 보라 마름모를 끌면 $\mathbf b$가 바뀐다. 보라 마름모는 $\mathbf a$의 머리에 이어 붙인 $\mathbf b$의 머리, 곧 합의 끝점에 있다. 파란 점을 끌면 $\mathbf b$는 모양을 유지한 채 따라온다. 그림 아래에서 바꿀 화살표를 고른 뒤 $x$, $y$ 입력을 조절해도 되고, 키보드로는 입력에 초점을 맞추고 방향키를 누른다. 점선은 순서를 바꿔 $\mathbf b$를 먼저 간 길이다.

보라 마름모를 끌어 $\mathbf b$를 $\mathbf a$와 같은 방향으로, 예를 들어 $(1.5,\,0.5)$로 놓아 보자. 두 길이의 합과 합의 길이는 어떻게 되는가? 이번에는 보라 마름모를 원점으로 끌어 $\mathbf b=-\mathbf a$로 만들어 보자. 합은 무엇이 되는가?

![처음 상태는 a (3, 1), b (1, 2)이고 합은 (4, 3), 길이 5다. 흰 화살표가 합, 점선이 순서를 바꾼 길이다.](/images/robotics-vector-projection/sum-lab.svg)

조작 기능을 사용할 수 없는 환경과 인쇄본에는 처음 상태의 그림이 표시된다. 「화살표를 이어 붙이면 더해진다」 절의 예와 같은 값이다.

## 한 방향으로 그림자 내리기

이제 두 번째 질문이다. 레일의 방향을 길이 1인 벡터 $\mathbf u=(0.6,0.8)$로 나타내자. 앞 글의 $(3,4)$를 길이 5로 나눈 방향이고, 길이는 $\sqrt{0.6^2+0.8^2}=1$이다. 손끝의 변위 $\mathbf a=(1,3)$이 레일을 따라 얼마나 갔는지 알고 싶다.

원점을 지나 $\mathbf u$ 방향으로 뻗은 직선을 $\ell$이라 하자. $\mathbf a$를 원점에서 그리고, 그 끝점에서 $\ell$에 수직으로 그은 선이 $\ell$과 만나는 점을 $F$라 한다. 이 점을 수선의 발이라고 부른다. 화살표 $\overrightarrow{OF}$를 $\mathbf a$의 $\mathbf u$ 방향 **정사영**이라고 부른다. $\ell$에 수직으로 빛을 비출 때 $\mathbf a$가 $\ell$ 위에 드리우는 그림자로 생각하면 된다.

$\overrightarrow{OF}$는 $\ell$ 위에 있으므로 어떤 수 $s$로 $\overrightarrow{OF}=s\,\mathbf u$라고 쓸 수 있다. 이 $s$를 정사영의 길이라 부르자. $F$가 원점에서 $\mathbf u$ 쪽에 있으면 양수, 반대쪽에 있으면 음수, 원점이면 0인 부호 있는 길이다.

![(1, 3)의 끝점에서 (0.6, 0.8) 방향의 직선에 수선을 내리면 발 F는 (1.8, 2.4)다. 노란 선이 정사영, 초록 점선이 나머지이고, φ는 u에서 a까지 잰 각이다.](/images/robotics-vector-projection/shadow.svg)

$s$는 $\mathbf a$의 길이와 각도로 구할 수 있다. 그림 전체를 원점 중심으로 돌려서 $\mathbf u$가 오른쪽을 향하게 하자. 종이를 돌릴 때처럼 길이, 각도, 수직 관계는 바뀌지 않는다. 돌린 그림에서 $\ell$은 가로축이고, 끝점에서 가로축에 내린 수선의 발은 끝점의 가로 좌표 자리다. $\mathbf u$에서 $\mathbf a$까지 반시계 방향을 양수로 잰 각을 $\varphi$라 하면, 돌린 그림의 $\mathbf a$는 가로축에서 $\varphi$만큼 돈 길이 $\lVert\mathbf a\rVert$의 화살표다. 앞 글의 결론에 따라 그 끝점의 가로 좌표는 $\lVert\mathbf a\rVert\cos\varphi$이므로

$$
s=\lVert\mathbf a\rVert\cos\varphi
$$

다. 앞 글의 결론은 모든 각도에서 성립했으므로 이 식도 $\varphi$가 몇이든 부호까지 맞는다. 같은 방향을 가리키는 각은 $360^\circ$씩 차이 나는 여러 값이 있지만 모두 같은 끝점을 주므로, 어느 값을 써도 $\cos\varphi$는 같다. 부호를 따질 때는 그 가운데 $-180^\circ$보다 크고 $180^\circ$ 이하인 값을 고른다. 이 범위에서 $\varphi$의 크기가 $90^\circ$보다 작으면 $s>0$, $90^\circ$이면 $s=0$, $90^\circ$보다 크면 $s<0$이다. $\mathbf a$가 영벡터이면 $F$가 원점이라 $s=0$이다.

![u를 오른쪽으로 돌려 놓은 그림 세 칸. φ가 50°이면 정사영의 길이 s가 양수, 90°이면 0, 140°이면 음수다.](/images/robotics-vector-projection/shadow-signs.svg)

축 방향으로 내린 정사영은 이미 아는 값이다. $\mathbf u=\mathbf e_x$이면 $\ell$은 $x$축이고, 끝점 $(a_x,a_y)$에서 $x$축에 내린 수선의 발은 $(a_x,0)$이다. 정사영은 $a_x\mathbf e_x$이고 길이는 $a_x$다. 같은 방식으로 $\mathbf e_y$ 방향의 정사영 길이는 $a_y$다. 성분은 축 방향으로 내린 정사영의 길이였다.

## 그림자의 길이를 성분으로 계산하기

$\lVert\mathbf a\rVert\cos\varphi$를 쓰려면 각도 $\varphi$를 알아야 한다. 성분만 알 때도 $s$를 구할 수 있도록 세 단계를 밟는다.

**첫째, 정사영의 길이도 더해지고 실수배된다.** $\mathbf u$가 오른쪽을 향하도록 돌린 그림에서 정사영의 길이는 화살표의 가로 성분이다. 그림을 돌리면 모든 화살표가 같은 각만큼 돌므로, 평행이동한 두 화살표는 돌린 뒤에도 평행이동한 관계, 곧 같은 벡터다. 두 화살표를 이어 붙인 그림을 통째로 돌리면 이어 붙인 모양도 그대로 돌아가므로, 돌린 그림에서도 $\mathbf a+\mathbf b$는 돌린 $\mathbf a$와 돌린 $\mathbf b$를 이어 붙인 화살표다. 가로 이동은 가로 이동끼리 쌓이므로 $\mathbf a+\mathbf b$의 정사영 길이는 두 정사영 길이의 합이다. 실수배도 마찬가지다. 돌려도 길이의 비율과 방향이 같은지 반대인지는 그대로라, $k\mathbf a$를 돌린 화살표는 돌린 $\mathbf a$의 $k$배이고 정사영 길이도 $k$배가 된다.

**둘째, 길이 1인 두 화살표는 서로의 방향으로 같은 길이만큼 정사영된다.** $\mathbf u$가 $x$축의 양의 방향에서 $\alpha$만큼 돈 방향이라 하자. $\mathbf u$에서 $\mathbf e_x$까지 잰 각은 $-\alpha$이므로, $\mathbf e_x$를 $\mathbf u$ 방향으로 정사영한 길이는 $\cos(-\alpha)$다. 거꾸로 $\mathbf e_x$에서 $\mathbf u$까지 잰 각은 $\alpha$라, $\mathbf u$를 $\mathbf e_x$ 방향으로 정사영한 길이는 $\cos\alpha$다. 각도의 부호를 바꾸면 끝점이 $x$축에 대해 뒤집히고 가로 좌표는 그대로이므로 $\cos(-\alpha)=\cos\alpha$다. 앞 글에서 $-30^\circ$의 끝점이 $30^\circ$의 끝점과 가로 좌표가 같았던 것과 같은 이유다. $\cos\alpha$는 $\mathbf u$를 $x$축에 정사영한 길이, 곧 $\mathbf u$의 가로 성분 $u_x$이므로 $\mathbf e_x$를 $\mathbf u$ 방향으로 정사영한 길이도 $u_x$다.

$\mathbf e_y$도 같은 방식으로 구한다. $\mathbf e_y$는 $x$축의 양의 방향에서 $90^\circ$ 돈 방향이므로, $\mathbf u$에서 $\mathbf e_y$까지 잰 각은 $90^\circ-\alpha$, $\mathbf e_y$에서 $\mathbf u$까지 잰 각은 $\alpha-90^\circ$다. 두 각은 부호만 달라 코사인이 같다. 뒤의 각으로 구한 값은 $\mathbf u$를 $\mathbf e_y$ 방향으로 정사영한 길이이고, 앞 절에 따라 그 길이는 $\mathbf u$의 세로 성분 $u_y$다. $\mathbf e_y$를 $\mathbf u$ 방향으로 정사영한 길이도 $u_y$다.

![길이 1인 e_x와 u가 α를 이룰 때, e_x를 u 방향으로 정사영한 길이와 u를 e_x 방향으로 정사영한 길이는 모두 cos α다. 두 직각삼각형은 사이각의 이등분선에 대해 대칭이다.](/images/robotics-vector-projection/mutual-shadow.svg)

그림의 대칭은 이 사실을 눈으로 확인하는 방법이고, 증명은 앞 문단의 $\cos(-\alpha)=\cos\alpha$다.

**셋째, 성분으로 쪼개서 더한다.** $\mathbf a=a_x\mathbf e_x+a_y\mathbf e_y$였다. 첫째 단계에 따라 $\mathbf a$의 정사영 길이는 $\mathbf e_x$의 정사영 길이를 $a_x$배 한 값과 $\mathbf e_y$의 정사영 길이를 $a_y$배 한 값의 합이다. 둘째 단계의 두 값을 넣으면

$$
s=a_xu_x+a_yu_y
$$

다. 이 계산을 두 벡터의 **내적**이라 부르고 가운뎃점으로 쓴다.

$$
\mathbf a\cdot\mathbf b=a_xb_x+a_yb_y.
$$

길이 1인 $\mathbf u$에 대해 $\mathbf a\cdot\mathbf u$가 정사영의 길이이고, 앞 절의 식과 합치면 $\mathbf a\cdot\mathbf u=\lVert\mathbf a\rVert\cos\varphi$다. 처음 예에 넣으면

$$
(1,3)\cdot(0.6,0.8)=1\times0.6+3\times0.8=0.6+2.4=3
$$

이고, 정사영은 $3\mathbf u=(1.8,\;2.4)$다. 그림의 $F$와 같은 점이다. 손끝은 레일을 따라 3만큼 갔다.

내적은 길이가 1이 아닌 벡터에도 쓸 수 있다. 영벡터가 아닌 $\mathbf b$에 $1/\lVert\mathbf b\rVert$를 곱한 $\mathbf u_b$는 $\mathbf b$와 같은 방향의 단위벡터이고, $\mathbf b=\lVert\mathbf b\rVert\,\mathbf u_b$다. 내적의 정의에서 한쪽 성분에 똑같이 곱한 수는 밖으로 묶여 나오므로

$$
\mathbf a\cdot\mathbf b=\lVert\mathbf b\rVert\,(\mathbf a\cdot\mathbf u_b)=\lVert\mathbf a\rVert\,\lVert\mathbf b\rVert\cos\varphi
$$

다. 여기서 $\varphi$는 $\mathbf b$에서 $\mathbf a$까지 잰 각이다.

이 식에서 두 가지를 읽을 수 있다. 영벡터가 아닌 두 벡터는 길이가 양수이므로, 내적이 0이라는 조건은 $\cos\varphi=0$과 같다. $\varphi$를 $-180^\circ$보다 크고 $180^\circ$ 이하인 범위에서 고르면 단위원의 가로 좌표가 0인 각은 $\pm90^\circ$뿐이므로, 영벡터가 아닌 두 벡터는 내적이 0일 때, 그리고 그때에만 수직이다. 예를 들어 $(-4,3)\cdot(3,4)=-12+12=0$이라 두 벡터는 수직이다. 또 자기 자신과의 내적은 $\mathbf a\cdot\mathbf a=a_x^2+a_y^2=\lVert\mathbf a\rVert^2$이다.

## 정사영과 나머지로 나누기

$\mathbf a$에서 정사영을 빼고 남은 부분을 **나머지**라 부르고 $\mathbf r$로 쓰자.

$$
\mathbf r=\mathbf a-s\,\mathbf u,\qquad s=\mathbf a\cdot\mathbf u.
$$

$\mathbf r$과 $\mathbf u$의 내적을 성분으로 풀면

$$
\mathbf r\cdot\mathbf u=(a_x-su_x)u_x+(a_y-su_y)u_y=(a_xu_x+a_yu_y)-s\,(u_x^2+u_y^2)=s-s\cdot1=0
$$

이다. $u_x^2+u_y^2$는 $\mathbf u$의 길이의 제곱이라 1이다. 내적이 0이므로 $\mathbf r$은 영벡터가 아닌 한 $\mathbf u$에 수직이다. $\mathbf r$이 영벡터이면 $\mathbf a$가 처음부터 $\ell$ 위에 있던 경우다.

$\mathbf a$는 $\ell$을 따르는 정사영 $s\mathbf u$와 $\ell$에 수직인 나머지 $\mathbf r$의 합으로 나뉜다. 처음 예에서 $\mathbf r=(1,3)-(1.8,2.4)=(-0.8,\;0.6)$이고, $\mathbf r\cdot\mathbf u=-0.48+0.48=0$이다. 길이는 $\sqrt{0.64+0.36}=1$이다. 수직인 두 화살표를 이어 붙이면 직각삼각형이 되므로 피타고라스 정리에 따라 $\lVert\mathbf a\rVert^2=s^2+\lVert\mathbf r\rVert^2$이고, 실제로 $10=3^2+1^2$이다.

레일 질문의 답이 나왔다. 손끝은 레일을 따라 3만큼 갔고, 레일에서 길이 1만큼 벗어났다. 레일을 따라서만 움직이게 만든 관절은 이 나머지가 0이 되도록 부품을 묶는다. 관절을 식으로 쓰는 방법은 뒤의 글에서 다룬다.

$F$에는 성질이 하나 더 있다. $\ell$ 위의 점 가운데 $\mathbf a$의 끝점에 가장 가까운 점이다. $\ell$ 위의 다른 점 $t\mathbf u$에서 끝점으로 가는 화살표는

$$
\mathbf a-t\mathbf u=(s-t)\,\mathbf u+\mathbf r
$$

이다. $(s-t)\mathbf u$는 $\ell$을 따르고 $\mathbf r$은 $\ell$에 수직이므로, 다시 피타고라스 정리로 거리의 제곱은 $(s-t)^2+\lVert\mathbf r\rVert^2$이다. $(s-t)^2$은 $t=s$일 때만 0이고 다른 점에서는 양수이므로, 끝점에 가장 가까운 점은 $F$ 하나뿐이다.

## 정사영을 직접 바꿔 보기

아래 그림에서 파란 점을 끌면 $\mathbf a$가 바뀌고, 흰 마름모 $D$를 끌면 직선의 방향이 바뀐다. $\mathbf u$는 원점에서 $D$ 쪽을 향하는 길이 1인 화살표인데, 정사영과 겹치지 않도록 직선 옆에 그렸다. 그림 아래에서 움직일 대상을 고른 뒤 $x$, $y$ 입력을 조절해도 된다. $D$는 방향만 정하므로 원점에는 둘 수 없다.

먼저 $D$를 끌어 직선을 돌려 보자. 노란 정사영이 사라지는 때는 직선이 $\mathbf a$와 몇 도를 이룰 때인가? 그다음 $D$를 처음 자리 $(3,4)$로 되돌리고 $\mathbf a$를 $(1.5,\,2)$로 옮겨 직선 위에 올려 보자. 초록 나머지는 어떻게 되는가? 읽기 값의 $\mathbf a\cdot\mathbf u$와 $\lVert\mathbf a\rVert\cos\varphi$가 늘 같은지도 확인해 보자. 읽기 값의 $\varphi$는 부호를 뗀 크기로 보인다. 코사인은 부호에 영향받지 않기 때문이다.

![처음 상태는 a (1, 3), D (3, 4)이고 u는 (0.6, 0.8)이다. 노란 정사영의 길이는 3이고 발은 (1.8, 2.4), 초록 점선이 나머지다.](/images/robotics-vector-projection/projection-lab.svg)

조작 기능을 사용할 수 없는 환경과 인쇄본에는 처음 상태의 그림이 표시된다. 「그림자의 길이를 성분으로 계산하기」 절의 예와 같은 값이다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

두 화살표를 이어 붙인 합은 성분끼리 더한 $(a_x+b_x,\,a_y+b_y)$이고, 순서를 바꿔도 같다. 실수배 $k\mathbf a$는 길이가 $|k|$배이고, $k<0$이면 방향이 반대다. 모든 벡터는 $a_x\mathbf e_x+a_y\mathbf e_y$로 쓸 수 있다. 길이 1인 $\mathbf u$ 방향으로 내린 정사영의 길이는 내적 $\mathbf a\cdot\mathbf u=a_xu_x+a_yu_y=\lVert\mathbf a\rVert\cos\varphi$이고, 나머지 $\mathbf a-(\mathbf a\cdot\mathbf u)\mathbf u$는 $\mathbf u$와의 내적이 0이다. 영벡터가 아닌 두 벡터는 내적이 0일 때, 그리고 그때에만 수직이다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

막대를 돌리면 막대에 붙은 두 축도 함께 돈다. 돌아간 막대 위의 점은 돌아간 두 단위벡터의 실수배를 더해 얻는다. 다음 글에서는 돌아간 두 단위벡터의 성분을 구하고, 그 두 쌍의 수가 회전행렬의 두 열이 되는 과정을 본다.

</div>

## 참고 자료

- [OpenStax, Calculus Volume 3, 2.1 Vectors in the Plane](https://openstax.org/books/calculus-volume-3/pages/2-1-vectors-in-the-plane): 꼬리를 머리에 잇는 덧셈과 평행사변형 방법, 실수배의 길이와 방향, 표준 단위벡터.
- [OpenStax, Calculus Volume 3, 2.3 The Dot Product](https://openstax.org/books/calculus-volume-3/pages/2-3-the-dot-product): 내적의 성분 공식과 각도 공식, 내적이 0인 두 벡터의 수직, 정사영과 그에 수직인 나머지.
