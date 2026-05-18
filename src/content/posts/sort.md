---
title: "정렬 알고리즘 — Selection / Merge / Quick"
date: 2026-05-18T08:00:00
description: "선택 정렬, 병합 정렬, 퀵 정렬의 동작 원리를 코드 수준에서 살펴보고, 각 정렬의 올바름을 루프 불변식과 수학적 귀납법으로 증명한다. 시간 복잡도 $O(n^2)$, $O(n \\log n)$, 최악 $O(n^2)$/평균 $O(n \\log n)$의 차이가 어디서 오는지 정리한다."
tags: ["Algorithm", "Sorting", "Selection Sort", "Merge Sort", "Quick Sort"]
category: algorithm
difficulty: 입문
---

> 정렬은 알고리즘 수업의 단골 주제다. 같은 문제를 푸는 세 가지 방식이 각각 어떤 가정을 깔고 있고, 왜 복잡도가 갈리는지 들여다본다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>정렬 문제의 두 조건 — <strong>집합 조건</strong>과 <strong>정렬 조건</strong></li>
<li>Selection Sort — 반복문/재귀 두 형태와 루프 불변식 증명</li>
<li>Merge Sort — 분할 정복과 $T(n) = n + 2T(n/2) = O(n \log n)$ 유도</li>
<li>Quick Sort — pivot 기반 분할, 최선/최악 복잡도의 격차</li>
</ul>
</div>

## 정렬 문제의 두 조건

입력 배열을 $a[\,]$, 출력 배열을 $b[\,]$라 하자. "$b$는 $a$를 정렬한 결과"라는 말은 다음 두 조건을 동시에 만족한다는 뜻이다.

| 조건 | 의미 |
|---|---|
| **집합 조건** | $\{a[0], a[1], \ldots, a[n-1]\} = \{b[0], b[1], \ldots, b[n-1]\}$ |
| **정렬 조건** | $b[0] < b[1] < \cdots < b[n-1]$ |

집합 조건은 "값이 생겨나거나 사라지지 않는다"는 뜻이다. 정렬 조건은 "오름차순"이다. 이 글에서 다루는 세 알고리즘은 모두 **제자리 교환(swap)** 만 사용하므로, 집합 조건은 자연스럽게 보존된다. 증명의 무게는 **정렬 조건**에 실린다.

이 글은 중복이 없는 경우(strict less-than)를 가정한다. 같은 값이 있을 때는 $\le$로 바꾸면 모든 논의가 그대로 통한다.

---

## Selection Sort

**선택 정렬(Selection Sort)** 은 가장 직관적인 정렬이다. "남은 원소 중 가장 작은 것을 골라 앞으로 보낸다"를 끝까지 반복한다.

### 반복문 버전

```cpp
void sort(int a[], int n) {
    for (int i = 0; i < n; i++) {
        // 1. a[i..n-1] 중 최솟값의 인덱스를 찾는다
        int m = i;
        for (int j = i; j < n; j++) {
            if (a[m] > a[j]) m = j;
        }
        // 2. 최솟값을 i번째 자리로 보낸다
        int t = a[i];
        a[i] = a[m];
        a[m] = t;
    }
}
```

### 정렬됨의 증명 — 루프 불변식

핵심 도구는 **루프 불변식(Loop Invariant)** 이다.

> **불변식 $I_k$:** $k$번째 바깥쪽 루프가 끝난 직후,
> 1. $a[0] < a[1] < \cdots < a[k-1]$ (앞쪽이 정렬되어 있다)
> 2. 모든 $x \ge k$에 대해 $a[k-1] < a[x]$ (앞쪽의 마지막 원소가 뒤쪽 전체보다 작다)

$n$번째 루프가 끝난 후, 조건 1에 의해 $a[0] < a[1] < \cdots < a[n-1]$이 성립한다. 조건 2는 $x > n-1$인 $x$가 없으므로 [vacuously true](/blog/algo-orientation)다. 따라서 불변식이 매 단계 유지되면 정렬이 완성된다.

![Selection Sort 루프 불변식 — k=3에서 앞쪽 3칸은 정렬되고 뒤쪽은 모두 a[2]보다 큰 상태](/images/sort/selection-sort-invariant.svg)

**불변식의 귀납적 증명:**

- **Base ($k = 0$):** 두 조건 모두 "$a[-1]$"이 등장하므로 공백 조건이다. Vacuously true.
- **Step ($k$ → $k+1$):** $I_k$가 성립한다고 가정.
  1. 조건 2에 의해 $a[k]$ 이후의 원소들은 모두 $a[k-1]$보다 크다. $(k+1)$번째 루프는 그 중 **최솟값**을 $a[k]$ 자리로 옮기므로, 새로운 $a[k]$ 역시 $a[k-1]$보다 크다. 따라서 $a[0] < a[1] < \cdots < a[k]$가 성립한다.
  2. 같은 루프에서 $a[k]$는 $a[k..n-1]$의 최솟값이므로, 이후 모든 $x > k$에서 $a[k] < a[x]$.

두 조건이 모두 성립하므로 $I_{k+1}$이 참. 귀납에 의해 모든 $k$에서 $I_k$가 성립한다. $\square$

### 재귀 버전

같은 알고리즘을 재귀로 쓰면 한결 짧다.

```cpp
void sort(int a[], int n) {
    if (n <= 1) return;     // Base
    int m = 0;
    for (int j = 0; j < n; j++) {
        if (a[m] > a[j]) m = j;
    }
    // 가장 작은 원소를 맨 앞으로
    int t = a[0]; a[0] = a[m]; a[m] = t;
    sort(a + 1, n - 1);     // 나머지 n-1개를 재귀 정렬
}
```

핵심 통찰은 이렇다. "전체에서 가장 작은 원소가 맨 앞으로 왔다면, 나머지만 잘 정렬되면 전체가 정렬된 것이다."

### 재귀 버전의 증명

명제 $P(n)$을 "`sort(a, n)`이 길이 $n$의 배열을 올바르게 정렬한다"로 두자.

- **Base ($n = 1$):** 길이 1 배열은 이미 정렬되어 있다. 코드는 즉시 반환한다. 성립.
- **Step:** $P(n-1)$이 참이라 가정. 길이 $n$ 배열에서:
  1. for문 종료 후 $a[0]$은 $a[0..n-1]$ 중 최솟값이다. 즉, 모든 $x > 0$에 대해 $a[0] < a[x]$.
  2. `sort(a+1, n-1)`은 귀납 가정에 의해 $a[1..n-1]$을 올바르게 정렬한다. 따라서 $a[1] < a[2] < \cdots < a[n-1]$.
  3. 1번에 의해 $a[0] < a[1]$도 성립하므로, $a[0] < a[1] < \cdots < a[n-1]$. $P(n)$이 참.

귀납에 의해 모든 $n \ge 1$에서 $P(n)$이 성립한다. $\square$

### 시간 복잡도

바깥쪽 루프는 $n$번, 안쪽 비교는 평균 $n/2$번. 총 비교 횟수는 $\frac{n(n-1)}{2} = \Theta(n^2)$.

$$T(n) = \Theta(n^2)$$

최선/평균/최악 모두 같다. 입력 분포에 무관하게 항상 $n^2$이다.

---

## Merge Sort

**병합 정렬(Merge Sort)** 의 아이디어는 한 문장으로 요약된다.

> **정렬된 두 배열을 합치면 정렬된 배열을 만들 수 있다.** 그러니 배열을 반으로 쪼개 각각 정렬하고, 그 결과를 합치자.

쪼개진 부분 배열은 또 같은 방식으로 정렬한다 — 자연스러운 재귀 구조다.

### Merge 단계

두 정렬된 배열을 합치는 연산은 **두 포인터(two-pointer)** 로 단순하게 수행된다. 각 배열의 앞부터 작은 값을 골라 결과 배열에 차례로 채운다.

![Merge 단계 — 왼쪽 i, 오른쪽 j 두 포인터로 작은 값을 결과 배열 k에 채우기](/images/sort/merge-step.svg)

```cpp
void merge(int a[], int h, int n, int b[]) {
    // a[0..h-1], a[h..n-1]는 각각 정렬되어 있다고 가정
    int i = 0, j = h, k = 0;
    while (i < h && j < n) {
        if (a[i] <= a[j]) b[k++] = a[i++];
        else              b[k++] = a[j++];
    }
    while (i < h) b[k++] = a[i++];
    while (j < n) b[k++] = a[j++];
    for (int x = 0; x < n; x++) a[x] = b[x];
}
```

각 단계는 $O(1)$이며 포인터는 한쪽씩만 전진하므로, 길이 $n$의 두 배열을 합치는 데 **$O(n)$** 이 든다.

### 재귀 코드

```cpp
void sort(int a[], int n) {
    if (n <= 1) return;     // Base
    int h = n / 2;
    sort(a, h);             // 왼쪽 절반 정렬
    sort(a + h, n - h);     // 오른쪽 절반 정렬
    int b[n];
    merge(a, h, n, b);      // 두 정렬 결과를 합쳐 a[]에 덮어쓰기
}
```

### 정렬됨의 증명

명제 $P(n)$: "`sort(a, n)`은 $a[\,]$를 올바르게 정렬한다."

- **Base ($n \le 1$):** 즉시 반환. 정렬 필요 없음.
- **Step:** $P(k)$가 모든 $k < n$에서 참이라 가정 (강한 귀납법). 길이 $n$ 배열에서:
  1. `sort(a, h)`는 귀납 가정($h < n$)에 의해 $a[0..h-1]$을 정렬한다.
  2. `sort(a+h, n-h)`도 마찬가지로 $a[h..n-1]$을 정렬한다.
  3. `merge`가 올바르다면, 두 정렬된 부분을 합친 결과는 전체 정렬이다.

`merge` 자체의 올바름은 두 포인터의 진행 규칙에 대한 또 다른 불변식 증명으로 보일 수 있다(생략). $\square$

집합 조건은 코드 어디서도 값을 새로 만들거나 버리지 않으므로 자동 보존된다.

### 시간 복잡도 — $O(n \log n)$ 유도

merge 비용 $cn$과 두 번의 재귀 호출로 점화식이 세워진다.

$$T(n) = 2T\!\left(\frac{n}{2}\right) + cn$$

전개하면 다음과 같다.

$$
\begin{aligned}
T(n) &= 2T(n/2) + cn \\
     &= 2\bigl(2T(n/4) + c(n/2)\bigr) + cn = 4T(n/4) + 2cn \\
     &= 8T(n/8) + 3cn \\
     &\;\;\vdots \\
     &= 2^{\log_2 n} T(1) + cn \log_2 n \\
     &= n + cn \log_2 n \\
     &= O(n \log n)
\end{aligned}
$$

[재귀 트리](/blog/recursion#재귀-트리-분석)로도 같은 결과를 얻는다. 각 레벨의 총 작업량이 $cn$으로 같고, 트리 깊이가 $\log_2 n$이므로 총합 $cn \log_2 n$.

$$T(n) = \Theta(n \log n)$$

입력에 무관하게 최선·평균·최악 모두 $\Theta(n \log n)$이다. 대신 추가 배열 $b[\,]$를 위한 $O(n)$ 메모리가 필요하다.

---

## Quick Sort

**퀵 정렬(Quick Sort)** 도 분할 정복이지만 분할 방식이 다르다. 정확히 반으로 자르지 않고, **pivot**이라 부르는 한 원소를 기준으로 "작은 것은 왼쪽, 큰 것은 오른쪽"으로 나눈다.

### 알고리즘

배열 $a[\,]$에서 pivot $p$를 하나 고른다(여기서는 $a[0]$). 다음을 만족하도록 $a$를 재배치한다.

- $a[d] = p$
- $a[0], a[1], \ldots, a[d-1] < p$
- $a[d+1], a[d+2], \ldots, a[n-1] > p$

![Quick Sort partition — pivot 7을 기준으로 작은 값은 왼쪽, 큰 값은 오른쪽으로 재배치](/images/sort/quicksort-partition.svg)

이 재배치 이후 $a[d]$의 자리는 **이미 최종 위치**다. pivot보다 작은 모든 값이 왼쪽에, 큰 모든 값이 오른쪽에 있으므로 $a[d]$의 인덱스가 곧 정렬 후의 자리다. 남은 일은 왼쪽 영역과 오른쪽 영역을 각각 재귀적으로 정렬하는 것뿐이다.

### 재귀 코드

```cpp
void qsort(int a[], int n) {
    if (n <= 0) return;     // Base
    int p = a[0];           // pivot
    int d = partition(a, n, p);
    // 이 시점에서:
    //   a[d] == p
    //   a[0], ..., a[d-1] < p
    //   a[d+1], ..., a[n-1] > p
    qsort(a, d);             // 왼쪽 영역
    qsort(a + d + 1, n - d - 1);  // 오른쪽 영역
}
```

`partition`이 어떻게 $d$를 정하는지는 구현 디테일이다. pivot의 위치는 입력에 따라 달라지며, **양쪽 영역의 크기가 같다는 보장은 없다**. 미리 위치를 통제할 필요도 없다 — 양쪽이 서로 독립적이기 때문이다.

### 정렬됨의 증명

명제 $P(n)$: "`qsort(a, n)`은 $a[\,]$를 올바르게 정렬한다."

- **Base ($n \le 0$):** 정렬할 원소가 없다. 즉시 반환.
- **Step:** $P(k)$가 모든 $k < n$에서 참이라 가정.
  1. partition 직후, 모든 $x < d$에 대해 $a[x] < p = a[d]$이고, 모든 $y > d$에 대해 $a[y] > a[d]$.
  2. `qsort(a, d)`는 귀납 가정에 의해 $a[0..d-1]$을 정렬한다. 그 결과 $a[0] < a[1] < \cdots < a[d-1]$. 또한 이 호출은 집합 조건을 유지하므로, 정렬 후에도 모든 $a[x]\,(x < d)$가 여전히 $p$보다 작다.
  3. `qsort(a+d+1, n-d-1)`도 마찬가지로 $a[d+1..n-1]$을 정렬하고, 그 값들은 여전히 $p$보다 크다.
  4. 따라서 $a[d-1] < a[d] < a[d+1]$이 성립하고, 전체적으로 $a[0] < \cdots < a[d-1] < a[d] < a[d+1] < \cdots < a[n-1]$. $P(n)$이 참. $\square$

### 시간 복잡도

partition은 $O(n)$이다. 점화식은 pivot이 어디로 가느냐에 달려 있다.

- **최선 (pivot이 항상 중앙):** $T(n) = 2T(n/2) + cn = \Theta(n \log n)$. Merge Sort와 동일.
- **최악 (pivot이 항상 끝):** 한쪽은 길이 0, 다른 쪽은 $n-1$. $T(n) = T(n-1) + cn = \Theta(n^2)$. Selection Sort와 유사.

이미 정렬된 배열에 항상 $a[0]$을 pivot으로 잡으면 정확히 최악 경우가 된다.

### 그런데 왜 빠른가?

이론적 최악 복잡도가 $O(n^2)$인데도 Quick Sort는 실제로 Merge Sort보다 종종 **2배 이상** 빠르다. 이유를 정리하면 다음과 같다.

- **평균 복잡도가 $O(n \log n)$.** 무작위로 pivot을 고르면 최악 경우의 확률이 무시 가능할 만큼 작아진다.
- **제자리 정렬(in-place).** Merge Sort가 매 단계 추가 배열을 쓰는 반면, Quick Sort는 원본 배열 안에서 교환만으로 분할이 가능하다. 캐시 지역성이 좋고 메모리 할당 오버헤드가 없다.
- **상수 계수가 작다.** partition은 단순한 비교·교환의 반복이라 분기 예측이 잘 맞고, 한 번의 패스로 끝난다.

세 가지가 합쳐져, 같은 $\Theta(n \log n)$이라도 실측 성능 차이가 크게 벌어진다.

---

## 세 알고리즘 비교

| | Selection Sort | Merge Sort | Quick Sort |
|---|---|---|---|
| 최선 | $\Theta(n^2)$ | $\Theta(n \log n)$ | $\Theta(n \log n)$ |
| 평균 | $\Theta(n^2)$ | $\Theta(n \log n)$ | $\Theta(n \log n)$ |
| 최악 | $\Theta(n^2)$ | $\Theta(n \log n)$ | $\Theta(n^2)$ |
| 추가 메모리 | $O(1)$ | $O(n)$ | $O(1)$ |
| 입력 의존성 | 없음 | 없음 | pivot 선택에 민감 |
| 핵심 아이디어 | 매 단계 최솟값 선택 | 분할 + 병합 | 분할 + pivot 배치 |

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>정렬의 올바름은 <strong>집합 조건</strong>과 <strong>정렬 조건</strong> 두 축으로 증명한다. 교환만 쓰는 알고리즘에서는 집합 조건이 자동 보존되므로, 무게중심은 정렬 조건에 있다.</li>
<li><strong>Selection Sort:</strong> "남은 영역의 최솟값을 앞으로"라는 그리디 규칙. 루프 불변식 "$a[k-1]$이 뒤쪽 전체보다 작다"로 정렬됨을 증명한다. 모든 경우 $\Theta(n^2)$.</li>
<li><strong>Merge Sort:</strong> 분할 정복 + 두 포인터 병합. $T(n) = 2T(n/2) + cn = \Theta(n \log n)$. 입력에 무관하지만 추가 메모리 $O(n)$이 필요하다.</li>
<li><strong>Quick Sort:</strong> pivot 기반 분할로 $a[d]$가 한 번에 최종 자리에 들어간다. 평균 $\Theta(n \log n)$, 최악 $\Theta(n^2)$. 제자리 정렬이라 실측 성능이 좋다.</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>그리디 알고리즘 — 매 순간 가장 좋아 보이는 선택</strong> — 매 단계 가장 좋아 보이는 선택을 하고 번복하지 않는 그리디의 정의를 살펴본다. Selection Sort로 그리디가 통하는 예를, Shortest Path로 그리디가 무너지는 예를 비교한다.</p>
</div>
