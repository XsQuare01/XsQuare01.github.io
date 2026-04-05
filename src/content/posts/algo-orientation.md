---
title: "알고리즘 오리엔테이션 — 알고리즘이란 무엇인가"
date: 2026-04-05T09:00:00
description: "알고리즘의 정의와 올바름(Correctness)을 살펴보고, 수학적 귀납법과 루프 불변식으로 알고리즘을 증명한다. 정지 문제(Halting Problem)로 알고리즘의 근본 한계를 확인하고, RAM 모델과 점근적 표기법(Big-O, Θ, Ω)으로 효율을 분석한다."
tags: ["Algorithm", "Complexity Theory", "Big-O"]
category: algorithm
difficulty: 입문
---

> 알고리즘은 컴퓨터 과학의 심장이다. 어떤 문제를 어떻게 푸는지, 얼마나 빠르게 푸는지를 수학적으로 분석하는 것이 알고리즘 학습의 시작이다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>알고리즘의 정의와 올바른 알고리즘의 조건</li>
<li>수학적 귀납법과 루프 불변식 — 올바름을 수학적으로 증명하는 방법</li>
<li>정지 문제 — 어떤 알고리즘도 풀 수 없는 문제가 존재한다</li>
<li>RAM 모델, 점근적 표기법(Big-O / Ω / Θ)으로 효율 분석</li>
</ul>
</div>

## 알고리즘이란 무엇인가

**알고리즘(Algorithm)** 이란 어떤 문제를 해결하기 위한 **명확하고 유한한 절차**다. 9세기 페르시아의 수학자 알-콰리즈미(Al-Khwārizmī)의 이름에서 유래했다.

알고리즘은 다음 다섯 가지 성질을 만족해야 한다.

| 성질 | 설명 |
|---|---|
| **Input** | 0개 이상의 입력을 받는다 |
| **Output** | 1개 이상의 출력을 낸다 |
| **Definiteness** | 각 단계가 명확하고 모호하지 않아야 한다 |
| **Finiteness** | 유한한 단계 후에 반드시 종료해야 한다 |
| **Effectiveness** | 각 단계는 실제로 수행 가능한 기본 연산이어야 한다 |

"충분히 큰 소수를 찾아라"는 알고리즘이 될 수 없다. **종료 기준이 불명확**하기 때문이다. "이 배열에서 가장 큰 수를 반환하라"는 알고리즘이다.

---

## Correctness — 알고리즘의 올바름

알고리즘이 **올바르다(correct)** 는 것은 다음을 의미한다.

> 모든 유효한 입력에 대해, 알고리즘이 항상 종료하고 올바른 출력을 낸다.

이 정의는 두 층위로 나뉜다.

- **Partial Correctness (부분 올바름):** 알고리즘이 종료한다면, 올바른 답을 낸다.
- **Total Correctness (완전 올바름):** 알고리즘이 반드시 종료하고, 올바른 답을 낸다.

단순히 몇 가지 테스트 케이스를 통과하는 것은 올바름을 보장하지 않는다. 올바름을 수학적으로 증명하려면 **수학적 귀납법**이나 **루프 불변식(Loop Invariant)** 을 사용한다.

**루프 불변식 예시:** "배열의 첫 $k$개 원소 중 최댓값은 `max_val`에 저장되어 있다."라는 불변식을 매 반복에서 유지함으로써 find_max의 올바름을 증명할 수 있다.

---

## 수학적 귀납법 — 올바름의 증명 도구

**수학적 귀납법(Mathematical Induction)** 은 알고리즘의 올바름을 수학적으로 증명하는 가장 강력한 도구다. 재귀 알고리즘의 정당성, 반복문의 정확성, 복잡도 공식의 유도 모두 귀납법을 기반으로 한다.

### 약한 귀납법 (Weak Induction)

명제 $P(n)$이 모든 양의 정수 $n$에 대해 참임을 증명하는 절차:

1. **기저 사례 (Base Case):** $P(1)$이 참임을 직접 보인다.
2. **귀납 단계 (Inductive Step):** $P(k)$가 참이라는 **귀납 가정(Inductive Hypothesis)** 하에, $P(k+1)$이 참임을 보인다.

**예제:** $1 + 2 + 3 + \cdots + n = \dfrac{n(n+1)}{2}$ 증명

- **Base Case:** $n = 1$이면 좌변 $= 1$, 우변 $= \frac{1 \cdot 2}{2} = 1$. 성립.
- **Inductive Step:** $1 + 2 + \cdots + k = \frac{k(k+1)}{2}$라 가정하면,

$$1 + 2 + \cdots + k + (k+1) = \frac{k(k+1)}{2} + (k+1) = \frac{(k+1)(k+2)}{2} \quad \square$$

### 강한 귀납법 (Strong Induction)

귀납 가정을 "$P(1), P(2), \ldots, P(k)$ 모두 참"으로 강화한다. 하위 문제가 꼭 $k$가 아니라 $k$ 이하의 임의의 값에 의존할 때 사용한다.

재귀 알고리즘 분석에서는 강한 귀납법이 더 자연스럽다. 예를 들어, $\text{factorial}(n)$이 올바름을 증명할 때 "$\text{factorial}(n-1)$이 올바르다"는 가정이 필요하기 때문이다.

### 루프 불변식 (Loop Invariant)

반복문의 올바름은 루프 불변식을 통해 귀납법으로 증명한다. 루프 불변식이란 **루프의 매 반복 전후에 항상 참인 명제**다.

증명은 세 단계를 따른다.

| 단계 | 의미 |
|---|---|
| **초기화 (Initialization)** | 루프 시작 전에 불변식이 참 (Base Case에 해당) |
| **유지 (Maintenance)** | 한 반복이 끝난 후에도 불변식이 참 (Inductive Step에 해당) |
| **종료 (Termination)** | 루프 종료 조건과 불변식을 결합하면 알고리즘의 올바름이 도출 |

**find_max에 대한 루프 불변식 증명:**

> **불변식 I:** 루프의 $k$번째 반복 직전, `max_val`은 `arr[0..k]`의 최댓값이다.

- **초기화:** $k = 1$일 때, `max_val = arr[0]`이므로 `arr[0..0]`의 최댓값 = `arr[0]`. 성립.
- **유지:** $k$번째 반복에서 `arr[k]`를 읽고, `arr[k] > max_val`이면 `max_val`을 갱신한다. 갱신 후 `max_val`은 `arr[0..k]`의 최댓값. 성립.
- **종료:** 루프가 $k = n-1$에서 끝나면, 불변식에 의해 `max_val`은 `arr[0..n-1]`의 최댓값. $\square$

---

## 정지 문제 — 알고리즘으로 풀 수 없는 문제

알고리즘은 모든 문제를 풀 수 있을까? 그렇지 않다.

**정지 문제 (Halting Problem):** 임의의 알고리즘 $A$와 입력 $x$가 주어졌을 때, $A(x)$가 유한한 시간 내에 종료(halt)하는지 아니면 무한 루프에 빠지는지를 판별하는 알고리즘이 존재하는가?

앨런 튜링(Alan Turing, 1936)은 이 문제가 **결정 불가능(Undecidable)** 하다는 것을 증명했다. 즉, 어떤 알고리즘도 정지 문제를 올바르게 풀 수 없다.

### 증명 — 대각선 논법 (Diagonal Argument)

**가정(귀류법):** `halts(program, input)`이라는 알고리즘이 존재한다고 하자. 이 알고리즘은 `program(input)`이 종료하면 `True`를, 무한 루프에 빠지면 `False`를 항상 올바르게 반환한다.

이 가정 하에 다음 알고리즘을 만들 수 있다.

```python
def halts(program, input) -> bool:
    # program(input)이 종료하면 True, 무한루프면 False를 반환
    ...  # 이런 알고리즘이 존재한다고 가정

def paradox(program):
    if halts(program, program):  # program(program)이 종료하면
        while True:               #   paradox는 무한루프에 빠진다
            pass
    else:                         # program(program)이 무한루프면
        return                    #   paradox는 즉시 종료한다
```

이제 `paradox(paradox)`를 실행하면:

| `halts(paradox, paradox)`의 반환값 | `paradox(paradox)`의 실제 동작 | 결론 |
|---|---|---|
| `True` (종료한다고 판정) | 무한루프에 빠짐 (종료하지 않음) | 모순 |
| `False` (무한루프라고 판정) | 즉시 종료 (종료함) | 모순 |

어느 경우에도 모순이 발생한다. 따라서 `halts`는 존재할 수 없다. $\square$

### 함의: 알고리즘으로 해결할 수 없는 문제가 존재한다

이 증명의 구조는 칸토어(Cantor)의 대각선 논법과 동일하며, [기수(Cardinality)](../cardinality) 포스트에서 다룬 "실수가 자연수보다 많다"는 증명과 정확히 같은 아이디어다.

<div class="callout callout-simple">
<div class="callout-title">정지 문제가 중요한 이유</div>
<p>정지 문제의 결정 불가능성은 소프트웨어 검증에 직접적인 한계를 부여한다. "이 프로그램이 버그 없이 항상 종료하는가?"를 완전히 자동으로 검증하는 범용 알고리즘은 존재하지 않는다. 정적 분석 도구들이 보수적 근사(conservative approximation)를 사용하는 이유가 바로 여기에 있다.</p>
</div>

---

## Efficiency — 왜 빠른 알고리즘이 필요한가

컴퓨터가 초당 $10^9$번 연산을 수행한다고 가정했을 때, 입력 크기에 따른 실행 시간을 비교해 보자.

| 복잡도 | $n = 100$ | $n = 10^4$ | $n = 10^6$ | $n = 10^9$ |
|---|---|---|---|---|
| $O(\log n)$ | 7 ns | 14 ns | 20 ns | 30 ns |
| $O(n)$ | 100 ns | 10 μs | 1 ms | 1 s |
| $O(n \log n)$ | 700 ns | 140 μs | 20 ms | 30 s |
| $O(n^2)$ | 10 μs | 100 ms | 17 min | 31 년 |
| $O(2^n)$ | $10^{12}$ 년 | — | — | — |

$n = 10^9$인 데이터를 $O(n^2)$ 알고리즘으로 처리하면 **31년**이 걸린다. 같은 문제를 $O(n \log n)$으로 처리하면 **30초**다. 알고리즘의 선택이 하드웨어 업그레이드보다 훨씬 강력한 이유가 여기 있다.

---

## RAM 모델 — 알고리즘 분석의 기준

알고리즘의 성능을 정량적으로 비교하려면 공통된 계산 모델이 필요하다. 알고리즘 분석에서는 **RAM 모델(Random Access Machine)** 을 표준으로 사용한다.

**RAM 모델의 가정:**
- 덧셈, 뺄셈, 곱셈, 나눗셈, 비교, 대입 등 **기본 연산**은 각각 $O(1)$ 시간이 걸린다.
- 배열 인덱스, 포인터 역참조 등 **메모리 임의 접근**은 주소에 관계없이 $O(1)$ 시간이 걸린다.
- 입력의 크기를 **$n$** 으로 추상화하고, 알고리즘의 수행 시간을 **$T(n)$** 으로 표현한다.

실제 하드웨어의 캐시 미스, 분기 예측, 메모리 대역폭 등은 무시한다. RAM 모델의 목적은 정확한 시간 예측이 아니라, **알고리즘의 본질적인 성장률**을 비교하는 것이다.

---

## 점근적 표기법 — Big-O, Ω, Θ

$n$이 충분히 커질 때 $T(n)$의 **성장률**을 나타내는 표기 체계다. 상수 계수나 낮은 차수의 항은 무시하고 지배적인 항만 남긴다.

### Big-O (상한, Upper Bound)

$$f(n) = O(g(n)) \iff \exists\, c > 0,\; n_0 > 0 \;\text{s.t.}\; \forall n \ge n_0,\; f(n) \le c \cdot g(n)$$

"$f$는 충분히 큰 $n$에 대해 $c \cdot g(n)$을 절대 넘지 않는다." 즉, $g(n)$은 $f(n)$의 **상한**이다.

**예:** $3n^2 + 5n + 1 = O(n^2)$

$c = 4$, $n_0 = 6$으로 놓으면 $n \ge 6$인 모든 정수에서 $3n^2 + 5n + 1 \le 4n^2$ 성립.

### Big-Ω (하한, Lower Bound)

$$f(n) = \Omega(g(n)) \iff \exists\, c > 0,\; n_0 > 0 \;\text{s.t.}\; \forall n \ge n_0,\; f(n) \ge c \cdot g(n)$$

"$f$는 충분히 큰 $n$에 대해 $c \cdot g(n)$ 이상이다." 즉, $g(n)$은 $f(n)$의 **하한**이다.

**예:** $3n^2 + 5n + 1 = \Omega(n^2)$

$c = 1$로 놓으면 모든 $n \ge 1$에서 $3n^2 + 5n + 1 \ge n^2$ 성립.

### Big-Θ (엄밀한 한계, Tight Bound)

$$f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \;\text{and}\; f(n) = \Omega(g(n))$$

"$f$와 $g$는 본질적으로 같은 성장률을 갖는다."

**예:** $3n^2 + 5n + 1 = \Theta(n^2)$ ($O(n^2)$이고 $\Omega(n^2)$이므로)

<div class="callout callout-simple">
<div class="callout-title">점근적 표기법 계산 규칙</div>
<ul>
<li><strong>상수 계수 제거:</strong> $5n^2 = O(n^2)$, $\;100 \cdot \log n = O(\log n)$</li>
<li><strong>낮은 차수 제거:</strong> $n^3 + n^2 + n + 1 = O(n^3)$</li>
<li><strong>합의 규칙:</strong> $O(f) + O(g) = O(\max(f, g))$</li>
<li><strong>곱의 규칙:</strong> $O(f) \cdot O(g) = O(f \cdot g)$</li>
<li><strong>로그 밑수 무관:</strong> $\log_2 n = O(\log_3 n)$ (변환 공식으로 상수 인수 차이만 존재)</li>
</ul>
</div>

---

## 주요 복잡도 클래스

자주 등장하는 복잡도 클래스를 성장 속도 순으로 나열하면 다음과 같다.

$$O(1) \;\subset\; O(\log n) \;\subset\; O(\sqrt{n}) \;\subset\; O(n) \;\subset\; O(n \log n) \;\subset\; O(n^2) \;\subset\; O(2^n) \;\subset\; O(n!)$$

| 복잡도 | 이름 | 대표 알고리즘 |
|---|---|---|
| $O(1)$ | 상수 | 배열 인덱스 접근, 해시 테이블 조회 |
| $O(\log n)$ | 로그 | 이진 탐색, 균형 이진 트리 |
| $O(n)$ | 선형 | 순차 탐색, 배열 순회 |
| $O(n \log n)$ | 선형 로그 | 병합 정렬, 힙 정렬, 퀵 정렬(평균) |
| $O(n^2)$ | 이차 | 삽입 정렬, 버블 정렬, 선택 정렬 |
| $O(n^3)$ | 삼차 | 행렬 곱셈(나이브), Floyd-Warshall |
| $O(2^n)$ | 지수 | 부분집합 완전 탐색, 피보나치(단순 재귀) |
| $O(n!)$ | 팩토리얼 | 순열 완전 탐색, TSP 브루트포스 |

---

## 예제 1: 배열에서 최댓값 찾기

```python
def find_max(arr: list[int]) -> int:
    max_val = arr[0]       # 1회
    for x in arr[1:]:      # n-1번 반복
        if x > max_val:    #   비교 1회
            max_val = x    #   대입 (최악 기준 1회)
    return max_val
```

**연산 횟수 분석 (RAM 모델):**

| 연산 | 횟수 |
|---|---|
| 초기 대입 | 1 |
| 루프 비교 | $n - 1$ |
| 루프 내 대입 (최악) | $n - 1$ |
| 반환 | 1 |

$$T_{\text{worst}}(n) = 1 + (n-1) + (n-1) + 1 = 2n = O(n)$$
$$T_{\text{best}}(n) = 1 + (n-1) + 0 + 1 = n = O(n)$$

최선과 최악 모두 $O(n)$이므로 $T(n) = \Theta(n)$.

---

## 예제 2: 순차 탐색 vs 이진 탐색

### 순차 탐색 (Linear Search)

```python
def linear_search(arr: list[int], target: int) -> int:
    """배열에서 target의 인덱스를 반환. 없으면 -1."""
    for i, x in enumerate(arr):
        if x == target:
            return i
    return -1
```

- **최선:** 첫 번째 원소가 target → $O(1)$
- **최악:** 마지막까지 없음 → $O(n)$
- **평균:** $O(n)$

정렬 여부와 무관하게 동작한다.

### 이진 탐색 (Binary Search)

**전제 조건: 배열이 정렬되어 있어야 한다.**

```python
def binary_search(arr: list[int], target: int) -> int:
    """정렬된 배열에서 target의 인덱스를 반환. 없으면 -1."""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2  # 중간 인덱스

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1         # 오른쪽 절반 탐색
        else:
            right = mid - 1        # 왼쪽 절반 탐색

    return -1
```

매 반복마다 탐색 범위가 **절반**으로 줄어든다.

$$n \to \frac{n}{2} \to \frac{n}{4} \to \cdots \to 1 \quad \Rightarrow \quad \frac{n}{2^k} = 1 \implies k = \log_2 n$$

- **최선:** $O(1)$ (첫 시도에 발견)
- **최악:** $O(\log n)$

| | 순차 탐색 | 이진 탐색 |
|---|---|---|
| 시간 복잡도 | $O(n)$ | $O(\log n)$ |
| 정렬 필요 여부 | X | O (필수) |
| $n = 10^6$일 때 최악 | ~$10^6$회 | ~20회 |
| $n = 10^9$일 때 최악 | ~$10^9$회 | ~30회 |

$10^9$개 원소의 정렬된 배열에서 이진 탐색은 **30번의 비교**로 끝난다.

![이진 탐색 추적 다이어그램 — arr=[2,5,8,11,14,17,20,23]에서 14를 찾는 3단계 과정](/images/algo-orientation/binary-search-trace.svg)

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>알고리즘은 명확하고 유한한 절차다. <strong>Definiteness</strong>와 <strong>Finiteness</strong>가 핵심 조건이다.</li>
<li><strong>수학적 귀납법</strong>: 기저 사례 + 귀납 단계로 알고리즘의 올바름을 증명한다. 루프 불변식은 반복문에 귀납법을 적용한 것이다.</li>
<li><strong>정지 문제</strong>: "이 프로그램이 종료하는가?"를 판별하는 범용 알고리즘은 존재하지 않는다. 대각선 논법으로 모순을 이끌어 낸다.</li>
<li>점근적 표기법: Big-O는 <strong>상한</strong>, Big-Ω는 <strong>하한</strong>, Big-Θ는 <strong>엄밀한 동치</strong>다. 상수 계수와 낮은 차수 항은 무시한다.</li>
<li>같은 문제도 알고리즘에 따라 성능이 수십만 배 달라질 수 있다. 하드웨어 업그레이드보다 알고리즘 개선이 훨씬 강력하다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>재귀 — 문제를 자기 자신으로 푼다</strong> — 알고리즘 설계의 핵심 기법인 재귀를 다룬다. 팩토리얼, 피보나치, 하노이의 탑을 통해 재귀적 사고를 익히고, 재귀 트리와 마스터 정리로 $T(n) = aT(n/b) + f(n)$ 형태의 점화식을 분석한다.</p>
</div>
