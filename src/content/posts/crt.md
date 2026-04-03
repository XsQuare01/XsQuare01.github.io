---
title: "Chinese Remainder Theorem — 중국인의 나머지 정리"
date: 2026-03-24T12:00:00
description: "서로소인 여러 모듈러스에 대한 연립 합동식이 항상 유일한 해를 가짐을 구성적으로 증명하고, 단계별 계산 예시와 RSA-CRT 속도 최적화까지 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
difficulty: 중급
---

> 서로 다른 시계 여러 개가 동시에 특정 시각을 가리키는 순간은 언제인가 — 중국인의 나머지 정리는 이 질문에 항상 유일한 답이 존재함을 보장하고, 그 답을 명시적으로 구성한다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>설정</strong>: m₁,...,mᵣ이 서로 쌍으로 서로소(pairwise coprime)이고 m = m₁···mᵣ</li>
<li><strong>보장</strong>: 임의의 c₁,...,cᵣ에 대해 x ≡ cᵢ (mod mᵢ)를 동시에 만족하는 x가 mod m에서 유일하게 존재</li>
<li><strong>구성</strong>: Mᵢ = m/mᵢ,  Nᵢ = Mᵢ⁻¹ mod mᵢ,  x = Σ cᵢ·Mᵢ·Nᵢ mod m</li>
<li><strong>응용</strong>: RSA-CRT 최적화 (처리 속도 약 4배 향상)</li>
</ul>
</div>

## 정확한 설정

**$m_1, \ldots, m_r$이 쌍으로 서로소(pairwise coprime)**: 임의의 $i \neq j$에 대해 $\gcd(m_i, m_j) = 1$.

여기서 주의할 점은 **전체 gcd가 1인 것** 과 **쌍으로 서로소** 는 다르다는 것이다. 예를 들어 $\{6, 10, 15\}$는 $\gcd(6,10,15)=1$이지만, $\gcd(6,10)=2 \neq 1$이므로 쌍으로 서로소가 아니다.

$m = m_1 \cdot m_2 \cdots m_r$로 정의한다.

**정리**: 임의의 정수 $c_1, \ldots, c_r$에 대해, 다음 연립 합동식을 동시에 만족하는 $x$가 $\bmod\ m$에서 **유일하게** 존재한다.

$$
x \equiv c_1 \pmod{m_1}, \quad x \equiv c_2 \pmod{m_2}, \quad \ldots, \quad x \equiv c_r \pmod{m_r}
$$

## 유일성 증명

$x$와 $y$가 모두 연립 합동식을 만족한다고 하자. 그러면 각 $i$에 대해

$$
x \equiv c_i \pmod{m_i}, \quad y \equiv c_i \pmod{m_i} \implies m_i \mid (x - y)
$$

$m_1, \ldots, m_r$이 쌍으로 서로소이고 모두 $(x-y)$를 나누므로, 이들의 곱도 $(x-y)$를 나눈다.

$$
m = m_1 \cdots m_r \mid (x - y) \implies x \equiv y \pmod{m}
$$

따라서 해는 $\bmod\ m$에서 유일하다.

## 존재성 증명 — 구성 (Construction)

다음과 같이 변수를 정의한다.

$$
M_i = \frac{m}{m_i} \quad \text{($m_i$를 제외한 나머지를 모두 곱한 값)}
$$

$M_i$와 $m_i$는 서로소이다 ($m_i$를 제외한 나머지의 곱이므로). 따라서 $M_i$의 $\bmod\ m_i$ 역원이 존재한다.

$$
N_i = M_i^{-1} \pmod{m_i} \quad \text{(베주 항등식으로 계산)}
$$

이제 다음을 해(解)로 정의한다.

$$
x = \sum_{i=1}^{r} c_i M_i N_i \pmod{m}
$$

**검증**: $j$번째 조건 $x \equiv c_j \pmod{m_j}$를 확인한다.

$$
x \bmod m_j = \sum_{i=1}^{r} c_i M_i N_i \bmod m_j
$$

- $i \neq j$인 항: $M_i = m/m_i$에 $m_j$가 인수로 포함되어 있으므로 $M_i \equiv 0 \pmod{m_j}$. 해당 항은 사라진다.
- $i = j$인 항: $M_j N_j \equiv 1 \pmod{m_j}$ (역원의 정의). 따라서 $c_j M_j N_j \equiv c_j \pmod{m_j}$.

$$
x \equiv c_j \pmod{m_j} \quad \checkmark
$$

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>CRT는 "여러 개의 작은 시계를 보고 하나의 큰 시계 시각을 알아내는 방법"이다. 서로소인 여러 수로 나눈 나머지들을 동시에 만족하는 수가 딱 하나 존재하고, 그 수를 명시적으로 구성할 수 있다. RSA에서는 이를 이용해 큰 수의 연산을 작은 수들의 연산으로 쪼개서 약 4배 빠르게 처리한다.</p>
</div>

## 단계별 계산 예시

연립 합동식: $x \equiv 2 \pmod{3}$,  $x \equiv 3 \pmod{5}$,  $x \equiv 2 \pmod{7}$

$m = 3 \times 5 \times 7 = 105$

![CRT 구성 계산표](/images/crt/construction.svg)

**단계 1** — $M_i$ 계산:

$$
M_1 = \frac{105}{3} = 35, \quad M_2 = \frac{105}{5} = 21, \quad M_3 = \frac{105}{7} = 15
$$

**단계 2** — $N_i$ 계산 (베주 항등식 또는 직접 탐색):

$$
35 \equiv 2 \pmod{3} \implies N_1 = 2^{-1} \pmod{3} = 2 \quad (2 \times 2 = 4 \equiv 1)
$$

$$
21 \equiv 1 \pmod{5} \implies N_2 = 1^{-1} \pmod{5} = 1
$$

$$
15 \equiv 1 \pmod{7} \implies N_3 = 1^{-1} \pmod{7} = 1
$$

**단계 3** — 합산:

$$
x = 2 \cdot 35 \cdot 2 + 3 \cdot 21 \cdot 1 + 2 \cdot 15 \cdot 1 = 140 + 63 + 30 = 233
$$

$$
233 \bmod 105 = 23
$$

**검증**: $23 = 7 \times 3 + 2$ ✓,  $23 = 4 \times 5 + 3$ ✓,  $23 = 3 \times 7 + 2$ ✓

## 연산 보존 성질

$x$가 $(c_1, \ldots, c_r)$에, $y$가 $(d_1, \ldots, d_r)$에 대응할 때, CRT 표현에서의 연산이 원래 연산을 보존한다.

$$
x + y \longleftrightarrow (c_1 + d_1,\ c_2 + d_2,\ \ldots,\ c_r + d_r)
$$

$$
x \cdot y \longleftrightarrow (c_1 d_1,\ c_2 d_2,\ \ldots,\ c_r d_r)
$$

즉, $m$에 대한 큰 연산을 $m_i$들에 대한 작은 연산들로 **분해** 할 수 있고, 결과를 다시 합칠 수 있다. 이것이 CRT 최적화의 핵심이다.

## 응용 — RSA-CRT 최적화

RSA 복호화는 $m = c^d \bmod n$ ($n = pq$)을 계산하는데, $d$가 수백 비트이면 비용이 크다.

**RSA-CRT 방법**: $n = pq$ ($p$, $q$ 소수, $\gcd(p,q)=1$)일 때 CRT를 적용한다.

$$
m_p = c^{d_p} \pmod{p}, \quad d_p = d \bmod (p-1) \quad \text{(페르마의 소정리 적용)}
$$

$$
m_q = c^{d_q} \pmod{q}, \quad d_q = d \bmod (q-1)
$$

$m_p$와 $m_q$를 구한 뒤 CRT로 $m \bmod n$을 복원한다.

**속도 향상 이유**: 지수 연산의 복잡도는 모듈러스 크기의 제곱에 비례한다. $n$ 대신 $p$와 $q$ ($n$의 절반 크기)로 나누어 계산하면, 각각 $1/4$ 비용이고 두 번 수행하므로 전체는 **약 $1/2$** 비용이다. 실제로는 CRT 조합 과정까지 포함해도 약 **4배** 가속이 가능하다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>CRT는 쌍으로 서로소인 모듈러스들에 대한 연립 합동식이 mod m에서 유일한 해를 가짐을 보장한다.</li>
<li>유일성: 두 해의 차가 모든 mᵢ의 배수이므로 m의 배수 → mod m에서 동일. 존재성: 구성적 증명으로 해를 명시적으로 구성한다.</li>
<li>연산 보존 성질 덕분에 큰 모듈러스 연산을 작은 연산들로 분해·병렬화할 수 있다. 이것이 RSA-CRT의 수학적 근거다.</li>
<li>RSA-CRT는 n=pq 구조를 활용해 복호화 속도를 약 4배 향상시키는 실용적 최적화 기법이다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Find Prime — 소수 판별과 확률적 소수 탐색</strong> — 소수 밀도 추정, Fermat 테스트의 한계, Witness와 Miller-Rabin 테스트까지 — RSA에서 큰 소수를 어떻게 찾는지 다룬다.</p>
</div>
