---
title: "Problem & Solution — Complexity Theory의 수학적 정의"
date: 2026-03-19
description: "Complexity Theory에서 '문제'와 '풀이'는 어떻게 정의될까? Decision Problem, Language, 튜링 머신을 통해 풀리지 않는 문제가 왜 대부분인지를 살펴본다."
tags: ["Mathematics", "Complexity Theory"]
category: theory
difficulty: 입문
---

> Complexity Theory에서 '문제'와 '풀이'는 우리가 일상적으로 쓰는 의미와 다르게 정의된다. 이 글에서는 그 수학적 정의를 따라가며, 풀 수 있는 문제보다 풀 수 없는 문제가 압도적으로 많다는 사실을 확인한다.

<div class="callout">
<div class="callout-title">선수지식</div>
<ul>
<li>집합의 크기(Cardinality) — 가산/불가산 무한</li>
<li>자연수 ℕ 와 실수 ℝ 의 크기 차이</li>
</ul>
</div>

<div class="callout callout-key">
<div class="callout-title">이 글의 핵심</div>
<ul>
<li>Complexity Theory에서는 문제를 <strong>Language</strong>로 정의한다.</li>
<li>Problem의 수는 <strong>불가산 무한 |ℝ|</strong>, Solution의 수는 <strong>가산 무한 |ℕ|</strong>이다.</li>
<li>따라서 <strong>풀 수 없는 문제가 대부분</strong>이다.</li>
</ul>
</div>

---

## Decision Problem

**답이 yes 또는 no인 문제** 를 Decision Problem이라 한다.

Complexity Theory에서는 모든 문제를 Decision Problem으로 다룬다. 이유는 두 가지다.

1. 출력이 yes/no로 단순해 다루기 쉽다.
2. Decision Problem만으로도 모든 문제를 해결할 수 있다.

두 번째 이유가 직관적으로 와 닿지 않을 수 있다. Shortest Path 문제를 예시로 살펴보자.

<div class="example-label">Example</div>

### Shortest Path 예시

다음 세 가지 문제를 생각해보자.

| 문제 유형 | 입력 | 출력 |
|---|---|---|
| 경로 문제 | Graph G, Start S, End E | 경로 P |
| 길이 문제 | Graph G, Start S, End E | 길이 L |
| Decision 문제 | Graph G, Start S, End E, Length L | yes / no |

![Decision Problem 환원 체인](/images/problem-and-solution/problem-transform.svg)

**Decision으로 길이를 구할 수 있을까?**

Binary Search로 가능하다. $L$의 범위를 최솟값(edge 최소 길이)과 최댓값(모든 edge의 합)으로 잡고, 중간값에 대해 Decision 문제를 반복 호출하면 최단 거리 $L$을 구할 수 있다.

**길이로 경로를 구할 수 있을까?**

다음 과정으로 가능하다.

1. 임의의 edge 하나를 제거한 그래프 $G'$에서 최단 거리 $L'$을 구한다.
2. $L' > L$이면 제거한 edge가 최단 경로에 포함된 것이므로 복원한다.
3. $L' = L$이면 제거한 edge는 최단 경로에 불필요하므로 그대로 제거한다.
4. 이 과정을 반복하면 최종적으로 최단 경로 $P$만 남는다.

따라서 **Decision Problem 하나만으로도 경로 문제의 답을 구할 수 있다.** 물론 시간·공간적으로 비효율적이지만, 핵심은 "Decision Problem만으로 모든 문제를 해결할 수 있다"는 사실이다.

---

## Terminology

<div class="glossary">
<div class="glossary-item">
<span class="glossary-term">Alphabet (Σ)</span>
<span class="glossary-def">사용할 문자들의 유한 집합. 각 원소를 Symbol이라 한다.</span>
</div>
<div class="glossary-item">
<span class="glossary-term">String</span>
<span class="glossary-def">Symbol을 유한하게 나열한 것. λ는 빈 문자열.</span>
</div>
<div class="glossary-item">
<span class="glossary-term">Language</span>
<span class="glossary-def">String들의 집합. 크기 제한 없음.</span>
</div>
</div>

### Alphabet ($\Sigma$)

우리가 사용하는 문자들의 유한한 집합.

- **Symbol**: Alphabet의 각 원소
- 영어 알파벳, 숫자 등 무엇이든 유한하기만 하면 된다.
  - 보통 앞의 글자부터 사용한다. (a, b, c, …)
  - 실제로는 2진수(0, 1)만으로도 모든 것을 표현할 수 있다. 컴퓨터도 내부적으로 0과 1의 문자열로 모든 데이터를 저장한다.

### String

Symbol을 유한하게 나열한 것(단어).

- 문자열을 나타낼 때는 보통 뒤쪽 알파벳을 사용한다. (x, y, z, …)
- 예시: $x = abbbac$
- $\lambda$: 길이가 0인 빈 문자열
- **Concatenation**: 두 문자열을 이어붙이는 것
  - $x = 110,\ y = 10 \Rightarrow xy = 11010$
  - $x = 110 \Rightarrow \lambda x = 110$

### Language

String들의 집합. 크기가 유한하든 무한하든 상관없다.

- 예시: $\{\lambda,\ 0,\ 10,\ 010,\ 100\}$

---

## Problem = Language

**답이 yes인 입력들을 모아놓은 집합이 곧 Problem이다.**

$$\text{Language} = \text{Problem}$$

Language에 속하는 문자열은 답이 yes인 입력이다. 예시를 통해 이해해보자.

- **Problem $X_1$**: 2진수로 해석했을 때 입력이 짝수인가?
  - **Language $L_1$**: $\{0, 00, 10, 010, \ldots\}$

- **Problem $X_2$**: 입력이 0으로 끝나는가?
  - **Language $L_2$**: $\{0, 00, 10, 010, \ldots\}$

$L_1 = L_2$이므로, $X_1$과 $X_2$는 서로 같은 문제다.

이처럼 Problem을 Language로 정의하면, 두 문제가 동일한지 비교하기 쉬워진다.

> 이제 Problem을 Language로 정의했으니, 가능한 문제의 수를 셀 수 있다.

---

## 문제는 몇 개나 존재할까?

### String의 수: $|\Sigma^*|$

$\Sigma = \{a, b, c\}$라 할 때, 가능한 모든 문자열 집합 $\Sigma^*$는 다음과 같다.

$$\Sigma^* = \{(\lambda)_0,\ (a, b, c)_1,\ aa,\ ab,\ ac,\ \ldots\}$$

길이에 따라 자연수 번호를 붙일 수 있으므로, $|\Sigma^*| = |\mathbb{N}|$ — 가산 무한이다.

### Problem의 수: $|2^{\Sigma^*}|$

모든 Problem은 $\Sigma^*$의 부분집합이므로, 가능한 문제의 집합은 $2^{\Sigma^*}$이다.

$$|2^{\Sigma^*}| = |\mathbb{R}|$$

<div class="callout callout-key">
<div class="callout-title">핵심 크기 비교</div>
<ul>
<li>String의 수: |Σ*| = |ℕ| — 가산 무한</li>
<li>Problem의 수: |2^Σ*| = |ℝ| — <strong>불가산 무한</strong></li>
</ul>
</div>

즉, **문제의 수는 불가산 무한** 이다.

---

## 모든 문제는 설명 가능한가?

위에서 문제의 수가 불가산 무한($|\mathbb{R}|$)임을 확인했다. 그렇다면 우리가 실제로 설명할 수 있는 문제는 몇 개나 될까?

설명할 수 없는 문제는 다룰 수 없기 때문에 이 질문은 중요하다.

문제를 설명하려면 **유한한 문자열** 로 표현해야 한다. 따라서 설명 가능한 문제의 수는 가산 무한($|\mathbb{N}|$)에 불과하다.

> **대부분의 문제는 설명조차 할 수 없다.**

이런 상황이 발생하는 이유는 Problem을 Language로 정의했기 때문이다. '설명할 수 없는 것을 문제라고 부를 수 있는가'라는 철학적 의문이 생기지만, Problem = Language로 정의하는 이유는 단순히 Problem을 직접 정의하기 어렵기 때문에 Language의 정의를 빌려 쓰는 것이다.

> 문제의 수를 알았다면, 이제 그것을 푸는 방법(Solution)의 수와 비교해야 한다.

---

## Solution: 튜링 머신

### Turing Machine

현재 컴퓨터의 이론적 모델이 된 수학적 기계. 알란 튜링이 1936년에 제안했다.

### Church-Turing Thesis

> 튜링 머신으로 모든 머신을 시뮬레이션할 수 있다.

Thesis(명제)라고 부르는 이유는, 아직 만들어지지 않은 미래의 컴퓨터도 존재할 수 있기 때문에 완전히 증명된 것은 아니기 때문이다.

### 튜링 머신의 구조

- **Tape**: 읽고 쓰는 저장 공간. 한쪽 방향으로 무한하다.
  - 최대한 단순하게 설계하기 위해 한쪽 방향만 무한하게 설정했다.
- **Cell**: Tape의 한 칸. 어떤 Symbol도 저장할 수 있다.
- **Read/Write Head**: 현재 읽고 있는 Cell을 가리킨다.
- **Finite Control (Head Control)**: 규칙(Rule)을 담고 있는 제어 장치. 컴퓨터의 CPU에 해당한다.
  - **State**: Control의 현재 상태
  - **Rule**: 다음과 같이 표현한다.

$$(q,\ x_1) \to (x_2,\ R,\ r)$$

현재 State가 $q$이고 Head가 $x_1$을 가리키면, $x_2$를 쓰고 오른쪽($R$)으로 이동 후 State를 $r$로 전환한다.

이 단순한 Rule 하나만으로도 모든 계산이 가능하며, 이것이 Church's Thesis의 핵심 주장이다.

**따라서, 튜링 머신이 풀 수 없는 문제는 어떤 컴퓨터로도 풀 수 없다. 이를 기준으로 Solution을 정의한다.**

---

## Solution은 몇 개나 존재할까?

Solution = 튜링 머신이다.

튜링 머신의 State 집합($Q$)과 Transition function은 모두 **유한한 문자열** 로 표현 가능해야 한다. 따라서 가능한 튜링 머신의 수, 즉 **Solution의 수는 가산 무한($|\mathbb{N}|$)** 이다.

앞서 문제의 수는 불가산 무한($|\mathbb{R}|$)이었다.

![Problems vs Solutions — 크기 비교](/images/problem-and-solution/problem-vs-solution.svg)

<div class="callout callout-key">
<div class="callout-title">최종 결론</div>
<ul>
<li>Problems: |2^Σ*| = |ℝ| — 불가산 무한</li>
<li>Solutions: |ℕ| — 가산 무한</li>
<li><strong>풀 수 없는 문제가 압도적으로 많다.</strong> 풀 수 있는 문제는 전체 중 극히 일부에 불과하다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>DFA — 결정론적 유한 오토마타</strong> — 계산 이론에서 가장 단순한 계산 모델인 DFA의 구조와 동작 원리를 살펴본다. Pumping Lemma를 통해 DFA로도 풀 수 없는 문제가 존재함을 증명한다.</p>
</div>
