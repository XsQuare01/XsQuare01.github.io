---
title: "NP-Complete — NP에서 가장 어려운 문제들"
date: 2026-03-23T10:34:21
description: "NP 내에서 가장 어려운 문제들의 집합인 NP-Complete를 정의하고, Reduction(귀착) 개념과 Cook의 정리를 통해 SAT가 최초의 NP-Complete 문제임을 증명하는 과정을 살펴본다."
tags: ["Computer Science", "Complexity Theory"]
category: cryptography
difficulty: 심화
---

> NP에 속하면서도 NP의 모든 문제를 자신으로 귀착시킬 수 있는 문제가 존재한다. 이런 문제를 NP-Complete라 부른다. 1971년 Stephen Cook이 SAT(Boolean Satisfiability) 문제가 NP-Complete임을 최초로 증명했다. 이 발견은 수천 개의 NP-Complete 문제 발견으로 이어졌다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>NP-Complete</strong>: NP에 속하면서, NP의 모든 문제가 다항식 시간에 귀착되는 가장 어려운 문제들의 집합</li>
<li><strong>Reduction (귀착)</strong>: 문제 A를 문제 B로 변환하는 방법 — A ≤ₚ B이면 B가 A만큼 어렵다</li>
<li><strong>SAT</strong>: 논리식을 참으로 만드는 변수 배정이 존재하는지 판별하는 문제</li>
<li><strong>Cook의 정리</strong>: 모든 NP 문제는 SAT로 다항식 시간에 귀착된다 — SAT는 최초의 NP-Complete 문제</li>
<li><strong>NP-Hard</strong>: 모든 NP 문제가 귀착되지만, NP에 속하지 않을 수 있는 문제들</li>
<li><strong>Co-NP</strong>: "No"에 대한 증명서가 존재하는 언어 클래스 — L ∈ Co-NP ⟺ Lᶜ ∈ NP</li>
</ul>
</div>

앞선 글에서 NP를 두 가지 동치 정의(NTM 기반, 검증자 기반)로 살펴봤다. 이 글에서는 NP 안에서도 특별한 위치를 차지하는 NP-Complete를 다룬다. NP-Complete는 "NP 문제 중 가장 어려운 것들"이다. 하나의 NP-Complete 문제를 다항식 시간에 풀 수 있다면, 모든 NP 문제를 다항식 시간에 풀 수 있다 — 즉 P = NP가 성립한다.

---

## NP-Complete의 정의

![NP 복잡도 클래스 계층](/images/np-complete/complexity-np.svg)

<div class="callout callout-key">
<div class="callout-title">NP-Complete의 정의</div>
<p>문제 L이 NP-Complete이려면 다음 두 조건을 모두 만족해야 한다.</p>
<ol>
<li><strong>L ∈ NP</strong>: L은 NP에 속한다.</li>
<li><strong>NP-hardness</strong>: NP의 모든 문제 A에 대해 A ≤ₚ L — 다항식 시간 귀착이 존재한다.</li>
</ol>
</div>

두 번째 조건만 만족하고 NP에 속하지 않을 수 있는 문제들을 **NP-Hard** 라 한다. 따라서 NP-Complete = NP ∩ NP-Hard다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>NP-Complete는 "NP 문제들 중 가장 어려운 보스 문제"다. 이 보스를 하나라도 빠르게 풀 수 있다면, NP의 모든 문제를 빠르게 풀 수 있다. 반대로 말하면, 수천 개의 NP-Complete 문제 중 단 하나도 빠른 풀이법이 발견되지 않았다는 사실이 P != NP를 강력하게 시사한다.</p>
</div>

---

## Reduction (귀착)

![다항식 시간 귀착 과정](/images/np-complete/reduction.svg)

**Reduction(귀착)** 은 문제의 난이도를 비교하는 핵심 도구다. 문제 $A$를 문제 $B$로 **다항식 시간 귀착** 한다는 것은, 다항식 시간에 계산 가능한 변환 함수 $f$가 존재해 다음이 성립하는 것이다.

$$A \leq_p B \iff \exists f \text{ (다항식 시간 계산 가능) s.t. } x \in A \Leftrightarrow f(x) \in B$$

귀착 과정은 다음 세 단계로 이루어진다.

1. 문제 $A$의 입력 $x$를 문제 $B$의 입력 $f(x)$로 **변환(Transform)** 한다.
2. $B$의 알고리즘으로 $f(x)$에 대한 답을 구한다.
3. 그 답이 $A$에 대한 답이 된다.

### 귀착과 난이도의 관계

$A \leq_p B$가 성립하면 **"$B$는 $A$만큼 어렵다"** — $B$를 풀 수 있으면 $A$도 풀 수 있다.

| 귀착 방향 | 의미 |
|---|---|
| $A \leq_p B$ | $B$의 난이도 $\geq$ $A$의 난이도 |
| $A \leq_p B$ 이고 $B \leq_p A$ | $A$와 $B$의 난이도가 동일 |

> **왜 다항식 시간으로 제한하는가?** 변환에 너무 많은 계산을 허용하면, 변환 과정에서 문제를 거의 풀어버리게 되어 난이도 비교가 의미 없어진다. NP에서 "다항식 시간 귀착"은 원래 난이도를 왜곡하지 않는 변환을 의미한다.

---

## SAT (Boolean Satisfiability)

SAT는 주어진 Boolean formula를 참(True)으로 만드는 변수 배정이 존재하는지 판별하는 문제다.

**Satisfiable 예시:**

$$\varphi = (p \lor q) \land \lnot p$$

$p = \text{False},\ q = \text{True}$로 설정하면 $\varphi$가 참 → **Satisfiable**

**Unsatisfiable 예시:**

$$\varphi = p \land \lnot p$$

어떤 변수 배정으로도 참이 될 수 없음 → **Unsatisfiable**

SAT는 변수가 $n$개일 때 $2^n$가지 배정을 검사해야 하기 때문에, 결정론적 다항식 시간 알고리즘은 현재까지 알려져 있지 않다.

---

## Cook의 정리: SAT ∈ NP-Complete

SAT가 NP-Complete임을 증명하려면 두 조건을 모두 확인해야 한다.

### 1. SAT ∈ NP

NTM으로 모든 변수 배정을 비결정론적으로 탐색한다. 어떤 경로에서든 "Yes"인 배정을 찾으면 accept하므로, SAT ∈ NP.

### 2. 모든 NP 문제는 SAT로 귀착된다

이것이 Cook의 핵심 증명이다. 임의의 NP 문제 $L$에 대해 $L \leq_p \text{SAT}$를 보인다.

<div class="callout">
<div class="callout-title">증명 구조: NTM → 회로 → 논리식</div>
<p>모든 논리 회로는 Boolean formula로 표현할 수 있다. NTM을 회로로 변환할 수 있다면, 그 회로를 SAT 인스턴스로 바꿀 수 있다.</p>
</div>

**Step 1: DTM을 논리 회로로**

DTM의 실행을 시간 $t = 0, 1, 2, \ldots, T$에 따라 테이프 내용을 기록하면, 시간의 흐름이 회로의 층(layer)이 된다. 각 셀은 다음 정보를 인코딩한다.

| 셀 정보 | 역할 |
|---|---|
| Head 유무 | 이 위치에 헤드가 있는가 |
| State | DTM의 현재 상태 |
| Symbol | 테이프에 기록된 심볼 |

헤드가 위치한 셀만 다음 시간 단계에서 변경된다. 이 규칙을 게이트 회로로 표현하면, DTM 실행 전체를 Boolean 회로로 시뮬레이션할 수 있다.

**Step 2: NTM을 회로로 — Choice 변수 추가**

NP의 임의의 문제 $L$을 푸는 NTM $M$이 있다고 하자. NTM은 각 단계에서 여러 선택지가 존재한다. 이 선택을 **Choice 변수** 로 인코딩한다.

$$\text{Choice}_t \in \{0, 1\} : \text{시간 } t \text{에서 어느 전이를 선택하는가}$$

| 구분 | DTM | NTM |
|---|---|---|
| 같은 입력 $x$에 대한 테이프 내용 | 결정적 (상수) | 결정적 (상수) |
| 전이 선택 | 없음 | Choice 변수 (가변) |

같은 입력 $x$라도 Choice 변수 값에 따라 NTM의 실행 경로가 달라진다. 입력 $x$가 NTM에서 accept되는 경로가 존재한다면, 그 경로에 대응하는 Choice 값이 존재한다.

**Step 3: SAT로 변환**

$$\text{Choice 변수} \longleftrightarrow \text{SAT의 변수}$$
$$\text{NTM 회로식} \longleftrightarrow \text{SAT의 논리식}$$

입력 $x$가 $L$에 속하면 해당 Choice 변수 값이 논리식을 참으로 만들고, 속하지 않으면 어떤 값으로도 참이 되지 않는다.

$$x \in L \iff \text{(NTM 회로에 대한 SAT 인스턴스가 Satisfiable)}$$

임의의 NP 문제 $L$을 SAT로 다항식 시간에 귀착할 수 있다. **따라서 SAT ∈ NP-Complete.**

<div class="callout callout-key">
<div class="callout-title">Cook의 정리의 의미</div>
<p>SAT가 NP-Complete임이 증명된 이후, 다른 문제의 NP-Complete 여부를 증명하는 방법이 생겼다.</p>
<p><strong>어떤 문제 A가 NP-Complete임을 보이려면:</strong></p>
<ol>
<li>A ∈ NP임을 보인다.</li>
<li>기존에 알려진 NP-Complete 문제 B에서 B ≤ₚ A임을 보인다.</li>
</ol>
<p>이 방식으로 SAT → 3-SAT → Vertex Cover → Independent Set → … 수천 개의 NP-Complete 문제가 연쇄적으로 발견되었다.</p>
</div>

---

## NP-Hard

NP-Hard는 두 번째 조건(NP-hardness)만 만족하는 더 넓은 개념이다. NP-Complete와 달리, NP에 속하지 않을 수 있다.

| | NP 포함 | NP-hardness | 예시 |
|---|---|---|---|
| NP-Complete | ✓ | ✓ | SAT, 3-SAT, Vertex Cover |
| NP-Hard (NP 외부) | ✗ | ✓ | Halting Problem, TSP 최적화 |

**Function Problem** 도 NP-Hard로 분류된다. 예를 들어, 그래프의 최단 경로 길이를 구하는 문제는 Yes/No 형식이 아니지만, 이를 Decision Problem으로 변환하면 NP-Complete다 — 따라서 원래 Function Problem은 NP-Hard에 속한다.

---

## Co-NP

Co-NP는 NP의 보완(complement) 개념이다.

$$L \in \text{Co-NP} \iff L^c \in \text{NP}$$

NP가 **"Yes"에 대한 짧은 증명서** 가 존재하는 언어라면, Co-NP는 **"No"에 대한 짧은 증명서** 가 존재하는 언어다.

$\text{NP} \cap \text{Co-NP}$에 속하는 문제는 "Yes"와 "No" 모두에 대한 효율적인 증명이 존재한다. 대표적인 예로 **소인수분해(Factoring)** 가 있다.

> NP = Co-NP인지는 아직 미해결 문제다. P = NP가 성립하면 NP = Co-NP도 자동으로 성립하지만, 역은 성립하지 않는다.

---

## 결론

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>NP-Complete = NP ∩ NP-Hard: NP에 속하면서 모든 NP 문제를 귀착시킬 수 있는 가장 어려운 문제들</li>
<li>Cook의 정리: SAT는 최초의 NP-Complete 문제. 임의의 NTM 실행을 SAT 인스턴스로 변환할 수 있다.</li>
<li>어떤 NP-Complete 문제 하나를 다항식 시간에 풀면, 모든 NP 문제가 다항식 시간에 풀린다 — P = NP 성립</li>
<li>P ≠ NP로 추정되지만, 컴퓨터 과학 최대의 미해결 문제로 남아 있다.</li>
</ul>
</div>
