---
title: "회전행렬 — 돌아간 두 축이 행렬의 두 열이 된다"
date: 2026-10-22T09:00:00+09:00
description: "원점을 중심으로 θ만큼 돌리면 x축 방향 단위벡터는 (cos θ, sin θ)로, y축 방향 단위벡터는 (−sin θ, cos θ)로 간다. 이 두 쌍을 열로 나란히 적은 표가 회전행렬이고, 돌아간 점은 두 열에 막대 좌표를 곱해 더해 얻는다."
tags: ["Robotics", "Kinematics", "Matrix"]
category: robotics
difficulty: 입문
numbered: true
---

로봇 팔의 첫 관절이 원점에 있고, 그 관절에 붙은 막대에 집게가 달려 있다고 하자. 집게 끝은 막대 위에 있지 않고 옆으로 비켜 있어서, 막대를 따라 3, 막대의 왼쪽으로 1만큼 간 자리에 있다. 막대가 오른쪽을 가리키면 집게 끝의 좌표는 $(3,1)$이다. 막대를 $\theta$만큼 돌리면 집게 끝은 어디로 갈까?

[사인과 코사인 글](/blog/robotics-sine-cosine)에서는 막대 위의 끝점을, [앞 글](/blog/robotics-vector-projection)에서는 막대 둘을 이어 붙인 끝점을 구했다. 집게 끝도 원점에서의 거리 $\sqrt{10}$과 처음 각도를 구한 뒤 $\theta$를 더해 찾을 수 있다. 그러려면 두 각을 더한 각의 코사인과 사인을 구하는 공식이 필요하다. 이 글은 그 공식 없이 답을 구하고, 그 과정에서 회전행렬의 네 숫자가 어디서 나오는지 본다. 그 공식은 마지막에 덤으로 얻는다.

## 막대에 붙은 두 축

막대에 축 두 개를 붙이자. 하나는 막대가 가리키는 방향의 단위벡터 $\mathbf e_x'$다. 다른 하나는 $\mathbf e_x'$를 반시계 방향으로 $90^\circ$ 돌린 단위벡터 $\mathbf e_y'$로, 막대가 가리키는 쪽을 앞으로 볼 때 왼쪽을 가리킨다. 막대가 오른쪽을 가리키는 처음 자세에서 두 축은 앞 글의 $\mathbf e_x=(1,0)$, $\mathbf e_y=(0,1)$과 같다.

집게 끝 $P$는 막대를 따라 3, 왼쪽으로 1만큼 간 자리이므로

$$
\overrightarrow{OP}=3\,\mathbf e_x'+1\,\mathbf e_y'
$$

이다. 막대의 두 축으로 읽은 두 수 $(3,1)$을 $P$의 **막대 좌표**라 부르고 $(s_x,s_y)$로 쓰자. 바닥에 고정된 $x$, $y$축으로 읽은 좌표는 **고정 좌표**라 부르고 $(p_x,p_y)$로 쓴다. 로봇 공학 교재는 막대 좌표를 local 좌표, 고정 좌표를 world 좌표라고 부르고, 이 시리즈도 이후 글에서 이 이름을 쓴다.

집게는 막대에 고정돼 있으므로 막대가 돌아도 막대에 대한 자리는 그대로다. 막대 좌표 $(3,1)$은 막대를 몇 도 돌리든 바뀌지 않는다. 바뀌는 것은 두 축의 방향이다. 질문을 이렇게 바꿀 수 있다. 돌아간 두 축 $\mathbf e_x'$, $\mathbf e_y'$의 고정 좌표는 무엇인가?

![왼쪽은 돌리기 전, 오른쪽은 막대를 θ만큼 돌린 뒤다. 막대에 붙은 두 축 e′_x, e′_y와 집게가 함께 돌고, 집게 끝 P는 여전히 막대를 따라 3, 막대 왼쪽으로 1인 자리에 있다.](/images/robotics-rotation-matrix/rod-frame.svg)

## 돌아간 두 축의 성분

이 글은 회전에 관한 사실 하나를 전제로 쓴다. 원점을 중심으로 그림 전체를 돌리면 종이를 돌릴 때처럼 길이와 각도가 그대로이고, 그림 속 모든 화살표가 같은 각만큼 돈다. 이어 붙인 화살표는 이어 붙은 채로 돌고, $k$배 한 화살표는 돌린 뒤에도 돌린 화살표의 $k$배다. 앞 글에서 정사영의 길이가 더해지고 실수배된다는 점을 보일 때 쓴 사실과 같다.

먼저 $\mathbf e_x'$다. $\mathbf e_x'$는 길이 1인 막대를 $x$축의 양의 방향에서 $\theta$만큼 돌린 화살표이므로, 사인과 코사인 글의 정의에 따라

$$
\mathbf e_x'=(\cos\theta,\;\sin\theta)
$$

다. 그 정의는 모든 각도에 값을 주므로 $\theta$가 몇이든 맞는다.

$\mathbf e_y'$를 구하려면 $90^\circ$ 돌리기를 먼저 알아야 한다. 반시계 방향으로 $90^\circ$ 돌리면 $\mathbf e_x$는 위쪽을 가리키는 $(0,1)$이 된다. $\mathbf e_y$는 원래 $90^\circ$ 방향에 있으므로 $180^\circ$ 방향으로 가서 $(\cos180^\circ,\sin180^\circ)=(-1,0)$이 된다. 어떤 벡터든 $(a,b)=a\,\mathbf e_x+b\,\mathbf e_y$로 쓸 수 있었다. 전제에 따라 $a\,\mathbf e_x$는 $a(0,1)$로, $b\,\mathbf e_y$는 $b(-1,0)$으로 이어 붙은 채 돌므로

$$
(a,\;b)\ \xrightarrow{\ 90^\circ\ }\ a(0,1)+b(-1,0)=(-b,\;a)
$$

다. 방향을 반대로 바꾸는 음수배도 실수배이므로, $a$, $b$가 음수여도 이 식은 그대로 성립한다. 이 식을 $90^\circ$ 규칙이라 부르자. 예를 들어 $(3,1)$을 $90^\circ$ 돌리면 $(-1,3)$이다.

![(3, 1)은 e_x 세 개와 e_y 하나를 이은 화살표다. 90° 돌리면 e_x는 (0, 1)로, e_y는 (−1, 0)으로 가므로 3 × (0, 1)과 1 × (−1, 0)을 이은 (−1, 3)이 된다.](/images/robotics-rotation-matrix/quarter-turn.svg)

막대에 축을 붙일 때는 $\mathbf e_x'$를 $90^\circ$ 돌린 단위벡터를 $\mathbf e_y'$로 정했다. 처음 자세의 $\mathbf e_y$를 막대와 함께 $\theta$만큼 돌린 화살표도 $\mathbf e_y'$와 같다. $\mathbf e_y$는 $\mathbf e_x$를 $90^\circ$ 돌린 화살표이므로, $\theta$만큼 돌린 $\mathbf e_y$는 $\mathbf e_x$를 모두 $90^\circ+\theta$만큼 돌린 화살표다. 같은 원점을 중심으로 돌리면 돌린 각이 더해질 뿐이라 $\mathbf e_x$를 $\theta$만큼 먼저 돌리고 $90^\circ$만큼 나중에 돌려도 결과가 같고, 그 결과는 $\mathbf e_x'$를 $90^\circ$ 돌린 $\mathbf e_y'$다. $90^\circ$ 규칙을 $\mathbf e_x'=(\cos\theta,\sin\theta)$에 쓰면

$$
\mathbf e_y'=(-\sin\theta,\;\cos\theta)
$$

다. 앞 글의 내적으로 검산할 수 있다. 길이는 $\sqrt{\sin^2\theta+\cos^2\theta}=1$이고, $\mathbf e_x'\cdot\mathbf e_y'=-\cos\theta\sin\theta+\sin\theta\cos\theta=0$이라 두 축은 수직이다.

![돌아간 x축은 (cos θ, sin θ), 돌아간 y축은 (−sin θ, cos θ)다. 노란 성분 삼각형을 90° 돌리면 초록 성분 삼각형이 된다.](/images/robotics-rotation-matrix/turned-axes.svg)

그림의 두 성분 삼각형은 이 결과를 눈으로 확인하는 방법이다. $\mathbf e_x'$의 노란 성분 삼각형은 가로 $\cos\theta$, 세로 $\sin\theta$다. 이 삼각형을 원점 중심으로 $90^\circ$ 돌리면 가로 변은 $y$축을 따라 위로 서고 세로 변은 그 끝에서 왼쪽으로 눕는다. 그렇게 얻은 초록 성분 삼각형은 위로 $\cos\theta$, 왼쪽으로 $\sin\theta$ 간 자리에서 끝나고, 그 자리가 $\mathbf e_y'$의 끝점이다. 그림은 $\theta$가 $0^\circ$와 $90^\circ$ 사이일 때의 모양이고, 증명은 모든 각도에서 성립하는 $90^\circ$ 규칙이다.

예를 들어 $\cos\theta=0.6$, $\sin\theta=0.8$인 각을 생각하자. 사인과 코사인 글에서 $\operatorname{atan2}(4,3)\approx53.13^\circ$로 구한 각이다. 이때 $\mathbf e_x'=(0.6,0.8)$, $\mathbf e_y'=(-0.8,0.6)$이다. 앞 글에서 레일 방향으로 쓴 $\mathbf u$와, $(1,3)$을 정사영한 나머지 $\mathbf r$이 바로 이 두 벡터였다.

## 돌아간 점은 두 축의 실수배를 더한 것이다

이제 질문에 답할 수 있다. 돌리기 전 집게 끝은 $s_x\mathbf e_x+s_y\mathbf e_y$다. 막대와 함께 그림 전체를 $\theta$만큼 돌리면 앞 절에서 본 대로 $\mathbf e_x$는 $\mathbf e_x'$로, $\mathbf e_y$는 $\mathbf e_y'$로 간다. 전제에 따라 $s_x\mathbf e_x$는 $s_x\mathbf e_x'$가 되고 $s_y\mathbf e_y$는 $s_y\mathbf e_y'$가 되며, 둘은 이어 붙은 채로 돈다. 고정 좌표 $(p_x,p_y)$를 성분으로 하는 벡터를 $\mathbf p$라 하면, 돌아간 집게 끝은

$$
\mathbf p=s_x\,\mathbf e_x'+s_y\,\mathbf e_y'
$$

이다. 막대 좌표는 그대로 두고 두 축만 돌아간 축으로 바꾸면 된다. 앞 절의 두 축을 넣어 성분으로 쓰면

$$
\mathbf p=s_x(\cos\theta,\;\sin\theta)+s_y(-\sin\theta,\;\cos\theta)=(s_x\cos\theta-s_y\sin\theta,\;\;s_x\sin\theta+s_y\cos\theta)
$$

다. 전제와 두 축의 성분이 모든 각도에서 성립하므로 이 식도 모든 $\theta$와 모든 막대 좌표에서 맞는다.

집게 끝 $(3,1)$을 $\cos\theta=0.6$, $\sin\theta=0.8$인 각만큼 돌리면

$$
3(0.6,\;0.8)+1(-0.8,\;0.6)=(1.8-0.8,\;\;2.4+0.6)=(1,\;3)
$$

이다. 막대를 따라 $3\mathbf e_x'=(1.8,2.4)$까지 간 뒤, 막대의 왼쪽으로 $\mathbf e_y'=(-0.8,0.6)$만큼 더 갔다. $(1.8,2.4)$는 앞 글에서 $(1,3)$을 레일에 정사영했을 때의 수선의 발 $F$였다. $90^\circ$ 돌릴 때는 $\mathbf e_x'=(0,1)$, $\mathbf e_y'=(-1,0)$이라 $3(0,1)+1(-1,0)=(-1,3)$이고, 앞 절의 $90^\circ$ 규칙과 같은 답이다.

![막대를 cos θ = 0.6, sin θ = 0.8인 각만큼 돌리면 집게 끝은 노란 3e′_x = (1.8, 2.4)를 따라간 뒤 초록 e′_y = (−0.8, 0.6)만큼 더 가서 고정 좌표 (1, 3)에 닿는다.](/images/robotics-rotation-matrix/turned-point.svg)

돌려도 원점까지의 거리는 그대로여야 한다. 전제로 둔 사실이지만 성분으로도 확인할 수 있다.

$$
\begin{aligned}
p_x^2+p_y^2&=(s_x\cos\theta-s_y\sin\theta)^2+(s_x\sin\theta+s_y\cos\theta)^2\\
&=s_x^2(\cos^2\theta+\sin^2\theta)+s_y^2(\sin^2\theta+\cos^2\theta)\\
&=s_x^2+s_y^2.
\end{aligned}
$$

두 제곱을 펼칠 때 생기는 $-2s_xs_y\cos\theta\sin\theta$와 $+2s_xs_y\sin\theta\cos\theta$는 서로 지워진다. 집게 끝은 어느 각도로 돌려도 원점에서 $\sqrt{10}$만큼 떨어져 있다.

## 두 열을 나란히 적으면 회전행렬이다

앞 절의 계산에서 $\theta$가 정하는 수는 $\mathbf e_x'$의 두 성분과 $\mathbf e_y'$의 두 성분, 모두 네 개다. 이 네 수를 표 하나로 묶으면 계산을 짧게 적을 수 있다. 수를 가로 줄과 세로 줄로 늘어놓은 표를 **행렬**이라 하고, 가로 줄을 **행**, 세로 줄을 **열**이라 부른다. 행렬 옆에서는 벡터의 성분을 세로로 적는다. 이렇게 적은 벡터를 **열벡터**라 하며, 괄호 안에 가로로 적은 벡터와 같은 벡터다.

$$
\begin{bmatrix}s_x\\ s_y\end{bmatrix}=(s_x,\;s_y).
$$

두 열이 $\mathbf c_1$, $\mathbf c_2$인 행렬과 열벡터의 곱은 첫째 열을 $s_x$배, 둘째 열을 $s_y$배 해서 더한 벡터로 정한다.

$$
\begin{bmatrix}\mathbf c_1&\mathbf c_2\end{bmatrix}\begin{bmatrix}s_x\\ s_y\end{bmatrix}=s_x\,\mathbf c_1+s_y\,\mathbf c_2.
$$

첫째 열에 $\mathbf e_x'$를, 둘째 열에 $\mathbf e_y'$를 세워 적은 행렬을 $R(\theta)$라 하자.

$$
R(\theta)=\begin{bmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{bmatrix}.
$$

곱의 정의에 따라 $R(\theta)$와 막대 좌표의 곱은 $s_x\mathbf e_x'+s_y\mathbf e_y'$이고, 앞 절에 따라 이것이 돌아간 점이다. 막대 좌표를 성분으로 하는 벡터를 $\mathbf s$라 하면

$$
\mathbf p=R(\theta)\,\mathbf s
$$

다. $R(\theta)$를 $\theta$만큼 돌리는 **회전행렬**이라 부른다. 회전행렬의 네 숫자는 돌아간 두 축의 성분이다. 첫째 열은 $\mathbf e_x$가 돌아간 자리, 둘째 열은 $\mathbf e_y$가 돌아간 자리다. 실제로 $\mathbf s=(1,0)$을 넣으면 첫째 열만, $\mathbf s=(0,1)$을 넣으면 둘째 열만 남는다.

같은 곱을 행으로 읽을 수도 있다. 고정 좌표의 가로 성분 $p_x$는 두 열의 첫 성분에 $s_x$와 $s_y$를 곱해 더한 값이므로, 첫 성분끼리 모은 첫째 행 $(\cos\theta,-\sin\theta)$와 $(s_x,s_y)$의 내적이다. 세로 성분 $p_y$는 둘째 행 $(\sin\theta,\cos\theta)$와 $(s_x,s_y)$의 내적이다.

$$
p_x=\cos\theta\,s_x-\sin\theta\,s_y,\qquad p_y=\sin\theta\,s_x+\cos\theta\,s_y.
$$

열로 읽든 행으로 읽든 같은 네 곱 $\cos\theta\,s_x$, $-\sin\theta\,s_y$, $\sin\theta\,s_x$, $\cos\theta\,s_y$를 성분마다 더하므로 결과가 같다. 열로 읽으면 두 축을 이어 붙인 그림이 보이고, 행으로 읽으면 고정 좌표를 성분 하나씩 계산하는 식이 된다. 손으로 계산할 때는 보통 행으로 읽는다. 집게 끝의 예를 행으로 계산하면

$$
\begin{bmatrix}0.6&-0.8\\ 0.8&0.6\end{bmatrix}\begin{bmatrix}3\\ 1\end{bmatrix}=\begin{bmatrix}0.6\times3+(-0.8)\times1\\ 0.8\times3+0.6\times1\end{bmatrix}=\begin{bmatrix}1\\ 3\end{bmatrix}
$$

이다. $90^\circ$와 $0^\circ$의 회전행렬은

$$
R(90^\circ)=\begin{bmatrix}0&-1\\ 1&0\end{bmatrix},\qquad R(0^\circ)=\begin{bmatrix}1&0\\ 0&1\end{bmatrix}
$$

이다. $R(90^\circ)$는 앞의 $90^\circ$ 규칙 $(a,b)\to(-b,a)$를 행렬로 적은 것이다. $R(0^\circ)$의 두 열은 $\mathbf e_x$, $\mathbf e_y$ 그대로라 점을 움직이지 않는다.

평면에서는 이 표기가 계산을 짧게 적는 방법 정도다. 공간에서는 회전 여러 개를 이어 자세를 만들기 때문에 행렬로 정리하는 편이 훨씬 편해진다. 그 이야기는 뒤의 글에서 다룬다.

## 막대를 직접 돌려 보기

아래 그림에서 흰 마름모(막대 끝)를 끌면 막대가 돌고, 파란 점(집게 끝 $P$)을 끌면 막대 좌표가 바뀐다. 막대에 붙은 격자도 막대와 함께 돌고, 파란 점은 그 격자의 반 칸(0.5) 단위로 움직인다. 그림 아래의 각도 $\theta$와 막대 좌표 $s_x$, $s_y$ 입력으로 바꿔도 되고, 키보드로는 입력에 초점을 맞추고 방향키를 누른다. 그림 맨 아래의 식은 $R(\theta)\,\mathbf s$와 그 결과다. 행렬의 첫째 열은 노란 $\mathbf e_x'$와, 둘째 열은 초록 $\mathbf e_y'$와 같은 색으로 적었다. 읽기 값은 소수 둘째 자리까지 반올림하므로, 반올림한 수가 들어간 식은 $=$ 대신 $\approx$로 잇는다.

먼저 $\theta$를 $90^\circ$로 놓아 보자. 행렬의 두 열은 무엇이 되고, 두 화살표는 어디를 가리키는가? 다음으로 $\theta$를 바꿔 가며 막대 좌표와 고정 좌표의 읽기 값을 비교해 보자. 어느 쪽이 그대로이고 어느 쪽이 바뀌는가? 마지막으로 막대 좌표를 $(3,1)$에 두고 $\theta$를 $53^\circ$로 놓으면 집게 끝은 $(1,3)$에 아주 가까워지지만 정확히 닿지는 않는다. 정확히 닿는 각은 약 $53.13^\circ$라 1° 단위로는 고를 수 없다.

![처음 상태는 θ = 30°, 막대 좌표 (3, 1)이고 고정 좌표는 약 (2.1, 2.37)이다. 아래 식은 회전행렬과 막대 좌표의 곱이다.](/images/robotics-rotation-matrix/rotation-lab.svg)

조작 기능을 사용할 수 없는 환경과 인쇄본에는 처음 상태의 그림이 표시된다. $30^\circ$는 사인과 코사인 글의 실험이 처음 쓴 각도다.

## 거꾸로: 정사영으로 막대 좌표 되찾기

이번에는 반대 질문이다. 집어야 할 물건이 고정 좌표 $(1,3)$에 있고, 막대는 $\cos\theta=0.6$, $\sin\theta=0.8$인 각만큼 돌아 있다. 막대에서 보면 물건은 막대를 따라 얼마, 막대의 왼쪽으로 얼마인 자리에 있을까?

물건은 막대에 붙어 있지 않지만 막대 좌표는 정할 수 있다. 물건이 막대에 붙어 있다고 치고 막대와 함께 $\theta$만큼 되돌리면 막대는 처음 자세로 돌아오고, 그 자세에서 읽은 물건의 고정 좌표가 막대 좌표 $(s_x,s_y)$다. 거기서 다시 $\theta$만큼 돌리면 물건은 제자리로 오므로, 돌아간 점의 식에 따라 $\mathbf p=s_x\mathbf e_x'+s_y\mathbf e_y'$이다. 이 식에서 $s_x$와 $s_y$를 꺼내면 된다. 앞 글의 정사영이 그 방법이다. $\mathbf e_x'$와 $\mathbf e_y'$는 서로 수직인 단위벡터이므로, $\mathbf p$를 $\mathbf e_x'$ 방향으로 정사영한 길이는

$$
\mathbf p\cdot\mathbf e_x'=s_x\,(\mathbf e_x'\cdot\mathbf e_x')+s_y\,(\mathbf e_y'\cdot\mathbf e_x')=s_x\cdot1+s_y\cdot0=s_x
$$

다. 첫 등호는 내적이 덧셈과 실수배에 나뉘어 들어간다는 성질이다. 내적의 정의 $a_xb_x+a_yb_y$에 합이나 실수배를 넣고 성분마다 묶으면 바로 나오며, 앞 글에서 정사영의 길이가 더해지고 실수배된다고 한 것과 같은 내용이다. $\mathbf e_x'\cdot\mathbf e_x'$는 길이의 제곱이라 1이고, $\mathbf e_x'\cdot\mathbf e_y'=0$은 앞에서 확인했다. 같은 방법으로 $\mathbf p\cdot\mathbf e_y'=s_y$다. 성분으로 쓰면

$$
s_x=p_x\cos\theta+p_y\sin\theta,\qquad s_y=-p_x\sin\theta+p_y\cos\theta
$$

이고, 어떤 $\theta$와 고정 좌표에서도 성립한다. 물건의 예에서는 $(1,3)\cdot(0.6,0.8)=0.6+2.4=3$, $(1,3)\cdot(-0.8,0.6)=-0.8+1.8=1$이므로 막대 좌표는 $(3,1)$이다. 앞에서 막대 좌표 $(3,1)$을 돌려 $(1,3)$을 얻었으므로 맞는 답이다. 앞 글에서 $(1,3)$을 레일에 정사영한 길이는 3이었고, 그 나머지 $(-0.8,0.6)$은 $\mathbf e_y'$의 1배다. 막대 좌표 $(3,1)$은 그 정사영 길이 3과 이 1이다.

두 식을 행렬로 적으면

$$
\begin{bmatrix}s_x\\ s_y\end{bmatrix}=\begin{bmatrix}\cos\theta&\sin\theta\\ -\sin\theta&\cos\theta\end{bmatrix}\begin{bmatrix}p_x\\ p_y\end{bmatrix}
$$

이다. 이 행렬의 첫째 행은 $\mathbf e_x'$, 둘째 행은 $\mathbf e_y'$다. $R(\theta)$의 두 열이 이번에는 두 행으로 들어갔다. 행과 열을 맞바꾼 행렬을 **전치행렬**이라 부르고 $R(\theta)^{\mathsf T}$로 쓴다.

이 행렬은 반대 방향으로 $\theta$만큼 돌리는 회전행렬 $R(-\theta)$이기도 하다. 각도의 부호를 바꾸면 끝점이 $x$축에 대해 뒤집히므로 가로 좌표는 그대로이고 세로 좌표는 부호만 바뀐다. $\cos(-\theta)=\cos\theta$, $\sin(-\theta)=-\sin\theta$를 $R(-\theta)$에 넣으면 위의 행렬과 같다. 앞에서 막대 좌표를 정할 때 물건을 막대와 함께 $\theta$만큼 되돌렸는데, $R(-\theta)$를 곱하는 일이 바로 그 되돌리기다.

$R(\theta)$와 $R(\theta)^{\mathsf T}$는 $\sin\theta$에 붙은 부호의 자리만 다르다. 둘을 바꿔 쓰면 점이 반대 방향으로 돈다.

## 두 각의 합 공식

처음에 피해 간 두 각의 합 공식도 이제 얻을 수 있다. 길이가 1이고 $x$축의 양의 방향에서 $\alpha$만큼 돈 화살표 $(\cos\alpha,\sin\alpha)$를 생각하자. 이 화살표를 원점 중심으로 $\theta$만큼 더 돌리면 모두 $\alpha+\theta$만큼 돈 길이 1인 화살표가 되므로, 사인과 코사인 글의 정의에 따라 돌린 결과는 $(\cos(\alpha+\theta),\sin(\alpha+\theta))$다. 한편 돌리기 전에는 막대 좌표와 고정 좌표가 같으므로 $(\cos\alpha,\sin\alpha)$를 막대 좌표로 보고 돌아간 점의 식에 넣으면

$$
\cos\alpha\,(\cos\theta,\;\sin\theta)+\sin\alpha\,(-\sin\theta,\;\cos\theta)
$$

이다. 두 결과는 같은 화살표이므로 성분을 맞추면

$$
\begin{aligned}
\cos(\alpha+\theta)&=\cos\alpha\cos\theta-\sin\alpha\sin\theta,\\
\sin(\alpha+\theta)&=\sin\alpha\cos\theta+\cos\alpha\sin\theta
\end{aligned}
$$

다. 고교에서 배우는 삼각함수의 덧셈정리다. 앞의 논증은 각도의 크기나 부호에 기대지 않으므로 모든 $\alpha$, $\theta$에서 성립한다. $\alpha=30^\circ$, $\theta=60^\circ$로 검산하면

$$
\cos90^\circ=\frac{\sqrt3}{2}\cdot\frac12-\frac12\cdot\frac{\sqrt3}{2}=0,\qquad \sin90^\circ=\frac12\cdot\frac12+\frac{\sqrt3}{2}\cdot\frac{\sqrt3}{2}=1
$$

이다. 다음 글에서 두 번째 막대의 방향을 성분으로 풀 때 이 공식을 쓴다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

원점을 중심으로 $\theta$만큼 돌리면 $\mathbf e_x$는 $\mathbf e_x'=(\cos\theta,\sin\theta)$로, $\mathbf e_y$는 $\mathbf e_y'=(-\sin\theta,\cos\theta)$로 간다. 막대에 붙은 점의 막대 좌표 $(s_x,s_y)$는 돌려도 그대로이고, 돌아간 점은 $s_x\mathbf e_x'+s_y\mathbf e_y'$다. 첫째 열이 $\mathbf e_x'$, 둘째 열이 $\mathbf e_y'$인 행렬 $R(\theta)$가 회전행렬이고, 행렬과 열벡터의 곱은 각 열에 성분을 곱해 더한 벡터다. 같은 곱을 행으로 읽으면 행마다 내적 하나다. 거꾸로 고정 좌표에서 막대 좌표를 되찾을 때는 돌아간 두 축으로 정사영하고, 그 행렬은 $R(\theta)^{\mathsf T}=R(-\theta)$다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

로봇 팔에 관절이 두 개 있으면 두 번째 막대는 첫 막대에 붙어서 함께 돈다. 두 번째 관절의 각도는 첫 막대를 기준으로 재므로, 두 번째 막대는 첫 막대의 막대 좌표로 놓인다. 다음 글에서는 이 글의 회전행렬로 두 번째 막대를 고정 좌표로 옮기고, 앞 글의 덧셈으로 손끝의 위치를 구한다.

</div>

## 참고 자료

- [Dan Margalit, Joseph Rabinoff, Interactive Linear Algebra, 2.3 Matrix Equations](https://textbooks.math.gatech.edu/ila/matrix-equations.html): 행렬과 벡터의 곱을 열의 일차결합으로 정의하고, 행마다 계산하는 방법을 함께 보인다.
- [Dan Margalit, Joseph Rabinoff, Interactive Linear Algebra, 3.3 Linear Transformations](https://textbooks.math.gatech.edu/ila/linear-transformations.html): 행렬의 열이 표준 단위벡터가 옮겨 간 자리라는 사실과, 반시계 방향 회전의 행렬.
- [OpenStax, Algebra and Trigonometry 2e, 9.2 Sum and Difference Identities](https://openstax.org/books/algebra-and-trigonometry-2e/pages/9-2-sum-and-difference-identities): 두 각의 합에 대한 코사인과 사인의 공식.
