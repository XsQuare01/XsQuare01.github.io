---
title: "NP의 다른 정의 — 검증자와 증명서"
date: 2026-03-22T14:00:00
description: "NTM 기반의 NP 정의와 검증자(Verifier) 기반의 NP 정의가 동치임을 보인다. '힌트가 있을 때 빠르게 검증할 수 있는 문제'라는 직관이 어떻게 수학적으로 엄밀해지는지 탐구한다."
tags: ["Computer Science", "Complexity Theory"]
category: cryptography
---

> NP를 "NTM이 다항식 시간에 푸는 문제"라 정의했다. 그런데 NP에는 전혀 다른, 더 직관적인 정의가 존재한다. 두 정의는 완전히 동치다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>NP의 두 정의</strong>: Df1(NTM 기반)과 Df2(검증자/증명서 기반) — 두 정의는 동치</li>
<li><strong>증명서(Certificate)</strong>: 어떤 입력이 언어에 속함을 증명해주는 힌트. 다항식 길이 이하</li>
<li><strong>검증자(Verifier)</strong>: 입력과 증명서를 받아 다항식 시간에 검증하는 DTM</li>
<li><strong>암호학적 함의</strong>: P ≠ NP라면 Eve는 도청한 암호문만으로 복호화할 수 없다</li>
</ul>
</div>

앞선 글에서 NP를 "NTM이 다항식 시간에 결정하는 언어 클래스"로 정의했다. 이 정의는 수학적으로 명확하지만, 현실에서 NTM은 존재하지 않는다. NP를 더 현실적으로 이해할 수 있는 동치 정의가 있다.

---

## NP의 두 가지 정의

### Df1: NTM 기반 정의

$$L \in NP \iff \exists \text{ 다항식 시간 NTM } M : L = L(M)$$

NTM이 모든 계산 경로를 동시에 탐색하는 것을 허용한다. 경로 중 하나라도 accept 상태에 도달하면 accept한다.

### Df2: 검증자(Verifier) 기반 정의

$$L \in NP \iff \exists \text{ 다항식 시간 DTM (검증자) } V,\ \exists \text{ 다항식 } p : $$

$$x \in L \iff \exists h,\ |h| \leq p(|x|) : V(x, h) = \text{Yes}$$

여기서 $h$를 **증명서(Certificate)** 또는 **증인(Witness)** 이라 한다. $x$가 언어에 속한다는 사실을 증명해주는 힌트다.

![NP의 검증자 모델](/images/np-alternative/np-certificate.svg)

---

## 증명서란 무엇인가?

증명서 $h$는 네 가지 조건을 만족해야 한다.

1. **존재 조건**: $x \in L$이면, $V(x, h) = \text{Yes}$인 $h$가 반드시 존재한다.
2. **건전성 조건**: $x \notin L$이면, 어떤 $h$를 제시해도 $V(x, h) = \text{No}$다.
3. **길이 조건**: $|h| \leq p(|x|)$ — 입력 크기에 대한 다항식 이하
4. **효율성 조건**: $V(x, h)$가 다항식 시간에 Yes/No를 판정

조건 1과 2의 **비대칭성** 이 핵심이다. 증명서 $h$는 "$x$가 L에 속함"을 증명할 수 있지만, $h$가 없다는 사실이 "$x$가 L에 속하지 않음"을 증명하지는 않는다. 즉, V가 No를 출력했다고 해서 $x \notin L$이라는 뜻이 아니다 — 단지 그 $h$가 올바른 증명서가 아닌 것이다.

### 구체적인 예: Longest Path 문제

그래프 $G$, 두 정점 $s, t$, 정수 $k$가 주어졌을 때, $G$에서 $s$에서 $t$까지의 단순 경로 중 길이가 $k$ 이상인 것이 존재하는지 판별하는 문제다.

- **증명서**: 길이 $k$ 이상의 구체적인 경로 (정점 목록)
- **검증**: 주어진 경로가 단순 경로인지, 길이가 $k$ 이상인지 확인 — 다항식 시간

증명서 없이 이 경로를 찾는 것(결정)은 어렵지만, 누군가 경로를 알려주면 검증은 쉽다. 이것이 NP의 핵심 직관이다.

---

## 암호학적 함의: 힌트의 비대칭성

![P ≠ NP 가정 하의 암호학적 함의](/images/np-alternative/np-crypto.svg)

암호화 체계에서 핵심은 **힌트(key)의 유무** 다.

- **Bob(수신자)**: 암호문 $c$와 key $k$를 가진다. $k$는 증명서 역할을 한다. 검증자 $V$를 실행해 다항식 시간에 복호화한다.
- **Eve(도청자)**: 암호문 $c$만 가진다. 증명서 없이 NP 문제를 직접 풀어야 한다.

P ≠ NP라면 Eve는 지수 시간 이상이 필요하므로, 현실적인 시간 안에 복호화할 수 없다. 암호학적 안전성이 P ≠ NP 가정 위에 서 있는 이유다.

---

## Df1과 Df2의 동치 증명

### Df1 ⊆ Df2: NTM → 검증자

NTM $M$이 $x \in L$을 accept할 때, 계산 트리에서 accept에 이르는 경로가 하나 이상 존재한다.

**그 경로 자체를 증명서 $h$로 사용한다.**

- $M$이 다항식 시간 $p(n)$ 안에 동작하므로, accept 경로의 길이도 $p(n)$ 이하
- 검증자 $V$는 $h$로 지정된 경로를 따라 $M$을 시뮬레이션한다
- $M$이 accept하면 $V$는 Yes를 출력한다

따라서 $L \in \text{Df1} \Rightarrow L \in \text{Df2}$

### Df2 ⊆ Df1: 검증자 → NTM

검증자 $V$와 다항식 $p$가 존재해 $x \in L \iff \exists h, |h| \leq p(|x|) : V(x,h) = \text{Yes}$라 하자.

**NTM을 다음과 같이 구성한다:**

1. 비결정론적으로 길이 $p(|x|)$ 이하의 모든 가능한 $h$를 열거한다
2. 각 $h$에 대해 $V(x, h)$를 실행한다
3. $V(x, h) = \text{Yes}$인 경우 accept한다

- $h$의 길이는 $p(|x|)$ 이하이므로, 가능한 후보의 수는 유한하고, NTM은 이를 비결정론적으로 선택할 수 있다
- $V$가 다항식 시간에 동작하므로, 전체 NTM도 다항식 시간 안에 동작한다

따라서 $L \in \text{Df2} \Rightarrow L \in \text{Df1}$

---

## 결론

| | Df1 (NTM 기반) | Df2 (검증자 기반) |
|---|---|---|
| 핵심 아이디어 | 모든 경로를 동시에 탐색 | 힌트가 있으면 빠르게 검증 |
| 직관 | 병렬 탐색 | 힌트의 비대칭성 |
| 증명서 | 암묵적 (경로 = 증명서) | 명시적 (증명서 $h$) |
| 동치 여부 | 두 정의는 완전히 동치 | — |

<div class="callout callout-key">
<div class="callout-title">핵심 정리: NP의 검증자 정의</div>
<ul>
<li>NP = "다항식 길이의 증명서가 존재하면, 다항식 시간에 검증할 수 있는 언어 클래스"</li>
<li>Df1(NTM)과 Df2(검증자)는 동치다 — 증명서 = NTM accept 경로, NTM = 증명서를 비결정론적으로 추측하는 기계</li>
<li>P ≠ NP 가정이 성립하면, 증명서(key) 없는 Eve는 암호문을 현실적 시간 안에 풀 수 없다</li>
<li>NP 문제의 어려움은 "풀기"에 있지, "검증하기"에 있지 않다 — 이 비대칭성이 현대 암호학의 기반이다</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>NP-Complete — NP에서 가장 어려운 문제들</strong> — NP 안에서도 특별한 위치를 차지하는 NP-Complete를 정의하고, Reduction(귀착) 개념과 Cook의 정리를 통해 SAT가 최초의 NP-Complete 문제임을 증명하는 과정을 살펴본다.</p>
</div>
