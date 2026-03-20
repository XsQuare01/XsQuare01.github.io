---
title: "DFA — 결정론적 유한 오토마타"
date: 2026-03-20
description: "튜링 머신을 단순화한 계산 모델인 DFA의 구조와 동작 원리를 살펴보고, Pumping Lemma를 통해 DFA로 풀 수 없는 문제가 존재함을 증명한다."
tags: ["Computer Science", "Complexity Theory"]
category: cs
---

> DFA는 계산 이론에서 가장 단순한 형태의 계산 모델이다. 튜링 머신을 극도로 제한한 이 기계는 어떤 문제를 풀 수 있고, 어떤 문제를 풀 수 없을까?

DFA(Deterministic Finite Automata)는 튜링 머신을 단순화한 자동 기계로, 상태를 저장하는 state machine이다. 계산 이론에서 DFA는 가장 제한적인 계산 모델이며, 이를 통해 "어떤 문제가 DFA로 해결 가능한가?"라는 질문에 답할 수 있다.

---

## DFA의 구조

DFA는 다섯 가지 요소의 튜플로 정의한다.

$$M = (Q,\ \Sigma,\ q,\ F,\ s)$$

- **Q**: State들의 집합
- **$\Sigma$**: Tape에 들어갈 수 있는 Symbol들의 집합 (= Alphabet)
- **q**: 처음 시작할 위치 (Initial state)
- **F**: Final State의 집합 (Accepting State)
  - 종료 시점의 상태를 $t$라 할 때, $t \in F$이면 **yes**를 출력한다.
- **s**: Transition Function
  - $(q, a) \to r$: 상태 $q$에서 입력 $a$를 읽으면 상태 $r$로 전이한다.

---

## DFA의 조건

DFA가 문제를 accept하려면 **오직 하나의 유한한 machine**이 해당 string을 처리해야 한다.

즉, 문제를 풀기 위해 여러 DFA를 동원하는 것은 허용되지 않는다. 예를 들면:

1. $0^i$ 부분은 M1이 해결하고, $1^i$ 부분은 M2가 해결하는 방식은 안 된다.
2. 입력 길이 0, 1, 2, 3, …에 따라 M0, M1, M2, M3, …을 만들어 해결하면 안 된다.
3. 입력 집합 $\{0, 1, 01, 10, 11, \ldots\}$에 대해 M0, M1, M10, …을 만들어 해결하면 안 된다.

> 2번과 3번은 machine의 개수가 무한히 많아지기 때문에도 허용되지 않는다.

---

## Problem X1: 입력은 짝수인가?

$$L_1 = \{0, 00, 10, 010, \ldots\}$$

마지막 비트가 0인 문자열, 즉 짝수를 나타내는 이진 문자열의 집합이다. 이에 대한 DFA는 다음과 같다.

![L1 DFA](/images/dfa/L1.jpeg)

- 맨 왼쪽의 화살표는 초기 상태($\lambda$)를 나타낸다.
- edge 위의 숫자는 해당 입력을 의미한다.
- **Accepting state**는 원을 2개로 표시한다.

---

## Problem X3: 입력에 '101'이 존재하는가?

$$L_3 = \{101, 0101, 01010, 1101, \ldots\}$$

부분 문자열로 `101`을 포함하는 모든 문자열의 집합이다. 이에 대한 DFA는 다음과 같다.

![L3 DFA](/images/dfa/L3.png)

---

## L4: $\{x \mid x = 0^i 1^j,\ \text{some}\ i, j \ge 0\}$

- $\lambda \in L_4$ ($\because\ i = j = 0$)
- 0이 임의의 횟수 나온 뒤 1이 임의의 횟수 나오는 문자열의 집합이다.

$$L_4 \text{의 DFA:}$$

![L4 DFA](/images/dfa/L4.png)

---

## 추가) Problem X4': 입력에 '10'이 존재하는가?

$$L_4' = \{x \mid x \text{는 '10'을 포함한다}\}$$

![L4' DFA](/images/dfa/L4prime.png)

이 DFA를 자세히 보면 L4의 DFA를 뒤집은 것과 유사하다.

L4에서 Accepting State가 되려면 **1이 나온 이후 0이 나오면 안 된다**. 따라서 L4를 다음과 같이 재정의할 수 있다.

$$L_4 = \{x \mid x\text{는 '10'을 포함하지 않는다}\}$$

---

## L5: $\{x \mid x = 0^i 1^i,\ \text{some}\ i \ge 0\}$

L4와의 차이점은 **0과 1의 개수가 같아야 한다**는 점이다.

L4에서는 앞에 0이 몇 개 나오든 상관없었지만, L5에서는 0이 1개 나올 때와 2개 나올 때의 상태가 달라야 한다. 0이 $k$개 나오면 반드시 1도 $k$개 나와야 accept하기 때문이다.

따라서 DFA로 일부만 표현하면 다음과 같다.

![L5 DFA (일부)](/images/dfa/L5.png)

1. $\lambda$는 L5에 속한다 ($i = 0$).
2. 0이 입력되면, 다음에 반드시 1이 입력되어야 한다.
   - 1이 들어오면 accept.
   - 그 이후 추가 입력이 오면 reject (왼쪽 dead state로 이동).
3. 0이 한 번 더 들어오면, "0이 1개인 상태"와 "0이 2개인 상태"는 다른 state여야 한다.
   - 전자는 이후 1이 한 번 나와야 accept, 후자는 두 번 나와야 accept하기 때문이다.
4. 이 과정을 반복하면 Machine의 크기가 무한히 커진다.

> 무한히 큰 machine은 현실에서 의미가 없지만, 이것만으로 "DFA로 풀 수 없다"는 근거가 되지는 않는다. 지금까지의 논의만으로는 L5가 DFA로 해결 가능한지 결론 내릴 수 없다.

---

## 증명: DFA로는 L5를 풀 수 없다

### 보조 가정

> **$n$개의 상태를 가진 DFA M이 길이 $n$ 이상의 string을 accept한다면, M은 무한히 많은 string을 accept한다.**

$n$개의 입력이 처리되는 동안의 상태 전이를 다음과 같이 표현한다.

$$q_1 \xrightarrow{i_1} q_2 \xrightarrow{i_2} q_3 \xrightarrow{i_3} \cdots \xrightarrow{i_n} q_{n+1}$$

$q_1, q_2, \ldots, q_{n+1}$은 총 $n+1$개이지만 상태는 $n$개뿐이다. **비둘기집 원리**에 의해 반드시 중복 상태가 존재한다. 이 중복 상태를 $r_k$라 하면:

$$q_1 \xrightarrow{i_1} \cdots \xrightarrow{i_l} r_k \xrightarrow{i_m} \cdots \xrightarrow{i_o} r_k \xrightarrow{i_p} \cdots \xrightarrow{i_n} q_f$$

$r_k$에서 $r_k$로 돌아오는 구간을 제거하거나 반복해도 여전히 $q_f$ (accepting state)에 도달할 수 있다. L3의 DFA를 예로 들면, $q_3 \to q_1$로 돌아가는 cycle이 있어, 이 구간을 생략하거나 반복해도 accepting state에 도달한다.

### Pumping Lemma

accept되는 string $w$에 대해, $|w| \ge n$이면 $w = xyz$로 분해할 수 있다.

$$|xy| \le n,\quad |y| > 0$$

이때 다음이 모두 accept된다.

$$xz,\ xyz,\ xy^2z,\ xy^3z,\ \ldots,\ xy^iz$$

- $x = i_1 i_2 \cdots i_l$ ($r_k$ 앞의 string)
- $y = i_m \cdots i_o$ ($r_k$에서 $r_k$로 돌아오는 구간)
  - 비둘기집 원리에 의해 중복은 반드시 발생하므로, $|y| > 0$
- $z = i_p \cdots i_n$ ($r_k$ 뒤의 string)
- $|x|, |z| \ge 0$ (겹치는 부분의 앞뒤가 없을 수도 있으므로)

$y$는 중복이 발생하는 구간이므로, 이를 제거하거나 반복해도 accept된다. 또한 길이 $n$인 string을 처리하는 동안 중복이 발생하므로 $|xy| \le n$이다.

### 귀류법으로 증명

**가정**: $n$개의 state를 가진 DFA M이 L5를 풀 수 있다.

1. M은 $n$개의 state를 가지므로 $0^n 1^n$을 accept한다.
2. Pumping Lemma에 따라 $w = 0^n 1^n = xyz$로 분해할 수 있다.
3. $|xy| \le n$이므로 $x$와 $y$는 모두 0으로만 구성된다. 즉, $xyz = x \cdot y \cdot z'1^n$ 형태이다.
4. 따라서 $xz'1^n$, $xyz'1^n$, $xy^2z'1^n$, … 모두 accept되어야 한다.
5. 그런데 $xz'1^n$을 보면, $|y| > 0$이므로 0의 개수가 최소 1개 줄어들어 **0의 개수 ≠ 1의 개수**가 된다.
6. L5는 $0^i 1^i$ ($i$개씩 같아야 accept)이므로, $xz'1^n \notin L_5$이다. **모순.**

$$\therefore \text{DFA로는 L5를 풀 수 없다.}$$

---

## 결론: DFA로도 풀 수 없는 문제가 존재한다

위의 증명을 통해 DFA는 0과 1의 개수를 **기억**할 수 없다는 것을 알 수 있다. 유한한 상태만으로는 "지금까지 0이 몇 개 나왔는지"를 무제한으로 추적할 수 없기 때문이다.

---

## Classes: Problem들의 집합

**Class**는 공통된 성질을 가진 Problem들의 집합이다. Problem의 집합 전체 크기는 약 $2^{2^{|\Sigma^*|}}$개, 즉 $|2^{|\mathbb{R}|}|$개에 달하지만, 실제로 기술(describable) 가능한 Class의 수는 가산 무한(Countable Infinite)이다.

### Class DFA

**DFA로 풀 수 있는 Language들의 집합**을 Class DFA라 한다.

$$L_4 \in \text{DFA}, \quad L_5 \notin \text{DFA}$$
