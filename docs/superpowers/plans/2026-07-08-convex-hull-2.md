# 볼록 껍질 ② 포스트 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 노션 `Convex hull 1` 노트의 Graham Scan 섹션(하한 논증 포함)을 블로그 포스트 `convex-hull-2.md`와 SVG 도판 5장으로 옮긴다.

**Architecture:** 1편 `convex-hull-1.md`의 구조(도입 blockquote → 목차 callout → 본문 → 핵심 정리 → 이어지는 글)와 SVG 스타일(다크 배경 `#0f1117`, 초록/파랑/주황 팔레트)을 그대로 따른다. 수식은 KaTeX, 코드는 C++ 의사코드 수준(컴파일 검증 불필요).

**Tech Stack:** Astro content collections, remark-math + rehype-katex, 정적 SVG.

**Branch:** `feat/post-convex-hull-2` (이미 생성·스펙 커밋 완료)

## Global Constraints

- frontmatter: `category: algorithm`, `difficulty: 중급`, date는 작성일 `2026-07-08T09:00:00`
- 코드 언어는 C++, 1편의 `struct P`·`ccw()`를 재사용한다고 서술
- main 직접 커밋 금지, 모든 커밋은 `feat/post-convex-hull-2`에서
- SVG는 viewBox 가로 680 기준, 1편과 동일한 색상 규칙(배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 초록 `#34d399`, 파랑 `#93c5fd`/`#3b82f6`, 빨강 `#ef4444`/`#f87171`, 각주 `#94a3b8`)

---

## File Structure

- Create: `public/images/convex-hull-2/angle-sort.svg` — 기준점 각도 정렬 개념도
- Create: `public/images/convex-hull-2/scan-push.svg` — 좌회전 → push 장면
- Create: `public/images/convex-hull-2/scan-pop.svg` — 우회전 → pop 장면
- Create: `public/images/convex-hull-2/scan-result.svg` — 스캔 완료 후 껍질
- Create: `public/images/convex-hull-2/lower-bound.svg` — 정렬→껍질 환원
- Create: `src/content/posts/convex-hull-2.md` — 포스트 본문

도판 4장(angle-sort, scan-push, scan-pop, scan-result)은 **같은 점 배치**를 공유해 독자가 장면을 이어 볼 수 있게 한다. 점 배치(스크린 좌표, y 아래 방향):

| 점 | 좌표 | 비고 |
|---|---|---|
| Y | (150, 340) | 최하단 기준점 |
| 1 | (540, 320) | 각도 최소 |
| 2 | (520, 250) | |
| 3 | (460, 150) | |
| 4 | (360, 120) | |
| 5 | (280, 190) | 유일한 안쪽 점 — 6 도착 시 pop |
| 6 | (230, 160) | |
| 7 | (140, 220) | 각도 최대 |

이 배치에서 회전 방향은 실제 CCW 계산과 일치한다: Y→1→2, 1→2→3, 2→3→4, 3→4→5 모두 좌회전, **4→5→6만 우회전**(5 pop), pop 후 3→4→6 좌회전. 최종 껍질은 Y-1-2-3-4-6-7.

---

### Task 1: SVG 도판 5장 작성

**Files:**
- Create: `public/images/convex-hull-2/angle-sort.svg`
- Create: `public/images/convex-hull-2/scan-push.svg`
- Create: `public/images/convex-hull-2/scan-pop.svg`
- Create: `public/images/convex-hull-2/scan-result.svg`
- Create: `public/images/convex-hull-2/lower-bound.svg`

**Interfaces:**
- Produces: 포스트 본문(Task 2)이 `/images/convex-hull-2/<이름>.svg` 경로로 참조

- [ ] **Step 1: angle-sort.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="as-o" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#fbbf24"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">각도 정렬 — 기준점에서 반시계 순서 매기기</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">최하단 점 Y 기준 각도 오름차순 (비교는 각도가 아니라 CCW로)</text>

  <!-- horizontal baseline from Y -->
  <line x1="150" y1="340" x2="620" y2="340" stroke="#475569" stroke-width="1.3" stroke-dasharray="5 4"/>
  <text x="600" y="358" fill="#64748b" font-size="11">수평선(각도 0)</text>

  <!-- rays from Y to each point -->
  <g stroke="#334155" stroke-width="1">
    <line x1="150" y1="340" x2="540" y2="320"/>
    <line x1="150" y1="340" x2="520" y2="250"/>
    <line x1="150" y1="340" x2="460" y2="150"/>
    <line x1="150" y1="340" x2="360" y2="120"/>
    <line x1="150" y1="340" x2="280" y2="190"/>
    <line x1="150" y1="340" x2="230" y2="160"/>
    <line x1="150" y1="340" x2="140" y2="220"/>
  </g>

  <!-- CCW sweep arc -->
  <path d="M 260 334 A 112 112 0 0 0 176 236" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#as-o)"/>
  <text x="285" y="300" fill="#fbbf24" font-size="11" font-weight="600">반시계로 훑는 순서</text>

  <!-- points with order labels -->
  <g>
    <circle cx="540" cy="320" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="558" y="325" fill="#93c5fd" font-size="13" font-weight="700">1</text>
    <circle cx="520" cy="250" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="538" y="255" fill="#93c5fd" font-size="13" font-weight="700">2</text>
    <circle cx="460" cy="150" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="476" y="145" fill="#93c5fd" font-size="13" font-weight="700">3</text>
    <circle cx="360" cy="120" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="360" y="105" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">4</text>
    <circle cx="280" cy="190" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="296" y="185" fill="#93c5fd" font-size="13" font-weight="700">5</text>
    <circle cx="230" cy="160" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="226" y="145" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">6</text>
    <circle cx="140" cy="220" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="122" y="215" fill="#93c5fd" font-size="13" font-weight="700">7</text>
  </g>

  <!-- base point Y -->
  <circle cx="150" cy="340" r="8" fill="#34d399"/>
  <text x="138" y="368" fill="#6ee7b7" font-size="12" font-weight="700">Y (최하단)</text>

  <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">정렬된 순서 1→2→…→7로 도는 것이 Y를 도는 반시계 한 바퀴가 된다</text>
</svg>
```

- [ ] **Step 2: scan-push.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="sp-g" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Graham Scan — 좌회전이면 push</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">스택 위 두 점과 새 점이 좌회전이면 새 점을 스택에 쌓는다</text>

  <!-- path so far: Y -> 1 -> 2, candidate 2 -> 3 -->
  <line x1="150" y1="340" x2="540" y2="320" stroke="#34d399" stroke-width="2.5"/>
  <line x1="540" y1="320" x2="520" y2="250" stroke="#34d399" stroke-width="2.5"/>
  <line x1="520" y1="250" x2="460" y2="150" stroke="#34d399" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#sp-g)"/>

  <!-- left-turn arc at point 2 -->
  <path d="M 528 278 A 30 30 0 0 0 504 224" fill="none" stroke="#fbbf24" stroke-width="2"/>
  <text x="560" y="215" fill="#fbbf24" font-size="12" font-weight="600">좌회전 → push</text>

  <!-- remaining points (gray) -->
  <g fill="#64748b">
    <circle cx="360" cy="120" r="5"/>
    <circle cx="280" cy="190" r="5"/>
    <circle cx="230" cy="160" r="5"/>
    <circle cx="140" cy="220" r="5"/>
  </g>

  <!-- stacked points -->
  <circle cx="150" cy="340" r="8" fill="#34d399"/>
  <text x="140" y="368" fill="#6ee7b7" font-size="12" font-weight="700">Y</text>
  <circle cx="540" cy="320" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
  <text x="558" y="325" fill="#93c5fd" font-size="13" font-weight="700">1</text>
  <circle cx="520" cy="250" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
  <text x="540" y="255" fill="#93c5fd" font-size="13" font-weight="700">2</text>
  <circle cx="460" cy="150" r="7" fill="#34d399"/>
  <text x="476" y="145" fill="#6ee7b7" font-size="13" font-weight="700">3 (새 점)</text>

  <!-- stack visual -->
  <g>
    <text x="80" y="120" fill="#94a3b8" font-size="12" font-weight="600">스택</text>
    <rect x="60" y="132" width="64" height="26" rx="4" fill="#0b3b2e" stroke="#34d399" stroke-width="1.5"/>
    <text x="92" y="150" text-anchor="middle" fill="#6ee7b7" font-size="12" font-weight="700">3 ← push</text>
    <rect x="60" y="162" width="64" height="26" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="180" text-anchor="middle" fill="#93c5fd" font-size="12">2</text>
    <rect x="60" y="192" width="64" height="26" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="210" text-anchor="middle" fill="#93c5fd" font-size="12">1</text>
    <rect x="60" y="222" width="64" height="26" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="240" text-anchor="middle" fill="#93c5fd" font-size="12">Y</text>
  </g>

  <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">1→2 방향에서 2→3이 왼쪽으로 꺾이므로(ccw &gt; 0) 3을 push한다</text>
</svg>
```

- [ ] **Step 3: scan-pop.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="pp-g" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Graham Scan — 우회전이면 pop</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">우회전이 나오면 좌회전이 될 때까지 스택에서 점을 뺀다</text>

  <!-- confirmed path: Y -> 1 -> 2 -> 3 -> 4 -->
  <g stroke="#34d399" stroke-width="2.5">
    <line x1="150" y1="340" x2="540" y2="320"/>
    <line x1="540" y1="320" x2="520" y2="250"/>
    <line x1="520" y1="250" x2="460" y2="150"/>
    <line x1="460" y1="150" x2="360" y2="120"/>
  </g>

  <!-- rejected detour through 5 (red dashed) -->
  <line x1="360" y1="120" x2="280" y2="190" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 5"/>
  <line x1="280" y1="190" x2="230" y2="160" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="322" y="185" fill="#f87171" font-size="12" font-weight="600">우회전!</text>

  <!-- corrected edge after pop -->
  <line x1="360" y1="120" x2="230" y2="160" stroke="#34d399" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#pp-g)"/>

  <!-- popped point 5 -->
  <circle cx="280" cy="190" r="7" fill="#1f2937" stroke="#ef4444" stroke-width="2"/>
  <line x1="271" y1="181" x2="289" y2="199" stroke="#ef4444" stroke-width="2"/>
  <line x1="289" y1="181" x2="271" y2="199" stroke="#ef4444" stroke-width="2"/>
  <text x="290" y="215" fill="#f87171" font-size="12" font-weight="700">5 → pop</text>

  <!-- other points -->
  <circle cx="150" cy="340" r="8" fill="#34d399"/>
  <text x="140" y="368" fill="#6ee7b7" font-size="12" font-weight="700">Y</text>
  <g>
    <circle cx="540" cy="320" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="558" y="325" fill="#93c5fd" font-size="13" font-weight="700">1</text>
    <circle cx="520" cy="250" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="540" y="255" fill="#93c5fd" font-size="13" font-weight="700">2</text>
    <circle cx="460" cy="150" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="476" y="145" fill="#93c5fd" font-size="13" font-weight="700">3</text>
    <circle cx="360" cy="120" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="360" y="105" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">4</text>
  </g>
  <circle cx="230" cy="160" r="7" fill="#34d399"/>
  <text x="226" y="145" text-anchor="middle" fill="#6ee7b7" font-size="13" font-weight="700">6 (새 점)</text>
  <circle cx="140" cy="220" r="5" fill="#64748b"/>

  <!-- stack visual -->
  <g>
    <text x="80" y="90" fill="#94a3b8" font-size="12" font-weight="600">스택</text>
    <rect x="60" y="102" width="64" height="24" rx="4" fill="#1f2937" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 3"/>
    <text x="92" y="119" text-anchor="middle" fill="#f87171" font-size="12">5 → pop</text>
    <rect x="60" y="130" width="64" height="24" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="147" text-anchor="middle" fill="#93c5fd" font-size="12">4</text>
    <rect x="60" y="158" width="64" height="24" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="175" text-anchor="middle" fill="#93c5fd" font-size="12">3</text>
    <rect x="60" y="186" width="64" height="24" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="203" text-anchor="middle" fill="#93c5fd" font-size="12">2</text>
    <rect x="60" y="214" width="64" height="24" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="231" text-anchor="middle" fill="#93c5fd" font-size="12">1</text>
    <rect x="60" y="242" width="64" height="24" rx="4" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="92" y="259" text-anchor="middle" fill="#93c5fd" font-size="12">Y</text>
  </g>

  <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">4→5에서 5→6이 오른쪽으로 꺾이므로 5를 pop — 4→6은 좌회전이라 여기서 멈춘다</text>
</svg>
```

- [ ] **Step 4: scan-result.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">스캔 완료 — 스택에 남은 점이 볼록 껍질</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">모든 점을 한 번씩 처리하면 스택에는 껍질 꼭짓점만 반시계 순서로 남는다</text>

  <!-- hull polygon: Y-1-2-3-4-6-7 -->
  <polygon points="150,340 540,320 520,250 460,150 360,120 230,160 140,220"
           fill="#34d39914" stroke="#34d399" stroke-width="2.5"/>

  <!-- interior point 5 -->
  <circle cx="280" cy="190" r="6" fill="#64748b"/>
  <text x="294" y="196" fill="#94a3b8" font-size="11">5 (안쪽 — pop됨)</text>

  <!-- hull vertices -->
  <circle cx="150" cy="340" r="8" fill="#34d399"/>
  <text x="140" y="368" fill="#6ee7b7" font-size="12" font-weight="700">Y</text>
  <g>
    <circle cx="540" cy="320" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="558" y="325" fill="#93c5fd" font-size="13" font-weight="700">1</text>
    <circle cx="520" cy="250" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="540" y="255" fill="#93c5fd" font-size="13" font-weight="700">2</text>
    <circle cx="460" cy="150" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="476" y="145" fill="#93c5fd" font-size="13" font-weight="700">3</text>
    <circle cx="360" cy="120" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="360" y="105" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">4</text>
    <circle cx="230" cy="160" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="226" y="145" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">6</text>
    <circle cx="140" cy="220" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="122" y="215" fill="#93c5fd" font-size="13" font-weight="700">7</text>
  </g>

  <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">최종 스택 [Y, 1, 2, 3, 4, 6, 7] — 각 점은 최대 한 번 push, 한 번 pop되므로 스캔은 O(N)</text>
</svg>
```

- [ ] **Step 5: lower-bound.svg 작성**

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="lb-o" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#fbbf24"/>
    </marker>
    <marker id="lb-b" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#3b82f6"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">정렬을 볼록 껍질로 풀기 — 하한의 근거</text>
  <text x="340" y="50" text-anchor="middle" fill="#64748b" font-size="11">숫자를 원 위의 점으로 바꾸면, 껍질의 꼭짓점 순서가 곧 정렬 결과다</text>

  <!-- input numbers -->
  <text x="100" y="105" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="600">정렬할 숫자</text>
  <g>
    <rect x="70" y="120" width="60" height="30" rx="5" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="100" y="141" text-anchor="middle" fill="#93c5fd" font-size="14" font-weight="700">3</text>
    <rect x="70" y="160" width="60" height="30" rx="5" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="100" y="181" text-anchor="middle" fill="#93c5fd" font-size="14" font-weight="700">1</text>
    <rect x="70" y="200" width="60" height="30" rx="5" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="100" y="221" text-anchor="middle" fill="#93c5fd" font-size="14" font-weight="700">4</text>
    <rect x="70" y="240" width="60" height="30" rx="5" fill="#1e3a5f" stroke="#3b82f6" stroke-width="1.5"/>
    <text x="100" y="261" text-anchor="middle" fill="#93c5fd" font-size="14" font-weight="700">2</text>
  </g>

  <!-- transform arrow -->
  <line x1="150" y1="195" x2="255" y2="195" stroke="#3b82f6" stroke-width="2" marker-end="url(#lb-b)"/>
  <text x="202" y="180" text-anchor="middle" fill="#93c5fd" font-size="11">v ↦ 각도 v·2π/5</text>
  <text x="202" y="216" text-anchor="middle" fill="#64748b" font-size="10">(원 위의 점으로)</text>

  <!-- circle -->
  <circle cx="430" cy="230" r="120" fill="none" stroke="#334155" stroke-width="1.5" stroke-dasharray="5 4"/>

  <!-- hull (= all points, CCW order 1,2,3,4) -->
  <polygon points="467,116 333,159 333,301 467,344"
           fill="#34d39914" stroke="#34d399" stroke-width="2.5"/>

  <!-- CCW arrow along hull -->
  <path d="M 505 140 A 132 132 0 0 0 352 130" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#lb-o)"/>
  <text x="438" y="88" text-anchor="middle" fill="#fbbf24" font-size="11" font-weight="600">껍질을 반시계로 읽는다</text>

  <!-- points on circle -->
  <g>
    <circle cx="467" cy="116" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="485" y="112" fill="#93c5fd" font-size="13" font-weight="700">1</text>
    <circle cx="333" cy="159" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="303" y="155" fill="#93c5fd" font-size="13" font-weight="700">2</text>
    <circle cx="333" cy="301" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="303" y="313" fill="#93c5fd" font-size="13" font-weight="700">3</text>
    <circle cx="467" cy="344" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="485" y="356" fill="#93c5fd" font-size="13" font-weight="700">4</text>
  </g>

  <!-- result -->
  <text x="612" y="205" text-anchor="middle" fill="#94a3b8" font-size="12" font-weight="600">껍질 순회</text>
  <text x="612" y="228" text-anchor="middle" fill="#6ee7b7" font-size="14" font-weight="700">1→2→3→4</text>
  <text x="612" y="250" text-anchor="middle" fill="#94a3b8" font-size="11">= 정렬 결과</text>

  <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">원 위의 점은 전부 껍질 꼭짓점 — 껍질이 각도 순서, 즉 원래 숫자의 크기 순서를 돌려준다</text>
</svg>
```

- [ ] **Step 6: 커밋**

```bash
git add public/images/convex-hull-2/
git commit -m "feat(convex-hull): 2편 SVG 도판 5장 추가"
```

---

### Task 2: 포스트 본문 작성

**Files:**
- Create: `src/content/posts/convex-hull-2.md`

**Interfaces:**
- Consumes: Task 1의 SVG 5장 (`/images/convex-hull-2/*.svg`)
- Produces: 슬러그 `convex-hull-2` (1편의 "이어지는 글" 링크 대상)

- [ ] **Step 1: 포스트 파일 작성**

아래 내용을 그대로 작성한다.

`````markdown
---
title: "볼록 껍질 ② — Graham Scan과 정렬 하한"
date: 2026-07-08T09:00:00
description: "Package Wrapping은 걸음마다 남은 점 전체를 다시 훑어 최악 O(N²)이다. Graham Scan은 기준점에서 각도 정렬을 한 번만 한 뒤, 스택으로 좌회전만 남기며 훑어 O(N log N)에 볼록 껍질을 구한다. 나아가 정렬 문제를 볼록 껍질로 환원해, 비교 기반 모델에서는 이보다 빠를 수 없다는 Ω(N log N) 하한까지 확인한다."
tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Graham Scan"]
category: algorithm
difficulty: 중급
---

> [1편](/blog/convex-hull-1)의 Package Wrapping은 껍질 점 하나를 확정할 때마다 남은 점 전체를 다시 훑는다. 걸음마다 하는 일은 사실 "각도상 가장 바깥 점 찾기"로 매번 비슷하다. 그렇다면 **처음에 각도 정렬을 한 번만** 해 두면 어떨까? 이 아이디어가 **Graham Scan**이고, 결과는 $O(N \log N)$ — 그리고 그것이 사실상 한계라는 것까지 이번 편에서 확인한다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- Package Wrapping이 느려지는 이유 — 같은 계산의 반복
- 기준점 기준 **각도 정렬**을 CCW 비교로 한 번만 수행
- 스택으로 좌회전만 남기는 **Graham Scan** $O(N \log N)$
- 각 점이 최대 한 번 push/pop — 스캔 자체는 $O(N)$
- 정렬 문제의 환원으로 보는 **$\Omega(N \log N)$ 하한**

</div>

---

## 되짚어보기 — Package Wrapping의 한계

[1편](/blog/convex-hull-1)에서 세 점의 회전 방향을 정수 연산만으로 판정하는 **CCW**를 만들었고, 이를 이용해 포장지로 감싸듯 껍질을 한 변씩 찾는 **Package Wrapping**을 봤다. 최하단 점에서 시작해, 매 걸음 나머지 점을 전부 훑어 가장 바깥 점을 다음 껍질 점으로 확정하는 방식이었다. 걸음 하나가 $O(N)$, 걸음 수가 껍질 점 개수 $H$라서 전체 $O(NH)$ — 최악의 경우 모든 점이 껍질 위에 있으면 $O(N^2)$이다.

이 방법의 낭비는 분명하다. **걸음마다 남은 점 전체를 다시 훑는데, 매번 하는 계산이 거의 같다.** 각 걸음이 묻는 것은 결국 "현재 점 기준으로 어느 점이 가장 바깥(각도상 가장 앞)인가"이다. 이런 질문을 $H$번 반복할 거라면, 차라리 처음에 **모든 점을 각도순으로 정렬해 두는 편**이 낫지 않을까?

---

## 아이디어 — 각도 정렬을 한 번만

시작은 1편과 같다. **y좌표가 가장 작은 점 $Y$** 를 잡는다. 모든 점이 $Y$보다 위에 있으므로 $Y$는 반드시 껍질 위의 점이다.

이제 나머지 $N-1$개의 점을 **$Y$에서 바라본 각도 오름차순**으로 정렬한다. $Y$에서 오른쪽 수평 방향을 각도 0으로 두고, 반시계 방향으로 훑으며 만나는 순서대로 번호를 매기는 셈이다.

![각도 정렬 — 최하단 점 Y를 기준으로, 수평선에서 반시계 방향으로 훑으며 만나는 순서대로 점에 번호를 매긴다.](/images/convex-hull-2/angle-sort.svg)

각도를 직접 계산하지는 않는다. 1편에서 본 대로 $\arctan$은 부동소수점 오차를 부르기 때문이다. 두 점 $A$, $B$ 중 누가 각도상 앞인지는 **$\text{ccw}(Y, A, B)$의 부호**로 판정할 수 있다. 값이 양수면 $Y \to A \to B$가 좌회전, 즉 $A$가 $B$보다 각도가 작다(먼저 만난다). 이 비교 함수로 표준 정렬을 돌리면 끝이다.

```cpp
// Y: 최하단 점, ccw(): 1편에서 정의
sort(pts.begin() + 1, pts.end(),
     [&](P a, P b) { return ccw(Y, a, b) > 0; });
```

정렬이 끝나면 좋은 성질이 하나 생긴다. **정렬된 순서 그대로 점을 방문하면, $Y$ 주위를 반시계로 정확히 한 바퀴 도는 순회가 된다.** 껍질의 꼭짓점들도 이 순서 안에 (그 순서 그대로) 들어 있다. 남은 문제는 하나 — 이 순회에서 **어떤 점이 껍질에 남고, 어떤 점이 안쪽에 묻히는지**를 가려내는 것이다.

---

## Graham Scan — 스택으로 좌회전만 남기기

가려내는 기준은 이미 가지고 있다. **볼록 다각형을 반시계로 돌면 모든 꺾임이 좌회전**이다. 거꾸로 말해, 순회 도중 우회전이 나타났다면 그 꺾임점은 껍질의 꼭짓점일 수 없다 — 안쪽으로 파인 것이므로.

그래서 **스택**을 쓴다. 정렬된 순서대로 점을 하나씩 보면서:

1. 처음 두 점($Y$와 각도가 가장 작은 점)을 스택에 넣는다.
2. 새 점이 올 때마다, **스택 위의 두 점과 새 점**이 이루는 회전을 본다. **좌회전이면** 새 점을 push한다.
3. **우회전이면** 스택 맨 위의 점을 pop한다. 좌회전이 될 때까지 반복해서 뺀 뒤, 새 점을 push한다.

![좌회전이면 push — 스택 위 두 점(1, 2)과 새 점 3이 좌회전이므로 3을 스택에 쌓는다.](/images/convex-hull-2/scan-push.svg)

우회전이 나오는 순간이 이 알고리즘의 핵심 장면이다. 아래 그림에서 점 5까지는 순조롭게 쌓였지만, 점 6이 도착하자 $4 \to 5 \to 6$이 우회전이다. 이는 **점 5가 선분 $4$–$6$보다 안쪽에 있다**는 뜻이다. 5는 껍질의 꼭짓점이 될 수 없으므로 pop하고, 다시 스택 위 두 점($3$, $4$)과 $6$의 회전을 본다. 이번엔 좌회전이므로 pop을 멈추고 6을 push한다.

![우회전이면 pop — 4→5→6이 우회전이므로 5를 스택에서 빼고, 3→4→6이 좌회전이 되어 멈춘다.](/images/convex-hull-2/scan-pop.svg)

마지막 점까지 처리하고 나면 **스택에 남은 점들이 곧 볼록 껍질**이다. 반시계 순서 그대로 쌓여 있다.

![스캔 완료 — 스택에 남은 점 Y, 1, 2, 3, 4, 6, 7이 반시계 순서의 볼록 껍질을 이루고, pop된 5만 안쪽에 남는다.](/images/convex-hull-2/scan-result.svg)

<div class="callout callout-simple">
<div class="callout-title">처음 두 점은 pop되지 않는다</div>

pop은 스택에 점이 3개 이상일 때만 일어난다(회전을 보려면 세 점이 필요하다). 그리고 $Y$와 각도 최소 점은 애초에 pop될 이유가 없다 — 각도 정렬의 정의상 **나머지 모든 점이 이 두 점을 잇는 직선의 왼쪽**에 있기 때문에, 이 둘을 포함한 어떤 세 점을 잡아도 우회전이 만들어지지 않는다.

</div>

전체 코드는 정렬과 스캔 두 단계다.

```cpp
// pts: 점 목록, ccw(), struct P: 1편에서 정의
vector<P> grahamScan(vector<P> pts) {
    // 1) 기준점: y가 가장 작은 점을 맨 앞으로
    swap(pts[0], *min_element(pts.begin(), pts.end(),
        [](P a, P b) { return a.y < b.y; }));
    P Y = pts[0];

    // 2) 기준점 각도순 정렬 — 각도 대신 CCW로 비교
    sort(pts.begin() + 1, pts.end(),
         [&](P a, P b) { return ccw(Y, a, b) > 0; });

    // 3) 스캔 — 우회전이면 좌회전이 될 때까지 pop
    vector<P> hull;                       // 스택으로 사용
    for (P p : pts) {
        while (hull.size() >= 2 &&
               ccw(hull[hull.size()-2], hull.back(), p) < 0)
            hull.pop_back();
        hull.push_back(p);
    }
    return hull;                          // 반시계 순서의 껍질
}
```

**복잡도.** 스캔 단계부터 보자. while 루프 때문에 한 점을 처리하는 데 오래 걸릴 것 같지만, 전체를 놓고 보면 **각 점은 스택에 최대 한 번 들어가고 최대 한 번 나온다.** push 총 $N$번, pop 총 $N$번 이하 — 스캔 전체가 $O(N)$이다. 남는 것은 정렬뿐이므로,

$$
\underbrace{O(N \log N)}_{\text{정렬}} + \underbrace{O(N)}_{\text{스캔}} = O(N \log N)
$$

이다. Package Wrapping과 달리 껍질 점 개수 $H$와 무관하게 항상 $O(N \log N)$이 보장된다.

---

## 더 빠를 수는 없을까 — 정렬 하한

$O(N \log N)$에서 멈춰야 할까? 더 빠른 알고리즘을 찾으려 애쓰기 전에, **불가능하다는 증명**이 있는지 확인해 보자. 방법은 [가장 가까운 점 쌍](/blog/closest-pair-1)에서도 썼던 **환원(reduction)** 이다: "볼록 껍질을 빠르게 풀 수 있다면 정렬도 빠르게 풀린다"를 보이면, 정렬의 하한이 볼록 껍질의 하한이 된다.

정렬할 양수 $v_1, \cdots, v_N$이 있다고 하자. 최댓값 $M$을 찾은 뒤($O(N)$), 각 숫자를 **원 위의 점**으로 바꾼다.

$$
v_i \;\mapsto\; \theta_i = \frac{v_i}{M+1} \cdot 2\pi \;\mapsto\; \left(r\cos\theta_i,\; r\sin\theta_i\right)
$$

숫자가 클수록 각도가 크고, $M+1$로 나눈 덕분에 모든 각도는 $(0, 2\pi)$ 안에서 서로 겹치지 않는다. 그리고 결정적으로 — **원 위의 점은 전부 볼록 껍질의 꼭짓점이다.** 어떤 점도 다른 점들 안쪽에 있을 수 없기 때문이다.

![정렬을 볼록 껍질로 — 숫자를 각도로 바꿔 원 위에 올리면, 껍질을 반시계로 읽는 순서가 곧 숫자의 크기 순서다.](/images/convex-hull-2/lower-bound.svg)

이 점들의 볼록 껍질을 구하면 무슨 일이 벌어질까? 볼록 껍질 알고리즘은 꼭짓점을 **둘레를 도는 순서**로 내놓는다. 원 위에서 둘레를 도는 순서는 곧 **각도 순서**이고, 각도는 원래 숫자에 비례하므로 — **껍질의 출력이 곧 정렬 결과다.** 변환에 $O(N)$, 껍질 출력에서 정렬 결과를 읽는 데 $O(N)$이면 충분하다.

정리하면: 볼록 껍질을 $T(N)$에 푸는 알고리즘이 있다면 정렬을 $T(N) + O(N)$에 풀 수 있다. 그런데 정렬은 $\Omega(N \log N)$보다 빠를 수 없으므로,

$$
T(N) + O(N) = \Omega(N \log N) \quad\Longrightarrow\quad T(N) = \Omega(N \log N)
$$

이다. **볼록 껍질은 정렬만큼 어렵다.** Graham Scan의 $O(N \log N)$은 우연히 도달한 값이 아니라, 이 문제가 허용하는 최선이다.

<div class="callout callout-simple">
<div class="callout-title">하한의 전제 — 계산 모델</div>

정렬의 $\Omega(N \log N)$ 하한은 **비교 기반 모델**에서 성립하는 결과다(기수 정렬처럼 값의 구조를 이용하는 정렬은 이 하한을 비켜 간다). 볼록 껍질의 하한도 마찬가지로, 좌표에 대한 대수적 연산·비교만 허용하는 모델을 전제한다. 이 전제 안에서 위 환원이 하한을 옮겨 준다.

</div>

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- Package Wrapping의 낭비는 **걸음마다 같은 선형 탐색을 반복**하는 데 있다. 각도 정렬을 한 번만 해 두면 반복이 사라진다.
- 각도 정렬은 $\arctan$ 없이 **$\text{ccw}(Y, A, B)$의 부호를 비교 함수로** 써서 수행한다.
- **Graham Scan**은 정렬된 순서로 점을 훑으며, 스택 위 두 점과 새 점이 **우회전이면 좌회전이 될 때까지 pop**하고 push한다. 스택에 남는 것이 반시계 순서의 껍질이다.
- 각 점은 최대 한 번 push, 한 번 pop → 스캔은 $O(N)$, 전체는 정렬이 지배해 $O(N \log N)$.
- 숫자를 원 위의 점으로 바꾸는 환원으로 **볼록 껍질 $\Rightarrow$ 정렬**이 성립하므로, 볼록 껍질은 (비교 기반 모델에서) $\Omega(N \log N)$ — Graham Scan은 최적이다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

Graham Scan은 모든 점을 미리 알고 시작한다. 그런데 점이 **하나씩 추가되는** 상황이라면 어떨까? 3편에서는 **Plane Sweeping**으로 점을 x좌표 순서로 하나씩 삼키며 껍질을 점진적으로 키우는 방법을 다룬다. 접선을 찾아 껍질을 갱신하는 $O(N^2)$ 버전에서 출발해, 균형 이진 트리로 $O(N \log N)$까지 내려간다.

계산 기하의 다른 문제인 [가장 가까운 점 쌍](/blog/closest-pair-1)도 함께 보면 좋다.

</div>
`````

- [ ] **Step 2: 커밋**

```bash
git add src/content/posts/convex-hull-2.md
git commit -m "feat(convex-hull): 2편 포스트 본문 추가"
```

---

### Task 3: 빌드 검증

**Files:** (없음 — 검증 전용)

- [ ] **Step 1: 빌드 실행**

Run: `npm run build`
Expected: 에러 없이 완료. content collection 스키마 위반이나 KaTeX 파싱 오류가 없어야 한다. 출력에 `convex-hull-2` 페이지가 생성됨.

- [ ] **Step 2: 빌드 실패 시 대응**

스키마 오류면 프론트매터(`category: algorithm`, `difficulty: 중급`)를 확인한다. KaTeX 오류면 해당 수식의 `$`/`$$` 짝과 백슬래시 이스케이프를 확인한다. 수정 후 Step 1 재실행.

---

### Task 4: 포스트 리뷰

**Files:** (없음)

- [ ] **Step 1: review-post skill 실행**

`/review-post convex-hull-2` 로 main 대비 변경된 포스트의 내용·문체·SVG를 리뷰한다. 지적 사항이 있으면 반영 후 다시 커밋한다.

---

### Task 5: PR 생성

**Files:** (없음)

- [ ] **Step 1: push 및 PR 생성**

```bash
git push -u origin feat/post-convex-hull-2
gh pr create --title "feat(convex-hull): 볼록 껍질 ② — Graham Scan과 정렬 하한" --body "..."
```

PR 본문은 사용자 지침(2026-06-30)을 따른다: **Why는 충분히 길게**(1편이 예고한 후속, Package Wrapping의 한계를 해소하는 표준 알고리즘, 시리즈 완결성), **How는 방법론 중심**(각도 정렬의 CCW 비교자 치환, 스택 불변식 서사, 환원 기반 하한 논증, 도판 4장의 점 배치 공유). 구체 파일 경로는 '참조 코드 위치' 섹션에만.

---

## Self-Review

**1. Spec coverage:**
- 본문 5개 섹션(되짚어보기 → 아이디어 → Graham Scan → 하한 → 정리/예고) — Task 2 본문에 모두 포함.
- SVG 4~5장 — Task 1에서 5장(각도 정렬, push, pop, 결과, 하한 환원).
- CCW 비교자, 처음 두 점 안전성, push/pop O(N) 논증, 모델 조건 callout — 본문에 포함.
- 빌드 검증 — Task 3. review-post — Task 4. PR — Task 5.
- 갭 없음.

**2. Placeholder scan:** SVG·본문 전체가 코드 블록으로 포함됨. PR 본문만 방향 서술(작성 시점에 확정) — 지침 참조로 대체.

**3. Type consistency:** SVG 파일명 5개가 본문 `![...]` 참조와 일치. 점 배치 좌표가 도판 4장에서 동일. 슬러그 `convex-hull-2`는 1편 예고 링크(`/blog/convex-hull-2` 예정)와 일치. 프론트매터 키는 1편과 동일 구조.
