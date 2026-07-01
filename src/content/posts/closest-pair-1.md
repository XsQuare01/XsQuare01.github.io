---
title: "가장 가까운 점 쌍 ① — 분할 정복과 O(n log²n)"
date: 2026-06-30T09:00:00
description: "2차원 평면에서 가장 가까운 두 점을 찾는 문제. 모든 쌍을 보면 O(n²)이지만, 분할 정복으로 더 빠르게 풀 수 있다. x좌표로 좌우를 나눠 각 영역의 최소 거리 D를 구한 뒤, 경계의 폭 D 밴드만 합치는 과정을 보고 O(n log²n)임을 유도한다."
tags: ["Algorithm", "Closest Pair", "Divide and Conquer", "Computational Geometry"]
category: algorithm
difficulty: 고급
---

> 2차원 평면에 $n$개의 점이 흩어져 있다. 이 중 가장 가까운 두 점을 찾아라. 계산 기하(computational geometry)의 대표적인 문제로, 그림으로 보면 직관적이지만 막상 코드로 풀면 주의할 점이 많다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 브루트포스 $O(n^2)$과 더 빠른 풀이가 존재하는 이유
- 1차원 문제에서 얻는 직관 — 정렬이 왜 핵심인가
- x좌표로 좌우를 나누는 **분할 정복** 뼈대
- Combine 단계의 핵심: 폭 $D$ **밴드**와 "한 점은 다음 7개만 비교"
- 복잡도 유도: $O(n \log n) \times \log n$ 레벨 $= O(n \log^2 n)$
- C++ 구현 전체 코드 (거리 제곱 비교, `long long`)

</div>

---

## 문제와 브루트포스

입력은 2차원 좌표 $(x_1, y_1), (x_2, y_2), \ldots, (x_n, y_n)$이다. 두 점 $p_i$, $p_j$ 사이의 유클리드 거리는

$$
d(p_i, p_j) = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}
$$

이고, 이 값을 최소화하는 쌍을 찾으면 된다.

가장 단순한 풀이는 **모든 쌍**을 비교하는 것이다. $\binom{n}{2} = \frac{n(n-1)}{2}$ 쌍이 있으므로 $O(n^2)$이다.

이보다 빠를 수 없을까? 놀랍게도 목표는 **$O(n \log n)$** 이다. 그리고 이 목표가 합리적이라는 단서는 정렬에 있다. 가장 가까운 두 원소를 찾는 문제는 — 자세한 이유는 아래에서 살펴보겠지만 — 정렬과 동등한 수준의 어려움을 가진다. 정렬의 하한이 $\Omega(n \log n)$이니, 목표도 $O(n \log n)$이 된다.

이 글에서 유도하는 알고리즘은 $O(n \log^2 n)$이고, 2편에서 이를 $O(n \log n)$으로 개선한다.

---

## 1차원에서 먼저

본격적으로 2차원으로 가기 전에, **1차원**에서 같은 문제를 생각해 보자. 수직선 위에 $n$개의 수가 있을 때, 가장 가까운 두 수의 쌍을 찾아라.

직관적으로 바로 보인다. **정렬하면 끝이다.** 정렬하면 가장 가까운 쌍은 반드시 인접한 쌍 안에 있고, 인접한 $n-1$쌍을 한 번만 훑으면 된다. 전체 복잡도는 정렬 $O(n \log n)$.

그런데 왜 정렬을 해야만 하는가? 정렬 없이 가장 가까운 쌍을 찾을 수 있다면 $O(n \log n)$보다 빠를 수도 있지 않을까?

그렇지 않다. 정렬 없이 1차원 가장 가까운 쌍을 찾는 것은, 값들 사이에 일정 거리 이하인 두 값이 있는지 판별하는 것(uniqueness)과 계산 복잡도가 동등하다는 것이 알려져 있다. 이 판별 자체가 정렬만큼 어렵다. 따라서 1차원에서도 $\Omega(n \log n)$이 하한이고, 정렬 후 인접 쌍 비교가 최적이다.

2차원에서는 한 좌표만으로 거리를 판단할 수 없으니, 정렬만으로는 충분하지 않다. 여기서 [분할 정복](/blog/divide-and-conquer)이 등장한다.

---

## 2차원 분할 정복

분할 정복의 세 단계 — **나누기, 풀기, 합치기** — 를 가장 가까운 점 쌍 문제에 적용한다.

**나누기.** 점들을 **x좌표 기준으로 정렬**한 뒤, 중앙을 기준으로 왼쪽 절반과 오른쪽 절반으로 나눈다.

**풀기.** 왼쪽 절반에서 가장 가까운 거리 $D_L$을, 오른쪽 절반에서 $D_R$을 각각 재귀로 구한다. (귀납적으로 각 절반의 문제는 올바르게 풀린다고 가정한다.)

**합치기.** 두 영역의 최솟값을 합치면

$$
D = \min(D_L, D_R)
$$

그런데 이것만으로는 끝이 아니다. **분할선을 가로지르는 쌍**, 즉 한 점은 왼쪽 영역에, 다른 점은 오른쪽 영역에 있는 쌍도 확인해야 한다. 그리고 이 Combine 단계가 알고리즘의 핵심이다.

<div class="callout callout-simple">
<div class="callout-title">왜 x좌표만으론 거리 판단이 안 되는가</div>

x좌표 차이가 작아도 y좌표 차이가 크면 실제 거리는 멀 수 있다. 반대로 x좌표 차이가 $D$를 넘으면 — 그 쌍의 거리는 이미 $D$ 이상이므로 — 굳이 볼 필요가 없다. 즉, x좌표 차이가 $D$ 이내인 쌍만 살펴보면 된다. 이것이 밴드의 근거다.

</div>

---

## Combine: 경계의 밴드

합치기 단계에서 분할선을 가로지르는 쌍 중 현재 최솟거리 $D$보다 짧을 가능성이 있는 쌍은 어디에 있는가?

**양쪽으로 폭 $D$인 밴드** 안에 있는 점들이다. 분할선에서 x좌표 차이가 $D$를 넘는 쌍은, x좌표 차이만으로도 이미 거리가 $D$ 이상이기 때문에 $D$를 갱신할 수 없다.

![가장 가까운 점 쌍 — 분할선 좌우 폭 D 밴드. 밴드 밖 점(회색)은 Combine에 영향 없고, 밴드 안 점(파랑/초록)만 반대편과 비교한다.](/images/closest-pair/band.svg)

따라서 밴드 안 점들만 반대편의 밴드 점과 비교하면 된다.

그런데 이걸로 충분할까? **밴드 안 점이 너무 많으면 어떻게 되는가?** 최악의 경우, 모든 점이 밴드 안에 있을 수 있다. 그러면 밴드 안 점을 모두 비교하는 비용이 $O(n^2)$이 되어, 분할 정복을 쓴 의미가 없다.

이 문제를 해결하는 것이 다음 단계다.

---

## 한 점은 다음 7개만 비교하면 된다

밴드 안 점들을 **y좌표 순으로 정렬**하면, 한 점은 y좌표 기준으로 자신의 위쪽에 있는 최대 **7개** 점만 비교하면 된다는 사실이 알려져 있다.

<div class="callout callout-simple">
<div class="callout-title">왜 7개인가 — 기하 논거 (별도 글에서 증명)</div>

$D$는 왼쪽과 오른쪽 각 영역의 최솟거리다. 같은 편 두 점은 항상 거리 $\ge D$다. $P$ 위쪽으로 y 차이가 $D$ 미만인 범위는 폭 $2D$(분할선 좌우 각 $D$) × 높이 $D$인 직사각형이다. 이 직사각형을 한 변 $D/2$인 셀로 나누면 8개 셀이 나온다. 같은 편 제약으로 셀 안에 점이 최대 1개이므로, $P$ 포함 최대 8점 → 다음 **7개**면 충분하다. 자세한 논거는 [별도 글](/blog/closest-pair-five-points)에서 다룬다.

</div>

그러므로 Combine 알고리즘은 다음과 같다.

1. 밴드 안에 있는 점들(x좌표 차이의 제곱이 $d$ 이하인 점들, 여기서 $d$는 현재 최솟거리의 **제곱**)을 추린다.
2. 이 점들을 **y좌표로 정렬**한다.
3. 각 점에서 y좌표 기준 위쪽 7개 점과의 거리를 계산해 $d$를 갱신한다.

<div class="callout callout-simple">
<div class="callout-title">거리를 제곱으로 다루는 이유</div>

제곱근 계산은 부동소수점 오차를 유발할 수 있다. 두 거리를 비교할 때 $d_1 < d_2 \iff d_1^2 < d_2^2$ (두 값 모두 양수일 때)이므로, 제곱 상태로 저장하고 비교한다. 코드 전체에서 거리는 **제곱값**이며, 밴드 폭 비교도 x좌표 차이를 제곱해 $d$(거리 제곱)와 비교한다. 좌표값이 클 때 오버플로를 막기 위해 `long long`을 사용한다.

</div>

---

## 복잡도 — $O(n \log^2 n)$

재귀의 각 단계에서 비용이 어떻게 쌓이는지 분석한다.

**초기 정렬.** 맨 처음 x좌표로 전체를 정렬한다. $O(n \log n)$.

**Combine 비용 (한 레벨).** 재귀의 각 레벨에서 Combine을 수행한다. Combine에서는 밴드 안 점들을 y좌표로 정렬(최대 $O(n \log n)$)하고, 각 점에서 위 7개를 비교(최대 $O(n)$)한다. Combine이 끝나면 다음 단계의 Combine을 위해 구간을 x좌표로 **재정렬**해야 한다. 같은 레벨의 여러 서브문제에서 combine 비용을 모두 합산해도 $O(n \log n)$에 수렴한다($2 \cdot O(\tfrac{n}{2} \log \tfrac{n}{2}) = O(n \log n)$). 따라서 한 레벨의 비용은 $O(n \log n)$이다.

**재귀 깊이.** 매 단계 절반씩 나누므로 깊이는 $\log n$.

![가장 가까운 점 쌍 복잡도 — 재귀 트리 깊이 log n, 각 레벨 combine 비용 O(n log n). 전체 O(n log² n).](/images/closest-pair/complexity.svg)

따라서 전체 복잡도는

$$
O(n \log n) \times \log n = O(n \log^2 n)
$$

초기 x정렬 $O(n \log n)$은 재귀 비용 $O(n \log^2 n)$보다 낮은 차수이므로 지배항이 되지 않는다.

---

## 코드

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<ll, ll> pll;

// 두 점 사이 거리의 제곱 반환 (루트 회피, long long 사용)
ll dist2(pll a, pll b) {
    ll dx = a.first  - b.first;
    ll dy = a.second - b.second;
    return dx * dx + dy * dy;
}

// y좌표 오름차순 정렬용 비교 함수
bool compY(const pll& a, const pll& b) {
    return a.second < b.second;
}

// arr[st..ed] 는 x좌표로 정렬된 상태.
// 반환값: 이 구간에서 가장 가까운 두 점 거리의 제곱.
// 함수 종료 시 arr[st..ed] 는 x좌표로 재정렬됨.
ll divideAndConquer(vector<pll>& arr, int st, int ed) {
    // ── 기저 사례 ──────────────────────────────────────────────
    if (ed == st) return LLONG_MAX;           // 점 1개: 비교 불가
    if (ed - st == 1) return dist2(arr[st], arr[ed]); // 점 2개

    // 점 3개: 세 쌍 중 최솟값 직접 계산
    if (ed - st == 2) {
        ll d = min({ dist2(arr[st], arr[st+1]),
                     dist2(arr[st+1], arr[ed]),
                     dist2(arr[st], arr[ed]) });
        // x재정렬은 이미 정렬된 상태이므로 생략
        return d;
    }

    // ── 분할 + 재귀 ────────────────────────────────────────────
    int mid = (st + ed) / 2;
    ll le = divideAndConquer(arr, st, mid);   // 왼쪽 재귀
    ll ri = divideAndConquer(arr, mid + 1, ed); // 오른쪽 재귀
    ll d = min(le, ri);                       // 현재 최솟거리 제곱

    // ── Combine: 밴드 안 점 추리기 ────────────────────────────
    // x좌표 차이 제곱이 d 이하인 점만 밴드에 포함.
    // (실제 x거리 기준으론 √d = D이지만, 제곱으로 비교)
    ll midX = arr[mid].first;
    int le_idx = mid, ri_idx = mid + 1;

    while (le_idx > st &&
           (midX - arr[le_idx - 1].first) * (midX - arr[le_idx - 1].first) <= d)
        le_idx--;
    while (ri_idx < ed &&
           (arr[ri_idx + 1].first - midX) * (arr[ri_idx + 1].first - midX) <= d)
        ri_idx++;

    // ── 밴드 점을 y좌표로 정렬 ────────────────────────────────
    sort(arr.begin() + le_idx, arr.begin() + ri_idx + 1, compY);

    // ── 한 점에서 위쪽 최대 7개 비교 ─────────────────────────
    for (int i = le_idx; i <= ri_idx; i++) {
        for (int j = 1; j <= 7; j++) {
            if (i + j > ri_idx) break;
            ll td = dist2(arr[i], arr[i + j]);
            d = min(d, td);
        }
    }

    // ── x좌표로 재정렬 (상위 호출의 Combine을 위해) ───────────
    sort(arr.begin() + st, arr.begin() + ed + 1);

    return d;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<pll> arr(n);
    for (auto& [x, y] : arr) cin >> x >> y;

    // 초기 x좌표 정렬
    sort(arr.begin(), arr.end());

    ll ans = divideAndConquer(arr, 0, n - 1);
    // ans는 최솟거리의 제곱. 실제 거리가 필요하면 sqrt(ans).
    cout << ans << "\n";

    return 0;
}
```

**코드 흐름 요약:**

| 단계 | 설명 | 비용 |
|:---|:---|:---:|
| 초기 `sort` | x좌표 정렬 | $O(n \log n)$ |
| 기저 사례 | 크기 1·2·3에서 직접 계산 | $O(1)$ |
| 재귀 | 좌우 절반씩 분리해 반환값 = 거리 제곱 | — |
| 밴드 추리기 | x차이 제곱 $\le d$ 인 점만 선택 | $O(n)$ |
| y정렬 | 밴드 점을 y좌표로 정렬 | $O(n \log n)$ |
| 7개 비교 | 각 점에서 위 최대 7개 검사 | $O(n)$ |
| x재정렬 | 상위 레벨 Combine 준비 | $O(n \log n)$ |

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 가장 가까운 점 쌍 문제는 **계산 기하**의 대표적인 문제로, 브루트포스는 $O(n^2)$이다.
- **분할 정복** 접근: x좌표로 정렬 후 좌우 분할, 각각 재귀로 $D_L$, $D_R$을 구하고 $D = \min(D_L, D_R)$.
- Combine 단계에서 분할선 양쪽 폭 $D$인 **밴드** 안의 점만 비교하면 충분하다.
- 밴드 안 점을 y좌표로 정렬하면, 한 점은 위쪽 **최대 7개** 점만 비교해도 된다.
- 거리는 **제곱값**으로 다뤄 부동소수점 루트 계산을 피하고, `long long`으로 오버플로를 막는다.
- 각 재귀 레벨의 Combine 비용은 $O(n \log n)$, 재귀 깊이는 $\log n$이므로 전체 $O(n \log^2 n)$.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

이 알고리즘의 $O(n \log^2 n)$ 병목은 Combine마다 y정렬과 x재정렬을 반복하는 데 있다. [2편](/blog/closest-pair-2)에서는 이를 개선한다. 병합 정렬처럼 재귀가 y정렬된 결과를 물려주게 만들면, Combine에서 y정렬 대신 $O(n)$의 merge만 수행하면 된다. 이를 통해 전체 복잡도를 $O(n \log n)$으로 줄이는 과정을 다룬다. 그 다음 글에서는 Plane Sweeping 관점의 해석도 살펴본다.

분할 정복의 일반적인 뼈대와 점화식 분석은 [분할 정복](/blog/divide-and-conquer) 포스트에서, 정렬 알고리즘 전반은 [정렬](/blog/sort) 포스트에서 다룬다.

</div>
