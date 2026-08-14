---
title: "RSA — 공개키 암호의 수학적 구조"
date: 2026-03-25T10:00:00
description: "RSA의 키 생성, 암복호화, 복호화 정확성 증명(오일러·페르마·CRT), 소인수분해 보안 근거, Square-and-Multiply 고속 지수연산까지 — 공개키 암호의 수학 전체를 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
difficulty: 고급
---

> Division Theorem, GCD, Modular Arithmetic, Euler 정리, Fermat 정리, CRT — 지금까지 쌓아온 정수론의 모든 도구가 RSA 하나를 위해 수렴한다. 큰 소수 두 개의 곱을 되돌리기 어렵다는 사실 하나가 최초의 실용적 공개키 암호를 낳았고, 40여 년이 지난 지금도 웹의 인증서와 전자서명을 떠받치고 있다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li><strong>RSA 키</strong>: $n = pq$ (공개), $e$ (공개 지수), $d$ (개인 지수), $ed \equiv 1 \pmod{\varphi(n)}$</li>
<li><strong>암복호화</strong>: $C = m^e \bmod n$ → $m = C^d \bmod n = m^{ed} \bmod n$</li>
<li><strong>복호화 정확성</strong>: $m^{ed} \equiv m \pmod{n}$ — $\gcd(m,n)=1$이면 오일러 정리, 아니면 페르마+CRT</li>
<li><strong>보안 근거</strong>: $\phi(n)$과 $d$를 구하는 것은 소인수분해와 동치, RSA 문제 자체의 어려움은 미해결</li>
<li><strong>고속 지수연산</strong>: Square-and-Multiply — 지수의 값 $k$에 비례하던 비용을 자릿수 $\log k$에 비례하게</li>
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

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>RSA 복호화가 정확히 원래 메시지를 돌려주는 이유는 "거듭제곱의 주기성" 덕분이다. $e$번 거듭제곱해서 암호화하고, $d$번 거듭제곱해서 복호화하면, $ed$번 거듭제곱한 셈인데 — 오일러 정리에 의해 이것이 정확히 1번 거듭제곱한 것과 같아진다. 즉 원래 메시지로 돌아온다.</p>
</div>

## 보안 근거 — 소인수분해 문제

$d$를 복원하려면 $ed \equiv 1 \pmod{\phi(n)}$을 풀어야 한다. 이를 위해서는 $\phi(n) = (p-1)(q-1)$이 필요하다.

$\phi(n)$을 $n$으로부터 구하는 것은 $n$을 소인수분해하는 것과 동등하다. $y = \phi(n) = pq - p - q + 1$을 알면,

$$
n - y + 1 = p + q, \quad n = pq
$$

$p + q$와 $pq$를 알면 $p$, $q$를 이차방정식으로 구할 수 있다. 따라서 $\phi(n)$을 아는 것과 $n$을 소인수분해하는 것은 동치이다.

소인수분해의 **판정 버전**("$n$에 $k$보다 작은 소인수가 있는가")은 **NP ∩ co-NP** 에 속한다. yes에 대한 증거는 그런 소인수 하나이고, no에 대한 증거는 모든 소인수가 $k$ 이상임을 보이는 완전한 소인수분해다. 어느 쪽이든 다항식 시간에 검증된다. 그리고 현재까지 다항식 시간 알고리즘은 알려져 있지 않다.

따라서 다음을 공개하고 나머지를 숨긴다.

- **공개**: $n$, $e$
- **비공개**: $p$, $q$, $d$, $\phi(n)$

<div class="callout">
<div class="callout-title">"인수분해와 동치"라는 말이 어디까지 참인가</div>

RSA를 깨는 길이 하나가 아니므로, 무엇이 인수분해와 동치인지를 나눠 봐야 한다.

| 할 수 있게 되는 일 | 인수분해와의 관계 |
|---|---|
| $\phi(n)$을 구한다 | **동치.** 위에서 이차방정식으로 보였다 |
| $d$를 구한다 | **동치.** $(n, e, d)$에서 $n$을 인수분해하는 알고리즘이 알려져 있다 |
| 주어진 $C$에서 $m$을 복원한다 | **미해결.** 인수분해할 수 있으면 복원할 수 있지만, 그 역은 알려져 있지 않다 |

세 번째 줄이 핵심이다. "$C$에서 $m$을 복원하라"는 문제를 **RSA 문제**라 부르는데, 이것이 인수분해만큼 어렵다는 것은 **증명된 적이 없다.** 오히려 지수 $e$가 작은 경우에는 인수분해를 RSA 문제로 되돌리는 특정 형태의 환원이 존재한다면 그 자체로 효율적인 인수분해 알고리즘이 나온다는 결과가 있어, 그런 환원을 찾기 어려우리라는 쪽에 무게가 실린다.

그래서 정확히 말하면 RSA의 안전성은 인수분해의 어려움이 아니라 **RSA 문제의 어려움**이라는 별도의 가정 위에 선다. 인수분해가 어렵다는 것은 그 가정의 **필요조건**이다. 인수분해가 뚫리면 RSA도 뚫리지만, 인수분해가 어렵다고 해서 RSA 문제가 어렵다는 보장은 아직 없다.

</div>

## 모듈러 지수연산 (Square-and-Multiply)

암호화 $C = m^e \bmod n$과 복호화 $m = C^d \bmod n$은 지수만 다를 뿐 같은 연산이다. 그래서 일반화해 **밑 $a$를 지수 $k$번 거듭제곱하는 $a^k \bmod n$** 을 어떻게 계산할지 본다.

지수의 크기는 두 방향에서 크게 다르다. $e$는 관례상 **65537** $= 2^{16}+1$을 써서 17비트에 불과하지만, $d$는 2048비트 RSA에서 약 2048비트에 달한다. 비용이 문제가 되는 쪽은 복호화다.

$a$를 $k$번 곱하는 직접 계산은 곱셈이 $k-1$번 필요하다. 여기서 $k$는 **지수의 값**이지 비트 수가 아니다. $d$가 2048비트라면 $k \approx 2^{2048}$이므로 우주가 끝날 때까지 끝나지 않는다.

**핵심 아이디어**: $k$를 이진수로 펼치면 $O(\log k)$번의 곱셈으로 끝난다. $\log k$는 곧 **지수의 비트 수**이므로, 지수의 값에 비례하던 비용이 자릿수에 비례하는 비용으로 바뀐다.

알고리즘 (MSB → LSB):

1. 지수 $k$의 최상위 비트부터 시작해 `result = a`로 초기화
2. 이후 각 비트에 대해:
   - **항상**: `result = result² mod n` (제곱)
   - **비트 = 1이면 추가**: `result = result × a mod n` (곱셈)

![Square-and-Multiply — 17^23 단계별 계산](/images/rsa/modular-exp.svg)

예시 $17^{23}$에서 $23 = 10111_2$: 총 **7회** 곱셈 (4회 제곱 + 3회 $\times a$). 직접 계산의 22회 대비 3배 이상 절약.

복호화 지수 $d$가 2048비트라면 직접 계산은 약 $2^{2048}$번이지만, Square-and-Multiply는 제곱 약 2048번과 곱셈 약 1024번($1$인 비트가 절반쯤이므로), 즉 3000여 번으로 충분하다. 각 단계에서 `mod n`을 함께 적용하므로 수의 크기도 $n$ 미만으로 유지된다.

## 적절한 p, q 선택

$p$와 $q$를 아무렇게나 선택하면 공격에 취약해진다.

**$|p - q|$가 작을 때**: $p \approx q \approx \sqrt{n}$이면, $\sqrt{n}$ 근처 값들을 검색해 $p$, $q$를 쉽게 찾을 수 있다 (Fermat 인수분해 공격).

**$p - 1$이 작은 소인수만 갖는 경우**: **Pollard의 $p-1$ 알고리즘**에 취약하다. $p-1$의 소인수가 모두 어떤 한계 $B$ 이하라면 $p-1$은 $K = \text{lcm}(1, 2, \ldots, B)$를 나눈다. 그러면 페르마 소정리로 $a^{K} \equiv 1 \pmod p$이므로 $p \mid a^K - 1$이고, $\gcd(a^K - 1,\ n)$을 계산하면 $p$가 그대로 떨어져 나온다. $q-1$에 대해서도 같다.

현재 권장 기준:
- $p$, $q$: 각 1024비트 이상 → $n$: 2048비트 이상
- $|p - q|$: 충분히 클 것
- $p - 1$, $q - 1$: 큰 소인수를 포함할 것

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>RSA는 $ed \equiv 1 \pmod{\varphi(n)}$을 이용해 $m^{ed} \equiv m \pmod{n}$을 성립시킨다 — 오일러 정리가 핵심이다.</li>
<li>$\gcd(m, n) \neq 1$인 예외 케이스도 $\bmod p$와 $\bmod q$를 분리한 페르마+CRT 접근으로 성립함을 증명할 수 있다.</li>
<li>$\phi(n)$을 구하는 것과 $d$를 구하는 것은 각각 소인수분해와 <strong>동치</strong>다. 다만 "$C$에서 $m$을 복원한다"가 소인수분해만큼 어려운지는 <strong>미해결</strong>이다. 인수분해의 어려움은 RSA 안전성의 필요조건이지 충분조건이 아니다.</li>
<li>Square-and-Multiply로 지수연산이 $O(k)$에서 $O(\log k)$로 줄어든다. 여기서 $k$는 지수의 <strong>값</strong>이고 $\log k$는 <strong>비트 수</strong>다. 2048비트 지수도 3000여 번 연산으로 처리된다.</li>
</ul>
</div>

## 요약

RSA는 세 가지 수학적 사실 위에 서있다.

첫째, $ed \equiv 1 \pmod{\phi(n)}$이라는 조건 하에 $m^{ed} \equiv m \pmod{n}$이 성립한다 — 오일러 정리의 직접적인 귀결이다. 둘째, $\phi(n)$을 알려면 $n = pq$를 소인수분해해야 하므로, $n$과 $e$만 공개해도 $d$는 감추어진다. 셋째, Square-and-Multiply로 수천 비트 지수연산도 $O(\log e)$ 만에 처리할 수 있어 실용적이다.

남은 질문은 하나다: **실제로 큰 소수를 어떻게 찾는가?** RSA 키 생성에서 1024비트 이상의 소수 두 개가 필요한데, 이 크기에서 소수인지 판별하는 직접적인 방법은 현실적으로 불가능하다. 다음 글 [Find Prime](/blog/find-prime)에서 Fermat 테스트와 확률적 소수 탐색 알고리즘을 다룬다.
