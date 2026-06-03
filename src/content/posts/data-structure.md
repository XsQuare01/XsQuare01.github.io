---
title: "자료구조 — 데이터를 담는 그릇의 설계"
date: 2026-04-06T09:00:00
description: "Array, Stack, Queue, Linked List, BST, AVL Tree, Heap, 2-3 Tree, Graph까지 — 각 자료구조의 구조와 핵심 연산을 시각적으로 정리한다."
tags: ["Data Structure", "Algorithm", "Tree", "Graph"]
category: algorithm
difficulty: 입문
---

> 자료구조는 데이터를 **어떤 형태로 저장하고 접근할 것인가**를 결정하는 설계다. 같은 데이터라도 그릇이 다르면 연산의 효율이 완전히 달라진다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>
<ul>
<li>Array — 연속된 메모리와 직접 접근</li>
<li>Stack과 Queue — 삽입/삭제 순서의 제약</li>
<li>Linked List — 포인터로 연결된 노드 체인</li>
<li>Binary Search Tree — 정렬된 탐색 트리</li>
<li>AVL Tree — 균형을 유지하는 BST</li>
<li>Heap — 우선순위 큐의 기반</li>
<li>2-3 Tree — 다중 키 균형 트리</li>
<li>Graph — 정점과 간선의 일반 구조</li>
</ul>
</div>

## Array

**배열(Array)** 은 연속된 메모리 주소에 동일한 타입의 데이터를 저장하는 가장 기본적인 자료구조다.

![Array 구조](/images/data-structure/array.svg)

| 특성 | 설명 |
|---|---|
| **직접 접근** | 인덱스를 통해 O(1)로 임의의 원소에 접근 가능 |
| **고정 크기** | 배열의 크기는 생성 시 결정되며, 이후 변경 불가 |
| **연속 메모리** | 원소들이 메모리에 연속으로 배치되어 캐시 효율이 높음 |

인덱스를 통한 직접 접근이 가능하기 때문에 정렬된 배열에서는 Binary Search 같은 알고리즘을 적용할 수 있다. 또한 배열은 다른 자료구조(Stack, Queue, Heap 등)의 내부 구현에도 자주 등장한다.

---

## Stack

**스택(Stack)** 은 Last In, First Out(LIFO) 원칙을 따르는 자료구조다. 가장 나중에 삽입된 데이터가 가장 먼저 제거된다.

배열을 이용한 구현의 경우, **스택 포인터(Stack Pointer)** 를 사용한다.

| 연산 | 동작 |
|---|---|
| **Push** | Stack Pointer + 1, 해당 위치에 데이터 삽입 |
| **Pop** | 현재 Stack Pointer 위치의 데이터 제거, Stack Pointer - 1 |

## Queue

**큐(Queue)** 는 First In, First Out(FIFO) 원칙을 따르는 자료구조다. 가장 먼저 삽입된 데이터가 가장 먼저 제거된다.

![Stack과 Queue](/images/data-structure/stack-queue.svg)

배열을 이용한 구현의 경우, **Tail**과 **Head** 두 개의 포인터를 사용한다.

| 포인터 | 역할 |
|---|---|
| **Tail** | 다음에 Pop(Dequeue)해야 하는 위치 |
| **Head** | 다음에 Push(Enqueue)할 위치 |

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
Stack은 접시를 쌓는 것과 같다. 맨 위에 올리고 맨 위에서 꺼낸다. Queue는 줄 서기와 같아서, 먼저 온 사람이 먼저 나간다. 포인터 정의는 구현에 따라 달라질 수 있으며, Circular Queue로 확장할 수도 있다.
</div>

---

## Linked List

**연결 리스트(Linked List)** 는 **노드(Node)** 와 **포인터(Link)** 로 구성된 자료구조다.

![Linked List 구조](/images/data-structure/linked-list.svg)

각 노드는 데이터를 저장하는 영역과 다음 노드의 주소를 저장하는 포인터로 이루어진다. 노드는 메모리에 연속적으로 배치될 필요가 없으며, 포인터로 논리적 순서를 유지한다.

| 특성 | 설명 |
|---|---|
| **Insert / Delete** | 해당 위치의 포인터만 변경하면 되므로 O(1) |
| **탐색** | 순차 접근만 가능하여 O(n) |
| **Binary Search 불가** | 임의 접근이 불가능하므로 이진 탐색을 적용할 수 없음 |

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
배열이 아파트(연속된 호수)라면, 연결 리스트는 보물찾기와 같다. 각 보물 상자에 "다음 상자의 위치"가 적혀 있다. 중간에 상자를 추가하거나 빼기 쉽지만, "5번째 상자"를 바로 찾을 수는 없다.
</div>

---

## Binary Search Tree

**이진 탐색 트리(BST)** 는 각 노드가 키(Key)를 가지며, 왼쪽 서브트리의 모든 키 < 루트 키 < 오른쪽 서브트리의 모든 키라는 성질을 만족하는 트리다.

![Binary Search Tree](/images/data-structure/bst.svg)

정확한 정의는 다음과 같다.

- 각 Node는 Key를 포함한다.
- 비어 있지 않은 BST에는 하나의 Root Node가 존재한다.
- Root Node는 최대 두 개의 Child Node를 가질 수 있다.
- 각 Child는 자신만의 SubTree의 Root이며, 각 SubTree는 그 자체로 BST다.
- Left Subtree의 모든 Key는 Root의 Key보다 작고, Right Subtree의 모든 Key는 Root의 Key보다 크다.
- 이 성질은 모든 서브트리에서 재귀적으로 유지된다.

<div class="callout callout-simple">
<div class="callout-title">쉽게 말하면</div>
BST는 사전과 같다. 찾고 싶은 단어가 현재 페이지보다 앞에 있으면 왼쪽을, 뒤에 있으면 오른쪽을 본다. 매번 절반을 버리니 빠르지만, 사전이 한쪽으로 치우쳐 있으면(편향 트리) 결국 처음부터 끝까지 넘겨야 한다.
</div>

---

## AVL Tree

**AVL Tree**는 BST의 균형을 자동으로 유지하는 트리다. BST가 편향되면 탐색 시간이 O(n)까지 악화되는데, AVL Tree는 이를 방지한다.

![AVL Tree — 불균형에서 균형으로](/images/data-structure/avl-tree.svg)

### 핵심 원리

- 각 노드는 **L**(왼쪽 서브트리 높이)과 **R**(오른쪽 서브트리 높이)의 레이블을 가진다.
- 모든 노드에서 |L - R| ≤ 1 을 유지해야 한다.
- 이 조건이 깨지면 **회전(Rotation)** 을 통해 균형을 복구한다.

### 높이 보장: O(log n)

N개의 노드가 존재할 때, AVL Tree의 높이는 O(log n)이다.

**증명의 핵심**

1. Root에서 가장 가까운 leaf까지의 높이를 $h$라 하면, 높이 $h$까지는 모든 노드가 꽉 차 있다. 따라서 $N \ge 2^h$이고, $h \le \log N$이다.
2. AVL 조건에 의해 가장 먼 leaf까지의 높이는 최대 $2h$다.
   - 어떤 노드의 L이 $k$라면, 왼쪽 자식은 $k-1$을 반드시 가져야 하고, $k-2$는 존재할 수도 있다.
   - "가장 멀리 가려면" 1 차이를 따라가고, "가장 가까이 가려면" 2 차이를 따라가야 한다.
3. $h \le \log N$이므로, $2h \le 2\log N$. 따라서 최대 높이는 O(log n)이다.

---

## Heap

**힙(Heap)** 은 Priority Queue를 구현하는 데 사용되는 완전 이진 트리다. Min Heap에서는 부모가 항상 자식보다 작다.

![Min Heap 구조와 연산](/images/data-structure/heap.svg)

### Insert

1. 트리가 꽉 차도록(완전 이진 트리 유지) 맨 뒤에 삽입한다.
2. 삽입된 노드 $x$를 부모와 비교하여, $x$가 더 작으면 위로 올린다(Bubble Up).
3. 부모가 $x$보다 작을 때까지 반복한다.

이전 과정에서 모든 노드의 위치가 적절하다는 가정 하에, 잘못될 가능성이 있는 것은 $x$와 그 부모의 관계뿐이므로 이 둘만 비교하면 된다.

### Delete (Extract Min)

1. Root(최솟값)를 제거한다.
2. 맨 뒤의 노드 $x$를 root로 이동시킨다.
3. $x$의 두 자식을 비교하여, 더 작은 값을 위로 올린다.
   - $a$와 $b$ 중 $a$가 더 작아서 올라갔다면, $a < b$이므로 위치가 적절하다.
4. $x$보다 작은 자식이 없을 때까지 반복한다(Bubble Down).

---

## 2-3 Tree

**2-3 Tree**는 각 노드가 1개 또는 2개의 키를 가지며, 따라서 2개 또는 3개의 자식을 갖는 균형 트리다.

![2-3 Tree 구조](/images/data-structure/two-three-tree.svg)

| 노드 유형 | Key 수 | Children 수 |
|---|---|---|
| **2-node** | 1 | 2 |
| **3-node** | 2 | 3 |

모든 leaf까지의 거리가 동일하므로, 트리의 높이는 O(log n)이다. Disk 기반의 자료구조(B-Tree 등)에서 이 구조를 확장하여 많이 사용한다.

---

## Graph

**그래프(Graph)** 는 **정점(Vertex)** 의 집합과 **간선(Edge)** 의 집합으로 구성되는 가장 일반적인 자료구조다.

![Graph 구조](/images/data-structure/graph.svg)

### 정의

**Simple Graph** $G = (V, E)$는 다음으로 구성된다.

- $V$: 비어 있지 않은 정점(Vertices)의 집합
- $E$: 간선(Edges)의 집합 (비어 있을 수 있음). 각 간선은 $V$의 원소 2개로 이루어진 **무순서쌍(unordered pair)**

Simple Graph에서 간선은 방향이 없으므로 $\{u, v\} = \{v, u\}$이다.

### 최대 간선 수

$n$개의 정점이 존재할 때, 가능한 간선의 최대 수는 다음과 같다.

$$|E|_{\max} = \binom{n}{2} = \frac{n(n-1)}{2}$$

무순서쌍의 개수이므로, 모든 정점 쌍을 간선으로 연결한 **완전 그래프(Complete Graph)** 가 이 값을 달성한다.

---

## 정리

| 자료구조 | 접근 | 삽입 | 삭제 | 특징 |
|---|---|---|---|---|
| **Array** | O(1) | O(n) | O(n) | 인덱스 직접 접근, 고정 크기 |
| **Stack** | O(n) | O(1) | O(1) | LIFO, SP로 관리 |
| **Queue** | O(n) | O(1) | O(1) | FIFO, Head/Tail로 관리 |
| **Linked List** | O(n) | O(1) | O(1) | 포인터 기반, 가변 크기 |
| **BST** | O(h) | O(h) | O(h) | 정렬 유지, 편향 가능 |
| **AVL Tree** | O(log n) | O(log n) | O(log n) | 균형 BST, 회전 비용 |
| **Heap** | O(1)* | O(log n) | O(log n) | *min/max만 O(1) |
| **2-3 Tree** | O(log n) | O(log n) | O(log n) | 균형 보장, Disk 최적화 |
| **Graph** | — | — | — | 가장 일반적 구조 |

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- **Array**는 연속된 메모리에 인덱스로 직접 접근한다. 읽기는 O(1)이지만 중간 삽입/삭제는 O(n)이다.
- **Stack**(LIFO)과 **Queue**(FIFO)는 삽입·삭제 순서의 제약으로 구분된다. 핵심은 SP 또는 Head/Tail 포인터 관리다.
- **Linked List**는 포인터로 연결된 노드 체인이다. 가변 크기이고 삽입/삭제는 O(1)이지만 임의 접근은 O(n)이다.
- **BST**는 정렬된 탐색 트리, **AVL Tree**는 회전으로 균형을 강제해 모든 연산 O(log n)을 보장한다. **2-3 Tree**는 다중 키 방식으로 같은 효과를 낸다.
- **Heap**은 우선순위 큐의 기반이다. min/max 조회는 O(1), 삽입·삭제는 O(log n)이다.
- **Graph**는 정점과 간선만으로 거의 모든 관계를 표현하는 가장 일반적인 자료구조다.

</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>

**[정렬 알고리즘 — Selection / Merge / Quick](/blog/sort)**. 자료구조 위에서 가장 자주 마주치는 연산이 정렬이다. Selection sort의 $O(n^2)$에서 출발해, 분할 정복으로 만든 Merge sort의 $O(n \log n)$, 그리고 Quick sort의 평균 $O(n \log n)$ / 최악 $O(n^2)$까지 살펴본다. 각 알고리즘이 어떤 자료구조 위에서 어떻게 움직이는지를 구체적으로 본다.

</div>
