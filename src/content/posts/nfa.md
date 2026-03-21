---
title: "NFA — 비결정론적 유한 오토마타"
date: 2026-03-20T10:00:00
description: "DFA를 확장한 계산 모델인 NFA의 구조와 accept 조건을 살펴보고, Powerset Construction을 통해 NFA와 DFA의 계산 능력이 동일함을 설명한다."
tags: ["Computer Science", "Complexity Theory"]
category: cryptography
---

> DFA에서는 하나의 상태에서 하나의 입력에 대해 정확히 하나의 다음 상태만 존재했다. NFA는 이 제약을 풀어, 하나의 입력에 대해 여러 상태로 동시에 전이할 수 있다. 더 강력한 모델처럼 보이지만, 실제 계산 능력은 DFA와 동일하다.

NFA(Non-deterministic Finite Automata)는 **비결정론적 유한 자동기계** 다. DFA와 구조는 유사하지만, 하나의 상태에서 동일한 입력에 대해 여러 상태로 동시에 전이할 수 있다는 점이 근본적으로 다르다. "비결정론적"이란 다음 상태가 하나로 결정되지 않는다는 의미다.

---

## NFA의 구조

NFA도 DFA와 마찬가지로 다섯 가지 요소의 튜플로 정의한다.

$$M = (Q,\ \Sigma,\ q_0,\ F,\ \Delta)$$

- **$Q$**: State들의 집합
- **$\Sigma$**: Alphabet
- **$q_0$**: Initial state
- **$F$**: Accepting state들의 집합
- **$\Delta$**: Transition **relation**

$$\Delta: Q \times \Sigma \to \mathcal{P}(Q)$$

DFA의 transition function $\delta: Q \times \Sigma \to Q$는 항상 정확히 **하나의** 다음 상태를 반환한다. 반면 NFA의 $\Delta$는 가능한 다음 상태들의 **집합**을 반환한다.

예를 들어 $\Delta(q, a) = \{r, s\}$이면, 상태 $q$에서 $a$를 읽었을 때 $r$로도, $s$로도 전이할 수 있다. 만약 $\Delta(q, a) = \emptyset$이면 해당 경로는 막힌다(dead end).

---

## NFA의 Accept 조건

NFA는 같은 입력에 대해 선택 가능한 경로가 여러 개 존재한다. **하나의 경로라도 accepting state에서 종료되면 accept** 한다. 모든 경로가 accepting state에서 끝나지 않아야만 reject다.

이 성질 때문에 NFA를 시뮬레이션하면 마치 "정답 경로를 미리 알고" 이동하는 것처럼 보이기도 한다. accept하는 경로가 단 하나라도 있으면 되므로, 그 경로만 따라가면 되기 때문이다. 실제 시뮬레이션에서는 가능한 모든 경로를 동시에 탐색하여 하나라도 accept하는지 확인한다.

---

## NFA와 DFA의 관계: Powerset Construction

NFA는 직접 구현하기보다 **이론적 도구** 로서 유용하다. DFA보다 설계가 간결하고 직관적이기 때문에, 복잡한 언어를 NFA로 먼저 설계한 뒤 DFA로 변환하는 방식을 사용한다.

모든 NFA는 **Powerset Construction(부분집합 구성법)**을 통해 동등한 DFA로 변환할 수 있다. NFA의 state 집합을 $Q$라 하면, 변환된 DFA의 각 state는 $Q$의 부분집합 $\mathcal{P}(Q)$의 원소가 된다.

아래는 4개의 state를 가진 NFA의 예시다.

![NFA 예시](/images/nfa/nfa-example.png)

이 NFA를 DFA로 변환하면 최대 $2^4 = 16$개의 state가 필요하다.

> 실제로는 도달 불가능한 state가 있어 16개보다 적을 수 있지만, 최악의 경우 상태 수는 지수적($2^n$)으로 증가한다.

### 변환 예시

NFA가 state 1과 3에 **동시에** 있는 상황을 DFA의 state $\{1, 3\}$으로 표현한다.

**입력 1이 들어올 경우:**

- state 1에서 1 → $\{1, 2\}$
- state 3에서 1 → $\{4\}$
- 합집합: 다음 DFA state $= \{1, 2, 4\}$

**입력 0이 들어올 경우:**

- state 1에서 0 → $\{1\}$
- state 3에서 0 → $\emptyset$
- 합집합: 다음 DFA state $= \{1\}$

변환된 DFA는 다음과 같이 구성된다.

| 항목 | 값 |
|---|---|
| Initial state | $\{1\}$ (NFA의 initial state만 포함) |
| Accepting states | NFA의 accepting state(state 4)를 원소로 포함하는 모든 부분집합 |

$$\{4\},\ \{1,4\},\ \{2,4\},\ \{3,4\},\ \{1,2,4\},\ \ldots$$

---

## 결론: Class NFA = Class DFA

모든 NFA는 Powerset Construction으로 동등한 DFA로 변환할 수 있다. 따라서 NFA가 accept하는 모든 언어는 DFA도 accept할 수 있고, 그 역도 성립한다.

$$\text{Class NFA} = \text{Class DFA}$$

NFA는 DFA보다 설계가 간결하고 직관적이지만, 두 모델이 인식할 수 있는 **언어의 집합(Regular Languages)은 완전히 동일하다.** DFA로 풀 수 없는 문제(예: $L_5 = \{0^i1^i\}$)는 NFA로도 풀 수 없다.
