---
title: "Diffie-Hellman — 공개 채널 위의 비밀 키 교환"
date: 2026-03-28T10:00:00
description: "ElGamal의 수학적 기반이 된 Diffie-Hellman 키 교환 — 프로토콜 구조, 정확성 증명, CDH/DDH 가정, 중간자 공격과 인증 문제, 그리고 ElGamal·TLS로의 확장까지 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
difficulty: 중급
---

> ElGamal에서 복호화가 성립하는 핵심은 Alice와 Bob이 독립적으로 동일한 공유 비밀 $g^{kx}$를 계산한다는 것이었다. 이 아이디어의 원형이 바로 Diffie-Hellman 키 교환이다. 1976년, 공개 채널만으로 비밀 키를 공유할 수 있다는 혁명적 발상이 공개키 암호학 전체의 문을 열었다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li><strong>핵심 문제</strong>: 도청 가능한 공개 채널에서 비밀 키를 공유하는 방법</li>
<li><strong>프로토콜</strong>: Alice는 $g^a$, Bob은 $g^b$를 교환 → 공유 비밀 $g^{ab}$</li>
<li><strong>보안 근거</strong>: CDH 가정 — $g^a$, $g^b$로부터 $g^{ab}$를 계산하는 것은 어렵다</li>
<li><strong>한계</strong>: 인증 없음 → 중간자 공격(MITM)에 취약</li>
<li><strong>확장</strong>: DH + 메시지 마스킹 = ElGamal 암호화</li>
</ul>
</div>

## 키 교환 문제: 왜 어려운가

대칭키 암호(AES 등)는 빠르고 효율적이지만, 근본적인 문제가 있다. 양쪽이 **같은 비밀 키**를 미리 공유해야 한다. 그런데 도청자가 있는 채널에서 비밀 키를 어떻게 전달하는가?

직관적으로 불가능해 보인다. 채널 위의 모든 메시지를 도청자가 볼 수 있다면, 비밀 키를 그대로 보내는 순간 도청자도 그 키를 갖는다. Whitfield Diffie와 Martin Hellman이 1976년에 보인 것은, **일방향 함수(one-way function)** 를 활용하면 공개 메시지만으로 비밀을 공유할 수 있다는 것이었다.

핵심 통찰은 곱셈의 순서가 결과에 영향을 주지 않는다는 것이다. 즉 $g^{ab} = g^{ba}$이다.

## 프로토콜

**공개 파라미터**: 큰 소수 $p$, $\mathbb{Z}_p^*$의 생성원 $g$

**Step 1. Alice의 준비**

1. 비밀 $a$를 $1 \leq a \leq p-2$ 범위에서 무작위 선택
2. $A = g^a \bmod p$ 계산
3. $A$를 Bob에게 전송 (공개 채널)

**Step 2. Bob의 준비**

1. 비밀 $b$를 $1 \leq b \leq p-2$ 범위에서 무작위 선택
2. $B = g^b \bmod p$ 계산
3. $B$를 Alice에게 전송 (공개 채널)

**Step 3. 공유 비밀 계산**

- Alice: $s = B^a \bmod p$
- Bob: $s = A^b \bmod p$

![Diffie-Hellman 키 교환 — p=23, g=5 수치 예시](/images/diffie-hellman/dh-key-exchange.svg)

## 정확성 증명

왜 Alice와 Bob이 같은 값을 얻는가.

$$
B^a = (g^b)^a = g^{ba} \pmod{p}
$$

$$
A^b = (g^a)^b = g^{ab} \pmod{p}
$$

지수법칙에 의해 $g^{ba} = g^{ab}$이므로

$$
B^a = A^b = g^{ab} \pmod{p} \quad \checkmark
$$

도청자는 $g$, $p$, $A = g^a$, $B = g^b$를 모두 알지만, $a$도 $b$도 모른다. $g^{ab}$를 계산하려면 $a$ 또는 $b$가 필요한데, 이산 대수 문제(DLP)에 의해 $A$에서 $a$를 역산하는 것이 계산적으로 어렵다.

## 수치 예시: p=23, g=5

구체적으로 계산해 보자.

**Alice**: $a = 6$을 선택

$$
A = 5^6 \bmod 23 = 15625 \bmod 23 = 8
$$

**Bob**: $b = 15$를 선택

$$
B = 5^{15} \bmod 23 = 19
$$

**공유 비밀 계산**:

- Alice: $s = B^a = 19^6 \bmod 23 = 2$
- Bob: $s = A^b = 8^{15} \bmod 23 = 2$

검증: $g^{ab} = 5^{6 \cdot 15} = 5^{90} \bmod 23 = 2$ $\checkmark$

도청자는 $p=23$, $g=5$, $A=8$, $B=19$를 알지만, $a$와 $b$ 없이는 $s=2$를 계산할 수 없다.

## 보안 근거: CDH와 DDH 가정

DH 프로토콜의 보안은 두 가지 가정에 기반한다. 가정을 적기 전에 **어느 군에서 이야기하는지**부터 정해야 한다. 아래 두 가정은 $\mathbb{Z}_p^*$ 전체가 아니라 그 안의 **소수 위수 $q$인 부분군**에서 세운다. 이유는 DDH 항목에서 밝힌다.

### CDH (Computational Diffie-Hellman)

> $g$, $g^a$, $g^b$가 주어졌을 때, $g^{ab}$를 **계산**하는 다항식 시간 알고리즘이 존재하지 않는다.

이것은 ElGamal에서 다룬 것과 동일한 가정이다.

두 문제의 관계는 **한쪽 방향만** 알려져 있다. DLP를 풀 수 있으면 $g^a$에서 $a$를 얻어 $(g^b)^a$를 계산할 수 있으므로 CDH도 풀린다. 뒤집으면 **CDH가 어려우면 DLP도 어렵다.** 반대 방향, 곧 CDH를 푸는 능력으로 DLP를 푸는 일반적인 방법은 알려져 있지 않다. 그래서 CDH 가정은 DLP 가정보다 **강한** 가정이다. 「DLP가 어려우니 CDH도 어렵다」고 말할 수는 없다.

### DDH (Decisional Diffie-Hellman)

> $g$, $g^a$, $g^b$, $Z$가 주어졌을 때, $Z = g^{ab}$인지 $Z$가 랜덤인지 **구별**하는 것이 어렵다.

DDH는 CDH보다 강한 가정이다. $g^{ab}$를 계산하지 못하는 것(CDH)을 넘어, $g^{ab}$인지 아닌지조차 구별할 수 없다는 것이다.

**$\mathbb{Z}_p^*$ 전체에서는 DDH가 성립하지 않는다.** 르장드르 기호로 원소가 제곱잉여인지 아닌지를 다항식 시간에 판정할 수 있고, $g^{ab}$가 제곱잉여인지는 $g^a$와 $g^b$의 제곱잉여 여부만으로 정해지기 때문이다. 공격자는 $Z$의 제곱잉여 여부를 그 예측과 맞춰 보기만 하면 되고, 무작위 $Z$는 절반의 확률로 어긋난다.

그래서 DDH는 **소수 위수 $q$인 부분군**에서 세운다. 위수가 소수면 항등원이 아닌 모든 원소가 생성원이고, 제곱잉여 여부 같은 부분군 정보가 남지 않는다. $p = 2q + 1$인 안전 소수에서 제곱잉여 부분군이 바로 그런 군이다.

$$
\text{DDH 어려움} \implies \text{CDH 어려움} \implies \text{DLP 어려움}
$$

DDH 가정이 성립하면, 도청자가 $A$, $B$를 보더라도 공유 비밀 $s$에 대한 어떤 정보도 얻을 수 없다. $s$가 랜덤 값과 구별 불가능하기 때문이다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>DDH 가정은 CDH보다 한 단계 더 강한 주장이다. CDH는 "공유 비밀을 계산할 수 없다"이고, DDH는 "공유 비밀인지 랜덤 값인지 구별조차 할 수 없다"이다. 도청자가 $g^a$와 $g^b$를 모두 보더라도, 실제 공유 비밀 $g^{ab}$와 아무 관계 없는 랜덤 값을 구별할 방법이 없다는 뜻이다.</p>
</div>

## 중간자 공격 (MITM)

DH의 치명적 한계는 **인증(authentication)이 없다**는 것이다. Alice는 상대방이 Bob인지 확인할 방법이 없다.

공격자 Mallory가 Alice와 Bob 사이에 위치하면:

1. Alice → Mallory: $g^a$ (Alice는 Bob에게 보냈다고 믿음)
2. Mallory → Bob: $g^{m_1}$ (Mallory가 자신의 비밀 $m_1$로 생성)
3. Bob → Mallory: $g^b$ (Bob은 Alice에게 보냈다고 믿음)
4. Mallory → Alice: $g^{m_2}$ (Mallory가 자신의 비밀 $m_2$로 생성)

결과적으로 두 개의 독립된 세션이 만들어진다:

- Alice ↔ Mallory: 공유 비밀 $g^{a \cdot m_2}$
- Mallory ↔ Bob: 공유 비밀 $g^{m_1 \cdot b}$

Mallory는 양쪽 세션의 비밀을 모두 알고 있으므로, 모든 메시지를 복호화하고 변조한 뒤 재암호화할 수 있다. Alice와 Bob은 서로 직접 통신하고 있다고 믿는다.

![중간자 공격 — DH의 인증 부재 취약점](/images/diffie-hellman/mitm-attack.svg)

**해결책**: 전자 서명과 인증기관(CA)을 결합한다. DH 교환 시 $g^a$와 $g^b$에 서명을 붙이면, 수신자는 서명을 검증해 상대방의 신원을 확인할 수 있다. 이것이 TLS 핸드셰이크의 구조다.

## DH에서 ElGamal으로

ElGamal 포스트에서 "복호화 정확성은 Diffie-Hellman 키 교환의 직접적인 응용"이라고 했다. 이제 정확히 어떤 관계인지 볼 수 있다.

| DH 키 교환 | ElGamal 암호화 |
|:---:|:---:|
| Alice의 비밀 $a$ | 수신자의 비밀키 $x$ |
| Alice의 공개값 $g^a$ | 수신자의 공개키 $h = g^x$ |
| Bob의 비밀 $b$ | 송신자의 임시 키 $k$ |
| Bob의 공개값 $g^b$ | 암호문의 $A = g^k$ |
| 공유 비밀 $g^{ab}$ | 공유 비밀 $g^{xk}$ |

DH는 공유 비밀을 만드는 것에서 끝나지만, ElGamal은 여기에 메시지 마스킹이라는 한 단계를 추가한다. 이 흐름에서 ElGamal 암호화를 수행하는 송신자는 Bob이고, Alice는 자신의 비밀키로 복호화하는 수신자다. 공유 비밀 $g^{xk}$를 사용해 평문 $m$을 $B = m \cdot g^{xk}$로 마스킹한다.

![Diffie-Hellman에서 ElGamal으로의 확장 — 키 교환에서 암호화로](/images/diffie-hellman/dh-elgamal-relation.svg)

또한 DH는 양쪽이 **동시에 온라인**이어야 하는 대화형(interactive) 프로토콜이다. ElGamal은 수신자의 공개키를 미리 알고 있으면 수신자가 **오프라인**이어도 암호화할 수 있는 비대화형(non-interactive) 프로토콜로 전환한 것이다. 매 암호화마다 Bob이 새로운 $k$를 선택하는 것은 매번 일회성 DH 키 교환을 수행하는 것과 같다.

## 전방향 안전성 (Forward Secrecy)

DH의 중요한 보안 속성 중 하나는 **전방향 안전성(Forward Secrecy)** 이다.

말하기 전에 **키를 두 종류로 갈라야 한다.** 앞에서 본 프로토콜에는 $a$, $b$밖에 없어 「장기 키」라고 부를 것이 없다.

- **장기 키.** 상대가 누구인지 확인하는 데 쓴다. 서버 인증서의 서명 키가 그것이다. 앞 절에서 본 MITM 공격을 막으려면 이 키로 교환 메시지에 서명해야 한다.
- **임시 키(ephemeral).** 세션마다 새로 뽑는 $a$, $b$다. 공유 비밀 $g^{ab}$는 오직 이것으로 정해진다.

전방향 안전성은 이 구분 위에서 성립한다. 장기 서명 키가 나중에 새어도 과거 세션의 $g^{ab}$는 복원되지 않는다. 서명 키는 상대를 확인하는 데만 쓰였고 공유 비밀에는 들어가지 않기 때문이다.

**다만 조건이 붙는다.** $a$와 $b$를 세션이 끝난 뒤 실제로 지워야 하고, 세션마다 새로 뽑아야 한다. 같은 $a$를 여러 세션에서 재사용하면(static DH) 그 $a$가 새는 순간 그 $a$를 쓴 모든 과거 세션이 함께 풀린다. 전방향 안전성을 주는 것은 DH 자체가 아니라 **키를 임시로 쓰고 지운다는 운용**이다.

TLS 1.3은 이 방식을 표준으로 삼아, 키 교환을 하는 모드에서는 ephemeral (EC)DH만 허용하고 RSA 키 전송 방식을 없앴다. RSA 키 전송에서는 서버 개인키가 새면 과거 세션이 모두 복호화된다. 다만 TLS 1.3에도 미리 공유한 키만 쓰는 PSK-only 모드가 있어 모든 핸드셰이크가 DH를 쓰는 것은 아니다.

## 파라미터 선택

**소수 $p$**: DLP의 어려움은 $p$의 크기에 비례한다. 현재 권장은 2048비트 이상. $p$는 안전 소수(safe prime), 즉 $p = 2q + 1$ 형태로 $q$도 소수인 값을 사용해야 한다. $p-1$의 소인수가 작으면 Pohlig-Hellman 공격으로 DLP가 쉬워진다.

**생성원 $g$**: ElGamal과 동일하게, $g$는 $\mathbb{Z}_p^*$의 생성원이어야 한다. 실무에서는 $g$를 위수 $q = (p-1)/2$인 부분군의 생성원으로 선택해, $\mathbb{Z}_p^*$의 안전한 부분군에서 연산한다.

**비밀 $a$, $b$**: 각 세션마다 새로 생성해야 한다. 재사용하면 전방향 안전성이 깨진다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>Diffie-Hellman은 공개 채널만으로 비밀 키를 공유하는 최초의 프로토콜이다. $g^{ab} = g^{ba}$라는 지수법칙이 전부다.</li>
<li>보안은 CDH 가정에 기반한다 — $g^a$, $g^b$로부터 $g^{ab}$를 계산하는 것이 어렵다. DDH 가정은 더 나아가 $g^{ab}$인지 랜덤인지 구별조차 어렵다고 말한다.</li>
<li>인증이 없으므로 중간자 공격에 취약하다. 전자 서명·인증서와 결합해야 실용적이다.</li>
<li>ElGamal은 DH 키 교환에 메시지 마스킹을 결합한 것이다. 매 암호화가 일회성 DH 세션이다.</li>
<li>전방향 안전성 — 임시 비밀 폐기로 과거 세션이 보호된다. TLS 1.3이 DH 기반 교환을 필수로 요구하는 이유다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Digital Signature — 전자 서명의 수학적 구조</strong> — RSA·ElGamal 서명의 생성과 검증, 인증기관(CA)의 역할, 암호화 해시와 결합한 최종 프로토콜까지 디지털 서명의 전체 그림을 다룬다.</p>
</div>
