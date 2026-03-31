---
title: "Digital Signature — 전자 서명의 수학적 구조"
date: 2026-03-31T10:00:00
description: "RSA·ElGamal 전자 서명의 생성과 검증, 인증기관(CA)의 역할, 암호화 해시(SHA)와 Birthday Paradox, 그리고 AES+RSA+SHA를 결합한 최종 프로토콜까지 — 디지털 서명의 전체 그림을 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> RSA로 메시지를 암호화하면 기밀성은 확보된다. 하지만 Bob은 여전히 모른다 — 이 메시지가 정말 Alice에게서 왔는가? 전자 서명은 그 질문에 답한다. 비밀키 없이는 위조할 수 없고, 공개키만으로 누구나 검증할 수 있는 수학적 사인이다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>RSA 서명</strong>: s = m^d mod n, 검증: s^e = m — 비밀키로 서명, 공개키로 검증</li>
<li><strong>ElGamal 서명</strong>: r = g^k mod p, s = (m − ar)k⁻¹ mod (p−1) — DLP 기반</li>
<li><strong>인증기관(CA)</strong>: 공개키의 신뢰를 보증하는 신뢰 앵커</li>
<li><strong>암호화 해시</strong>: SHA로 m → h(고정 크기) — 서명 크기와 속도 문제 해결</li>
<li><strong>최종 프로토콜</strong>: AES(기밀성) + RSA(키 전달·서명) + SHA(무결성) 통합</li>
</ul>
</div>

## 왜 서명이 필요한가

대칭키 시스템에서는 Alice와 Bob만이 키 $k$를 공유한다. Bob이 $k$로 암호문을 복호화했다면, 그 메시지는 $k$를 아는 Alice가 보냈다고 추론할 수 있다.

하지만 RSA 같은 공개키 시스템에서는 누구나 공개키 $(n, e)$로 암호화할 수 있다. Bob은 암호문을 복호화할 수 있지만, **누가 보냈는지는 알 수 없다**.

전자 서명은 이 문제를 해결한다. 현실의 서명처럼 두 가지 조건을 만족해야 한다.

- **본인만 서명할 수 있다** — 비밀키 없이는 위조 불가
- **누구나 검증할 수 있다** — 공개키로 누구나 확인

디지털 환경에서는 한 가지 조건이 추가된다.

- **Not Convertible** — 서명은 특정 문서에 묶여야 한다. 복사·붙여넣기로 다른 문서에 재사용할 수 없어야 한다.

## RSA 서명

RSA의 암호화($m^e$)와 복호화($m^d$)는 서로 대칭이다. 즉 어느 방향으로 적용해도 원문이 복원된다.

$$
(m^d)^e \equiv m^{de} \equiv m \pmod{n}
$$

이 대칭성을 서명에 활용한다.

**서명 생성** (Alice, 비밀키 $d$ 사용):

$$
s = m^d \bmod n
$$

**서명 검증** (Bob, Alice의 공개키 $e$ 사용):

$$
s^e \bmod n \stackrel{?}{=} m
$$

![RSA 전자 서명 — 서명 생성과 검증 흐름](/images/signature/rsa-signature.svg)

복호화 과정이 서명 생성, 암호화 과정이 서명 검증이 된다. 비밀키 $d$를 가진 Alice만이 유효한 $s$를 만들 수 있고, 공개키 $e$는 공개되어 있으므로 누구나 검증할 수 있다.

## 인증기관 (Certificate Authority)

RSA 서명에는 한 가지 취약점이 있다. Bob이 사용하는 공개키 $e$가 정말 Alice의 것인가?

공격자 Eve가 자신의 공개키 $e'$를 Alice의 것인 척 배포하면, Bob은 Eve의 서명을 Alice의 서명으로 착각할 수 있다.

이를 해결하는 것이 **인증기관(CA, Certificate Authority)**이다.

1. Alice가 자신의 공개키와 신원 정보를 CA에 제출한다.
2. CA는 이를 검토한 뒤 **(공개키 + 신원 정보)**에 CA 자신의 서명을 붙인다 → **인증서(Certificate)**
3. Bob은 CA의 서명을 검증해 Alice의 공개키가 진짜임을 확인한다.

CA는 "누구나 신뢰하는 기관"이라는 전제 위에 작동한다. 공인인증서와 HTTPS 인증서가 이 구조로 동작한다.

## ElGamal 서명

RSA가 소인수분해 어려움에 기반한다면, ElGamal 서명은 [이산 대수 문제(DLP)](/blog/elgamal)에 기반한다.

**설정**: 공개 파라미터 $p$, $g$. Alice의 비밀키 $a$, 공개키 $y = g^a \bmod p$.

**서명 생성** (Alice, 비밀키 $a$ 사용):

1. 임의의 $k$를 선택한다 ($\gcd(k, p-1) = 1$)
2. $r = g^k \bmod p$
3. $s = (m - ar) \cdot k^{-1} \bmod (p-1)$

서명: $(r, s)$

**서명 검증** (Bob, Alice의 공개키 $y$ 사용):

$$
g^m \equiv y^r \cdot r^s \pmod{p}
$$

**검증이 성립하는 이유**:

$$
y^r \cdot r^s = (g^a)^r \cdot (g^k)^s = g^{ar} \cdot g^{k \cdot (m-ar)k^{-1}} = g^{ar} \cdot g^{m-ar} = g^m \pmod{p}
$$

$k$와 $k^{-1}$이 상쇄되고, $a$는 공개키 $y = g^a$ 형태로만 검증에 사용된다 — 비밀키 $a$ 없이는 서명 생성 불가능, 공개키 $y$만으로 검증 가능.

ElGamal 서명을 표준화한 것이 **DSS(Digital Signature Standard)**이다.

## 서명 크기 문제: 암호화 해시

RSA 서명의 문제는 크기이다. $m$이 100MB라면 서명 $s = m^d \bmod n$ 역시 비슷한 크기가 된다. 목적(누가 보냈는가 확인)에 비해 과도하게 크다.

해결책은 **암호화 해시 함수(Cryptographic Hash Function)**다.

$$
h = \text{SHA}(m)
$$

SHA는 임의 길이의 메시지 $m$을 고정 크기(SHA-256이면 256비트)의 해시값 $h$로 변환한다. 서명은 $m$ 대신 $h$에 생성한다.

$$
s = h^d \bmod n = \text{SHA}(m)^d \bmod n
$$

![Hash + Signature — 크기 문제 해결과 Not Convertible 보장](/images/signature/hash-signature.svg)

해시 함수는 두 가지 성질을 만족해야 한다.

**일방향성(One-way)**: $h$에서 $m$을 역산할 수 없다. 서명 위조를 위해 특정 해시값을 갖는 메시지를 찾는 것이 불가능해야 한다.

**충돌 저항성(Collision Resistance)**: $\text{SHA}(m_1) = \text{SHA}(m_2)$인 두 메시지 $m_1 \neq m_2$를 찾는 것이 불가능해야 한다. 이를 충족하면 Not Convertible이 자동으로 보장된다 — $m$이 다르면 $h$도 달라지므로, 서명 $s$를 다른 문서에 재사용할 수 없다.

## Birthday Paradox와 해시 길이

해시가 $n$비트라면, 특정 해시값 $h$와 충돌하는 메시지를 찾으려면 평균 $2^n$번의 시도가 필요하다.

그런데 **특정 값이 아닌 임의의 충돌 쌍** $m_1, m_2$를 찾는 것은 훨씬 쉽다. 생일 역설(Birthday Paradox)에 의해 약 $2^{n/2}$번이면 충분하다.

> 365일 중 생일이 같은 두 사람을 찾으려면 23명이면 충분하다 ($\approx \sqrt{365}$). 특정인과 생일이 같으려면 253명이 필요하다.

따라서 SHA-256(256비트)의 충돌 저항성은 사실상 $2^{128}$이다. 이를 감안해 SHA-256 이상을 사용하는 것이 현재 권장 기준이다.

## 최종 프로토콜: AES + RSA + SHA

실제 보안 통신은 세 알고리즘을 역할에 따라 조합한다.

**설정**:
- Alice: RSA 키쌍 $(e_a, d_a)$
- Bob: RSA 키쌍 $(e_b, d_b)$
- 대칭키 $k$: Alice가 임의 생성

![AES + RSA + SHA 최종 프로토콜 — 기밀성·무결성·인증 통합](/images/signature/full-protocol.svg)

**Alice → Bob 전송**:

1. 임의의 대칭키 $k$ 생성
2. $C = \text{AES}_k(m)$ — 평문을 AES로 암호화 (속도)
3. $k' = k^{e_b} \bmod n$ — 대칭키를 Bob의 공개키로 암호화
4. $h = \text{SHA}(m)$, $s = h^{d_a} \bmod n$ — 해시에 Alice의 서명 생성
5. 전송 패킷: $(C,\ k',\ s)$

**Bob의 복호화 및 검증**:

1. $k = k'^{d_b} \bmod n$ — RSA로 대칭키 복원
2. $m = \text{AES}_k^{-1}(C)$ — AES로 평문 복원
3. $h = s^{e_a} \bmod n$ — Alice의 공개키로 서명 복원
4. $h' = \text{SHA}(m)$, $h' \stackrel{?}{=} h$ — 직접 해시와 비교

각 구성 요소의 역할:

| 알고리즘 | 역할 | 이유 |
|----------|------|------|
| AES | 메시지 암호화 | 빠르고 대용량 처리 가능 |
| RSA | 키 전달 + 서명 | AES 키를 안전하게 공유, 신원 인증 |
| SHA | 해시 | 서명 크기 고정, Not Convertible 보장 |

이 구조가 TLS(HTTPS), PGP, 이메일 암호화 등 현대 보안 통신의 기반이다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>RSA 서명은 복호화 키(d)로 서명하고 암호화 키(e)로 검증한다. ed ≡ 1 (mod φ(n))에서 m^(ed) = m이 성립하기 때문이다.</li>
<li>ElGamal 서명은 DLP에 기반하며, g^m ≡ y^r · r^s (mod p)로 검증한다. 비밀키 a 없이는 유효한 (r, s)를 만들 수 없다.</li>
<li>SHA로 m → h(고정 크기)를 만들어 서명하면 서명 크기가 메시지 크기와 무관해진다. 충돌 저항성이 Not Convertible을 보장한다.</li>
<li>Birthday Paradox에 의해 n비트 해시의 실질적 충돌 저항성은 2^(n/2)이다. SHA-256의 실질 안전성은 2^128이다.</li>
<li>현대 보안 통신은 AES(기밀성) + RSA(키 전달·인증) + SHA(무결성)를 결합한다. 이것이 TLS·PGP의 구조다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Cryptographic Hashing — 암호화 해시 함수</strong> — SHA의 내부 구조(Merkle-Damgård), 일방향성·충돌 저항성의 수학, Birthday Paradox가 해시 길이에 미치는 영향, 그리고 MD5/SHA-1이 왜 더 이상 안전하지 않은지까지 다룬다.</p>
</div>
