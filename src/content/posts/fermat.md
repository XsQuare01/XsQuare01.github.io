---
title: "Fermat's Little Theorem — 페르마의 소정리"
date: 2026-03-24T11:30:00
description: "소수 p와 서로소인 a에 대해 a^(p-1) ≡ 1 (mod p)가 성립함을 두 가지 방법으로 증명하고, 모듈러 역원 계산과 RSA 복호화, 페르마 소수 판별법까지 응용을 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> 소수는 '나누어지지 않는다'는 단순한 성질을 갖지만, 모듈러 산술 위에서는 놀라운 주기성을 만들어낸다. a를 소수 p번 거듭제곱하면 반드시 a 자신으로 돌아온다 — 이 필연성이 RSA 암호를 가능하게 한다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>페르마의 소정리</strong>: p가 소수이고 gcd(a, p) = 1이면 a^(p−1) ≡ 1 (mod p)</li>
<li><strong>동치 형태</strong>: 모든 정수 a에 대해 a^p ≡ a (mod p)</li>
<li><strong>모듈러 역원</strong>: a^(−1) ≡ a^(p−2) (mod p)</li>
<li><strong>페르마 소수 판별법</strong>: a^(n−1) ≢ 1 (mod n)이면 n은 합성수</li>
<li><strong>한계</strong>: Carmichael 수 — 합성수이지만 모든 a에 대해 테스트를 통과하는 예외</li>
</ul>
</div>

## 정리의 두 형태

**형태 1** (기본형): $p$가 소수이고 $\gcd(a, p) = 1$이면,

$$
a^{p-1} \equiv 1 \pmod{p}
$$

**형태 2** (일반형): $p$가 소수이면 모든 정수 $a$에 대해,

$$
a^p \equiv a \pmod{p}
$$

두 형태는 동치이다. 형태 1에서 양변에 $a$를 곱하면 형태 2가 나오고, 형태 2에서 $p \nmid a$일 때 $a$로 나누면 형태 1이 복원된다. $p \mid a$인 경우 형태 2는 $0 \equiv 0 \pmod{p}$으로 자명하다.

## 증명 1 — 오일러 정리의 특수화

소수 $p$에 대해 $\phi(p) = p - 1$이다 ($1$부터 $p-1$까지 모두 $p$와 서로소).

오일러 정리 $a^{\phi(m)} \equiv 1 \pmod{m}$에 $m = p$를 대입하면 즉시 얻어진다.

## 증명 2 — 곱셈군 이중 치환

$\gcd(a, p) = 1$일 때, 집합 $S = \{1, 2, \ldots, p-1\}$을 고려한다.

$S$의 각 원소에 $a$를 곱한 집합 $aS = \{a, 2a, \ldots, (p-1)a\}$를 $\bmod\ p$로 환산하면:

- 각 $ia \bmod p$는 $0$이 아니다 ($\gcd(a, p) = 1$이고 $1 \leq i \leq p-1$이므로)
- $ia \not\equiv ja \pmod{p}$ ($i \neq j$일 때) — $a$가 역원을 가지므로 소거 가능

따라서 $aS \bmod p$의 원소들은 $\{1, 2, \ldots, p-1\}$의 재배열이다. 두 집합의 모든 원소를 곱하면,

$$
a \cdot 2a \cdot 3a \cdots (p-1)a \equiv 1 \cdot 2 \cdot 3 \cdots (p-1) \pmod{p}
$$

$$
a^{p-1} \cdot (p-1)! \equiv (p-1)! \pmod{p}
$$

$\gcd((p-1)!, p) = 1$이므로 양변에서 $(p-1)!$을 소거하면,

$$
a^{p-1} \equiv 1 \pmod{p}
$$

## 예시

![페르마의 소정리 — p=7에서 a^k mod 7 순환표](/images/fermat/cycle-table.svg)

$p = 7$에서 $\mathbb{Z}_7^* = \{1,2,3,4,5,6\}$의 각 원소는 고유한 순환 주기를 갖지만, $k = p - 1 = 6$에서 반드시 $1$로 수렴한다.

몇 가지 직접 계산:

$$
2^6 = 64 = 9 \times 7 + 1 \implies 2^6 \equiv 1 \pmod{7}
$$

$$
3^{10} \equiv 1 \pmod{11} \quad (p = 11,\ p-1 = 10)
$$

$$
5^{12} \equiv 1 \pmod{13} \quad (p = 13,\ p-1 = 12)
$$

## 응용 1 — 모듈러 역원

$\gcd(a, p) = 1$이면 $a^{p-1} \equiv 1$에서,

$$
a \cdot a^{p-2} \equiv 1 \pmod{p}
$$

따라서 $a$의 모듈러 역원은 $a^{-1} \equiv a^{p-2} \pmod{p}$이다.

확장 유클리드 알고리즘 없이도 빠른 모듈러 지수연산(Fast Exponentiation)만으로 역원을 구할 수 있다. 예를 들어 $3^{-1} \pmod{7} = 3^5 \bmod 7 = 243 \bmod 7 = 5$. 검증: $3 \times 5 = 15 \equiv 1 \pmod{7}$ ✓

## 응용 2 — 페르마 소수 판별법 (Fermat Primality Test)

$n$이 소수이면 $a^{n-1} \equiv 1 \pmod{n}$이 성립한다. 대우명제: **이 합동이 성립하지 않으면 $n$은 합성수** 이다.

**절차**: 랜덤하게 $a$ ($1 < a < n$)를 선택해 $a^{n-1} \bmod n$을 계산한다.
- $a^{n-1} \not\equiv 1$ → $n$은 합성수 (확정)
- $a^{n-1} \equiv 1$ → $n$이 소수일 가능성이 높음 (확정 아님)

여러 $a$에 대해 반복할수록 소수 판정의 신뢰도가 높아진다.

## 한계 — Carmichael 수

합성수임에도 **모든** $\gcd(a, n) = 1$인 $a$에 대해 $a^{n-1} \equiv 1 \pmod{n}$을 만족하는 수가 존재한다. 이를 **Carmichael 수(카마이클 수)** 라 한다.

가장 작은 예: $n = 561 = 3 \times 11 \times 17$

$$
a^{560} \equiv 1 \pmod{561} \quad \text{for all } \gcd(a, 561) = 1
$$

Carmichael 수 때문에 페르마 테스트 단독으로는 소수를 완전히 판별할 수 없다. 실용적인 소수 판별에는 **밀러-라빈 테스트(Miller-Rabin)** 를 사용한다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>a^(p-1) ≡ 1 (mod p)는 오일러 정리의 특수화이자, 집합 {1,...,p-1}이 곱셈에 대한 군(group)임을 반영한다.</li>
<li>모듈러 역원 a^(−1) ≡ a^(p−2)는 확장 유클리드 없이 지수연산만으로 역원을 구하는 실용적 공식이다.</li>
<li>페르마 소수 판별법은 확률적 테스트다 — Carmichael 수라는 반례가 존재하므로 단독으로 완전한 증명이 되지 않는다.</li>
<li>RSA에서 복호화 정확성(m^(de) ≡ m (mod n))은 페르마의 소정리(혹은 오일러 정리)에 직접 의존한다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Chinese Remainder Theorem — 중국인의 나머지 정리</strong> — 서로소인 여러 모듈러스의 연립 합동식이 항상 유일한 해를 가짐을 증명하고, RSA-CRT 속도 최적화까지 다룬다.</p>
</div>
