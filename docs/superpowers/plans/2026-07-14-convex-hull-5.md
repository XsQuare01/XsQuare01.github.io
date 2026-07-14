# 볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 볼록 껍질 시리즈 마지막 편 — 껍질을 도구로 써서 평면의 가장 먼 두 점(지름)을 Rotating Calipers로 O(N log N)에 찾는 글을 SVG 3장과 함께 발행한다.

**Architecture:** Astro content collection 포스트 한 편(`src/content/posts/convex-hull-5.md`) + 인라인 SVG 3장(`public/images/convex-hull-5/*.svg`). 발행 후 4편의 "이어지는 글" 예고를 5편으로 하이퍼링크 연결. "테스트"는 `npm run build`(스키마 + KaTeX)와 `/review-post`.

**Tech Stack:** Astro, Markdown + KaTeX, 인라인 SVG(viewBox 680×420, 다크 팔레트).

## Global Constraints

- 브랜치 `feat/post-convex-hull-5`에서만 작업. main 직접 커밋 금지.
- 커밋 메시지에 **co-author 트레일러 넣지 않음**(feedback-no-coauthor-trailer).
- frontmatter: `title`, `date`(2026-07-14T09:00:00), `description`(**160자 이하**), `tags`(배열), `category: algorithm`, `difficulty: 심화`.
- 코드는 의사코드 수준 C++, 컴파일 검증 불필요. 시리즈 정의(`struct P`/`ccw`/외적) 재사용 서술.
- SVG 팔레트: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`, 파랑 `#93c5fd`/`#3b82f6`, 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`. viewBox `0 0 680 420`, width 1020 height 630.
- 공유 껍질 좌표(세 도판 공통): `150,300 120,190 230,110 400,100 540,180 560,300 350,360`. 지름 쌍 = (120,190)-(560,300).
- 미발행 '추가 설명'은 텍스트 예고만(하이퍼링크 금지).

---

### Task 1: SVG 도판 3장

**Files:**
- Create: `public/images/convex-hull-5/hull-vertices.svg`
- Create: `public/images/convex-hull-5/antipodal.svg`
- Create: `public/images/convex-hull-5/calipers.svg`

**Interfaces:**
- Produces: 본문(Task 2)이 참조하는 이미지 경로 3개. 세 도판이 같은 껍질 좌표를 공유한다.

- [ ] **Step 1: `hull-vertices.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="hv-a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#f87171"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">가장 먼 두 점은 껍질 꼭짓점이다</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">안쪽 점은 바깥으로 밀수록 멀어져 가장 먼 쌍의 후보가 못 된다</text>

  <polygon points="150,300 120,190 230,110 400,100 540,180 560,300 350,360" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>

  <!-- 지름(가장 먼 두 점) -->
  <line x1="120" y1="190" x2="560" y2="300" stroke="#fbbf24" stroke-width="2.6"/>
  <text x="330" y="230" text-anchor="middle" fill="#fbbf24" font-size="12" font-weight="700">가장 먼 두 점 (지름)</text>

  <!-- 껍질 꼭짓점 -->
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="150" cy="300" r="5"/><circle cx="230" cy="110" r="5"/><circle cx="400" cy="100" r="5"/>
    <circle cx="540" cy="180" r="5"/><circle cx="350" cy="360" r="5"/>
  </g>
  <!-- 지름 양 끝 강조 -->
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.6">
    <circle cx="120" cy="190" r="6"/><circle cx="560" cy="300" r="6"/>
  </g>

  <!-- 내부 점 X와 밀어내기 -->
  <circle cx="315" cy="285" r="6" fill="#ef4444"/>
  <text x="315" y="307" text-anchor="middle" fill="#f87171" font-size="12" font-weight="700">X</text>
  <line x1="315" y1="285" x2="540" y2="180" stroke="#64748b" stroke-width="1.4" stroke-dasharray="5 4"/>
  <path d="M315,285 Q250,250 205,150" fill="none" stroke="#f87171" stroke-width="2" marker-end="url(#hv-a)" stroke-dasharray="4 3"/>
  <text x="150" y="150" text-anchor="middle" fill="#f87171" font-size="11">밀수록 멀어짐</text>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">그러므로 껍질 위 꼭짓점만 검사하면 된다</text>
</svg>
```

- [ ] **Step 2: `antipodal.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">평행선 회전과 대척점 쌍 (antipodal pair)</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">평행한 두 지지선이 닿는 두 점. 각도를 돌리며 이 쌍만 훑는다</text>

  <!-- 평행한 두 지지선(수평) -->
  <line x1="70" y1="100" x2="610" y2="100" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>
  <line x1="70" y1="360" x2="610" y2="360" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>
  <text x="620" y="104" fill="#93c5fd" font-size="10">지지선</text>
  <text x="620" y="364" fill="#93c5fd" font-size="10">지지선</text>

  <polygon points="150,300 120,190 230,110 400,100 540,180 560,300 350,360" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>

  <!-- 대척점 쌍(위·아래 접점) + 지름 후보 선분 -->
  <line x1="400" y1="100" x2="350" y2="360" stroke="#fbbf24" stroke-width="2.4" stroke-dasharray="6 4"/>
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.6">
    <circle cx="400" cy="100" r="6"/><circle cx="350" cy="360" r="6"/>
  </g>
  <text x="300" y="235" text-anchor="end" fill="#fbbf24" font-size="12" font-weight="700">대척점 쌍</text>
  <text x="300" y="252" text-anchor="end" fill="#94a3b8" font-size="11">(이 각도의 지름 후보)</text>

  <!-- 나머지 꼭짓점 -->
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="150" cy="300" r="5"/><circle cx="120" cy="190" r="5"/>
    <circle cx="540" cy="180" r="5"/><circle cx="560" cy="300" r="5"/>
  </g>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">가장 먼 쌍은 어떤 각도에서 반드시 대척점 쌍으로 나타난다</text>
</svg>
```

- [ ] **Step 3: `calipers.svg` 작성**

```xml
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="cl-a" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Rotating Calipers 한 걸음</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">더 작은 각도로 벌어진 쪽 포인터를 다음 꼭짓점으로 전진</text>

  <!-- 기울인 평행 지지선 (P4·P0 접점) -->
  <line x1="470" y1="90" x2="650" y2="330" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>
  <line x1="70" y1="180" x2="250" y2="420" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>

  <polygon points="150,300 120,190 230,110 400,100 540,180 560,300 350,360" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>

  <!-- 두 포인터 i, j (대척점) -->
  <circle cx="540" cy="180" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.6"/>
  <circle cx="150" cy="300" r="7" fill="#0f1117" stroke="#34d399" stroke-width="2.6"/>
  <text x="556" y="176" fill="#6ee7b7" font-size="12" font-weight="700">포인터 i</text>
  <text x="150" y="322" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">포인터 j</text>

  <!-- 각 포인터의 다음 꼭짓점으로의 전진 후보 -->
  <path d="M540,180 Q560,245 555,292" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="4 3"/>
  <path d="M150,300 Q128,250 123,198" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#cl-a)" stroke-dasharray="4 3"/>
  <text x="95" y="235" fill="#6ee7b7" font-size="11" font-weight="600">전진</text>

  <!-- 나머지 꼭짓점 -->
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2">
    <circle cx="120" cy="190" r="5"/><circle cx="230" cy="110" r="5"/><circle cx="400" cy="100" r="5"/>
    <circle cx="560" cy="300" r="5"/><circle cx="350" cy="360" r="5"/>
  </g>

  <text x="340" y="404" text-anchor="middle" fill="#94a3b8" font-size="12">두 포인터가 한 바퀴 도는 동안 만난 대척점 쌍 거리만 비교 — O(N)</text>
</svg>
```

- [ ] **Step 4: 커밋**

```bash
git add public/images/convex-hull-5/
git commit -m "feat(convex-hull): 5편 SVG 도판 3장"
```

---

### Task 2: 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-5.md`

**Interfaces:**
- Consumes: Task 1의 SVG 경로 3개.
- Produces: 라우트 `/blog/convex-hull-5`. Task 3이 4편에서 이 라우트로 링크한다.

- [ ] **Step 1: 본문 파일 작성 (전체 인라인)**

````markdown
---
title: "볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers"
date: 2026-07-14T09:00:00
description: "볼록 껍질을 도구로 써서 평면의 가장 먼 두 점(지름)을 찾는다. 가장 먼 쌍은 껍질 꼭짓점이며, 평행선을 돌리며 대척점 쌍만 훑는 Rotating Calipers로 모든 쌍 O(N²) 대신 O(N)에 얻는다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Rotating Calipers"]
category: algorithm
difficulty: 심화
---

> [1편](/blog/convex-hull-1)부터 [4편](/blog/convex-hull-4)까지, 우리는 흩어진 점들의 볼록 껍질을 **구하는** 네 가지 길을 걸었다. Package Wrapping, Graham Scan, Plane Sweeping, 그리고 분할 정복. 마지막 편은 방향을 바꾼다. 껍질을 **도구로 쓴다.** 평면에서 가장 멀리 떨어진 두 점, 곧 점들의 **지름(diameter)** 을 찾는 문제인데, 모든 쌍을 재보는 $O(N^2)$ 대신 껍질을 구한 뒤 $O(N)$에 훑는 **Rotating Calipers**로 전체 $O(N \log N)$에 푼다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- 1차원에서 2차원으로 — 왜 어려워지나
- 가장 먼 두 점은 **껍질 꼭짓점**이다
- 평행선 회전과 **대척점 쌍(antipodal pair)**
- **Rotating Calipers**로 대척점만 $O(N)$에 훑기

</div>

이번에도 껍질은 1~4편에서처럼 일반 위치(한 직선 위에 점이 3개 이상 없음)를 가정하고, 이미 반시계 순서로 구해 두었다고 하자.

---

## 1차원에서 2차원으로

가장 먼 두 점을 찾는 문제는 1차원에선 시시하다. 수직선 위의 점들 중 가장 먼 쌍은 **최솟값과 최댓값**이니, 한 번 훑어 $O(N)$에 끝난다.

평면은 다르다. 어느 두 점이 가장 먼지 미리 알 수 없어, 소박하게는 **모든 쌍의 거리를 재야** 한다. 점이 $N$개면 쌍이 약 $N^2/2$개라 $O(N^2)$. 점이 많아지면 버겁다. 더 좋은 길이 있을까? 볼록 껍질이 열쇠다.

---

## 가장 먼 두 점은 껍질 꼭짓점이다

첫 관찰은 이것이다. **가장 먼 두 점은 반드시 볼록 껍질의 꼭짓점이다.**

어떤 점 $p$가 껍질 내부에 있다고 하자. 다른 점 $q$에서 $p$를 바라보면, $q$에서 멀어지는 방향으로 $p$를 밀어낼 여지가 항상 있고, 껍질 경계에 닿을 때까지 밀수록 $q$와의 거리는 커진다. 즉 내부 점은 결코 "가장 먼" 쌍의 한쪽이 될 수 없다. 가장 먼 쌍의 양 끝은 둘 다 바깥, 곧 껍질 위 꼭짓점이다.

![가장 먼 두 점은 껍질 꼭짓점 — 내부 점은 바깥으로 밀수록 멀어지므로 후보가 못 된다.](/images/convex-hull-5/hull-vertices.svg)

그래서 전략이 선다. 먼저 볼록 껍질을 구해(1~4편의 어느 방법이든 $O(N \log N)$) 후보를 껍질 꼭짓점으로 좁힌다. 남은 일은 **껍질 꼭짓점들 중 가장 먼 쌍**을 찾는 것이다.

---

## 평행선 회전과 대척점 쌍

껍질 꼭짓점만 봐도 그 쌍을 다 재면 다시 $O(H^2)$($H$는 꼭짓점 수)다. 여기서 기하적 그림 하나가 볼 쌍의 수를 확 줄인다.

볼록 다각형을 **평행한 두 직선**으로 양쪽에서 떠받친다고 하자(자를 양옆에 대는 느낌). 두 직선은 각각 다각형에 한 점(또는 한 변)에서 닿는다. 이렇게 마주 보며 닿는 점 쌍을 **대척점 쌍(antipodal pair)** 이라 부른다.

![대척점 쌍 — 평행한 두 지지선이 껍질에 닿는 두 점. 그 사이 선분이 지름 후보다.](/images/convex-hull-5/antipodal.svg)

이제 평행선의 **각도를 0°에서 180°까지 돌린다.** 각도가 바뀔 때마다 닿는 대척점 쌍도 바뀐다. 핵심은 이것이다. **가장 먼 두 점은 반드시 어떤 각도에서 대척점 쌍으로 나타난다.** 가장 먼 쌍 $a$, $b$를 잇는 선분에 수직인 방향으로 평행선을 대면 두 직선이 정확히 $a$와 $b$에 닿기 때문이다. 그러니 **모든 대척점 쌍만 훑어 그중 최대 거리를 고르면** 그게 지름이다. 대척점이 아닌 쌍은 볼 필요조차 없다.

---

## Rotating Calipers — $O(N)$

남은 문제는 "평행선을 연속으로 돌린다"를 어떻게 이산적인 알고리즘으로 옮기느냐다. 다행히 대척점 쌍은 각도가 돌면서 껍질 위를 **한 방향으로만** 이동한다. 그래서 직선을 직접 돌리는 대신, 껍질 위에 **두 포인터**를 두고 그것들을 회전시키면 된다. 물체를 양쪽에서 재는 자(caliper) 두 짝을 벌려 돌리는 그림이라 **Rotating Calipers**다.

한 걸음은 이렇다. 두 포인터가 각각 위·아래 지지선의 접점이라 하자. 각 접점에서 다음 변으로 넘어가려면 지지선을 얼마나 돌려야 하는지 비교해, **더 작은 각도로 벌어진(먼저 닿는) 쪽 포인터를 다음 꼭짓점으로 전진**시킨다. 전진할 때마다 마주친 대척점 쌍의 거리를 재 최댓값을 갱신한다.

![Rotating Calipers 한 걸음 — 두 포인터 중 더 작은 각도로 벌어진 쪽을 다음 꼭짓점으로 전진시킨다.](/images/convex-hull-5/calipers.svg)

각도 비교는 삼각함수 없이 **외적(cross product)** 으로 한다. 외적의 크기는 한 점이 어떤 변(직선)에서 얼마나 떨어져 있는지에 비례하므로, 다음 꼭짓점이 현재 변에서 더 멀어지는 동안 포인터를 밀면 그 변의 대척점에 닿는다(1편 CCW와 같은 도구).

```cpp
// hull: 볼록 껍질 꼭짓점(반시계 순서) 배열, H개. struct P·cross는 1편 정의.
// cross(O, A, B): 벡터 OA × OB (부호 있는 넓이의 2배)
// dist2(A, B): 제곱거리 — 부동소수 없이 비교하려고 제곱으로 둔다
long long best = 0;
int j = 1;
for (int i = 0; i < H; i++) {
    int ni = (i + 1) % H;                 // 변 i→ni
    // 변 i→ni에서 가장 먼 꼭짓점(대척점)까지 j를 전진
    while (cross(hull[i], hull[ni], hull[(j + 1) % H])
             > cross(hull[i], hull[ni], hull[j])) {
        j = (j + 1) % H;
    }
    // (i, j)와 (ni, j)가 대척점 쌍 후보
    best = max(best, dist2(hull[i], hull[j]));
    best = max(best, dist2(hull[ni], hull[j]));
}
// best = 지름의 제곱. 실제 지름은 sqrt(best).
```

<div class="callout callout-simple">
<div class="callout-title">엣지 케이스는 추가 설명에서</div>

평행한 두 **변**이 동시에 닿을 때(대척점 쌍이 여럿), 포인터가 언제 둘 다 움직여야 하는지, 대척점 쌍을 빠짐없이 세는 정확한 조건 등은 경우가 갈려 흐름을 끊는다. 이 상세는 곧 이어질 **추가 설명** 글에서 따로 정리한다. 여기서는 "두 포인터를 더 작은 각도 쪽으로 전진시켜 한 바퀴 돈다"는 뼈대만 가져간다.

</div>

---

## 복잡도

두 포인터는 각각 껍질을 **한 바퀴만** 돈다. $i$는 for 문으로 $H$번, $j$는 while 문에서 전진하되 뒤로는 가지 않아 전체를 통틀어 $H$번을 넘지 못한다. 그러니 대척점 순회는 $O(H)$이고, 껍질 크기가 최대 $N$이니 $O(N)$이다.

여기에 껍질을 구하는 $O(N \log N)$을 더하면 전체 $O(N \log N)$. 모든 쌍을 재는 $O(N^2)$과 비교하면, 껍질을 먼저 구하느라 들인 비용이 톡톡히 회수된다. 껍질은 가장 먼 점뿐 아니라 폭(width)·최소 외접 사각형 같은 여러 극값 문제의 공통 발판이 된다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 평면에서 **가장 먼 두 점(지름)** 은 반드시 볼록 껍질의 **꼭짓점**이다. 내부 점은 밖으로 밀수록 멀어지기 때문이다.
- 평행한 두 지지선을 돌리며 닿는 **대척점 쌍**만 보면 된다. 가장 먼 쌍은 어떤 각도에서 반드시 대척점 쌍으로 나타난다.
- **Rotating Calipers**는 직선 대신 껍질 위 두 포인터를 회전시켜, 더 작은 각도로 벌어진 쪽을 전진하며 대척점 쌍을 $O(N)$에 순회한다. 각도 비교는 외적으로 한다.
- 껍질 $O(N \log N)$ + 순회 $O(N)$ = 전체 $O(N \log N)$. 모든 쌍 $O(N^2)$보다 빠르다.

</div>

<div class="callout">
<div class="callout-title">시리즈를 마치며</div>

다섯 편에 걸쳐 볼록 껍질을 **구하는 네 가지 길**(Package Wrapping · Graham Scan · Plane Sweeping · 분할 정복)과, 그렇게 구한 껍질을 **도구로 쓰는 법**(가장 먼 두 점)을 살펴봤다. 껍질은 그 자체가 답인 동시에, 여러 기하 문제를 푸는 발판이다.

Rotating Calipers의 엣지 케이스(평행 변·대척점 쌍의 정확한 열거)는 곧 이어질 **추가 설명** 글에서 마저 다룬다. 계산 기하의 이웃 문제인 [가장 가까운 점 쌍](/blog/closest-pair-1)도 함께 보면 좋다.

</div>
````

- [ ] **Step 2: 빌드 검증**

Run: `npm run build`
Expected: 성공, "N page(s) built". KaTeX/frontmatter 오류 없음. `[SEO]` description 경고 없음(160자 이하).

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-5.md
git commit -m "feat(convex-hull): 5편 본문 — 가장 먼 두 점과 Rotating Calipers"
```

---

### Task 3: 4편 forward link 연결

**Files:**
- Modify: `src/content/posts/convex-hull-4.md` (이어지는 글의 "5편" 텍스트)

**Interfaces:**
- Consumes: Task 2가 만든 라우트 `/blog/convex-hull-5`.

- [ ] **Step 1: 4편의 "5편" 예고를 하이퍼링크로**

`src/content/posts/convex-hull-4.md`의 "이어지는 글" 문단에서:

찾기:
```
5편에서는 껍질을 도구로 쓰는 문제로 넘어간다.
```
바꾸기:
```
[5편](/blog/convex-hull-5)에서는 껍질을 도구로 쓰는 문제로 넘어간다.
```

- [ ] **Step 2: 빌드 재검증**

Run: `npm run build`
Expected: 성공.

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-4.md
git commit -m "docs(convex-hull): 4편에서 5편으로 링크 연결"
```

---

### Task 4: 리뷰 (플랜 외 후속)

플랜 실행이 끝나면 `/review-post convex-hull-5`로 결정적 검사 + LLM 비평(L1~L7, 노션 원본 대조 포함)을 돌리고, 지적을 반영한 뒤 재빌드한다. 리포트는 `docs/reviews/2026-07-14-convex-hull-5.md`. 반영 완료 후 PR 생성. 이후 별건으로 'Rotating Calipers 엣지 케이스' 추가 설명 페이지 작업.

## Self-Review

**1. Spec coverage:** 스펙 본문 9개 구성(도입·목차·1차원워밍업·껍질꼭짓점·대척점·Rotating Calipers·복잡도·핵심정리·마무리)은 Task 2 본문에 모두 포함. SVG 3장은 Task 1. 4편 링크 연결은 Task 3. 빌드/리뷰는 Task 2·4. description 160자 이하 제약은 Task 2 Step 2에서 검증. 누락 없음.

**2. Placeholder scan:** SVG·본문·수정 문구 모두 실제 내용 인라인. '추가 설명'은 스펙대로 텍스트 예고(하이퍼링크 없음). "TBD/적절히" 없음.

**3. Type consistency:** 세 SVG가 동일 껍질 좌표(`150,300 …`) 사용. 본문 이미지 경로 3개가 Task 1 생성 파일과 일치. 의사코드 헬퍼(`cross`, `dist2`)는 본문 주석으로 의미 정의. 4편 치환 문구는 현재 파일의 "이어지는 글"과 일치.
