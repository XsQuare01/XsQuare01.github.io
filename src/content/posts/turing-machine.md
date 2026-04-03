---
title: "Turing Machine — 계산의 극한"
date: 2026-03-21T10:00:00
description: "현대 컴퓨터의 이론적 모델인 튜링 머신의 구조를 살펴보고, 2-Tape DTM, Universal Turing Machine, 그리고 DTM과 NTM의 계산 능력이 동일함을 정리한다."
tags: ["Computer Science", "Complexity Theory"]
category: theory
difficulty: 심화
---

> DFA에 스택을 추가하면 DPDA, 스택을 2개로 늘리면 튜링 머신과 동등해진다. 그렇다면 튜링 머신 자체는 어떤 구조를 가지며, 얼마나 강력할까?

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>DTM</strong>: Deterministic Turing Machine — 결정론적 튜링 머신</li>
<li><strong>NTM</strong>: Non-deterministic Turing Machine — 비결정론적 튜링 머신</li>
<li><strong>UTM</strong>: Universal Turing Machine — 임의의 TM을 시뮬레이션하는 TM</li>
<li><strong>Configuration</strong>: 현재 상태 + 테이프 내용 + 헤드 위치의 조합</li>
<li><strong>Tape alphabet Γ</strong>: 테이프에 쓸 수 있는 심볼 집합 (공백 ⊔ 포함)</li>
</ul>
</div>

DTM(Deterministic Turing Machine)은 현재 컴퓨터의 이론적 모델이다. 1936년 앨런 튜링이 제안했으며, Church-Turing Thesis에 따르면 튜링 머신으로 시뮬레이션할 수 없는 계산 모델은 존재하지 않는다.

---

## 튜링 머신의 구조

![튜링 머신 구조](/images/turing-machine/tm-structure.svg)

튜링 머신은 다음 여섯 가지 요소의 튜플로 정의한다.

$$M = (Q,\ \Sigma,\ \Gamma,\ q_0,\ F,\ \delta)$$

- **$Q$**: State들의 집합
- **$\Sigma$**: 입력 알파벳 (Input alphabet). 입력으로 들어올 수 있는 심볼들의 집합
- **$\Gamma$**: 테이프 알파벳 (Tape alphabet). 테이프에 쓸 수 있는 심볼들의 집합. $\Sigma \subseteq \Gamma$이며, 공백(blank) 심볼 $\sqcup$도 포함한다
- **$q_0$**: 초기 상태 (Initial state)
- **$F$**: 최종 상태들의 집합 (Final/Accepting states)
- **$\delta$**: 전이 함수 (Transition function)

전이 함수는 다음과 같이 표현한다.

$$(q,\ a) \to (r,\ b,\ R)$$

현재 상태가 $q$이고 헤드가 $a$를 읽으면, $b$를 쓰고 헤드를 오른쪽($R$)으로 이동한 뒤 상태를 $r$로 전환한다. 헤드의 이동 방향은 Left($L$), Right($R$), Stay($S$), 세 가지다.

![한 스텝 실행 trace](/images/turing-machine/tm-step-trace.svg)

---

## L13: 튜링 머신으로 문제 풀기

$$L_{13} = \{x \mid x = y \mathtt{2} y,\ y \in \{0, 1\}^*\}$$

구분자 $\mathtt{2}$를 기준으로 앞뒤의 문자열 $y$가 동일한지 검사하는 문제다.

![L13 알고리즘](/images/turing-machine/l13-algorithm.svg)

**동작 방식:**

1. 가장 왼쪽의 처리되지 않은 심볼을 읽는다.
   - $0$이면 $3$으로, $1$이면 $4$로 마킹(marking)하고 오른쪽으로 이동한다.
2. $\mathtt{2}$를 만날 때까지 이미 마킹된 심볼(3, 4)을 건너뛰며 오른쪽으로 이동한다.
3. $\mathtt{2}$를 지나 대응되는 위치의 심볼을 확인한다.
   - 마킹한 심볼이 $3$(원래 $0$)이었다면 $0$을 기대한다. $0$이 맞으면 $3$으로 마킹하고 처음으로 돌아간다.
   - 마킹한 심볼이 $4$(원래 $1$)이었다면 $1$을 기대한다. $1$이 맞으면 $4$로 마킹하고 처음으로 돌아간다.
   - 기대한 심볼과 다르면 **Reject** 한다.

![L13 헤드 이동 예시](/images/turing-machine/l13-head-move.svg)

4. **Accept 조건**: $\mathtt{2}$ 앞의 $y$와 뒤의 $y$ 모두 전부 마킹된 상태일 때 accept한다.

이 예시를 통해 알 수 있는 핵심은, **튜링 머신의 좌/우 이동 전이 함수만으로도 복잡한 문제를 해결할 수 있다** 는 점이다.

---

## 2-Tape DTM

테이프를 2개로 늘리면 계산 능력이 향상될까?

![1-Tape vs 2-Tape DTM](/images/turing-machine/tm-tape-comparison.svg)

DPDA에 스택을 1개 더 추가했을 때는 튜링 머신과 동등해질 만큼 계산 능력이 크게 늘었다. 그러나 **튜링 머신의 테이프를 2개로 늘려도 계산 능력 자체는 변하지 않는다.**

이유는 튜링 머신의 테이프가 한 방향으로 무한하기 때문이다. 1개의 무한한 테이프를 두 구역으로 나누어 사용하면 2개의 테이프 역할을 충분히 대신할 수 있다. 다만 두 테이프를 번갈아 읽어야 하므로 시간이 더 걸릴 수 있다.

이 성질은 차원으로도 확장된다. 2차원 테이프 역시 1개의 1차원 테이프로 표현할 수 있다.

---

## Universal Turing Machine (UTM)

2-Tape DTM을 활용한 특별한 모델이다. 임의의 튜링 머신 M을 **시뮬레이션** 하는 튜링 머신이다.

![UTM 구조](/images/turing-machine/utm-structure.svg)

**동작 방식:**

- **테이프 1**: 시뮬레이션할 튜링 머신 M의 rule set(전이 함수 목록)을 기록한다. 모든 규칙은 이진수로 인코딩할 수 있다.
- **테이프 2**: M의 초기 상태 $q_0$를 맨 앞에 기록하고, 이어서 M의 테이프 내용을 기록한다. 헤드의 현재 위치도 마킹한다.

실행 시, 테이프 2에서 현재 상태와 심볼을 읽어 테이프 1의 rule set과 비교한다. 매치되는 규칙이 있으면 해당 전이를 실행한다.

테이프 1의 내용을 M'의 rule set으로 교체하면 M'을 시뮬레이션할 수 있다. 즉, UTM은 **어떤 튜링 머신이든 시뮬레이션할 수 있는 튜링 머신** 이다.

이것이 현재 컴퓨터의 이론적 기반이다. 폰 노이만(John von Neumann)은 UTM의 개념을 실제 컴퓨터 설계에 적용하여, 프로그램을 메모리에 저장하고 순차적으로 실행하는 **폰 노이만 아키텍처(Von Neumann Architecture)** 를 고안했다. 이는 EDVAC 설계 보고서(1945)에서 처음 제시되었으며, 오늘날 거의 모든 컴퓨터의 구조적 기반이다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
<p>보편 튜링 머신(UTM)은 "모든 프로그램을 실행할 수 있는 프로그램"이다. 다른 튜링 머신의 규칙을 테이프에 적어두고 그대로 따라 실행하면, 어떤 튜링 머신이든 흉내 낼 수 있다. 이것이 바로 우리가 쓰는 컴퓨터의 원리다 — 하드웨어 하나에 소프트웨어(프로그램)를 바꿔 넣으면 무엇이든 할 수 있다.</p>
</div>

---

## DTM vs NTM: 계산 능력은 같다

지금까지의 결과를 정리하면 다음과 같다.

- DFA = NFA
- DPDA ≠ NPDA
- **DTM = NTM**

DPDA와 NPDA는 계산 능력이 달랐지만, DTM과 NTM은 동일하다. UTM을 이용해 이를 증명할 수 있다.

### NTM이란?

NTM(Non-deterministic Turing Machine)은 동일한 상태와 심볼에 대해 여러 전이 규칙을 가질 수 있는 튜링 머신이다.

예를 들어 $(q, a) \to (r, b, R)$과 $(q, a) \to (r, c, R)$이 동시에 존재할 수 있다.

![DTM vs NTM 비교](/images/turing-machine/ntm-dtm-compare.svg)

### 증명: UTM으로 NTM 시뮬레이션

UTM은 DTM이다. UTM으로 NTM을 시뮬레이션할 수 있다면, DTM = NTM이 된다.

NTM의 실행은 선택 지점마다 가지가 갈라지는 **계산 트리(computation tree)** 로 나타낼 수 있다. UTM은 이 트리를 BFS(너비 우선 탐색)로 순회하며 모든 가능한 경로를 탐색한다.

![NTM 시뮬레이션](/images/turing-machine/ntm-simulation.svg)

1. 현재 상태와 심볼을 읽고, 대응되는 모든 전이 규칙을 찾는다.
2. 각 규칙을 적용한 결과를 별도의 테이프에 복사하고, 각각을 독립적으로 시뮬레이션한다.
3. 시뮬레이션된 경로 중 하나라도 accept 상태에 도달하면 전체를 accept한다.

NTM이 accept한다면 UTM도 그 경로를 탐색하여 accept하므로, DTM = NTM이 성립한다.

$$\text{Class DTM} = \text{Class NTM}$$

---

## 결론

| 모델 | 결정론 vs 비결정론 | 계산 능력 |
|---|---|---|
| DFA vs NFA | 동일 | Regular Languages |
| DPDA vs NPDA | 다름 | DCFL ⊊ CFL |
| DTM vs NTM | 동일 | Recursively Enumerable |

<div class="callout callout-key">
<div class="callout-title">핵심 정리: 계산 가능성 vs 효율성</div>
<ul>
<li>비결정론이 항상 계산 능력을 높이는 것은 아니다. DFA, DTM에서는 비결정론을 도입해도 인식하는 언어가 달라지지 않는다.</li>
<li><strong>계산 가능성(무엇을 풀 수 있는가)</strong>: DTM = NTM</li>
<li><strong>효율성(얼마나 빠르게 푸는가)</strong>: NTM이 더 빠를 수 있다 — 이것이 P vs NP 문제의 핵심이다.</li>
<li>DPDA에서만 비결정론이 계산 능력 자체의 차이를 만들어낸다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Classes — 계산 가능성 클래스 D, E, co-E</strong> — 튜링 머신으로 풀 수 있는 문제를 D(결정 가능), E(열거 가능), co-E로 분류하고, Dovetailing 기법과 정지 문제의 모순 증명을 통해 D = E ∩ co-E를 보인다.</p>
</div>
