---
title: "Kruskal 알고리즘 — 그리디로 MST를 만든다"
date: 2026-05-26T10:00:00
description: "Kruskal 알고리즘으로 최소 신장 트리(MST)를 구성한다. 가장 작은 엣지부터 그리디하게 고르는 전략이 왜 최적인지 컷 기반 교환 논법으로 증명하고, Union-Find로 사이클 검사를 거의 상수 시간에 처리해 O(m log m)으로 마무리한다."
tags: ["Algorithm", "Graph", "MST", "Greedy"]
category: algorithm
difficulty: 중급
---

> Kruskal은 가장 작은 엣지부터 욕심내어 고른다. 그 욕심이 어떻게 최적해와 만나는지를 보여주는, 단순함 뒤에 정직함이 숨은 알고리즘이다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>최소 신장 트리(MST)의 정의와 그리디 전략</li>
<li>Kruskal 알고리즘의 기본 과정 — 정렬 후 사이클 없는 엣지 추가</li>
<li>Prim 알고리즘과의 차이 — 한 군데에서 자라는가, 여러 군데에서 자라는가</li>
<li>컷(cut) 기반 교환 논법으로 정확성 증명</li>
<li>Union-Find로 사이클 검사 — 전체 시간 복잡도 O(m log m)</li>
</ul>
</div>

## 최소 신장 트리

**신장 트리(Spanning Tree)** 는 무방향 가중 그래프에서 모든 정점을 연결하는 트리 부분 그래프다. 정점이 $n$개라면 신장 트리의 엣지는 정확히 $n - 1$개이고 사이클이 없다.

**최소 신장 트리(Minimum Spanning Tree, MST)** 는 신장 트리 중 엣지 가중치의 합이 가장 작은 것이다.

- 네트워크 케이블을 깔 때 모든 건물을 연결하되 비용을 최소화하는 문제
- 클러스터링에서 가까운 점들끼리 묶어 단일 연결로 만드는 문제
- 미로 생성, 회로 설계, 도로망 계획

이런 문제들이 MST로 모델링된다.

---

## 기본 과정

Kruskal 알고리즘은 다음 세 단계를 반복한다.

| 단계 | 동작 |
|---|---|
| 1 | 아직 처리하지 않은 엣지 중 가장 작은 가중치의 엣지를 선택 |
| 2 | 선택한 엣지가 사이클을 만들지 않으면 추가, 만들면 버림 |
| 3 | 추가된 엣지가 $n - 1$개가 될 때까지 1-2 반복 |

핵심은 **그리디(greedy)** 다. 매 순간 "가장 좋아 보이는 것"을 고른다. 그 욕심이 전역 최적을 가져온다는 점이 이 알고리즘의 비범한 부분이다.

![Kruskal 단계별 진행 — 엣지를 가중치 오름차순으로 보며 사이클을 만들지 않는 것만 추가](/images/kruskal/mst-progress.svg)

### 손으로 따라가기

정점 $\{A, B, C, D, E\}$와 엣지 7개가 있는 그래프(위 다이어그램과 동일)를 가중치 순서로 처리하면:

| 순위 | 엣지 | 가중치 | 결정 | 누적 컴포넌트 |
|---|---|---|---|---|
| 1 | A–B | 1 | + 추가 | $\{A, B\}$ |
| 2 | B–C | 2 | + 추가 | $\{A, B, C\}$ |
| 3 | A–C | 3 | × 사이클 (A, C 이미 같은 컴포넌트) | $\{A, B, C\}$ |
| 4 | C–D | 4 | + 추가 | $\{A, B, C, D\}$ |
| 5 | D–E | 5 | + 추가 ✓ ($|T| = n - 1$) | $\{A, B, C, D, E\}$ |
| 6 | C–E | 6 | (미검사 — 종료됨) | — |
| 7 | B–E | 7 | (미검사 — 종료됨) | — |

총 가중치 $1 + 2 + 4 + 5 = 12$. 알고리즘은 4개 엣지를 추가하고 즉시 종료한다.

---

## Prim과의 차이

MST를 만드는 또 다른 그리디 알고리즘으로 **Prim**이 있다. 둘은 그리디 전략을 공유하지만 자라는 방식이 다르다.

| 측면 | Prim | Kruskal |
|---|---|---|
| 시작점 | 임의의 한 정점 | 엣지 전체 |
| 자라는 방식 | 한 군데에서 트리가 확장 | 여러 군데에서 동시에 자라다 합쳐짐 |
| 그룹 구조 | 트리에 들어간 노드 / 들지 않은 노드 | 여러 부분 트리(forest) |
| 자료구조 | 우선순위 큐 | 정렬 + Union-Find |

Prim은 한 점에서 풍선이 부풀듯 퍼지고, Kruskal은 흩어진 점들이 작은 섬으로 뭉치다 결국 하나의 대륙이 된다.

---

## 정확성 증명

Kruskal이 정말로 MST를 찾는다는 것을 **루프 불변식 + 컷 기반 교환 논법**으로 증명한다.

**불변식:** 알고리즘이 현재까지 추가한 엣지 집합 $T$는 어떤 MST $T_{mst}$의 부분집합이다.

$$T \subseteq T_{mst}$$

매 반복마다 이 불변식이 유지된다는 것만 보이면, 종료 시 $|T| = n - 1$이고 신장 트리의 크기 역시 $n - 1$이므로 $T = T_{mst}$, MST가 완성된다.

### Base case

$|T| = 0$이면 $T = \emptyset$이므로 어떤 $T_{mst}$의 부분집합. 자명.

### Inductive step

$|T| = k$에서 $T \subseteq T_{mst}$가 성립한다고 가정하자. 알고리즘이 다음 엣지 $e = (u, v)$를 추가해 $T' = T \cup \{e\}$가 됐을 때, $T' \subseteq T_{mst}'$ ($T_{mst}'$는 같은 MST이거나 같은 가중치의 다른 MST)이 성립함을 보인다.

$e \in T_{mst}$이면 곧장 $T' \subseteq T_{mst}$, 끝. 이하 $e \notin T_{mst}$ 경우만 본다.

**컷 잡기.** $e$를 추가하는 시점의 forest $T$가 정점 집합 $V$를 여러 컴포넌트로 분할한다. $e$가 사이클 없이 추가됐으므로 $u$와 $v$는 $T$의 서로 다른 컴포넌트에 속한다. $u$가 속한 컴포넌트를 $S$라 하면 $(S, V \setminus S)$는 $u$와 $v$를 가르는 **컷(cut)** 이고, $e$는 이 컷을 가로지른다.

**교환 엣지 선택.** $T_{mst} \cup \{e\}$ 안에 $e$를 포함하는 사이클 $C$가 존재한다. $C$는 $u$와 $v$를 잇는 단순 사이클이므로 컷 $(S, V \setminus S)$를 짝수 번 가로지른다. $e$ 외에 컷을 가로지르는 엣지가 적어도 하나 존재하며, 그중 하나를 $e'$로 선택한다. 이 $e'$는 다음을 만족한다.

- $e' \in T_{mst}$ — 사이클 $C$의 일부이고 $C \subseteq T_{mst} \cup \{e\}$, 그리고 $e' \neq e$
- $e' \notin T$ — $T$는 forest인데 컷을 가로지르는 $T$의 엣지가 있다면 $S$와 $V \setminus S$가 한 컴포넌트가 되어 컴포넌트 정의에 모순

특히 $e'$가 컷을 가로지른다는 사실은 결정적이다. **이 시점의 $T$에서 $e'$의 양 끝점은 서로 다른 컴포넌트**, 즉 $e'$를 추가해도 사이클이 생기지 않는다.

이제 $w(e)$와 $w(e')$를 비교한다.

**Case 1.** $w(e) < w(e')$

$T_{mst}'' = (T_{mst} \setminus \{e'\}) \cup \{e\}$는 여전히 신장 트리이면서 가중치 합이 $T_{mst}$보다 작다. $T_{mst}$가 MST라는 가정에 모순. **발생 불가.**

**Case 2.** $w(e) > w(e')$

Kruskal은 가중치 오름차순으로 엣지를 처리하므로 $e'$를 $e$보다 먼저 봤다. $e'$를 보던 시점의 forest를 $T_{\text{prev}}$라 하면 $T_{\text{prev}} \subseteq T$ (엣지는 추가만 됨). 컴포넌트는 forest가 커질수록 합쳐지므로, $T$에서 $e'$ 양 끝점이 다른 컴포넌트라면 $T_{\text{prev}}$에서도 다른 컴포넌트. 즉 $e'$ 시점에도 사이클이 없었고, 알고리즘은 $e'$를 추가했어야 한다 — 그러면 $e' \in T$이지만, 위에서 $e' \notin T$임을 보였다. **모순, 발생 불가.**

**Case 3.** $w(e) = w(e')$

$T_{mst}'' = (T_{mst} \setminus \{e'\}) \cup \{e\}$도 같은 총 가중치의 또 다른 MST. $T \cup \{e\} \subseteq T_{mst}''$이 성립하므로 불변식은 (다른 MST로 옮겨가서) 유지된다.

세 경우를 모두 다뤘다. 어느 경우든 불변식이 깨지지 않는다. $\square$

이 논증은 **컷 속성(cut property)** 의 표준적 적용이다: *어떤 컷을 가로지르는 가장 가벼운 엣지는 반드시 어떤 MST에 속한다.* Kruskal이 매 반복에서 추가하는 엣지가 그 시점 forest의 컷에 대해 가장 가벼운 후보임이 보장되므로, 그리디 선택이 안전하다.

---

## 구현 — Union-Find

알고리즘의 골격은 단순하다.

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge { int u, v, w; };

// Kruskal MST. (UnionFind는 아래에서 정의)
// 가정:
//   - 정점 번호는 0 이상 n 미만의 정수
//   - edges는 (u, v, w) 형태의 무방향 엣지 목록
//   - 그래프가 연결되어 있다고 가정 (아니면 최소 신장 포레스트가 반환)
// 반환: MST를 구성하는 엣지 목록
vector<Edge> kruskal(int n, vector<Edge> edges) {
    // 가중치 오름차순 (edges를 값으로 받으므로 원본은 보존됨)
    sort(edges.begin(), edges.end(),
         [](const Edge& a, const Edge& b) { return a.w < b.w; });

    UnionFind uf(n);
    vector<Edge> mst;
    for (const Edge& e : edges) {
        if (uf.find(e.u) != uf.find(e.v)) {
            uf.unite(e.u, e.v);
            mst.push_back(e);
            if ((int)mst.size() == n - 1) break;
        }
    }
    return mst;
}
```

몇 가지 주의점.

- **입력 보존.** 위 코드는 `edges`를 값으로 받아 **복사본**을 정렬하므로 호출 측 원본은 그대로다. 큰 그래프에서 복사 비용이 부담이면 `vector<Edge>&`로 참조를 받아 in-place로 정렬한다(대신 원본이 재정렬됨).
- **연결성 가정.** 그래프가 연결되지 않은 경우 종료 시 `mst.size() < n - 1`이고, 반환되는 것은 엄밀히 말해 **최소 신장 포레스트(MSF)** 다. 호출 측에서 크기 검사로 연결성 여부를 판단할 수 있다.
- **정점 인덱싱.** 위 코드는 정점이 $0, 1, \ldots, n-1$로 라벨링됨을 가정한다. 임의 라벨이라면 정점-인덱스 매핑을 먼저 만들어야 한다.

핵심은 **사이클 검사를 얼마나 빠르게 하느냐**다. 매번 그래프 탐색(BFS/DFS)으로 확인하면 한 번에 $O(n)$이 들어 전체가 $O(mn)$. 반면 **Union-Find** 자료구조는 두 정점이 같은 컴포넌트에 속하는지를 거의 상수 시간에 판단한다.

![Union-Find — 각 정점이 자기 자신 root인 상태에서 시작해 union으로 점차 합쳐진다](/images/kruskal/union-find.svg)

Union-Find의 두 연산.

- `find(x)`: $x$가 속한 컴포넌트의 대표 원소(root)를 반환
- `unite(x, y)` (union 연산): $x$와 $y$가 속한 두 컴포넌트를 하나로 합침

**경로 압축(path compression)** 과 **union by rank**를 함께 적용하면 두 연산의 amortized 시간 복잡도가 $O(\alpha(n))$이 된다. 여기서 $\alpha$는 역 Ackermann 함수로, 실용적 범위($n \le 10^{600}$)에서 4 이하의 값. 사실상 상수다.

```cpp
struct UnionFind {
    vector<int> parent, rnk;   // rnk: 트리 높이 상한 (union by rank용)

    UnionFind(int n) : parent(n), rnk(n, 0) {
        iota(parent.begin(), parent.end(), 0);  // 각 원소가 자기 자신을 root로
    }

    int find(int x) {                 // 경로 압축
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    void unite(int x, int y) {        // union by rank (union은 예약어라 unite)
        int rx = find(x), ry = find(y);
        if (rx == ry) return;
        if (rnk[rx] < rnk[ry]) swap(rx, ry);
        parent[ry] = rx;
        if (rnk[rx] == rnk[ry]) rnk[rx]++;
    }
};
```

---

## 시간 복잡도

엣지 수를 $m$, 정점 수를 $n$이라 하자.

| 단계 | 시간 |
|---|---|
| 엣지 정렬 | $O(m \log m)$ |
| Union-Find 연산 $m$회 | $O(m \cdot \alpha(n))$ |
| **합계** | $O(m \log m + m \cdot \alpha(n)) = O(m \log m)$ |

$m \log m$이 지배적이다. 엣지가 이미 가중치 순으로 주어졌거나 정수 가중치를 카운팅 정렬할 수 있는 특수한 경우라면 $O(m \cdot \alpha(n))$ 까지 줄일 수 있지만, 일반적으로는 $O(m \log m)$.

---

## 정리

| 항목 | 값 |
|---|---|
| 분류 | 그리디 |
| 자료구조 | Union-Find (Disjoint Set) |
| 시간 복잡도 | $O(m \log m)$ |
| 보조 공간 | $O(n)$ — Union-Find $O(n)$ + 결과 $O(n)$, 입력 엣지 $O(m)$ 별도 |
| 대표 응용 | 네트워크 설계, 클러스터링, 미로 생성 |

Kruskal은 그리디가 항상 손해 보지 않는다는 것을 보여주는 좋은 예다. "지금 가장 작은 엣지를 고른다"는 단순한 규칙이, 사이클을 만들지만 않는다면 반드시 어떤 MST의 일부가 된다 — 컷 속성이 그 안전성을 보장한다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- **Kruskal**은 가중치 오름차순으로 간선을 검사하며 사이클을 만들지 않는 것만 추가하는 그리디 알고리즘이다.
- 사이클 검사는 **Union-Find**(경로 압축 + union by rank)로 amortized $O(\alpha(n))$ — 사실상 상수.
- 정확성은 **컷 속성(cut property)** 의 표준적 적용으로 증명된다: 현재 forest의 컷을 가르는 가장 가벼운 간선은 반드시 어떤 MST에 속한다.
- 전체 시간 복잡도는 $O(m \log m)$, **정렬이 지배적**이다. Union-Find 연산은 거의 상수.
- 그래프가 연결되지 않으면 출력은 엄밀히 말해 **최소 신장 포레스트(MSF)** — 호출 측에서 `mst.size() == n - 1`로 연결성을 검사할 수 있다.

</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>

**[Prim·Kruskal은 모든 MST를 찾을 수 있는가](/blog/any-mst)** — 같은 그래프에 여러 MST가 존재할 수 있다. 가중치 동률 간선이 있을 때 Prim의 시작점·tie-breaking과 Kruskal의 정렬 순서가 어떻게 다른 답을 만드는지 분석하고, **Stable sort**의 결정성과 한계를 짚는다. 그 다음 알고리즘이 **모든 가능한 MST를 찾을 수 있음**을 교환 논법으로 증명하고, "모든 간선 가중치가 다르면 MST는 유일하다"는 결론까지 정리한다.

</div>
