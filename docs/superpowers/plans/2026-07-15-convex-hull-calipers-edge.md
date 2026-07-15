# 추가 설명 — 평행한 변이 만드는 동률과 대척점 쌍 열거 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 5편이 미뤄둔 Rotating Calipers 동률(평행 변) 처리와 대척점 쌍 완전 열거를, "지름 값은 뼈대로 이미 맞다"는 정직한 논지 전환과 함께 SVG 2장으로 정리한 '추가 설명' 페이지를 발행한다.

**Architecture:** Astro content collection 포스트 한 편(`src/content/posts/convex-hull-calipers-edge.md`) + 인라인 SVG 2장(`public/images/convex-hull-calipers-edge/*.svg`). 발행 후 5편의 "시리즈를 마치며" 텍스트 예고를 이 글로 하이퍼링크 연결. "테스트"는 `npm run build`(스키마 + KaTeX)와 `/review-post`.

**Tech Stack:** Astro, Markdown + KaTeX, 인라인 SVG(다크 팔레트).

## Global Constraints

- 브랜치 `feat/post-convex-hull-calipers-edge`에서만 작업. main 직접 커밋 금지.
- 커밋 메시지에 **co-author 트레일러 넣지 않음**(feedback-no-coauthor-trailer).
- frontmatter: `title`, `date`(2026-07-15T09:00:00), `description`(**160자 이하**), `tags`(배열), `category: algorithm`, `difficulty: 고급`.
- 코드는 의사코드 수준 C++, 컴파일 검증 불필요. 시리즈 정의(`cross`) 재사용 서술.
- SVG 팔레트: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`, 파랑 `#93c5fd`/`#3b82f6`, 채움 `#1e293b40`/stroke `#334155`, 주황 `#fbbf24`, 빨강 `#f87171`.
- **논지 고정(과대주장 금지):** 5편 뼈대의 **지름 값은 평행 변이 있어도 옳다**. 이 글은 대척점 쌍을 **빠짐없이·중복 없이 열거**하는 별개 문제를 다룬다. 이 전환이 5편 L7을 닫는 핵심.
- 발행 전까지 5편 링크 연결(Task 3)은 하지 않는다(라우트 존재 후).

---

### Task 1: SVG 도판 2장

**Files:**
- Create: `public/images/convex-hull-calipers-edge/contact-types.svg`
- Create: `public/images/convex-hull-calipers-edge/parallel-pairs.svg`

**Interfaces:**
- Produces: 본문(Task 2)이 참조하는 이미지 경로 2개.

- [ ] **Step 1: `contact-types.svg` — 접촉의 세 유형(3분할)**

세 패널: 꼭짓점–꼭짓점(쌍 1개) / 꼭짓점–변(쌍 2개) / 변–변(쌍 4개). 각 패널에 수평 평행 지지선 2개(y=90, y=250)와 볼록 도형, 접점(주황)·대척 선분·쌍 개수 표기.

```xml
<svg viewBox="0 0 720 340" width="1080" height="510" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="720" height="340" rx="10" fill="#0f1117"/>

  <text x="360" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">접촉의 세 유형 — 지지선이 변에 밀착하면 대척점 쌍이 늘어난다</text>
  <text x="360" y="50" text-anchor="middle" fill="#64748b" font-size="11">평행한 두 지지선(파랑 점선)이 껍질에 닿는 방식</text>

  <!-- ===== 패널 A: 꼭짓점–꼭짓점 (cx=120) ===== -->
  <line x1="25" y1="90" x2="215" y2="90" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <line x1="25" y1="250" x2="215" y2="250" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <polygon points="120,90 185,150 170,215 120,250 70,215 55,150" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>
  <line x1="120" y1="90" x2="120" y2="250" stroke="#fbbf24" stroke-width="2.2"/>
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2"><circle cx="185" cy="150" r="4"/><circle cx="170" cy="215" r="4"/><circle cx="70" cy="215" r="4"/><circle cx="55" cy="150" r="4"/></g>
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.6"><circle cx="120" cy="90" r="6"/><circle cx="120" cy="250" r="6"/></g>
  <text x="120" y="290" text-anchor="middle" fill="#e2e8f0" font-size="12" font-weight="600">꼭짓점–꼭짓점</text>
  <text x="120" y="310" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">대척점 쌍 1개</text>

  <!-- ===== 패널 B: 꼭짓점–변 (cx=360) ===== -->
  <line x1="265" y1="90" x2="455" y2="90" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <line x1="265" y1="250" x2="455" y2="250" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <polygon points="325,90 395,90 420,170 360,250 300,170" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>
  <line x1="325" y1="90" x2="435" y2="90" stroke="#93c5fd" stroke-width="3"/>
  <line x1="360" y1="250" x2="325" y2="90" stroke="#fbbf24" stroke-width="2.2"/>
  <line x1="360" y1="250" x2="395" y2="90" stroke="#fbbf24" stroke-width="2.2"/>
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2"><circle cx="420" cy="170" r="4"/><circle cx="300" cy="170" r="4"/></g>
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.6"><circle cx="325" cy="90" r="6"/><circle cx="395" cy="90" r="6"/><circle cx="360" cy="250" r="6"/></g>
  <text x="360" y="290" text-anchor="middle" fill="#e2e8f0" font-size="12" font-weight="600">꼭짓점–변</text>
  <text x="360" y="310" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">대척점 쌍 2개</text>

  <!-- ===== 패널 C: 변–변 (cx=600) ===== -->
  <line x1="505" y1="90" x2="695" y2="90" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <line x1="505" y1="250" x2="695" y2="250" stroke="#93c5fd" stroke-width="1.4" stroke-dasharray="7 5"/>
  <polygon points="565,90 635,90 645,250 555,250" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>
  <line x1="560" y1="90" x2="640" y2="90" stroke="#93c5fd" stroke-width="3"/>
  <line x1="550" y1="250" x2="650" y2="250" stroke="#93c5fd" stroke-width="3"/>
  <g stroke="#fbbf24" stroke-width="1.8">
    <line x1="565" y1="90" x2="555" y2="250"/><line x1="635" y1="90" x2="645" y2="250"/>
    <line x1="565" y1="90" x2="645" y2="250"/><line x1="635" y1="90" x2="555" y2="250"/>
  </g>
  <g fill="#0f1117" stroke="#fbbf24" stroke-width="2.6"><circle cx="565" cy="90" r="6"/><circle cx="635" cy="90" r="6"/><circle cx="645" cy="250" r="6"/><circle cx="555" cy="250" r="6"/></g>
  <text x="600" y="290" text-anchor="middle" fill="#e2e8f0" font-size="12" font-weight="600">변–변</text>
  <text x="600" y="310" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">대척점 쌍 4개 (2×2)</text>
</svg>
```

- [ ] **Step 2: `parallel-pairs.svg` — 변–변 동률의 대척점 열거**

평행한 두 변(아래 i→ni, 위 j→j+1) 사이 네 조합을 색으로 구분: 뼈대 기록(초록 실선) / 동률 분기 추가(주황 점선) / 다음 변에서(회색 점선).

```xml
<svg viewBox="0 0 680 440" width="1020" height="660" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="440" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">변–변 동률에서 대척점 쌍 열거</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">평행한 두 변 사이 네 조합이 모두 대척점 — 뼈대는 일부만 기록한다</text>

  <!-- 평행 지지선(두 변의 연장) -->
  <line x1="60" y1="110" x2="620" y2="110" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="6 6" opacity="0.5"/>
  <line x1="60" y1="340" x2="620" y2="340" stroke="#93c5fd" stroke-width="1.2" stroke-dasharray="6 6" opacity="0.5"/>

  <!-- 껍질 조각(두 평행 변을 가진 사각형) -->
  <polygon points="160,340 520,340 560,110 200,110" fill="#1e293b40" stroke="#334155" stroke-width="1.6"/>

  <!-- 네 조합 -->
  <line x1="520" y1="340" x2="200" y2="110" stroke="#64748b" stroke-width="1.8" stroke-dasharray="5 4"/>
  <line x1="160" y1="340" x2="200" y2="110" stroke="#fbbf24" stroke-width="2.4" stroke-dasharray="6 4"/>
  <line x1="160" y1="340" x2="560" y2="110" stroke="#34d399" stroke-width="2.6"/>
  <line x1="520" y1="340" x2="560" y2="110" stroke="#34d399" stroke-width="2.6"/>

  <!-- 꼭짓점 -->
  <g fill="#0f1117" stroke="#3b82f6" stroke-width="2.4">
    <circle cx="160" cy="340" r="6"/><circle cx="520" cy="340" r="6"/>
    <circle cx="560" cy="110" r="6"/><circle cx="200" cy="110" r="6"/>
  </g>
  <text x="150" y="362" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">i</text>
  <text x="524" y="362" fill="#93c5fd" font-size="13" font-weight="700">ni</text>
  <text x="566" y="104" fill="#93c5fd" font-size="13" font-weight="700">j</text>
  <text x="196" y="102" text-anchor="end" fill="#93c5fd" font-size="13" font-weight="700">j+1</text>

  <!-- 범례 -->
  <g font-size="12">
    <line x1="200" y1="392" x2="240" y2="392" stroke="#34d399" stroke-width="2.6"/>
    <text x="248" y="396" fill="#6ee7b7">뼈대가 기록 — (i, j), (ni, j)</text>
    <line x1="200" y1="410" x2="240" y2="410" stroke="#fbbf24" stroke-width="2.4" stroke-dasharray="6 4"/>
    <text x="248" y="414" fill="#fbbf24">동률 분기로 추가 — (i, j+1)</text>
    <line x1="200" y1="428" x2="240" y2="428" stroke="#64748b" stroke-width="1.8" stroke-dasharray="5 4"/>
    <text x="248" y="432" fill="#94a3b8">다음 변에서 나옴 — (ni, j+1)</text>
  </g>
</svg>
```

- [ ] **Step 3: 커밋**

```bash
git add public/images/convex-hull-calipers-edge/
git commit -m "feat(convex-hull): 추가 설명 SVG 2장 — 접촉 유형·평행 변 대척점 열거"
```

---

### Task 2: 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-calipers-edge.md`

**Interfaces:**
- Consumes: Task 1의 SVG 경로 2개.
- Produces: 라우트 `/blog/convex-hull-calipers-edge`. Task 3이 5편에서 이 라우트로 링크한다.

- [ ] **Step 1: 본문 파일 작성 (전체 인라인)**

````markdown
---
title: "추가 설명 — 평행한 변이 만드는 동률과 대척점 쌍 열거"
date: 2026-07-15T09:00:00
description: "볼록 껍질 ⑤의 Rotating Calipers 뼈대는 평행한 변이 있어도 지름 값이 옳다. 이 글은 대척점 쌍을 빠짐없이 열거하는 별개 문제와, 평행한 변이 만드는 동률·교차 쌍 처리를 다룬다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Rotating Calipers", "추가 설명"]
category: algorithm
difficulty: 고급
---

> [볼록 껍질 ⑤](/blog/convex-hull-5)에서 Rotating Calipers의 뼈대를 세우며, 그 의사코드는 "일반 위치(동률 없는 경우)를 가정한 기본 뼈대"라고 못박고 평행한 변이 겹칠 때의 **완전한 열거**를 여기로 미뤘다. 그 미뤄둔 조각을 마저 맞춘다. 다만 먼저 짚을 게 있다. 뼈대가 내놓는 **지름 값 자체는 평행한 변이 있어도 옳다.** 이 글이 채우는 건 지름 값이 아니라, 대척점 쌍을 하나의 목록으로 **빠짐없이·중복 없이 열거**하는 별개의 문제다.

<div class="callout">
<div class="callout-title">이 글에서 다루는 내용</div>

- 동률은 언제 생기나 — 변이 변과 **평행**할 때
- 접촉의 세 유형: 꼭짓점–꼭짓점 · 꼭짓점–변 · 변–변
- 지름 값은 왜 뼈대로 **이미 맞는가** — '두 끝점 검사'의 정체
- 빠짐없는 **열거**는 왜 다른 문제인가 — 놓치는 교차 쌍, `>` vs `>=`
- 포인터를 둘 다 전진시키는 경우와 중복 없는 종료

</div>

---

## 동률은 어디서 오는가

5편에서 평행한 두 지지선을 돌리며 대척점 쌍을 훑었다. 지지선이 껍질에 닿는 방식은 보통 **한 점**이다. 하지만 지지선의 방향이 껍질의 어떤 **변과 나란해지는** 순간, 지지선은 그 변을 한 점이 아니라 **통째로** 떠받친다. 변의 두 끝 꼭짓점에 동시에 닿는 것이다.

이때 대척점 쌍은 하나로 딱 떨어지지 않는다. 한쪽 지지선이 변에 밀착하면 반대쪽 점 하나는 그 변의 **두 끝점 모두와** 대척을 이룬다. 두 지지선이 **동시에** 각자의 변에 밀착하면(껍질에 평행한 두 변이 있다는 뜻) 한 각도에서 대척점 쌍이 **여럿** 생긴다. 이 겹침이 5편이 말한 '동률'의 정체다. 동률은 우연이 아니라 **평행한 변**에서 온다. 정사각형이나 정육각형처럼 평행한 변을 가진 껍질이라면 반드시 마주친다.

---

## 접촉의 세 유형

지지선이 껍질에 닿는 방식을 세 가지로 나누면 동률이 선명해진다.

- **꼭짓점–꼭짓점.** 두 지지선이 각각 **한 꼭짓점**에 닿는 일반적인 경우. 그 각도의 대척점 쌍은 하나뿐이다.
- **꼭짓점–변.** 한 지지선은 한 꼭짓점에, 다른 지지선은 한 변에 밀착한다. 그 꼭짓점은 변의 두 끝점과 각각 대척을 이뤄 쌍이 **둘**이다.
- **변–변.** 두 지지선 모두 변에 밀착한다(평행한 두 변). 한쪽 변의 두 끝점과 다른 쪽 변의 두 끝점이 서로 모두 대척이라 조합이 **2×2**다.

![접촉의 세 유형 — 지지선이 변에 밀착할수록 한 각도의 대척점 쌍이 1개→2개→4개로 늘어난다.](/images/convex-hull-calipers-edge/contact-types.svg)

동률을 다룬다는 건 결국 뒤 두 경우, 특히 **변–변**에서 이 여러 쌍을 어떻게 처리하느냐의 문제다.

---

## 지름 값은 왜 뼈대로 이미 맞는가

결론부터 말하면, 5편 뼈대는 평행한 변이 있어도 **지름을 정확히** 내놓는다. 변마다 대척점을 하나만 보는 듯해도, 실제로는 **두 끝점을 모두 재기** 때문이다.

```cpp
// 5편 뼈대의 두 줄 — 변 i→ni의 가장 먼 꼭짓점 j에 대해
best = max(best, dist2(hull[i],  hull[j]));   // (i, j)
best = max(best, dist2(hull[ni], hull[j]));   // (ni, j)
```

변 $i \to ni$에서 가장 먼 꼭짓점 $j$를 찾은 뒤, 뼈대는 $(i, j)$뿐 아니라 $(ni, j)$의 거리도 잰다. 왜 두 끝점을 다 재야 할까? 지름을 이루는 쌍 $(u, v)$를 떠올려 보자. 이 쌍을 떠받치는 평행 지지선을 조금씩 돌리면, 둘 중 하나는 **반드시 어떤 변에 밀착하는 순간**을 지난다(평행선을 계속 돌리는 한 언젠가 한 변과 나란해진다). 그 변을 $i \to ni$라 하면, 반대쪽 점 $v$는 그 변에서 가장 먼 꼭짓점 $j$이고, $u$는 그 변의 두 끝점 중 하나 — 곧 $i$ 아니면 $ni$다. 뼈대는 $(i, j)$와 $(ni, j)$를 **둘 다** 재므로, $u$가 어느 끝이든 $(u, v)$를 반드시 검사한다.

변–변 동률에서 생기는 '교차' 쌍(한 변의 끝점과 맞은편 변의 **반대쪽** 끝점)도 마찬가지다. 지금 변에서 놓치더라도 **맞은편 변을 처리할 때** 그 쌍이 다시 후보로 올라온다. 그래서 최댓값만 필요한 지름 계산은, 평행한 변이 있어도 뼈대만으로 안전하다. 직사각형으로 눈으로 확인해도 좋다. 네 변을 차례로 처리하면 두 대각선이 모두 후보로 잡혀, 더 긴 쪽이 지름으로 남는다.

---

## 빠짐없는 열거는 왜 다른 문제인가

그렇다면 5편은 왜 뼈대를 "일반 위치 기본 뼈대"로 좁혔을까? 지름 **값**이 아니라 대척점 쌍을 **목록으로** 뽑는 문제가 남기 때문이다. 폭(width), 최소 외접 사각형, 두 볼록 다각형 사이 거리 같은 문제는 지름 하나가 아니라 **대척점 쌍 하나하나**를 손에 쥐어야 풀린다. 여기서 평행한 변의 동률이 정확히 문제를 만든다.

변–변 동률을 다시 보자. 뼈대가 변 $i \to ni$를 처리할 때 포인터 $j$는 맞은편 변의 한 끝(그림의 $j$)에 멈춘다. strict `>` 비교라 **다음 꼭짓점 $j{+}1$로는 넘어가지 않는다** — 두 외적(넓이)이 같아 `>`가 거짓이기 때문이다. 그래서 뼈대가 이 변에서 기록하는 대척점 쌍은 $(i, j)$와 $(ni, j)$뿐이고, 맞은편 변의 다른 끝 $j{+}1$과 이루는 **교차 쌍은 빠진다.**

![변–변 동률의 대척점 열거 — 뼈대는 (i,j)·(ni,j)를 기록하고, 교차 쌍 (i,j+1)은 동률 분기로 채워야 한다.](/images/convex-hull-calipers-edge/parallel-pairs.svg)

- $(i, j)$, $(ni, j)$ — 뼈대가 이 변에서 기록한다.
- $(i, j{+}1)$ — 이 각도에도 성립하는 대척점인데 뼈대가 건너뛴다. 목록에 넣으려면 **명시로 추가**해야 한다.
- $(ni, j{+}1)$ — 다음 변 $ni \to \cdots$를 처리할 때 나온다.

지름만 볼 때는 $(i, j{+}1)$을 놓쳐도 그 거리가 다른 변에서 다시 잡혔지만, **모든 쌍을 하나씩** 필요로 하는 문제에서는 이 하나가 통째로 사라진다. 그게 5편이 미룬 '완전한 열거'의 공백이다.

<div class="callout callout-simple">
<div class="callout-title">그럼 <code>&gt;</code>를 <code>&gt;=</code>로 바꾸면?</div>

동률에서 $j$가 못 넘어가는 게 문제라면 비교를 `>=`로 풀어 $j$를 전진시키면 될 것 같다. 하지만 그러면 동률이 아닌 자리에서도 $j$가 한 칸 더 밀려, 어느 변의 대척점인지 경계가 흐려지고 $j$가 한 바퀴 도는 횟수가 어긋난다. 대척점을 중복해 세거나, 심하면 종료가 꼬인다. 그래서 표준 해법은 `>`를 그대로 두어 "변마다 대척점 하나"라는 단조성을 지키고, **넓이가 정확히 같은 동률만 따로 분기**해 빠진 교차 쌍을 채운다.

</div>

---

## 코드

동률 분기를 뼈대에 얹으면 이렇다. 5편 뼈대에서 달라진 곳은 `report`와 그 아래 `if` 하나뿐이다.

```cpp
// hull: 반시계 볼록 껍질, H개. cross는 1편 정의.
// report(a, b): 대척점 쌍 (hull[a], hull[b])을 목록에 추가
int j = 1;
for (int i = 0; i < H; i++) {
    int ni = (i + 1) % H;
    // 변 i→ni에서 가장 먼 꼭짓점까지 j를 전진 (strict '>' 유지)
    while (cross(hull[i], hull[ni], hull[(j + 1) % H])
             > cross(hull[i], hull[ni], hull[j])) {
        j = (j + 1) % H;
    }
    report(i, j);                              // (i, j)는 대척점 쌍

    // 변 i→ni 가 변 j→(j+1) 과 평행하면(넓이 동률) 이 각도에 쌍이 여럿
    if (cross(hull[i], hull[ni], hull[(j + 1) % H])
          == cross(hull[i], hull[ni], hull[j])) {
        report(i, (j + 1) % H);                // 교차 대척점 쌍 하나 더
    }
}
```

- **지름만 필요하면 이 `if` 분기는 없어도 된다.** 놓친 교차 쌍은 맞은편 변에서 다시 후보로 오르기 때문이다. 분기가 필요한 건 대척점 쌍을 **목록으로** 뽑을 때뿐이다.
- 각 변에서 $(ni, j)$를 따로 `report`하지 않은 이유: 그 쌍은 `for`가 $ni$를 다음 $i$로 삼는 회차에서 $(i, j)$ 자리로 자연히 나온다. 한 바퀴를 다 돌면 모든 대척점 쌍이 모인다.
- **중복 없이 딱 한 번씩** 뽑으려면 여기에 종료 관리를 더한다. 첫 대척점의 위치를 시작 마커로 기억해 두고, $j$가 그 마커로 되돌아오면 멈추는 방식이다(Toussaint의 고전적 열거법). 원리는 지금 뼈대와 같다. 평행한 변에서만 쌍을 하나 더 채우고, 한 바퀴에서 정확히 끊는다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 동률은 **평행한 변**에서 온다. 지지선이 변과 나란해지면 그 변 전체에 밀착해, 한 각도에서 대척점 쌍이 여럿 생긴다(꼭짓점–변 2개, 변–변 2×2).
- 5편 뼈대의 **지름 값은 평행 변이 있어도 옳다.** 변마다 두 끝점 $(i, j)$·$(ni, j)$를 모두 재고, 놓친 교차 쌍은 맞은편 변에서 다시 잡히기 때문이다.
- 5편이 미룬 건 지름이 아니라 대척점 쌍의 **완전한 열거**다(폭·최소 외접 사각형 등에 필요). 변–변 동률에서 뼈대는 교차 쌍 하나를 건너뛴다.
- strict `>`는 유지해 단조성을 지키고, 넓이가 같은 **동률만 따로 분기**해 빠진 교차 쌍을 채운다. 중복 없는 종료는 시작 마커로 한 바퀴를 끊어 관리한다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>이 열거가 뿌리를 둔 Rotating Calipers의 뼈대와 지름 문제 전체는 <a href="/blog/convex-hull-5">볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers</a>에서 다룬다. 여기서 채운 동률 처리를 얹으면, 폭이나 최소 외접 사각형 같은 이웃 문제로도 곧장 넘어갈 수 있다.</p>
</div>
````

- [ ] **Step 2: 빌드 검증**

Run: `npm run build`
Expected: 성공, "N page(s) built". KaTeX/frontmatter 오류 없음. `[SEO]` description 경고 없음(160자 이하).

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-calipers-edge.md
git commit -m "feat(convex-hull): 추가 설명 본문 — 평행 변 동률과 대척점 쌍 열거"
```

---

### Task 3: 5편 forward link 연결

**Files:**
- Modify: `src/content/posts/convex-hull-5.md` ("시리즈를 마치며" callout의 '추가 설명' 텍스트)

**Interfaces:**
- Consumes: Task 2가 만든 라우트 `/blog/convex-hull-calipers-edge`.

- [ ] **Step 1: 5편의 '추가 설명' 예고를 하이퍼링크로**

`src/content/posts/convex-hull-5.md`의 "시리즈를 마치며" 문단에서:

찾기:
```
Rotating Calipers의 엣지 케이스(평행 변·대척점 쌍의 정확한 열거)는 곧 이어질 **추가 설명** 글에서 마저 다룬다.
```
바꾸기:
```
Rotating Calipers의 엣지 케이스(평행 변·대척점 쌍의 정확한 열거)는 [추가 설명](/blog/convex-hull-calipers-edge) 글에서 마저 다룬다.
```

- [ ] **Step 2: 빌드 재검증**

Run: `npm run build`
Expected: 성공.

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/convex-hull-5.md
git commit -m "docs(convex-hull): 5편에서 추가 설명(대척점 열거)으로 링크 연결"
```

---

### Task 4: 리뷰 (플랜 외 후속)

플랜 실행이 끝나면 `/review-post convex-hull-calipers-edge`로 결정적 검사 + LLM 비평(L1~L7, 특히 L7 논증·복잡도, L4 SVG↔본문 일치)을 돌리고, 지적을 반영한 뒤 재빌드한다. 리포트는 `docs/reviews/2026-07-15-convex-hull-calipers-edge.md`. 반영 완료 후 PR 생성(Why 충분히, How 방법론 중심, 참조 코드 위치).

## Self-Review

**1. Spec coverage:** 스펙 본문 구성(되짚어보기·목차·동률출처·접촉3유형·지름값이미맞음·열거는다른문제·`>`vs`>=`·코드·핵심정리·이어지는글)은 Task 2 본문에 모두 포함. SVG 2장(접촉 유형, 평행 변 열거)은 Task 1. 5편 링크 연결은 Task 3. 빌드/리뷰는 Task 2·4. description 160자 이하는 Task 2 Step 2에서 검증. 누락 없음.

**2. Placeholder scan:** SVG·본문·치환 문구 모두 실제 내용 인라인. "TBD/적절히" 없음. 미발행 링크 없음(5편은 이미 발행됨).

**3. Type consistency:** SVG2의 꼭짓점 라벨 i/ni/j/j+1이 본문·코드의 대척점 쌍 표기와 일치(뼈대 기록=녹색 (i,j)·(ni,j), 동률 추가=주황 (i,j+1), 다음 변=회색 (ni,j+1)). 포인터 j는 CCW 순서상 맞은편 변의 top-right 꼭짓점에 멈춤(strict `>` 정지)을 SVG와 본문이 공유. 코드 헬퍼(`cross`, `dist2`, `report`)는 주석으로 의미 정의. 이미지 경로 2개가 Task 1 생성 파일과 일치. 5편 치환 문구는 현재 5편 "시리즈를 마치며"와 일치.
