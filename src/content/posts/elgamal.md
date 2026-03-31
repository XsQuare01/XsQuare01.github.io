---
title: "ElGamal — 이산 대수 기반 공개키 암호"
date: 2026-03-27T11:00:00
description: "RSA와 달리 이산 대수 문제(DLP)의 어려움에 기반한 ElGamal 암호화 — 키 생성, 암복호화, 정확성 증명, 확률적 암호화의 보안 이점까지 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> RSA가 소인수분해의 어려움 위에 서있다면, ElGamal은 이산 대수 문제(DLP) 위에 서있다. 두 시스템은 서로 다른 수학적 어려움을 활용하지만, 결정적 차이가 하나 있다 — ElGamal은 암호화할 때마다 다른 암호문을 생성한다. 이것이 단순한 특성을 넘어 의미론적 안전성(IND-CPA)의 핵심이 된다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>보안 근거</strong>: 이산 대수 문제 (DLP) — g^x mod p에서 x를 구하는 것은 지수적으로 어렵다</li>
<li><strong>키 생성</strong>: 비밀키 x, 공개키 h = g^x mod p</li>
<li><strong>암호화</strong>: 랜덤 k 선택 → 암호문 (A, B) = (g^k, m·h^k) mod p</li>
<li><strong>복호화</strong>: 공유 비밀 s = A^x, 평문 m = B·s⁻¹ mod p</li>
<li><strong>확률적 암호화</strong>: 같은 평문도 k가 달라지면 다른 암호문 → IND-CPA 만족</li>
</ul>
</div>

## RSA와의 차이: 왜 다른 어려움이 필요한가

RSA는 $n = pq$ 소인수분해의 어려움에 의존한다. 이 문제는 검증된 어려움이지만, 같은 평문을 항상 같은 암호문으로 변환한다는 **결정론적(deterministic)** 특성이 있다. 공격자가 후보 평문을 암호화해 비교하는 선택 평문 공격(CPA)에 취약하다.

ElGamal은 **이산 대수 문제(Discrete Logarithm Problem, DLP)** 라는 독립적인 어려움을 사용한다. 그리고 암호화 과정에 랜덤성을 도입해 동일한 평문도 매번 다른 암호문으로 변환된다.

## 이산 대수 문제 (DLP)

**소수 $p$, 생성원(generator) $g \in \mathbb{Z}_p^*$, 그리고 $h = g^x \bmod p$가 주어졌을 때, $x$를 구하여라.**

정방향 계산 $k \to g^k \bmod p$는 Square-and-Multiply로 $O(\log k)$에 가능하다. 반면 역방향 $g^k \bmod p \to k$를 구하는 알고리즘은 아직 다항식 시간으로 알려져 있지 않다. 가장 빠른 알고리즘(Number Field Sieve)조차 준지수 시간 $L[1/3]$이 필요하다.

![이산 대수 문제 — p=11, g=2에서 ℤ₁₁* 순환과 DLP](/images/elgamal/dlp-visualization.svg)

**생성원(Generator)**: 소수 $p$에 대해 $g \in \mathbb{Z}_p^*$가 **생성원** 이라는 것은 $g$의 거듭제곱이 $\mathbb{Z}_p^*$의 모든 원소를 순환한다는 의미다.

$$
\{g^0, g^1, g^2, \ldots, g^{p-2}\} = \mathbb{Z}_p^* \quad (\bmod\ p)
$$

$p = 11$, $g = 2$이면 $\{1, 2, 4, 8, 5, 10, 9, 7, 3, 6\} = \mathbb{Z}_{11}^*$으로 10개 원소 전부를 생성한다. 페르마의 소정리에 의해 $g^{p-1} \equiv 1 \pmod{p}$이므로, 지수는 주기 $p-1$로 순환한다.

## ElGamal 설정

**공개 파라미터**: 큰 소수 $p$, $\mathbb{Z}_p^*$의 생성원 $g$

**키 생성 (수신자 Alice)**:

1. 비밀키 $x$를 $1 \leq x \leq p-2$ 범위에서 무작위 선택
2. $h = g^x \bmod p$ 계산
3. **공개키**: $(p,\ g,\ h)$  ·  **개인키**: $x$

**암호화 (송신자 Bob)**:

1. 임시 비밀(ephemeral key) $k$를 $1 \leq k \leq p-2$ 범위에서 무작위 선택
2. $A = g^k \bmod p$
3. $B = m \cdot h^k \bmod p$
4. **암호문**: $(A,\ B)$

**복호화 (수신자 Alice)**:

1. 공유 비밀 $s = A^x \bmod p$ 계산
2. $s$의 모듈러 역원 $s^{-1} \bmod p$ 계산 (확장 유클리드 알고리즘)
3. **복원**: $m = B \cdot s^{-1} \bmod p$

![ElGamal 암복호화 흐름 — p=11, g=2 수치 예시](/images/elgamal/elgamal-flow.svg)

## 복호화 정확성 증명

왜 $B \cdot s^{-1}$이 $m$을 복원하는가.

$$
s = A^x = (g^k)^x = g^{kx} \pmod{p}
$$

$$
h^k = (g^x)^k = g^{xk} \pmod{p}
$$

따라서 $s = h^k$이다. $B$의 정의에 의해

$$
B \cdot s^{-1} = m \cdot h^k \cdot (h^k)^{-1} = m \pmod{p} \quad \checkmark
$$

핵심은 Alice와 Bob이 각자 독립적으로 **동일한 공유 비밀 $g^{kx} \bmod p$** 를 계산한다는 것이다.

- Bob: $h^k = (g^x)^k$  — Alice의 공개키 $h$와 자신의 임시 키 $k$ 사용
- Alice: $A^x = (g^k)^x$  — Bob이 보낸 $A$와 자신의 비밀키 $x$ 사용

이는 **Diffie-Hellman 키 교환** 의 직접적인 응용이다. ElGamal 암호화는 DH 키 교환에 메시지 마스킹($m \cdot h^k$)을 결합한 구조이다.

## 보안 근거: CDH 가정

ElGamal의 보안은 **계산적 Diffie-Hellman(CDH) 가정** 에 기반한다.

> $g$, $g^x$, $g^k$ 가 주어졌을 때, $g^{xk}$를 계산하는 다항식 시간 알고리즘이 존재하지 않는다.

공격자가 암호문 $(A, B) = (g^k, m \cdot h^k)$을 가로채더라도, 공유 비밀 $g^{xk}$를 계산하지 못하면 $m$을 복원할 수 없다. CDH를 풀려면 DLP를 풀어야 하므로, CDH $\leq$ DLP — CDH가 쉬우면 DLP도 쉽다. 따라서 DLP가 어려운 한 CDH도 어렵다고 가정한다.

## 확률적 암호화와 IND-CPA 안전성

ElGamal의 핵심 이점은 **확률적(randomized)** 암호화다.

같은 평문 $m$도 임시 키 $k$가 달라지면 완전히 다른 암호문이 생성된다.

![확률적 암호화 — ElGamal vs RSA 의미론적 안전성 비교](/images/elgamal/probabilistic-encryption.svg)

이 성질은 **IND-CPA(선택 평문 공격 하 식별 불가능성)** 안전성을 가능하게 한다.

- **RSA(교과서적)**: $m \to C$가 결정론적. 공격자가 두 후보 $m_0, m_1$을 직접 암호화해 도전 암호문 $C^*$와 비교 가능.
- **ElGamal**: $m \to (A, B)$가 확률적. 공격자가 $m$을 암호화해도 $k$가 달라 $C^*$와 일치하지 않음.

단, 암호문이 두 개의 군 원소 $(A, B)$로 구성되므로 평문 대비 **암호문 크기가 2배** 로 증가한다. RSA 대비 트레이드오프다.

<div class="callout">
<div class="callout-title">ElGamal vs RSA 비교</div>
<ul>
<li><strong>보안 근거</strong>: ElGamal — DLP (이산 대수),  RSA — 소인수분해</li>
<li><strong>암호화 유형</strong>: ElGamal — 확률적 (IND-CPA),  RSA — 결정론적 (교과서적)</li>
<li><strong>암호문 크기</strong>: ElGamal — 평문의 2배,  RSA — 평문과 동일</li>
<li><strong>랜덤 비트 사용</strong>: ElGamal — 매번 필요,  RSA — 불필요 (OAEP 적용 시 필요)</li>
</ul>
</div>

## 올바른 파라미터 선택

**소수 $p$ 크기**: DLP의 어려움은 $p$의 크기에 비례한다. 현재 권장은 2048비트 이상. $p-1$이 큰 소인수를 포함해야 한다 (Pohlig-Hellman 공격 방지).

**생성원 $g$ 선택**: $g$가 $\mathbb{Z}_p^*$ 전체를 생성해야 한다. $p-1$의 소인수 $q$에 대해 $g^{(p-1)/q} \not\equiv 1 \pmod{p}$를 확인한다.

**임시 키 $k$ 관리**: $k$는 암호화마다 독립적으로 새로 선택해야 한다. 같은 $k$를 두 번 사용하면 두 암호문 $B_1 = m_1 \cdot h^k$, $B_2 = m_2 \cdot h^k$에서 $B_1 / B_2 = m_1 / m_2$가 노출된다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>ElGamal은 DLP의 어려움에 기반한다. g^x를 알아도 x를 역산하는 다항식 알고리즘은 알려져 있지 않다.</li>
<li>복호화 정확성은 A^x = h^k = g^(kx)라는 공유 비밀의 동등성에서 비롯된다. Diffie-Hellman 키 교환의 직접 응용이다.</li>
<li>확률적 암호화 덕분에 동일 평문도 매번 다른 암호문을 생성한다 — IND-CPA 안전성의 핵심이다.</li>
<li>임시 키 k를 재사용하면 즉시 평문 비율이 노출된다. k는 반드시 매번 새로 생성해야 한다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Digital Signature — 전자 서명의 수학적 구조</strong> — RSA·ElGamal 서명의 생성과 검증, 인증기관(CA)의 역할, 암호화 해시와 결합한 최종 프로토콜까지 디지털 서명의 전체 그림을 다룬다.</p>
</div>
