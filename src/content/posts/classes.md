---
title: "Classes — 계산 가능성 클래스 D, E, co-E"
date: 2026-03-21T14:00:00
description: "결정 가능한 문제의 집합 D, 열거 가능한 문제의 집합 E, 그리고 co-E를 정의하고, D = E ∩ co-E를 증명한다. 정지 문제를 통해 E ≠ D임을 확인한다."
tags: ["Computer Science", "Complexity Theory"]
category: theory
---

> 튜링 머신으로 풀 수 있는 문제를 분류하면 어떤 계층이 만들어질까? Class D, E, co-E는 이 계층의 가장 기본적인 세 층이다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>Class D</strong>: 결정 가능한 언어(Decidable) — TM이 항상 Yes 또는 No로 정지</li>
<li><strong>Class E</strong>: 열거 가능한 언어(Enumerable, RE) — TM이 x∈L이면 accept로 정지, x∉L이면 루프 가능</li>
<li><strong>Class co-E</strong>: E의 보집합 언어 — x∉L이면 accept로 정지, x∈L이면 루프 가능</li>
<li><strong>Dovetailing</strong>: 여러 TM을 동시에 한 단계씩 실행하는 병렬 시뮬레이션 기법</li>
<li><strong>정지 문제 (Halting Problem)</strong>: TM M과 입력 x에 대해 "M(x)가 정지하는가?"를 묻는 문제. E에 속하지만 D에는 속하지 않는다.</li>
</ul>
</div>

튜링 머신으로 풀 수 있는 문제를 **계산 가능성(Computability)** 의 관점에서 분류하면 세 개의 핵심 클래스가 드러난다. 이 글에서는 D, E, co-E의 정의와 관계, 그리고 이들의 경계를 결정짓는 정지 문제를 다룬다.

---

## Class D: 결정 가능한 문제

**Class D(Decidable)** 는 튜링 머신이 모든 입력에 대해 항상 정지하면서 Yes/No를 올바르게 답하는 언어들의 집합이다.

> TM M₁이 L의 **결정기(decider)** 라는 것은: 임의의 x에 대해 M₁(x)가 항상 정지하고, x∈L이면 accept, x∉L이면 reject를 출력함을 의미한다.

D에 속하는 예시:

- DFA가 인식하는 모든 Regular Language
- CFL (Context-Free Language)
- "TM의 헤드가 왼쪽으로 움직이는가?" (전이 함수 δ를 직접 분석해 L 방향 전이가 있는지 확인)

---

## Class E: 열거 가능한 문제

**Class E(Enumerable)**, 혹은 **RE(Recursively Enumerable)** 는 TM이 x∈L이면 반드시 accept로 정지하는 언어들의 집합이다. x∉L인 경우에는 reject로 정지할 수도 있고, 무한히 루프할 수도 있다.

> TM M₂가 L의 **열거기(enumerator)** 라는 것은: x∈L이면 M₂(x)가 accept로 정지함을 의미한다. x∉L에 대한 동작은 보장하지 않는다.

### 왜 "Enumerable"인가?

이름의 유래는 **L에 속하는 모든 문자열을 열거(enumerate)할 수 있다** 는 것에서 온다. 만약 TM M₂가 L의 열거기라면, M₂를 이용해 L의 원소를 하나씩 출력하는 또 다른 TM을 만들 수 있다.

어떻게? **Dovetailing** 기법을 사용한다.

Dovetailing은 여러 계산을 동시에 한 단계씩 교대로 실행하는 기법이다. 모든 문자열 s₁, s₂, s₃, ...에 대해 M₂를 병렬로 실행하되, 한 번에 한 단계씩 라운드를 늘려가며 처리한다.

![도브테일링 실행 순서](/images/classes/dovetailing.svg)

표에서 **s₁, s₂, s₃, ...** 는 특정한 집합이 아니라, 알파벳으로 만들 수 있는 **모든 문자열을 순서대로 나열한 것** 이다 (ε, a, b, aa, ab, ba, ...). 즉 "s₁이 L의 원소"라는 말은 "첫 번째 문자열이 L에 속한다"는 뜻이고, 어떤 특정 집합 S를 가리키는 게 아니다.

셀 안의 숫자는 전체 처리 순서이며, **초록 점(●)** 은 그 셀에서 M₂가 accept를 출력한 순간을 표시한다. 셀 ②에 초록 점이 찍혔다는 것은 다음을 의미한다:

> M₂(s₁)를 2단계까지 실행했더니 accept가 나왔다. → s₁이 L에 속함이 확인됐다. → s₁을 출력한다.

이것이 "Enumerate(열거)"다. 도브테일링은 각 라운드마다 대각선 방향으로 하나씩 더 많은 문자열을 커버하며(1라운드: s₁, 2라운드: s₁+s₂, ...) accept가 발견되는 문자열을 하나씩 수집한다. 결과적으로 L에 속하는 모든 문자열이 언젠가는 출력된다.

이 기법의 핵심은, 어떤 한 문자열에 무한 루프가 걸리더라도 다른 문자열의 진행이 막히지 않는다는 점이다. 만약 Dovetailing 없이 M₂(s₁)를 끝까지 기다리다가 무한 루프에 빠지면, s₂, s₃, ...는 영원히 처리되지 않는다.

### 사전식 나열과 결정 가능성

L이 **사전식 순서(lexicographic order)** 로 열거 가능하다면, L∈D임을 보일 수 있다.

> **정리**: L을 사전순으로 열거하는 TM이 존재하면, L∈D이다.

**증명**: x가 L에 속하는지 결정하려면, 사전순 열거를 시작한다. 언젠가 x보다 사전순으로 뒤에 있는 문자열이 출력되면, 그 시점까지 x가 나타나지 않았으므로 x∉L이다. 만약 x가 나타나면 x∈L이다. 어느 경우든 TM이 정지한다. ∎

단, 사전순 열거가 아닌 임의 순서의 열거라면 이 논리가 성립하지 않는다. "x가 아직 나오지 않았다"는 사실이 "x∉L"을 보장하지 않기 때문이다.

---

## D ⊆ E

결정 가능한 언어는 모두 열거 가능하다. 직관적으로, 항상 정지하는 TM은 이미 열거기의 조건을 만족한다.

> **증명**: L∈D라 하면 결정기 M₁이 존재한다. M₁은 모든 입력에 대해 정지하므로, 특히 x∈L이면 accept로 정지한다. 따라서 M₁은 그 자체로 L의 열거기이고, L∈E이다. ∎

---

## E ≠ D: 정지 문제

**정지 문제(Halting Problem)** 는 다음과 같이 정의한다.

$$L_{halt} = \{ \langle M, x \rangle \mid M \text{은 TM이고 } M(x) \text{가 정지함} \}$$

### L_halt ∈ E

> **증명**: UTM(Universal Turing Machine)을 이용해 M(x)를 시뮬레이션한다. M(x)가 정지하면 UTM도 정지하고 accept한다. M(x)가 정지하지 않으면 UTM도 루프한다. 따라서 $L_{halt} \in E$이다. ∎

### L_halt ∉ D: 자기 참조 모순

![정지 문제 모순 증명](/images/classes/halting-proof.svg)

H가 $L_{halt}$의 결정기라고 가정하자. 즉, 모든 ⟨M, x⟩에 대해 H가 정지하며, M(x)가 정지하면 accept, 루프하면 reject를 출력한다.

이제 H를 이용해 기계 S를 구성한다.

> **S(⟨M⟩)**: H(⟨M, ⟨M⟩⟩)를 실행한다.
> - H가 accept하면 (M(⟨M⟩)이 정지한다고 판단하면) → S는 **무한 루프** 한다.
> - H가 reject하면 (M(⟨M⟩)이 루프한다고 판단하면) → S는 **정지(accept)** 한다.

이제 S에 자기 자신 ⟨S⟩를 입력으로 넣으면:

- **경우 A**: S(⟨S⟩)가 정지한다고 가정 → H(⟨S, ⟨S⟩⟩) = accept → S는 루프해야 함 → **모순**
- **경우 B**: S(⟨S⟩)가 루프한다고 가정 → H(⟨S, ⟨S⟩⟩) = reject → S는 정지해야 함 → **모순**

두 경우 모두 모순이 발생하므로, H는 존재할 수 없다. 따라서 $L_{halt} \notin D$이다. ∎

---

## Class co-E

Language L의 **보집합(complement)** 은 $\bar{L} = \Sigma^* \setminus L$로 정의한다. **Class co-E** 는 보집합이 E에 속하는 언어들의 집합이다.

$$\text{co-E} = \{ L \mid \bar{L} \in E \}$$

TM M이 L의 열거기라면, M의 accept/reject 출력을 단순히 반전시키는 것만으로는 co-E의 열거기를 얻을 수 없다. reject가 "정지하고 거절"이 아니라 "무한 루프"일 수 있기 때문이다.

**D ⊆ co-E** 도 성립한다. L∈D이면 결정기의 accept/reject를 교환하면 $\bar{L}$의 결정기가 되므로 $\bar{L} \in D \subseteq E$, 즉 $L \in \text{co-E}$이다.

---

## D = E ∩ co-E

결정 가능한 언어가 정확히 열거 가능하면서 동시에 co-열거 가능한 언어들과 일치함을 증명한다.

![클래스 계층도](/images/classes/class-hierarchy.svg)

### D ⊆ E ∩ co-E

앞서 D ⊆ E와 D ⊆ co-E를 각각 보였다. 따라서 D ⊆ E ∩ co-E이다.

### E ∩ co-E ⊆ D

**증명**

L∈E이고 L∈co-E라 하자.

그러면 다음이 각각 존재한다.

- L의 열거기 M₂
- $\bar{L}$의 열거기 M₃

결정기 M₁(x)를 다음과 같이 구성한다.

> Dovetailing으로 M₂(x)와 M₃(x)를 병렬 실행한다.
> - M₂(x)가 먼저 accept하면 → x∈L이므로 M₁은 **accept** 하고 정지한다.
> - M₃(x)가 먼저 accept하면 → x∈$\bar{L}$이므로 x∉L, M₁은 **reject** 하고 정지한다.

x∈L이면 M₂(x)가 언젠가 accept하고,
x∉L이면 M₃(x)가 언젠가 accept하므로,
M₁은 모든 입력에 대해 정지한다.

따라서 L∈D이다. ∎

$$D = E \cap \text{co-E}$$

---

## 결정 불가능한 문제의 예

**"TM이 테이프에 'a'를 쓰는가?"**

$$L_a = \{ \langle M \rangle \mid \text{어떤 입력에 대해 M이 테이프에 } a \text{를 쓴다} \}$$

이 문제는 결정 불가능($L_a \notin D$)하다. $L_{halt}$에서의 환산(reduction)으로 증명한다: 만약 $L_a$의 결정기가 존재한다면, M이 어떤 입력 x에 대해 정지할 때만 'a'를 쓰도록 M을 변형함으로써 $L_{halt}$의 결정기도 만들 수 있다. 하지만 $L_{halt} \notin D$이므로 모순이다.

반면 **"TM의 헤드가 왼쪽으로 움직이는가?"** 는 결정 가능하다. 전이 함수 δ를 직접 분석해 L(Left) 방향 전이가 포함되었는지 확인하면 된다. 실행 없이 TM의 구조만 보면 되므로 항상 정지한다.

---

## 결론

| 클래스 | 정의 | 대표 예시 |
|---|---|---|
| D | 모든 입력에 정지, Yes/No 출력 | Regular, CFL |
| E | x∈L이면 accept로 정지 | $L_{halt}$ |
| co-E | x∉L이면 accept로 정지 | $\bar{L}_{halt}$ |

<div class="callout callout-key">
<div class="callout-title">핵심 정리: D = E ∩ co-E</div>
<ul>
<li>D ⊆ E: 결정기는 열거기이기도 하다. 항상 정지하는 TM은 accept 조건을 당연히 만족한다.</li>
<li>E ≠ D: 정지 문제(L_halt)는 E에 속하지만 D에는 속하지 않는다. 자기 참조 모순으로 증명한다.</li>
<li>D = E ∩ co-E: L과 L̄ 모두 열거 가능하면, Dovetailing으로 결정기를 구성할 수 있다.</li>
<li>결정 불가능 문제는 항상 Halting Problem의 변형이거나 reduction으로 연결된다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Alice and Bob — 계산 복잡도 클래스 P, NP, PSPACE</strong> — 암호화의 안전성을 계산 복잡도로 정의한다. P, NP, EXP, PSPACE 클래스와 P ⊆ NP ⊆ PSPACE ⊆ EXP 계층 관계를 살펴본다.</p>
</div>
