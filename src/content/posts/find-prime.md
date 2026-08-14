---
title: "Find Prime — 소수 판별과 확률적 소수 탐색"
date: 2026-03-26T10:00:00
description: "소수 밀도 추정, Fermat 테스트, Witness와 Carmichael 수의 한계, Witness 밀도 증명 — 임의의 큰 수가 소수인지 확률적으로 판별하는 방법을 단계적으로 구성한다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
difficulty: 중급
---

> RSA는 '두 큰 소수의 곱'에서 시작한다. 그렇다면 큰 소수는 어떻게 찾는가? 소수인지 아닌지조차 어떻게 확인하는가? 이 질문에 답하는 것이 Find Prime 문제다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li><strong>소수 밀도</strong>: 1~$n$ 범위에 약 $n / \ln n$개의 소수가 존재한다 (소수 정리)</li>
<li><strong>Fermat 판별법</strong>: $n$이 소수이면 $\gcd(a, n) = 1$인 모든 $a$에 대해 $a^{n-1} \equiv 1 \pmod{n}$</li>
<li><strong>Witness</strong>: $a^{n-1} \not\equiv 1 \pmod{n}$을 만족하는 $a$. $n$이 합성수임을 확인해 주는 증인</li>
<li><strong>Carmichael 수</strong>: Witness가 없는 합성수. Fermat 테스트를 통과하는 예외</li>
<li><strong>Witness 밀도</strong>: Carmichael 수가 아닌 합성수에서 Witness는 $\mathbb{Z}_n^*$의 절반 이상</li>
<li><strong>Find Prime</strong>: Witness 테스트를 $k$번 반복하면 오류 확률이 $1/2^k$ 이하</li>
</ul>
</div>

## 소수는 얼마나 많은가: 소수 정리

소수의 개수는 무한하다. 유클리드의 고전적인 증명부터 알려져 있다.

더 나아가, 소수의 **밀도**에 대한 정량적인 추정도 존재한다.

<div class="callout callout-info">
<div class="callout-title">소수 정리 (Prime Number Theorem)</div>

$1$부터 $n$까지의 정수 중 소수의 개수 $\pi(n)$은 다음과 같이 근사된다:

$$
\pi(n) \approx \frac{n}{\ln n}
$$

</div>

예를 들어 $n = 1{,}000{,}000$이면:

$$
\frac{1{,}000{,}000}{\ln 1{,}000{,}000} \approx \frac{1{,}000{,}000}{13.8} \approx 72{,}000
$$

실제 $\pi(1{,}000{,}000) = 78{,}498$이다. 근사값과 상당히 가깝다.

즉, 큰 수 근방에서 임의의 수를 골랐을 때 그것이 소수일 확률은 $1/\ln n$이다. $n$이 크더라도 소수는 드물지 않다.

## 소수 판별 문제

임의의 큰 수 $n$이 주어졌을 때, 이것이 소수인지 어떻게 확인할 수 있는가?

가장 단순한 방법은 $2$부터 $\sqrt{n}$까지 모든 수로 나누어 보는 것이지만, $n$이 수백 자리에 달하면 현실적으로 불가능하다. RSA에서 사용하는 소수는 통상 1024비트 이상이다.

여기서 **Fermat의 소정리**를 활용한 확률적 판별법이 등장한다.

## Fermat 소수 판별법

페르마의 소정리는 다음을 보장한다:

$$
n \text{이 소수이고 } \gcd(a, n) = 1 \implies a^{n-1} \equiv 1 \pmod{n}
$$

대우를 취하면:

$$
a^{n-1} \not\equiv 1 \pmod{n} \implies n \text{은 합성수}
$$

**판별 절차:**

1. $1 < a < n$이고 $\gcd(a, n) = 1$인 임의의 $a$를 선택한다.
2. $a^{n-1} \bmod n$을 계산한다.
3. 결과가 $1$이 아니면 $n$은 **확실히 합성수**다.
4. 결과가 $1$이면 $n$이 소수일 **가능성이 있다**. 확정은 아니다.

**예시: 8379 판별**

$$
35^{8378} \equiv 2989 \pmod{8379}
$$

$2989 \neq 1$이므로 $8379$는 합성수이다. (실제로 $8379 = 3 \times 2793 = 3 \times 3 \times 931$)

## Witness

$a^{n-1} \not\equiv 1 \pmod{n}$을 만족하는 $a$를 $n$의 **Witness**라 부른다. $n$이 합성수임을 증언하는 값이라는 의미다.

Witness가 하나라도 존재하면 $n$이 합성수임이 확정된다. 반대로 Witness를 찾지 못했다고 해서 $n$이 소수라는 보장은 없다.

<div class="callout callout-tip">
<div class="callout-title">여담: Twin Prime (쌍둥이 소수)</div>

두 소수의 차이가 2인 쌍을 **쌍둥이 소수**(Twin Prime)라 한다: $(3, 5),\ (5, 7),\ (11, 13),\ (17, 19), \ldots$

차이가 1일 수는 없다. 연속한 두 정수 중 하나는 반드시 짝수이기 때문이다. 3보다 큰 쌍둥이 소수는 모두 $(6k-1,\ 6k+1)$ 형태를 띤다.
</div>

## Carmichael 수: Fermat 판별법의 한계

문제가 있다. 합성수임에도 **모든** $\gcd(a, n) = 1$인 $a$에 대해 $a^{n-1} \equiv 1 \pmod{n}$을 만족하는 수가 존재한다.

이런 수들을 **Carmichael 수**라 한다. 즉, Carmichael 수는 Witness를 하나도 갖지 않는 합성수다.

가장 작은 Carmichael 수: $561 = 3 \times 11 \times 17$

$$
a^{560} \equiv 1 \pmod{561} \quad \text{for all } \gcd(a, 561) = 1
$$

Carmichael 수에 대해서는 Fermat 테스트가 전혀 동작하지 않는다.

## Witness의 밀도: 왜 반복 테스트가 효과적인가

Carmichael 수를 제외한 합성수에서는 Witness가 얼마나 많은가?

**주장**: Carmichael 수가 아닌 합성수 $n$에서 Witness의 수는 $\mathbb{Z}_n^*$의 **절반 이상**이다.

![Witness 밀도 — B에서 A로의 단사함수 시각화](/images/find-prime/witness-density.svg)

**증명:**

$\mathbb{Z}_n^*$를 Witness 집합 $A$와 non-Witness 집합 $B$로 분리한다:

$$
A = \{ a \in \mathbb{Z}_n^* \mid a^{n-1} \not\equiv 1 \pmod{n} \}
$$

$$
B = \{ b \in \mathbb{Z}_n^* \mid b^{n-1} \equiv 1 \pmod{n} \}
$$

$n$이 Carmichael 수가 아니므로 적어도 하나의 Witness $a \in A$가 존재한다. 이제 함수 $f: B \to \mathbb{Z}_n^*$를

$$
f(b) = ab
$$

로 정의하면:

- $b^{n-1} \equiv 1 \pmod{n}$이고 $a^{n-1} \equiv k \pmod{n}$ ($k \neq 1$)이므로,

$$
(ab)^{n-1} \equiv k \cdot 1 = k \not\equiv 1 \pmod{n}
$$

- 따라서 $ab \in A$, 즉 $f(b)$는 Witness다.

$f$는 단사(injective)이므로 $|B| \leq |A|$. 따라서:

$$
|A| \geq \frac{|\mathbb{Z}_n^*|}{2}
$$

**임의의 $a$를 골랐을 때 그것이 Witness일 확률은 $\geq 1/2$이다.**

## Find Prime 알고리즘

위 결과를 바탕으로 소수를 찾는 확률적 알고리즘을 구성할 수 있다.

![Find Prime 알고리즘 흐름도](/images/find-prime/algorithm.svg)

페르마 테스트를 그대로 쓸 수는 없다. Carmichael 수를 걸러 내야 하는데, **어떤 수가 Carmichael 수인지 미리 판별하는 빠른 방법이 없기 때문이다.** 그것을 알려면 사실상 소인수분해를 해야 하고, 그럴 수 있다면 애초에 소수 판정이 끝난다.

그래서 실제로는 페르마 테스트를 조금 고친 **밀러·라빈(Miller–Rabin) 테스트**를 쓴다. 이 테스트는 Carmichael 수에도 통한다.

### 밀러·라빈 한 라운드

홀수 $n$에 대해 $n - 1 = 2^s d$ ($d$는 홀수)로 쓴다. 밑 $a$를 하나 잡고 다음을 본다.

1. $x = a^d \bmod n$을 계산한다. $x \equiv 1$ 또는 $x \equiv -1$이면 이 밑은 **통과**다.
2. 아니면 $x \leftarrow x^2 \bmod n$을 최대 $s-1$번 되풀이한다. 도중에 $x \equiv -1$이 되면 **통과**다.
3. 끝까지 $-1$을 만나지 못하면 $a$는 **증인(witness)** 이고, $n$은 합성수로 **확정**된다.

페르마 테스트가 $a^{n-1} \equiv 1$ 하나만 보는 데 비해, 밀러·라빈은 그 값에 이르는 제곱근들까지 살핀다. 소수 $n$에서는 $1$의 제곱근이 $\pm 1$뿐인데 합성수에서는 그렇지 않다는 점을 쓰는 것이다. Carmichael 수가 페르마 테스트를 빠져나가는 것도 이 자리에서 막힌다.

### 알고리즘

1. 임의의 홀수 $n$을 선택한다.
2. 작은 소수들로 나눠 본다. 나누어떨어지면 합성수이므로 1로 돌아간다. 값싼 걸러 내기이고 생략해도 정확성에는 영향이 없다.
3. $1 < a < n-1$인 임의의 $a$를 고른다.
4. 밑 $a$로 밀러·라빈 한 라운드를 돌린다.
   - 증인이면 $n$은 합성수 → 1로 돌아간다.
   - 통과하면 3으로 돌아가 다른 $a$로 반복한다.

$k$번을 모두 통과하면 $n$을 **아마도 소수(probable prime)** 로 판정한다. 통과는 소수라는 증명이 아니라 합성수라는 증거를 $k$번 찾지 못했다는 뜻이다.

**오류 확률 분석:**

홀수 합성수 $n$에 대해, 무작위로 고른 밑이 밀러·라빈 한 라운드를 통과할 확률은 $1/4$ 이하다. Carmichael 수를 포함해 모든 홀수 합성수에서 성립한다. 따라서

$$
P(\text{오판}) \leq \left(\frac{1}{4}\right)^k
$$

$k = 50$이면 $4^{-50} = 2^{-100}$으로, 실용적으로는 $0$에 수렴한다.

<div class="callout callout-simple">
<div class="callout-title">페르마 테스트의 상계와 다르다</div>

앞 절에서 본 페르마 테스트의 $\left(\frac{1}{2}\right)^k$는 **Carmichael 수가 아닌** 합성수에 대해서만 성립한다. 게다가 밑을 단위군에서 독립·균등하게 뽑는다는 전제도 붙는다. Carmichael 수에서는 서로소인 밑이 모두 통과하므로 상계 자체가 뜻을 잃는다.

밀러·라빈의 $\left(\frac{1}{4}\right)^k$에는 그런 예외가 없다. 두 수를 같은 것으로 보고 비교하면 안 된다.

</div>

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>소수 정리에 의해 1~$n$ 범위에 약 $n/\ln n$개의 소수가 존재한다. 큰 소수는 충분히 많다.</li>
<li>Fermat 테스트: $a^{n-1} \not\equiv 1 \pmod{n}$이면 $n$은 합성수. 통과했다고 소수가 아니다.</li>
<li>Carmichael 수는 Witness가 없는 합성수이며, Fermat 테스트의 맹점이다.</li>
<li>Carmichael 수만 걸러내면, 나머지 합성수에서 Witness는 절반 이상 존재한다.</li>
<li>테스트를 $k$번 반복하면 오판 확률이 $1/2^k$ 이하로 줄어든다. RSA의 소수 생성은 이 원리에 기반한다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>RSA: 공개키 암호의 수학적 구조</strong>. 소수 생성부터 키 생성, 암복호화, 오일러 정리 기반 정확성 증명, Square-and-Multiply 최적화까지 RSA 전체를 다룬다.</p>
</div>
