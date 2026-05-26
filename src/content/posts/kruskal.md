---
title: "Kruskal 알고리즘 — 그리디로 MST를 만든다"
date: 2026-05-26T10:00:00
description: "Kruskal 알고리즘으로 최소 신장 트리(MST)를 구성하는 과정을 따라간다. 가장 작은 엣지부터 그리디하게 선택하는 단순한 전략이 왜 최적해를 보장하는지 컷(cut) 기반 교환 논법으로 증명하고, Union-Find로 사이클 검사를 거의 상수 시간에 처리해 전체 O(m log m)으로 마무리한다."
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

이런 문제들이 모두 MST로 환원된다.

---

## 기본 과정

Kruskal 알고리즘은 다음 세 단계를 반복한다.

| 단계 | 동작 |
|---|---|
| 1 | 모든 엣지 중 가장 작은 가중치의 엣지를 선택 |
| 2 | 선택한 엣지가 사이클을 만들지 않으면 추가, 만들면 버림 |
| 3 | 추가된 엣지가 $n - 1$개가 될 때까지 1-2 반복 |

핵심은 **그리디(greedy)** 다. 매 순간 "가장 좋아 보이는 것"을 고른다. 그 욕심이 전역 최적을 가져온다는 점이 이 알고리즘의 비범한 부분이다.

![Kruskal 단계별 진행 — 엣지를 가중치 오름차순으로 보며 사이클을 만들지 않는 것만 추가](/images/kruskal/mst-progress.svg)

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

```python
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    n: 정점 개수
    edges: (u, v, w) 형태의 엣지 리스트
    반환: MST를 구성하는 엣지 리스트
    """
    edges.sort(key=lambda e: e[2])  # 가중치 오름차순
    uf = UnionFind(n)
    mst = []
    for u, v, w in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, w))
            if len(mst) == n - 1:
                break
    return mst
```

핵심은 **사이클 검사를 얼마나 빠르게 하느냐**다. 매번 그래프 탐색(BFS/DFS)으로 확인하면 한 번에 $O(n)$이 들어 전체가 $O(mn)$. 반면 **Union-Find** 자료구조는 두 정점이 같은 컴포넌트에 속하는지를 거의 상수 시간에 판단한다.

![Union-Find — 각 정점이 자기 자신 root인 상태에서 시작해 union으로 점차 합쳐진다](/images/kruskal/union-find.svg)

Union-Find의 두 연산.

- `find(x)`: $x$가 속한 컴포넌트의 대표 원소(root)를 반환
- `union(x, y)`: $x$와 $y$가 속한 두 컴포넌트를 하나로 합침

**경로 압축(path compression)** 과 **union by rank**를 함께 적용하면 두 연산의 amortized 시간 복잡도가 $O(\alpha(n))$이 된다. 여기서 $\alpha$는 역 Ackermann 함수로, 실용적 범위($n \le 10^{600}$)에서 4 이하의 값. 사실상 상수다.

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        # 경로 압축
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
```

---

## 시간 복잡도

엣지 수를 $m$, 정점 수를 $n$이라 하자.

| 단계 | 시간 |
|---|---|
| 엣지 정렬 | $O(m \log m)$ |
| Union-Find 연산 $m$회 | $O(m \cdot \alpha(m))$ |
| **합계** | $O(m \log m + m \cdot \alpha(m)) = O(m \log m)$ |

정렬이 지배적이다. 엣지가 이미 가중치 순서로 주어졌거나 정수 가중치를 카운팅 정렬할 수 있는 특수한 경우라면 $O(m \cdot \alpha(m))$ 까지 줄일 수 있지만, 일반적으로는 $O(m \log m)$.

---

## 정리

| 항목 | 값 |
|---|---|
| 분류 | 그리디 |
| 자료구조 | Union-Find (Disjoint Set) |
| 시간 복잡도 | $O(m \log m)$ |
| 공간 복잡도 | $O(n + m)$ |
| 대표 응용 | 네트워크 설계, 클러스터링, 미로 생성 |

Kruskal은 그리디가 항상 손해 보지 않는다는 것을 보여주는 좋은 예다. "지금 가장 작은 엣지를 고른다"는 단순한 규칙이, 사이클을 만들지만 않는다면 반드시 어떤 MST의 일부가 된다 — 컷 속성이 그 안전성을 보장한다.

**다음 읽을거리.** Kruskal과 Prim 모두 MST를 찾지만, 같은 가중치를 갖는 엣지가 있을 때는 서로 다른 답을 낼 수 있다. 그런데도 "모든 MST를 다 찾을 수 있는가" — 이 질문은 별도 글에서 다룬다.
