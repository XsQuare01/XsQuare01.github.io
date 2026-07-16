# 블로그 UI 리프레시 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 블로그를 "기계는 터미널로, 사람은 논문으로" 주장에 맞춰 다크 터미널 크롬 + 라이트 논문 본문으로 재설계한다.

**Architecture:** 단일 전역 스타일시트(`global.css`)의 토큰과 컴포넌트를 개편하고, 두 레이아웃(`BaseLayout`·`PostLayout`)의 마크업을 조정한다. 포스트 마크다운과 156개 SVG는 건드리지 않는다 — 다이어그램/코드는 다크 "플레이트"에 담겨 그대로 재사용된다. 사용자 테마 토글은 제거하고 영역별 고정 이중 톤으로 간다.

**Tech Stack:** Astro 6, 전역 CSS(`src/styles/global.css`), rehype 플러그인(`astro.config.mjs`), Shiki 듀얼테마, Google Fonts(Nanum Myeongjo 다이나믹 서브셋).

## Global Constraints

- 스펙 원본: `docs/superpowers/specs/2026-07-16-ui-refresh-design.md` (모든 결정의 근거).
- 포스트 마크다운(`src/content/posts/*.md`)과 SVG(`public/images/**`)는 **변경 금지**.
- 커밋 메시지에 **Co-Authored-By 트레일러 넣지 않음** (블로그 저장소 규칙).
- 브랜치: `design/ui-refresh` (이미 체크아웃됨). main 직접 커밋 금지.
- 액센트는 **앰버/테라코타 단색**. 3색(orange/sky/violet) 채도 액센트 금지.
- 제거 대상: 사용자 light/dark 토글, `html.light` 오버라이드, radial-gradient 배경 blob, hover 글로우, staggered fadeInUp, gradient accent bar.
- 색 토큰(정확값):
  - `--paper:#faf8f3` `--ink:#22201b` `--ink-soft:#5c574d` `--ink-faint:#918a7b` `--rule:#e2dccf`
  - `--amber:#b56a1a` `--amber-soft:rgba(181,106,26,.10)` `--term-amber:#d99b4e`
  - `--term-bg:#15171c` `--term-fg:#cdd3cc` `--term-dim:#6a7069` `--term-green:#6fc07a`
- 폰트 토큰:
  - `--serif:'Nanum Myeongjo', Georgia, 'Times New Roman', serif`
  - `--mono:'JetBrains Mono','Cascadia Code','SF Mono',Consolas,monospace`
  - `--sans:'Pretendard',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif`
- 검증: 각 태스크는 `npm run build` 성공 + `npm run dev`(http://localhost:4321) 육안 확인으로 끝낸다. CSS/시각 작업이라 유닛 테스트 대신 빌드+육안이 검증 루프다.
- `prefers-reduced-motion: reduce`에서 커서 깜빡임·전환 비활성.

---

### Task 1: 디자인 토큰 · 웹폰트 · 라이트모드/토글 제거 (기반)

새 색·폰트 토큰을 심고, 웹폰트를 로드하고, 사용자 테마 토글과 모든 `html.light` 코드를 제거한다. 읽는 표면(body/main)을 종이색으로 전환한다.

**Files:**
- Modify: `src/styles/global.css` (`:root`, `html.light`, `body`, `::selection`, `:focus-visible`, `/* ── Theme Toggle ── */`, `/* ── Light Mode Overrides ── */` 섹션)
- Modify: `src/layouts/BaseLayout.astro` (head: 폰트 link + preconnect; inline 테마 초기화 스크립트 제거; `theme-color` meta; theme-toggle 버튼 마크업 제거; 하단 `theme-toggle` JS 제거; `<html>`의 `color-scheme`)

**Interfaces:**
- Produces: 전역 CSS 변수(위 Global Constraints의 토큰 전체). 이후 모든 태스크가 이 변수를 사용.

- [ ] **Step 1: 웹폰트 로드 + preconnect 추가**

`BaseLayout.astro` head에서 KaTeX `<link>`(112행 부근) 바로 위에 추가:

```html
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&display=swap" />
```

> Google Fonts CSS2는 Nanum Myeongjo를 unicode-range로 분할 제공(= 다이나믹 서브셋). `display=swap`으로 렌더 블로킹 없음. 빌드 후 dev에서 네트워크 탭으로 woff2가 범위별로 로드되는지 확인.

- [ ] **Step 2: 테마 초기화 인라인 스크립트 제거**

`BaseLayout.astro` 103–111행의 `<script is:inline>` (localStorage 'theme' 읽어 `html.light` 붙이는 블록) 전체 삭제.

- [ ] **Step 3: `<html>` color-scheme + theme-color 고정**

59행 `<html lang="ko" style="color-scheme: dark light">` → `<html lang="ko" style="color-scheme: light">`.
63행 `<meta name="theme-color" content="#0f1117" />` → `<meta name="theme-color" content="#15171c" />` (다크 크롬 기준).

- [ ] **Step 4: 사이드바 테마 토글 버튼 마크업 제거**

`BaseLayout.astro` 203–225행 `.sidebar-footer` 안의 `<button id="theme-toggle" ...>...</button>` 전체 삭제. `.sidebar-footer`의 `© {year}` div는 남긴다.

- [ ] **Step 5: 테마 토글 JS 제거**

`BaseLayout.astro` 하단 script의 413–416행 `document.getElementById('theme-toggle')?.addEventListener(...)` 블록 삭제.

- [ ] **Step 6: `:root` 토큰 교체**

`global.css` 20–36행 `:root { ... }` 를 아래로 교체:

```css
:root {
  --paper: #faf8f3;
  --ink: #22201b;
  --ink-soft: #5c574d;
  --ink-faint: #918a7b;
  --rule: #e2dccf;

  --amber: #b56a1a;
  --amber-soft: rgba(181, 106, 26, 0.10);
  --term-amber: #d99b4e;

  --term-bg: #15171c;
  --term-fg: #cdd3cc;
  --term-dim: #6a7069;
  --term-green: #6fc07a;

  /* 하위 호환 별칭: 기존 셀렉터가 참조하던 이름 → 새 팔레트로 매핑 */
  --bg: var(--paper);
  --bg-card: #f1ece0;
  --bg-hover: rgba(34, 32, 27, 0.05);
  --text: var(--ink);
  --text-muted: var(--ink-soft);
  --text-dim: var(--ink-faint);
  --border: var(--rule);
  --accent: var(--amber);
  --accent-dim: var(--amber-soft);
  --accent-2: var(--amber);
  --accent-3: var(--amber);

  --sidebar-width: 224px;
  --font-sans: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-serif: 'Nanum Myeongjo', Georgia, 'Times New Roman', serif;
  --font-mono: 'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace;
}
```

> `--accent-2/3`을 모두 `--amber`로 별칭 처리해, 기존에 sky/violet을 참조하던 셀렉터가 자동으로 단색 액센트가 된다. 후속 태스크에서 개별 셀렉터를 다듬는다.

- [ ] **Step 7: `html.light` 블록 제거**

`global.css` 38–51행 `html.light { ... }` 전체 삭제.

- [ ] **Step 8: base 타이포/배경 종이화**

53–61행 `html { ... }` 에서 `background: var(--bg);`는 종이색을 가리키므로 유지. `font-family: var(--font-sans);` 유지(UI 기본).
74–79행 `body { ... }`의 `background-image: radial-gradient(...)` 두 줄 **삭제**(AI 티 제거). `body`는 `display:flex; min-height:100vh;`만 남긴다.
4–11행 `::selection`/`::-moz-selection`의 `background: rgba(249,115,22,.25)` → `background: var(--amber-soft)`.
15행 `:focus-visible outline: 2px solid rgba(249,115,22,.6)` → `outline: 2px solid var(--amber)`.

- [ ] **Step 9: Theme Toggle / Light Mode Overrides CSS 섹션 제거**

`global.css`의 `/* ── Theme Toggle ── */` 섹션(268–306행)과 `/* ── Light Mode Overrides ── */` 섹션(308–348행) 전체 삭제. (해당 마크업/스크립트는 Step 4–5에서 제거됨.)

- [ ] **Step 10: 빌드 + 육안 검증**

Run: `npm run build`
Expected: 에러 없이 완료.
Run: `npm run dev` 후 http://localhost:4321 열기.
Expected: 배경이 종이색(#faf8f3), 방사 그라디언트 사라짐, 사이드바에 테마 토글 버튼 없음, 콘솔 에러 없음. (사이드바는 아직 라이트 — Task 2에서 다크화.)

- [ ] **Step 11: 커밋**

```bash
git add src/styles/global.css src/layouts/BaseLayout.astro
git commit -m "refactor(ui): 디자인 토큰·웹폰트 교체, 라이트모드/테마토글 제거"
```

---

### Task 2: 사이드바 → 터미널 크롬

사이드바를 다크 터미널로 재스타일. 프로필을 `user@host` 프롬프트로, 네비를 파일 경로 스타일로, 활성 항목을 앰버로.

**Files:**
- Modify: `src/layouts/BaseLayout.astro` (`.sidebar-profile` 내부 마크업 — 아바타/이름/바이오 → 터미널 헤더)
- Modify: `src/styles/global.css` (`/* ── Sidebar ── */` 섹션 85–266행)

**Interfaces:**
- Consumes: Task 1의 `--term-*`, `--amber`, `--font-mono`.

- [ ] **Step 1: 사이드바 프로필 마크업을 터미널 헤더로**

`BaseLayout.astro` 153–157행 `.sidebar-profile` 블록을 교체:

```html
    <div class="sidebar-profile">
      <div class="term-prompt"><span class="term-user">xsquare</span><span class="term-dim">@blog</span></div>
      <div class="sidebar-name">~/algorithms</div>
      <div class="sidebar-bio">정리하고 기록하는 개발자</div>
    </div>
```

(아바타 `<img>`는 제거 — 터미널 헤더에는 부적합. GitHub 아바타는 OG 이미지로 계속 쓰이므로 자산 자체는 유지.)

- [ ] **Step 2: 사이드바 셀렉터 재스타일**

`global.css` 85–99행 `.sidebar`에 다크 배경/모노 적용. 아래 선언을 반영(기존 값 위에 덮어쓰기):

```css
.sidebar {
  width: var(--sidebar-width);
  min-height: 100vh;
  background: var(--term-bg);
  border-right: 1px solid #23262e;
  position: fixed;
  top: 0; left: 0;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1.1rem;
  overflow-y: auto;
  z-index: 100;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--term-fg);
}
```

- [ ] **Step 3: 프로필/헤더 요소 스타일**

101–130행 `.sidebar-profile`/`.sidebar-avatar`/`.sidebar-name`/`.sidebar-bio` 를 교체:

```css
.sidebar-profile { margin-bottom: 1.25rem; padding-bottom: 0.9rem; border-bottom: 1px solid #23262e; }
.term-prompt { font-size: 0.82rem; }
.term-user { color: var(--term-green); }
.term-dim { color: var(--term-dim); }
.sidebar-name { font-size: 0.9rem; font-weight: 700; color: #eef3ee; margin-top: 2px; }
.sidebar-bio { font-size: 0.72rem; color: var(--term-dim); margin-top: 0.3rem; line-height: 1.5; }
/* .sidebar-avatar 규칙(108–116행)은 마크업 제거로 미사용 → 삭제 */
```

- [ ] **Step 4: 네비/카테고리/태그 라벨 + 링크 터미널화**

139–257행의 네비 관련 규칙에서 색을 터미널 팔레트로 조정. 핵심 교체:

```css
.sidebar-nav-label { font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: var(--term-dim); margin: 0.9rem 0 0.4rem; }
.sidebar-nav a, .sidebar-category-link { color: var(--term-fg); }
.sidebar-nav a:hover, .sidebar-category-link:hover { background: rgba(255,255,255,0.04); color: #fff; }
.sidebar-nav a.active, .sidebar-category-link.active { color: var(--term-amber); background: transparent; }
.sidebar-nav a.active::before { content: '▸ '; }
.sidebar-category-count { color: var(--term-dim); }
.sidebar-tags .tag { color: var(--term-amber); border: 1px solid #3a3f37; background: transparent; }
.sidebar-tags .tag:hover { background: rgba(217,155,78,0.12); }
.sidebar-footer { color: var(--term-dim); }
```

기존 `.sidebar-nav a` 규칙의 gradient/border-left 슬라이드(157–178행 transition·border-color) 및 hover 글로우 관련 선언은 제거하고 위 단순 규칙으로 대체.

- [ ] **Step 5: 검색 버튼(#search-btn) 터미널화**

`#search-btn` 규칙을 찾아(검색 시 `search-btn`) 배경/보더를 터미널 톤으로: `background: transparent; border: 1px solid #3a3f37; color: var(--term-fg);` hover 시 `background: rgba(255,255,255,0.04)`. `kbd`는 `color: var(--term-dim); border-color:#3a3f37`.

- [ ] **Step 6: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, 홈 열기.
Expected: 사이드바가 다크 터미널(모노), `xsquare@blog` 프롬프트(green), `~/algorithms`, 활성 메뉴 앰버 `▸`, 종이 본문과 대비. 아바타 없음.

- [ ] **Step 7: 커밋**

```bash
git add src/styles/global.css src/layouts/BaseLayout.astro
git commit -m "feat(ui): 사이드바를 터미널 크롬으로 재설계"
```

---

### Task 3: 본문 타이포그래피 → 논문 (Prose)

`.prose`를 종이 위 세리프 논문으로. 섹션 헤딩의 gradient bar를 모노 앰버 `##` 접두사로 교체.

**Files:**
- Modify: `src/styles/global.css` (`/* ── Prose ── */` 섹션 563–705행 범위)

**Interfaces:**
- Consumes: `--serif`, `--ink`, `--amber`, `--rule`.

- [ ] **Step 1: 본문 기본 세리프화**

564행 `.prose { color: var(--text); }` 및 591–594행 문단/리스트를 교체:

```css
.prose { color: var(--ink); font-family: var(--font-serif); font-size: 1.04rem; line-height: 1.75; }
.prose p { margin-bottom: 1.2rem; }
.prose ul, .prose ol { padding-left: 1.5rem; margin-bottom: 1.2rem; }
.prose li { margin-bottom: 0.4rem; }
.prose li::marker { color: var(--amber); }
```

- [ ] **Step 2: h2 gradient bar → 모노 `##` 접두사**

565–588행 `.prose h2`와 `.prose h2::before`를 교체:

```css
.prose h2 {
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin: 2.4rem 0 1rem;
  color: var(--ink);
  scroll-margin-top: 1.5rem;
}
.prose h2::before {
  content: '##';
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 400;
  color: var(--amber);
  margin-right: 0.55rem;
  vertical-align: 0.18em;
}
```

- [ ] **Step 3: h3/h4 단색화**

589–590행 교체(sky/violet 제거):

```css
.prose h3 { font-family: var(--font-serif); font-size: 1.18rem; font-weight: 600; margin: 2rem 0 0.6rem; color: var(--ink); }
.prose h4 { font-family: var(--font-serif); font-size: 1rem; font-weight: 700; margin: 1.5rem 0 0.4rem; color: var(--ink-soft); }
```

- [ ] **Step 4: 링크·blockquote·hr·표·strong 종이화**

```css
.prose a { color: var(--amber); border-bottom: 1px solid rgba(181,106,26,0.35); }
.prose a:hover { border-bottom-color: var(--amber); }
.prose blockquote { border-left: 3px solid var(--rule); padding-left: 1rem; margin: 1.4rem 0; color: var(--ink-soft); font-style: italic; }
.prose hr { border: none; border-top: 1px solid var(--rule); margin: 2.5rem 0; }
.prose th { background: var(--bg-card); font-weight: 700; color: var(--ink); }
.prose th, .prose td { border: 1px solid var(--rule); padding: 0.6rem 0.9rem; }
.prose tr:hover td { background: var(--bg-hover); }
.prose strong { color: var(--ink); font-weight: 700; }
```

(602–603행 `.prose blockquote > * { margin:0 }` 유지. 700–705행의 표/strong/a 규칙을 위 값으로 덮어쓰기.)

- [ ] **Step 5: 인라인 code 종이 위 스타일**

603–611행 `.prose code`(인라인)를 종이 위에서 읽히도록:

```css
.prose code {
  font-family: var(--font-mono);
  font-size: 0.86em;
  background: #efe9dc;
  color: #7a3f12;
  padding: 0.12em 0.38em;
  border-radius: 4px;
}
```

(블록 코드 `.prose pre code`는 Task 5에서 처리하므로 여기선 인라인만.)

- [ ] **Step 6: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, `/blog/convex-hull-5` 열기.
Expected: 본문이 명조 세리프, 섹션 제목 앞 앰버 `##`, 링크 앰버, 인라인 코드 종이 위에서 읽힘. (코드 블록/이미지/콜아웃은 다음 태스크들에서.)

- [ ] **Step 7: 커밋**

```bash
git add src/styles/global.css
git commit -m "feat(ui): 본문을 논문(세리프)으로, 섹션 헤딩 ## 접두사"
```

---

### Task 4: 정리/콜아웃 블록 + 여백 노트

포스트에서 쓰는 `.callout`을 앰버 룰 정리 블록으로. 미래 포스트용 `.margin-note` 캡처 스타일 추가(기존 포스트 retrofit 없음).

**Files:**
- Modify: `src/styles/global.css` (`.callout` 관련 규칙 — 검색으로 위치 확인; 없으면 `/* ── Prose ── */` 끝에 추가)

**Interfaces:**
- Consumes: `--amber`, `--amber-soft`, `--font-mono`, `--font-serif`.

- [ ] **Step 1: 현재 callout 규칙 확인**

Run: `grep -n "callout" src/styles/global.css`
기존 `.callout`, `.callout-title` 규칙 위치를 파악.

- [ ] **Step 2: callout → 정리 블록 재스타일**

기존 `.callout`/`.callout-title` 규칙을 교체:

```css
.callout {
  border-left: 3px solid var(--amber);
  background: var(--amber-soft);
  padding: 0.9rem 1.1rem;
  margin: 1.5rem 0;
  border-radius: 0 5px 5px 0;
  font-family: var(--font-serif);
}
.callout > *:last-child { margin-bottom: 0; }
.callout-title {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 0.4rem;
}
```

- [ ] **Step 3: 여백 노트 캡처 스타일 추가**

`.callout` 규칙 아래에 추가:

```css
.margin-note {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--ink-faint);
  line-height: 1.5;
  border-left: 2px solid var(--rule);
  padding: 0.1rem 0 0.1rem 0.8rem;
  margin: 0.8rem 0;
}
@media (min-width: 1200px) {
  .prose { position: relative; }
  .margin-note { position: absolute; right: -180px; width: 160px; border-left: none; border-top: 1px solid var(--rule); padding: 0.4rem 0 0; }
}
```

> 기존 포스트는 `.margin-note`를 쓰지 않으므로 시각 변화 없음(캡처만 준비). 향후 포스트에서 `<p class="margin-note">…</p>`로 사용.

- [ ] **Step 4: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, `/blog/convex-hull-5`의 "이 포스트에서 다루는 내용" callout 확인.
Expected: 앰버 왼쪽 룰 + 연한 앰버 배경, 라벨이 모노 대문자 앰버.

- [ ] **Step 5: 커밋**

```bash
git add src/styles/global.css
git commit -m "feat(ui): 콜아웃을 정리 블록으로, 여백 노트 캡처 추가"
```

---

### Task 5: 코드 블록 → 터미널 카드

블록 코드를 종이 위에 박힌 다크 터미널 카드로. 라이트모드 제거로 코드는 항상 다크(Shiki dark). 복사 버튼 유지.

**Files:**
- Modify: `src/styles/global.css` (`.prose pre`, `.prose pre code`, `.astro-code` 규칙 612–638행, `.code-copy-btn`)

**Interfaces:**
- Consumes: `--term-bg`, `--term-fg`, `--font-mono`.

- [ ] **Step 1: 코드가 항상 다크가 되도록 Shiki 매핑 고정**

631–638행을 교체(라이트 오버라이드 삭제):

```css
.astro-code,
.astro-code span {
  color: var(--shiki-dark) !important;
  background-color: transparent !important;
}
```

(`html.light .astro-code` 블록은 삭제.)

- [ ] **Step 2: pre 카드화**

612–630행 `.prose pre`/`.prose pre code`를 교체:

```css
.prose pre {
  background: var(--term-bg);
  color: var(--term-fg);
  font-family: var(--font-mono);
  font-size: 0.84rem;
  line-height: 1.7;
  border-radius: 8px;
  padding: 1rem 1.1rem;
  margin: 1.6rem 0;
  overflow-x: auto;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
  border: 1px solid #23262e;
}
.prose pre code {
  background: transparent;
  color: inherit;
  padding: 0;
  font-size: inherit;
}
```

- [ ] **Step 3: 복사 버튼 톤 조정**

`.code-copy-btn` 규칙을 찾아 다크 카드 위에서 읽히도록: `background: rgba(255,255,255,0.07); color: var(--term-fg); border: 1px solid #3a3f37;` hover `background: rgba(255,255,255,0.14)`. `.code-copy-btn.copied` 는 `color: var(--term-green)`.

- [ ] **Step 4: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, 코드가 있는 포스트(예: `/blog/convex-hull-4`) 열기.
Expected: 코드 블록이 다크 터미널 카드(둥근 모서리+미세 그림자), 종이 본문과 대비. 하이라이팅 색 유지. 복사 버튼 동작.

- [ ] **Step 5: 커밋**

```bash
git add src/styles/global.css
git commit -m "feat(ui): 코드 블록을 다크 터미널 카드로"
```

---

### Task 6: 다이어그램 → 다크 플레이트 + figure 캡션

본문 이미지를 다크 플레이트에 담아 기존 다크 SVG를 그대로 살린다. rehype 플러그인으로 `img`(alt 있음)을 `figure > img + figcaption`으로 감싸 alt를 캡션으로 렌더.

**Files:**
- Modify: `astro.config.mjs` (rehype 플러그인 추가)
- Modify: `src/styles/global.css` (`.prose img`, `figure`, `figcaption`)
- Modify: `src/layouts/PostLayout.astro` (라이트박스 셀렉터가 `figure img`도 잡는지 확인 — 이미 `.prose img`라 유지됨)

**Interfaces:**
- Consumes: `--term-bg`, `--ink-faint`, `--rule`.
- Produces: `rehypeFigureCaption` (alt 텍스트를 가진 `img`를 figure로 감싸는 rehype 플러그인).

- [ ] **Step 1: figure 캡션 rehype 플러그인 추가**

`astro.config.mjs`의 `rehypeLazyImages` 함수 아래에 추가:

```js
// 본문 이미지(alt 있음)를 figure+figcaption으로 감싸 다크 플레이트 + 캡션 렌더
function rehypeFigureCaption() {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.flatMap((child) => {
        if (
          child.tagName === 'p' &&
          child.children &&
          child.children.length === 1 &&
          child.children[0].tagName === 'img' &&
          child.children[0].properties &&
          child.children[0].properties.alt
        ) {
          const img = child.children[0];
          return [{
            type: 'element', tagName: 'figure', properties: { className: ['post-figure'] },
            children: [
              img,
              { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: img.properties.alt }] },
            ],
          }];
        }
        walk(child);
        return [child];
      });
    };
    walk(tree);
  };
}
```

`rehypePlugins` 배열을 `[rehypeKatex, rehypeLazyImages, rehypeFigureCaption]`로 수정(55행).

- [ ] **Step 2: 이미지/figure 플레이트 스타일**

640–641행 `.prose img` 및 `:hover`를 교체:

```css
.post-figure {
  margin: 1.8rem 0;
  background: var(--term-bg);
  border: 1px solid #23262e;
  border-radius: 10px;
  padding: 1rem 1rem 0.5rem;
  box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}
.prose img { max-width: 100%; display: block; margin: 0 auto; border-radius: 4px; cursor: zoom-in; }
.prose figcaption {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--ink-faint);
  text-align: center;
  margin-top: 0.7rem;
  line-height: 1.5;
}
```

> 다크 플레이트가 이미지의 다크 배경(#0d1424 등)과 자연스럽게 이어져 기존 156개 SVG를 손대지 않고 재사용.

- [ ] **Step 3: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, `/blog/convex-hull-5` 열기.
Expected: SVG 다이어그램이 다크 플레이트 카드 안에 들어가고, alt 텍스트가 하단 모노 캡션으로 표시. 종이 위에서 글씨 안 깨짐. 이미지 클릭 시 라이트박스 동작.

- [ ] **Step 4: 커밋**

```bash
git add astro.config.mjs src/styles/global.css
git commit -m "feat(ui): 다이어그램 다크 플레이트 + alt 캡션(figure)"
```

---

### Task 7: 아티클 헤더(커맨드 에코) + 포스트 크롬

포스트 상단에 커맨드 에코 + 키커를 추가하고, breadcrumb·meta·난이도·post-nav·TOC·읽기 진행바·back-to-top 색을 새 팔레트로.

**Files:**
- Modify: `src/layouts/PostLayout.astro` (`.post-header` 마크업)
- Modify: `src/styles/global.css` (`.post-header`, `.post-meta`, `.post-breadcrumb`, `.difficulty-badge`, `.post-nav*`, `.toc*`, `#reading-progress`, `#back-to-top`)

**Interfaces:**
- Consumes: 모든 새 토큰.

- [ ] **Step 1: 아티클 헤더에 커맨드 에코 + 키커 추가**

`PostLayout.astro` 166–167행을 교체:

```html
    <div class="post-header">
      <div class="post-cmd"><span class="post-cmd-op">$</span> cat {category ? `${category}/` : ''}{title}.md <span class="post-cmd-op">|</span> render</div>
      <h1>{title}</h1>
```

- [ ] **Step 2: 헤더/메타/breadcrumb 스타일**

509–562행 범위를 새 팔레트로. 핵심:

```css
.post-cmd { font-family: var(--font-mono); font-size: 0.74rem; color: var(--ink-faint); margin-bottom: 0.6rem; }
.post-cmd-op { color: var(--amber); }
.post-header h1 { font-family: var(--font-serif); font-size: 2rem; font-weight: 600; letter-spacing: -0.015em; line-height: 1.18; color: var(--ink); }
.post-meta { color: var(--ink-faint); font-family: var(--font-mono); font-size: 0.78rem; }
.post-breadcrumb, .post-breadcrumb a { color: var(--ink-faint); }
.post-breadcrumb a:hover { color: var(--amber); }
```

- [ ] **Step 3: 난이도 배지 단색화**

`.difficulty-badge` 및 `.difficulty-*` 규칙을 찾아, 색을 앰버 계열 단색으로: `border: 1px solid var(--amber); color: var(--amber); background: var(--amber-soft);` (난이도별 색상 분기는 제거하고 통일).

- [ ] **Step 4: post-nav 카드 종이화 + 글로우 제거**

`.post-nav-item` 규칙에서 hover 글로우/translateY 제거, 종이 카드로:

```css
.post-nav-item { border: 1px solid var(--rule); border-radius: 8px; background: var(--bg-card); transition: border-color 0.15s; }
.post-nav-item:hover { border-color: var(--amber); }
.post-nav-label { color: var(--amber); font-family: var(--font-mono); font-size: 0.72rem; }
.post-nav-title { color: var(--ink); }
.post-nav-desc { color: var(--ink-faint); }
```

- [ ] **Step 5: TOC / 읽기 진행바 / back-to-top**

```css
.toc-title { color: var(--ink-soft); font-family: var(--font-mono); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }
.toc-link { color: var(--ink-faint); }
.toc-link:hover { color: var(--ink); }
.toc-link.active { color: var(--amber); text-shadow: none; }
#reading-progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--amber); box-shadow: none; z-index: 200; }
#back-to-top { background: var(--term-bg); color: var(--term-fg); border: 1px solid #3a3f37; }
#back-to-top:hover { background: #1d2027; }
```

(TOC active의 기존 text-shadow glow, 진행바 gradient+glow 제거.)

- [ ] **Step 6: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, `/blog/convex-hull-5` 열기.
Expected: 제목 위 `$ cat convex-hull/....md | render`(앰버 `$`/`|`), 제목 세리프, 메타 모노, 난이도 배지 앰버 단색, TOC active 앰버(글로우 없음), 진행바 앰버 단색, 이전/다음 글 카드 종이.

- [ ] **Step 7: 커밋**

```bash
git add src/layouts/PostLayout.astro src/styles/global.css
git commit -m "feat(ui): 아티클 헤더 커맨드 에코 + 포스트 크롬 팔레트 정리"
```

---

### Task 8: 홈/목록 + 검색 모달 + 잔여 정리

포스트 목록의 staggered 애니메이션·글로우 제거, 태그·검색 모달을 새 팔레트로, 남은 sky/violet·`html.light` 잔재 제거.

**Files:**
- Modify: `src/styles/global.css` (`/* ── Page Load Animation ── */`, `/* ── Post List ── */`, `/* ── Tags ── */`, 검색 모달 규칙)

**Interfaces:**
- Consumes: 모든 새 토큰.

- [ ] **Step 1: 등장 애니메이션 절제**

63–72행 `@keyframes fadeInUp`/`fadeIn`은 유지하되, 388–418행 `.post-item`의 `animation`과 `nth-child` 지연(410–418행) 블록을 삭제. 98행 `.sidebar { animation: fadeIn ... }`도 삭제(즉시 표시).

- [ ] **Step 2: post-item 종이 카드 + 글로우 제거**

395–468행 `.post-item*`를 종이화:

```css
.post-item { border: 1px solid var(--rule); border-radius: 8px; padding: 1rem 1.2rem; background: var(--bg-card); transition: border-color 0.15s; }
.post-item:hover { border-color: var(--amber); transform: none; box-shadow: none; }
.post-item-title { color: var(--ink); font-family: var(--font-serif); }
.post-item:hover .post-item-title { color: var(--amber); }
.post-item-date { color: var(--ink-faint); font-family: var(--font-mono); font-size: 0.74rem; }
.post-item-desc { color: var(--ink-soft); }
```

- [ ] **Step 3: 태그 단색화**

469–507행 `.tag`/`.post-list .tag`를 앰버 단색으로:

```css
.tag { font-family: var(--font-mono); font-size: 0.72rem; color: var(--amber); background: var(--amber-soft); border: 1px solid transparent; padding: 0.1rem 0.5rem; border-radius: 4px; transition: background 0.15s; }
.tag:hover { transform: none; box-shadow: none; background: rgba(181,106,26,0.18); }
.post-list .tag { background: var(--amber-soft); }
```

- [ ] **Step 4: 검색 모달 종이화**

검색 모달 규칙(`#search-modal`, `.search-modal-box`, `.search-result-item`, `.search-result-badge` 등)의 배경/보더/텍스트를 종이+룰+앰버로. `.search-result-item.focused`/`:hover` 배경 `var(--amber-soft)`, 텍스트 `var(--ink)`. 모달 박스 `background: var(--paper); border: 1px solid var(--rule)`.

- [ ] **Step 5: 잔여 sky/violet·html.light 스캔**

Run: `grep -nE "#38bdf8|#a78bfa|#f97316|sky|violet|html\\.light|0f1117|1a2035" src/styles/global.css`
Expected: 하드코딩된 옛 색/라이트 규칙이 남아 있으면 새 토큰으로 교체하거나 삭제. (별칭 토큰으로 이미 흡수된 경우 제외.)

- [ ] **Step 6: 빌드 + 육안 검증**

Run: `npm run build` → 성공.
Run: `npm run dev`, `/`, `/blog`, `/tags`, `/categories` 열기.
Expected: 목록 카드 종이+앰버 hover(글로우/이동 없음), 태그 앰버 단색, 검색(Ctrl K) 모달 종이 톤, staggered 등장 애니메이션 없음, 콘솔 에러 없음.

- [ ] **Step 7: 커밋**

```bash
git add src/styles/global.css
git commit -m "feat(ui): 목록·태그·검색 모달 팔레트 정리, staggered 애니메이션 제거"
```

---

### Task 9: 최종 QA — 반응형 · 모션 · 접근성 · 전체 빌드

**Files:**
- Modify: `src/styles/global.css` (필요 시 반응형/reduced-motion 보강)

- [ ] **Step 1: reduced-motion 가드**

`global.css` 끝에 추가:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
```

- [ ] **Step 2: 모바일 사이드바 확인**

Run: `npm run dev`, 브라우저를 375px 폭으로.
Expected: 햄버거(`#sidebar-toggle`)로 다크 사이드바 열림/닫힘 정상. 본문 종이 가독. `.margin-note`(있다면) 인라인으로 접힘.

- [ ] **Step 3: 가로 스크롤 격리 확인**

Expected: 코드 카드·표·다이어그램 플레이트가 자체 `overflow-x`로 스크롤되고, `body`는 가로 스크롤 없음.

- [ ] **Step 4: 대비/포커스 확인**

Expected: 종이(#faf8f3)/잉크(#22201b) 및 다크/term-fg 대비 충분. Tab 이동 시 `:focus-visible` 앰버 아웃라인 보임.

- [ ] **Step 5: 대표 페이지 전수 육안**

`/`, `/blog`, `/blog/convex-hull-5`(SVG+코드+콜아웃+수식 포함), `/blog/convex-hull-1`, `/tags`, `/categories`, `/stats`, `/404`.
Expected: 모든 페이지에서 라이트 잔재/깨진 색 없음, 주장이 일관되게 드러남.

- [ ] **Step 6: 최종 빌드 + 커밋**

Run: `npm run build`
Expected: 성공.

```bash
git add src/styles/global.css
git commit -m "chore(ui): reduced-motion 가드 + 최종 QA 보정"
```

---

## Self-Review

**Spec coverage:**
- 주장/이중 톤 → Task 1·2·3. 앰버 단색 → 전 태스크. light 토글 제거 → Task 1. 사이드바 터미널 → Task 2. 논문 본문/`##` 헤딩 → Task 3. 정리 블록/여백 노트 → Task 4. 코드 터미널 카드 → Task 5. SVG 다크 플레이트(마이그레이션 0)+캡션 → Task 6. 커맨드 에코·포스트 크롬 → Task 7. 목록/태그/검색·애니메이션 제거 → Task 8. 반응형/모션/접근성 → Task 9. 웹폰트 A(다이나믹 서브셋) → Task 1. **모든 스펙 항목이 태스크에 매핑됨.**
- 폰트 미결정(정확 URL): Task 1 Step 1에서 Google Fonts CSS2로 확정(unicode-range 분할 = 다이나믹 서브셋), dev 네트워크 탭으로 검증.

**Placeholder scan:** "적절히", "TODO" 없음. 각 CSS 스텝에 실제 선언 포함. grep 스텝은 값 교체를 위한 탐색이므로 허용.

**Type consistency:** 토큰 이름(`--amber`, `--term-bg`, `--ink-faint` 등)이 Task 1 정의와 전 태스크에서 일치. rehype 함수명 `rehypeFigureCaption` Task 6 내 일관. 클래스명 `.post-figure`/`.post-cmd`/`.margin-note`/`.callout` 일관.

**주의(실행 중 판단):** `global.css`는 편집이 누적되며 행 번호가 이동한다. 행 번호는 시작 시점 기준 참고값이고, **셀렉터/섹션 주석으로 위치를 찾아** 교체할 것.
