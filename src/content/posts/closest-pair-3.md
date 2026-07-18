---
title: "가장 가까운 점 쌍 ③ — Plane Sweeping과 균형 이진 탐색 트리"
date: 2026-07-02T09:00:00
description: "2편과 같은 O(n log n)에 다른 시선으로 닿는다. 점을 x좌표 순으로 훑으며 폭 D 안의 점만 균형 BST(std::set)에 담는 Plane Sweeping으로, y좌표 [y-D, y+D] 구간만 조회한다. 후보가 상수 개임을 보여 전체 O(n log n)을 유도한다."
tags: ["Algorithm", "Closest Pair", "Plane Sweeping", "Computational Geometry"]
category: algorithm
difficulty: 고급
numbered: true
---

> [①](/blog/closest-pair-1)·[②](/blog/closest-pair-2)에서 분할 정복으로 $O(n \log n)$에 닿았다. 이번엔 분할도 재귀도 없이, 점들을 왼쪽에서 오른쪽으로 **한 번 훑으면서** 같은 복잡도에 닿는다. 무기는 균형 이진 탐색 트리다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 분할 정복에서 **훑기(Plane Sweeping)** 로 시선 옮기기
- 현재 위치 왼쪽 폭 $D$ 안의 점만 남기는 **활성 집합**과 활성 구간의 왼쪽 밀어내기
- 활성 집합을 y좌표로 정렬해 두고 **$[y-D,\ y+D]$ 구간만 조회**하기
- 조회되는 후보가 **상수 개**임을 (1편의 칸 세기로) 다시 확인
- 균형 이진 탐색 트리(`std::set`)로 삽입·삭제·구간 조회를 각각 $O(\log n)$에
- C++ 구현 전체 코드와 복잡도 유도: $O(n \log n)$

</div>

---

## 분할 정복에서 훑기로

2편까지의 풀이는 문제를 절반으로 **쪼개고**, 각 절반을 푼 뒤 경계를 **합쳤다.** 이번엔 쪼개지 않는다. 점들을 x좌표가 작은 것부터 큰 것 순으로 **한 줄로 세워 놓고, 왼쪽부터 오른쪽으로 한 점씩 훑는다.** 상상 속의 수직선 하나가 왼쪽에서 오른쪽으로 쓸고 지나간다고 보면 된다. 이 수직선을 **sweep line**이라 부르고, 이런 접근을 **Plane Sweeping**(평면 훑기)이라 한다.

훑는 도중 우리는 **현재까지 본 점들 사이의 최솟거리 $D$**(정확히는 그 제곱 `best`)를 계속 들고 다닌다. 새 점 $P$를 만날 때마다 묻는다. *"지금까지 본 점들 중, $P$와의 거리가 $D$보다 짧은 점이 있는가?"* 있으면 $D$를 줄이고, 없으면 그대로 둔 채 다음 점으로 넘어간다. 마지막 점까지 훑고 나면 $D$가 곧 정답이다.

<div class="callout callout-simple">
<div class="callout-title">한 줄 요약</div>

분할 정복은 "나눠서 각각 풀고 경계를 합친다". Plane Sweeping은 "한 번 훑으며, 지금 점과 가까울 수 있는 이웃만 그때그때 확인한다". 핵심은 **"가까울 수 있는 이웃"을 어떻게 좁은 후보로 가두느냐**다.

</div>

문제는 그 질문("$P$보다 가까운 점이 있는가")을 매번 $O(n)$에 훑으면 전체가 다시 $O(n^2)$이 된다는 것이다. 분할 정복에서 밴드로 후보를 좁혔듯, 여기서도 $P$와 가까울 수 있는 점을 **상수 개**로 가두는 장치가 필요하다.

---

## 활성 집합 — 폭 D의 활성 구간

$P$의 x좌표를 $x_P$라 하자. x좌표 차이가 $D$를 넘는 점은 그 차이만으로 이미 거리가 $D$ 이상이므로 $P$의 후보가 될 수 없다. 우리는 x가 작은 순으로 훑고 있으니, $P$보다 **왼쪽**에 있으면서 x좌표가 $x_P - D$ 이상인 점들만 후보다.

<div class="thm def">
<div class="thm-head">정의 1<span class="en">active set</span></div>

sweep line이 점 $P$(x좌표 $x_P$)에 있을 때, x좌표가 $[x_P - D,\ x_P]$에 있는 (이미 처리된) 점들의 모음을 **활성 집합(active set)** 이라 한다.

</div>

훑기가 진행되며 sweep line이 오른쪽으로 갈수록,

- **오른쪽 끝**으로는 새로 만난 점 $P$가 들어오고,
- **왼쪽 끝**으로는 x좌표가 $x_P - D$보다 작아진 점들이 빠져나간다.

폭 $D$짜리 **활성 구간**이 sweep line을 따라 오른쪽으로 미끄러지는 그림이다. 이렇게 폭이 고정된 구간을 이동시키며 양 끝에서 원소를 넣고 빼는 기법을 **슬라이딩 윈도우(sliding window)** 라 한다.

![Plane Sweeping — x좌표 순으로 세운 점들 위를 sweep line이 훑는다. 현재 점 P 왼쪽 폭 D 안의 점만 활성 집합(파랑)으로 남고, x가 x_P−D보다 작아진 점(회색)은 활성 구간에서 빠져나간다. P는 활성 집합 중 y가 [y_P−D, y_P+D]인 점(초록)만 비교한다.](/images/closest-pair-3/sweep.svg)

<div class="thm">
<div class="thm-head">보조정리 1<span class="en">왼쪽 밀어내기의 안전성</span></div>

활성 집합의 왼쪽 경계는 되돌아오지 않는다. 따라서 전체 훑기 동안 삭제 연산은 많아야 $O(n)$번 일어난다.

</div>

<div class="proof">

<span class="proof-lead">증명.</span> `best`(현재 최솟거리의 제곱)는 훑는 동안 **줄어들기만** 한다. 어떤 점의 x좌표 차이 제곱이 이미 `best`를 넘어 활성 집합에서 빠졌다면, 앞으로 만날 점들은 x가 더 오른쪽에 있어 그 차이가 더 벌어질 뿐이다. 한 번 빠진 점은 다시 후보가 되지 않으므로 왼쪽 경계는 오른쪽으로만 전진한다. 각 점은 많아야 한 번 삭제되므로 전체 삭제는 $O(n)$번이다. <span class="qed">∎</span>

</div>

---

## y구간도 상수 개만

x로 활성 구간을 좁혀도, 그 안에 점이 많으면 여전히 곤란하다. 여기서 두 번째 제약이 들어온다. $P$와 거리 $D$ 미만이려면 **y좌표 차이도 $D$ 미만**이어야 한다. 즉 후보는 y가 $[\,y_P - D,\ y_P + D\,]$인 점들뿐이다.

<div class="thm">
<div class="thm-head">보조정리 2<span class="en">후보 수의 상한</span></div>

새 점 $P$가 비교해야 할 후보(활성 집합 중 y가 $[y_P - D,\ y_P + D]$인 점)는 $n$과 무관하게 **상수 개**다.

</div>

<div class="proof">

<span class="proof-lead">증명.</span> $D$는 $P$를 조회하기 **직전의** `best`에서 얻은 값이고, 그 시점의 `best`는 이미 처리한 점들 사이의 최솟거리다. 따라서 활성 집합 안의 두 점은 서로 거리 $D$ 이상이다(더 가까웠다면 `best`가 벌써 그만큼 작았을 것이다). 후보는 x로 폭 $D$, y로 폭 $2D$인 $D \times 2D$ 직사각형 안에 있고, 그 안의 점들은 서로 $D$ 이상 떨어져 있다. 직사각형을 한 변 $D/2$인 칸으로 쪼개면 칸당 최대 1점이므로, 직사각형에 들어갈 수 있는 점은 상수 개다. <span class="qed">∎</span>

</div>

이는 1편에서 밴드를 셀 때 쓴 것과 **같은 칸 세기** 방식을, 이번엔 분할선 밴드가 아니라 sweep line 뒤의 직사각형에 적용한 것이다. "다음 7개" 보조정리와 문자 그대로 같지는 않지만, 후보 수를 상수로 묶는 같은 종류의 packing 논거다.

<div class="callout callout-simple">
<div class="callout-title">같은 논거, 다른 무대</div>

분할 정복에서는 밴드를 y정렬한 배열 위에서 "다음 7개"로 잘랐다. Plane Sweeping에서는 활성 집합을 y로 정렬해 두고 "$[y_P-D,\ y_P+D]$ 구간"으로 자른다. 자르는 도구(배열 vs 트리)만 다를 뿐, **"$D$ 이상 떨어진 점은 좁은 직사각형에 상수 개뿐"** 이라는 기하 사실은 그대로다. 자세한 칸 세기는 [별도 글](/blog/closest-pair-five-points)에서 다룬다.

</div>

정리하면 새 점 $P$마다 필요한 연산은 세 가지다.

1. 활성 구간의 왼쪽 밀어내기 — x가 멀어진 점들을 활성 집합에서 **삭제**
2. y가 $[y_P - D,\ y_P + D]$인 점들을 **조회**해 $P$와 거리 비교, `best` 갱신
3. $P$를 활성 집합에 **삽입**

이 삽입·삭제·구간 조회를 빠르게 해 주는 자료구조가 **균형 이진 탐색 트리**다.

---

## 균형 이진 탐색 트리로

활성 집합에 필요한 것은 (ㄱ) 점의 삽입, (ㄴ) 점의 삭제, (ㄷ) "y좌표가 어떤 구간에 든 점만 훑기"다. 이 셋을 모두 $O(\log n)$(구간 조회는 $O(\log n +$ 조회 개수$)$)에 해내는 것이 **y좌표로 정렬 상태를 유지하는 균형 이진 탐색 트리**다. C++에서는 레드-블랙 트리로 구현된 `std::set`이 그대로 이 역할을 한다.

키는 `(y, x)` 쌍으로 둔다. y를 1순위로 정렬하므로 y 구간 조회가 자연스럽고, y가 같은 점들도 x로 구분돼 안전하게 공존한다.

- **구간의 시작**은 `lower_bound({y_P - D, -∞})` — y가 $y_P - D$ 이상인 첫 원소
- **구간의 끝**은 `upper_bound({y_P + D, +∞})` — y가 $y_P + D$ 이하인 마지막 원소의 다음

두 반복자 사이를 훑으면 y구간 안의 점만, 그것도 상수 개만 나온다. 트리가 어떻게 y정렬을 저절로 유지하고 이 구간을 어떻게 찾아 내려가는지는 [별도 글](/blog/closest-pair-bst)에서 자세히 다룬다.

<div class="callout callout-simple">
<div class="callout-title">y구간 폭 D는 정수로, 거리 비교는 제곱으로</div>

트리는 y좌표라는 **1차원 값**으로 정렬돼 있으므로, 구간 경계로는 제곱이 아닌 실제 길이 $D$가 필요하다. `best`(거리 제곱)에서 $D = \lceil\sqrt{\texttt{best}}\rceil$로 올림해 쓴다. 올림 덕분에 y구간은 참값보다 **약간 넓을 뿐 좁지 않아** 후보를 놓치지 않는다(넓어져 봐야 상수 개 몇이 더 들어올 뿐이다). 실제 거리 판정은 여전히 [정수 제곱거리](/blog/closest-pair-1) `dist2`로 하므로 부동소수점 오차가 정답에 끼어들지 않는다.

</div>

---

## 코드

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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<P> pts(n);
    for (auto& p : pts) cin >> p.x >> p.y;

    // ── 훑기 순서: x좌표 오름차순 정렬 (딱 한 번) ─────────────
    sort(pts.begin(), pts.end(),
         [](const P& a, const P& b) { return a.x < b.x; });

    // ── 활성 집합: y좌표로 정렬된 균형 BST. 키는 {y, x} ──────
    set<pair<ll, ll>> active;
    ll best = LLONG_MAX;   // 현재까지 최솟거리의 제곱
    int left = 0;          // 활성 구간의 왼쪽 경계 인덱스

    active.insert({pts[0].y, pts[0].x});

    for (int i = 1; i < n; i++) {
        // ── ① 활성 구간의 왼쪽 밀어내기 ─────────────────────
        // x차이 제곱이 best를 넘은 점은 다시 후보가 될 수 없음
        while (left < i) {
            ll dx = pts[i].x - pts[left].x;
            if (dx * dx > best) {
                active.erase({pts[left].y, pts[left].x});
                left++;
            } else break;   // pts[left]가 가장 왼쪽 → 나머지는 더 가까움
        }

        // ── ② y구간 [y-D, y+D]만 조회 (D = ⌈√best⌉) ─────────
        ll D = (ll)ceill(sqrtl((long double)best));
        auto lo = active.lower_bound({pts[i].y - D, LLONG_MIN});
        auto hi = active.upper_bound({pts[i].y + D, LLONG_MAX});
        for (auto it = lo; it != hi; ++it) {
            P q{ it->second, it->first };   // 키는 {y, x} 순
            best = min(best, dist2(pts[i], q));
        }

        // ── ③ 현재 점을 활성 집합에 삽입 ────────────────────
        active.insert({pts[i].y, pts[i].x});
    }

    // best 는 최솟거리의 제곱. 실제 거리가 필요하면 sqrt(best).
    cout << best << "\n";

    return 0;
}
```

**분할 정복 풀이(②)와의 대응:**

| 구분 | 분할 정복 ② | Plane Sweeping ③ |
|:---|:---|:---|
| 뼈대 | 재귀로 나누고 합침 | 왼쪽→오른쪽 한 번 훑기 |
| 후보 x 제약 | 분할선 좌우 폭 $D$ 밴드 | sweep line 왼쪽 폭 $D$ 활성 구간 |
| 후보 y 제약 | y정렬 후 다음 7개 | 트리에서 $[y-D,\ y+D]$ 구간 |
| 정렬 유지 | 재귀가 y정렬을 물려줌 | `std::set`이 y정렬을 유지 |
| 핵심 자료구조 | 배열 + merge | 균형 이진 탐색 트리 |

<div class="callout callout-simple">
<div class="callout-title">`long long`이 안전한 범위</div>

`dist2`의 `dx * dx + dy * dy`가 `long long`에 담기려면 좌표 범위가 정해져 있어야 한다. 예를 들어 좌표가 $[-10^4,\ 10^4]$이면 제곱거리는 최대 $2 \times (2\cdot10^4)^2 = 8 \times 10^8$로 넉넉하다. 좌표가 $[0,\ 10^9)$처럼 크면 제곱거리가 최대 $2 \times 10^{18}$로 `long long` 상한($\approx 9.2 \times 10^{18}$)에 아직 들어간다. 이보다 크면 곱셈에서 넘칠 수 있으니 `__int128`로 올리거나 좌표를 평행이동한다. `D = ⌈√best⌉`의 `best` 초깃값 `LLONG_MAX`에 대한 $\sqrt{\cdot}\approx 3\times10^9$도 `long long` 안이다.

</div>

---

## 복잡도 — O(n log n)

<div class="thm">
<div class="thm-head">정리 1<span class="en">전체 복잡도</span></div>

이 알고리즘은 $n$개의 점에 대해 $O(n \log n)$ 시간에 가장 가까운 점 쌍을 찾는다.

</div>

<div class="proof">

<span class="proof-lead">증명.</span> 비용을 항목별로 더한다. **초기 x정렬**은 $O(n \log n)$(딱 한 번). **삽입**은 점마다 한 번, 각 $O(\log n)$이므로 전체 $O(n \log n)$. **삭제**는 보조정리 1에 의해 전체 $O(n)$번, 각 $O(\log n)$이므로 $O(n \log n)$. **구간 조회**는 점마다 `lower_bound`·`upper_bound`가 $O(\log n)$이고, 조회되는 후보는 보조정리 2에 의해 상수 개라 비교는 $O(1)$이므로 전체 $O(n \log n)$. 모든 항이 $O(n \log n)$이므로 전체도 $O(n \log n)$이다. <span class="qed">∎</span>

</div>

![복잡도 O(n log n) — n개 점을 훑으며 점마다 삽입·삭제·구간 조회를 균형 BST에서 각 O(log n)에. 조회 후보는 상수 개. 전체 n × O(log n) = O(n log n).](/images/closest-pair-3/complexity.svg)

이는 2편의 분할 정복과 **같은 차수**, 즉 정렬의 하한 $\Omega(n \log n)$에 닿는 최적이다. 분할 정복과 Plane Sweeping이 서로 다른 방식으로 같은 최적 차수에 도달한 것이다.

<div class="callout callout-simple">
<div class="callout-title">그럼 어느 쪽을 쓰나</div>

점근 복잡도는 같지만, Plane Sweeping은 재귀도 임시 버퍼도 없이 `std::set` 하나로 끝나 **구현이 짧고 실수할 여지가 적다.** 대신 트리 연산의 상수 인자(포인터 추적, 재균형)가 배열 기반 분할 정복보다 무거운 편이라, 극단적으로 빠른 상수가 필요하면 분할 정복이 유리할 수 있다. 대회에서 "가장 가까운 두 점"류 문제에는 이 `std::set` 풀이가 가장 자주 쓰인다.

</div>

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- **Plane Sweeping**은 점을 x순으로 한 번 훑으며, 현재 점과 가까울 수 있는 이웃만 그때그때 확인한다.
- **활성 집합**은 sweep line 왼쪽 폭 $D$ 활성 구간 안의 점 모음이다(**슬라이딩 윈도우**). `best`가 줄기만 하므로 활성 구간의 왼쪽 경계는 되돌아오지 않고, 삭제는 전체 $O(n)$번.
- 후보의 y도 $[y-D,\ y+D]$로 제한되어, 후보는 $D\times 2D$ 직사각형 안 **상수 개**뿐이다(1편의 칸 세기와 동일 논거).
- 삽입·삭제·구간 조회를 각 $O(\log n)$에 해 주는 **균형 이진 탐색 트리**(`std::set`, 키 `(y, x)`)가 활성 집합을 구현한다.
- 거리 판정은 정수 제곱거리로, y구간 폭만 $D=\lceil\sqrt{\texttt{best}}\rceil$로 올려 쓴다(넓되 좁지 않게).
- 전체 $O(n \log n)$ — 분할 정복과 같은, 이론적 하한에 닿는 차수다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

이로써 가장 가까운 점 쌍을 세 갈래로 훑었다. 브루트포스 $O(n^2)$([①](/blog/closest-pair-1)) → 분할 정복 $O(n\log^2 n)$([①](/blog/closest-pair-1)) → 정렬 재활용으로 $O(n\log n)$([②](/blog/closest-pair-2)) → 그리고 전혀 다른 시선인 Plane Sweeping으로 다시 $O(n\log n)$(이 글). "왜 다음 7개(=상수 개)면 충분한가"의 기하 논거는 [별도 글](/blog/closest-pair-five-points)에서, 활성 집합을 떠받친 **균형 이진 탐색 트리가 y정렬을 유지하고 구간을 찾는 원리**는 [별도 글](/blog/closest-pair-bst)에서, 분할 정복의 뼈대와 점화식 분석은 [분할 정복](/blog/divide-and-conquer) 포스트에서 다룬다.

</div>
