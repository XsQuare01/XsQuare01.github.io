---
title: "Division Theorem — 정수 나눗셈의 기초"
date: 2026-03-23T11:04:51
description: "암호학의 수학적 기반이 되는 Division Theorem(나눗셈 정리)을 엄밀하게 증명한다. 나누어 떨어짐의 정의와 성질, 소수의 정의를 살펴보고, 몫과 나머지의 존재성·유일성을 보인다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> 암호학의 수학적 토대는 정수론에서 시작된다. Division Theorem은 그 출발점이다 — 임의의 양의 정수를 다른 양의 정수로 나누면, 몫과 나머지가 유일하게 결정된다. 이 단순한 사실이 모듈러 산술, GCD, RSA의 기초가 된다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>나누어 떨어짐 (Divisibility)</strong>: a | b — b = ca인 정수 c가 존재할 때 a가 b를 나눈다</li>
<li><strong>나누어 떨어짐의 성질</strong>: 선형 결합 성질, 추이 성질</li>
<li><strong>소수 (Prime)</strong>: 1, -1, p, -p만이 약수인 정수 p (p > 1)</li>
<li><strong>Division Theorem</strong>: a, b > 0에 대해 b = qa + r (0 ≤ r < a)을 만족하는 유일한 정수 q, r이 존재한다</li>
</ul>
</div>

앞선 글에서 NP-Complete와 계산 복잡도 이론을 다뤘다. 이 글부터는 암호학의 수학적 기반이 되는 정수론을 살펴본다. Division Theorem은 모듈러 산술과 GCD를 이해하기 위한 출발점이다.

---

## 나누어 떨어짐 (Divisibility)

정수 $a, b, c$에 대해, $b = ca$가 성립할 때 (나머지가 0일 때) $a$가 $b$를 **나누어 떨어뜨린다**고 하며, 다음과 같이 표기한다.

$$a \mid b \quad (a \text{ divides } b)$$

| 표현 | 의미 |
|---|---|
| $a \mid b$ | a가 b를 나눈다 (a divides b) |
| a는 b의 **약수(divisor)** | b = ca인 정수 c가 존재한다 |
| b는 a의 **배수(multiple)** | a로 나누어 떨어진다 |

---

## 나누어 떨어짐의 성질

임의의 정수 $a, b, c, x, y$에 대해 다음 성질들이 성립한다.

**기본 성질:**

$$1 \mid a, \quad -1 \mid a, \quad a \mid 0$$

$$a \mid a, \quad a \mid -a, \quad -a \mid a, \quad -a \mid -a$$

**선형 결합 성질 (Linear Combination):**

$$a \mid b, \quad a \mid c \implies a \mid (bx + cy)$$

**증명:** $b = k_1 a$, $c = k_2 a$로 놓으면:

$$bx + cy = k_1 ax + k_2 ay = a(k_1 x + k_2 y)$$

$k_1 x + k_2 y$는 정수이므로 $a \mid (bx + cy)$.

**추이 성질 (Transitivity):**

$$a \mid b, \quad b \mid c \implies a \mid c$$

**증명:** $b = k_1 a$, $c = k_2 b = k_1 k_2 a$이다. $k_1 k_2$는 정수이므로 $a \mid c$.

---

## 소수 (Prime)

정수 $p$가 **소수(Prime)** 이면, $p > 1$이고 $p$의 약수는 $1,\ -1,\ p,\ -p$ 뿐이다.

---

## Division Theorem

<div class="callout callout-key">
<div class="callout-title">Division Theorem</div>
<p>양의 정수 a, b에 대해, 다음을 만족하는 유일한 정수 q, r이 존재한다.</p>
<p style="text-align:center"><strong>b = qa + r &nbsp;&nbsp; (0 ≤ r &lt; a)</strong></p>
<p>q를 <strong>몫(quotient)</strong>, r을 <strong>나머지(remainder)</strong>라 한다.</p>
</div>

![Division Theorem 시각화](/images/division-theorem/division-algorithm.svg)

증명은 **존재성**과 **유일성** 두 부분으로 나뉜다.

### 1. 존재성 (Existence)

$b$에서 $a$를 반복해서 빼면 반드시 음수가 된다. $b - ka < 0$이 되는 최솟값 $k$를 잡으면:

$$b - ka < 0, \quad b - (k-1)a \geq 0$$

$q = k - 1,\ r = b - (k-1)a$로 정의하면:

| 확인 항목 | 근거 |
|---|---|
| $b = qa + r$ | 대입하면 $b = (k-1)a + (b-(k-1)a) = b$ ✓ |
| $r \geq 0$ | $b - (k-1)a \geq 0$이므로 ✓ |
| $r < a$ | $b - ka < 0$에서 $r - a = b - ka < 0$이므로 ✓ |

따라서 조건을 만족하는 정수 $q, r$이 존재한다.

### 2. 유일성 (Uniqueness)

두 쌍 $(q_1, r_1)$과 $(q_2, r_2)$가 모두 조건을 만족하고 $r_1 \leq r_2$라 하자.

$$b = q_1 a + r_1 = q_2 a + r_2 \quad (0 \leq r_1 \leq r_2 < a)$$

두 식의 차를 구하면:

$$(q_1 - q_2)a = r_2 - r_1$$

$0 \leq r_2 - r_1 < a$이므로 우변은 $0$ 이상이고 $a$ 미만이다. 그런데 좌변 $(q_1 - q_2)a$는 $a$의 배수이고, $0 \leq x < a$를 만족하는 $a$의 배수는 $0$ 뿐이다.

$$\therefore \ r_2 - r_1 = 0 \implies r_1 = r_2, \quad q_1 = q_2$$
---

## 결론

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>a | b는 b = ca인 정수 c가 존재함을 뜻한다. 나누어 떨어짐은 선형 결합 성질과 추이 성질을 만족한다.</li>
<li>Division Theorem: 양의 정수 a, b에 대해 b = qa + r (0 ≤ r < a)을 만족하는 유일한 q, r이 존재한다.</li>
<li>존재성은 반복 빼기의 최소성 논리로, 유일성은 r₂ - r₁이 a의 배수이면서 a 미만임을 이용한 모순으로 증명한다.</li>
<li>이 정리는 모듈러 산술, GCD(유클리드 호제법), RSA 등 암호학 전반의 수학적 기반이 된다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Greatest Common Divisor — 최대공약수와 유클리드 호제법</strong> — GCD를 대수적으로 정의하고, Division Theorem을 기반으로 한 유클리드 호제법과 확장 유클리드 알고리즘(베주 항등식)을 엄밀하게 증명한다. 서로소의 성질과 GCD 정의의 동치 증명까지 다룬다.</p>
</div>
