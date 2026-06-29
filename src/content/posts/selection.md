---
title: "선택 문제 — k번째 원소를 정렬 없이 O(n)에 찾기"
date: 2026-06-29T09:00:00
description: "k번째로 작은 원소를 찾는 선택 문제. 정렬하면 O(n log n)이지만 선택은 정렬보다 쉬운 문제다. 퀵소트의 분할을 재활용해 한쪽으로만 재귀하는 quickselect를 보고, 최악 O(n²)을 없애기 위해 approximate median(가운데 40%)을 5개씩 묶어 찾는 median of medians로 최악에도 O(n)임을 증명한다."
tags: ["Algorithm", "Selection", "Quickselect", "Median of Medians", "Linear Time"]
category: algorithm
difficulty: 심화
---

> [퀵 정렬](/blog/quicksort)은 최악의 경우 $O(n^2)$까지 느려진다. 만약 pivot으로 항상 중앙값을 고를 수 있다면, 최악에도 $O(n \log n)$이 보장된다. 그런데 중앙값을 찾는 것 자체가 문제다 — 이것이 바로 **선택 문제(selection problem)**다. 선택을 $O(n)$에 풀면, 퀵 정렬의 최악 또한 봉인된다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 선택 문제의 정의 — $k$번째로 작은 원소 찾기
- **Quickselect** — 퀵 정렬의 분할을 재활용해 한쪽으로만 재귀하기
- **Approximate median** — 정확한 중앙값 대신 "가운데 40%"면 충분하다
- **Median of medians** — 5개씩 묶어 approximate median을 $O(n)$에 찾고, 최악에도 $O(n)$ 보장

</div>

---

## 선택 문제란

$n$개의 수 $a_1, a_2, \ldots, a_n$이 주어질 때, **$k$번째로 작은 수**를 찾는 것이 선택 문제다.

- $k = 1$이면 최솟값
- $k = n$이면 최댓값
- $k = \lfloor n/2 \rfloor$이면 중앙값(median)

세 가지가 모두 같은 문제의 특수 경우다. 최솟값이나 최댓값은 선형 탐색 $O(n)$으로 쉽게 구할 수 있다. 그렇다면 일반적인 $k$에 대해서도 정렬 없이 $O(n)$에 풀 수 있을까?

---

## 정렬보다 쉬운 문제

가장 단순한 접근은 **정렬 후 인덱싱**이다. 배열을 정렬하고 $a[k-1]$을 반환하면 $O(n \log n)$에 풀린다. 하지만 이것은 지나치게 많은 일을 한다.

정렬은 $1$번째부터 $n$번째까지 **모든** 원소의 순서를 확정한다 — $n$개의 선택 문제를 한꺼번에 푸는 셈이다. 우리가 원하는 것은 그중 **하나**뿐이다.

하한을 먼저 생각해 보자. $k$번째 원소를 찾으려면 **모든 원소를 최소한 한 번은 봐야 한다.** 어떤 원소도 보지 않고 $k$번째를 특정할 수는 없으므로, $\Omega(n)$이 자명한 하한이다. 따라서 목표는 **$\Theta(n)$** — 선형 시간이다.

<div class="callout callout-simple">
<div class="callout-title">정렬을 다 하면 손해</div>

다른 모든 원소들의 대소관계를 다 알고 있다면, 그것은 이미 정렬 — $O(n \log n)$으로 회귀한다. 선택이 정렬보다 쉬운 이유는, 관심 없는 원소들 사이의 순서를 굳이 확정하지 않아도 되기 때문이다.

</div>

---

## Quickselect — 한쪽으로만 재귀

[퀵 정렬](/blog/quicksort)의 분할(partition)을 그대로 가져온다. pivot $p$를 하나 잡고 배열을 한 번 훑으면($O(n)$), pivot의 최종 위치 $j$가 정해진다. 이때 pivot의 **등수**는 $j + 1$이다.

- $k = j + 1$이면 $a[j]$가 바로 답이다.
- $k < j + 1$이면 $k$번째는 왼쪽 영역에만 있다 — 오른쪽은 볼 필요가 없다.
- $k > j + 1$이면 $k$번째는 오른쪽 영역에만 있다 — 왼쪽은 볼 필요가 없다.

퀵 정렬이 양쪽 모두를 재귀하는 것과 달리, **quickselect는 한쪽만 재귀**한다. 이것이 핵심이다.

```cpp
int select(int a[], int n, int k) {  // k번째(1-indexed) 작은 값
    int j = partition(a, n);   // 내부에서 a[0]을 pivot으로 써 제자리로, 반환은 경계 인덱스
    int rank = j + 1;          // pivot의 등수
    if (k == rank) return a[j];
    if (k < rank)  return select(a, j, k);            // 왼쪽만
    else           return select(a + j + 1, n - j - 1, k - rank);  // 오른쪽만
}
```

### 최선과 최악

**최선** — pivot이 매번 중앙값에 가까울 때. 분할 후 배열이 절반씩 줄어드는 등비수열이 된다.

$$
S(n) = n + S(n/2) = n + \frac{n}{2} + \frac{n}{4} + \cdots = O(n)
$$

등비수열의 합이 $2n$에 수렴하므로 $O(n)$이다.

**최악** — pivot이 매번 끝값(최솟값 또는 최댓값)일 때. 분할 후 한쪽이 $n-1$개로 고작 하나씩만 줄어든다.

$$
S(n) = n + S(n-1) = n + (n-1) + (n-2) + \cdots = O(n^2)
$$

이 합은 $\sum_{k=1}^{n} k = \frac{n(n+1)}{2} = O(n^2)$이다.

<div class="callout callout-simple">
<div class="callout-title">평균에 대한 한마디</div>

대부분의 경우 $O(n)$이지만 최악이 남는다. 평균이 정말 $O(n)$인지는 [별도 글](/blog/selection-average)에서 기댓값으로 따진다.

</div>

---

## Approximate median — 정확할 필요는 없다

최악을 없애려면 **pivot이 항상 중앙 근처여야** 한다. 그런데 정확한 중앙값을 찾는 것이 문제라면, 어디까지 "어림잡아도" 괜찮을까?

**정확한 중앙값이 아니어도 된다.** pivot이 전체의 **가운데 40%**, 즉 전체 중 30번째~70번째 백분위 사이의 값이면 충분하다. 이런 pivot을 **approximate median**이라 부른다.

먼저 이런 pivot이 **퀵 정렬**에 어떤 효과를 주는지 보자. Approximate median을 쓰면 분할 후 한쪽 배열의 크기가 최대 $0.7n$으로 묶인다. 점화식을 다루기 쉽게 이 상한을 넉넉히 $\frac{3}{4}n$로 잡으면(0.7n보다 크므로 안전한 상한이다), 퀵 정렬은 양쪽을 모두 정렬하므로 정렬 비용의 점화식은:

$$
Q(n) = n + Q\!\left(\frac{1}{4}n\right) + Q\!\left(\frac{3}{4}n\right)
$$

이를 재귀 트리로 그려 보면, 각 레벨의 작업량 합은 항상 $n$ 이하이고 트리 깊이는 $O(\log n)$이므로 전체 합은 $O(n \log n)$이다 — 퀵 정렬에서와 같은 논리다. 즉, pivot이 가운데 40% 안에만 들어오면 퀵 정렬은 항상 $O(n \log n)$을 유지한다.

다만 이 $Q(n)$은 **퀵 정렬**의 비용이지 선택의 비용이 아니다. 선택 알고리즘은 양쪽을 모두 푸는 것이 아니라 **한쪽만 재귀**하므로, 비용은 다음 섹션에서 $S(n)$으로 따로 세운다. 우선 남은 문제는 그런 approximate median pivot을 어떻게 **빠르게** 찾느냐다.

---

## Median of medians — 5개씩 묶기

Approximate median을 **$O(n)$에 찾는 알고리즘**이 median of medians다. 다음 세 단계로 구성된다.

1. $n$개의 원소를 **5개씩 묶어** $\lceil n/5 \rceil$개의 그룹으로 나눈다.
2. 각 그룹(최대 5개)을 **정렬해 그룹 중앙값** $X_i$를 구한다.
3. $X_i$들(총 $\lceil n/5 \rceil$개)의 **중앙값** $X'$를 재귀적으로 구한다. 이 $X'$가 approximate median이다.

![5개씩 묶어 그룹 중앙값을 구하고, 중앙값들의 중앙값 X'를 찾는 과정](/images/selection/median-of-medians.svg)

### 왜 X'는 가운데 40% 안에 있는가

$X'$는 $\lceil n/5 \rceil$개의 그룹 중앙값들의 중앙값이므로, **그룹 중앙값 중 절반($\approx n/10$개)이 $X'$ 이하다.**

각 그룹은 5개이고, 그룹 중앙값 $X_i$가 $X'$ 이하인 그룹에서는 중앙값 포함 아래 3개($X_i$ 이하 원소)가 $X'$ 이하다. 따라서 $X'$ 이하임이 보장되는 원소 수는:

$$
3 \times \frac{n}{10} = 0.3n
$$

대칭 논리로 $X'$ 이상임이 보장되는 원소도 $0.3n$개다.

결론: $X'$는 전체에서 최소 30%, 최대 70% 위치에 놓인다 — 즉 **가운데 40%** 안의 값이다. 따라서 $X'$를 pivot으로 분할하면 $X'$의 왼편에 최소 $0.3n$개, 오른편에 최소 $0.3n$개가 들어가, 어느 쪽으로 재귀하든 크기가 최대 $0.7n$으로 묶인다. Approximate median 조건을 정확히 만족한다.

<div class="callout callout-simple">
<div class="callout-title">왜 5개인가 (예고)</div>

왜 하필 5개씩일까? 3개로 나누면 왜 이 보장이 깨지는지는 [별도 글](/blog/selection-why-five)에서 다룬다.

</div>

---

## 분석 — 최악에도 O(n)

Median of medians를 pivot 선택에 쓰면 전체 알고리즘의 점화식을 세울 수 있다.

Approximate median을 구하는 비용을 $A(n)$이라 하자. $A(n)$은 두 부분으로 나뉜다.

- 5개씩 그룹 정렬: 상수 시간 그룹이 $n/5$개이므로 $O(n)$.
- 그룹 중앙값 $n/5$개에서 중앙값 재귀: $S(0.2n)$.

$$
A(n) = n + S(0.2n)
$$

Approximate median을 pivot으로 쓰면, 분할 후 재귀하는 쪽 배열 크기가 최대 $0.7n$이다. 따라서 전체 점화식은:

$$
S(n) = A(n) + n + S(0.7n) = \bigl(n + S(0.2n)\bigr) + n + S(0.7n)
$$

$$
\boxed{S(n) = 2n + S(0.2n) + S(0.7n)}
$$

### 대입법으로 풀기

$S(n) \le cn$이라는 선형 상한을 가정하고 점화식에 대입해, 이 가정이 유지되는 상수 $c$가 존재함을 보인다. 가정대로라면 $S(0.2n) \le 0.2cn$, $S(0.7n) \le 0.7cn$이므로 점화식에 대입하면:

$$
S(n) = 2n + S(0.2n) + S(0.7n) \le 2n + 0.2cn + 0.7cn = 2n + 0.9cn
$$

이 우변이 다시 $cn$ 이하가 되려면 $2n + 0.9cn \le cn$, 즉 $2 \le 0.1c$여야 한다. $c = 20$으로 잡으면 부등식이 성립하므로, $S(n) \le 20n = O(n)$이다.

핵심은 $0.2 + 0.7 = 0.9 < 1$이라는 점이다. 두 재귀의 크기 합이 $n$보다 작기 때문에 $0.1c \ge 2$를 만족하는 유한한 $c$가 존재하고, 그래서 선형 상한이 닫힌다. 이것이 median of medians 알고리즘이 최악에도 $O(n)$인 이유다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- **선택은 정렬보다 쉬운 문제다.** 정렬은 $n$개 선택 문제를 한꺼번에 푸는 것이고, 선택은 하나만 찾으면 된다. 하한은 $\Omega(n)$.
- **Quickselect**는 퀵 정렬의 분할을 재활용해 한쪽으로만 재귀한다. 평균 $O(n)$이지만 최악은 $O(n^2)$.
- **Approximate median**(가운데 40%)을 pivot으로 쓰면 재귀 크기가 최대 $0.7n$으로 줄어들어 최악을 통제할 수 있다.
- **Median of medians**는 5개씩 묶어 approximate median을 $O(n)$에 찾는다. 점화식 $S(n) = 2n + S(0.2n) + S(0.7n)$을 $S(n) \le cn$ 대입법으로 풀면 $c = 20$, 즉 최악에도 $O(n)$.
- 단, 상수 20과 메모리 오버헤드가 커서 **실전에서는 정렬 후 인덱싱이나 `std::nth_element`가 더 빠를 때가 많다.** Median of medians는 이론적 최악 보장이 중요한 상황에서 쓴다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>Quickselect의 평균이 정말 $O(n)$인지 기댓값으로 유도하려면 <a href="/blog/selection-average">quickselect 평균 O(n) 유도</a>를 보자. 왜 3개가 아닌 5개로 묶어야 하는지는 <a href="/blog/selection-why-five">왜 5개로 나누는가</a>에서 다룬다. 이 글의 바탕이 된 분할 알고리즘은 <a href="/blog/quicksort">퀵 정렬</a>에, 점화식을 푸는 일반 도구는 <a href="/blog/divide-and-conquer">분할 정복</a>에서 다룬다.</p>
</div>
