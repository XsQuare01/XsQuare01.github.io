---
title: "Greatest Common Divisor — 최대공약수와 유클리드 호제법"
date: 2026-03-24T10:15:00
description: "암호학의 핵심 도구인 최대공약수(GCD)를 대수적으로 정의하고, 유클리드 호제법과 확장 유클리드 알고리즘(베주 항등식)을 엄밀하게 증명한다. 서로소의 성질과 GCD 정의의 동치 증명까지 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
difficulty: 입문
---

> Division Theorem이 나눗셈의 기초라면, GCD는 그 위에 세워진 정수론의 첫 번째 건물이다. 두 정수가 공유하는 가장 큰 약수는 단순한 수치를 넘어, 베주 항등식을 통해 암호학의 핵심 알고리즘을 뒷받침한다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>GCD 대수적 정의</strong>: d | a, d | b이고, c | a, c | b이면 c | d가 되는 유일한 d ≥ 0</li>
<li><strong>유클리드 호제법</strong>: gcd(b, a) = gcd(a, r), 나머지가 0이 될 때까지 반복</li>
<li><strong>확장 유클리드 알고리즘</strong>: gcd(a, b) = xa + yb (베주 항등식)</li>
<li><strong>서로소 성질</strong>: gcd(a, b) = 1 ↔ ax + by = 1인 정수 x, y가 존재</li>
</ul>
</div>

## GCD 정의

임의의 정수 $a$, $b$에 대해, **최대공약수** $d = \gcd(a, b)$는 다음 두 조건을 동시에 만족하는 유일한 정수 $d \geq 0$이다.

1. $d \mid a$ 이고 $d \mid b$
2. 모든 정수 $c$에 대해 $c \mid a$ 이고 $c \mid b$ 이면, $c \mid d$

두 번째 조건이 핵심이다. 일상적인 정의("공약수 중 가장 큰 수")에서는 $c \leq d$를 요구하지만, $c \mid d$는 이보다 엄밀한(tight한) 조건이다 — $c$가 $d$의 약수이면 자동으로 $c \leq d$이기 때문이다.

$a$와 $b$가 **서로소(coprime)** 이면 $\gcd(a, b) = 1$이다.

## GCD 계산

GCD를 구하는 방법은 크게 두 가지다.

**소인수분해(Factorization)**: 두 수를 각각 소인수분해한 뒤 공통 소인수의 최솟값을 곱한다. 직관적이지만, 큰 수에서는 소인수분해 자체가 NP와 co-NP의 교집합에 속하는 난문제로 매우 느리다.

**유클리드 호제법(Euclid Algorithm)**: 나머지 연산을 반복해 빠르게 GCD를 구한다.

## 유클리드 호제법

양의 정수 $a$, $b$에 대해, 나머지가 0이 될 때까지 다음 과정을 반복한다.

$$
b = q_1 a + r_1
$$
$$
a = q_2 r_1 + r_2
$$
$$
r_1 = q_3 r_2 + r_3
$$
$$
\vdots
$$
$$
r_{k-2} = q_k r_{k-1} + r_k
$$
$$
r_{k-1} = q_{k+1} r_k + 0
$$

이때 $\gcd(a, b) = r_k$이다. 핵심 관계식은 다음과 같다.

$$
b = qa + r \implies \gcd(b, a) = \gcd(a, r)
$$

![유클리드 호제법 시각화](/images/gcd/euclid-algorithm.svg)

**증명** — 공약수 집합의 상호 포함으로 증명한다.

$\gcd(b, a)$의 원소들의 집합을 $D_1$, $\gcd(a, r)$의 원소들의 집합을 $D_2$라 하자.

**$D_1 \subseteq D_2$**: $p \in D_1$이면 $p \mid b$, $p \mid a$. $r = b - qa$이므로 $p \mid (b - qa)$, 즉 $p \mid r$. 따라서 $p \mid a$, $p \mid r$이므로 $p \in D_2$.

**$D_2 \subseteq D_1$**: $p \in D_2$이면 $p \mid a$, $p \mid r$. $b = qa + r$이므로 $p \mid b$. 따라서 $p \mid a$, $p \mid b$이므로 $p \in D_1$.

두 방향 포함이 성립하므로 $D_1 = D_2$, 즉 $\gcd(b, a) = \gcd(a, r)$이다.

## 확장 유클리드 알고리즘

유클리드 호제법의 각 단계를 역으로 거슬러 올라가면, GCD를 $a$와 $b$의 **일차 결합(linear combination)** 으로 표현할 수 있다.

$$
r_k = r_{k-2} - q_k r_{k-1}
$$

$r_{k-1}$을 다시 $r_{k-3}$과 $r_{k-2}$로 표현하고 이 과정을 반복하면,

$$
r_k = (1 + q_k q_{k-1}) r_{k-2} - q_k r_{k-3}
$$

최종적으로 $r_k$를 $a$와 $b$의 일차 결합으로 나타낼 수 있다.

$$
\gcd(a, b) = xa + yb \quad (x, y \in \mathbb{Z})
$$

이것이 **베주 항등식(Bézout's Identity)** 이다. $x$와 $y$는 $a$, $b$에 의존하며 유일하지 않다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>확장 유클리드 알고리즘은 "GCD를 구하는 과정을 거꾸로 되감으면, GCD를 두 원래 수의 덧셈·뺄셈 조합으로 표현할 수 있다"는 뜻이다. 예를 들어 gcd(12, 8) = 4이면, 4 = 12 × 1 + 8 × (−1)처럼 쓸 수 있다. 이 성질이 RSA에서 비밀키를 계산하는 핵심 도구가 된다.</p>
</div>

## 서로소의 성질

### 성질 1: 서로소 판별 기준

$$
\gcd(a, b) = 1 \iff \text{어떤 정수 } x, y \text{에 대해 } ax + by = 1
$$

**증명 (⟹)**: $\gcd(a, b) = 1$이면 베주 항등식에 의해 $ax + by = 1$인 $x, y$가 존재한다.

**증명 (⟸)**: $ax + by = 1$을 만족하는 $x, y$가 존재한다고 하자. $d = \gcd(a, b)$라 하면 $d \mid a$, $d \mid b$이므로 $d \mid (ax + by) = 1$. 따라서 $d \leq 1$이고, $d \geq 0$이므로 $d = 1$.

### 성질 2: 서로소와 배수

$$
a \mid bc \text{ 이고 } \gcd(a, b) = 1 \implies a \mid c
$$

**증명**: $\gcd(a, b) = 1$이므로 $ax + by = 1$인 $x, y$가 존재한다. 양변에 $c$를 곱하면 $acx + bcy = c$. $bc = ka$ (가정에서 $a \mid bc$)를 대입하면 $acx + kay = c$, 즉 $a(cx + ky) = c$. 따라서 $a \mid c$.

### 성질 3: 서로소의 곱셈 보존

$$
\gcd(a, b) = 1 \text{ 이고 } \gcd(a, c) = 1 \implies \gcd(a, bc) = 1
$$

**증명**: $\gcd(a, b) = 1$이면 $ax_1 + by_1 = 1$, $\gcd(a, c) = 1$이면 $ax_2 + cy_2 = 1$인 정수들이 존재한다. 두 식을 곱하면,

$$
(ax_1 + by_1)(ax_2 + cy_2) = a(ax_1 x_2 + cx_1 y_2 + bx_2 y_1) + bc \cdot y_1 y_2 = 1
$$

이를 $a$와 $bc$의 일차 결합으로 표현했으므로, 성질 1에 의해 $\gcd(a, bc) = 1$.

## GCD 정의 동치 증명

일상적 정의("공약수 중 가장 큰 수")와 위의 대수적 정의가 동치임을 증명한다.

$A$, $B$, $D$를 각각 $a$, $b$, $d$의 약수 집합이라 하자. $d$가 최대공약수이려면 $D = A \cap B$, 즉 $d$의 약수 집합이 $a$와 $b$의 공약수 집합과 일치해야 한다.

**$A \cap B \subseteq D$**: $t \in A \cap B$이면 $t \mid a$, $t \mid b$. 베주 항등식 $d = xa + yb$에서 $t \mid (xa + yb) = d$. 따라서 $t \in D$.

**$D \subseteq A \cap B$**: $t \in D$이면 $t \mid d$, 즉 $d = tk$. $a = a'd$, $b = b'd$로 쓰면 $a = a'tk$, $b = b'tk$. 따라서 $t \mid a$, $t \mid b$이므로 $t \in A \cap B$.

두 방향 포함이 성립하므로 $D = A \cap B$. 두 정의가 동치임이 증명되었다.

## GCD 확장

GCD는 3개 이상의 정수로 자연스럽게 확장된다.

$d = \gcd(a, b, c)$는 다음을 만족하는 유일한 정수 $d \geq 0$이다.

1. $d \mid a$, $d \mid b$, $d \mid c$
2. 모든 정수 $e$에 대해 $e \mid a$, $e \mid b$, $e \mid c$이면 $e \mid d$

계산은 연속 적용으로 처리한다. $\gcd(a, b, c) = \gcd(\gcd(a, b), c)$.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>GCD의 대수적 정의는 "가장 큰 공약수"라는 직관적 정의와 동치이며, c | d 조건이 더 엄밀하고 다루기 쉽다.</li>
<li>유클리드 호제법은 gcd(b, a) = gcd(a, r)을 반복 적용해 로그 시간에 GCD를 구한다.</li>
<li>확장 유클리드 알고리즘(베주 항등식)은 gcd(a, b) = xa + yb를 보장한다. 이는 서로소 판별, 모듈러 역원 계산, RSA 키 생성의 수학적 근거가 된다.</li>
<li>서로소 성질(gcd = 1)은 정수론 전반에서 핵심 도구로 쓰이며, 특히 암호 시스템에서 키와 모듈러스의 관계를 보장하는 데 필수적이다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Modular Arithmetic — 모듈러 산술과 잉여계</strong> — GCD를 기반으로 모듈러 산술의 동치 관계를 정의하고, 완전·축약 잉여계, 오일러 정리, 페르마의 소정리, 중국인의 나머지 정리(CRT)까지 — 공개키 암호의 계산 엔진을 완성한다.</p>
</div>
