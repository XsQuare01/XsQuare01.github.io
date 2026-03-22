---
title: "Alice and Bob — 계산 복잡도 클래스 P, NP, PSPACE"
date: 2026-03-22T10:00:00
description: "암호화의 안전성을 계산 복잡도로 정의한다. P, NP, EXP, PSPACE 클래스를 소개하고, P ⊆ NP ⊆ PSPACE ⊆ EXP 계층 관계와 PSPACE = NPSPACE를 설명한다."
tags: ["Computer Science", "Complexity Theory"]
category: cryptography
---

> 정보 이론적으로 완벽하게 안전한 암호는 존재한다. 그러나 실용적이지 않다. 그렇다면 "충분히 안전하다"는 것을 어떻게 정의할까? 답은 계산 복잡도에 있다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>Alice, Bob, Eve</strong>: 암호학의 표준 3인 등장인물 — 송신자, 수신자, 도청자</li>
<li><strong>Class P</strong>: 다항식 시간 안에 결정 가능한 언어 (DTM 기준)</li>
<li><strong>Class NP</strong>: 다항식 시간 안에 결정 가능한 언어 (NTM 기준)</li>
<li><strong>Class EXP</strong>: 지수 시간 안에 결정 가능한 언어 (DTM 기준)</li>
<li><strong>Class PSPACE</strong>: 다항식 공간 안에 결정 가능한 언어 (DTM 기준)</li>
<li><strong>Savitch 정리</strong>: PSPACE = NPSPACE — 공간에서는 비결정론이 결정론보다 강하지 않다</li>
</ul>
</div>

앞선 글에서 튜링 머신으로 "무엇을 풀 수 있는가(계산 가능성)"를 다뤘다. 이 글에서는 한 발 더 나아가 "얼마나 빠르게(혹은 적은 공간으로) 풀 수 있는가"를 묻는다. 이것이 **계산 복잡도 이론(Computational Complexity Theory)** 의 핵심 질문이다.

---

## Alice, Bob, Eve

암호학에서 등장인물은 세 명이다.

![Alice-Bob-Eve 통신 모델](/images/alice-bob/alice-bob-eve.svg)

- **Alice**: 메시지 m을 Bob에게 전달하려는 송신자
- **Bob**: Alice의 메시지를 받으려는 수신자
- **Eve**: 공개 채널을 도청해 m을 알아내려는 공격자

Alice는 메시지 m을 key k로 암호화해 암호문 c = Enc_k(m)을 전송한다. Bob은 k를 이용해 c를 복호화해 m을 얻는다. Eve는 c를 가로채지만, k가 없으므로 m을 쉽게 알 수 없다.

---

## 암호화의 안전성

### 완벽한 보안: One-time Pad

이론적으로 완벽히 안전한 암호 체계가 존재한다. **One-time Pad**다.

- key: 무한히 긴 랜덤 이진 문자열
- 과정: Alice가 메시지 m을 key와 XOR하여 c를 만든다. Bob은 동일한 key로 XOR하여 m을 복원한다. 사용한 key는 즉시 폐기한다.
- 보안: Eve는 c만 보고 m에 대한 어떤 정보도 얻을 수 없다.

그러나 One-time Pad는 실용적이지 않다.

> 무한히 긴 랜덤 key를 Alice와 Bob이 사전에 **공유**해야 한다. key를 전달하는 데 또 다른 보안 채널이 필요하고, 이 과정이 무한히 반복된다.

### 계산적 보안

현실적인 암호는 **정보 이론적 안전성** 대신 **계산적 안전성**을 목표로 한다.

> Bob이 c를 m으로 복원하는 데 10분이 걸리고, Eve가 key 없이 m을 찾아내는 데 10년이 걸린다면, 그 암호는 실용적으로 안전하다.

단, Eve에게 **무한한 시간**이 주어진다면 어떤 암호도 뚫린다. key는 유한한 길이의 문자열이므로, 모든 가능한 key를 순서대로 시도하면(brute-force) 언젠가 m을 찾아낼 수 있다.

따라서 "안전하다"의 의미는 **"현실적인 시간 안에 풀 수 없다"** 로 재정의된다. 이를 수학적으로 표현하기 위해 복잡도 클래스가 필요하다.

---

## 시간 복잡도 클래스

### Class P: 다항식 시간

$$L \in P \iff \exists \text{ DTM } M_1,\ \exists \text{ 다항식 } p \text{ s.t. } M_1 \text{ decides } L,\ \forall x:\ T_{M_1}(x) \leq p(|x|)$$

임의의 입력 x에 대해 **다항식 시간** $p(|x|)$ 안에 Yes/No를 출력하는 DTM이 존재하면 $L \in P$이다.

다항식 시간은 특정 다항식 $p$가 하나로 고정되어야 한다. 어떤 입력에는 $5n^3$, 다른 입력에는 $6n^4$이 걸린다면, 모든 입력에 대해 $6n^4$ 안에 들어오므로 P에 속한다. 중요한 것은 어떤 단일 다항식이 모든 입력을 커버해야 한다는 점이다.

### Class NP: 비결정론적 다항식 시간

$$L \in NP \iff \exists \text{ NTM } M_2,\ \exists \text{ 다항식 } p \text{ s.t. } M_2 \text{ decides } L,\ \forall x,\ \forall \text{경로}:\ T_{M_2}(x) \leq p(|x|)$$

NTM이 다항식 시간 안에 L을 결정하면 $L \in NP$이다. 여기서 다항식 시간의 기준은 **모든 계산 경로**다. NTM은 각 단계에서 여러 경로를 동시에 시도하므로, 가장 긴 경로가 $p(|x|)$ 안에 끝나야 한다.

직관적으로: NTM을 "모든 경우의 수를 동시에 출발해 탐색하는 기계"로 보면, NP는 이 모든 경로가 다항식 시간 안에 종료되는 문제의 집합이다.

### Class EXP: 지수 시간

$$L \in EXP \iff \exists \text{ DTM } M_3,\ \exists \text{ 다항식 } p \text{ s.t. } M_3 \text{ decides } L \text{ in time } 2^{p(|x|)}$$

DTM이 지수 시간 $2^{p(n)}$ 안에 L을 결정하면 $L \in EXP$이다. 다항식 시간은 지수 시간에 포함되므로 $P \subseteq EXP$이다.

### Class NEXP: 비결정론적 지수 시간

EXP의 NTM 버전이다. 지수 시간 안에 결정하는 NTM이 존재하면 $L \in NEXP$이다.

---

## 공간 복잡도 클래스

시간 외에 **공간(메모리 사용량)** 도 복잡도의 척도가 된다.

- **PSPACE**: 다항식 공간을 사용하는 DTM이 존재하면 $L \in PSPACE$
- **NPSPACE**: 다항식 공간을 사용하는 NTM이 존재하면 $L \in NPSPACE$
- **EXPSPACE**: 지수 공간을 사용하는 DTM이 존재하면 $L \in EXPSPACE$

---

## 시간과 공간의 관계

### 다항식 공간 → 지수 시간: PSPACE ⊆ EXP

공간이 제한되면 시간도 제한된다. 다항식 공간 $s(n)$을 쓰는 TM이 가질 수 있는 서로 다른 **형상(configuration)** 의 수를 세어 보자.

- 테이프 내용: $|\Gamma|^{s(n)}$ 가지
- 헤드 위치: $s(n)$ 가지
- 상태: $|Q|$ 가지

$$\text{총 형상 수} = |\Gamma|^{s(n)} \times s(n) \times |Q|$$

이는 $s(n)$에 대해 지수적이다. TM이 이 수보다 많은 단계를 실행하면 동일한 형상이 반복되어 무한 루프에 빠진다(Pumping 논리). 따라서 다항식 공간을 쓰는 TM은 지수 시간 안에 반드시 정지한다.

$$PSPACE \subseteq EXP$$

### 전체 계층

아래 관계가 성립한다.

$$P \subseteq NP \subseteq PSPACE \subseteq EXP \subseteq NEXP \subseteq \cdots$$

각 포함 관계의 증명:

**1. P ⊆ NP**: DTM은 경로가 하나뿐인 NTM이다. DTM이 다항식 시간에 결정하면, NTM으로서도 다항식 시간에 결정한다.

**2. NP ⊆ PSPACE**: NTM의 계산 트리를 DTM으로 **DFS(깊이 우선 탐색)** 시뮬레이션한다.
- 각 계산 경로의 길이는 최대 $p(n)$
- DFS는 한 번에 하나의 경로만 탐색하며, 경로가 끝나면 공간을 재사용
- 따라서 어느 순간에도 $O(p(n))$ 공간만 사용됨

**3. PSPACE ⊆ EXP**: 위의 형상 수 계산 논리에 의해 성립한다.

![복잡도 클래스 계층](/images/alice-bob/complexity-classes.svg)

### PSPACE = NPSPACE (Savitch 정리)

공간에서는 비결정론이 결정론보다 강하지 않다.

> **Savitch 정리**: NTM이 공간 $s(n)$을 사용한다면 ($s(n) \geq \log n$), DTM으로 공간 $O(s(n)^2)$에 시뮬레이션할 수 있다.

조건 $s(n) \geq \log n$은 테이프 헤드 위치와 단계 수를 추적하는 데 필요한 최소 공간이 $\log n$ 수준이기 때문에 붙는다. 이 조건 미만에서는 시뮬레이션 자체를 표현할 공간이 부족하다. PSPACE는 $s(n) = n^k$ 형태이므로 이 조건을 항상 만족한다.

$s(n)$이 다항식이면 $s(n)^2$도 다항식이므로 NPSPACE ⊆ PSPACE가 성립하고, 반대 방향은 자명하므로:

$$PSPACE = NPSPACE$$

이는 시간 클래스(P vs NP)와 대조적이다. 공간에서는 비결정론의 이점이 제곱 인수 이내로 흡수된다.

---

## 결론

| 클래스 | 자원 | 기계 | 관계 |
|---|---|---|---|
| P | 다항식 시간 | DTM | 가장 효율적 |
| NP | 다항식 시간 | NTM | P ⊆ NP |
| PSPACE | 다항식 공간 | DTM | NP ⊆ PSPACE |
| EXP | 지수 시간 | DTM | PSPACE ⊆ EXP |

<div class="callout callout-key">
<div class="callout-title">핵심 정리: P, NP, PSPACE, EXP</div>
<ul>
<li>암호학적 안전성은 "정보 이론적 불가능"이 아닌 "계산적으로 비현실적"으로 정의한다.</li>
<li>P ⊆ NP ⊆ PSPACE ⊆ EXP — 각 포함 관계는 증명되어 있으나, 등호 여부는 대부분 미해결이다.</li>
<li>P ≠ EXP는 증명되어 있다. P = NP인지는 컴퓨터 과학 최대의 미해결 문제다.</li>
<li>PSPACE = NPSPACE (Savitch 정리) — 공간에서는 비결정론이 결정론보다 본질적으로 강하지 않다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>NP의 다른 정의 — 검증자와 증명서</strong> — NP를 "힌트가 있으면 다항식 시간에 검증 가능한 문제"로 재정의한다. 두 정의가 동치임을 증명하고, P ≠ NP 가정이 왜 암호학의 근간인지를 설명한다.</p>
</div>
