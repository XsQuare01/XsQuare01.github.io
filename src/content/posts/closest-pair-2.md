---
title: "가장 가까운 점 쌍 ② — 정렬을 유지해 O(n log n)으로"
date: 2026-07-01T09:00:00
description: "1편의 O(n log²n)에서 여분의 log n은 combine마다 y정렬을 새로 하는 데서 나온다. merge sort처럼 재귀가 y좌표로 정렬된 결과를 반환하게 만들면, combine은 y정렬 대신 O(n) merge만 하면 된다. 분할은 x로, 순서는 y로 유지하는 미묘한 지점을 짚고 전체를 O(n log n)으로 끌어내린다."
tags: ["Algorithm", "Closest Pair", "Divide and Conquer", "Computational Geometry"]
category: algorithm
difficulty: 고급
---

> [가장 가까운 점 쌍 ①](/blog/closest-pair-1)에서 분할 정복으로 $O(n \log^2 n)$ 풀이를 얻었다. 이제 여분의 $\log n$을 어디서 흘리고 있는지 찾아, merge sort의 아이디어로 이를 $O(n \log n)$까지 끌어내린다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 1편의 $O(n \log^2 n)$에서 **여분의 $\log n$이 나온 곳** — combine마다 반복하는 정렬
- merge sort처럼 **재귀가 y정렬된 결과를 반환**하게 만드는 아이디어
- 미묘한 지점: **분할은 x좌표로, 순서는 y좌표로** 유지하기
- combine의 y정렬을 $O(n)$ **merge**로 대체하기
- 복잡도 유도: $T(n) = 2T(n/2) + O(n) = O(n \log n)$
- C++ 구현 전체 코드

</div>

---

## 여분의 log n은 어디서 왔나

1편의 복잡도를 다시 보자. 재귀 깊이는 $\log n$이고, **각 레벨의 combine 비용이 $O(n \log n)$** 이었다. 그래서 전체가 $O(n \log^2 n)$이 됐다.

그런데 왜 한 레벨의 combine이 $O(n \log n)$이나 들었는가? combine 안을 뜯어보면 답이 보인다.

1. 밴드 안 점을 추린다 — $O(n)$
2. 밴드 점을 **y좌표로 정렬한다** — $O(n \log n)$ ← 여기
3. 각 점에서 위쪽 7개를 비교한다 — $O(n)$
4. 상위 레벨을 위해 구간을 **x좌표로 재정렬한다** — $O(n \log n)$ ← 여기

$O(n)$이면 충분할 combine을, 정렬 두 번 때문에 $O(n \log n)$으로 쓰고 있다. 이 반복 정렬만 없애면 combine이 $O(n)$이 되고, 전체는 $\log n$이 하나 빠진 $O(n \log n)$이 된다.

핵심 질문은 이것이다. **매번 y정렬을 새로 하지 않을 수 없을까?**

---

## Merge Sort에서 빌려 오는 아이디어

[merge sort](/blog/divide-and-conquer)을 떠올려 보자. merge sort는 두 절반을 각각 정렬한 뒤, 이미 정렬된 두 배열을 **merge**로 합친다. 이미 정렬된 것끼리는 앞에서부터 훑으며 $O(n)$에 하나로 합칠 수 있다. 새로 정렬할 필요가 없다.

같은 발상을 combine에 적용한다.

**재귀가 최솟거리뿐 아니라, 그 구간을 y좌표로 정렬한 결과까지 남기게 만든다.** 그러면 combine 시점에 왼쪽 절반과 오른쪽 절반은 *이미 각각 y정렬돼 있다.* 밴드를 위한 y정렬을 새로 할 필요가 없다. 두 절반을 $O(n)$ merge로 합치면 구간 전체가 y정렬되고, 이 결과를 그대로 상위 호출에 물려준다.

<div class="callout callout-simple">
<div class="callout-title">한 줄 요약</div>

1편은 combine마다 y정렬을 **새로** 했다. 2편은 재귀가 y정렬 결과를 **물려주고**, combine은 두 y정렬 절반을 $O(n)$ merge로 합칠 뿐이다. 정렬을 버리지 않고 재활용하는 것이 전부다.

</div>

![y좌표로 정렬된 두 절반을 O(n) merge로 합쳐 구간 전체를 y정렬로 만든다. 새로 정렬하지 않고 앞에서부터 훑기만 한다.](/images/closest-pair-2/merge.svg)

---

## 미묘한 지점 — 분할은 x, 순서는 y

여기에 함정이 하나 있다. 분할 정복의 **나누기**는 여전히 x좌표 기준이어야 한다. 좌우를 x좌표 중앙값으로 갈라야 밴드 논리(x차이가 $D$를 넘으면 볼 필요 없음)가 성립하기 때문이다.

그런데 재귀가 배열을 **y좌표 순서로 흐트러뜨린다.** 그러면 "x좌표 중앙"을 어떻게 잡는가?

해법은 두 정렬 기준을 분리하는 것이다.

- **분할 경계는 처음 한 번의 x정렬로 고정한다.** 맨 처음 전체를 x좌표로 정렬해 두면, 인덱스 구간 `[st, ed]`의 중앙 `mid = (st+ed)/2`가 곧 x좌표 중앙이다. 재귀에 들어가기 **전에** 분할선의 x좌표(`midX = pts[mid].x`)를 읽어 둔다.
- **구간 내부의 순서는 y정렬로 유지한다.** 재귀가 반환하면서 구간을 y정렬로 남기므로, combine의 밴드 비교는 y순서 위에서 이뤄진다.

<div class="callout callout-simple">
<div class="callout-title">왜 midX를 재귀 전에 읽어야 하는가</div>

`solve(st, mid, ...)`와 `solve(mid+1, ed, ...)`를 호출하고 나면 그 구간들이 **y좌표로 재배열**된다. 그러면 `pts[mid]`에 들어 있던 점이 바뀌어, `pts[mid].x`는 더 이상 분할선의 x좌표가 아니다. 그래서 분할선 x좌표는 재귀를 부르기 **전에** 지역 변수(`midX`)에 저장해 둬야 한다. 인덱스 경계 `mid` 자체는 변하지 않지만, 그 자리의 **값**은 변한다는 점이 핵심이다.

</div>

밴드에 넣을지 판단할 때도 이 `midX`를 쓴다. 각 점의 x좌표와 `midX`의 차이가 (제곱 기준으로) 현재 최솟거리 이하이면 밴드에 포함한다. 밴드는 이미 y정렬된 배열을 순서대로 훑으며 뽑으므로, 밴드 자체도 y정렬 상태를 유지한다. 여기서도 추가 정렬이 없다.

---

## 코드

1편과 달라진 곳은 combine의 두 정렬이다. y정렬은 **merge**로, x재정렬은 아예 **삭제**된다(순서를 y로 물려주므로 상위 호출이 x정렬을 기대하지 않는다).

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
struct P { ll x, y; };

// 두 점 사이 거리의 제곱 (루트 회피, long long 사용)
ll dist2(const P& a, const P& b) {
    ll dx = a.x - b.x;
    ll dy = a.y - b.y;
    return dx * dx + dy * dy;
}

// y좌표 오름차순 비교
bool byY(const P& a, const P& b) { return a.y < b.y; }

// pts[st..ed] 는 (전체 x정렬 덕분에) x좌표로 정렬된 구간.
// 반환값: 이 구간의 가장 가까운 두 점 거리의 제곱.
// 함수 종료 시 pts[st..ed] 는 y좌표로 정렬됨.
ll solve(vector<P>& pts, int st, int ed, vector<P>& buf) {
    // ── 작은 구간: 직접 비교 후 y정렬 ────────────────────────
    if (ed - st < 3) {
        ll d = LLONG_MAX;
        for (int i = st; i <= ed; i++)
            for (int j = i + 1; j <= ed; j++)
                d = min(d, dist2(pts[i], pts[j]));
        sort(pts.begin() + st, pts.begin() + ed + 1, byY);
        return d;
    }

    // ── 분할선 x좌표는 재귀 전에 확보 (재귀가 y로 재배열하므로) ─
    int mid = (st + ed) / 2;
    ll midX = pts[mid].x;

    ll dl = solve(pts, st, mid, buf);       // 왼쪽 재귀 → 왼쪽이 y정렬됨
    ll dr = solve(pts, mid + 1, ed, buf);   // 오른쪽 재귀 → 오른쪽이 y정렬됨
    ll d = min(dl, dr);

    // ── combine ①: 두 y정렬 절반을 O(n) merge (정렬 아님!) ────
    merge(pts.begin() + st,      pts.begin() + mid + 1,
          pts.begin() + mid + 1, pts.begin() + ed + 1,
          buf.begin() + st, byY);
    copy(buf.begin() + st, buf.begin() + ed + 1, pts.begin() + st);
    // 이제 pts[st..ed] 전체가 y정렬 상태 (그대로 상위 호출에 물려줌)

    // ── combine ②: 밴드 추리기 (y순서 유지) ──────────────────
    // x차이 제곱이 d 이하인 점만. d 는 거리의 제곱임에 유의.
    vector<P> band;
    for (int i = st; i <= ed; i++) {
        ll dx = pts[i].x - midX;
        if (dx * dx <= d) band.push_back(pts[i]);
    }

    // ── combine ③: 각 점에서 y순으로 다음 7개 비교 ───────────
    for (int i = 0; i < (int)band.size(); i++)
        for (int j = i + 1; j <= i + 7 && j < (int)band.size(); j++)
            d = min(d, dist2(band[i], band[j]));

    return d;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<P> pts(n);
    for (auto& p : pts) cin >> p.x >> p.y;

    // 초기 x좌표 정렬 (분할 경계의 기준, 딱 한 번)
    sort(pts.begin(), pts.end(),
         [](const P& a, const P& b) { return a.x < b.x; });

    vector<P> buf(n);                 // merge 임시 버퍼
    ll ans = solve(pts, 0, n - 1, buf);
    // ans 는 최솟거리의 제곱. 실제 거리가 필요하면 sqrt(ans).
    cout << ans << "\n";

    return 0;
}
```

**1편과 달라진 점:**

| 구분 | 1편 ($O(n \log^2 n)$) | 2편 ($O(n \log n)$) |
|:---|:---|:---|
| combine의 y정렬 | 매번 `sort` — $O(n \log n)$ | `merge` — $O(n)$ |
| combine의 x재정렬 | 매번 `sort` — $O(n \log n)$ | **없음** (y순서로 물려줌) |
| 재귀 반환 후 구간 | x정렬 상태 | y정렬 상태 |
| 분할선 x좌표 | 그때그때 `arr[mid]` | 재귀 전 `midX`에 확보 |

<div class="callout callout-simple">
<div class="callout-title">`long long`이 안전한 범위</div>

`dist2`가 계산하는 `dx * dx + dy * dy`는 좌표 범위가 정해져 있어야 오버플로 없이 `long long`에 담긴다. 이 문제의 좌표는 $[0,\ 10^9)$이므로 $dx, dy$의 절댓값이 $10^9$ 미만이고, 제곱거리는 최대 $2 \times (10^9)^2 = 2 \times 10^{18}$로 `long long` 상한($\approx 9.2 \times 10^{18}$) 안에 들어간다. 좌표 범위가 이보다 크면 곱셈 단계에서 이미 넘칠 수 있으므로, 중간 계산을 `__int128`로 올리거나 좌표를 적절히 평행이동해 범위를 줄여야 한다.

</div>

---

## 복잡도 — O(n log n)

이제 한 레벨의 combine 비용을 다시 계산한다.

- merge: $O(n)$
- 밴드 추리기: $O(n)$
- 각 점에서 다음 7개 비교: $7n = O(n)$

정렬이 사라졌으므로 combine은 통틀어 $O(n)$이다. 크기 $n$ 문제를 절반 두 개로 나누므로 점화식은

$$
T(n) = 2\,T\!\left(\tfrac{n}{2}\right) + O(n)
$$

이는 merge sort와 **같은 점화식**이고, 대입법으로 풀면 $T(n) = O(n \log n)$이다. (유도 과정은 [분할 정복](/blog/divide-and-conquer) 참고.)

![복잡도 O(n log n) — 재귀 깊이 log n, 각 레벨 combine 비용이 정렬 제거로 O(n)이 되어 레벨 합이 O(n)씩, 전체 O(n log n).](/images/closest-pair-2/complexity.svg)

맨 처음의 x정렬 $O(n \log n)$은 딱 한 번뿐이라 지배항을 바꾸지 않는다. 정렬의 하한 $\Omega(n \log n)$을 생각하면, 가장 가까운 점 쌍 문제는 이제 **이론적 하한에 도달**한 셈이다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 1편의 여분의 $\log n$은 combine마다 하는 **y정렬과 x재정렬**에서 나왔다.
- merge sort처럼 **재귀가 y정렬된 결과를 반환**하게 만들면, combine은 두 절반을 $O(n)$ **merge**로 합칠 뿐이다.
- 분할 경계는 x좌표 기준이어야 하므로, 처음 한 번 x정렬로 고정하고 **분할선 x좌표를 재귀 전에 확보**한다. 구간 내부 순서는 y정렬로 유지한다.
- combine이 $O(n)$이 되어 점화식이 $T(n) = 2T(n/2) + O(n) = O(n \log n)$으로 떨어진다.
- 이는 정렬의 하한 $\Omega(n \log n)$과 같은 차수로, **이론적으로 최적**이다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

분할 정복이 아닌 다른 시선으로도 같은 $O(n \log n)$에 닿을 수 있다. 점들을 x좌표 순으로 훑으며 "현재 위치에서 폭 $D$ 안의 점들"만 후보로 관리하는 **Plane Sweeping**(평면 훑기) 관점을, 균형 이진 탐색 트리와 함께 다음 글에서 다룬다.

분할 정복의 뼈대와 merge sort의 점화식 분석은 [분할 정복](/blog/divide-and-conquer) 포스트에서, "왜 다음 7개만 비교하면 되는가"는 [별도 글](/blog/closest-pair-five-points)에서 다룬다.

</div>
