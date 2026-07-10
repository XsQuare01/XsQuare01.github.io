# 볼록 껍질 ③ 보강(접선 이진 탐색) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 3편이 미뤄둔 "접선 이진 탐색의 방향 판정"을 x-사슬 프레이밍으로 설명하는 추가 설명 포스트 `convex-hull-bst-tangent.md`와 SVG 3장을 만들고, 3편 callout에서 이 페이지로 링크를 연결한다.

**Architecture:** 기존 "추가 설명" 포스트(closest-pair-bst) 구조와 1·2·3편 SVG 스타일을 따른다. 수식은 KaTeX, 코드는 C++ 의사코드. 3편의 upper/lower hull + x-키 BST 프레이밍과 반드시 일관되게 쓴다.

**Tech Stack:** Astro content collections, remark-math + rehype-katex, 정적 SVG.

**Branch:** `feat/post-convex-hull-bst-tangent` (이미 생성·스펙 커밋 완료)

## Global Constraints

- frontmatter: `category: algorithm`, `difficulty: 고급`, date는 작성일 `2026-07-10T09:00:00`
- 코드 언어는 C++, 1편의 `ccw()` 재사용 서술
- 3편과 정합: upper/lower hull, **x좌표 단조 사슬**, x-키 BST. right-hull/y좌표로 서술하지 않는다
- 위쪽 접선만 본문에서 다루고 lower/아래쪽은 대칭이라고 서술
- main 직접 커밋 금지, 모든 커밋은 `feat/post-convex-hull-bst-tangent`에서
- SVG 색상: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 초록 `#34d399`/`#6ee7b7`, 파랑 `#93c5fd`/`#3b82f6`(채움 `#1e3a5f`), 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`, 각주 `#94a3b8`

---

## File Structure

- Create: `public/images/convex-hull-bst-tangent/tangent-condition.svg` — 접선 조건(접함 vs 뚫음)
- Create: `public/images/convex-hull-bst-tangent/direction-cases.svg` — 왼쪽/오른쪽 방향 판정
- Create: `public/images/convex-hull-bst-tangent/halving.svg` — BST 하강=사슬 반감
- Create: `src/content/posts/convex-hull-bst-tangent.md` — 본문
- Modify: `src/content/posts/convex-hull-3.md` — "방향 판정은 다음 글에서" callout에 링크 연결

figs 1·2는 같은 사슬·외부 점 배치를 공유한다(스크린 좌표, y 아래 방향):

| 점 | 좌표 | 비고 |
|---|---|---|
| 1 | (90, 300) | 최소 x |
| 2 | (170, 210) | |
| 3 | (250, 150) | fig2 후보 A(오른쪽으로) |
| 4 | (340, 120) | 위쪽 접점 t |
| 5 | (430, 150) | |
| 6 | (510, 220) | fig2 후보 B(왼쪽으로) |
| 7 | (580, 300) | 최대 x |
| p | (650, 200) | 외부 점(최우측) |

이 배치에서 위쪽 접점은 4번(직선 $p$–4 아래에 나머지 전부). 후보 3에서는 오른쪽 이웃 4가 직선 $p$–3 위로 삐져나오고, 후보 6에서는 왼쪽 이웃 5가 직선 $p$–6 위로 삐져나온다.

---

### Task 1: SVG 도판 3장 작성

**Files:**
- Create: `public/images/convex-hull-bst-tangent/tangent-condition.svg`
- Create: `public/images/convex-hull-bst-tangent/direction-cases.svg`
- Create: `public/images/convex-hull-bst-tangent/halving.svg`

**Interfaces:**
- Produces: 본문(Task 2)이 `/images/convex-hull-bst-tangent/<이름>.svg`로 참조

- [ ] **Step 1: tangent-condition.svg 작성**

```svg
<svg viewBox="0 0 720 400" width="1080" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="720" height="400" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="tc-up" markerWidth="9" markerHeight="9" refX="4.5" refY="8" orient="auto">
      <path d="M4.5,0 L9,9 L0,9 Z" fill="#f87171"/>
    </marker>
  </defs>

  <text x="360" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">접점의 조건 — 사슬이 직선 아래에 다 들어가는 꼭짓점</text>
  <text x="360" y="50" text-anchor="middle" fill="#64748b" font-size="11">접함: 두 이웃이 모두 직선 아래 · 뚫음: 이웃이 직선 위로 삐져나옴</text>

  <!-- chain (dim) -->
  <polyline points="90,300 170,210 250,150 340,120 430,150 510,220 580,300" fill="none" stroke="#334155" stroke-width="2"/>

  <!-- non-tangent line p-6 (red dashed) -->
  <line x1="430" y1="231" x2="650" y2="200" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 5"/>
  <!-- tangent line p-4 (green) -->
  <line x1="260" y1="99" x2="650" y2="200" stroke="#34d399" stroke-width="2.5"/>

  <!-- poke arrow at 5 -->
  <line x1="430" y1="150" x2="430" y2="196" stroke="#f87171" stroke-width="2" marker-end="url(#tc-up)"/>
  <text x="440" y="182" fill="#f87171" font-size="11" font-weight="600">이웃이 위로 → 뚫음</text>

  <!-- vertices -->
  <g fill="#0f1117" stroke="#64748b" stroke-width="2">
    <circle cx="90" cy="300" r="5"/><circle cx="170" cy="210" r="5"/><circle cx="250" cy="150" r="5"/>
    <circle cx="510" cy="220" r="5"/><circle cx="580" cy="300" r="5"/>
  </g>
  <circle cx="430" cy="150" r="6" fill="#1f2937" stroke="#f87171" stroke-width="2"/>
  <!-- tangent point 4 -->
  <circle cx="340" cy="120" r="7" fill="#34d399"/>
  <text x="330" y="108" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">접점 t</text>
  <!-- p -->
  <circle cx="650" cy="200" r="8" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="662" y="204" fill="#93c5fd" font-size="13" font-weight="700">p</text>

  <text x="360" y="384" text-anchor="middle" fill="#94a3b8" font-size="12">초록 직선은 사슬을 스치고(접선), 빨강 직선은 이웃 하나가 위로 나와 껍질을 뚫는다</text>
</svg>
```

- [ ] **Step 2: direction-cases.svg 작성**

```svg
<svg viewBox="0 0 720 400" width="1080" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="720" height="400" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="dc-r" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#fbbf24"/>
    </marker>
    <marker id="dc-l" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#93c5fd"/>
    </marker>
  </defs>

  <text x="360" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">왼쪽인가 오른쪽인가 — 위로 삐져나온 이웃 쪽으로</text>
  <text x="360" y="50" text-anchor="middle" fill="#64748b" font-size="11">후보의 두 이웃에 CCW를 돌려, 위로 나온 이웃이 있는 방향으로 내려간다</text>

  <!-- chain (dim) -->
  <polyline points="90,300 170,210 250,150 340,120 430,150 510,220 580,300" fill="none" stroke="#334155" stroke-width="2"/>

  <!-- candidate A: p-3 (amber), next 4 is above -> go right -->
  <line x1="180" y1="141" x2="650" y2="200" stroke="#fbbf24" stroke-width="2" stroke-dasharray="2 0" opacity="0.85"/>
  <circle cx="250" cy="150" r="7" fill="#1f2937" stroke="#fbbf24" stroke-width="2.5"/>
  <text x="238" y="172" fill="#fbbf24" font-size="12" font-weight="700">후보 A (3)</text>
  <line x1="360" y1="118" x2="405" y2="118" stroke="#fbbf24" stroke-width="2" marker-end="url(#dc-r)"/>
  <text x="350" y="104" fill="#fbbf24" font-size="11" font-weight="600">오른쪽 이웃(4) 위 → 오른쪽 자식</text>

  <!-- candidate B: p-6 (blue), prev 5 is above -> go left -->
  <line x1="450" y1="229" x2="650" y2="200" stroke="#93c5fd" stroke-width="2"/>
  <circle cx="510" cy="220" r="7" fill="#1f2937" stroke="#93c5fd" stroke-width="2.5"/>
  <text x="500" y="242" fill="#93c5fd" font-size="12" font-weight="700">후보 B (6)</text>
  <line x1="430" y1="150" x2="385" y2="150" stroke="#93c5fd" stroke-width="2" marker-end="url(#dc-l)"/>
  <text x="360" y="140" fill="#93c5fd" font-size="11" font-weight="600">왼쪽 이웃(5) 위 → 왼쪽 자식</text>

  <!-- other vertices -->
  <g fill="#0f1117" stroke="#64748b" stroke-width="2">
    <circle cx="90" cy="300" r="5"/><circle cx="170" cy="210" r="5"/>
    <circle cx="340" cy="120" r="5"/><circle cx="430" cy="150" r="5"/><circle cx="580" cy="300" r="5"/>
  </g>
  <!-- p -->
  <circle cx="650" cy="200" r="8" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="662" y="204" fill="#93c5fd" font-size="13" font-weight="700">p</text>

  <text x="360" y="384" text-anchor="middle" fill="#94a3b8" font-size="12">두 이웃이 다 아래면 그 후보가 접점 — 세 갈래 판정이 겹치지 않는다</text>
</svg>
```

- [ ] **Step 3: halving.svg 작성**

```svg
<svg viewBox="0 0 720 400" width="1080" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="720" height="400" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="hv-o" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#fbbf24"/>
    </marker>
  </defs>

  <text x="360" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">왜 이진 탐색인가 — 한 번 판정에 후보 절반이 사라진다</text>
  <text x="360" y="50" text-anchor="middle" fill="#64748b" font-size="11">후보는 트리의 한 노드 · 판정에 따라 왼/오른 자식으로 내려간다 (예: 오른쪽)</text>

  <!-- edges -->
  <g stroke="#334155" stroke-width="1.6">
    <line x1="360" y1="95" x2="220" y2="165"/><line x1="360" y1="95" x2="500" y2="165"/>
    <line x1="220" y1="165" x2="140" y2="235"/><line x1="220" y1="165" x2="300" y2="235"/>
    <line x1="500" y1="165" x2="420" y2="235"/><line x1="500" y1="165" x2="580" y2="235"/>
  </g>
  <!-- discarded left subtree (dim) -->
  <g font-size="12" font-weight="700" opacity="0.4">
    <circle cx="220" cy="165" r="16" fill="#0f1117" stroke="#64748b" stroke-width="2"/><text x="220" y="170" text-anchor="middle" fill="#94a3b8">2</text>
    <circle cx="140" cy="235" r="16" fill="#0f1117" stroke="#64748b" stroke-width="2"/><text x="140" y="240" text-anchor="middle" fill="#94a3b8">1</text>
    <circle cx="300" cy="235" r="16" fill="#0f1117" stroke="#64748b" stroke-width="2"/><text x="300" y="240" text-anchor="middle" fill="#94a3b8">3</text>
  </g>
  <text x="200" y="290" text-anchor="middle" fill="#64748b" font-size="11">작은 x 절반 — 후보에서 버림</text>
  <!-- active nodes -->
  <g font-size="12" font-weight="700">
    <circle cx="360" cy="95" r="17" fill="#1e3a5f" stroke="#fbbf24" stroke-width="2.5"/><text x="360" y="100" text-anchor="middle" fill="#fbbf24">4</text>
    <circle cx="500" cy="165" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="500" y="170" text-anchor="middle" fill="#93c5fd">6</text>
    <circle cx="420" cy="235" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="420" y="240" text-anchor="middle" fill="#93c5fd">5</text>
    <circle cx="580" cy="235" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="580" y="240" text-anchor="middle" fill="#93c5fd">7</text>
  </g>
  <!-- go-right arrow -->
  <line x1="382" y1="112" x2="478" y2="150" stroke="#fbbf24" stroke-width="2" marker-end="url(#hv-o)"/>
  <text x="470" y="120" fill="#fbbf24" font-size="11" font-weight="600">오른쪽으로</text>

  <!-- chain strip -->
  <text x="60" y="330" fill="#94a3b8" font-size="11" font-weight="600">사슬(x순)</text>
  <g>
    <circle cx="150" cy="355" r="7" fill="#0f1117" stroke="#64748b" stroke-width="2" opacity="0.4"/><text x="150" y="378" text-anchor="middle" fill="#64748b" font-size="10" opacity="0.6">1</text>
    <circle cx="220" cy="355" r="7" fill="#0f1117" stroke="#64748b" stroke-width="2" opacity="0.4"/><text x="220" y="378" text-anchor="middle" fill="#64748b" font-size="10" opacity="0.6">2</text>
    <circle cx="290" cy="355" r="7" fill="#0f1117" stroke="#64748b" stroke-width="2" opacity="0.4"/><text x="290" y="378" text-anchor="middle" fill="#64748b" font-size="10" opacity="0.6">3</text>
    <circle cx="360" cy="355" r="8" fill="#fbbf24"/><text x="360" y="378" text-anchor="middle" fill="#fbbf24" font-size="10" font-weight="700">4</text>
    <circle cx="430" cy="355" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="430" y="378" text-anchor="middle" fill="#93c5fd" font-size="10">5</text>
    <circle cx="500" cy="355" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="500" y="378" text-anchor="middle" fill="#93c5fd" font-size="10">6</text>
    <circle cx="570" cy="355" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="570" y="378" text-anchor="middle" fill="#93c5fd" font-size="10">7</text>
  </g>
  <text x="620" y="330" text-anchor="middle" fill="#64748b" font-size="11">높이 O(log N)</text>
</svg>
```

- [ ] **Step 4: 커밋**

```bash
git add public/images/convex-hull-bst-tangent/
git commit -m "feat(convex-hull): 3편 보강 SVG 도판 3장 추가"
```

---

### Task 2: 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-bst-tangent.md`

**Interfaces:**
- Consumes: Task 1의 SVG 3장
- Produces: 슬러그 `convex-hull-bst-tangent` (3편 callout 링크 대상)

- [ ] **Step 1: 포스트 파일 작성**

아래 내용을 그대로 작성한다.

`````markdown
---
title: "추가 설명 — 균형 트리에서 접선을 O(log N)에 찾기"
date: 2026-07-10T09:00:00
description: "볼록 껍질 ③이 미뤄둔 부분을 채운다. x좌표로 정렬된 볼록 사슬을 균형 트리에 담아 두면, 외부 점에서 그은 접선의 접점을 어떻게 O(log N)에 찾는가. 후보 꼭짓점의 두 이웃 변에 CCW를 돌려 왼쪽·오른쪽·여기를 가르는 방향 판정과, 그것이 왜 이진 탐색이 되는지를 그림으로 따라간다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "추가 설명"]
category: algorithm
difficulty: 고급
---

> [볼록 껍질 ③](/blog/convex-hull-3)에서 Plane Sweeping을 $O(N \log N)$으로 끌어내리며 "껍질을 균형 트리에 담으면 접선을 이진 탐색으로 $O(\log N)$에 찾는다"고 했다. 그때 미뤄둔 **방향 판정** — 트리를 내려갈 때 왼쪽으로 갈지 오른쪽으로 갈지를 무엇으로 정하는지 — 을 여기서 푼다.

<div class="callout">
<div class="callout-title">이 글에서 다루는 내용</div>

- 사슬 위에서 **접점이 만족하는 조건**
- 후보에서 **왼쪽·오른쪽·여기**를 가르는 CCW 판정
- "직선이 껍질을 **뚫고 들어가는가**"라는 직관
- 왜 후보가 매 단계 **절반**으로 줄어 $O(\log N)$인가
- C++ 의사코드

</div>

---

## 다시, 무대

3편에서 upper hull은 x좌표에 단조로운 볼록 사슬이었고, 이를 균형 BST에 **x를 키로** 담았다. 트리에 담긴 덕에 각 꼭짓점에서 두 가지에 바로 닿을 수 있다. 하나는 **사슬 이웃** — x가 바로 작은 꼭짓점(prev)과 바로 큰 꼭짓점(next) — 이고, 다른 하나는 **트리 자식** — 작은 x 쪽(왼쪽)과 큰 x 쪽(오른쪽) — 이다.

외부 점 $p$는 Plane Sweeping에서 늘 가장 오른쪽에 있다. $p$에서 이 사슬에 그을 수 있는 접선은 위·아래로 두 개인데, 여기서는 **위쪽 접선**만 다룬다. lower hull과 아래쪽 접선은 위아래를 뒤집으면 똑같다.

---

## 접점의 조건

위쪽 접선의 접점 $t$는 한마디로 **직선 $p$–$t$ 아래에 사슬 전체가 들어가는** 꼭짓점이다. 하지만 사슬 전체를 매번 확인하면 $O(N)$이라 이진 탐색이 되지 않는다. 다행히 볼록성 덕분에 이 조건이 **국소 조건**으로 바뀐다.

> 꼭짓점 $t$의 두 이웃(prev, next)이 **모두 직선 $p$–$t$ 아래**에 있으면, $t$가 접점이다.

반대로 어떤 후보 $v$에서 이웃 하나가 직선 $p$–$v$ **위로 삐져나오면**, 그 직선은 사슬을 스치는 게 아니라 **뚫고 들어간다.** 뚫고 들어간다는 건 사슬이 그 직선 위로 더 솟은 부분이 있다는 뜻이고, 그러니 $v$는 접점이 아니다.

![접점의 조건 — 초록 직선(p–t)은 두 이웃이 모두 아래라 사슬을 스치는 접선이고, 빨강 직선은 이웃 하나가 위로 삐져나와 껍질을 뚫는다.](/images/convex-hull-bst-tangent/tangent-condition.svg)

---

## 왼쪽인가 오른쪽인가

접점이 아니라면, 어느 쪽으로 가야 접점에 가까워질까? 답은 방금 본 "뚫음"에 있다. **직선이 뚫고 들어간 쪽, 즉 이웃이 위로 삐져나온 쪽에 접점이 있다.** 그래서 후보 $v$에서 볼 것은 두 이웃뿐이다. $v$의 오른쪽 이웃(next)과 왼쪽 이웃(prev)이 각각 직선 $p$–$v$의 위인지 아래인지를, 1편의 CCW로 판정한다.

- **오른쪽 이웃이 위로 삐져나옴** → 접점은 더 오른쪽(큰 x). 트리에서 **오른쪽 자식**으로.
- **왼쪽 이웃이 위로 삐져나옴** → 접점은 더 왼쪽(작은 x). **왼쪽 자식**으로.
- **둘 다 아래** → $v$가 접점. 멈춘다.

![왼쪽인가 오른쪽인가 — 후보 A(3)는 오른쪽 이웃 4가 위로 나와 오른쪽으로, 후보 B(6)는 왼쪽 이웃 5가 위로 나와 왼쪽으로 내려간다.](/images/convex-hull-bst-tangent/direction-cases.svg)

<div class="callout callout-simple">
<div class="callout-title">두 이웃이 동시에 위로 나오지는 않는다</div>

볼록한(위로 볼록한) 사슬에서, 한 후보의 두 이웃이 동시에 직선 $p$–$v$ 위로 솟는 일은 없다. 그러려면 $v$가 두 이웃보다 아래로 파인 골짜기여야 하는데, 위로 볼록한 사슬에는 그런 꼭짓점이 없기 때문이다. 그래서 위 세 갈래가 서로 겹치지 않고 언제나 하나로 정해진다.

</div>

---

## 왜 이진 탐색인가

후보 $v$는 트리의 한 노드다. 판정이 "오른쪽"이면 오른쪽 자식으로, "왼쪽"이면 왼쪽 자식으로 내려간다. 트리는 x를 키로 균형 잡혀 있으니, **오른쪽 자식으로 가는 순간 x가 $v$보다 작은 꼭짓점 절반이 통째로 후보에서 빠진다.** 매 단계 후보가 절반으로 줄고, 트리 높이가 $O(\log N)$이므로 접점도 $O(\log N)$에 나온다.

![왜 이진 탐색인가 — 후보는 트리의 한 노드이고, 오른쪽으로 판정되면 작은 x 절반(왼쪽 서브트리)이 통째로 후보에서 사라진다. 높이 O(log N)만큼 내려가면 접점이다.](/images/convex-hull-bst-tangent/halving.svg)

이것이 3편에서 "이진 탐색으로 $O(\log N)$"이라고 한 말의 속이다. 사슬을 왼쪽부터 훑으면 $O(N)$이지만, 방향 판정이 매번 **가지 않을 절반**을 알려 주므로 트리를 타고 곧장 접점까지 내려갈 수 있다.

---

## 코드로

지금까지의 세 갈래 판정을 그대로 옮기면 된다.

```cpp
// upper: upper hull을 x좌표 키로 담은 균형 BST
//   각 노드에서 사슬 이웃(prev: x가 바로 작은 꼭짓점, next: 바로 큰 꼭짓점)과
//   트리 자식(left: 작은 x쪽, right: 큰 x쪽)에 모두 닿을 수 있다.
// p: 외부 점(스위핑에서 가장 오른쪽), ccw(): 1편에서 정의

// q가 직선 p–v의 '위쪽(바깥)'에 있는가 — 부호는 그림의 방향(위쪽 접선)에 맞춘다
bool above(P p, P v, P q) { return ccw(p, v, q) > 0; }

Node* upperTangent(Node* root, P p) {
    Node* v = root;
    while (true) {
        P c = v->point;
        bool rightUp = v->next && above(p, c, v->next->point);  // 오른쪽 이웃이 위
        bool leftUp  = v->prev && above(p, c, v->prev->point);  // 왼쪽 이웃이 위
        if      (rightUp) v = v->right;   // 접점은 더 오른쪽(큰 x)
        else if (leftUp)  v = v->left;    // 접점은 더 왼쪽(작은 x)
        else              return v;       // 두 이웃 다 아래 → 접점
    }
}
```

`above`의 부등호 방향은 좌표계와 "위쪽"의 정의에 맞춰 고정한 것이고, 나머지는 그림의 세 갈래를 그대로 옮긴 것이다. 아래쪽 접선은 이 부호와 자식 방향을 뒤집으면 된다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 위쪽 접점 $t$는 **직선 $p$–$t$ 아래에 사슬 전체가 들어가는** 꼭짓점이고, 볼록성 덕분에 "$t$의 두 이웃이 모두 그 직선 아래"라는 국소 조건으로 판정된다.
- 후보 $v$에서 두 이웃에 CCW를 돌려, **위로 삐져나온 이웃이 있는 쪽(뚫고 들어간 쪽)** 으로 간다. 오른쪽 이웃이 위면 오른쪽 자식, 왼쪽 이웃이 위면 왼쪽 자식, 둘 다 아래면 접점.
- 위로 볼록한 사슬에서는 두 이웃이 동시에 위로 나오지 않으므로 판정이 항상 하나로 정해진다.
- 트리 자식으로 내려갈 때마다 x 기준 **절반**이 후보에서 빠지므로, 접점을 $O(\log N)$에 찾는다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>이 방향 판정을 쓰는 전체 알고리즘 — Plane Sweeping을 $O(N \log N)$으로, 그리고 완성된 껍질을 점 추가마다 갱신하는 동적 볼록 껍질 — 은 <a href="/blog/convex-hull-3">볼록 껍질 ③ — Plane Sweeping과 동적 갱신</a>에서 다룬다. 아래쪽 접선과 lower hull은 위아래를 뒤집으면 그대로다.</p>
</div>
`````

- [ ] **Step 2: 커밋**

```bash
git add src/content/posts/convex-hull-bst-tangent.md
git commit -m "feat(convex-hull): 3편 보강 본문(접선 이진 탐색) 추가"
```

---

### Task 3: 3편 callout에 링크 연결

**Files:**
- Modify: `src/content/posts/convex-hull-3.md`

**Interfaces:**
- Consumes: Task 2의 슬러그 `convex-hull-bst-tangent`

- [ ] **Step 1: callout 문장에 링크 추가**

`src/content/posts/convex-hull-3.md`의 "방향 판정은 다음 글에서" callout 안에서 아래 문장을 찾아 링크를 건다.

찾을 문자열:
```
이 케이스 분석은 별도의 **추가 설명** 글에서 따로 정리한다.
```

바꿀 문자열:
```
이 케이스 분석은 [별도의 **추가 설명** 글](/blog/convex-hull-bst-tangent)에서 따로 정리한다.
```

- [ ] **Step 2: 커밋**

```bash
git add src/content/posts/convex-hull-3.md
git commit -m "docs(convex-hull): 3편 callout에서 접선 보강 글로 링크 연결"
```

---

### Task 4: 빌드 검증

**Files:** (없음 — 검증 전용)

- [ ] **Step 1: 빌드 실행**

Run: `npm run build`
Expected: 에러 없이 완료. 출력에 `convex-hull-bst-tangent` 페이지가 생성되고, `convex-hull-3` 페이지도 정상 재생성.

- [ ] **Step 2: 빌드 실패 시 대응**

스키마 오류면 프론트매터(`category: algorithm`, `difficulty: 고급`)를 확인한다. KaTeX 오류면 수식의 `$`/`$$` 짝과 백슬래시를 확인한다. 수정 후 Step 1 재실행.

---

### Task 5: 포스트 리뷰

**Files:** (없음)

- [ ] **Step 1: review-post skill 실행**

`/review-post convex-hull-bst-tangent` 로 리뷰한다. 특히 L7에서 (1) 접점의 국소 조건("두 이웃 모두 아래")이 볼록 사슬에서 옳은지, (2) 방향 판정 세 갈래가 MECE인지("두 이웃 동시 위로 불가" 근거 포함), (3) 트리 자식 하강이 x-절반을 소거해 $O(\log N)$인지 점검한다. 지적 반영 후 다시 커밋한다.

---

### Task 6: PR 생성

**Files:** (없음)

- [ ] **Step 1: push 및 PR 생성**

```bash
git push -u origin feat/post-convex-hull-bst-tangent
gh pr create --title "feat(convex-hull): 추가 설명 — 균형 트리에서 접선을 O(log N)에 찾기" --body "..."
```

PR 본문은 사용자 지침(2026-06-30)을 따른다: **Why는 충분히 길게**(3편이 의도적으로 미룬 하드 코어를 채워 시리즈 완결성 확보, 어려운 곁가지를 본문에서 분리해 별도 페이지로 두는 편집 방침, 3편 callout의 forward reference를 실제 링크로 잇는 마감), **How는 방법론 중심**(접점의 전역 조건을 볼록성으로 국소 조건으로 환원, 뚫음=방향이라는 직관, 트리 자식 하강의 x-절반 소거로 O(log N), 3편 x-사슬 프레이밍과의 정합). 구체 파일 경로는 '참조 코드 위치' 섹션에만.

---

## Self-Review

**1. Spec coverage:**
- 본문 5개 섹션(무대 → 접점 조건 → 방향 판정 → 이진 탐색 → 코드) + 정리/예고 — Task 2.
- SVG 3장(tangent-condition, direction-cases, halving) — Task 1.
- 3편 callout 링크 연결 — Task 3.
- x-사슬 정합, 위쪽 접선만+lower 대칭 서술 — Task 2 본문에 반영.
- 빌드 Task 4, 리뷰 Task 5, PR Task 6.
- 갭 없음.

**2. Placeholder scan:** SVG·본문 전체가 코드 블록으로 포함됨. PR 본문만 방향 서술(작성 시 확정) — 지침 참조로 대체.

**3. Type consistency:** SVG 파일명 3개가 본문 `![...]` 참조와 일치. figs 1·2가 공유 점 배치(1~7, p) 사용. 슬러그 `convex-hull-bst-tangent`가 Task 3의 링크 대상과 일치. 프론트매터 키는 기존 "추가 설명" 포스트(closest-pair-bst)와 동일 구조. 의사코드 `ccw`는 1편 정의 재사용, `above`/`upperTangent`는 본문 안에서 자기완결.
