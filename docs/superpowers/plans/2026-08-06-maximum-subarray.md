# 최대 부분배열 포스트 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Notion 「Maximum Subarray」 노트를 본편 `maximum-subarray.md` 와 추가 설명 `maximum-subarray-why-extend.md` 두 편으로 발행한다.

**Architecture:** 본편은 `O(N^3) → O(N^2) → O(N)` 개선 서사로 카데인 갱신식까지 세우고, 갱신식의 정당성 증명과 누적합 관점(원문 Idea 3)은 추가 설명으로 뺀다. 도판 5장은 모두 같은 예시 배열 `[3, -5, 2, 4, -2, 3, -6, 8]` 과 같은 열 좌표계를 써서 장면이 이어지게 한다.

**Tech Stack:** Astro content collection (Markdown + KaTeX), 손으로 쓴 SVG, C++ 의사코드.

## Global Constraints

- 스펙: `docs/superpowers/specs/2026-08-06-maximum-subarray-design.md`. 계산값·provenance·정정 근거는 전부 거기에 있다.
- 브랜치 `feat/post-maximum-subarray`. main 직접 커밋 금지.
- 커밋 메시지에 `Co-Authored-By` 트레일러를 넣지 않는다.
- frontmatter 필수 키: `title`, `date`, `description`, `tags`, `category`, `difficulty`. `description` 은 40자 이상 220자 이하 (`review_post.py` 임계치).
- 문장 **내부**에 줄표(—)를 쓰지 않는다. "즉/곧/마침표"로 쓴다. 제목, 이미지 alt, SVG 텍스트의 구조적 줄표는 허용.
- 문두 접속어를 최소화한다 (`docs/writing-rules.md` 5단계 대원칙).
- SVG 열 좌표계 (도판 ①②③ 공통): 셀 `i` (1-based) 는 `x = 120 + 80(i-1)`, 너비 72. 중심은 `156 + 80(i-1)`. 경계 `j` (0-based) 는 `x = 116 + 80j`.
- SVG 팔레트: 배경 `#0f1117`, 제목 `#e2e8f0`, 부제 `#64748b`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`(채움 `#0e3a2c`), 파랑 `#93c5fd`/`#3b82f6`, 주황 `#fbbf24`(채움 `#3a2c0f`), 빨강 `#f87171`, 중립 셀 `#1e293b`/`#475569`.
- 예시 배열의 고정값: `P_0..P_8 = 0, 3, -2, 0, 4, 2, 5, -1, 7`, `k_1..k_8 = 3, 0, 2, 6, 4, 7, 1, 9`, 정답 9 (`a_3..a_8`), 부분배열 개수 36.

---

### Task 1: 본편 도판 3장

**Files:**
- Create: `public/images/maximum-subarray/problem.svg`
- Create: `public/images/maximum-subarray/prefix-sum.svg`
- Create: `public/images/maximum-subarray/kadane-scan.svg`

**Interfaces:**
- Consumes: 없음.
- Produces: Task 2 의 본문이 `/images/maximum-subarray/{problem,prefix-sum,kadane-scan}.svg` 세 경로를 참조한다.

- [ ] **Step 1: 디렉터리 생성**

```bash
mkdir -p public/images/maximum-subarray
```

- [ ] **Step 2: `problem.svg` 작성**

```svg
<svg viewBox="0 0 860 380" width="1290" height="570" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="860" height="380" rx="10" fill="#0f1117"/>

  <text x="430" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">합이 가장 큰 연속 구간 — 배열 전체를 쓰는 것이 답이 아니다</text>
  <text x="430" y="53" text-anchor="middle" fill="#64748b" font-size="11">전체 합은 7, 최대 부분배열의 합은 9</text>

  <!-- index labels -->
  <g fill="#64748b" font-size="11" text-anchor="middle">
    <text x="156" y="92">a₁</text>
    <text x="236" y="92">a₂</text>
    <text x="316" y="92">a₃</text>
    <text x="396" y="92">a₄</text>
    <text x="476" y="92">a₅</text>
    <text x="556" y="92">a₆</text>
    <text x="636" y="92">a₇</text>
    <text x="716" y="92">a₈</text>
  </g>

  <!-- cells: 1,2 중립 / 3..8 정답 구간 -->
  <rect x="120" y="104" width="72" height="56" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="200" y="104" width="72" height="56" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="280" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="360" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="440" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="520" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="600" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="680" y="104" width="72" height="56" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>

  <g font-size="20" font-weight="600" text-anchor="middle">
    <text x="156" y="141" fill="#e2e8f0">3</text>
    <text x="236" y="141" fill="#f87171">−5</text>
    <text x="316" y="141" fill="#6ee7b7">2</text>
    <text x="396" y="141" fill="#6ee7b7">4</text>
    <text x="476" y="141" fill="#f87171">−2</text>
    <text x="556" y="141" fill="#6ee7b7">3</text>
    <text x="636" y="141" fill="#f87171">−6</text>
    <text x="716" y="141" fill="#6ee7b7">8</text>
  </g>

  <!-- 전체 구간 -->
  <path d="M120,188 v10 H752 v-10" fill="none" stroke="#475569" stroke-width="1.4"/>
  <text x="436" y="216" text-anchor="middle" fill="#94a3b8" font-size="12.5">a₁ … a₈ = 3 − 5 + 2 + 4 − 2 + 3 − 6 + 8 = 7</text>

  <!-- 정답 구간 -->
  <path d="M280,248 v10 H752 v-10" fill="none" stroke="#34d399" stroke-width="1.8"/>
  <text x="516" y="276" text-anchor="middle" fill="#6ee7b7" font-size="13.5" font-weight="700">a₃ … a₈ = 2 + 4 − 2 + 3 − 6 + 8 = 9</text>

  <line x1="100" y1="300" x2="760" y2="300" stroke="#1e293b" stroke-width="1"/>

  <text x="430" y="326" text-anchor="middle" fill="#94a3b8" font-size="11.5">앞머리 a₁ + a₂ = −2 라, 둘을 함께 쓰면 뒤의 모든 구간이 2만큼 손해를 본다.</text>
  <text x="430" y="350" text-anchor="middle" fill="#94a3b8" font-size="11.5">중간의 −2 와 −6 은 통과한다. 연속이라는 조건 때문에 뒤의 8 을 쓰려면 반드시 지나가야 한다.</text>
</svg>
```

- [ ] **Step 3: `prefix-sum.svg` 작성**

```svg
<svg viewBox="0 0 860 420" width="1290" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="ms-ps-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 Z" fill="#fbbf24"/>
    </marker>
  </defs>

  <rect width="860" height="420" rx="10" fill="#0f1117"/>

  <text x="430" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">누적합을 미리 만들면 구간합이 뺄셈 한 번</text>
  <text x="430" y="53" text-anchor="middle" fill="#64748b" font-size="11">Pⱼ = a₁ + … + aⱼ, P₀ = 0 · 구간합 aᵢ + … + aⱼ = Pⱼ − Pᵢ₋₁</text>

  <g fill="#64748b" font-size="11" text-anchor="middle">
    <text x="156" y="92">a₁</text>
    <text x="236" y="92">a₂</text>
    <text x="316" y="92">a₃</text>
    <text x="396" y="92">a₄</text>
    <text x="476" y="92">a₅</text>
    <text x="556" y="92">a₆</text>
    <text x="636" y="92">a₇</text>
    <text x="716" y="92">a₈</text>
  </g>

  <rect x="120" y="102" width="72" height="50" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="200" y="102" width="72" height="50" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="280" y="102" width="72" height="50" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="360" y="102" width="72" height="50" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="440" y="102" width="72" height="50" rx="6" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <rect x="520" y="102" width="72" height="50" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="600" y="102" width="72" height="50" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="680" y="102" width="72" height="50" rx="6" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>

  <g font-size="17" font-weight="600" text-anchor="middle">
    <text x="156" y="135" fill="#cbd5e1">3</text>
    <text x="236" y="135" fill="#f87171">−5</text>
    <text x="316" y="135" fill="#6ee7b7">2</text>
    <text x="396" y="135" fill="#6ee7b7">4</text>
    <text x="476" y="135" fill="#f87171">−2</text>
    <text x="556" y="135" fill="#cbd5e1">3</text>
    <text x="636" y="135" fill="#f87171">−6</text>
    <text x="716" y="135" fill="#cbd5e1">8</text>
  </g>

  <!-- 경계로 내려가는 점선 -->
  <path d="M276,152 V216" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3 3"/>
  <path d="M516,152 V216" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3 3"/>

  <!-- 경계 축: 누적합은 원소가 아니라 경계에 붙는다 -->
  <line x1="96" y1="232" x2="776" y2="232" stroke="#334155" stroke-width="1.2"/>
  <g stroke="#475569" stroke-width="1.2">
    <line x1="116" y1="224" x2="116" y2="240"/>
    <line x1="196" y1="224" x2="196" y2="240"/>
    <line x1="356" y1="224" x2="356" y2="240"/>
    <line x1="436" y1="224" x2="436" y2="240"/>
    <line x1="596" y1="224" x2="596" y2="240"/>
    <line x1="676" y1="224" x2="676" y2="240"/>
    <line x1="756" y1="224" x2="756" y2="240"/>
  </g>
  <g stroke="#fbbf24" stroke-width="1.8">
    <line x1="276" y1="222" x2="276" y2="242"/>
    <line x1="516" y1="222" x2="516" y2="242"/>
  </g>

  <g fill="#64748b" font-size="10" text-anchor="middle">
    <text x="116" y="216">P₀</text>
    <text x="196" y="216">P₁</text>
    <text x="356" y="216">P₃</text>
    <text x="436" y="216">P₄</text>
    <text x="596" y="216">P₆</text>
    <text x="676" y="216">P₇</text>
    <text x="756" y="216">P₈</text>
  </g>
  <g fill="#fbbf24" font-size="10.5" text-anchor="middle" font-weight="700">
    <text x="276" y="214">P₂</text>
    <text x="516" y="214">P₅</text>
  </g>

  <g fill="#cbd5e1" font-size="13" text-anchor="middle">
    <text x="116" y="262">0</text>
    <text x="196" y="262">3</text>
    <text x="356" y="262">0</text>
    <text x="436" y="262">4</text>
    <text x="596" y="262">5</text>
    <text x="676" y="262">−1</text>
    <text x="756" y="262">7</text>
  </g>
  <g fill="#fbbf24" font-size="14" text-anchor="middle" font-weight="700">
    <text x="276" y="262">−2</text>
    <text x="516" y="262">2</text>
  </g>

  <!-- 두 경계 사이가 곧 구간 -->
  <path d="M276,300 H516" fill="none" stroke="#fbbf24" stroke-width="1.6" marker-start="url(#ms-ps-arrow)" marker-end="url(#ms-ps-arrow)"/>
  <text x="396" y="292" text-anchor="middle" fill="#fcd34d" font-size="12">P₅ − P₂</text>

  <text x="430" y="336" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">a₃ + a₄ + a₅ = 2 − (−2) = 4</text>

  <line x1="100" y1="358" x2="760" y2="358" stroke="#1e293b" stroke-width="1"/>
  <text x="430" y="384" text-anchor="middle" fill="#94a3b8" font-size="11.5">누적합은 원소가 아니라 원소 사이의 경계에 붙는다. 경계는 양끝을 합쳐 N + 1 개다.</text>
  <text x="430" y="406" text-anchor="middle" fill="#94a3b8" font-size="11.5">P₀ = 0 을 두면 앞머리가 비어 있는 구간에도 같은 뺄셈이 그대로 성립한다.</text>
</svg>
```

- [ ] **Step 4: `kadane-scan.svg` 작성**

```svg
<svg viewBox="0 0 860 420" width="1290" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="860" height="420" rx="10" fill="#0f1117"/>

  <text x="430" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">자리마다 값 하나만 들고 간다 — kᵢ₊₁ = max(kᵢ + x, 0)</text>
  <text x="430" y="53" text-anchor="middle" fill="#64748b" font-size="11">kᵢ = aᵢ 에서 끝나는 부분배열의 최대 합 (빈 배열 허용)</text>

  <g fill="#64748b" font-size="11" text-anchor="middle">
    <text x="156" y="86">i = 1</text>
    <text x="236" y="86">2</text>
    <text x="316" y="86">3</text>
    <text x="396" y="86">4</text>
    <text x="476" y="86">5</text>
    <text x="556" y="86">6</text>
    <text x="636" y="86">7</text>
    <text x="716" y="86">8</text>
  </g>

  <!-- a 행 -->
  <text x="104" y="124" text-anchor="end" fill="#94a3b8" font-size="12">aᵢ</text>
  <rect x="120" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="200" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="280" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="360" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="440" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="520" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="600" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="680" y="98" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <g font-size="15" text-anchor="middle">
    <text x="156" y="124" fill="#cbd5e1">3</text>
    <text x="236" y="124" fill="#f87171">−5</text>
    <text x="316" y="124" fill="#cbd5e1">2</text>
    <text x="396" y="124" fill="#cbd5e1">4</text>
    <text x="476" y="124" fill="#f87171">−2</text>
    <text x="556" y="124" fill="#cbd5e1">3</text>
    <text x="636" y="124" fill="#f87171">−6</text>
    <text x="716" y="124" fill="#cbd5e1">8</text>
  </g>

  <!-- k 행 -->
  <text x="104" y="196" text-anchor="end" fill="#94a3b8" font-size="12">kᵢ</text>
  <rect x="120" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="200" y="170" width="72" height="40" rx="5" fill="#3a2c0f" stroke="#fbbf24" stroke-width="1.8"/>
  <rect x="280" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="360" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="440" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="520" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="600" y="170" width="72" height="40" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
  <rect x="680" y="170" width="72" height="40" rx="5" fill="#0e3a2c" stroke="#34d399" stroke-width="2"/>
  <g font-size="15" text-anchor="middle">
    <text x="156" y="196" fill="#cbd5e1">3</text>
    <text x="236" y="196" fill="#fef3c7" font-weight="700">0</text>
    <text x="316" y="196" fill="#cbd5e1">2</text>
    <text x="396" y="196" fill="#cbd5e1">6</text>
    <text x="476" y="196" fill="#cbd5e1">4</text>
    <text x="556" y="196" fill="#cbd5e1">7</text>
    <text x="636" y="196" fill="#cbd5e1">1</text>
    <text x="716" y="196" fill="#6ee7b7" font-weight="700">9</text>
  </g>

  <!-- 끊기는 자리 -->
  <path d="M276,164 V246" stroke="#fbbf24" stroke-width="1.4" stroke-dasharray="5 4"/>
  <text x="270" y="266" text-anchor="end" fill="#fcd34d" font-size="11">k₁ + a₂ = 3 − 5 = −2 &lt; 0 이라 0으로 끊는다</text>
  <text x="282" y="266" text-anchor="start" fill="#94a3b8" font-size="11">여기서부터 새 구간이 자란다</text>

  <line x1="100" y1="290" x2="760" y2="290" stroke="#1e293b" stroke-width="1"/>

  <text x="430" y="322" text-anchor="middle" fill="#34d399" font-size="20" font-weight="700">max(k₁ … k₈) = 9</text>
  <text x="430" y="348" text-anchor="middle" fill="#94a3b8" font-size="12">끊긴 자리 다음인 a₃ 에서 자라기 시작해 a₈ 에서 최대가 된다</text>

  <text x="430" y="390" text-anchor="middle" fill="#94a3b8" font-size="11.5">모든 부분배열은 어딘가에서 끝나므로, 자리별 최선을 다 모으면 빠뜨린 후보가 없다.</text>
</svg>
```

- [ ] **Step 5: SVG 파싱 검증**

```bash
python -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in sorted(glob.glob('public/images/maximum-subarray/*.svg'))]; print('svg ok', len(glob.glob('public/images/maximum-subarray/*.svg')))"
```

Expected: `svg ok 3`

- [ ] **Step 6: 커밋**

```bash
git add public/images/maximum-subarray
git commit -m "content(algo): 최대 부분배열 본편 도판 3장"
```

---

### Task 2: 본편 본문

**Files:**
- Create: `src/content/posts/maximum-subarray.md`

**Interfaces:**
- Consumes: Task 1 의 세 SVG 경로.
- Produces: 라우트 `/blog/maximum-subarray`. Task 4 의 추가 설명이 이 경로로 돌아오는 링크를 건다.

- [ ] **Step 1: 본문 전체 작성**

`src/content/posts/maximum-subarray.md` 를 아래 내용 그대로 만든다.

````markdown
---
title: "최대 부분배열 — 자리마다 최선 하나만 들고 간다"
date: 2026-08-06T09:00:00
description: "합이 가장 큰 연속 구간을 찾는 문제를 세 번 푼다. 모든 구간을 세면 O(N³), 누적합을 미리 만들면 O(N²), 각 자리에서 끝나는 최선의 합 하나만 들고 가면 O(N)이다. 빈 배열을 답으로 허용하느냐가 점화식을 어떻게 바꾸는지까지 본다."
tags: ["Algorithm", "Maximum Subarray", "Kadane", "Prefix Sum", "Dynamic Programming"]
category: algorithm
difficulty: 중급
numbered: true
---

> 배열의 원소가 전부 양수라면 답은 뻔하다. 무엇을 더 붙여도 합이 커지니 배열 전체가 답이다. 음수가 섞이는 순간 문제가 시작된다. 어디서 끊고, 어디서 손해를 감수하고 지나갈 것인가.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- **문제**: 합이 가장 큰 연속 구간. 전체를 다 쓰는 것이 답이 아닌 이유
- **$O(N^3)$**: 모든 구간을 세어 본다. 구간은 몇 개인가
- **$O(N^2)$**: 누적합을 미리 만들면 구간합이 뺄셈 한 번
- **$O(N)$**: 자리마다 최선 하나만 들고 가는 갱신
- **빈 배열을 허용하는가**: 정의가 점화식을 바꾼다

</div>

---

## 문제

연속 부분배열은 배열에서 이웃한 원소를 통째로 잘라낸 조각이다. 배열 $a_1, a_2, \dots, a_N$ 에서 $a_i, a_{i+1}, \dots, a_j$ ($i \le j$) 꼴이면 모두 연속 부분배열이다. 이 중 원소의 합이 가장 큰 것을 찾는다.

원소가 전부 양수면 고민할 것이 없다. 무엇을 더 붙여도 합이 커지므로 배열 전체가 답이다. 음수가 섞이면 달라진다.

$a = [3, -5, 2, 4, -2, 3, -6, 8]$ 을 보자. 배열 전체의 합은 $3 - 5 + 2 + 4 - 2 + 3 - 6 + 8 = 7$ 이다. 답은 7이 아니다. 앞의 $3, -5$ 를 버리고 $a_3$ 부터 끝까지 고르면 $2 + 4 - 2 + 3 - 6 + 8 = 9$ 다.

![예시 배열 [3, −5, 2, 4, −2, 3, −6, 8]. 전체 합은 7이지만 a₃부터 a₈까지 고른 구간의 합이 9로 더 크다.](/images/maximum-subarray/problem.svg)

앞머리를 버린 이유는 $a_1 + a_2 = -2$ 라서다. 이 둘을 함께 끌고 가면 뒤에 오는 모든 구간이 2만큼 손해를 본다. 중간의 $-2$ 와 $-6$ 은 사정이 다르다. 버리고 싶어도 연속이라는 조건 때문에 뒤의 8을 쓰려면 반드시 지나가야 한다. 지나가는 대가 6보다 그 뒤에서 얻는 8이 크므로 감수한다.

어떤 음수는 버리고 어떤 음수는 통과하는 이 판단을 자동으로 내리는 것이 이 문제다.

---

## 모두 세어 보기

가장 단순한 방법은 모든 연속 부분배열을 나열하고 각각의 합을 구하는 것이다. 비용을 따지려면 후보가 몇 개인지부터 알아야 한다.

**시작 위치로 세기.** $a_1$ 에서 시작하는 부분배열은 끝 위치가 $a_1$ 부터 $a_N$ 까지 $N$ 개다. $a_2$ 에서 시작하면 $N-1$ 개, 계속 줄어 $a_N$ 에서 시작하면 1개다. 모두 더하면

$$
N + (N-1) + \cdots + 1 = \frac{N(N+1)}{2}
$$

**경계로 세기.** 부분배열 하나는 왼쪽 경계와 오른쪽 경계로 결정된다. 경계는 $a_1$ 앞, 원소 사이 $N-1$ 곳, $a_N$ 뒤를 합쳐 $N+1$ 개다. 서로 다른 두 곳을 고르면 부분배열 하나가 정해지므로

$$
\binom{N+1}{2} = \frac{N(N+1)}{2}
$$

두 셈법이 같은 값을 준다. $N = 8$ 이면 36개다.

후보 하나의 합을 처음부터 더하면 최악 $O(N)$ 이 걸린다. 후보가 $\Theta(N^2)$ 개이므로 전체는 $O(N^3)$ 이다.

---

## 누적합으로 $O(N^2)$

$O(N^3)$ 에 곱해진 마지막 $N$ 은 합을 매번 처음부터 다시 더해서 생긴다. 합을 미리 준비해 두면 사라진다.

누적합 $P_j$ 를 앞에서부터 $j$ 개의 합으로 정의한다.

$$
P_0 = 0, \qquad P_j = a_1 + a_2 + \cdots + a_j
$$

$a_i$ 부터 $a_j$ 까지의 합은 $P_j$ 에서 앞머리 $P_{i-1}$ 을 덜어낸 값이다.

$$
a_i + a_{i+1} + \cdots + a_j = P_j - P_{i-1}
$$

$P_0 = 0$ 을 따로 둔 이유가 여기서 나온다. $i = 1$ 일 때 덜어낼 앞머리가 없는데, $P_0 = 0$ 이 그 "비어 있음"을 대신한다. 누적합이 원소가 아니라 원소 사이의 경계에 붙는다고 보면 자연스럽다. 경계가 $N+1$ 개라는 앞 절의 셈과 같은 이야기다.

예시 배열의 누적합은 $P_0 \dots P_8 = 0,\, 3,\, -2,\, 0,\, 4,\, 2,\, 5,\, -1,\, 7$ 이다. $a_3$ 부터 $a_5$ 까지의 합을 확인하면 $P_5 - P_2 = 2 - (-2) = 4$ 이고, 직접 더한 $2 + 4 - 2 = 4$ 와 같다.

![원소 배열 아래에 경계마다 누적합 P₀부터 P₈까지를 붙인 그림. P₅ − P₂ = 2 − (−2) = 4가 a₃ + a₄ + a₅ 와 같다.](/images/maximum-subarray/prefix-sum.svg)

누적합을 만드는 데 한 번의 훑기, 곧 $O(N)$ 이면 된다. 그 뒤로는 후보 하나의 합이 뺄셈 한 번이다. 후보가 $\Theta(N^2)$ 개이므로 전체는 $O(N^2)$ 이고, 누적합 배열을 저장하는 공간 $O(N)$ 이 더 든다.

---

## 자리마다 최선 하나

$O(N^2)$ 은 후보를 여전히 전부 본다. 더 줄이려면 후보를 세는 일 자체를 그만두어야 한다.

먼저 정의를 못박는다. **빈 배열도 답으로 허용한다.** 원소를 하나도 고르지 않으면 합은 0이다. 모든 원소가 음수인 배열에서 답이 0인지 가장 큰 음수인지는 이 정의가 갈라놓는다. 문제마다 조건으로 주어지며, 풀이는 거의 같다.

<div class="callout callout-key">
<div class="callout-title">부분 문제의 정의</div>

$k_i$ = $a_i$ **에서 끝나는** 부분배열의 합 중 최댓값 (빈 배열 허용)

</div>

각 자리마다 이 값 하나씩만 들고 다닌다. $k_1, \dots, k_N$ 을 모두 구하면 답은 그중 최댓값이다. 모든 부분배열은 어딘가에서 끝나므로 빠뜨린 후보가 없다.

$k_i$ 에서 $k_{i+1}$ 로 넘어가는 규칙을 보자. $x = a_{i+1}$ 이라 하자. $a_{i+1}$ 에서 끝나는 부분배열은 두 종류다.

- **$x$ 를 포함하는 것.** $a_i$ 에서 끝나는 부분배열 뒤에 $x$ 를 붙인 모양이다. 앞부분이 비어 있어도 되므로 $x$ 하나짜리도 여기 들어간다. 앞부분으로 가능한 최대 합이 $k_i$ 이니, 이 종류의 최대 합은 $k_i + x$ 다.
- **빈 배열.** 합은 0이다.

둘 중 큰 쪽이 $k_{i+1}$ 이다.

$$
k_0 = 0, \qquad k_{i+1} = \max(k_i + x,\; 0)
$$

$k_i + x$ 가 음수면 0을 고르는 편이 낫다. 여기서 구간이 한 번 끊긴다. 지금까지 끌고 온 앞부분을 통째로 버리고 다음 자리부터 새로 시작한다는 뜻이다.

"앞부분으로 가능한 최대 합이 $k_i$" 라는 한 줄에 이 알고리즘의 정당성이 전부 들어 있다. 앞부분을 조금 손해 보게 잡으면 뒤에서 더 벌 수 있지 않을까 하는 의심은 [추가 설명 — 왜 이어 붙이는 것이 최선인가](/blog/maximum-subarray-why-extend)에서 닫는다.

예시 배열을 훑으면 $k$ 수열은 $3,\, 0,\, 2,\, 6,\, 4,\, 7,\, 1,\, 9$ 다. $i = 2$ 에서 $k_1 + a_2 = 3 - 5 = -2$ 라 0으로 끊었고, 그 다음 자리부터 자란 구간이 $i = 8$ 에서 9에 닿는다.

![aᵢ 행과 kᵢ 행을 나란히 놓은 표. i=2에서 kᵢ가 0으로 끊기고, i=8에서 최댓값 9가 나온다.](/images/maximum-subarray/kadane-scan.svg)

코드는 값 두 개만 들고 가면 된다.

```cpp
// a[0..n-1].  빈 배열을 허용하는 정의이므로 답은 항상 0 이상이다.
long long maxSubarray(const vector<int>& a) {
    long long k = 0, best = 0;   // k: 지금 자리에서 끝나는 최선, best: 지금까지의 답
    for (int x : a) {
        k = max(k + x, 0LL);     // 음수로 내려가면 앞부분을 버린다
        best = max(best, k);
    }
    return best;
}
```

훑기 한 번, 변수 두 개다. 시간은 $O(N)$, 공간은 $O(1)$ 이다. 누적합 배열조차 남기지 않는다.

---

## 빈 배열을 허용하지 않으면

원소를 최소 하나는 골라야 한다는 조건이면 정의가 바뀐다. $k_i$ 를 "$a_i$ 에서 끝나는 **비어 있지 않은** 부분배열의 최대 합"으로 다시 두자. $a_{i+1}$ 에서 끝나고 비어 있지 않은 부분배열도 두 종류다.

- **원소가 둘 이상.** 앞부분이 비어 있지 않으므로 최대 합은 $k_i + x$ 다.
- **$x$ 하나뿐.** 합은 $x$ 다.

$$
k_1 = a_1, \qquad k_{i+1} = \max(k_i + x,\; x)
$$

0 대신 $x$ 와 비교한다는 점만 다르다. 이제 $k_i$ 가 음수일 수 있다.

```cpp
// 원소를 최소 하나 고르는 정의.  a 는 비어 있지 않다고 가정한다.
long long maxSubarrayNonEmpty(const vector<int>& a) {
    long long k = a[0], best = a[0];
    for (size_t i = 1; i < a.size(); i++) {
        k = max(k + a[i], (long long)a[i]);
        best = max(best, k);
    }
    return best;
}
```

정의가 항상 답을 바꾸지는 않는다. 예시 배열을 비허용 정의로 돌리면 $k$ 수열은 $3,\, -2,\, 2,\, 6,\, 4,\, 7,\, 1,\, 9$ 이고 답은 그대로 9다. 답이 양수인 배열에서는 빈 배열이 최선이 될 일이 없다. 갈라지는 것은 모든 원소가 음수일 때다. $[-3, -1, -2]$ 에서 허용하면 답이 0, 허용하지 않으면 $-1$ 이다.

---

## 포함하는가, 포함하지 않는가

같은 알고리즘을 다른 말로 적을 수도 있다. 자리마다 값 두 개를 들고 간다.

- $a_i$ 를 **포함하는** 부분배열 중 최선
- $a_i$ 를 **포함하지 않는** 부분배열 중 최선

첫 번째는 $k_i$ 그 자체다. 두 번째는 $a_i$ 앞에서 이미 끝난 부분배열의 최선, 곧 $k_1, \dots, k_{i-1}$ 의 최댓값이다. 위 코드의 `best` 변수가 바로 이 값을 들고 다닌다. 두 값을 나란히 적는 서술과 `k`·`best` 두 변수를 굴리는 코드는 같은 계산이다.

[동적 계획법 ②](/blog/dp-2)는 "마지막 날에 일하는가"라는 결정 하나로 점화식을 세웠다. 여기서도 결정은 하나, "이 자리를 포함하는가"다. 결정이 깔끔하게 두 갈래로 갈리는 것은 부분 문제를 "$a_i$ 에서 끝나는"으로 잡았기 때문이다. 부분 문제를 "$a_1 \dots a_i$ 안에서의 답"으로 잡으면 이렇게 되지 않는다. 앞의 답이 어디서 끝났는지 모르면 $a_{i+1}$ 을 이어 붙일 수 있는지 판단할 수 없다. 부분 문제를 어떻게 정의하느냐가 점화식의 난이도를 정한다.

---

## 더 나가면

여기서부터는 강의 노트 밖 확장이다.

두 가지가 남았다. 하나는 $k_{i+1} = \max(k_i + x,\, 0)$ 이 왜 옳은가다. "앞부분의 최선은 $k_i$" 를 당연하게 받아들였지만, 앞부분에서 조금 손해 보고 뒤에서 더 버는 상황이 없다고 어떻게 장담하는가.

다른 하나는 누적합으로 돌아가는 길이다. 모든 부분배열의 합이 $P_j - P_i$ 꼴이므로, $P_j$ 를 훑으면서 지금까지 본 가장 작은 $P$ 를 빼면 답이 나온다. 이 방법도 $O(N)$ 이고, 사실 위의 갱신식과 같은 계산이다.

둘 다 [추가 설명 — 왜 이어 붙이는 것이 최선인가](/blog/maximum-subarray-why-extend)에서 다룬다.

---

## 마치며

같은 문제를 세 번 풀었다. 후보는 세 번 모두 같았고 달라진 것은 후보를 보는 방법이다. $O(N^3)$ 은 후보마다 합을 처음부터 계산했다. $O(N^2)$ 은 합을 미리 만들어 뺄셈으로 바꿨다. $O(N)$ 은 후보를 나열하는 일 자체를 그만뒀다.

마지막 도약의 열쇠는 "$a_i$ 에서 끝나는"이라는 부분 문제의 정의였다. 이 한 줄이 $\Theta(N^2)$ 개의 후보를 $N$ 개의 값으로 접었다. 문제를 어떻게 쪼개느냐가 알고리즘을 정한다.
````

- [ ] **Step 2: 빌드 검증**

```bash
npm run build
```

Expected: 오류 없이 종료하고 `N page(s) built` 출력. 직전 대비 페이지 수가 1 늘어난다.

- [ ] **Step 3: 결정적 검사**

```bash
python .claude/review_post.py src/content/posts/maximum-subarray.md
```

Expected: `발견 사항 없음 ✅`. 줄표·굵게·description 길이·이미지 경로 지적이 나오면 문장을 고쳐 다시 돌린다. 이때 조건이나 논증 단계를 삭제하지 않는다.

- [ ] **Step 4: 커밋**

```bash
git add src/content/posts/maximum-subarray.md
git commit -m "content(algo): 최대 부분배열 본편"
```

---

### Task 3: 추가 설명 도판 2장

**Files:**
- Create: `public/images/maximum-subarray-why-extend/extend.svg`
- Create: `public/images/maximum-subarray-why-extend/prefix-min.svg`

**Interfaces:**
- Consumes: 없음.
- Produces: Task 4 의 본문이 `/images/maximum-subarray-why-extend/{extend,prefix-min}.svg` 두 경로를 참조한다.

- [ ] **Step 1: 디렉터리 생성**

```bash
mkdir -p public/images/maximum-subarray-why-extend
```

- [ ] **Step 2: `extend.svg` 작성**

```svg
<svg viewBox="0 0 860 440" width="1290" height="660" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="ms-ex-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 Z" fill="#94a3b8"/>
    </marker>
    <marker id="ms-ex-arrow-hi" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 Z" fill="#34d399"/>
    </marker>
  </defs>

  <rect width="860" height="440" rx="10" fill="#0f1117"/>

  <text x="430" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">a₆ 을 포함하는 후보는 a₅ 에서 끝나는 후보와 1:1로 대응한다</text>
  <text x="430" y="51" text-anchor="middle" fill="#64748b" font-size="11">x = a₆ = 3 · 모든 후보에 같은 3을 더하므로 순위가 바뀌지 않는다</text>

  <text x="246" y="82" text-anchor="middle" fill="#94a3b8" font-size="11.5">S₅ : a₅ 에서 끝나는 후보 (빈 배열 포함)</text>
  <text x="636" y="82" text-anchor="middle" fill="#94a3b8" font-size="11.5">T₆ : a₆ 에서 끝나고 a₆ 을 포함하는 후보</text>

  <!-- row 1 -->
  <rect x="96" y="96" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="110" y="117" fill="#cbd5e1" font-size="12.5">빈 배열</text>
  <text x="382" y="117" text-anchor="end" fill="#cbd5e1" font-size="13">0</text>
  <path d="M404,112 H478" fill="none" stroke="#94a3b8" stroke-width="1.2" marker-end="url(#ms-ex-arrow)"/>
  <text x="441" y="104" text-anchor="middle" fill="#64748b" font-size="9.5">+3</text>
  <rect x="486" y="96" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="500" y="117" fill="#cbd5e1" font-size="12.5">[a₆]</text>
  <text x="772" y="117" text-anchor="end" fill="#cbd5e1" font-size="13">3</text>

  <!-- row 2 -->
  <rect x="96" y="140" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="110" y="161" fill="#cbd5e1" font-size="12.5">[a₅]</text>
  <text x="382" y="161" text-anchor="end" fill="#f87171" font-size="13">−2</text>
  <path d="M404,156 H478" fill="none" stroke="#94a3b8" stroke-width="1.2" marker-end="url(#ms-ex-arrow)"/>
  <text x="441" y="148" text-anchor="middle" fill="#64748b" font-size="9.5">+3</text>
  <rect x="486" y="140" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="500" y="161" fill="#cbd5e1" font-size="12.5">[a₅ a₆]</text>
  <text x="772" y="161" text-anchor="end" fill="#cbd5e1" font-size="13">1</text>

  <!-- row 3 -->
  <rect x="96" y="184" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="110" y="205" fill="#cbd5e1" font-size="12.5">[a₄ a₅]</text>
  <text x="382" y="205" text-anchor="end" fill="#cbd5e1" font-size="13">2</text>
  <path d="M404,200 H478" fill="none" stroke="#94a3b8" stroke-width="1.2" marker-end="url(#ms-ex-arrow)"/>
  <text x="441" y="192" text-anchor="middle" fill="#64748b" font-size="9.5">+3</text>
  <rect x="486" y="184" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="500" y="205" fill="#cbd5e1" font-size="12.5">[a₄ a₅ a₆]</text>
  <text x="772" y="205" text-anchor="end" fill="#cbd5e1" font-size="13">5</text>

  <!-- row 4 : 최댓값 -->
  <rect x="96" y="228" width="300" height="32" rx="5" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <text x="110" y="249" fill="#6ee7b7" font-size="12.5" font-weight="700">[a₃ a₄ a₅]</text>
  <text x="382" y="249" text-anchor="end" fill="#6ee7b7" font-size="13.5" font-weight="700">4</text>
  <path d="M404,244 H478" fill="none" stroke="#34d399" stroke-width="1.6" marker-end="url(#ms-ex-arrow-hi)"/>
  <text x="441" y="236" text-anchor="middle" fill="#34d399" font-size="9.5">+3</text>
  <rect x="486" y="228" width="300" height="32" rx="5" fill="#0e3a2c" stroke="#34d399" stroke-width="1.8"/>
  <text x="500" y="249" fill="#6ee7b7" font-size="12.5" font-weight="700">[a₃ a₄ a₅ a₆]</text>
  <text x="772" y="249" text-anchor="end" fill="#6ee7b7" font-size="13.5" font-weight="700">7</text>

  <!-- row 5 -->
  <rect x="96" y="272" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="110" y="293" fill="#cbd5e1" font-size="12.5">[a₂ a₃ a₄ a₅]</text>
  <text x="382" y="293" text-anchor="end" fill="#f87171" font-size="13">−1</text>
  <path d="M404,288 H478" fill="none" stroke="#94a3b8" stroke-width="1.2" marker-end="url(#ms-ex-arrow)"/>
  <text x="441" y="280" text-anchor="middle" fill="#64748b" font-size="9.5">+3</text>
  <rect x="486" y="272" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="500" y="293" fill="#cbd5e1" font-size="12.5">[a₂ a₃ a₄ a₅ a₆]</text>
  <text x="772" y="293" text-anchor="end" fill="#cbd5e1" font-size="13">2</text>

  <!-- row 6 -->
  <rect x="96" y="316" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="110" y="337" fill="#cbd5e1" font-size="12.5">[a₁ a₂ a₃ a₄ a₅]</text>
  <text x="382" y="337" text-anchor="end" fill="#cbd5e1" font-size="13">2</text>
  <path d="M404,332 H478" fill="none" stroke="#94a3b8" stroke-width="1.2" marker-end="url(#ms-ex-arrow)"/>
  <text x="441" y="324" text-anchor="middle" fill="#64748b" font-size="9.5">+3</text>
  <rect x="486" y="316" width="300" height="32" rx="5" fill="#1e293b" stroke="#475569" stroke-width="1.1"/>
  <text x="500" y="337" fill="#cbd5e1" font-size="12.5">[a₁ a₂ a₃ a₄ a₅ a₆]</text>
  <text x="772" y="337" text-anchor="end" fill="#cbd5e1" font-size="13">5</text>

  <line x1="96" y1="366" x2="786" y2="366" stroke="#1e293b" stroke-width="1"/>

  <text x="246" y="394" text-anchor="middle" fill="#34d399" font-size="14" font-weight="700">최댓값 4 = k₅</text>
  <text x="636" y="394" text-anchor="middle" fill="#34d399" font-size="14" font-weight="700">최댓값 7 = k₆ = k₅ + 3</text>
  <text x="430" y="422" text-anchor="middle" fill="#94a3b8" font-size="11.5">떼어낸 것이 x 하나뿐이라 대응하는 두 후보의 합은 정확히 x 만큼 차이 난다. 그래서 순위가 보존된다.</text>
</svg>
```

- [ ] **Step 3: `prefix-min.svg` 작성**

```svg
<svg viewBox="0 0 860 420" width="1290" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="ms-pm-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 Z" fill="#34d399"/>
    </marker>
  </defs>

  <rect width="860" height="420" rx="10" fill="#0f1117"/>

  <text x="430" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">누적합 꺾은선에서 낙차가 가장 큰 구간</text>
  <text x="430" y="51" text-anchor="middle" fill="#64748b" font-size="11">골짜기는 봉우리보다 왼쪽에 있어야 한다 · 여기서는 P₂ = −2 에서 P₈ = 7 까지</text>

  <!-- 0 기준선 -->
  <line x1="88" y1="234" x2="790" y2="234" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="80" y="238" text-anchor="end" fill="#64748b" font-size="10">0</text>

  <!-- 지금까지의 최소 mⱼ -->
  <path d="M110,234 H270 V278 H750" fill="none" stroke="#fbbf24" stroke-width="1.6" stroke-dasharray="5 4"/>

  <!-- 누적합 Pⱼ -->
  <polyline points="110,234 190,168 270,278 350,234 430,146 510,190 590,124 670,256 750,80"
            fill="none" stroke="#93c5fd" stroke-width="2"/>

  <g fill="#3b82f6" stroke="#93c5fd" stroke-width="1.4">
    <circle cx="110" cy="234" r="4"/>
    <circle cx="190" cy="168" r="4"/>
    <circle cx="350" cy="234" r="4"/>
    <circle cx="430" cy="146" r="4"/>
    <circle cx="510" cy="190" r="4"/>
    <circle cx="590" cy="124" r="4"/>
    <circle cx="670" cy="256" r="4"/>
  </g>
  <circle cx="270" cy="278" r="5.5" fill="#fbbf24" stroke="#fcd34d" stroke-width="1.4"/>
  <circle cx="750" cy="80" r="5.5" fill="#34d399" stroke="#6ee7b7" stroke-width="1.4"/>

  <!-- 값 라벨 -->
  <g fill="#93c5fd" font-size="10.5" text-anchor="middle">
    <text x="110" y="222">0</text>
    <text x="190" y="156">3</text>
    <text x="350" y="222">0</text>
    <text x="430" y="134">4</text>
    <text x="510" y="178">2</text>
    <text x="590" y="112">5</text>
    <text x="670" y="274">−1</text>
  </g>
  <text x="248" y="296" text-anchor="middle" fill="#fbbf24" font-size="11" font-weight="700">−2</text>
  <text x="732" y="70" text-anchor="middle" fill="#6ee7b7" font-size="11" font-weight="700">7</text>

  <!-- 낙차 -->
  <path d="M750,278 V80" fill="none" stroke="#34d399" stroke-width="1.6" marker-start="url(#ms-pm-arrow)" marker-end="url(#ms-pm-arrow)"/>
  <text x="768" y="176" text-anchor="start" fill="#34d399" font-size="15" font-weight="700">9</text>
  <text x="270" y="312" text-anchor="middle" fill="#fbbf24" font-size="10">지금까지의 최소</text>

  <!-- x축 라벨 -->
  <g fill="#64748b" font-size="10" text-anchor="middle">
    <text x="110" y="340">P₀</text>
    <text x="190" y="340">P₁</text>
    <text x="270" y="340">P₂</text>
    <text x="350" y="340">P₃</text>
    <text x="430" y="340">P₄</text>
    <text x="510" y="340">P₅</text>
    <text x="590" y="340">P₆</text>
    <text x="670" y="340">P₇</text>
    <text x="750" y="340">P₈</text>
  </g>

  <line x1="88" y1="358" x2="790" y2="358" stroke="#1e293b" stroke-width="1"/>

  <line x1="140" y1="380" x2="176" y2="380" stroke="#93c5fd" stroke-width="2"/>
  <text x="186" y="384" fill="#94a3b8" font-size="11">누적합 Pⱼ</text>
  <line x1="300" y1="380" x2="336" y2="380" stroke="#fbbf24" stroke-width="1.6" stroke-dasharray="5 4"/>
  <text x="346" y="384" fill="#94a3b8" font-size="11">지금까지의 최소 mⱼ</text>

  <text x="430" y="406" text-anchor="middle" fill="#94a3b8" font-size="11.5">각 j 에서 Pⱼ − mⱼ 를 재고, 그중 가장 큰 값이 답이다.</text>
</svg>
```

- [ ] **Step 4: SVG 파싱 검증**

```bash
python -c "import xml.dom.minidom,glob; [xml.dom.minidom.parse(f) for f in sorted(glob.glob('public/images/maximum-subarray-why-extend/*.svg'))]; print('svg ok', len(glob.glob('public/images/maximum-subarray-why-extend/*.svg')))"
```

Expected: `svg ok 2`

- [ ] **Step 5: 커밋**

```bash
git add public/images/maximum-subarray-why-extend
git commit -m "content(algo): 최대 부분배열 추가 설명 도판 2장"
```

---

### Task 4: 추가 설명 본문

**Files:**
- Create: `src/content/posts/maximum-subarray-why-extend.md`

**Interfaces:**
- Consumes: Task 3 의 두 SVG 경로, Task 2 가 만든 `/blog/maximum-subarray` 라우트.
- Produces: 라우트 `/blog/maximum-subarray-why-extend`. Task 2 의 본문이 이미 이 경로를 두 곳에서 참조한다.

- [ ] **Step 1: 본문 전체 작성**

`src/content/posts/maximum-subarray-why-extend.md` 를 아래 내용 그대로 만든다.

````markdown
---
title: "추가 설명 — 왜 이어 붙이는 것이 최선인가"
date: 2026-08-06T10:00:00
description: "최대 부분배열의 갱신식은 '앞부분의 최선은 kᵢ' 라는 한 줄을 당연하게 쓴다. 그 한 줄을 후보끼리의 1:1 대응으로 증명하고, 누적합에서 지금까지의 최소를 빼는 다른 풀이가 사실 같은 값을 계산한다는 것까지 보인다."
tags: ["Algorithm", "Maximum Subarray", "Kadane", "Prefix Sum", "추가 설명"]
category: algorithm
difficulty: 고급
numbered: true
---

> [최대 부분배열](/blog/maximum-subarray)은 자리마다 최선 하나만 들고 가면 된다고 했다. 이 글은 강의 노트 밖 확장으로, 그 갱신에 손해가 없는 이유를 증명하고 누적합 관점의 다른 풀이와 이어 붙인다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- **이어 붙이기가 최선인 이유**: 후보를 1:1로 대응시키는 논증
- **누적합으로 다시 보기**: 지금까지의 최소를 빼면 답이 나오는 이유
- **두 풀이는 같다**: $k_j = P_j - \min_{i \le j} P_i$ 를 귀납으로
- **훑기 세 번을 한 번으로**

</div>

기호는 본편 그대로다. 배열은 $a_1, \dots, a_N$, 누적합은 $P_0 = 0$, $P_j = a_1 + \cdots + a_j$, 그리고 $k_i$ 는 $a_i$ 에서 끝나는 부분배열의 최대 합이다. 빈 배열을 답으로 허용하는 정의를 계속 쓴다.

---

## 이어 붙이기가 최선인 이유

본편의 갱신식은 이렇다.

$$
k_{i+1} = \max(k_i + x,\; 0), \qquad x = a_{i+1}
$$

여기서 $k_i + x$ 를 "$a_{i+1}$ 에서 끝나고 $x$ 를 포함하는 부분배열의 최대 합"이라고 주장했다. 의심할 만한 지점이 있다. 앞부분을 $k_i$ 를 내는 그 부분배열로 고정해 버리면, 시작점을 다르게 잡았을 때 뒤에서 더 벌 기회를 놓치는 것 아닌가.

놓치지 않는다. 두 후보 집합이 정확히 대응하기 때문이다.

<div class="callout callout-key">
<div class="callout-title">주장</div>

$S_i$ 를 $a_i$ 에서 끝나는 부분배열의 집합이라 하고 빈 배열도 여기 넣는다. $T_{i+1}$ 을 $a_{i+1}$ 에서 끝나고 $a_{i+1}$ 을 포함하는 부분배열의 집합이라 하자. 그러면 $T_{i+1}$ 의 최대 합은 $k_i + x$ 다.

</div>

**증명.** $T_{i+1}$ 의 원소 하나를 잡으면 $a_s, \dots, a_{i+1}$ ($s \le i+1$) 꼴이다. 마지막 원소 $x$ 를 떼어내면 $a_s, \dots, a_i$ 가 남는다. $s \le i$ 면 이것은 $S_i$ 의 원소다. $s = i+1$ 이면 빈 배열이 남는데, 빈 배열도 $S_i$ 에 넣어 두었다. 거꾸로 $S_i$ 의 원소 뒤에 $x$ 를 붙이면 $T_{i+1}$ 의 원소가 된다. 두 연산은 서로의 역이므로 $S_i$ 와 $T_{i+1}$ 은 1:1로 대응한다.

대응하는 두 원소의 합은 정확히 $x$ 만큼 차이 난다. 떼어낸 것이 $x$ 하나뿐이기 때문이다. 곧 $S_i$ 에서 합이 $s$ 인 원소에 대응하는 $T_{i+1}$ 의 원소는 합이 $s + x$ 다. 모든 후보에 같은 값을 더하면 순위가 바뀌지 않으므로, $s$ 가 최대일 때 $s + x$ 도 최대다. $S_i$ 에서의 최대 합이 $k_i$ 이므로 $T_{i+1}$ 의 최대 합은 $k_i + x$ 다. $\blacksquare$

![S₅의 여섯 후보와 T₆의 여섯 후보를 화살표로 짝지은 표. 각 쌍의 합은 정확히 3만큼 차이 나고, 최댓값은 4에서 7로 옮겨간다.](/images/maximum-subarray-why-extend/extend.svg)

원문 노트는 이 사실을 "$k$ 배열의 시작점을 옮기면 반드시 $k$ 와 같거나 작은 값이 나온다"로 적었다. 같은 말이다. 시작점을 옮긴 배열도 $S_i$ 의 원소이고, $k_i$ 는 $S_i$ 전체의 최댓값이니 그보다 클 수 없다. 손해를 뒤에서 만회할 수 없는 이유는, 뒤에 붙는 것이 어느 후보에게나 똑같이 $x$ 하나뿐이라서다.

숫자로 확인해 보자. $i = 5$, $x = a_6 = 3$ 이다. $S_5$ 의 원소를 합과 함께 적으면 빈 배열 0, $[a_5]$ 는 $-2$, $[a_4 a_5]$ 는 2, $[a_3 a_4 a_5]$ 는 4, $[a_2 \dots a_5]$ 는 $-1$, $[a_1 \dots a_5]$ 는 2다. 최댓값 4는 $k_5$ 와 맞는다. 각각에 3을 더하면 $3, 1, 5, 7, 2, 5$ 이고 최댓값은 7이다. $k_6 = \max(4 + 3,\, 0) = 7$ 과 맞는다. 순서가 하나도 바뀌지 않았다는 점이 이 논증의 전부다.

---

## 누적합으로 다시 보기

전혀 다른 길로 가도 $O(N)$ 이 나온다. 본편의 누적합을 다시 쓴다. 앞머리 인덱스를 $i$ 로 두면

$$
a_{i+1} + a_{i+2} + \cdots + a_j = P_j - P_i
$$

부분배열 하나는 $0 \le i \le j \le N$ 인 쌍 $(i, j)$ 와 1:1로 대응한다. 두 경계를 고르는 것이 곧 부분배열을 고르는 것이고, $i = j$ 는 빈 배열이다. 따라서 답은

$$
\max_{0 \le i \le j \le N} (P_j - P_i)
$$

$j$ 를 고정하면 $P_j$ 는 상수이므로 $P_i$ 를 가장 작게 만들면 된다. 고를 수 있는 $i$ 는 $j$ 이하다.

$$
\text{답} = \max_{0 \le j \le N} \left( P_j - \min_{0 \le i \le j} P_i \right)
$$

$P$ 를 왼쪽에서 오른쪽으로 훑으면서 지금까지 본 최솟값을 들고 다니면 각 $j$ 의 항이 $O(1)$ 에 나온다. 원문 노트가 "사실 이게 답이 되는지는 모르겠다"고 남긴 방법인데, 위 두 줄이 그 근거다. 모든 부분배열이 $P_j - P_i$ 꼴이고 $j$ 마다 최선의 $i$ 를 고른 것뿐이라 빠뜨린 후보가 없다.

![누적합 P₀부터 P₈까지의 꺾은선과 지금까지의 최소를 나타내는 계단선. P₂ = −2에서 P₈ = 7까지의 낙차 9가 답이다.](/images/maximum-subarray-why-extend/prefix-min.svg)

그림으로 보면 누적합 꺾은선에서 낙차가 가장 큰 구간을 찾는 문제다. 왼쪽 어딘가의 골짜기에서 오른쪽 어딘가의 봉우리까지, 단 골짜기가 봉우리보다 왼쪽에 있어야 한다. 예시 배열에서는 $P_2 = -2$ 가 골짜기, $P_8 = 7$ 이 봉우리이고 낙차는 9다.

$\min$ 의 범위가 $i < j$ 가 아니라 $i \le j$ 라는 점을 눈여겨볼 만하다. $i = j$ 를 허용하는 것이 곧 빈 배열을 허용하는 것이고, 그래서 이 식의 값은 항상 0 이상이다. 빈 배열을 허용하지 않으려면 $i < j$ 로 좁히면 된다. 그러면 $j$ 는 1부터 시작하고 최솟값은 $P_0, \dots, P_{j-1}$ 중에서 고른다.

---

## 두 풀이는 같다

두 방법이 우연히 같은 답을 내는 것이 아니다. 매 자리에서 같은 값을 계산한다.

<div class="callout callout-key">
<div class="callout-title">주장</div>

모든 $j$ 에 대해 $k_j = P_j - \min_{0 \le i \le j} P_i$.

</div>

**증명.** $m_j = \min_{0 \le i \le j} P_i$ 로 두고 $j$ 에 대한 귀납법을 쓴다.

$j = 0$ 일 때 $k_0 = 0$ 이고 $P_0 - m_0 = 0 - 0 = 0$ 이므로 성립한다.

$j$ 에서 성립한다고 가정하고 $j+1$ 을 보자. $x = a_{j+1}$ 이라 하면 $P_{j+1} = P_j + x$ 이고 $m_{j+1} = \min(m_j,\, P_{j+1})$ 이다.

$$
P_{j+1} - m_{j+1} = P_{j+1} - \min(m_j,\; P_{j+1}) = \max(P_{j+1} - m_j,\; 0)
$$

두 번째 등호는 $-\min(u, v) = \max(-u, -v)$ 에서 나온다. 이어서 $P_{j+1} - m_j = (P_j - m_j) + x$ 이고, 귀납 가정에 따라 $P_j - m_j = k_j$ 이므로

$$
P_{j+1} - m_{j+1} = \max(k_j + x,\; 0) = k_{j+1}
$$

본편의 갱신식 그대로다. $\blacksquare$

예시로 확인해 보자. $P_0 \dots P_8 = 0,\, 3,\, -2,\, 0,\, 4,\, 2,\, 5,\, -1,\, 7$ 이고 $m_0 \dots m_8 = 0,\, 0,\, -2,\, -2,\, -2,\, -2,\, -2,\, -2,\, -2$ 다. 차를 나열하면 $0,\, 3,\, 0,\, 2,\, 6,\, 4,\, 7,\, 1,\, 9$ 이고, 본편의 $k_0 \dots k_8$ 과 정확히 겹친다.

카데인은 $k_j$ 를 직접 굴린다. 누적합 풀이는 $P_j$ 와 $m_j$ 를 따로 들고 다니다 마지막에 뺀다. 들고 다니는 값의 개수만 다르고 계산하는 것은 같다.

---

## 훑기 세 번을 한 번으로

원문 노트는 누적합 풀이에 "prefix sum, prefix minimum, 빼는 과정까지 총 3번을 탐색"해야 한다고 적었다. 세 번 훑어도 $O(N)$ 이라 복잡도는 같다. 한 번으로 합칠 수도 있다.

```cpp
// 누적합 관점의 O(N).  배열을 한 번만 지나간다.
long long maxSubarrayPrefix(const vector<int>& a) {
    long long p = 0, m = 0, best = 0;   // p: 누적합, m: 지금까지의 최소 누적합
    for (int x : a) {
        p += x;
        best = max(best, p - m);        // 이 자리에서 끝나는 최선
        m = min(m, p);                  // 다음 자리를 위해 최솟값 갱신
    }
    return best;
}
```

`m` 을 갱신하기 전에 `p - m` 을 읽는 순서가 걱정될 수 있다. 이 자리에서 쓰는 최솟값은 $m_j$ 가 아니라 $m_{j-1}$ 이기 때문이다. 문제가 없는 이유는 `best` 가 항상 0 이상이라서다. $P_j - m_{j-1}$ 이 음수라면 $P_j$ 자신이 새 최솟값이 되어 $P_j - m_j = 0$ 인데, 0은 이미 `best` 에 반영되어 있다. 두 경우 모두 `best` 는 올바른 값을 유지한다.

본편의 카데인 코드와 나란히 놓으면 변수 이름만 다르다. 앞 절의 증명이 그 사실을 말해 준다.

---

## 마치며

본편이 넘긴 두 질문에 답했다. 갱신식이 옳은 이유는 후보 집합이 1:1로 대응하고 모든 후보에 같은 값이 더해져 순위가 보존되기 때문이다. 누적합에서 지금까지의 최소를 빼는 풀이가 옳은 이유는 모든 부분배열이 두 경계의 차이로 표현되기 때문이다.

두 답은 결국 한 식으로 모인다. $k_j = P_j - \min_{i \le j} P_i$. 서로 다른 두 관점에서 출발해 같은 자리에 도착하는 일은 흔하다. 도착점이 같다는 사실을 확인하고 나면, 둘 중 편한 쪽을 골라 쓰면 된다.

[← 최대 부분배열](/blog/maximum-subarray)
````

- [ ] **Step 2: 빌드 검증**

```bash
npm run build
```

Expected: 오류 없이 종료. 페이지 수가 Task 2 대비 1 늘어난다.

- [ ] **Step 3: 결정적 검사 (두 편 모두)**

```bash
python .claude/review_post.py src/content/posts/maximum-subarray.md src/content/posts/maximum-subarray-why-extend.md
```

Expected: `발견 사항 없음 ✅`

- [ ] **Step 4: 링크 왕복 확인**

```bash
grep -n "maximum-subarray-why-extend" src/content/posts/maximum-subarray.md
grep -n "blog/maximum-subarray)" src/content/posts/maximum-subarray-why-extend.md
```

Expected: 앞 명령은 2줄(자리마다 최선 하나 절, 더 나가면 절), 뒤 명령은 2줄(도입 blockquote, 마지막 돌아가기 링크).

- [ ] **Step 5: 커밋**

```bash
git add src/content/posts/maximum-subarray-why-extend.md
git commit -m "content(algo): 최대 부분배열 추가 설명"
```

---

### Task 5: 리뷰와 반영

**Files:**
- Create: `docs/reviews/2026-08-06-maximum-subarray.md`
- Modify: `src/content/posts/maximum-subarray.md`, `src/content/posts/maximum-subarray-why-extend.md` (지적 반영 시)

**Interfaces:**
- Consumes: Task 2·4 의 두 포스트.
- Produces: 리뷰 리포트와 반영 결과. PR 본문이 이 리포트를 근거로 삼는다.

- [ ] **Step 1: `/review-post maximum-subarray` 실행**

결정적 검사와 LLM 비평 L1~L7 을 돌린다. L7(논증·복잡도)에서는 아래를 실제 값으로 검증한다.

- $k$ 수열 `3, 0, 2, 6, 4, 7, 1, 9` 가 갱신식과 맞는가
- 비허용 정의의 $k$ 수열 `3, -2, 2, 6, 4, 7, 1, 9` 가 맞는가
- $P_j - m_j$ 수열이 $k_j$ 와 일치하는가
- 부분배열 개수 $N(N+1)/2 = 36$ 이 맞는가
- `maxSubarrayPrefix` 의 `best` 갱신과 `m` 갱신 순서가 옳은가

- [ ] **Step 2: `/review-post maximum-subarray-why-extend` 실행**

- [ ] **Step 3: 지적 반영 후 재검증**

```bash
python .claude/review_post.py src/content/posts/maximum-subarray.md src/content/posts/maximum-subarray-why-extend.md
npm run build
```

Expected: `발견 사항 없음 ✅` 와 빌드 성공.

- [ ] **Step 4: 리포트에 "반영 결과" 섹션 추가하고 커밋**

```bash
git add docs/reviews/2026-08-06-maximum-subarray.md src/content/posts
git commit -m "content(algo): 최대 부분배열 리뷰 반영"
```

---

### Task 6: PR

**Files:**
- 없음 (커밋 푸시와 PR 생성만)

**Interfaces:**
- Consumes: Task 1~5 의 모든 커밋.
- Produces: `feat/post-maximum-subarray` → `main` PR.

- [ ] **Step 1: 푸시**

```bash
git push -u origin feat/post-maximum-subarray
```

- [ ] **Step 2: PR 생성**

제목: `feat(algo): 최대 부분배열 본편 + 추가 설명`

본문 규칙은 사용자 지침을 따른다. **Why 는 길게** 쓴다. 원문 노트가 세 가지 $O(N)$ 아이디어를 나열만 하고 두 곳에 물음표를 남긴 상태였다는 점, 부분배열 개수 수식이 틀려 있었다는 점, 그래서 노트를 그대로 옮기면 독자가 "왜 그 갱신이 옳은가"를 답 없이 넘겨야 한다는 점을 배경으로 쓴다. **How 는 방법론 중심**으로 쓴다. 파일 경로나 함수명 대신 "개선 서사와 정당성 논증의 분리", "후보 집합의 1:1 대응으로 교환 논증 대체", "두 관점을 하나의 등식으로 수렴" 같은 설계 원칙으로 서술한다. 구체적 위치는 마지막 '참조 코드 위치' 섹션에만 둔다.

PR 본문 끝에 `🤖 Generated with [Claude Code](https://claude.com/claude-code)` 를 넣는다. 커밋에는 `Co-Authored-By` 트레일러를 넣지 않는다.

---

## Self-Review

**1. 스펙 커버리지**

| 스펙 항목 | 담당 |
|---|---|
| 원문 6개 줄기 (문제·N³·N²·Idea 1·2·3) | Task 2 (문제~포함/미포함), Task 4 (Idea 3) |
| `N(N-1)/2` → `N(N+1)/2` 정정, 두 셈법 보존 | Task 2 「모두 세어 보기」 |
| 빈 배열 허용·비허용 두 갈래 | Task 2 「자리마다 최선 하나」·「빈 배열을 허용하지 않으면」 |
| `[-3,-1,-2]` 반례 | Task 2 |
| Idea 2 = 카데인 + 전역 최댓값 | Task 2 「포함하는가, 포함하지 않는가」 |
| 1:1 대응 논증 | Task 4 「이어 붙이기가 최선인 이유」 |
| Idea 3 정당성 | Task 4 「누적합으로 다시 보기」 |
| `k_j = P_j - min_{i≤j} P_i` 귀납 증명 | Task 4 「두 풀이는 같다」 |
| 훑기 3번 → 1번 | Task 4 「훑기 세 번을 한 번으로」 |
| dp-2 연결 | Task 2 「포함하는가, 포함하지 않는가」 |
| 도판 5장 | Task 1 (3장), Task 3 (2장) |
| 복잡도 모듈 (시간·공간, 최악 기준) | Task 2 각 절 말미 |
| 계산 예시 모듈 | Task 2·4 본문의 수열, Task 5 Step 1 검증 목록 |
| 증명 모듈 | Task 4 두 증명 |
| SVG 모듈 | Task 1 Step 5, Task 3 Step 4, Task 5 |
| 빌드 통과 | Task 2 Step 2, Task 4 Step 2 |

빠진 항목 없음.

**2. 플레이스홀더 스캔**

본문과 SVG 전체를 인라인으로 담았다. "적절히", "비슷하게", "TBD" 없음. Task 5 의 리뷰 지적 반영만 실행 시점에 내용이 정해지는데, 이는 리뷰 결과에 의존하는 성질상 불가피하며 검증 명령과 기대 출력은 명시했다.

**3. 이름·값 일관성**

- 슬러그 `maximum-subarray`, `maximum-subarray-why-extend` 가 파일명·이미지 디렉터리·링크·grep 명령에서 모두 일치한다.
- SVG 파일명 `problem`, `prefix-sum`, `kadane-scan`, `extend`, `prefix-min` 이 생성 스텝과 본문 `![]()` 경로에서 일치한다.
- 함수명 `maxSubarray`, `maxSubarrayNonEmpty`, `maxSubarrayPrefix` 가 서로 겹치지 않는다.
- 기호 `k_i`, `P_j`, `m_j`, `S_i`, `T_{i+1}`, `x = a_{i+1}` 이 두 편에서 같은 뜻으로 쓰인다.
- 수치 `0,3,-2,0,4,2,5,-1,7` (P), `3,0,2,6,4,7,1,9` (k), `3,-2,2,6,4,7,1,9` (비허용 k), `0,0,-2,…` (m), 36, 9 가 본문·SVG·스펙에서 모두 같다.
- SVG marker id 가 파일마다 다르다 (`ms-ps-arrow`, `ms-ex-arrow`, `ms-ex-arrow-hi`, `ms-pm-arrow`). 한 페이지에 두 SVG 가 들어가도 충돌하지 않는다.
