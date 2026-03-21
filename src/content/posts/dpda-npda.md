---
title: "DPDA와 NPDA — 스택을 가진 오토마타"
date: 2026-03-21T09:00:00
description: "DFA에 스택을 추가한 DPDA가 해결할 수 있는 문제와 없는 문제를 살펴보고, NPDA와의 계산 능력 차이를 분석한다. 스택 2개로 튜링 머신을 시뮬레이션하는 원리까지 다룬다."
tags: ["Computer Science", "Complexity Theory"]
category: cryptography
---

> DFA는 상태만 기억한다. 스택을 하나 추가하면 어디까지 가능해질까? 그리고 비결정론적으로 동작하면 얼마나 더 강력해질까?

DFA에 스택(Stack)을 추가한 계산 모델을 **PDA(Pushdown Automata)** 라 부른다. 결정론적으로 동작하면 DPDA, 비결정론적으로 동작하면 NPDA가 된다. 스택이 생기면 DFA로는 불가능했던 문제들을 해결할 수 있지만, DPDA만으로는 여전히 해결하지 못하는 문제가 존재한다.

![계산 모델별 메모리 구조](/images/dpda/model-expansion.svg)

---

## DPDA

**DPDA(Deterministic Pushdown Automata)** 는 DFA에 스택을 추가한 계산 모델이다. 상태 전이뿐 아니라 스택에 대한 push/pop 연산도 수행할 수 있다.

### DPDA로 L5 해결하기

DFA로는 풀 수 없었던 $L_5 = \{0^i 1^i \mid i \ge 0\}$을 DPDA는 스택을 활용해 해결할 수 있다.

**동작 방식:**

1. 입력이 $0$이면 스택에 push하고 계속 진행한다.
   - 이후 $1$이 들어오면 스택에서 pop하고 계속 진행한다.
     - 이때 또 $0$이 들어오면 **Reject** 한다. ($0^i 1^j 0$ 형태이므로)
     - $1$이 들어왔지만 스택이 비어있으면 **Reject** 한다. (1의 개수가 0의 개수를 초과)
     - 모든 입력이 끝났을 때,
       - 스택이 비어있으면 **Accept** 한다.
       - 스택이 비어있지 않으면 **Reject** 한다. (0이 1보다 많음)
2. 첫 입력부터 $1$이 들어오면 **Reject** 한다.

스택 덕분에 "지금까지 $0$이 몇 개 나왔는지"를 기억할 수 있고, 이를 통해 $0$과 $1$의 개수를 비교할 수 있다.

![L5 스택 처리 과정](/images/dpda/l5-stack-trace.svg)

---

## DPDA의 한계: L7

DPDA도 모든 문제를 해결할 수는 없다. 대표적인 예시가 다음 언어다.

$$L_7 = \{x \mid x = yy^R,\ y \in \{a, b\}^*\}$$

$y^R$은 $y$를 뒤집은 문자열이다. 예를 들어 abba는 $y = \text{ab}$, $y^R = \text{ba}$이므로 $L_7$에 속한다.

### DPDA가 L7을 풀 수 없는 이유

DPDA가 $L_7$을 accept한다고 가정하자.

그러면 DPDA는 abba를 accept해야 한다 ($y = \text{ab}$). DPDA가 abba를 처리하다 어떤 시점에 $y$의 끝을 인식하고, 이후 $y^R$과 스택의 내용을 매칭하여 스택이 빈 상태로 도달한다.

이제 abbaabba ($y = \text{abba}$, $y^R = \text{abba}$)를 생각해보자. DPDA는 앞의 abba를 처리할 때 이미 스택이 빈 상태가 된다. 왜냐하면 현재 상황에서 DPDA는 이 abba가 짧은 입력 abba의 전부인지, 긴 입력 abbaabba의 앞부분인지 구분할 수 없기 때문이다.

더 나아가 abaababba를 생각해보자. 이를 abaaba | abba로 나누면, abaaba의 역은 abaaba이므로 abba와 다르다. 즉, abaababba ∉ $L_7$이다. 그러나 DPDA가 abaaba를 처리한 시점에 스택이 빈 상태라면, 이후 어떤 문자열이 오더라도 accept해버리는 상황이 발생한다. abbaabba에서 abba를 처리했을 때와 같은 상태이기 때문이다.

이처럼 DPDA는 $y$와 $y^R$의 경계 지점, 즉 **전환점(midpoint)** 을 결정론적으로 찾을 수 없기 때문에 $L_7$을 올바르게 accept하지 못한다.

---

## NPDA

**NPDA(Non-deterministic Pushdown Automata)** 는 NFA처럼 하나의 상태에서 여러 선택지를 동시에 탐색할 수 있는 PDA다.

현실에서 실제로 구현하는 기계는 아니기 때문에 직관적으로 이해하기 어려울 수 있다. NPDA는 이론적 계산 능력을 분석하기 위한 모델로, **하나의 경로라도 accept에 도달하면 accept** 한다는 점은 NFA와 동일하다.

---

## DPDA vs NPDA: 계산 능력은 다르다

| | DPDA | NPDA |
|---|---|---|
| 비결정성 | 결정론적 | 비결정론적 |
| 인식 가능한 언어 | Deterministic CFL | Context-Free Languages |
| 대표 예시 | L5: $0^i 1^i$ | L5, L7: $yy^R$ |
| 풀 수 없는 언어 | L7: $yy^R$ | — |
| 계산 능력 | DPDA ⊊ NPDA | — |

DFA와 NFA의 경우, 모든 DFA는 NFA의 특수한 경우이고 모든 NFA는 Powerset Construction을 통해 DFA로 변환할 수 있다. 그래서 둘의 계산 능력은 동일했다.

그러나 **DPDA와 NPDA의 계산 능력은 다르다.** 이는 $L_7$을 통해 확인할 수 있다.

- **DPDA는 $L_7$을 풀 수 없다.** $y$와 $y^R$의 전환점이 어디인지 결정론적으로 알 수 없기 때문이다.
- **NPDA는 $L_7$을 풀 수 있다.** 가능한 모든 전환점을 동시에 시도해, 그 중 하나라도 올바르게 매칭되면 accept하면 된다.

$$\text{Class DPDA} \subsetneq \text{Class NPDA}$$

---

<div class="section-label section-label-deep">심화</div>

## DPDA에 스택을 하나 더 추가하면?

DPDA는 DFA에 스택을 1개 추가한 모델이다. 그렇다면 스택을 1개 더 추가하면, 즉 스택 2개짜리 DPDA는 얼마나 강력해질까?

아래의 언어들을 먼저 살펴보자. 여기서 $\mathtt{2}$는 구분자 역할을 하는 알파벳 심볼이다.

$$L_8 = \{x \mid x = y \mathtt{2} y^R \mathtt{2} y^R\}$$
$$L_9 = \{x \mid x = y \mathtt{2} y^R \mathtt{2} y^R \mathtt{2} y^R\}$$
$$L_{10} = \{x \mid x = yy^Ry^R\}$$
$$L_{11} = \{x \mid x = yy^Ry^Ry^R\}$$

이 언어들은 모두 스택 1개짜리 DPDA로는 해결할 수 없다. $y$를 스택에 push해 첫 번째 $y^R$과 매칭한 뒤에는 스택이 비어버리기 때문에, 두 번째 $y^R$을 매칭할 때 필요한 $y$의 정보를 이미 잃어버린 상태다.

### 스택 2개 = 튜링 머신

흥미롭게도, **스택이 2개가 되면 튜링 머신을 시뮬레이션할 수 있다.**

원리는 다음과 같다:

- **스택 1번**: 튜링 머신 테이프의 현재 위치 왼쪽
- **스택 2번**: 튜링 머신 테이프의 현재 위치 오른쪽

테이프 헤드를 왼쪽으로 이동하고 싶으면 스택 1번에서 pop해 스택 2번에 push하고, 오른쪽으로 이동하고 싶으면 반대로 하면 된다. 이로써 두 스택이 튜링 머신의 테이프 역할을 완전히 대신할 수 있다.

따라서 위의 $L_8$–$L_{11}$은 튜링 머신으로 풀 수 있는 문제이므로, 스택 2개짜리 DPDA로도 해결 가능하다.

> 어떤 문제가 튜링 머신으로 풀 수 있는지 확인하는 가장 직관적인 방법은, 프로그래밍 언어로 해당 문제를 풀 수 있는지 생각해보는 것이다.

---

## 결론

| 모델 | 설명 | 해결 가능한 언어 |
|---|---|---|
| DFA | 상태만 기억 | Regular Languages |
| DPDA | 상태 + 스택 1개 (결정론적) | Deterministic Context-Free Languages |
| NPDA | 상태 + 스택 1개 (비결정론적) | Context-Free Languages |
| 스택 2개 DPDA | 상태 + 스택 2개 | Recursively Enumerable (튜링 머신과 동등) |

스택 하나의 추가가 계산 능력을 극적으로 확장시키고, 비결정론의 도입이 결정론적 모델로는 불가능한 언어를 해결 가능하게 만든다. 계산 이론의 핵심은 이처럼 "모델의 제약을 조금씩 풀었을 때 무엇이 가능해지는가"를 탐구하는 데 있다.

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Turing Machine — 계산의 극한</strong> — 스택 2개는 튜링 머신과 동등하다. 현대 컴퓨터의 이론적 모델인 튜링 머신의 구조와 Universal Turing Machine의 의미, 그리고 DTM과 NTM의 계산 능력이 동일함을 탐구한다.</p>
</div>
