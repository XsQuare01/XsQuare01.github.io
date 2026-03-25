---
title: "RSA — 공개키 암호의 수학적 구조"
date: 2026-03-25T10:00:00
description: "RSA의 키 생성, 암복호화, 복호화 정확성 증명(오일러·페르마·CRT), 소인수분해 보안 근거, Square-and-Multiply 고속 지수연산까지 — 공개키 암호의 수학 전체를 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> Division Theorem, GCD, Modular Arithmetic, Euler 정리, Fermat 정리, CRT — 지금까지 쌓아온 정수론의 모든 도구가 RSA 하나를 위해 수렴한다. 큰 소수 두 개의 곱을 되돌리는 것이 어렵다는 단 하나의 사실 위에, 전 세계 인터넷 암호화가 서있다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>RSA 키</strong>: n = pq (공개), e (공개 지수), d (개인 지수), ed ≡ 1 (mod φ(n))</li>
<li><strong>암복호화</strong>: C = m^e mod n → m = C^d mod n = m^(ed) mod n</li>
<li><strong>복호화 정확성</strong>: m^(ed) ≡ m (mod n) — gcd(m,n)=1이면 오일러 정리, 아니면 페르마+CRT</li>
<li><strong>보안 근거</strong>: n = pq 소인수분해 → NP ∩ co-NP, 현실적으로 불가능</li>
<li><strong>고속 지수연산</strong>: Square-and-Multiply — O(e) → O(log e)</li>
</ul>
</div>

## 대칭키 vs 공개키 암호

**대칭키(Secret Key) 시스템**: 송신자와 수신자가 동일한 키 $k$를 공유한다. 두 사람만 알면 되지만, $N$명이 통신하려면 $\binom{N}{2}$개의 키가 필요하고 키 배포 자체가 문제가 된다.

**공개키(Public Key) 시스템**: 암호화 키 $e$는 모두에게 공개하고, 복호화 키 $d$만 비밀로 유지한다. $N$명이 통신할 때 각자 키 쌍 하나만 있으면 된다. 단, 공개된 $e$로부터 $d$를 계산하는 것이 불가능해야 한다.

RSA는 대표적인 공개키 암호 시스템이다.

## RSA 설정

**키 생성:**

1. 큰 소수 $p$, $q$를 선택한다. ($p \neq q$)
2. $n = pq$ (공개, modulus)
3. $\phi(n) = \phi(pq) = (p-1)(q-1)$ (비공개)
4. $1 < e < \phi(n)$이고 $\gcd(e, \phi(n)) = 1$인 $e$ 선택 (공개 지수)
5. $ed \equiv 1 \pmod{\phi(n)}$인 $d$ 계산 (비공개 — 확장 유클리드 알고리즘)

**공개키**: $(n,\ e)$ · **개인키**: $(p,\ q,\ d,\ \phi(n))$

![RSA 구조 — 키 구성과 암복호화 흐름](/images/rsa/rsa-flow.svg)

**암호화**: 평문 $m$ ($0 \leq m < n$)에 대해

$$
C = m^e \bmod n
$$

**복호화**: 암호문 $C$에 대해

$$
m = C^d \bmod n
$$

## 왜 ed ≡ 1 (mod φ(n)) 인가

핵심은 지수 연산의 주기성이다.

오일러 정리에 의해 $\gcd(a, n) = 1$이면 $a^{\phi(n)} \equiv 1 \pmod{n}$이므로, 지수 연산의 관점에서 $\phi(n) \equiv 0$이다. 즉 지수는 $\bmod\ \phi(n)$으로 환산된다.

$$
a^i \cdot a^j \equiv a^{i+j} \equiv a^{(i+j) \bmod \phi(n)} \pmod{n}
$$

복호화가 원래 평문을 돌려주려면 $m^{ed} \equiv m^1 \pmod{n}$이어야 하므로, 지수 부분에서

$$
ed \equiv 1 \pmod{\phi(n)}
$$

이 조건이 필요하다.

## 복호화 정확성 증명 — m^(ed) ≡ m (mod n)

$ed = 1 + k\phi(n)$으로 쓰면 $m^{ed} = m \cdot (m^{\phi(n)})^k$이다.

### Case 1: gcd(m, n) = 1

오일러 정리에 의해 $m^{\phi(n)} \equiv 1 \pmod{n}$이므로,

$$
m^{ed} = m \cdot 1^k = m \pmod{n} \quad \checkmark
$$

### Case 2: gcd(m, n) = p (또는 q)

$n = pq$이고 $m < n$이므로 $\gcd(m, n)$은 $1$, $p$, $q$, $n$ 중 하나다. $m = 0$인 경우는 자명하고, $p$인 경우를 증명하면 $q$인 경우도 대칭이다.

$m = px$로 쓸 수 있다. CRT를 적용해 $\bmod\ p$와 $\bmod\ q$로 분리한다.

**mod p 검증**: $m \equiv 0 \pmod{p}$이므로

$$
m^{ed} \equiv 0^{ed} \equiv 0 \equiv m \pmod{p} \quad \checkmark
$$

**mod q 검증**: $m = px$이고 $p \neq q$ (둘 다 소수)이므로 $\gcd(m, q) = 1$. 페르마의 소정리에 의해 $m^{q-1} \equiv 1 \pmod{q}$. 이때

$$
ed \equiv 1 \pmod{(p-1)(q-1)} \implies ed = 1 + k(p-1)(q-1)
$$

$(q-1)$이 $(p-1)(q-1)$을 나누므로,

$$
ed \equiv 1 + k(p-1)(q-1) \equiv 1 \pmod{q-1}
$$

따라서

$$
m^{ed} \equiv m^1 \equiv m \pmod{q} \quad \checkmark
$$

**CRT로 결합**: $m^{ed} \equiv m \pmod{p}$이고 $m^{ed} \equiv m \pmod{q}$이며 $\gcd(p,q)=1$이므로,

$$
m^{ed} \equiv m \pmod{n} \quad \checkmark
$$

## 보안 근거 — 소인수분해 문제

$d$를 복원하려면 $ed \equiv 1 \pmod{\phi(n)}$을 풀어야 한다. 이를 위해서는 $\phi(n) = (p-1)(q-1)$이 필요하다.

$\phi(n)$을 $n$으로부터 구하는 것은 $n$을 소인수분해하는 것과 동등하다. $y = \phi(n) = pq - p - q + 1$을 알면,

$$
n - y + 1 = p + q, \quad n = pq
$$

$p + q$와 $pq$를 알면 $p$, $q$를 이차방정식으로 구할 수 있다. 따라서 $\phi(n)$을 아는 것과 $n$을 소인수분해하는 것은 동치이다.

소인수분해 문제는 **NP ∩ co-NP**에 속하며, 현재까지 다항식 시간 알고리즘이 알려져 있지 않다. RSA의 보안은 이 어려움에 의존한다.

따라서 다음을 공개하고 나머지를 숨긴다.

- **공개**: $n$, $e$
- **비공개**: $p$, $q$, $d$, $\phi(n)$

주의: RSA를 깨는 데 반드시 $d$를 구해야 하는 것은 아니다. $C \to m$을 복원하는 효율적 방법이 있다면 $p$, $q$도 복원 가능함이 알려져 있다 (동치 관계).

## 모듈러 지수연산 (Square-and-Multiply)

$C = m^e \bmod n$에서 $e$는 수천 비트에 달한다 (2048비트 RSA에서 $e$는 65537이 관례). $m$을 $e$번 곱하는 직접 계산은 $O(e)$ 연산이 필요하다 — 현실적으로 불가능하다.

**핵심 아이디어**: $e$를 이진수로 표현하면 $O(\log e)$번의 곱셈으로 계산 가능하다.

알고리즘 (MSB → LSB):

1. 최상위 비트부터 시작해 `result = m`으로 초기화
2. 이후 각 비트에 대해:
   - **항상**: `result = result² mod n` (제곱)
   - **비트 = 1이면 추가**: `result = result × m mod n` (곱셈)

![Square-and-Multiply — 17^23 단계별 계산](/images/rsa/modular-exp.svg)

예시 $17^{23}$에서 $23 = 10111_2$: 총 **7회** 곱셈 (4회 제곱 + 3회 ×m). 직접 계산의 22회 대비 3배 이상 절약.

$e$가 2000비트이면 직접 계산은 $2^{2000}$번이지만 Square-and-Multiply는 약 $2 \times 2000 = 4000$번으로 충분하다. 각 단계에서 `mod n`을 함께 적용하므로 수의 크기도 $n$으로 제한된다.

## 적절한 p, q 선택

$p$와 $q$를 아무렇게나 선택하면 공격에 취약해진다.

**$|p - q|$가 작을 때**: $p \approx q \approx \sqrt{n}$이면, $\sqrt{n}$ 근처 값들을 검색해 $p$, $q$를 쉽게 찾을 수 있다 (Fermat 인수분해 공격).

**$p - 1$이 작은 소인수만 갖는 경우**: Pohlig-Hellman 공격에 취약하다.

현재 권장 기준:
- $p$, $q$: 각 1024비트 이상 → $n$: 2048비트 이상
- $|p - q|$: 충분히 클 것
- $p - 1$, $q - 1$: 큰 소인수를 포함할 것

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>RSA는 ed ≡ 1 (mod φ(n))을 이용해 m^(ed) ≡ m (mod n)을 성립시킨다 — 오일러 정리가 핵심이다.</li>
<li>gcd(m, n) ≠ 1인 예외 케이스도 mod p와 mod q를 분리한 페르마+CRT 접근으로 성립함을 증명할 수 있다.</li>
<li>보안은 n = pq 소인수분해의 어려움에만 의존한다. 현재 다항식 시간 소인수분해 알고리즘은 알려져 있지 않다.</li>
<li>Square-and-Multiply로 O(e) → O(log e) 지수연산이 가능하다. 2000비트 지수도 약 4000번 곱셈으로 처리된다.</li>
</ul>
</div>
