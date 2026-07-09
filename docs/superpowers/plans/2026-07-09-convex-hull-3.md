# 볼록 껍질 ③ 포스트 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 노션 `Convex hull 2` 노트의 Plane Sweeping·Dynamic Case 섹션을 블로그 포스트 `convex-hull-3.md`와 SVG 도판 5장으로 옮긴다.

**Architecture:** 1·2편 구조(도입 blockquote → 목차 callout → 본문 → 핵심 정리 → 이어지는 글)와 SVG 스타일(다크 배경 `#0f1117`, 초록/파랑/주황 팔레트)을 그대로 따른다. 수식은 KaTeX, 코드는 C++ 의사코드 수준(컴파일 검증 불필요). 어려운 BST 이진 탐색 방향 판정은 본문에 넣지 않고 예고로만 남긴다.

**Tech Stack:** Astro content collections, remark-math + rehype-katex, 정적 SVG.

**Branch:** `feat/post-convex-hull-3` (이미 생성·스펙 커밋 완료)

## Global Constraints

- frontmatter: `category: algorithm`, `difficulty: 중급`, date는 작성일 `2026-07-09T09:00:00`
- 코드 언어는 C++, 1편의 `struct P`·`ccw()`를 재사용한다고 서술
- main 직접 커밋 금지, 모든 커밋은 `feat/post-convex-hull-3`에서
- BST 이진 탐색 방향 판정(뚫고 들어감/나감 케이스 분석)은 본문 제외, "다음 추가 설명 글" forward reference로만 (죽은 링크 금지)
- SVG 색상 규칙: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 초록 `#34d399`(+연초록 `#6ee7b7`), 파랑 `#93c5fd`/`#3b82f6`(채움 `#1e3a5f`), 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`, 각주 `#94a3b8`

---

## File Structure

- Create: `public/images/convex-hull-3/upper-lower.svg` — upper/lower hull 분해
- Create: `public/images/convex-hull-3/sweep-tangent.svg` — O(N²) 접선 찾기
- Create: `public/images/convex-hull-3/sweep-result.svg` — 접선 splice 후 새 껍질
- Create: `public/images/convex-hull-3/bst-idea.svg` — 껍질을 BST에 담아 이진 탐색(개념도)
- Create: `public/images/convex-hull-3/dynamic.svg` — 안쪽/바깥쪽 점 추가 대비
- Create: `src/content/posts/convex-hull-3.md` — 포스트 본문

sweep-tangent와 sweep-result는 **같은 점 배치**를 공유한다(현재 껍질 7점 + 새 점 p). 배치(스크린 좌표, y 아래 방향):

| 점 | 좌표 | 역할 |
|---|---|---|
| c0 | (130, 225) | 최좌측 |
| c1 | (235, 122) | upper |
| c2 | (360, 108) | upper·위쪽 접점 |
| c3 | (452, 168) | 버려짐 |
| c4 | (470, 262) | 버려짐 |
| c5 | (360, 338) | lower·아래쪽 접점 |
| c6 | (208, 322) | lower |
| p | (606, 205) | 새 점(최우) |

---

### Task 1: SVG 도판 5장 작성

**Files:**
- Create: `public/images/convex-hull-3/upper-lower.svg`
- Create: `public/images/convex-hull-3/sweep-tangent.svg`
- Create: `public/images/convex-hull-3/sweep-result.svg`
- Create: `public/images/convex-hull-3/bst-idea.svg`
- Create: `public/images/convex-hull-3/dynamic.svg`

**Interfaces:**
- Produces: 포스트 본문(Task 2)이 `/images/convex-hull-3/<이름>.svg`로 참조

- [ ] **Step 1: upper-lower.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">껍질을 반으로 나누기 — upper hull / lower hull</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">최좌측 점 L과 최우측 점 R이 껍질을 위아래 두 사슬로 가른다</text>

  <!-- filled hull -->
  <polygon points="120,240 250,125 400,108 525,168 590,248 445,335 255,345"
           fill="#1e293b40" stroke="none"/>

  <!-- lower hull chain (green) -->
  <polyline points="120,240 255,345 445,335 590,248" fill="none" stroke="#34d399" stroke-width="3"/>
  <!-- upper hull chain (blue) -->
  <polyline points="120,240 250,125 400,108 525,168 590,248" fill="none" stroke="#3b82f6" stroke-width="3"/>

  <!-- intermediate vertices -->
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="250" cy="125" r="5"/><circle cx="400" cy="108" r="5"/><circle cx="525" cy="168" r="5"/>
  </g>
  <g fill="#0f1117" stroke="#34d399" stroke-width="2">
    <circle cx="255" cy="345" r="5"/><circle cx="445" cy="335" r="5"/>
  </g>

  <!-- L, R -->
  <circle cx="120" cy="240" r="8" fill="#fbbf24"/>
  <text x="96" y="262" fill="#fbbf24" font-size="12" font-weight="700">L</text>
  <circle cx="590" cy="248" r="8" fill="#fbbf24"/>
  <text x="600" y="252" fill="#fbbf24" font-size="12" font-weight="700">R</text>

  <!-- labels -->
  <text x="360" y="95" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">upper hull</text>
  <text x="350" y="372" text-anchor="middle" fill="#6ee7b7" font-size="13" font-weight="700">lower hull</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">각 사슬은 x좌표에 대해 단조롭다 — 이 성질이 이진 탐색을 가능하게 한다</text>
</svg>
```

- [ ] **Step 2: sweep-tangent.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="st-g" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Plane Sweeping 한 걸음 — 접선 두 개로 새 점 붙이기</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">새 점 p(가장 오른쪽)에서 위·아래 접선을 긋고 사이 점을 버린다</text>

  <!-- sweeping line -->
  <line x1="545" y1="70" x2="545" y2="360" stroke="#475569" stroke-width="1.3" stroke-dasharray="6 5"/>
  <text x="545" y="384" text-anchor="middle" fill="#64748b" font-size="10">sweeping line</text>

  <!-- current hull outline (dim) -->
  <polygon points="130,225 235,122 360,108 452,168 470,262 360,338 208,322"
           fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>

  <!-- tangents -->
  <line x1="606" y1="205" x2="360" y2="108" stroke="#34d399" stroke-width="2.5" marker-end="url(#st-g)"/>
  <line x1="606" y1="205" x2="360" y2="338" stroke="#34d399" stroke-width="2.5" marker-end="url(#st-g)"/>
  <text x="470" y="135" fill="#6ee7b7" font-size="12" font-weight="600">위쪽 접선</text>
  <text x="470" y="300" fill="#6ee7b7" font-size="12" font-weight="600">아래쪽 접선</text>

  <!-- tangent points -->
  <circle cx="360" cy="108" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.5"/>
  <circle cx="360" cy="338" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.5"/>

  <!-- kept vertices -->
  <g fill="#0f1117" stroke="#64748b" stroke-width="2">
    <circle cx="130" cy="225" r="5"/><circle cx="235" cy="122" r="5"/>
    <circle cx="208" cy="322" r="5"/>
  </g>

  <!-- discarded vertices (red X) -->
  <g stroke="#ef4444" stroke-width="2">
    <circle cx="452" cy="168" r="7" fill="#1f2937"/>
    <line x1="446" y1="162" x2="458" y2="174"/><line x1="458" y1="162" x2="446" y2="174"/>
    <circle cx="470" cy="262" r="7" fill="#1f2937"/>
    <line x1="464" y1="256" x2="476" y2="268"/><line x1="476" y1="256" x2="464" y2="268"/>
  </g>
  <text x="486" y="215" fill="#f87171" font-size="12" font-weight="600">버려지는 점</text>

  <!-- new point p -->
  <circle cx="606" cy="205" r="8" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="618" y="209" fill="#93c5fd" font-size="13" font-weight="700">p</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">두 접점 사이, p를 마주 보는 점들은 새 경계 안쪽에 갇혀 버려진다</text>
</svg>
```

- [ ] **Step 3: sweep-result.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">갱신된 껍질 — p가 껍질에 들어가고 두 점이 내부로</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">접점 사이 점을 버리고 그 자리에 p를 끼우면 한 걸음이 끝난다</text>

  <!-- new hull -->
  <polygon points="130,225 235,122 360,108 606,205 360,338 208,322"
           fill="#34d39914" stroke="#34d399" stroke-width="2.5"/>

  <!-- interior (discarded) points -->
  <g fill="#64748b">
    <circle cx="452" cy="168" r="5"/><circle cx="470" cy="262" r="5"/>
  </g>
  <text x="486" y="222" fill="#94a3b8" font-size="11">내부가 된 점</text>

  <!-- hull vertices -->
  <g fill="#0f1117" stroke="#34d399" stroke-width="2">
    <circle cx="130" cy="225" r="6"/><circle cx="235" cy="122" r="6"/><circle cx="360" cy="108" r="6"/>
    <circle cx="360" cy="338" r="6"/><circle cx="208" cy="322" r="6"/>
  </g>
  <circle cx="606" cy="205" r="8" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="618" y="209" fill="#93c5fd" font-size="13" font-weight="700">p</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">다음 점이 오면 이 껍질을 상대로 같은 일을 되풀이한다</text>
</svg>
```

- [ ] **Step 4: bst-idea.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="bi-o" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#fbbf24"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">껍질을 균형 트리에 담으면 접선을 이진 탐색으로</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">껍질 점을 y좌표 순으로 저장 → 새 점의 접점을 O(log N)에 찾는다</text>

  <!-- left: hull with y-ordered vertices -->
  <polygon points="90,180 175,95 235,205 150,320 70,255"
           fill="#1e293b40" stroke="#3b82f6" stroke-width="2"/>
  <g font-size="12" font-weight="700">
    <circle cx="175" cy="95" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="188" y="92" fill="#93c5fd">B</text>
    <circle cx="90" cy="180" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="66" y="178" fill="#93c5fd">A</text>
    <circle cx="235" cy="205" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="248" y="209" fill="#93c5fd">C</text>
    <circle cx="70" cy="255" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="46" y="259" fill="#93c5fd">E</text>
    <circle cx="150" cy="320" r="7" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="163" y="336" fill="#93c5fd">D</text>
  </g>
  <!-- new point p -->
  <circle cx="300" cy="150" r="7" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="300" y="138" text-anchor="middle" fill="#93c5fd" font-size="12" font-weight="700">p</text>

  <!-- right: balanced BST keyed by y -->
  <text x="500" y="88" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="600">y좌표 균형 트리</text>
  <!-- edges -->
  <g stroke="#334155" stroke-width="1.6">
    <line x1="500" y1="120" x2="440" y2="185"/>
    <line x1="500" y1="120" x2="560" y2="185"/>
    <line x1="440" y1="185" x2="400" y2="250"/>
    <line x1="560" y1="185" x2="600" y2="250"/>
  </g>
  <!-- nodes -->
  <g font-size="12" font-weight="700">
    <circle cx="500" cy="120" r="16" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/><text x="500" y="125" text-anchor="middle" fill="#93c5fd">C</text>
    <circle cx="440" cy="185" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="440" y="190" text-anchor="middle" fill="#93c5fd">A</text>
    <circle cx="560" cy="185" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="560" y="190" text-anchor="middle" fill="#93c5fd">E</text>
    <circle cx="400" cy="250" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="400" y="255" text-anchor="middle" fill="#93c5fd">B</text>
    <circle cx="600" cy="250" r="16" fill="#0f1117" stroke="#3b82f6" stroke-width="2"/><text x="600" y="255" text-anchor="middle" fill="#93c5fd">D</text>
  </g>

  <!-- binary search path arrow -->
  <path d="M 318 158 C 400 150 470 110 484 112" fill="none" stroke="#fbbf24" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#bi-o)"/>
  <text x="470" y="300" text-anchor="middle" fill="#fbbf24" font-size="11" font-weight="600">루트에서 CCW로 방향을 정하며 내려간다</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">매 걸음 껍질을 다 훑는 대신, 트리 높이만큼만 내려가면 접점이 나온다</text>
</svg>
```

- [ ] **Step 5: dynamic.svg 작성**

```svg
<svg viewBox="0 0 760 400" width="1140" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="760" height="400" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="dy-g" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="380" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Dynamic Case — 점이 추가될 때 껍질 고치기</text>
  <text x="380" y="50" text-anchor="middle" fill="#64748b" font-size="11">새 점이 껍질 안이면 그대로, 밖이면 접선 두 개로 잘라 붙인다</text>

  <!-- divider -->
  <line x1="380" y1="72" x2="380" y2="368" stroke="#334155" stroke-width="1.3" stroke-dasharray="4 4"/>

  <!-- LEFT: inside -->
  <text x="185" y="92" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">안쪽 추가 → 변화 없음</text>
  <polygon points="70,180 140,110 250,130 270,240 170,300 80,255"
           fill="#34d39914" stroke="#34d399" stroke-width="2.5"/>
  <g fill="#0f1117" stroke="#34d399" stroke-width="2">
    <circle cx="70" cy="180" r="5"/><circle cx="140" cy="110" r="5"/><circle cx="250" cy="130" r="5"/>
    <circle cx="270" cy="240" r="5"/><circle cx="170" cy="300" r="5"/><circle cx="80" cy="255" r="5"/>
  </g>
  <circle cx="165" cy="205" r="7" fill="none" stroke="#93c5fd" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="178" y="209" fill="#93c5fd" font-size="12" font-weight="700">X</text>
  <text x="185" y="352" text-anchor="middle" fill="#94a3b8" font-size="11">X가 두 사슬 사이에 있으니 껍질 불변</text>

  <!-- RIGHT: outside -->
  <text x="575" y="92" text-anchor="middle" fill="#f87171" font-size="13" font-weight="700">바깥 추가 → 접선 2개로 splice</text>
  <polygon points="440,180 510,110 610,130 630,240 530,300 450,255"
           fill="#1e293b30" stroke="#334155" stroke-width="1.6"/>
  <!-- tangents from X -->
  <line x1="720" y1="175" x2="610" y2="130" stroke="#34d399" stroke-width="2.5" marker-end="url(#dy-g)"/>
  <line x1="720" y1="175" x2="530" y2="300" stroke="#34d399" stroke-width="2.5" marker-end="url(#dy-g)"/>
  <circle cx="610" cy="130" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.5"/>
  <circle cx="530" cy="300" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.5"/>
  <!-- kept vertices -->
  <g fill="#0f1117" stroke="#64748b" stroke-width="2">
    <circle cx="440" cy="180" r="5"/><circle cx="510" cy="110" r="5"/><circle cx="450" cy="255" r="5"/>
  </g>
  <!-- removed vertex -->
  <g stroke="#ef4444" stroke-width="2">
    <circle cx="630" cy="240" r="7" fill="#1f2937"/>
    <line x1="624" y1="234" x2="636" y2="246"/><line x1="636" y1="234" x2="624" y2="246"/>
  </g>
  <!-- X -->
  <circle cx="720" cy="175" r="8" fill="#93c5fd" stroke="#3b82f6" stroke-width="2"/>
  <text x="710" y="162" fill="#93c5fd" font-size="12" font-weight="700">X</text>
  <text x="575" y="352" text-anchor="middle" fill="#94a3b8" font-size="11">접선 사이 점을 버리고 X를 끼운다 — Plane Sweeping 한 걸음과 같다</text>
</svg>
```

- [ ] **Step 6: 커밋**

```bash
git add public/images/convex-hull-3/
git commit -m "feat(convex-hull): 3편 SVG 도판 5장 추가"
```

---

### Task 2: 포스트 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-3.md`

**Interfaces:**
- Consumes: Task 1의 SVG 5장 (`/images/convex-hull-3/*.svg`)
- Produces: 슬러그 `convex-hull-3` (2편 "이어지는 글" 예고 대상)

- [ ] **Step 1: 포스트 파일 작성**

아래 내용을 그대로 작성한다.

`````markdown
---
title: "볼록 껍질 ③ — Plane Sweeping과 동적 갱신"
date: 2026-07-09T09:00:00
description: "점이 왼쪽부터 하나씩 도착하거나, 껍질을 다 구한 뒤에도 새 점이 계속 밀려온다면? Plane Sweeping은 점을 x좌표 순으로 삼키며 껍질을 키운다. 모든 껍질 점을 훑어 접선을 찾는 O(N²)에서 출발해, 껍질을 균형 이진 트리에 담아 접선을 이진 탐색으로 찾는 O(N log N)까지 내려간다. 나아가 완성된 껍질에 점이 추가될 때마다 고쳐 나가는 동적 볼록 껍질을 다룬다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Plane Sweeping"]
category: algorithm
difficulty: 중급
---

> [1편](/blog/convex-hull-1)의 Package Wrapping도, [2편](/blog/convex-hull-2)의 Graham Scan도 점을 전부 미리 늘어놓고 시작했다. 하지만 점이 왼쪽부터 하나씩 도착한다면? 혹은 껍질을 다 구한 뒤에도 새 점이 계속 밀려온다면? 이번 편은 껍질을 **한 점씩 삼키며 키우는** Plane Sweeping과, 완성된 껍질을 **점 추가마다 고쳐 나가는** 동적 갱신을 다룬다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 껍질을 **upper / lower 두 사슬**로 나누는 어휘
- 점을 왼쪽부터 삼키는 **Plane Sweeping** $O(N^2)$
- 껍질을 균형 이진 트리에 담아 접선을 이진 탐색하는 $O(N \log N)$
- 완성된 껍질을 점 추가마다 고치는 **Dynamic Case**

</div>

이번에도 1편의 세 가정(모든 x좌표가 다르고, 모든 y좌표가 다르고, 한 직선 위에 점이 3개 이상 없다)을 그대로 쓴다.

---

## 껍질을 반으로 나누기

평면의 볼록 껍질은 하나의 닫힌 다각형이지만, 알고리즘을 세울 때는 이를 **두 개의 열린 사슬**로 쪼개는 편이 편하다.

가장 왼쪽 점 $L$과 가장 오른쪽 점 $R$은 반드시 껍질 위에 있다. 1편에서 최하단 점이 껍질 위에 있던 것과 같은 이유로, 모든 점이 $L$의 오른쪽·$R$의 왼쪽에 있기 때문이다. 이 두 점이 껍질을 위아래로 가른다. $L$에서 $R$로 이어지는 위쪽 사슬을 **upper hull**, 아래쪽 사슬을 **lower hull**이라 부른다.

![껍질을 반으로 나누기 — 최좌측 L과 최우측 R이 껍질을 upper hull(위)과 lower hull(아래) 두 사슬로 가른다.](/images/convex-hull-3/upper-lower.svg)

이렇게 나눠 두면 각 사슬이 **x좌표에 대해 단조롭다.** upper hull을 왼쪽부터 따라가면 x가 계속 커지고, lower hull도 마찬가지다. 단조로운 수열에서 원하는 값을 찾는 일은 이진 탐색의 자리다. 이 성질은 뒤에서 접선을 $O(\log N)$에 찾을 때, 그리고 4편의 분할정복에서 두 껍질을 이을 때 결정적으로 쓰인다.

---

## Plane Sweeping — $O(N^2)$

**스위핑 라인(sweeping line)** 은 세로 직선을 평면의 왼쪽 끝에서 오른쪽으로 쓸고 지나가는 상상이다. 실제 구현은 직선을 연속으로 움직이는 게 아니라, **x좌표가 작은 점부터 하나씩 처리하는 이벤트 점프**다. 라인이 지나온 왼쪽 영역에는 늘 "지금까지 본 점들의 볼록 껍질"을 유지한다.

점을 x좌표 순으로 정렬해 두었으니, 새로 처리하는 점 $p$는 언제나 지금까지 본 어떤 점보다 오른쪽에 있다. 이 사실 덕분에 $p$를 껍질에 더하는 일이 단순해진다. $p$에서 현재 껍질로 **위쪽 접선**과 **아래쪽 접선**을 하나씩 긋는다.

![Plane Sweeping 한 걸음 — 새 점 p에서 현재 껍질에 위·아래 접선을 긋는다. 두 접점 사이에서 p를 마주 보는 점들은 버려진다.](/images/convex-hull-3/sweep-tangent.svg)

두 접선이 닿는 두 접점 사이, $p$를 마주 보는 쪽의 껍질 점들은 이제 $p$와 접점들이 만든 새 경계 안쪽에 갇힌다. 이들을 버리고 그 자리에 $p$를 끼우면 갱신이 끝난다.

![갱신된 껍질 — 접점 사이 점을 버리고 p를 끼운 결과. 버려진 점은 내부가 된다.](/images/convex-hull-3/sweep-result.svg)

접선은 어떻게 찾을까? 가장 단순하게는 현재 껍질의 점을 **전부 훑는다.** $p$에서 봤을 때 가장 위(왼쪽)로 도는 점이 위쪽 접점, 가장 아래(오른쪽)로 도는 점이 아래쪽 접점이다. 방향 비교는 물론 1편의 CCW로 한다.

```cpp
// hull: 지금까지 본 점들의 껍질(반시계 순서), ccw()·struct P: 1편에서 정의
// p: 새로 도착한 가장 오른쪽 점
int up = 0, low = 0;
for (int i = 1; i < (int)hull.size(); i++) {
    if (ccw(p, hull[up],  hull[i]) > 0) up  = i;   // p에서 가장 위로 도는 접점
    if (ccw(p, hull[low], hull[i]) < 0) low = i;   // p에서 가장 아래로 도는 접점
}
// hull에서 up~low 사이(p를 마주 보는 쪽) 점들을 버리고 p를 끼운다
```

가끔은 접선이 평범하게 잡히지 않는다. 새 점 $p$가 지금까지의 모든 점보다 위에 있으면 위쪽 접선이 따로 없이 $p$ 자신이 새로운 최상단이 되어 upper hull 한쪽을 통째로 새로 쓰고, 아래에 있으면 그 반대다. 이런 경계 경우는 접점 탐색에서 자연스럽게 처리된다.

**복잡도.** 점이 $N$개, 점 하나를 붙일 때 접선 찾기가 껍질 전체를 훑어 $O(N)$이다. 곱하면 $O(N^2)$. 처음 한 번의 정렬 $O(N \log N)$은 여기에 묻힌다.

---

## $O(N \log N)$으로 — 균형 BST 아이디어

$O(N^2)$의 낭비는 2편에서 봤던 것과 똑같다. **걸음마다 껍질 전체를 다시 훑는다.** 그런데 접선을 찾는 일은 결국 "이 방향으로 가장 멀리 도는 점 고르기"이고, 앞서 봤듯 껍질의 각 사슬은 단조롭다. 단조로운 곳에서의 극값 찾기라면 이진 탐색이 통할 자리다.

그래서 껍질 점을 **균형 이진 트리(balanced BST)** 에 y좌표 순으로 담는다. 각 노드는 자기 점과 양옆 변을 함께 들고 있다. 새 점 $p$의 위쪽 접점을 찾을 때는, 트리 루트에서 시작해 "접점이 이 노드보다 위에 있나 아래에 있나"를 판정하며 한쪽으로 내려간다. 트리 높이가 $O(\log N)$이니 접점도 $O(\log N)$에 나온다.

![껍질을 균형 트리에 — 껍질 점을 y좌표 순으로 트리에 담으면, 새 점의 접점을 루트에서부터 방향을 정하며 O(log N)에 찾는다.](/images/convex-hull-3/bst-idea.svg)

<div class="callout callout-simple">
<div class="callout-title">방향 판정은 다음 글에서</div>

"접점이 위인가 아래인가"는 후보 점의 좌우 변이 각각 어느 쪽으로 도는지 CCW로 보면 알 수 있다. 직선이 껍질을 **뚫고 들어가는지 나가는지**에 따라 위로 올라갈지 아래로 내려갈지가 갈리는데, 경우가 여럿이라 흐름을 끊는다. 이 케이스 분석은 별도의 **추가 설명** 글에서 따로 정리한다. 여기서는 "단조로운 사슬이라 이진 탐색이 된다"는 뼈대만 가져간다.

</div>

**복잡도.** 점 하나를 삽입하는 데 $O(\log N)$. 접선 안쪽 점들을 지우는 삭제는 얼마나 들까? 언뜻 한 걸음에 많은 점을 지울 수 있어 보이지만, **각 점은 평생 한 번 삽입되고 최대 한 번 삭제된다.** 그러니 전체 삭제 횟수의 합이 $N$을 넘지 못하고, 삭제 하나가 $O(\log N)$이니 삭제에 드는 총비용도 $O(N \log N)$이다. 합쳐서 전체 $O(N \log N)$.

트리를 쓰는 만큼 상수 오버헤드가 있어 실전에서는 Graham Scan보다 느릴 수 있다. 그럼에도 이 방식이 매력적인 이유는, **매 걸음 '지금까지의 부분 껍질'을 손에 들고 있다**는 점이다. 그 부분 껍질이 필요한 문제라면 이만한 도구가 없다. 바로 다음 절이 그런 경우다.

---

## Dynamic Case — 점이 계속 추가된다면

Plane Sweeping은 점을 모두 안다고 가정하고 껍질을 **한 번** 만든다. 그런데 껍질을 완성한 뒤에도 점이 하나씩 새로 도착한다면 어떨까? 지도에 관측소가 늘어나거나, 실시간으로 좌표가 들어오는 상황이다.

매번 처음부터 $O(N \log N)$으로 다시 구하는 건 아깝다. 우리는 이미 껍질을 **BST에 upper / lower 두 사슬로 들고 있으니**, 그걸 고치기만 하면 된다. 새 점 $X$가 도착하면 먼저 물어야 할 것은 하나다. **$X$는 지금 껍질 안인가, 밖인가?**

![Dynamic Case — 새 점 X가 껍질 안이면 그대로 두고, 밖이면 접선 두 개를 찾아 사이를 잘라내고 X를 끼운다.](/images/convex-hull-3/dynamic.svg)

**안쪽 추가 — 껍질은 그대로다.** 판정은 두 사슬로 나눈 덕에 쉽다. $X$의 x좌표 위에 놓인 변을 upper hull에서 이진 탐색으로 찾아 $X$가 그 변보다 아래인지 CCW로 보고, lower hull에서도 같은 것을 본다. upper hull 아래이면서 lower hull 위이면 $X$는 내부이고, 아무것도 할 일이 없다.

**바깥쪽 추가 — Plane Sweeping의 한 걸음과 같다.** $X$에서 껍질로 접선 2개를 긋고, 사이 점들을 버리고 $X$를 끼운다. Plane Sweeping과 다른 점은 새 점이 반드시 오른쪽이라는 보장이 없다는 것뿐이다. 그래서 접선을 위·아래 어느 쪽에서 찾을지가 조금 더 갈리지만, "단조로운 사슬에서 접점을 이진 탐색"이라는 도구는 그대로다.

결국 Dynamic Case는 새 알고리즘이 아니라, Plane Sweeping에서 만든 **"껍질을 트리에 들고 접선으로 갱신한다"는 장치를 그대로 재사용**하는 것이다. 껍질을 굳이 트리에 담아 둔 수고가 여기서 보상받는다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 껍질은 최좌·최우 점을 기준으로 **upper hull / lower hull** 두 단조 사슬로 나뉜다. 이 단조성이 이진 탐색을 가능하게 한다.
- **Plane Sweeping**은 점을 x좌표 순으로 삼키며, 새 점(늘 가장 오른쪽)에서 위·아래 접선을 긋고 사이 점을 버려 껍질을 키운다. 접선을 전부 훑어 찾으면 $O(N^2)$.
- 껍질을 **균형 이진 트리**에 담으면 접선을 이진 탐색으로 $O(\log N)$에 찾는다. 각 점은 한 번 삽입·최대 한 번 삭제되므로 전체 $O(N \log N)$.
- **Dynamic Case**는 완성된 껍질에 점이 추가될 때, 안쪽이면 그대로 두고 바깥쪽이면 접선 2개로 잘라 붙인다. Plane Sweeping의 장치를 그대로 재사용한다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

4편에서는 같은 $O(N \log N)$을 전혀 다른 길로 얻는다. 점들을 절반으로 갈라 각각의 껍질을 재귀로 구한 뒤, 두 껍질을 **공통 접선(common tangent)** 으로 잇는 **Divide and Conquer**다. 정렬에서 본 merge sort의 재귀 구조가 기하에서 어떻게 다시 나타나는지 살펴본다.

계산 기하의 다른 문제인 [가장 가까운 점 쌍](/blog/closest-pair-1)도 함께 보면 좋다.

</div>
`````

- [ ] **Step 2: 커밋**

```bash
git add src/content/posts/convex-hull-3.md
git commit -m "feat(convex-hull): 3편 포스트 본문 추가"
```

---

### Task 3: 빌드 검증

**Files:** (없음 — 검증 전용)

- [ ] **Step 1: 빌드 실행**

Run: `npm run build`
Expected: 에러 없이 완료. content collection 스키마 위반이나 KaTeX 파싱 오류가 없어야 한다. 출력에 `convex-hull-3` 페이지가 생성됨.

- [ ] **Step 2: 빌드 실패 시 대응**

스키마 오류면 프론트매터(`category: algorithm`, `difficulty: 중급`)를 확인한다. KaTeX 오류면 해당 수식의 `$`/`$$` 짝과 백슬래시 이스케이프를 확인한다. 수정 후 Step 1 재실행.

---

### Task 4: 포스트 리뷰

**Files:** (없음)

- [ ] **Step 1: review-post skill 실행**

`/review-post convex-hull-3` 으로 main 대비 변경된 포스트의 내용·문체·SVG를 리뷰한다. 지적 사항이 있으면 반영 후 다시 커밋한다. 특히 L7(논증·복잡도)에서 접선 탐색 pseudocode의 CCW 부호와 삭제 분할상환 $O(N)$ 논증을 점검한다.

---

### Task 5: PR 생성

**Files:** (없음)

- [ ] **Step 1: push 및 PR 생성**

```bash
git push -u origin feat/post-convex-hull-3
gh pr create --title "feat(convex-hull): 볼록 껍질 ③ — Plane Sweeping과 동적 갱신" --body "..."
```

PR 본문은 사용자 지침(2026-06-30)을 따른다: **Why는 충분히 길게**(2편이 예고한 후속, 점진적·동적 관점이라는 새 축, 시리즈 완결성, BST 상세를 예고로 분리한 판단), **How는 방법론 중심**(upper/lower 분해라는 공통 토대, 접선 splice로서의 한 걸음, O(N²)→BST 아이디어, 삭제 분할상환, Dynamic이 도구 재사용이라는 서사, 어려운 케이스 분석의 의도적 분리). 구체 파일 경로는 '참조 코드 위치' 섹션에만.

---

## Self-Review

**1. Spec coverage:**
- 본문 6개 섹션(되짚어보기·목차 → upper/lower 분해 → Plane Sweeping O(N²) → BST O(N log N) → Dynamic Case → 정리/예고) — Task 2 본문에 모두 포함.
- SVG 5장 — Task 1(upper-lower, sweep-tangent, sweep-result, bst-idea, dynamic).
- BST 케이스 분석을 본문 제외·예고로 처리 — Task 2 "방향 판정은 다음 글에서" callout으로 반영, 죽은 링크 없음.
- Dynamic Case를 독립 클라이맥스 섹션으로 — Task 2에 반영.
- 1편 세 가정 유지 명시 — Task 2 도입부.
- 빌드 검증 Task 3, 리뷰 Task 4, PR Task 5.
- 갭 없음.

**2. Placeholder scan:** SVG·본문 전체가 코드 블록으로 포함됨. PR 본문만 방향 서술(작성 시 확정) — 지침 참조로 대체.

**3. Type consistency:** SVG 파일명 5개가 본문 `![...]` 참조와 일치. sweep-tangent와 sweep-result가 공유 점 배치(c0~c6, p) 사용. 슬러그 `convex-hull-3`은 2편 예고(`/blog/convex-hull-3` 예정)와 일치. 프론트매터 키는 1·2편과 동일 구조. 4편은 미발행이므로 2편 관례대로 텍스트 예고만 두고 하이퍼링크는 걸지 않는다(죽은 링크 방지).
