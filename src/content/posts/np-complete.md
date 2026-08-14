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
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li><strong>NP-Complete</strong>: NP에 속하면서, NP의 모든 문제가 다항식 시간에 귀착되는 가장 어려운 문제들의 집합</li>
<li><strong>Reduction (귀착)</strong>: 문제 $A$를 문제 $B$로 변환하는 방법 — $A \le_p B$이면 $B$가 $A$만큼 어렵다</li>
<li><strong>SAT</strong>: 논리식을 참으로 만드는 변수 배정이 존재하는지 판별하는 문제</li>
<li><strong>Cook의 정리</strong>: 모든 NP 문제는 SAT로 다항식 시간에 귀착된다 — SAT는 최초의 NP-Complete 문제</li>
<li><strong>NP-Hard</strong>: 모든 NP 문제가 귀착되지만, NP에 속하지 않을 수 있는 문제들</li>
<li><strong>Co-NP</strong>: "No"에 대한 증명서가 존재하는 언어 클래스 — $L \in \text{Co-NP} \iff L^c \in \text{NP}$</li>
</ul>
</div>

앞선 글에서 NP를 두 가지 동치 정의(NTM 기반, 검증자 기반)로 살펴봤다. 이 글에서는 NP 안에서도 특별한 위치를 차지하는 NP-Complete를 다룬다. NP-Complete는 "NP 문제 중 가장 어려운 것들"이다. 하나의 NP-Complete 문제를 다항식 시간에 풀 수 있다면, 모든 NP 문제를 다항식 시간에 풀 수 있다 — 즉 P = NP가 성립한다.

---

## NP-Complete의 정의

![NP 복잡도 클래스 계층. NP와 NP-Hard는 서로를 포함하지 않고 겹치기만 하며, 겹치는 부분이 NP-Complete다. SAT와 3-SAT, Hamiltonian Path가 그 안에 있다. P는 NP 안에 들어 있고 NP-Hard와는 만나지 않는다. Halting Problem과 TSP 최적화는 NP-Hard이면서 NP 밖에 있다](/images/np-complete/complexity-np.svg)

<div class="callout callout-key">
<div class="callout-title">NP-Complete의 정의</div>
<p>문제 $L$이 NP-Complete이려면 다음 두 조건을 모두 만족해야 한다.</p>
<ol>
<li><strong>$L \in \text{NP}$</strong>: $L$은 NP에 속한다.</li>
<li><strong>NP-hardness</strong>: NP의 모든 문제 $A$에 대해 $A \le_p L$ — 다항식 시간 귀착이 존재한다.</li>
</ol>
</div>

두 번째 조건만 만족하고 NP에 속하지 않을 수 있는 문제들을 **NP-Hard** 라 한다. 따라서 NP-Complete = NP ∩ NP-Hard다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>NP-Complete는 "NP 문제들 중 가장 어려운 보스 문제"다. 이 보스를 하나라도 빠르게 풀 수 있다면, NP의 모든 문제를 빠르게 풀 수 있다. 반대로 말하면, 수천 개의 NP-Complete 문제 중 단 하나도 빠른 풀이법이 발견되지 않았다는 사실이 $P \neq \text{NP}$를 강력하게 시사한다.</p>
</div>

---

## Reduction (귀착)

![다항식 시간 귀착 과정. 문제 A의 입력 x가 다항식 시간 변환 f를 거쳐 문제 B의 입력 f(x)가 되고, x가 A에 속하는 것과 f(x)가 B에 속하는 것이 서로 필요충분이다. 따라서 B를 풀 수 있으면 A도 풀 수 있고, B의 난이도가 A 이상이다](/images/np-complete/reduction.svg)

**Reduction(귀착)** 은 문제의 난이도를 비교하는 핵심 도구다. 문제 $A$를 문제 $B$로 **다항식 시간 귀착** 한다는 것은, 다항식 시간에 계산 가능한 변환 함수 $f$가 존재해 다음이 성립하는 것이다.

$$
A \leq_p B \iff \exists f \text{ (다항식 시간 계산 가능) s.t. } x \in A \Leftrightarrow f(x) \in B
$$

귀착 과정은 다음 세 단계로 이루어진다.

1. 문제 $A$의 입력 $x$를 문제 $B$의 입력 $f(x)$로 **변환(Transform)** 한다.
2. $B$의 알고리즘으로 $f(x)$에 대한 답을 구한다.
3. 그 답이 $A$에 대한 답이 된다.

### 귀착과 난이도의 관계

$A \leq_p B$가 성립하면 **"$B$는 적어도 $A$만큼 어렵다"** — $B$를 풀 수 있으면 $A$도 풀 수 있다.

| 귀착 방향 | 의미 |
|---|---|
| $A \leq_p B$ | $B$의 난이도 $\geq$ $A$의 난이도 |
| $A \leq_p B$ 이고 $B \leq_p A$ | $A$와 $B$의 난이도가 동일 |

> **왜 다항식 시간으로 제한하는가?** 변환에 너무 많은 계산을 허용하면, 변환 과정에서 문제를 거의 풀어버리게 되어 난이도 비교가 의미 없어진다. NP에서 "다항식 시간 귀착"은 원래 난이도를 왜곡하지 않는 변환을 의미한다.

---

## SAT (Boolean Satisfiability)

SAT는 주어진 Boolean formula를 참(True)으로 만드는 변수 배정이 존재하는지 판별하는 문제다.

**Satisfiable 예시:**

$$
\varphi = (p \lor q) \land \lnot p
$$

$p = \text{False},\ q = \text{True}$로 설정하면 $\varphi$가 참 → **Satisfiable**

**Unsatisfiable 예시:**

$$
\varphi = p \land \lnot p
$$

어떤 변수 배정으로도 참이 될 수 없음 → **Unsatisfiable**

변수가 $n$개일 때 가장 단순한 방법은 $2^n$가지 배정을 모두 검사하는 것이다. 이보다 본질적으로 빠른 결정론적 다항식 시간 알고리즘은 아직 알려져 있지 않다.

---

## Cook의 정리: SAT ∈ NP-Complete

SAT가 NP-Complete임을 증명하려면 두 조건을 모두 확인해야 한다.

### 1. SAT ∈ NP

NTM으로 모든 변수 배정을 비결정론적으로 탐색한다. 어떤 경로에서든 "Yes"인 배정을 찾으면 accept하므로, SAT ∈ NP.

### 2. 모든 NP 문제는 SAT로 귀착된다

이것이 Cook의 핵심 증명이다. 임의의 NP 문제 $L$에 대해 $L \leq_p \text{SAT}$를 보인다.

<div class="callout">
<div class="callout-title">증명 구조: NTM 실행 → 계산표 → 논리식</div>
<p>$M$이 $x$를 accept한다는 것은 accept로 끝나는 실행이 하나라도 있다는 뜻이다. 실행 하나를 표 한 장으로 적고, "이 표가 올바른 실행이다"를 논리식으로 옮긴다. 그러면 논리식을 참으로 만드는 배정이 곧 accept하는 실행이 된다.</p>
</div>

**Step 1: 실행 전체를 계산표 한 장으로**

$M$이 다항식 시간 $p(n)$ 안에 멈춘다고 하자. 그러면 헤드가 방문하는 테이프 칸도 $p(n)$개를 넘지 못한다. 시각을 세로로, 테이프 칸을 가로로 두면 $p(n) \times p(n)$짜리 표 한 장이 나온다. 이것을 **계산표(tableau)** 라 한다.

$i$행 $j$열 칸에는 시각 $i$에 테이프 $j$번 칸이 어떤 모습인지를 적는다. 칸이 가질 수 있는 값은 테이프 기호이거나, "여기 헤드가 있고 상태는 $q$다"를 뜻하는 기호다. 값의 가짓수 $|C|$가 $n$과 무관한 상수이므로, 칸마다 불리언 변수를 $|C|$개 두어 다음과 같이 인코딩한다.

$$
x_{i,j,s} = \text{참} \iff i \text{행 } j \text{열의 값이 } s
$$

변수는 모두 $|C| \cdot p(n)^2 = O(p(n)^2)$개다.

**Step 2: "올바른 실행"을 네 가지 제약으로**

표가 $M$의 accept하는 실행을 적은 것인지는 다음 넷을 모두 만족하는지로 판정된다.

| 제약 | 내용 | 크기 |
|---|---|---|
| $\varphi_{\text{cell}}$ | 모든 칸이 값을 정확히 하나 갖는다 | $O(p(n)^2)$ |
| $\varphi_{\text{start}}$ | 첫 행이 입력 $x$에 대한 초기 구성이다 | $O(p(n))$ |
| $\varphi_{\text{move}}$ | 한 행에서 다음 행으로 넘어가는 것이 $M$의 전이 규칙을 따른다 | $O(p(n)^2)$ |
| $\varphi_{\text{accept}}$ | 어느 칸엔가 accept 상태가 나타난다 | $O(p(n)^2)$ |

여기서 $\varphi_{\text{move}}$가 관건이다. "표 전체가 올바른 실행인가"를 한 번에 따지면 식이 걷잡을 수 없이 커진다.

<div class="callout callout-simple">
<div class="callout-title">국소성 — 이 증명이 굴러가는 지점</div>

머신의 한 걸음은 **국소적**이다. 헤드는 한 칸씩만 움직이므로, 어떤 칸의 다음 값은 바로 윗줄의 자기 자신과 좌우 이웃, 즉 세 칸으로 정해진다. 그래서 표 전체를 보지 않고 **연속한 두 행 × 연속한 세 열**로 이루어진 $2 \times 3$ 창을 모두 훑어, 각 창이 전이 규칙에 맞는지만 확인하면 된다. 첫 행이 초기 구성이고 모든 창이 합법이면 표 전체가 올바른 실행임이 따라 나온다.

창 하나가 담는 칸은 6개이고 각 칸의 값은 $|C|$가지이므로, 가능한 창 내용은 $|C|^6$가지 — $n$과 무관한 상수다. 합법인 창을 모두 나열해 OR로 묶으면 창 하나당 상수 크기의 식이 되고, 창은 $O(p(n)^2)$개이므로 $\varphi_{\text{move}}$ 전체도 $O(p(n)^2)$에 머문다.

</div>

**Step 3: Choice는 어디에 있는가**

DTM이라면 첫 행이 정해지는 순간 나머지 행이 모두 결정된다. NTM은 다르다. $\varphi_{\text{move}}$는 전이 규칙에 맞는 창을 **모두** 허용하므로, 한 행에서 다음 행으로 가는 길이 여럿일 수 있다. 논리식을 참으로 만드는 배정을 고르는 일이 곧 매 단계의 전이를 고르는 일이다.

| 구분 | DTM | NTM |
|---|---|---|
| 매 단계의 전이 | 하나로 정해짐 | 여럿 중 하나를 고름 |
| 시각 $t$의 구성(configuration) | 입력 $x$가 정하면 하나로 결정 | 어느 전이를 골랐느냐에 따라 달라짐 |
| 표를 채우는 자유도 | 없음 | 있음 — 이 자유도가 곧 Choice |

즉 Choice는 따로 붙이는 변수가 아니라 **표를 채우는 자유도 자체**다. 입력 $x$가 accept되는 경로가 존재한다면, 그 경로를 적은 표가 네 제약을 모두 만족한다. 거꾸로 네 제약을 만족하는 표는 accept로 끝나는 실행 하나를 그대로 적어 놓은 것이다.

$$
x \in L \iff \varphi_x = \varphi_{\text{cell}} \land \varphi_{\text{start}} \land \varphi_{\text{move}} \land \varphi_{\text{accept}} \text{ 가 satisfiable}
$$

식의 크기가 $O(p(n)^2)$이고 $x$를 보고 식을 적어 내는 데도 그만큼의 시간이면 충분하다. 변환이 다항식 시간에 계산 가능하므로 귀착의 조건이 갖춰졌다. **따라서 SAT ∈ NP-Complete.**

> **회로를 거치면 무엇이 걸리는가.** "실행을 회로로 바꾸고 회로를 논리식으로 바꾼다"는 설명도 흔하다. 다만 회로를 그대로 논리식으로 펼치면, 출력이 여러 곳에 쓰이는 게이트가 쓰인 횟수만큼 복제되어 식이 지수적으로 커질 수 있다. 이를 피하려면 게이트마다 새 변수를 하나씩 두고 "이 변수는 이 게이트의 출력과 같다"는 절을 더하는 방식(Tseitin 변환)이 필요하다. 크기는 선형으로 유지되지만 원래 식과 **동치**가 아니라 **동시 충족 가능(equisatisfiable)** 한 다른 식이 된다. 위 계산표 경로는 처음부터 논리식을 만들기 때문에 이 단계를 거치지 않는다.

<div class="callout callout-key">
<div class="callout-title">Cook의 정리의 의미</div>
<p>SAT가 NP-Complete임이 증명된 이후, 다른 문제의 NP-Complete 여부를 증명하는 방법이 생겼다.</p>
<p><strong>어떤 문제 $A$가 NP-Complete임을 보이려면:</strong></p>
<ol>
<li>$A \in \text{NP}$임을 보인다.</li>
<li>기존에 알려진 NP-Complete 문제 $B$에서 $B \le_p A$임을 보인다.</li>
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

**최적화 문제** 도 NP-Hard에 들어간다. 다만 최적화라는 형식 때문이 아니라, 밑에 깔린 판정 문제가 NP-Complete일 때 그렇다. TSP를 보자. "길이 $k$ 이하인 순회가 있는가"는 판정 문제이고 NP-Complete다. "가장 짧은 순회의 길이는 얼마인가"는 Yes/No가 아니라 수를 내놓으므로 NP에 속한다고 말할 수 없지만, 최적값을 한 번 부르면 $k$와 비교해 판정 문제의 답이 바로 나온다. NP-hardness는 이렇게 그대로 물려받는다.

> **아무 최적화 문제나 어려운 것은 아니다.** 최단 경로를 예로 들면, 판정 버전인 "길이 $k$ 이하인 경로가 있는가"는 P에 속하고 최적값 자체도 Dijkstra로 다항식 시간에 구한다. 최적화 버전이라고 해서 NP-Hard가 되지는 않는다. 어려움을 만드는 것은 형식이 아니라 밑에 깔린 판정 문제다.

---

## Co-NP

Co-NP는 NP의 보완(complement) 개념이다.

$$
L \in \text{Co-NP} \iff L^c \in \text{NP}
$$

NP가 **"Yes"에 대한 짧은 증명서** 가 존재하는 언어라면, Co-NP는 **"No"에 대한 짧은 증명서** 가 존재하는 언어다.

$\text{NP} \cap \text{Co-NP}$에 속하는 문제는 "Yes"와 "No" 모두에 대한 효율적인 증명이 존재한다. 대표적인 예로 **소인수분해의 결정 버전(Factoring decision version)** 이 있다.

> NP = Co-NP인지는 아직 미해결 문제다. $P$는 여집합에 대해 닫혀 있으므로 $P = \text{NP}$가 성립하면 $\text{NP} = \text{Co-NP}$도 따라 나온다. 거꾸로 $\text{NP} = \text{Co-NP}$에서 $P = \text{NP}$가 따라 나오는지는 알려져 있지 않다. 성립하지 않는다고 밝혀진 것이 아니라, 어느 쪽인지 모른다.

---

## 결론

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>$\text{NP-Complete} = \text{NP} \cap \text{NP-Hard}$: NP에 속하면서 모든 NP 문제를 귀착시킬 수 있는 가장 어려운 문제들</li>
<li>Cook의 정리: SAT는 최초의 NP-Complete 문제. 임의의 NTM 실행을 SAT 인스턴스로 변환할 수 있다.</li>
<li>어떤 NP-Complete 문제 하나를 다항식 시간에 풀면, 모든 NP 문제가 다항식 시간에 풀린다 — $P = \text{NP}$ 성립</li>
<li>$P \neq \text{NP}$로 추정되지만, 컴퓨터 과학 최대의 미해결 문제로 남아 있다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>

**[Division Theorem — 정수 나눗셈의 기초](/blog/division-theorem)** — NP-Complete까지 살펴본 계산 복잡도 이론 위에서, 이제 암호학의 수학적 기반인 정수론으로 넘어간다. Division Theorem은 임의의 양의 정수를 나누면 몫과 나머지가 유일하게 결정된다는 단순한 사실이며, 이것이 모듈러 산술·GCD·RSA로 이어지는 출발점이다.

</div>
