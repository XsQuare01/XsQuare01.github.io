---
title: "Modular Arithmetic — 모듈러 산술과 잉여계"
date: 2026-03-24T11:00:00
description: "모듈러 산술의 동치 관계, 완전·축약 잉여계, 오일러 정리와 페르마의 소정리, 중국인의 나머지 정리(CRT)까지 — RSA를 비롯한 공개키 암호의 수학적 엔진을 완성한다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> GCD가 '두 수의 관계'라면, 모듈러 산술은 '수의 세계 자체를 재정의'한다. 나머지를 공유하는 수들을 하나로 묶는 순간, 덧셈·곱셈·역원이 정의된 대수 구조가 탄생한다 — RSA, ElGamal, Diffie-Hellman의 계산 엔진이 바로 이 위에서 돌아간다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>모듈러 산술</strong>: a ≡ b (mod m) ↔ m | (b − a) — 동치 관계(반사·대칭·추이) 성립</li>
<li><strong>완전 잉여계 Zm</strong>: {0, 1, ..., m−1} — 덧셈·뺄셈에 대해 닫혀있음</li>
<li><strong>축약 잉여계 Zm*</strong>: {a | gcd(a, m) = 1} — 곱셈에 대해 닫혀있고 역원 존재</li>
<li><strong>오일러 정리</strong>: a^φ(m) ≡ 1 (mod m) (a ∈ Zm*, φ(m) = |Zm*|)</li>
<li><strong>중국인의 나머지 정리</strong>: 서로소인 m1,...,mr에 대해 연립 합동식의 해 존재·유일</li>
</ul>
</div>

## GCD와 LCM의 관계

본론에 앞서, GCD와 LCM(최소공배수)의 관계를 정리한다.

$a$와 $b$의 최대공약수가 $d = \gcd(a, b)$이고 $a = a'd$, $b = b'd$로 쓰면,

$$
\text{lcm}(a, b) = a'b'd
$$

따라서 다음이 성립한다.

$$
\gcd(a, b) \cdot \text{lcm}(a, b) = d \cdot a'b'd = a'b'd^2 = a \cdot b
$$

특히 $a$, $b$가 서로소이면 $d = 1$이므로 $\text{lcm}(a, b) = ab$이다.

## 모듈러 산술과 동치 관계

**모듈러 산술(Modular Arithmetic)** 은 다음과 같이 정의한다.

$$
a \equiv b \pmod{m} \iff m \mid (b - a)
$$

직관적으로 $a$와 $b$를 $m$으로 나눴을 때 나머지가 같다는 의미이다.

이 관계는 **동치 관계(Equivalence Relation)** 이다 — 다음 세 성질을 만족한다.

![mod 7 시계 다이어그램 — 동치류 시각화](/images/modular/clock-equivalence.svg)

**반사성(Reflexive)**: $a \equiv a \pmod{m}$

$m \mid 0$이므로 성립.

**대칭성(Symmetric)**: $a \equiv b \pmod{m} \implies b \equiv a \pmod{m}$

$m \mid (b-a)$이면 $m \mid (a-b)$이므로 성립.

**추이성(Transitive)**: $a \equiv b \pmod{m}$이고 $b \equiv c \pmod{m}$이면 $a \equiv c \pmod{m}$

$m \mid (b-a)$, $m \mid (c-b)$이면 $m \mid (c-a)$이므로 성립.

따라서 $a \equiv b \pmod{m}$은 "$a$와 $b$가 모듈러 연산에서 같은 부류에 속한다"는 의미이다.

## 모듈러 연산의 보존 성질

$a \equiv b \pmod{m}$이고 $c \equiv d \pmod{m}$이면 다음이 성립한다.

$$
a + c \equiv b + d \pmod{m}
$$
$$
a - c \equiv b - d \pmod{m}
$$
$$
ac \equiv bd \pmod{m}
$$

**증명**: $b - a = mk$, $d - c = mk'$로 쓰면,

1. $(b+d) - (a+c) = (b-a) + (d-c) = m(k+k')$ — 덧셈 성립
2. $(b-d) - (a-c) = (b-a) - (d-c) = m(k-k')$ — 뺄셈 성립
3. $bd = (a+mk)(c+mk') = ac + m(ak'+ck+mkk')$ — 곱셈 성립

마찬가지로 상수 연산과 지수 연산에 대해서도 닫혀있다.

$$
a \equiv b \pmod{m} \implies a + k \equiv b + k \pmod{m}
$$
$$
a \equiv b \pmod{m} \implies ak \equiv bk \pmod{m}
$$
$$
a \equiv b \pmod{m} \implies a^n \equiv b^n \pmod{m}
$$

단, **나눗셈은 일반적으로 성립하지 않는다**. 예를 들어 $\text{mod}\ 6$에서 $2 \cdot 3 \equiv 0$이므로, 곱셈의 결과만으로는 원래 인수를 복원할 수 없다.

![모듈러 연산 보존 성질 — 덧셈·곱셈·지수 예시](/images/modular/operation-preservation.svg)

## 완전 잉여계 (Complete Residue System)

**완전 잉여계** $\mathbb{Z}_m$은 $m$으로 나눈 나머지 전체의 집합이다.

$$
\mathbb{Z}_m = \{0, 1, 2, \ldots, m-1\}
$$

이 집합의 원소는 두 가지 방식으로 해석할 수 있다.

1. **정수 자체**: 원소 $2$는 정수 $2$를 의미한다.
2. **동치류(Equivalence Class)**: 원소 $2$는 $m$으로 나눴을 때 나머지가 $2$인 모든 정수의 집합 $\{\ldots, 2-m, 2, 2+m, 2+2m, \ldots\}$를 의미한다.

$\mathbb{Z}_m$에서 **덧셈과 뺄셈은 잘 정의된다(well-defined)** — 연산 결과가 집합 안에 존재하고, 항등원($0$)과 역원이 존재한다. 원소 $a$의 덧셈 역원은 $-a \equiv m - a \pmod{m}$이다.

**정리**: $ka \equiv kb \pmod{m}$이고 $\gcd(k, m) = 1$이면 $a \equiv b \pmod{m}$이다.

**증명**: $m \mid k(a-b)$이고 $\gcd(k,m)=1$이므로, GCD 성질에 의해 $m \mid (a-b)$.

## 축약 잉여계 (Reduced Residue System)

**축약 잉여계** $\mathbb{Z}_m^*$는 $m$과 서로소인 원소들의 집합이다.

$$
\mathbb{Z}_m^* = \{a \in \mathbb{Z}_m \mid \gcd(a, m) = 1\}
$$

![잉여계 시각화](/images/modular/residue-systems.svg)

이 집합에서 **곱셈과 나눗셈은 잘 정의된다**.

**닫힘(Closure)**: $a, b \in \mathbb{Z}_m^*$이면 $\gcd(a, m) = 1$, $\gcd(b, m) = 1$이므로 GCD 서로소 성질에 의해 $\gcd(ab, m) = 1$. 따라서 $ab \in \mathbb{Z}_m^*$.

**역원 존재**: $\gcd(a, m) = 1$이므로 베주 항등식에 의해 $ax + my = 1$인 정수 $x$, $y$가 존재한다. 이를 $\bmod\ m$으로 취하면 $ax \equiv 1 \pmod{m}$이므로 $x$가 $a$의 곱셈 역원이다.

반면 **덧셈은 닫혀있지 않다**. 예를 들어 $m = 3$에서 $\gcd(4, 3) = \gcd(8, 3) = 1$이지만, $\gcd(4+8, 3) = \gcd(12, 3) = 3 \neq 1$.

**$m$이 소수(prime)일 때**: $1$부터 $m-1$까지 모든 수가 $m$과 서로소이므로

$$
\mathbb{Z}_m^* = \mathbb{Z}_m \setminus \{0\}, \quad \mathbb{Z}_m = \mathbb{Z}_m^* \cup \{0\}
$$

이 경우 $\mathbb{Z}_m$은 사칙연산이 모두 잘 정의된 **체(Field)** 가 된다.

## 오일러 정리

$$
a \in \mathbb{Z}_m^* \implies a^{\phi(m)} \equiv 1 \pmod{m}
$$

여기서 $\phi(m) = |\mathbb{Z}_m^*|$는 **오일러 피함수(Euler's totient function)** 이다.

예: $m = 10$이면 $\mathbb{Z}_{10}^* = \{1, 3, 7, 9\}$이므로 $\phi(10) = 4$.

$$
3^4 = 81 \equiv 1 \pmod{10}, \quad 7^4 = 2401 \equiv 1 \pmod{10}
$$

![오일러 정리 — b·Zm* = Zm* 전단사 대응 시각화](/images/modular/euler-theorem.svg)

**증명**: $\mathbb{Z}_m^* = \{a_1, \ldots, a_{\phi(m)}\}$에서 임의의 $b \in \mathbb{Z}_m^*$에 대해

$$
b\mathbb{Z}_m^* = \{ba_1, \ldots, ba_{\phi(m)}\}
$$

$\mathbb{Z}_m^*$는 곱셈에 대해 닫혀있으므로 $ba_i \in \mathbb{Z}_m^*$. 또한 $a_i \neq a_j$이면 $ba_i \neq ba_j$이므로 ($b$가 역원을 가지므로 양변에 $b^{-1}$ 곱 가능), 두 집합은 동일하다.

$$
\prod_{i=1}^{\phi(m)} a_i \equiv \prod_{i=1}^{\phi(m)} ba_i = b^{\phi(m)} \cdot \prod_{i=1}^{\phi(m)} a_i \pmod{m}
$$

$\prod a_i \in \mathbb{Z}_m^*$는 역원을 가지므로 양변에 곱하면

$$
b^{\phi(m)} \equiv 1 \pmod{m}
$$

## 페르마의 소정리

오일러 정리에서 $m = p$ (소수)로 놓으면 $\phi(p) = p - 1$이므로,

$$
a \in \mathbb{Z}_p^* \implies a^{p-1} \equiv 1 \pmod{p}
$$

이것이 **페르마의 소정리(Fermat's Little Theorem)** 이다. RSA에서 복호화 정확성을 보장하는 핵심 정리이다.

<div class="callout">
<div class="callout-title">참고</div>
<p>페르마의 소정리의 두 가지 증명, 모듈러 역원 공식(a^(p−2)), 페르마 소수 판별법, Carmichael 수의 한계까지 자세히 다룬다. → <strong>Fermat's Little Theorem — 페르마의 소정리</strong></p>
</div>

## 중국인의 나머지 정리 (CRT)

**설정**: $m_1, \ldots, m_r$이 서로 쌍으로 서로소(pairwise coprime)이고 $m = m_1 \cdots m_r$일 때,

임의의 $c_1, \ldots, c_r$에 대해 다음을 동시에 만족하는 $x$가 $\bmod\ m$에서 유일하게 존재한다.

$$
x \equiv c_1 \pmod{m_1}, \quad x \equiv c_2 \pmod{m_2}, \quad \ldots, \quad x \equiv c_r \pmod{m_r}
$$

![CRT 구성 다이어그램 — 단계별 해 구성](/images/modular/crt-construction.svg)

**구성(Construction)으로 증명**: 다음과 같이 정의한다.

$$
M_i = \frac{m}{m_i}, \quad N_i = M_i^{-1} \pmod{m_i}
$$

$M_i$와 $m_i$는 서로소이므로(정의에 의해) $N_i$가 존재한다. 그러면

$$
x = \sum_{i=1}^{r} c_i M_i N_i \pmod{m}
$$

**검증**: $x \bmod m_j$를 계산하면, $i \neq j$인 항에는 $M_i = m/m_i$에 $m_j$가 인수로 포함되어 $M_i \equiv 0 \pmod{m_j}$. 따라서

$$
x \equiv c_j M_j N_j \equiv c_j \cdot 1 = c_j \pmod{m_j}
$$

**연산 보존**: $x$가 $(c_1, \ldots, c_r)$에, $y$가 $(d_1, \ldots, d_r)$에 대응할 때,

$$
x + y \leftrightarrow (c_1 + d_1, \ldots, c_r + d_r)
$$
$$
x \cdot y \leftrightarrow (c_1 d_1, \ldots, c_r d_r)
$$

즉 $m$에 대한 연산을 각 $m_i$에 대한 작은 연산들로 분해할 수 있다. 이것이 CRT를 대규모 모듈러 연산 최적화에 활용하는 이유이다.

<div class="callout">
<div class="callout-title">참고</div>
<p>유일성 증명, 단계별 수치 계산 예시(x≡2(mod 3), x≡3(mod 5), x≡2(mod 7) → x=23), RSA-CRT 4배 속도 향상까지 자세히 다룬다. → <strong>Chinese Remainder Theorem — 중국인의 나머지 정리</strong></p>
</div>

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>모듈러 산술은 동치 관계를 형성한다. 덧셈·뺄셈·곱셈·지수 연산에 대해 닫혀있지만, 나눗셈은 일반적으로 성립하지 않는다.</li>
<li>Zm*는 gcd(a, m) = 1인 원소들로 이루어지며, 곱셈 역원이 모든 원소에 존재한다. m이 소수이면 Zm은 완전한 체(Field)가 된다.</li>
<li>오일러 정리(a^φ(m) ≡ 1)와 페르마의 소정리(a^(p−1) ≡ 1, p 소수)는 RSA 복호화의 수학적 근거이다.</li>
<li>CRT는 큰 모듈러 연산을 작은 연산들로 분해해 병렬 처리를 가능하게 한다. RSA-CRT 최적화의 핵심이다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>RSA — 공개키 암호의 수학적 구조</strong> — 지금까지 쌓아온 모든 정수론 도구(GCD, 모듈러 산술, 오일러 정리, 페르마 정리, CRT)가 수렴하는 지점. RSA 키 생성, 복호화 정확성 증명, 소인수분해 보안 근거, Square-and-Multiply 고속 지수연산까지 다룬다.</p>
</div>
