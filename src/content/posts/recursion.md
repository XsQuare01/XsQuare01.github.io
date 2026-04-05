---
title: "재귀 — 문제를 자기 자신으로 푼다"
date: 2026-04-05T10:00:00
description: "재귀(Recursion)의 구조와 올바른 설계 원칙을 이해하고, 팩토리얼·피보나치·하노이의 탑을 통해 재귀적 사고를 익힌다. 재귀 트리와 마스터 정리로 T(n) = aT(n/b) + f(n) 형태의 점화식을 분석한다."
tags: ["Algorithm", "Recursion", "Divide and Conquer"]
category: algorithm
difficulty: 입문
---

> 재귀는 자기 자신을 거울로 삼아 문제를 푸는 기법이다. 반복문이 "어떻게" 처리할지를 명시한다면, 재귀는 "무엇이" 해결책인지를 정의한다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>재귀의 구조: Base Case와 Recursive Case</li>
<li>팩토리얼, 피보나치, 하노이의 탑 — 재귀적 사고 훈련</li>
<li>단순 재귀의 지수적 폭발과 메모이제이션</li>
<li>재귀 트리와 마스터 정리로 복잡도 분석</li>
</ul>
</div>

## 재귀란 무엇인가

**재귀(Recursion)** 란 함수가 자기 자신을 호출하여 문제를 해결하는 기법이다. 핵심 아이디어는 **큰 문제를 더 작은 동일한 구조의 하위 문제로 분해**하는 것이다.

올바른 재귀 함수는 반드시 두 부분을 포함해야 한다.

| 구성 요소 | 설명 |
|---|---|
| **Base Case (기저 사례)** | 더 이상 재귀 호출 없이 직접 답을 반환하는 경우 |
| **Recursive Case (재귀 사례)** | 문제를 더 작은 하위 문제로 분해하고 재귀 호출 |

Base Case 없는 재귀는 무한히 자기 자신을 호출하다 **스택 오버플로(Stack Overflow)** 로 종료된다. Recursive Case가 문제를 실제로 더 작게 만들지 않아도 같은 결과가 발생한다.

<div class="callout callout-simple">
<div class="callout-title">재귀가 올바르게 종료하는 조건</div>
<ul>
<li>Base Case가 반드시 존재해야 한다.</li>
<li>모든 Recursive Case에서 하위 문제의 크기가 <strong>엄격하게 감소</strong>해야 한다.</li>
<li>유한 번의 감소 후 반드시 Base Case에 도달해야 한다.</li>
</ul>
</div>

---

## 팩토리얼

$$n! = n \times (n-1) \times (n-2) \times \cdots \times 1, \quad 0! = 1$$

이를 재귀적으로 정의하면:

$$n! = \begin{cases} 1 & n = 0 \\ n \times (n-1)! & n \ge 1 \end{cases}$$

```python
def factorial(n: int) -> int:
    # Base Case
    if n == 0:
        return 1
    # Recursive Case
    return n * factorial(n - 1)
```

**실행 흐름 (`factorial(4)`):**

```
factorial(4)
  = 4 * factorial(3)
        = 3 * factorial(2)
              = 2 * factorial(1)
                    = 1 * factorial(0)
                                = 1       ← Base Case
                    = 1 * 1 = 1
              = 2 * 1 = 2
        = 3 * 2 = 6
  = 4 * 6 = 24
```

**복잡도 분석:**

점화식: $T(n) = T(n-1) + O(1)$

이를 전개하면:

$$T(n) = T(n-1) + c = T(n-2) + 2c = \cdots = T(0) + nc = O(n)$$

시간 복잡도: $O(n)$, 공간 복잡도: $O(n)$ (콜 스택 깊이)

---

## 피보나치와 지수적 폭발

$$F(n) = \begin{cases} 0 & n = 0 \\ 1 & n = 1 \\ F(n-1) + F(n-2) & n \ge 2 \end{cases}$$

```python
def fib_naive(n: int) -> int:
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

직관적으로 깔끔해 보이지만, 이 구현은 심각한 문제를 갖는다. `fib(5)`를 계산해 보자.

```
fib(5)
  fib(4)
    fib(3)
      fib(2)
        fib(1) = 1
        fib(0) = 0
      fib(1) = 1
    fib(2)         ← fib(2) 중복 계산!
      fib(1) = 1
      fib(0) = 0
  fib(3)           ← fib(3) 중복 계산!
    fib(2)
      fib(1) = 1
      fib(0) = 0
    fib(1) = 1
```

`fib(n)`을 계산하는 데 필요한 호출 횟수를 $T(n)$이라 하면:

$$T(n) = T(n-1) + T(n-2) + O(1)$$

$T(n)$은 피보나치 수열 자체와 같은 성장률을 가지며, $T(n) = O(\phi^n)$ ($\phi \approx 1.618$, 황금비)이다. 이는 $O(2^n)$과 같은 **지수적 성장**이다.

**$n = 50$일 때:** $2^{50} \approx 10^{15}$번 호출 → 컴퓨터 수십 년 소요.

### 해결책: 메모이제이션

이미 계산한 결과를 저장해 두고 재사용한다.

```python
def fib_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]        # 캐시 히트
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

각 $F(k)$를 **정확히 1번**만 계산한다. 시간 복잡도: $O(n)$, 공간 복잡도: $O(n)$.

```python
# Python 표준 라이브러리 활용
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

---

## 하노이의 탑

세 개의 기둥(A, B, C)과 크기가 모두 다른 $n$개의 원판이 있다. 처음에 모든 원판이 A 기둥에 크기 순으로 쌓여 있다.

**규칙:**
1. 한 번에 원판 하나만 이동할 수 있다.
2. 큰 원판을 작은 원판 위에 올릴 수 없다.

A에서 C로 모든 원판을 옮기는 알고리즘은 다음과 같다.

$$\text{hanoi}(n, A \to C) = \text{hanoi}(n-1, A \to B) + \text{move}(A \to C) + \text{hanoi}(n-1, B \to C)$$

```python
def hanoi(n: int, source: str, target: str, aux: str) -> None:
    """
    n개의 원판을 source에서 target으로 aux를 이용해 옮긴다.
    """
    if n == 1:
        print(f"원판 1: {source} → {target}")
        return
    # 1단계: 위의 n-1개를 보조 기둥으로 이동
    hanoi(n - 1, source, aux, target)
    # 2단계: 가장 큰 원판을 목적지로 이동
    print(f"원판 {n}: {source} → {target}")
    # 3단계: n-1개를 보조 기둥에서 목적지로 이동
    hanoi(n - 1, aux, target, source)

# 실행
hanoi(3, 'A', 'C', 'B')
```

**점화식:**

$$T(n) = 2T(n-1) + 1, \quad T(1) = 1$$

전개하면:

$$T(n) = 2T(n-1) + 1 = 2(2T(n-2) + 1) + 1 = 4T(n-2) + 3 = \cdots = 2^{n-1}T(1) + (2^{n-1} - 1) = 2^n - 1$$

$$T(n) = \Theta(2^n)$$

$n = 64$일 때 필요한 이동 횟수: $2^{64} - 1 \approx 1.8 \times 10^{19}$회. 초당 1회 이동한다면 약 **5800억 년**이 걸린다.

---

## 재귀 트리 분석

재귀 호출의 구조를 트리로 시각화하면 총 수행 시간을 직관적으로 분석할 수 있다.

**병합 정렬(Merge Sort)의 점화식:** $T(n) = 2T(n/2) + O(n)$

```
                   n                  ← 레벨 0: 병합 비용 n
               /       \
          n/2             n/2         ← 레벨 1: 각 n/2, 합계 n
         /   \           /   \
       n/4   n/4       n/4   n/4      ← 레벨 2: 각 n/4, 합계 n
       ...   ...       ...   ...
        1    1    ...    1    1       ← 레벨 log n: 총 n개 리프
```

- 트리의 깊이: $\log_2 n$
- 각 레벨의 총 작업량: $n$
- 전체 작업량: $n \times \log_2 n = O(n \log n)$

---

## 마스터 정리

$a \ge 1$, $b > 1$인 상수에 대해 점화식이 다음 형태이면:

$$T(n) = aT\!\left(\frac{n}{b}\right) + f(n)$$

마스터 정리(Master Theorem)로 $T(n)$의 점근적 해를 구할 수 있다.

**직관적 이해:** $n^{\log_b a}$는 재귀 트리에서 리프 노드의 총 비용이고, $f(n)$은 각 레벨의 분할/병합 비용이다. 둘 중 어느 쪽이 지배적인가에 따라 해가 결정된다.

### Case 1: 리프 비용이 지배

$$f(n) = O(n^{\log_b a - \varepsilon}), \quad \varepsilon > 0 \implies T(n) = \Theta(n^{\log_b a})$$

### Case 2: 균형 (동등)

$$f(n) = \Theta(n^{\log_b a}) \implies T(n) = \Theta(n^{\log_b a} \cdot \log n)$$

### Case 3: 분할/병합 비용이 지배

$$f(n) = \Omega(n^{\log_b a + \varepsilon}), \quad \varepsilon > 0,\; af(n/b) \le cf(n) \implies T(n) = \Theta(f(n))$$

### 마스터 정리 적용 예시

| 점화식 | $a$ | $b$ | $n^{\log_b a}$ | $f(n)$ | 케이스 | 결과 |
|---|---|---|---|---|---|---|
| $T(n) = 2T(n/2) + n$ | 2 | 2 | $n^1 = n$ | $n$ | Case 2 | $\Theta(n \log n)$ |
| $T(n) = 4T(n/2) + n$ | 4 | 2 | $n^2$ | $n$ | Case 1 | $\Theta(n^2)$ |
| $T(n) = T(n/2) + n$ | 1 | 2 | $n^0 = 1$ | $n$ | Case 3 | $\Theta(n)$ |
| $T(n) = 9T(n/3) + n^2$ | 9 | 3 | $n^2$ | $n^2$ | Case 2 | $\Theta(n^2 \log n)$ |
| $T(n) = 2T(n/2) + n^2$ | 2 | 2 | $n$ | $n^2$ | Case 3 | $\Theta(n^2)$ |

**병합 정렬 검증:** $a=2$, $b=2$ → $n^{\log_2 2} = n^1 = n = f(n)$ → Case 2 → $T(n) = \Theta(n \log n)$ O

---

## 재귀 vs 반복

재귀와 반복문은 표현력이 동등하다. 모든 재귀는 반복문으로 변환할 수 있고, 그 역도 성립한다.

| 비교 항목 | 재귀 | 반복 |
|---|---|---|
| 코드 간결성 | 문제 구조가 재귀적이면 훨씬 간결 | 상태 관리를 직접 해야 함 |
| 가독성 | 수학적 정의와 1:1 대응 | 명시적 루프 제어 |
| 공간 복잡도 | 콜 스택 $O(d)$ ($d$: 재귀 깊이) | 일반적으로 $O(1)$ |
| 적합한 문제 | 트리, 그래프, 분할 정복 | 단순 반복, 배열 순회 |
| 주의사항 | 스택 오버플로 위험 | — |

재귀가 빛나는 문제는 **문제 자체가 재귀적 구조**를 가질 때다. 트리 순회, 분할 정복, 동적 프로그래밍의 원형은 재귀로 표현하는 것이 가장 자연스럽다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>재귀는 반드시 <strong>Base Case</strong>와 <strong>크기가 감소하는 Recursive Case</strong>를 가져야 올바르게 종료한다.</li>
<li>단순 재귀 피보나치는 $O(2^n)$이다. <strong>메모이제이션</strong>으로 중복 계산을 제거하면 $O(n)$이 된다.</li>
<li>하노이의 탑은 $T(n) = 2T(n-1) + 1 = 2^n - 1 = \Theta(2^n)$이다. 이 하한은 더 개선할 수 없다.</li>
<li>마스터 정리: $T(n) = aT(n/b) + f(n)$의 해는 $n^{\log_b a}$와 $f(n)$의 크기 비교로 결정된다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>정렬 알고리즘 — 비교 기반 정렬의 모든 것</strong> — 삽입 정렬, 병합 정렬, 힙 정렬, 퀵 정렬의 동작 원리와 복잡도를 분석한다. 비교 기반 정렬의 하한이 $\Omega(n \log n)$임을 결정 트리로 증명한다.</p>
</div>
