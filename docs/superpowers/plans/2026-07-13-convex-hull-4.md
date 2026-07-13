# 볼록 껍질 ④ — 분할 정복과 공통 접선 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 볼록 껍질 시리즈 4편 — 점을 절반으로 갈라 각 껍질을 재귀로 구한 뒤 공통 접선으로 잇는 분할 정복을, SVG 4장과 함께 한 편의 블로그 포스트로 발행한다.

**Architecture:** Astro content collection 포스트 한 편(`src/content/posts/convex-hull-4.md`) + 인라인 SVG 도판 4장(`public/images/convex-hull-4/*.svg`). 선행 3편의 forward reference(4편 예고)를 발행 후 하이퍼링크로 연결한다. "테스트"는 `npm run build`(content 스키마 + KaTeX 파싱) 통과와 `/review-post`다.

**Tech Stack:** Astro, Markdown + KaTeX, 인라인 SVG(viewBox 680×420, 다크 팔레트).

## Global Constraints

- 브랜치: `feat/post-convex-hull-4`에서만 작업. main 직접 커밋 금지.
- frontmatter 스키마: `title`, `date`, `description`, `tags`(배열), `category: algorithm`, `difficulty` 필수.
- date는 실제 작성일 `2026-07-13T09:00:00`.
- 코드는 의사코드 수준 C++, 컴파일 검증 불필요. 시리즈 정의(`struct P`/`ccw()`) 재사용 서술.
- SVG 팔레트: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`, 파랑 `#93c5fd`/`#3b82f6`, 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`. viewBox `0 0 680 420`, width 1020 height 630.
- 커밋 트레일러: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- 문장 내부 줄표(—) 남발 금지(결정적 검사 임계치). 경구식 마무리·과한 대칭 문장 자제.

---

### Task 1: SVG 도판 4장

**Files:**
- Create: `public/images/convex-hull-4/dc-split.svg`
- Create: `public/images/convex-hull-4/dc-tangent.svg`
- Create: `public/images/convex-hull-4/dc-walking.svg`
- Create: `public/images/convex-hull-4/dc-binary-tangent.svg`

**Interfaces:**
- Produces: 본문(Task 2)이 참조하는 이미지 경로 4개. 좌/우 두 껍질의 점 배치를 네 도판이 공유한다(왼쪽 껍질 `100,240 140,160 225,135 290,215 250,315 150,330`, 오른쪽 껍질 `400,215 455,130 560,155 600,255 540,335 430,320`).

- [ ] **Step 1: `dc-split.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">나누기 — 점을 절반으로 갈라 각각의 껍질을 구한다</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">x좌표 중앙을 기준으로 왼쪽 절반과 오른쪽 절반</text>

  <line x1="345" y1="70" x2="345" y2="360" stroke="#475569" stroke-width="1.3" stroke-dasharray="6 5"/>
  <text x="345" y="382" text-anchor="middle" fill="#64748b" font-size="10">x 중앙</text>

  <polygon points="100,240 140,160 225,135 290,215 250,315 150,330" fill="#34d39918" stroke="#34d399" stroke-width="2.5"/>
  <g fill="#0f1117" stroke="#34d399" stroke-width="2">
    <circle cx="100" cy="240" r="5"/><circle cx="140" cy="160" r="5"/><circle cx="225" cy="135" r="5"/>
    <circle cx="290" cy="215" r="5"/><circle cx="250" cy="315" r="5"/><circle cx="150" cy="330" r="5"/>
  </g>
  <text x="190" y="245" text-anchor="middle" fill="#6ee7b7" font-size="13" font-weight="700">왼쪽 껍질</text>

  <polygon points="400,215 455,130 560,155 600,255 540,335 430,320" fill="#3b82f618" stroke="#3b82f6" stroke-width="2.5"/>
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="400" cy="215" r="5"/><circle cx="455" cy="130" r="5"/><circle cx="560" cy="155" r="5"/>
    <circle cx="600" cy="255" r="5"/><circle cx="540" cy="335" r="5"/><circle cx="430" cy="320" r="5"/>
  </g>
  <text x="500" y="250" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">오른쪽 껍질</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">두 껍질은 x좌표로 완전히 분리돼 있다 — 이제 하나로 합친다</text>
</svg>
```

- [ ] **Step 2: `dc-tangent.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">합치기 — 상·하 공통 접선으로 두 껍질을 잇는다</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">접선 바깥 사슬은 살아남고, 사이에서 마주 보는 안쪽 점은 버려진다</text>

  <polygon points="100,240 140,160 225,135 290,215 250,315 150,330" fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>
  <polygon points="400,215 455,130 560,155 600,255 540,335 430,320" fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>

  <line x1="225" y1="135" x2="455" y2="130" stroke="#fbbf24" stroke-width="2.5"/>
  <line x1="250" y1="315" x2="430" y2="320" stroke="#fbbf24" stroke-width="2.5"/>
  <text x="335" y="118" text-anchor="middle" fill="#fbbf24" font-size="12" font-weight="700">상단 공통 접선</text>
  <text x="340" y="348" text-anchor="middle" fill="#fbbf24" font-size="12" font-weight="700">하단 공통 접선</text>

  <g fill="#0f1117" stroke="#64748b" stroke-width="2">
    <circle cx="100" cy="240" r="5"/><circle cx="140" cy="160" r="5"/><circle cx="150" cy="330" r="5"/>
    <circle cx="560" cy="155" r="5"/><circle cx="600" cy="255" r="5"/><circle cx="540" cy="335" r="5"/>
  </g>
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.5">
    <circle cx="225" cy="135" r="6"/><circle cx="455" cy="130" r="6"/>
    <circle cx="250" cy="315" r="6"/><circle cx="430" cy="320" r="6"/>
  </g>

  <g stroke="#ef4444" stroke-width="2">
    <circle cx="290" cy="215" r="7" fill="#1f2937"/>
    <line x1="284" y1="209" x2="296" y2="221"/><line x1="296" y1="209" x2="284" y2="221"/>
    <circle cx="400" cy="215" r="7" fill="#1f2937"/>
    <line x1="394" y1="209" x2="406" y2="221"/><line x1="406" y1="209" x2="394" y2="221"/>
  </g>
  <text x="345" y="197" text-anchor="middle" fill="#f87171" font-size="12" font-weight="600">버려지는 안쪽 점</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">두 접선만 찾으면 합치기가 끝난다 — 합치기의 전부는 공통 접선 찾기다</text>
</svg>
```

- [ ] **Step 3: `dc-walking.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="dw-a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#fbbf24"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">선형 워킹 — 포인터를 전진시켜 하단 공통 접선을 좁힌다</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">왼쪽 최우점·오른쪽 최좌점에서 시작해 더 내려갈 수 없을 때까지 전진</text>

  <polygon points="100,240 140,160 225,135 290,215 250,315 150,330" fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>
  <polygon points="400,215 455,130 560,155 600,255 540,335 430,320" fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>

  <line x1="290" y1="215" x2="400" y2="215" stroke="#64748b" stroke-width="1.6" stroke-dasharray="5 4"/>
  <text x="345" y="207" text-anchor="middle" fill="#64748b" font-size="10">시작 직선</text>

  <line x1="250" y1="315" x2="430" y2="320" stroke="#fbbf24" stroke-width="2.5"/>
  <text x="340" y="348" text-anchor="middle" fill="#fbbf24" font-size="12" font-weight="700">하단 공통 접선</text>

  <path d="M290,215 Q262,270 251,309" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#dw-a)" stroke-dasharray="4 3"/>
  <path d="M400,215 Q413,272 429,314" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#dw-a)" stroke-dasharray="4 3"/>

  <g fill="#0f1117" stroke="#93c5fd" stroke-width="2.5">
    <circle cx="290" cy="215" r="6"/><circle cx="400" cy="215" r="6"/>
  </g>
  <text x="278" y="205" text-anchor="end" fill="#93c5fd" font-size="11" font-weight="600">최우점</text>
  <text x="412" y="205" text-anchor="start" fill="#93c5fd" font-size="11" font-weight="600">최좌점</text>

  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.5">
    <circle cx="250" cy="315" r="6"/><circle cx="430" cy="320" r="6"/>
  </g>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">각 포인터는 한 방향으로만 돌아 전진 총횟수가 선형 — 접선 하나가 O(N)</text>
</svg>
```

- [ ] **Step 4: `dc-binary-tangent.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="db-a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#93c5fd"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">이진 탐색 접선 — 고정점에서 접점을 O(log N)에 찾는다</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">단조 사슬이라 후보의 양옆 변 방향(CCW)으로 한쪽을 버리며 내려간다</text>

  <polygon points="400,215 455,130 560,155 600,255 540,335 430,320" fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="400" cy="215" r="5"/><circle cx="455" cy="130" r="5"/><circle cx="560" cy="155" r="5"/>
    <circle cx="600" cy="255" r="5"/><circle cx="540" cy="335" r="5"/><circle cx="430" cy="320" r="5"/>
  </g>

  <line x1="150" y1="240" x2="560" y2="155" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5 4"/>
  <text x="572" y="150" fill="#64748b" font-size="10" font-weight="600">mid — 더 위로</text>

  <line x1="150" y1="240" x2="455" y2="130" stroke="#93c5fd" stroke-width="2.6" marker-end="url(#db-a)"/>

  <circle cx="150" cy="240" r="8" fill="#34d399"/>
  <text x="150" y="223" text-anchor="middle" fill="#6ee7b7" font-size="13" font-weight="700">고정점 a</text>

  <circle cx="455" cy="130" r="7" fill="#0f1117" stroke="#93c5fd" stroke-width="2.6"/>
  <text x="455" y="115" text-anchor="middle" fill="#93c5fd" font-size="12" font-weight="700">접점</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">고정점을 O(log N)번 옮기면 공통 접선이 O(log²N) — 총복잡도는 merge O(N)에 묶여 그대로</text>
</svg>
```

- [ ] **Step 5: 커밋**

```bash
git add public/images/convex-hull-4/
git commit -m "feat(convex-hull): 4편 SVG 도판 4장"
```

---

### Task 2: 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-4.md`

**Interfaces:**
- Consumes: Task 1의 SVG 경로 4개.
- Produces: 라우트 `/blog/convex-hull-4`. Task 3이 3편에서 이 라우트로 링크한다.

- [ ] **Step 1: 본문 파일 작성 (전체 인라인)**

````markdown
---
title: "볼록 껍질 ④ — 분할 정복과 공통 접선"
date: 2026-07-13T09:00:00
description: "점들을 절반으로 갈라 각각의 껍질을 재귀로 구한 뒤 공통 접선(common tangent)으로 잇는 분할 정복을 다룬다. 접선을 O(N) 선형 워킹으로, 나아가 O(log²N) 이진 탐색으로 찾는 두 방법과 그 복잡도의 진실을 살펴본다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Divide and Conquer"]
category: algorithm
difficulty: 심화
---

> [1편](/blog/convex-hull-1)과 [2편](/blog/convex-hull-2)은 점을 전부 늘어놓고 한 번에 훑었고, [3편](/blog/convex-hull-3)은 점을 왼쪽부터 하나씩 더하며 껍질을 키웠다. 이번 편은 또 다른 길이다. 점들을 **절반으로 갈라** 각각의 껍질을 따로 구한 뒤, 두 껍질을 **공통 접선(common tangent)** 하나로 잇는다. 정렬에서 봤던 merge sort의 재귀 구조가 기하에서 어떻게 다시 나타나는지, 그리고 두 껍질을 잇는 접선을 얼마나 빨리 찾을 수 있는지 살펴본다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 점을 절반으로 갈라 재귀로 푸는 **분할 정복**의 뼈대
- 두 껍질을 잇는 **상·하 공통 접선**
- 접선을 $O(N)$에 찾는 **선형 워킹**
- 접선을 $O(\log^2 N)$에 찾는 **이진 탐색**과 그 한계

</div>

이번에도 1편의 세 가정(모든 x좌표가 다르고, 모든 y좌표가 다르고, 한 직선 위에 점이 3개 이상 없다)을 그대로 쓴다. 껍질을 최좌·최우 점 기준으로 **upper hull / lower hull** 두 단조 사슬로 나눠 보는 [3편](/blog/convex-hull-3)의 어휘도 이어받는다.

---

## 나누기 — merge sort의 기하 버전

merge sort를 떠올려 보자. 배열을 반으로 갈라 각각 정렬한 뒤, 정렬된 두 조각을 하나로 합친다. 합치는 일이 $O(N)$이면 전체가 $O(N \log N)$이 된다.

볼록 껍질도 같은 틀로 풀 수 있다. 점들을 x좌표로 정렬해 두고, 가운데를 기준으로 왼쪽 절반과 오른쪽 절반으로 가른다. 각 절반의 볼록 껍질을 재귀로 구한다. 점이 두세 개로 줄면 그 점들 자체가 껍질이니 재귀가 멈춘다.

![나누기 — 점을 x좌표 중앙에서 갈라 좌·우 부분 껍질을 각각 구한다. 두 껍질은 x좌표로 완전히 분리된다.](/images/convex-hull-4/dc-split.svg)

남은 일은 왼쪽 껍질과 오른쪽 껍질을 하나로 합치는 것이다. 두 껍질은 x좌표로 완전히 갈라져 있다. 즉 왼쪽 껍질의 모든 점이 오른쪽 껍질의 모든 점보다 왼쪽에 있다. 이 분리가 합치기를 깔끔하게 만든다.

재귀 구조는 merge sort와 판박이다. $T(N) = 2T(N/2) + (\text{합치는 비용})$. 합치기가 $O(N)$이면 전체 $O(N \log N)$이다. 그러니 관건은 하나다. **두 껍질을 얼마나 빨리 합치느냐.**

---

## 합치기의 핵심은 공통 접선

두 볼록 다각형을 하나로 감싸는 큰 껍질을 그려 보자. 새 껍질의 경계는 대부분 원래 두 껍질의 경계를 그대로 쓴다. 다만 두 군데에서 왼쪽 껍질과 오른쪽 껍질을 **다리처럼 잇는 변**이 새로 생긴다. 위를 잇는 다리가 **상단 공통 접선(upper common tangent)**, 아래를 잇는 다리가 **하단 공통 접선(lower common tangent)** 이다.

공통 접선이란 두 껍질에 동시에 닿으면서 두 껍질을 모두 한쪽에 두는 직선이다. 상단 접선은 두 껍질을 자기 아래에 두고, 하단 접선은 자기 위에 둔다.

![합치기 — 상·하 공통 접선이 두 껍질을 잇는다. 접선 바깥 사슬은 살아남고, 두 접선 사이에서 서로 마주 보는 안쪽 점들은 버려진다.](/images/convex-hull-4/dc-tangent.svg)

이 두 접선만 찾으면 합치기가 끝난다. 상단 접선의 두 접점을 잇고, 거기서 바깥으로 도는 사슬을 따라 내려가다 하단 접선의 두 접점에서 다시 이으면 그게 새 껍질이다. 두 접선 사이에서 서로 마주 보던 안쪽 사슬, 곧 왼쪽 껍질의 오른쪽 면과 오른쪽 껍질의 왼쪽 면은 새 경계 안에 갇혀 버려진다. 3편 Plane Sweeping에서 접선 사이 점을 버리던 것과 같은 장면이다.

그러니 합치기의 전부는 **상·하 공통 접선을 찾는 일**로 좁혀진다.

---

## 선형 워킹으로 공통 접선 — $O(N)$

하단 공통 접선부터 찾아보자. 자연스러운 출발점은 두 껍질이 가장 가까운 곳, 즉 **왼쪽 껍질의 최우점**과 **오른쪽 껍질의 최좌점**이다. 이 두 점을 잇는 직선에서 시작해, 직선이 양쪽 껍질을 모두 위로 떠받칠 때까지 두 끝점을 아래로 내린다.

내리는 규칙은 1편의 CCW로 판정한다. 지금 접선 후보가 왼쪽 점 $a$와 오른쪽 점 $b$를 잇고 있다고 하자.

- 오른쪽 껍질에서 $b$의 아래쪽 이웃이 직선 $a \to b$보다 아래에 있으면, 직선이 아직 오른쪽 껍질을 파고든다. $b$를 그 이웃으로 내린다.
- 왼쪽 껍질에서 $a$의 아래쪽 이웃이 직선보다 아래에 있으면, $a$를 그 이웃으로 내린다.
- 양쪽 다 더 내릴 데가 없으면 그게 하단 공통 접선이다.

![선형 워킹 — 두 껍질의 최우점·최좌점에서 시작해, 더 내려갈 수 없을 때까지 포인터를 한 칸씩 전진시켜 접선을 좁힌다.](/images/convex-hull-4/dc-walking.svg)

의사코드로 쓰면 이렇다.

```cpp
// L, R: 왼쪽·오른쪽 껍질(반시계 순서 배열). ccw()·struct P는 1편 정의.
// below(a, b, c): 점 c가 직선 a→b의 아래쪽인지 (ccw로 판정)
int a = rightmost(L);   // 왼쪽 껍질의 최우점
int b = leftmost(R);    // 오른쪽 껍질의 최좌점
while (true) {
    bool moved = false;
    while (below(L[a], R[b], R[nextDown(b)])) { b = nextDown(b); moved = true; }
    while (below(R[b], L[a], L[nextDown(a)])) { a = nextDown(a); moved = true; }
    if (!moved) break;
}
// (a, b) = 하단 공통 접선. 상단 접선은 위 방향으로 같은 방식.
```

**복잡도.** 각 포인터는 껍질을 한 방향으로만 돈다. 한 번 내려간 점으로 되돌아오지 않는다. 그러니 $a$와 $b$가 전진하는 총횟수가 두 껍질의 점 수를 넘지 못하고, 접선 하나를 $O(N)$에 찾는다. 상·하 두 접선 모두 $O(N)$, 접선 사이 사슬을 이어 붙이는 것도 $O(N)$이다. **합치기 전체가 $O(N)$이다.**

---

## merge와 전체 복잡도

이제 재귀를 완성한다.

```cpp
hull(points):
    점이 3개 이하면 그대로 반환
    x좌표 중앙에서 좌 / 우로 분할
    Lh = hull(왼쪽 절반)
    Rh = hull(오른쪽 절반)
    return merge(Lh, Rh)   // 상·하 공통 접선으로 잇기, O(N)
```

merge가 $O(N)$이니 재귀식은 $T(N) = 2T(N/2) + O(N)$, 풀면 $O(N \log N)$이다. 처음 한 번의 x좌표 정렬 $O(N \log N)$도 같은 차수라 전체는 $O(N \log N)$에 머문다. 3편이 예고한 대로, **merge sort의 재귀 구조가 기하에 그대로 옮겨졌다.** 배열을 합치던 자리에 두 껍질을 공통 접선으로 잇는 일이 들어갔을 뿐이다.

---

## 접선을 더 빨리 — 이진 탐색 $O(\log^2 N)$

선형 워킹은 접선 하나에 $O(N)$을 쓴다. 그런데 3편에서 얻은 도구가 하나 있다. **볼록 껍질의 각 사슬은 x좌표에 단조로워서, 접점 찾기가 이진 탐색의 자리라는 것.**

접선을 두 단계로 나눠 생각하자. 먼저 왼쪽 껍질의 한 점 $a$를 고정하면, $a$에서 오른쪽 껍질로 긋는 접선의 접점은 하나로 정해진다. 오른쪽 껍질 위 후보 점의 양옆 변이 $a$에서 봤을 때 어느 쪽으로 도는지를 CCW로 보면, 접점이 사슬의 앞인지 뒤인지 갈린다. 사슬이 단조로우니 이 판정으로 한쪽을 버리며 내려가 접점을 $O(\log N)$에 찾는다. (이 방향 판정의 케이스 분석은 [추가 설명 글](/blog/convex-hull-bst-tangent)에서 정리했다. 같은 도구를 여기서 다시 쓴다.)

![이진 탐색 접선 — 왼쪽 껍질의 고정점에서 오른쪽 껍질의 접점을 이진 탐색으로 $O(\log N)$에 찾는다.](/images/convex-hull-4/dc-binary-tangent.svg)

그럼 왼쪽 점 $a$는 어떻게 정할까? $a$를 옮겨 가며 매번 오른쪽 접점을 다시 구하는데, $a$의 위치도 **이진 탐색으로** 좁힐 수 있다. $a$에서의 오른쪽 접선이 왼쪽 껍질을 파고드는 방향을 보면 $a$를 어느 쪽으로 옮겨야 할지 정해지기 때문이다. $a$ 후보가 $O(\log N)$개, 각 후보마다 오른쪽 접점 찾기가 $O(\log N)$이니 공통 접선 하나가 $O(\log^2 N)$이다.

**그런데 이걸로 전체가 빨라지지는 않는다.** 접선을 $O(\log^2 N)$에 찾아도, 합친 껍질을 새 배열로 만들려면 살아남는 점들을 $O(N)$에 복사해야 한다. merge가 $O(N)$에서 내려오지 않으니 분할 정복 총복잡도는 여전히 $O(N \log N)$이다.

그렇다면 $O(\log^2 N)$ 접선은 언제 값진가? **껍질을 통째로 다시 만들 필요가 없을 때다.** 3편의 동적 갱신처럼 껍질을 균형 트리에 들고 있어, 접선 두 개만 알면 그 사이를 $O(\log N)$에 잘라 붙일 수 있는 상황이라면, 접선을 빨리 찾는 것이 곧 껍질을 빨리 고치는 것이 된다. 두 껍질을 합치는 이 접선 찾기가 바로 그 트리 기반 갱신의 심장이다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- **분할 정복**은 점을 x좌표로 절반씩 갈라 각 껍질을 재귀로 구한 뒤 **공통 접선**으로 잇는다. merge sort의 기하 버전이다.
- 두 껍질은 **상·하 공통 접선** 두 개로 합쳐진다. 접선 바깥 사슬은 살아남고, 두 접선 사이의 마주 보는 안쪽 사슬은 버려진다.
- **선형 워킹**은 두 껍질의 최우점·최좌점에서 포인터를 한 방향으로만 전진시켜 접선을 $O(N)$에 찾는다. merge $O(N)$이므로 전체 $O(N \log N)$.
- **이진 탐색**은 단조 사슬을 이용해 접선을 $O(\log^2 N)$에 찾지만, 껍질 배열 재구성이 $O(N)$이라 분할 정복 총복잡도는 그대로다. 껍질을 트리에 들고 갱신하는(3편) 상황에서 진가를 낸다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

5편에서는 껍질을 도구로 쓰는 문제로 넘어간다. 평면에서 **가장 먼 두 점(지름)** 을 찾는 일인데, 가장 먼 두 점은 반드시 껍질의 꼭짓점이다. 평행한 두 직선을 회전시키며 맞닿는 대척점 쌍만 훑는 **Rotating Calipers**로, 모든 쌍을 비교하는 $O(N^2)$ 대신 껍질을 구한 뒤 $O(N)$에 지름을 얻는다.

계산 기하의 다른 문제인 [가장 가까운 점 쌍](/blog/closest-pair-1)도 함께 보면 좋다.

</div>
````

- [ ] **Step 2: 빌드 검증**

Run: `npm run build`
Expected: 성공, "N page(s) built" 출력. KaTeX/frontmatter 오류 없음.

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-4.md
git commit -m "feat(convex-hull): 4편 본문 — 분할 정복과 공통 접선"
```

---

### Task 3: 3편 forward link 연결

**Files:**
- Modify: `src/content/posts/convex-hull-3.md` (이어지는 글의 "4편" 텍스트)

**Interfaces:**
- Consumes: Task 2가 만든 라우트 `/blog/convex-hull-4`.

- [ ] **Step 1: 3편의 "4편" 예고를 하이퍼링크로**

`src/content/posts/convex-hull-3.md`의 "이어지는 글" 문단에서:

찾기:
```
4편에서는 같은 $O(N \log N)$을 전혀 다른 길로 얻는다.
```
바꾸기:
```
[4편](/blog/convex-hull-4)에서는 같은 $O(N \log N)$을 전혀 다른 길로 얻는다.
```

(발행 후 앞 글 callout에 링크 연결 관례 — 미발행 땐 텍스트만.)

- [ ] **Step 2: 빌드 재검증**

Run: `npm run build`
Expected: 성공.

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-3.md
git commit -m "docs(convex-hull): 3편에서 4편으로 링크 연결"
```

---

### Task 4: 리뷰 (플랜 외 후속)

플랜 실행이 끝나면 `/review-post convex-hull-4`로 결정적 검사 + LLM 비평(L1~L7)을 돌리고, 지적을 반영한 뒤 재빌드한다. 리포트는 `docs/reviews/2026-07-13-convex-hull-4.md`에 기록한다. 반영 완료 후 PR 생성.

## Self-Review

**1. Spec coverage:** 스펙의 본문 9개 구성 요소(도입·목차·나누기·공통접선·선형워킹·merge복잡도·이진탐색·핵심정리·이어지는글)는 Task 2 본문에 모두 포함. SVG 4장은 Task 1. 3편 링크 연결 관례는 Task 3. 빌드/리뷰는 Task 2·4. 누락 없음.

**2. Placeholder scan:** SVG·본문·수정 문구 모두 실제 내용으로 인라인. "TBD/TODO/적절히" 없음.

**3. Type consistency:** SVG 좌/우 껍질 점 배치가 네 도판에서 동일(`100,240 …`, `400,215 …`). 본문 이미지 경로 4개가 Task 1 생성 파일과 일치. 의사코드 헬퍼(`below`, `nextDown`, `rightmost`, `leftmost`)는 본문 내에서 주석으로 의미 정의됨. 3편 치환 문구는 현재 파일 line 119와 일치.
