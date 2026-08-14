---
title: "Interesting Number Paradox"
date: 2026-03-16
description: "수학적 증명에서 '정의(definition)'의 엄밀함이 왜 중요한지를 보여주는 패러독스. 암호학 Complexity Theory 도입부."
tags: ["Cryptography", "Complexity Theory", "Mathematics"]
category: theory
difficulty: 입문
---

<div class="callout callout-key">
<div class="callout-title">생각해볼 질문</div>
재미없는 자연수 중 가장 작은 수는 존재할까?<br/>
그리고 '재미있다'는 걸 정확히 정의하지 않으면, 증명은 어떻게 될까?
</div>

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- '모든 자연수는 흥미로운가?' 패러독스의 귀류법 논증
- 이 논증이 왜 엄밀한 수학적 증명이 아닌 반문(counter-argument)에 그치는가
- '흥미롭다'가 비형식적 개념일 때 증명이 무너지는 이유
- OEIS를 통한 객관화 시도와 그 한계
- **정의의 엄밀함**이 Complexity Theory와 암호학의 출발점인 이유

</div>

이 패러독스는 수학적 증명에서 **정의(definition)의 엄밀함이 왜 중요한지** 를 보여주는 예시다. Complexity Theory의 도입부에서 다루는 주제이며, 암호학에서도 수학적 엄밀성은 핵심 전제이기 때문에 이 개념을 먼저 짚고 넘어간다.

---

## 가정: 모든 자연수들은 '흥미로운가(Interesting)'?

- 1: $1^n = 1$
- 2: 가장 작은 소수
- 3: 가장 작은 홀수인 소수
- 4: 가장 작은 합성수
- 5: (가장 작은 소수) + (두번째로 작은 소수)
- 6: 완전수

이런 방법으로 모든 자연수를 표현할 수 있는가?

---

## 모순의 증명: 흥미롭지 않은 자연수가 존재한다고 가정 (귀류법)

![귀류법 전개 — 가정, 최소 원소 선택, 반전, 모순](/images/interesting-number-paradox/paradox-flow.svg)

1. $U:$ Uninteresting Number Set 이라고 할 때, 다음과 같이 표현할 수 있다.

$$
U \subseteq \mathbb{N} \quad ( U \ne \emptyset )
$$

2. 이때, $U$는 자연수를 원소로 갖는 집합이기 때문에, Least-number principle(= Well-ordering Principle)에 의해 가장 작은 원소 $x$가 존재한다.
   - **Least-number principle (Well-ordering Principle):** 공집합이 아닌 모든 자연수의 부분집합은 최소 원소가 존재한다.
     - 유리수에 대해서는 성립하지 않는다.
     - 다음과 같은 집합 $X$의 최소 원소는 정의할 수 없기 때문이다.

$$
X = \{x \in \mathbb{Q} \mid x > 1\}
$$

3. 이 최소 원소 $x$에 대해, '집합 $U$에서 가장 작은 원소'라는 '흥미로운' 점이 존재한다. 그러면 $x$는 흥미로운 수이므로 $U$에 속할 수 없는데, $x$는 $U$의 원소로 골랐다.

4. 따라서 모순이 발생하고, 가정이 무너진다.

$$
\therefore \text{ 귀류법에 의해, 모든 자연수는 흥미롭다.}
$$

<div class="callout">
<div class="callout-title">주의</div>
이 논증은 실제 수학적 정리가 아니다. '흥미롭다'가 엄밀하게 정의되지 않았기 때문에 성립하는 <strong>반문(counter-argument)</strong>일 뿐이다. 수학적 증명은 명확히 정의된 개념 위에서만 성립한다.
</div>

---

## '흥미롭다(Interesting)'의 정의가 모호하다

![직관적 정의 vs 수학적 정의](/images/interesting-number-paradox/definition-compare.svg)

- 흥미롭다(Interesting)는 것은 매우 주관적이다. 따라서, 듣는 사람에 따라서 '흥미롭다고' 느낄 수도 있고, 아닐 수도 있다.
- 사실, 위의 귀류법을 사용한 증명도 모호하다. 정확히는 '증명'이 아닌, '반문'이기에, 정확한 증명이라고 보기는 어렵다. 이는 '흥미롭다(Interesting)'가 수학적으로 엄밀하게 정의된 개념이 아닌, 비형식적(informal)인 개념이기 때문이다. **수학적 증명은 명확히 정의된 개념 위에서만 성립한다.**

---

## 추가) OEIS: On-line Encyclopedia of Integer Sequences

그렇다면, '흥미롭다'를 보다 객관적으로 정의하려는 시도를 해볼 수 있다. OEIS는 이러한 시도 중 하나의 기준이 될 수 있다.

- 온라인 정수열 사전으로, 수학·컴퓨터과학 등 다양한 분야의 '흥미로운 수열'들을 모아둔 데이터베이스다.
- 여기서 「흥미롭다」를 「OEIS의 어떤 수열에 나온다」로 바꿔 놓으면 어떻게 되는지 보자. 이렇게 두면 앞의 귀류법을 그대로 흉내 낼 수 있다. OEIS에 나오지 않는 수 가운데 가장 작은 수 $x$를 잡으면, 「OEIS에 나오지 않는 가장 작은 수」라는 성질 때문에 $x$가 흥미로워 보이고, 그러면 등재되어야 할 것 같다.
- **그런데 이것은 증명이 아니다.** 등재 여부는 편집자가 정하는 사회적 절차이지 수학적 술어가 아니다. 「흥미로워 보인다」에서 「등재된다」로 넘어가는 단계에 아무 근거가 없다. 또한 OEIS는 **수열**의 데이터베이스이지 개별 자연수의 목록이 아니어서, 「$x$가 OEIS에 있다」는 말부터 뜻이 하나로 정해지지 않는다.
- 그래서 이 시도가 보여 주는 것은 OEIS에 관한 어떤 정리가 아니라, **주관적인 「흥미롭다」를 등재 여부 같은 객관적 기준으로 갈아 끼워도 역설이 사라지지 않는다**는 사실이다. 기준을 바꾸면 모호함이 「흥미롭다」에서 「등재할 만한가」로 옮겨 갈 뿐이다.

> **한계:** OEIS는 개별 숫자가 아닌 수열(sequence) 단위로 관리된다. 따라서 "숫자 $n$이 흥미롭다"를 OEIS 등재 여부로 정의하는 것은 엄밀하지 않다. 특정 숫자는 여러 수열에 동시에 속할 수 있으며, OEIS에 없다고 해서 흥미롭지 않다고 단언할 수 없다.

---

<div class="callout callout-key">
<div class="callout-title">다음 글과의 연결</div>
<ul>
<li>이 글의 핵심은 <strong>정의가 모호하면 증명도 무너진다</strong>는 것이다.</li>
<li>Complexity Theory와 암호학은 이 교훈에서 출발한다 — 문제, 알고리즘, 안전성 모두 수학적으로 엄밀하게 정의되어야 한다.</li>
<li>다음 글에서는 집합의 크기(Cardinality) 개념을 통해 "풀 수 없는 문제가 압도적으로 많다"는 사실을 증명한다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Toss Coin over Telephone</strong> — 서로를 불신하는 두 사람이 전화로 공정한 동전 던지기를 할 수 있을까? 이차잉여 구조를 기반으로 한 암호학적 프로토콜로 합의에 이르는 방법을 살펴본다.</p>
</div>
