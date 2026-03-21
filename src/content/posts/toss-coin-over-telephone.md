---
title: "Toss Coin over Telephone"
date: 2026-03-17
description: "전화로 공정하게 동전 던지기를 할 수 있을까? Manuel Blum이 제안한 암호학적 동전 던지기 프로토콜과 그 수학적 배경을 다룬다."
tags: ["Cryptography", "Complexity Theory", "Mathematics"]
category: cryptography
---

> 이 프로토콜은 **Manuel Blum(1983)** 이 제안한 암호학적 동전 던지기(Coin Flipping over Telephone) 프로토콜이다. 두 참여자가 물리적으로 만나지 않고도 공정한 내기를 할 수 있음을 보여준다.

---

A와 B가 전화 통화를 하며 내기를 한다. A는 동전을 던지고, B는 A가 던진 동전의 면을 맞추는 내기이다. 당연히 A는 B가 말한 내용을 듣고 결과를 바꾸어 말할 수 있다. **공정하게 게임을 하기 위해서는 어떻게 해야 하는가?**

**핵심 아이디어:** 이차 합동식 $x^2 \equiv y \pmod{n}$은 $n$을 소인수분해할 수 있으면 4개의 해를 구할 수 있지만, $n$의 소인수를 모르면 풀기 어렵다는 수학적 성질을 이용한다.

| 참여자 | 알고 있는 정보 |
|---|---|
| A | $p,\ q,\ n$ 모두 |
| B | $n$과 자신이 선택한 $x$만 |

---

## 프로토콜 흐름

![프로토콜 흐름 — Alice & Bob](/images/toss-coin/protocol-flow.svg)

1. A는 다음을 만족하는 3 이상의 소수 $p,\ q \equiv 3 \pmod{4}$를 고르고 B에게 $n = pq$를 전달한다. 이때 $p, q$는 공개하지 않는다.
   - $p \equiv q \equiv 3 \pmod{4}$ 조건은 이후 이차잉여의 제곱근 계산을 쉽게 만들기 위함이다. 이 조건을 만족하는 $n = pq$를 **Blum 정수**라고 한다.

2. B는 $0 \leq x < n$을 만족하는 $x$를 선택한 후, $y \equiv x^2 \pmod{n}$을 만족하는 $y$를 A에게 전달한다. 이때 $x$는 공개하지 않는다.

3. A는 $p, q$를 알고 있으므로, **CRT(중국인의 나머지 정리)** 를 이용하여 $y \equiv x^2 \pmod{n}$의 네 근 $\pm x_1,\ \pm x_2$를 구하고, 이 중 하나를 B에게 전달한다.
   - $p \equiv 3 \pmod{4}$ 조건 덕분에 $r_p \equiv y^{(p+1)/4} \pmod{p}$로 $\pmod{p}$ 제곱근을 쉽게 구할 수 있다. (마찬가지로 $r_q \equiv y^{(q+1)/4} \pmod{q}$)
   - CRT로 두 값을 합성하면 네 근 $x_1,\ n-x_1,\ x_2,\ n-x_2$를 얻는다.

4. B가 선택한 $x$가 $x_1$ 또는 $n - x_1$과 같다고 가정하자.
   - A가 B에게 $x_2$ 또는 $n - x_2$를 전달하면: B는 서로 다른 두 제곱근 $x$와 $x_2$를 모두 알게 된다. 이를 이용해 $\gcd(x - x_2,\ n)$을 계산하면 $p$ 또는 $q$를 구할 수 있다. → **B 승리**
   - A가 B에게 $x_1$ 또는 $n - x_1$을 전달하면: B는 자신이 이미 아는 값만 얻게 되므로 $p, q$를 구할 수 없다. → **A 승리**

5. 따라서 B는 A로부터 받은 값으로 $p, q$를 소인수분해할 수 있으면 B의 승리, 그렇지 않으면 A의 승리다.
   - A는 4개의 근 중 어느 것을 줄지 선택할 수 있지만, B의 $x$를 모르기 때문에 **자신에게 유리한 것을 고를 수 없다.** → **공정성 보장**
   - 결과적으로 A가 이길 확률과 B가 이길 확률은 각각 $1/2$이다.

6. 만약 A가 올바른 $n$ 값을 전달하지 않을 경우, B는 다음과 같은 방법으로 검증할 수 있다.
   - A가 전달한 근 $x_1$에 대해 $x_1^2 \equiv y \pmod{n}$이 성립하는지 확인하면 된다.
   - 성립하지 않는다면 A가 올바른 $n$을 전달하지 않은 것이다.

---

## 왜 공정한가?

<div class="callout callout-key">
<div class="callout-title">보안 목표 요약</div>
<ul>
<li><strong>A의 속임 방지:</strong> A는 4개의 근 중 무엇을 보내야 B에게 불리한지 모른다. B의 x를 알 방법이 없기 때문이다.</li>
<li><strong>B의 속임 방지:</strong> B는 y를 전달한 뒤 x를 바꿀 수 없다. y = x² mod n으로 이미 커밋되어 있다.</li>
<li><strong>안전성의 근거:</strong> 소인수분해 문제의 어려움. 4개의 근을 모두 구하는 것 ↔ n을 소인수분해하는 것은 수학적으로 동등하다.</li>
</ul>
</div>

이 프로토콜의 안전성은 **소인수분해 문제의 어려움** 에 기반한다.

**핵심 동등성:**

> $x^2 \equiv y \pmod{n}$의 4개의 근을 모두 구할 수 있다 $\Longleftrightarrow$ $n$을 소인수분해할 수 있다.

**증명 (⇐):** $n = pq$를 알면 CRT로 4개의 근을 모두 구할 수 있다. (A가 하는 일)

**증명 (⇒):** 서로 다른 두 제곱근 $x, x'$에 대해 $x^2 \equiv x'^2 \pmod{n}$이면:

$$n \mid (x - x')(x + x')$$

$n \nmid (x - x')$이고 $n \nmid (x + x')$이므로, $\gcd(x - x',\ n)$은 $p$ 또는 $q$가 된다.

**공정성 보장:**
- A는 B가 어떤 $x$를 골랐는지 모르므로, B에게 유리한 쌍 $(x_2,\ n-x_2)$을 골라줄지, 불리한 쌍 $(x_1,\ n-x_1)$을 줄지 알 수 없다.
- 결과적으로 A의 선택은 사실상 **랜덤**이며, 각 참여자의 승률은 정확히 $1/2$이다.

---

## 공격 시나리오

| 공격자 | 시도 | 왜 실패하는가 |
|---|---|---|
| A | 올바르지 않은 $n$ 전달 | B가 $x_1^2 \equiv y \pmod{n}$ 검증으로 탐지 가능 |
| A | 결과 발표 직전 유리한 근 선택 | B의 $x$를 모르므로 어느 쌍이 유리한지 알 수 없음 |
| B | $x$ 사후 변경 | $y = x^2 \bmod n$으로 이미 커밋 — 변경 불가 |
| A | Blum 정수 아닌 $n$ 사용 | 근의 개수·분포가 달라져 공정성 붕괴. 영지식 증명으로 방지 가능 |

---

## 용어 정리

<div class="glossary">
  <div class="glossary-item">
    <span class="glossary-term">이차잉여 (Quadratic Residue)</span>
    <span class="glossary-def">x² ≡ a (mod n)을 만족하는 정수 x가 존재할 때, a를 n의 이차잉여라 한다.</span>
  </div>
  <div class="glossary-item">
    <span class="glossary-term">Blum 정수</span>
    <span class="glossary-def">p ≡ q ≡ 3 (mod 4)를 만족하는 두 소수의 곱 n = pq. 제곱근 계산 공식을 정수 지수로 쓸 수 있게 해준다.</span>
  </div>
  <div class="glossary-item">
    <span class="glossary-term">CRT (중국인의 나머지 정리)</span>
    <span class="glossary-def">서로소인 모듈러스의 연립 합동식을 유일하게 풀어주는 정리. (mod p)와 (mod q)의 근을 합성해 (mod n)의 4개 근을 구할 때 사용한다.</span>
  </div>
  <div class="glossary-item">
    <span class="glossary-term">커밋 (Commit)</span>
    <span class="glossary-def">값을 숨겨두되 나중에 공개·검증할 수 있게 하는 암호학적 약속. 이 프로토콜에서 y는 x에 대한 커밋이다.</span>
  </div>
</div>

---

<div class="section-label section-label-deep">수학 배경</div>

## 이차잉여 (Quadratic Residue)

**정의:** 정수 $a$가 $n$의 **이차잉여** 라는 것은, $x^2 \equiv a \pmod{n}$을 만족하는 정수 $x$가 존재함을 의미한다.

**소수 모듈러스에서의 제곱근 개수:**
- 소수 $p$에 대해, $a \not\equiv 0 \pmod{p}$인 이차잉여 $a$의 제곱근은 정확히 **2개** ($\pm r$)이다.

**합성수 모듈러스에서의 제곱근 개수:**
- $n = pq$ ($p, q$: 서로 다른 소수)일 때, $x^2 \equiv y \pmod{n}$의 해는 정확히 **4개** ($x_1,\ n-x_1,\ x_2,\ n-x_2$)이다.
- 이는 CRT에 의해 $\pmod{p}$의 해 2개와 $\pmod{q}$의 해 2개를 조합하기 때문이다.
- **핵심:** $n$의 소인수를 알면 4개의 근을 모두 구할 수 있지만, 모르면 하나의 근에서 나머지를 유추하기 어렵다.

## 왜 $p \equiv 3 \pmod{4}$인가?

$\pmod{p}$ 제곱근을 구하는 공식 $r_p \equiv y^{(p+1)/4} \pmod{p}$가 성립하는 이유를 확인해보자.

**전제 조건:**
$p$가 소수이고, $y$가 $p$의 이차잉여이면, **Euler's Criterion** 에 의해 다음이 성립한다.

$$y^{(p-1)/2} \equiv 1 \pmod{p}$$

**검증:**

$$\left(y^{(p+1)/4}\right)^2 = y^{(p+1)/2} = y^{(p-1)/2} \cdot y \equiv 1 \cdot y = y \pmod{p}$$

- 즉, $r_p = y^{(p+1)/4}$는 실제로 $y$의 $\pmod{p}$ 제곱근이 맞다.
- 단, 이 공식이 **정수**가 되려면 $(p+1)/4$가 정수여야 하므로, $p \equiv 3 \pmod{4}$ 조건이 필요하다.
  - $p \equiv 1 \pmod{4}$이면 $(p+1)/4$가 정수가 아니므로 이 방법을 쓸 수 없다.

---

## 프로토콜의 한계

1. **A의 Blum 정수 미준수:** A가 $n$을 Blum 정수가 아닌 값으로 전달해도 B가 즉시 알아채기 어렵다. 이를 막으려면 **영지식 증명(Zero-Knowledge Proof)** 으로 A가 올바른 Blum 정수를 전달했음을 증명해야 한다.

2. **B의 $x$ 선택 편향:** B가 $x$를 무작위로 고르지 않으면 프로토콜의 공정성이 깨질 수 있다.

3. **단일 비트 보장:** 이 프로토콜은 한 번의 동전 던지기만 보장한다. 여러 번 반복하려면 확장이 필요하다.

---

## 관련 개념

**Rabin 암호화:**
이 프로토콜과 동일한 수학적 구조를 사용한다. 공개 키 $n = pq$로 암호화하고($c \equiv m^2 \pmod{n}$), 비밀 키 $p, q$로 복호화한다. Rabin 암호화의 보안은 소인수분해 문제와 수학적으로 **동등** 함이 증명되어 있다.

**Blum-Blum-Shub (BBS) 난수 생성기:**
Blum 정수 $n = pq$와 초기값 $x_0$으로부터 $x_{i+1} = x_i^2 \pmod{n}$을 반복해 난수를 생성하는 암호학적으로 안전한 의사난수 생성기다. 이 프로토콜과 동일한 이차잉여 구조를 기반으로 한다.

## 출처

- Emory University Math Center — [Flipping Coins on the Phone](https://mathcenter.oxford.emory.edu/site/math125/flippingCoinsOnThePhone/)

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>집합의 크기(Cardinality)</strong> — 무한집합에도 크기가 있을까? 자연수·정수·유리수·실수의 크기를 비교하고, 칸토어의 대각선 논법을 통해 더 큰 무한이 존재함을 증명한다.</p>
</div>
