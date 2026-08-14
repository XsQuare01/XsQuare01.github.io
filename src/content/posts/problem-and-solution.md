---
title: "Problem & Solution — Complexity Theory의 수학적 정의"
date: 2026-03-19
description: "Complexity Theory에서 '문제'와 '풀이'는 어떻게 정의될까? Decision Problem, Language, 튜링 머신을 통해 풀리지 않는 문제가 왜 대부분인지를 살펴본다."
tags: ["Mathematics", "Complexity Theory"]
category: theory
difficulty: 초급
---

> Complexity Theory에서 '문제'와 '풀이'는 우리가 일상적으로 쓰는 의미와 다르게 정의된다. 이 글에서는 그 수학적 정의를 따라가며, 풀 수 있는 문제보다 풀 수 없는 문제가 압도적으로 많다는 사실을 확인한다.

<div class="callout">
<div class="callout-title">선수지식</div>
<ul>
<li>집합의 크기(Cardinality) — 가산/불가산 무한</li>
<li>자연수 $\mathbb{N}$ 와 실수 $\mathbb{R}$ 의 크기 차이</li>
</ul>
</div>

<div class="callout callout-key">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>Complexity Theory에서는 문제를 <strong>Language</strong>로 정의한다.</li>
<li>Problem의 수는 <strong>불가산 무한 $|\mathbb{R}|$</strong>, Solution의 수는 <strong>가산 무한 $|\mathbb{N}|$</strong>이다.</li>
<li>따라서 <strong>풀 수 없는 문제가 대부분</strong>이다.</li>
</ul>
</div>

---

## Decision Problem

**답이 yes 또는 no인 문제** 를 Decision Problem이라 한다.

Complexity Theory는 **주로** Decision Problem을 연구한다. 이유는 두 가지다.

1. 출력이 yes/no로 단순해 다루기 쉽다.
2. 자연스럽게 등장하는 탐색·최적화 문제 상당수가 대응하는 Decision Problem과 다항 시간 관계를 갖는다. 판정판을 풀 수 있으면 원래 문제도 풀 수 있고, 그 반대도 성립한다.

두 번째 이유가 직관적으로 와 닿지 않을 수 있다. Shortest Path 문제를 예시로 살펴보자.

<div class="example-label">Example</div>

### Shortest Path 예시

다음 세 가지 문제를 생각해보자.

| 문제 유형 | 입력 | 출력 |
|---|---|---|
| 경로 문제 | Graph G, Start S, End E | 최단 경로 P |
| 길이 문제 | Graph G, Start S, End E | 최단 거리 L |
| Decision 문제 | Graph G, Start S, End E, 임계값 L | 길이 $L$ **이하** 인 경로가 있는가 (yes / no) |

Decision 문제를 "길이가 정확히 $L$인 경로가 있는가"로 두면 아래 논증이 통하지 않는다. 아래가 기대는 것은 **$L$이 커질수록 답이 no에서 yes로 한 번만 바뀐다**는 단조성이고, 그것을 주는 것이 "이하"라는 부등호다.

![Decision Problem 환원 체인. 왼쪽부터 G·S·E·L을 받아 길이 L 이하 경로의 존재를 yes/no로 답하는 판정 문제, G·S·E를 받아 최단 거리 L을 내놓는 길이 문제, 최단 경로 P를 내놓는 경로 문제가 놓이고, 판정에서 길이로는 이진 탐색이, 길이에서 경로로는 간선 제거가 다리를 놓는다](/images/problem-and-solution/problem-transform.svg)

<div class="callout callout-simple">
<div class="callout-title">아래 논증이 서는 전제</div>

가중치는 **비음수 정수**이고, $S \neq E$이며 $S$에서 $E$로 가는 경로가 **존재**한다고 두자. 세 조건이 각각 하는 일이 있다. 비음수여야 "모든 간선 가중치의 합"이 상한이 되고, 정수여야 이진 탐색이 유한 번에 끝나며, 경로가 있어야 답이 정의된다. 실수 가중치라면 원하는 정밀도를 따로 정하고 탐색 구간을 그에 맞춰야 하고, 음수 가중치라면 최단 단순 경로 문제 자체가 어려워져 이 이야기의 범위를 벗어난다.

</div>

**Decision으로 길이를 구할 수 있을까?**

Binary Search로 가능하다. 답이 되는 $L$은 $0$ 이상, 모든 간선 가중치의 합 $W$ 이하다. 이 구간에서 중간값 $m$을 잡아 "길이 $m$ 이하인 경로가 있는가"를 묻고, yes면 위 절반을 버리고 no면 아래 절반을 버린다. 가중치가 정수이므로 구간이 한 점으로 좁혀지고, 그 값이 최단 거리 $L$이다.

호출 횟수는 $O(\log W)$다. 가중치가 2진수로 적혀 들어오므로 $\log W$는 입력 길이에 대한 다항식이고, 따라서 이 변환은 다항 시간에 끝난다.

**길이로 경로를 구할 수 있을까?**

간선을 하나씩 지워 보면 된다.

1. 아직 검사하지 않은 간선(edge) 하나를 제거한 그래프 $G'$에서 최단 거리 $L'$을 구한다.
2. $L' > L$이면 그 간선 없이는 거리를 유지할 수 없다는 뜻이므로 복원한다.
3. $L' = L$이면 그 간선 없이도 거리가 유지되므로 그대로 제거한다.
4. 모든 간선을 한 번씩 검사하면 최단 경로 $P$ 하나만 남는다.

4가 성립하는 이유는 이렇다. 매 단계에서 최단 거리가 $L$로 유지되므로, 끝난 그래프에도 길이 $L$인 경로 $P$가 남아 있다. 만약 $P$ 위에 없는 간선 $e$가 끝까지 살아남았다면, $e$를 검사하던 시점의 그래프는 지금보다 컸으니 $P$를 이미 품고 있었고, $e$를 빼도 $P$가 그대로 있어 $L' = L$이 나온다. 그러면 $e$는 그때 제거되었어야 한다. 모순이므로 살아남은 간선은 모두 $P$ 위에 있다.

이 절차는 최단 거리 계산을 간선 수만큼 부른다. 그 각각이 다시 이진 탐색으로 판정 문제를 $O(\log W)$번 부르므로, 전체는 판정 문제 호출 횟수의 다항식이다.

<div class="callout">
<div class="callout-title">이 예시가 보인 것과 보이지 않은 것</div>

<p><strong>보인 것.</strong> 최단 경로 문제는 자기 자신의 판정판으로 되돌려 풀 수 있다. 이런 성질을 <strong>자기 환원성(self-reducibility)</strong> 이라 하고, 자연스럽게 등장하는 탐색·최적화 문제 상당수가 이 성질을 갖는다. 그래서 판정 문제만 연구해도 잃는 것이 크지 않다.</p>

<p><strong>보이지 않은 것.</strong> "모든 문제가 판정 문제로 환원된다"는 명제는 여기서 따라 나오지 않는다. 위 논증은 최단 경로라는 특정 문제의 구조 — 임계값에 대한 단조성, 간선을 지워도 문제가 같은 꼴로 남는다는 점, 가중치가 정수라는 인코딩 조건 — 을 하나씩 썼다. 다른 문제에서는 이 구조가 없을 수 있다. 판정 문제 중심의 연구는 증명된 정리가 아니라 <strong>연구 대상을 고르는 방식</strong>이다.</p>

</div>

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

$$
\text{Language} = \text{Problem}
$$

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

$$
\Sigma^* = \{(\lambda)_0,\ (a, b, c)_1,\ aa,\ ab,\ ac,\ \ldots\}
$$

길이에 따라 자연수 번호를 붙일 수 있으므로, $|\Sigma^*| = |\mathbb{N}|$ — 가산 무한이다.

### Problem의 수: $|2^{\Sigma^*}|$

모든 Problem은 $\Sigma^*$의 부분집합이므로, 가능한 문제의 집합은 $2^{\Sigma^*}$이다.

$$
|2^{\Sigma^*}| = |\mathbb{R}|
$$

<div class="callout callout-key">
<div class="callout-title">핵심 크기 비교</div>
<ul>
<li>String의 수: $|\Sigma^*| = |\mathbb{N}|$ — 가산 무한</li>
<li>Problem의 수: $|2^{\Sigma^*}| = |\mathbb{R}|$ — <strong>불가산 무한</strong></li>
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

### Church-Turing 논제

> **직관적인 의미에서 "기계적인 절차로 계산 가능한" 함수는 모두 튜링 머신으로 계산할 수 있다.**

논제(thesis)라고 부르는 것은 이것이 정리가 아니기 때문이다. 등식의 한쪽인 "튜링 머신으로 계산 가능"은 수학적으로 정의되어 있지만, 다른 쪽인 "기계적인 절차로 계산 가능"은 직관에 기댄 말이라 증명의 대상이 되지 못한다. 증명 대신 근거로 삼는 것은, 사람들이 서로 다른 동기에서 제안한 계산 모델 — 람다 계산, 귀납적 함수, 레지스터 기계 등 — 이 하나같이 튜링 머신과 같은 함수 집합을 계산한다는 사실이다.

여기서 흔한 오해 하나를 짚어 두자. 이 논제는 **어떤 물리적 기계도 튜링 머신을 넘지 못한다**는 주장이 아니다. 그것은 물리학이 걸린 별개의 주장이고, 논제 자체는 "계산 가능"이라는 말의 뜻을 튜링 머신으로 고정하자는 제안에 가깝다.

### 튜링 머신의 구조

- **Tape**: 읽고 쓰는 저장 공간. 한쪽 방향으로 무한하다.
  - 최대한 단순하게 설계하기 위해 한쪽 방향만 무한하게 설정했다.
- **Cell**: Tape의 한 칸. 어떤 Symbol도 저장할 수 있다.
- **Read/Write Head**: 현재 읽고 있는 Cell을 가리킨다.
- **Finite Control (Head Control)**: 규칙(Rule)을 담고 있는 제어 장치. 컴퓨터의 CPU에 해당한다.
  - **State**: Control의 현재 상태
  - **Rule**: 규칙 하나는 다음과 같은 꼴이다.

$$
(q,\ x_1) \to (x_2,\ D,\ r), \qquad D \in \{L,\ R\}
$$

현재 State가 $q$이고 Head가 $x_1$을 가리키면, $x_2$를 쓰고 $D$가 가리키는 쪽(왼쪽 $L$ 또는 오른쪽 $R$)으로 한 칸 이동한 뒤 State를 $r$로 바꾼다.

이런 규칙 **하나**가 하는 일은 한 걸음뿐이다. 계산을 수행하는 것은 규칙들의 **유한한 집합**이며, 그 집합이 곧 이 튜링 머신의 프로그램이다. 상태와 읽은 심볼의 조합마다 규칙이 하나씩 정해져 있고, 머신은 멈춤 상태에 이를 때까지 해당하는 규칙을 찾아 적용하기를 반복한다.

규칙의 개수도, 상태의 개수도, 알파벳의 크기도 모두 유한하다. 이 유한성이 다음 절에서 "튜링 머신의 수는 가산 무한"이라는 결론으로 이어진다.

**Church-Turing 논제를 받아들이면, 튜링 머신이 풀 수 없는 문제는 기계적인 절차로도 풀 수 없다. 이 글은 그 위에서 Solution을 튜링 머신으로 정의한다.**

---

## Solution은 몇 개나 존재할까?

Solution = 튜링 머신이다.

튜링 머신의 State 집합($Q$)과 Transition function은 모두 **유한한 문자열** 로 표현 가능해야 한다. 따라서 가능한 튜링 머신의 수, 즉 **Solution의 수는 가산 무한($|\mathbb{N}|$)** 이다.

앞서 문제의 수는 불가산 무한($|\mathbb{R}|$)이었다.

![Problems와 Solutions의 크기 비교. 왼쪽은 모든 Decision Problem의 집합으로 불가산 무한이라 셀 수 없이 많고, 오른쪽은 튜링 머신의 집합으로 크기가 자연수 전체와 같은 가산 무한이다. 두 집합 사이에 훨씬 크다는 부등호가 놓인다](/images/problem-and-solution/problem-vs-solution.svg)

<div class="callout callout-key">
<div class="callout-title">최종 결론</div>
<ul>
<li>Problems: $|2^{\Sigma^*}| = |\mathbb{R}|$ — 불가산 무한</li>
<li>Solutions: $|\mathbb{N}|$ — 가산 무한</li>
<li><strong>풀 수 없는 문제가 압도적으로 많다.</strong> 풀 수 있는 문제는 전체 중 극히 일부에 불과하다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>DFA — 결정론적 유한 오토마타</strong> — 계산 이론에서 가장 단순한 계산 모델인 DFA의 구조와 동작 원리를 살펴본다. Pumping Lemma를 통해 DFA로도 풀 수 없는 문제가 존재함을 증명한다.</p>
</div>
