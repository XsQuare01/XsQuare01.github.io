# 모든 쌍 최단 거리 (2편) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 모든 노드 쌍의 최단 거리를 다루는 포스트 2편(`all-pairs-shortest-path`, `floyd-warshall-memory`)과 SVG 6장을 만든다.

**Architecture:** Astro 정적 블로그. 포스트는 `src/content/posts/<slug>.md`(마크다운 + raw HTML 콜아웃/정리/증명), 이미지는 `public/images/<slug>/*.svg`. dijkstra-1·2, dp-1·2·3과 같은 조판·팔레트·목소리를 따른다.

**Tech Stack:** Astro, 마크다운 + KaTeX 수식, raw HTML `div.callout` / `div.thm` / `div.proof`, 손으로 쓴 SVG.

## Global Constraints

- **설계 근거:** `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md`. 권한 순서는 AGENTS > 정본(`docs/writing-rules.md` 6단계) > 스펙 > 이 계획.
- **원문 보존:** 줄기(문제 정의 → 다익스트라 $N$번 → 범위 논증 → $\{1..k\}$ 전략 → 시뮬레이션 → 점화식 유도 → 의사코드 → 메모리 축소)를 지킨다. 스펙 §4의 A~G만 손댄다.
- **원문 언급 금지:** 본문에 "원문 노트", "강의 노트" 등 비공개 원천을 가리키는 서술을 넣지 않는다. 검출: `grep -nE '(원문|원본|강의) ?노트|원문에서는|노트 밖' <파일>`
- **표기 규약:** $N$ 노드 수, $M$ 간선 수. $D^k[i][j]$는 $i \to j$ 중 **중간 노드**가 모두 $\{1,\dots,k\}$에 있는 길 중 최단 거리. 기저 $D^0$은 간선 가중치(없으면 $\infty$, 대각 $0$). 점화식 $D^k[i][j] = \min(D^{k-1}[i][j],\ D^{k-1}[i][k] + D^{k-1}[k][j])$. 로그 밑은 $\log N$으로 통일(스펙 §4 C).
- **전제:** 무방향, **가중치 비음수**(스펙 §4 A). 이 글은 거리만 다루고 경로 복원은 다루지 않는다.
- **검증 예시(스펙 §5):** 간선 `1—2:1, 1—3:5, 1—4:7, 2—4:1, 3—4:10`. $k=1$에서 $(2,3)$이 $\infty \to 6$. $k=2$에서 $(1,4)$가 $7 \to 2$, $(3,4)$가 $10 \to 7$. $k=3,4$ 변화 없음. 최종 행렬은 Task 1 §5 표 그대로.
- **문장:** 초안 후 `docs/writing-rules.md` 5단계로 훑는다(문두 접속어 최소화 최우선). 문장 내부 줄표(—)는 임계치를 넘기지 말 것(리뷰 결정적 검사 대상) — "즉/곧/마침표"로 완화.
- **코드:** C++ 의사코드, 컴파일 검증 불필요.
- **커밋:** **Co-Authored-By 트레일러 넣지 않음.** 콘텐츠 편집 중 `.astro` 캐시 삭제 금지.
- **SVG 팔레트(다크 고정):** 배경 `#0f1117`(rx 10), 제목 `#e2e8f0`, 부제 `#64748b`, 각주 `#94a3b8`, 구분선 `#1e293b`/`#334155`, 중립 박스 `#1e293b`/`#475569`, 파랑 `#1e3a5f`/`#3b82f6`/글자 `#dbeafe`, 초록 `#14352b`/`#34d399`/글자 `#d1fae5`, 빨강 `#2a1414`/`#ef4444`/글자 `#fca5a5`, 앰버 `#3a2c0f`/`#f59e0b`/강조 `#fbbf24`. viewBox 약 680×420, width/height는 viewBox의 1.5배.
- **그래프 노드 좌표(4장 공유, 장면 연속성):** `1`(190,140) `2`(450,110) `3`(170,320) `4`(440,300). 노드는 r=22 원, 채움 `#1e293b`, 테두리 `#475569`, 번호 `#e2e8f0` 15px 중앙. 간선은 stroke `#475569` 2px, 가중치 라벨은 중점에서 살짝 띄워 `#94a3b8` 13px.

---

### Task 1: 본편 포스트 마크다운

**Files:**
- Create: `src/content/posts/all-pairs-shortest-path.md`
- Reference(Task 2에서 생성): `/images/all-pairs-shortest-path/{problem,k-meaning,simulation,recurrence}.svg`

**Interfaces:**
- Produces: slug `all-pairs-shortest-path`. 본문에서 `/blog/dijkstra-1`, `/blog/dijkstra-2`, `/blog/dp-1`로 역링크.
- `floyd-warshall-memory`는 **하드 링크 금지**(Task 3에서 생성 전까지 미발행 — 링크 검사 보호). 텍스트로만 예고.

**Frontmatter(정확히):**

```yaml
---
title: "모든 쌍 최단 거리 — 다익스트라 N번과 플로이드·워셜"
date: 2026-08-11T09:00:00
description: "한 시작점이 아니라 모든 노드 쌍의 최단 거리를 구한다. 다익스트라를 N번 돌리는 기준선을 세우고, 경유할 수 있는 노드를 {1..k}로 제한해 k를 늘려 가는 플로이드·워셜을 유도한다. 점화식 D^k[i][j]=min(D^{k-1}[i][j], D^{k-1}[i][k]+D^{k-1}[k][j])가 왜 성립하는지 양방향으로 증명한다."
tags: ["Algorithm", "Graph", "Shortest Path", "Floyd-Warshall", "Dynamic Programming", "All-Pairs"]
category: algorithm
difficulty: 중급
numbered: true
---
```

**본문 구성(내용·수치·수식·alt를 아래대로 고정, 문장은 시리즈 목소리로 작성):**

- [ ] **Step 1: 오프닝 + 목차 콜아웃**

오프닝 blockquote — [다익스트라 1](/blog/dijkstra-1)은 시작점 하나를 정하고 거기서 모든 노드까지의 거리를 구했다. 이번엔 시작점을 고르지 않는다. 모든 쌍이다. 답이 하나가 아니라 $N^2$개다.

목차 콜아웃(`<div class="callout">` + `<div class="callout-title">이 포스트에서 다루는 내용</div>`) 불릿 4개:
- 다익스트라를 $N$번 돌리는 기준선과 그 복잡도
- 경유할 수 있는 노드를 $\{1,\dots,k\}$로 제한하는 전략
- 점화식 $D^k[i][j] = \min(D^{k-1}[i][j],\ D^{k-1}[i][k]+D^{k-1}[k][j])$의 양방향 증명
- 3차원 배열 의사코드

- [ ] **Step 2: `## 무엇을 구하는가`**

무방향 가중 그래프, 가중치 비음수. 답은 $i,j$ 쌍마다 하나이므로 $N^2$개. 이 글은 최단 **거리**만 다루고 경로 자체는 다루지 않는다(한 줄). 방향 그래프에서도 아이디어는 같다(한 줄, 더 파지 않음).

이미지: `![노드 4개짜리 무방향 가중 그래프와, 채워야 할 4×4 거리 행렬.](/images/all-pairs-shortest-path/problem.svg)`

- [ ] **Step 3: `## 다익스트라를 N번 돌리면`**

다익스트라는 시작점 하나에서 모든 노드까지를 준다. 모든 시작점에 대해 돌리면 답이 나온다. 이진 힙 기준 1회 $O((M+N)\log N)$, $N$번이면 $O(N(M+N)\log N)$. 연결 그래프에서 $M \ge N-1$이므로 $M+N = O(M)$, 즉 $O(NM\log N)$.

밀집·희소 대비: $M \simeq N^2$이면 $O(N^3\log N)$, $M \simeq N$이면 $O(N^2\log N)$. 데이터 크기에 따라 달라진다.

- [ ] **Step 4: `## 새 알고리즘이 놓일 자리`**

원문 논증 그대로(스펙 §4 D — 보강하지 않음). 새 알고리즘이 다익스트라 한 번보다 빠르면 한 쌍만 필요한 상황에서도 그걸 쓰면 되니 다익스트라가 설 자리를 잃는다. 다익스트라를 $N$번 돌리는 것보다 느리면 굳이 배울 이유가 없다. 쓸모 있으려면 $O(M\log N)$과 $O(NM\log N)$ 사이 어딘가에 있으리라 **생각해 볼 수 있다**(단정하지 말 것).

- [ ] **Step 5: `## 지나갈 수 있는 노드를 제한한다`**

노드에 $1 \sim N$ 번호를 붙인다. $D^k[i][j]$를 "$i \to j$로 가되 **중간에 거치는 노드**가 모두 $\{1,\dots,k\}$ 안에 있는 길 중 최단 거리"로 정의한다. $i$와 $j$ 자신은 이 제한과 무관하다(끝점이므로).

$k$를 $0$부터 $N$까지 늘린다. $k=N$이면 제한이 사라지므로 답이다.

"쓸 수 있다"이지 "반드시 써야 한다"가 아님을 강조.

이미지: `![k가 0, 1, 2로 커지면서 중간에 지나갈 수 있는 노드 집합이 넓어진다.](/images/all-pairs-shortest-path/k-meaning.svg)`

- [ ] **Step 6: `## 손으로 따라가기`**

스펙 §5 그래프로 $k=0,1,2$를 따라간다. 간선: `1—2:1, 1—3:5, 1—4:7, 2—4:1, 3—4:10`(2—3 없음).

$k=0$: 중간 노드를 못 쓴다. 직행 간선이거나 $\infty$.

$k=1$: $\{1\}$을 쓸 수 있다. $(2,3)$이 $\infty \to 6$($2\to1\to3 = 1+5$). $(3,4)$는 $3\to1\to4 = 5+7 = 12 > 10$이라 **1번을 쓰지 않는다**.

$k=2$: $\{1,2\}$. 경우의 수가 늘어난다 — $i\to j$, $i\to1\to j$, $i\to2\to j$, $i\to1\to2\to j$, $i\to2\to1\to j$. $(1,4)$가 $7\to2$, $(3,4)$가 $10\to7$.

**핵심 관찰**(`<div class="callout callout-key">`): $k=1$에서 쓰지 않은 노드가 $k=2$에서 쓰일 수 있다. $3\to4$는 $k=1$에서 1번을 버렸지만 $k=2$에서 $3\to1\to2\to4 = 5+1+1 = 7$로 1번이 되살아난다. 각 단계는 "그 노드를 쓸지"가 아니라 "그 집합까지 허용했을 때의 최선"을 기록한다.

$k=3,4$에서는 변화가 없다. 최종 행렬:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | 1 | 5 | 2 |
| **2** | 1 | 0 | 6 | 1 |
| **3** | 5 | 6 | 0 | 7 |
| **4** | 2 | 1 | 7 | 0 |

이미지: `![k=0, 1, 2로 진행하며 갱신되는 거리 행렬. 바뀐 칸을 강조했다.](/images/all-pairs-shortest-path/simulation.svg)`

- [ ] **Step 7: `## 점화식 세우기` — 사이클 제거 먼저**

$D^0[i][j]$가 기저다(간선 가중치, 없으면 $\infty$, 대각 $0$). 채워야 할 칸은 $O(N^3)$개.

**정리 1**(`<div class="thm">` + `<div class="thm-head">정리 1<span class="en">최단 경로에 같은 노드는 두 번 나오지 않는다</span></div>`): 가중치가 비음수이면, 최단 거리를 내는 길 중에는 같은 노드를 두 번 지나지 않는 것이 있다.

**증명**(`<div class="proof">` + `<span class="proof-lead">증명.</span>` … `<span class="qed">∎</span>`): 어떤 노드 $a$가 두 번 나오면 그 사이 구간은 $a$에서 출발해 $a$로 돌아오는 닫힌 구간이다. 이 구간을 잘라내도 양 끝이 $a$로 이어지므로 여전히 $i \to j$ 길이다. 잘라낸 구간의 길이는 비음수이므로 전체 길이는 늘지 않는다. 같은 노드가 남아 있으면 반복한다. 노드 수는 유한하므로 유한 번에 멈춘다. **비음수 전제가 여기서 쓰인다**는 점을 명시.

- [ ] **Step 8: `### 경로 하나를 골라 가른다` — 스펙 §4 B**

최단 경로가 여러 개일 수 있다. "그 최단 경로"라고 지목하는 대신 **아무거나 하나를 골라** $P$라 한다.

$P$는 $k$를 지나거나 지나지 않는다. 둘 중 하나이고 둘 다일 수는 없다.

**$k$를 지나지 않는 경우.** $P$의 중간 노드는 모두 $\{1,\dots,k-1\}$에 있다. $P$는 $D^{k-1}[i][j]$를 겨루는 후보이고 $D^{k-1}[i][j]$는 후보들의 최솟값이므로 $D^{k-1}[i][j] \le |P|$.

**$k$를 지나는 경우.** 정리 1에 의해 $k$는 정확히 한 번 나온다. 그 자리에서 $P$를 $P_1: i \to k$와 $P_2: k \to j$로 자른다. 두 조각의 중간 노드는 $P$의 중간 노드에서 $k$를 뺀 것이므로 모두 $\{1,\dots,k-1\}$ 안에 있다. 각각 $D^{k-1}[i][k]$, $D^{k-1}[k][j]$의 후보이므로 $D^{k-1}[i][k] + D^{k-1}[k][j] \le |P_1| + |P_2| = |P|$.

어느 경우든 두 값 중 하나가 $|P| = D^k[i][j]$ 이하다.

**반대 방향.** $\{1,\dots,k-1\}$만 쓰는 길은 $\{1,\dots,k\}$ 아래에서도 쓸 수 있으므로 $D^k[i][j] \le D^{k-1}[i][j]$. $i \to k$ 최단 거리를 내는 길과 $k \to j$ 최단 거리를 내는 길을 이으면 중간 노드가 $\{1,\dots,k\}$ 안에 있는 $i \to j$ 길이므로 $D^k[i][j] \le D^{k-1}[i][k] + D^{k-1}[k][j]$.

양쪽을 합치면 등호:

$$D^k[i][j] = \min\!\left(D^{k-1}[i][j],\ D^{k-1}[i][k] + D^{k-1}[k][j]\right)$$

**유일성을 쓰지 않았음을 명시.** 여러 개면 아무거나 골랐고, 고른 것이 어느 경우에 들어가든 부등식은 성립했다.

**동점 확인(스펙 §5 변형).** 위 그래프에서 $3-4$가 10 대신 7이었다면 $k=2$에서 $3\to4$ 직행이 7, $3\to1\to2\to4$가 $5+1+1=7$로 최단 경로가 둘이다. 앞을 고르면 첫 경우로 가서 $D^1[3][4] = 7$, 뒤를 고르면 둘째 경우로 가서 $D^1[3][2] + D^1[2][4] = 6+1 = 7$. 어느 쪽이든 7이고 $\min$이 둘 다 덮는다.

이미지: `![k를 지나지 않는 길과 지나는 길. 둘 중 짧은 쪽이 D^k[i][j]다.](/images/all-pairs-shortest-path/recurrence.svg)`

- [ ] **Step 9: `## 의사코드`**

`W[i][j]`는 간선 가중치(없으면 `INF`, 대각 0). 원문 오타 `W[[i][j]`는 고쳐서 쓴다(스펙 §4 E).

```cpp
// D[k][i][j] : i -> j 중 중간 노드가 모두 {1..k} 에 있는 길의 최단 거리
int D[n + 1][n + 1][n + 1];

void floydWarshall(int W[][n + 1], int n) {
    // 기저: 중간 노드를 하나도 못 쓴다
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            D[0][i][j] = W[i][j];

    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                D[k][i][j] = min(D[k - 1][i][j],
                                 D[k - 1][i][k] + D[k - 1][k][j]);
}
```

세 겹 반복이므로 $O(N^3)$. 배열 칸도 $O(N^3)$.

- [ ] **Step 10: 마무리**

`<div class="callout callout-key">` 핵심 정리 — $D^k$의 정의, 점화식, $k=N$이 답.

`<div class="callout">` 이어지는 글 — $N^3$칸을 다 들고 있어야 하는지 묻는 다음 글 예고. **하드 링크 금지**, 텍스트로만.

- [ ] **Step 11: 문장 퇴고 + 원문 언급 검출**

```bash
grep -nE '(원문|원본|강의) ?노트|원문에서는|노트 밖' src/content/posts/all-pairs-shortest-path.md
grep -oE '(^|[.」”"] ?)(하지만|그리고|그런데|따라서|그러나|그래서|그러니|그러면)' src/content/posts/all-pairs-shortest-path.md | wc -l
```

Expected: 첫 명령 출력 없음. 둘째는 후보 수일 뿐이며 문맥으로 판단.

- [ ] **Step 12: 빌드**

Run: `npm run build`
Expected: `N page(s) built`, 에러 없음. 이미지가 아직 없어 404 경고가 날 수 있으나 빌드는 통과해야 한다.

- [ ] **Step 13: 커밋**

```bash
git add src/content/posts/all-pairs-shortest-path.md
git commit -m "feat(algo): 모든 쌍 최단 거리 본편"
```

---

### Task 2: 본편 SVG 4장

**Files:**
- Create: `public/images/all-pairs-shortest-path/problem.svg`
- Create: `public/images/all-pairs-shortest-path/k-meaning.svg`
- Create: `public/images/all-pairs-shortest-path/simulation.svg`
- Create: `public/images/all-pairs-shortest-path/recurrence.svg`

**Interfaces:**
- Consumes: Task 1의 `![alt](/images/...)` 경로와 alt 문구. 그림 내용이 alt와 어긋나면 안 된다.
- 네 장 모두 Global Constraints의 노드 좌표를 공유한다.

- [ ] **Step 1: `problem.svg`**

viewBox `0 0 680 420`. 왼쪽 절반(x 60~500)에 4노드 그래프, 오른쪽(x 520~660)에 빈 $4\times4$ 행렬 격자.

- 제목 `모든 쌍의 최단 거리` 24,32 위치 `#e2e8f0` 17px bold
- 부제 `답은 한 개가 아니라 N² 개다` `#64748b` 13px
- 간선 5개와 가중치 라벨: `1—2: 1`, `1—3: 5`, `1—4: 7`, `2—4: 1`, `3—4: 10`
- 행렬은 4×4 격자(셀 28×28, 선 `#334155`), 행·열 머리 `1 2 3 4` `#64748b` 11px, 셀은 비움
- 행렬 위 캡션 `?` 로 채워야 할 칸임을 표시, 각주 `#94a3b8` 12px

- [ ] **Step 2: `k-meaning.svg`**

viewBox `0 0 680 420`. 같은 그래프를 3열로 축소 배치(각 열 폭 약 200, 노드 좌표를 0.45배 축소 후 열마다 x 오프셋).

- 제목 `중간에 지나갈 수 있는 노드를 제한한다`
- 3열 캡션: `k = 0` / `k = 1` / `k = 2`
- 각 열에서 **경유 허용 노드**를 초록 테두리 `#34d399` + 채움 `#14352b`로, 나머지는 중립색
  - `k=0`: 아무도 초록 아님
  - `k=1`: 노드 1만
  - `k=2`: 노드 1, 2
- 각 열 아래 각주: `직행 간선만` / `1번을 경유할 수 있다` / `1번과 2번을 경유할 수 있다`
- 하단 각주 `#94a3b8` 12px: `쓸 수 있다는 뜻이지 반드시 써야 한다는 뜻이 아니다`

- [ ] **Step 3: `simulation.svg`**

viewBox `0 0 680 420`. 4×4 행렬 3개를 가로로 나열, 사이에 화살표 `→`.

- 제목 `k를 늘리며 행렬을 갱신한다`
- 행렬 1 캡션 `k = 0`, 값:
  ```
  0   1   5   7
  1   0  INF  1
  5  INF  0  10
  7   1  10   0
  ```
- 행렬 2 캡션 `k = 1`, 값은 위와 같되 $(2,3)$과 $(3,2)$가 `6`. 이 두 칸만 초록 채움 `#14352b` 테두리 `#34d399` 글자 `#d1fae5`
- 행렬 3 캡션 `k = 2`, 값:
  ```
  0   1   5   2
  1   0   6   1
  5   6   0   7
  2   1   7   0
  ```
  $(1,4),(4,1),(3,4),(4,3)$ 네 칸을 앰버 채움 `#3a2c0f` 테두리 `#f59e0b` 글자 `#fef3c7`
- 하단 각주: `3→4는 k=1에서 1번을 버렸지만 k=2에서 3→1→2→4 = 7로 되살아난다`

- [ ] **Step 4: `recurrence.svg`**

viewBox `0 0 680 420`. 위아래 두 갈래.

- 제목 `k를 지나는가, 지나지 않는가`
- 위쪽: $i$ ─── $j$ 직선, 위 라벨 `{1..k-1} 만 지나는 길`, 아래 라벨 `D^{k-1}[i][j]` 파랑 `#93c5fd`
- 아래쪽: $i$ ─── $k$ ─── $j$, 두 구간에 각각 `D^{k-1}[i][k]`, `D^{k-1}[k][j]` 앰버 `#fbbf24`. $k$ 노드는 앰버 테두리로 강조
- 가운데에 중괄호나 세로선으로 묶고 `min` 표기, 결과 `D^k[i][j]` 초록 `#34d399`
- 하단 각주: `최단 경로에 같은 노드가 두 번 나오지 않으므로 k는 정확히 한 번 지난다`

- [ ] **Step 5: 구조 검사**

```bash
python -c "import xml.dom.minidom,glob,sys; [xml.dom.minidom.parse(f) for f in glob.glob('public/images/all-pairs-shortest-path/*.svg')]; print('SVG 4장 파싱 OK')"
```

Expected: `SVG 4장 파싱 OK`

- [ ] **Step 6: 빌드 + 커밋**

Run: `npm run build` → 통과 확인.

```bash
git add public/images/all-pairs-shortest-path/
git commit -m "feat(algo): 모든 쌍 최단 거리 본편 도판 4장"
```

---

### Task 3: 후속 포스트 마크다운

**Files:**
- Create: `src/content/posts/floyd-warshall-memory.md`
- Modify: `src/content/posts/all-pairs-shortest-path.md` (마무리 콜아웃의 텍스트 예고를 `/blog/floyd-warshall-memory` 하드 링크로 교체)
- Reference(Task 4에서 생성): `/images/floyd-warshall-memory/{layers,overwrite-safe}.svg`

**Interfaces:**
- Consumes: Task 1이 정한 표기 규약($D^k[i][j]$, 점화식)을 그대로 쓴다.
- Produces: slug `floyd-warshall-memory`. 본편(`/blog/all-pairs-shortest-path`)으로 역링크.

**Frontmatter(정확히):**

```yaml
---
title: "플로이드·워셜의 메모리 줄이기 — 3차원 배열을 1차원으로"
date: 2026-08-11T10:00:00
description: "플로이드·워셜은 D[k][i][j]로 N³칸을 쓴다. k를 계산할 때 k-1층만 참조한다는 점에서 2층으로 줄이고, D^{k-1}[i][k]와 D^k[i][k]가 같다는 것을 보여 1층으로 줄인다. 덮어써도 답이 변하지 않는 이유를 증명한다."
tags: ["Algorithm", "Graph", "Shortest Path", "Floyd-Warshall", "Dynamic Programming"]
category: algorithm
difficulty: 중급
numbered: true
---
```

**본문 구성:**

- [ ] **Step 1: 오프닝 + 목차 콜아웃**

오프닝 blockquote — [모든 쌍 최단 거리](/blog/all-pairs-shortest-path)에서 점화식을 세웠다. 답은 나오지만 $N^3$칸을 들고 있다. $N$이 1000이면 10억 칸이다. 정말 다 필요한가.

목차 콜아웃 불릿 3개:
- $k$층은 $k-1$층만 참조한다 → 2층으로
- 덮어써도 되는 이유 → 1층으로
- 실제로 $O(N^3)$이 $O(N^3\log N)$보다 빠른 이유

- [ ] **Step 2: `## 2층이면 충분하다`**

$D^k$를 계산할 때 참조하는 것은 $D^{k-1}$뿐이다. $D^{k-2}$ 이하는 다시 쓰이지 않는다. 두 층만 두고 $k$의 홀짝으로 번갈아 쓴다.

```cpp
int D[2][n + 1][n + 1];

void floydWarshall(int W[][n + 1], int n) {
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            D[0][i][j] = W[i][j];

    for (int k = 1; k <= n; k++) {
        int prev = (k - 1) % 2, curr = k % 2;
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                D[curr][i][j] = min(D[prev][i][j],
                                    D[prev][i][k] + D[prev][k][j]);
    }
}
```

$O(N^3) \to O(N^2)$.

이미지: `![N³칸을 두 층으로, 다시 한 층으로 줄인다.](/images/floyd-warshall-memory/layers.svg)`

- [ ] **Step 3: `## 한 층으로 줄이면 무엇이 위험한가`**

층 구분을 없앤 코드:

```cpp
int D[n + 1][n + 1];

void floydWarshall(int W[][n + 1], int n) {
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            D[i][j] = W[i][j];

    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                D[i][j] = min(D[i][j], D[i][k] + D[k][j]);
}
```

위험은 분명하다. $D[i][k]$를 읽을 때 그것이 아직 $D^{k-1}[i][k]$인지 이미 $D^k[i][k]$로 덮인 것인지 알 수 없다. 같은 $k$ 반복 안에서 $(i,k)$ 칸이 먼저 갱신될 수 있기 때문이다.

- [ ] **Step 4: `### 덮어써도 값이 같다` — 정리 + 증명**

**정리 1**(`<div class="thm">` + `<div class="thm-head">정리 1<span class="en">k행과 k열은 k단계에서 변하지 않는다</span></div>`): 모든 $i$에 대해 $D^{k-1}[i][k] = D^k[i][k]$이고, 모든 $j$에 대해 $D^{k-1}[k][j] = D^k[k][j]$이다.

**증명** 두 갈래를 모두 싣는다.

*정의로 보는 논증.* 두 값의 차이는 중간에 $k$를 쓸 수 있느냐뿐이다. $i \to k$로 가는 길에서 $k$는 끝점이다. 정리(본편 정리 1)에 의해 같은 노드가 두 번 나오지 않으므로 $k$는 중간 노드로 쓰일 수 없다. 허용 여부가 결과를 바꾸지 못하므로 두 값은 같다.

*점화식에 넣어 보는 확인.* $j = k$를 대입하면

$$D^k[i][k] = \min\!\left(D^{k-1}[i][k],\ D^{k-1}[i][k] + D^{k-1}[k][k]\right)$$

이고 $D^{k-1}[k][k] = 0$이므로 두 인자가 같다. 따라서 $D^k[i][k] = D^{k-1}[i][k]$.

**결론.** 읽는 값이 어느 층이든 같으므로 덮어쓰기는 답을 바꾸지 않는다. 한 층이면 된다.

이미지: `![k단계에서 k행과 k열은 값이 바뀌지 않는다. 그래서 덮어써도 안전하다.](/images/floyd-warshall-memory/overwrite-safe.svg)`

- [ ] **Step 5: `## 그런데 왜 이걸 쓰는가` — 스펙 §4 F**

비교 대상을 명시한다. 밀집 그래프($M \simeq N^2$)에서 다익스트라 $N$번은 $O(N^3\log N)$, 플로이드·워셜은 $O(N^3)$. $\log N$ 하나 차이다.

$N$이 작으면 큰 차이로 보이지 않는다. 그럼에도 쓰는 이유는 표기에 드러나지 않는 상수와 자료구조에 있다. 플로이드·워셜은 우선순위 큐 없이 배열 세 겹 반복만 돌고 메모리 접근이 규칙적이다.

**단정하지 말 것**(스펙 §8): 측정 자료가 없으므로 "실측이 몇 배 빠르다"고 쓰지 않는다. 이유를 밝히는 선에서 멈춘다.

- [ ] **Step 6: 마무리**

`<div class="callout callout-key">` 핵심 정리 — 2층 근거, 1층 근거, $O(N^2)$ 공간.

`<div class="callout">` 이어지는 글 — 최단 **경로** 복원은 별도 주제라는 한 줄. **링크 걸지 않음**(미작성).

- [ ] **Step 7: 본편 링크 연결**

`src/content/posts/all-pairs-shortest-path.md` 마무리 콜아웃의 텍스트 예고를 `[플로이드·워셜의 메모리 줄이기](/blog/floyd-warshall-memory)` 하드 링크로 바꾼다.

- [ ] **Step 8: 문장 퇴고 + 원문 언급 검출**

```bash
grep -nE '(원문|원본|강의) ?노트|원문에서는|노트 밖' src/content/posts/floyd-warshall-memory.md
```

Expected: 출력 없음.

- [ ] **Step 9: 빌드 + 커밋**

Run: `npm run build`
Expected: 통과.

```bash
git add src/content/posts/floyd-warshall-memory.md src/content/posts/all-pairs-shortest-path.md
git commit -m "feat(algo): 플로이드·워셜 메모리 줄이기 후속"
```

---

### Task 4: 후속 SVG 2장

**Files:**
- Create: `public/images/floyd-warshall-memory/layers.svg`
- Create: `public/images/floyd-warshall-memory/overwrite-safe.svg`

**Interfaces:**
- Consumes: Task 3의 alt 문구.

- [ ] **Step 1: `layers.svg`**

viewBox `0 0 680 380`. 좌 → 우 3단계, 사이에 화살표.

- 제목 `층을 줄인다`
- 1단계: 격자 4장을 비스듬히 겹쳐 쌓은 그림, 캡션 `D[k][i][j]`, 각주 `N³ 칸`
- 2단계: 격자 2장, 캡션 `D[k%2][i][j]`, 각주 `2N² 칸`, 두 장에 `prev` / `curr` 라벨
- 3단계: 격자 1장, 캡션 `D[i][j]`, 각주 `N² 칸`, 초록 테두리로 결론 강조
- 하단 각주: `k층은 k-1층만 참조한다`

- [ ] **Step 2: `overwrite-safe.svg`**

viewBox `0 0 680 400`. 가운데에 큰 $N\times N$ 격자 하나(6×6 정도로 그리고 $k$를 4행/4열로 잡음).

- 제목 `k행과 k열은 변하지 않는다`
- $k$행 전체와 $k$열 전체를 앰버 채움 `#3a2c0f` 테두리 `#f59e0b`
- $(k,k)$ 칸에 `0` 표기
- 오른쪽에 수식 박스: `D^k[i][k] = min(D^{k-1}[i][k], D^{k-1}[i][k] + 0)` 파랑 계열
- 하단 각주: `읽는 값이 어느 층이든 같으므로 덮어써도 답이 바뀌지 않는다`

- [ ] **Step 3: 구조 검사**

```bash
python -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in glob.glob('public/images/floyd-warshall-memory/*.svg')]; print('SVG 2장 파싱 OK')"
```

Expected: `SVG 2장 파싱 OK`

- [ ] **Step 4: 빌드 + 커밋**

```bash
npm run build
git add public/images/floyd-warshall-memory/
git commit -m "feat(algo): 메모리 줄이기 도판 2장"
```

---

### Task 5: 리뷰

**Files:**
- Create: `docs/reviews/2026-08-11-all-pairs-shortest-path.md`
- Create: `docs/reviews/2026-08-11-floyd-warshall-memory.md`

- [ ] **Step 1: 결정적 검사**

```bash
python .claude/review_post.py src/content/posts/all-pairs-shortest-path.md
python .claude/review_post.py src/content/posts/floyd-warshall-memory.md
```

문장 내부 줄표(—) 임계치 초과가 잡히면 "즉/곧/마침표"로 완화한다. 섹션 제목과 이미지 alt의 구조적 줄표는 유지 가능.

- [ ] **Step 2: raw 수식 누출 검사**

콜아웃과 thm/proof 내부의 `$수식$`이 렌더되지 않고 raw로 남는 경우가 있다.

```bash
grep -nE '\$[^$]+\$' src/content/posts/all-pairs-shortest-path.md | head -40
```

빌드 산출물에서 확인:

```bash
grep -c '\$' dist/blog/all-pairs-shortest-path/index.html
```

Expected: 본문 영역에 raw `$`가 남지 않아야 한다. 남으면 thm/proof 내부에 빈 줄을 넣어 마크다운 처리를 유도한다.

- [ ] **Step 3: LLM 비평 L1~L7**

`/review-post all-pairs-shortest-path`, `/review-post floyd-warshall-memory`.

L7(논증·복잡도)은 스펙 §5의 층별 표와 대조해 실제로 검증한다. 특히:
- 점화식 양방향 증명의 각 부등식
- 정리 1(사이클 제거)이 비음수 전제를 쓰는 자리
- 후속편 정리 1의 두 갈래 증명
- 복잡도 유도($O(N(M+N)\log N)$, $O(N^3)$)

- [ ] **Step 4: 지적 반영 후 재검사**

```bash
python .claude/review_post.py src/content/posts/all-pairs-shortest-path.md
npm run build
```

Expected: `발견 사항 없음 ✅`, 빌드 통과. 리포트에 「반영 결과」 절 추가.

- [ ] **Step 5: 커밋**

```bash
git add docs/reviews/
git commit -m "docs(reviews): 모든 쌍 최단 거리 2편 리뷰"
```

---

## 자체 검토

**스펙 대응:**

| 스펙 절 | 담당 |
| --- | --- |
| §1 범위(2편, 제외 2편) | Task 1·3, 제외분은 착수하지 않음 |
| §2 provenance | Global Constraints, Task 5 리뷰 인계 |
| §3 예상 독자 | Task 1 Step 1(다익스트라 역링크로 전제 표시) |
| §4 A 비음수 | Task 1 Step 2, Step 7 정리 1 |
| §4 B 유일성 약화 | Task 1 Step 8 전체 |
| §4 C 로그 통일 | Global Constraints, Task 1 Step 3 |
| §4 D 범위 논증 원문 유지 | Task 1 Step 4(단정 금지 명시) |
| §4 E 의사코드 오타 | Task 1 Step 9 |
| §4 F 비교 대상 명시 | Task 3 Step 5 |
| §4 G 방향 그래프 한 줄 | Task 1 Step 2 |
| §5 계산 예시 | Task 1 Step 6, Step 8 동점 |
| §6 구조·frontmatter | Task 1·3 frontmatter 블록 |
| §7 SVG 6장 | Task 2·4 |
| §8 리뷰 인계 | Task 5 |

**표기 일관성:** $D^k[i][j]$ 표기를 Task 1·3에서 동일하게 쓴다. 의사코드는 `D[k][i][j]` → `D[2][...]` → `D[...]` 순으로 층이 줄어드는 것이 본문 서술과 일치한다.

**미해결:** 없음. 제외한 두 편은 스펙 §1에 사유와 함께 기록되어 있으며 이 계획의 범위가 아니다.
