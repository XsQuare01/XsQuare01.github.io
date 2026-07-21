# 사이드바 접힘/펼침 재배열 제거 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 사이드바 접힘↔펼침 시 카테고리/라벨이 재배열되며 튀는 현상을 제거하되, 접힘·pin·모바일 동작은 유지한다.

**Architecture:** `.sidebar` 자식을 고정 폭(14rem) `.sidebar-inner`로 감싸 콘텐츠를 항상 14rem 기준으로 레이아웃하고, `.sidebar`는 `overflow-x: hidden`으로 접힘 때 잘라 가린다. 라벨·확장영역의 표시 전환을 `display` 토글에서 `opacity/visibility` 페이드로 바꿔 레이아웃 불변을 만든다.

**Tech Stack:** Astro 정적 사이트, 순수 CSS.

## Global Constraints

- 유닛 테스트 없음 → 검증은 `npm run build` 성공 + 소스 grep + 육안.
- 커밋에 `Co-Authored-By` 트레일러 금지.
- 브랜치 `fix/sidebar-collapse-reflow`(생성됨), main 직접 커밋 금지.
- 변경 파일: `src/layouts/BaseLayout.astro`, `src/styles/global.css` 두 개로 한정.
- 접힘/펼침·pin(`html.rail-pinned`)·모바일 드로어·`prefers-reduced-motion` 동작 보존.

---

### Task 1: 고정 폭 내부 래퍼 + opacity 페이드 전환

**Files:**
- Modify: `src/layouts/BaseLayout.astro` (`.sidebar` 자식 전체를 `.sidebar-inner`로 래핑)
- Modify: `src/styles/global.css` (`.sidebar`/`.sidebar-inner` 분리, display 토글→opacity/visibility, 토큰, 모바일, reduced-motion)

**Interfaces:**
- Consumes: 기존 클래스 `.rail-txt`(라벨·brand-txt·kbd), `.rail-expand-only`(카테고리·태그·footer) — 마크업은 그대로 사용, 표시 규칙만 교체.
- Produces: 없음.

- [ ] **Step 1: 현재 상태 확인**

Run: `grep -n "rail-expand-only { display" src/styles/global.css`
Expected: `119:.rail-expand-only { display: none; }` (교체 대상 확인)

- [ ] **Step 2: BaseLayout에 `.sidebar-inner` 래퍼 추가**

`src/layouts/BaseLayout.astro`에서 `<aside class="sidebar" id="sidebar">` 여는 태그 **바로 다음 줄**에 `<div class="sidebar-inner">`를 넣고, 짝이 되는 `</aside>` **바로 앞**에 `</div>`를 넣어 브랜드~`.rail-bottom`까지 모든 자식을 감싼다.

```astro
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-inner">
      <a href="/" class="brand" aria-label="XsQuare01 홈">
      ...
      <div class="rail-bottom">
        ...
      </div>
    </div>
  </aside>
```
(자식 내용은 변경하지 않는다. 들여쓰기만 한 단계 추가하면 되고, 필수는 아니다.)

- [ ] **Step 3: `--rail-expanded` 토큰 추가**

`src/styles/global.css`의 `:root` 레일 토큰 블록(현재 `--rail-w`, `--main-gap`, `--rail-bg`)에 한 줄 추가:

```css
  --rail-expanded: 14rem;  /* 내부 콘텐츠 고정 폭 */
```

- [ ] **Step 4: `.sidebar`에서 flex·padding을 `.sidebar-inner`로 이관**

`.sidebar` 규칙(현재 라인 93~109)을 아래로 교체(‑ `display:flex`, `flex-direction`, `padding` 제거):

```css
.sidebar {
  width: var(--rail-w);
  min-height: 100vh;
  background: var(--rail-bg);
  border-right: 1px solid var(--rule);
  position: fixed;
  top: 0; left: 0;
  overflow-y: auto;
  overflow-x: hidden;
  z-index: 100;
  font-family: var(--font-sans);
  color: var(--ink-soft);
  transition: width 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
}
.sidebar-inner {
  width: var(--rail-expanded);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 1rem 0.5rem;
}
```

- [ ] **Step 5: display 토글(라인 117~125)을 opacity/visibility로 교체**

해당 6개 규칙 블록 전체를 아래로 바꾼다:

```css
/* 접힘/펼침 표시 전환: display 대신 opacity/visibility → 레이아웃 불변, 재배열 없음 */
.rail-txt, .rail-expand-only {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.18s ease, visibility 0.18s;
}
html.rail-pinned .rail-txt,
html.rail-pinned .rail-expand-only,
html:not(.rail-pinned) .sidebar:hover .rail-txt,
html:not(.rail-pinned) .sidebar:hover .rail-expand-only,
html:not(.rail-pinned) .sidebar:focus-within .rail-txt,
html:not(.rail-pinned) .sidebar:focus-within .rail-expand-only {
  opacity: 1;
  visibility: visible;
}
```

- [ ] **Step 6: 모바일 규칙 교체 + 내부 폭**

모바일 `@media (max-width: 768px)`에서 `.rail-txt { display: inline; }`·`.rail-expand-only { display: block; }`(현재 라인 1165~1166)을 아래로 바꾸고, 드로어를 채우도록 내부 폭을 100%로:

```css
  .rail-txt, .rail-expand-only { opacity: 1; visibility: visible; }
  .sidebar-inner { width: 100%; }
```

- [ ] **Step 7: reduced-motion 추가**

`.sidebar` 규칙 근처(예: 라인 115 뒤)에 추가:

```css
@media (prefers-reduced-motion: reduce) {
  .sidebar, .rail-txt, .rail-expand-only { transition: none; }
}
```

- [ ] **Step 8: 빌드**

Run: `npm run build`
Expected: `Complete!`

- [ ] **Step 9: 검증**

Run: `grep -c "display: none" src/styles/global.css` — (참고용, 사이드바 관련 display:none 감소 확인)
Run: `grep -n "sidebar-inner" src/styles/global.css src/layouts/BaseLayout.astro`
Expected: `.sidebar-inner` 규칙(2곳: 기본·모바일)과 마크업 래퍼가 존재.
Run: `grep -n "rail-txt, .rail-expand-only" src/styles/global.css`
Expected: opacity/visibility 규칙이 존재하고, 옛 `.rail-txt { display: none; }`·`.rail-expand-only { display: none; }`(라인 118~119)는 사라짐.

- [ ] **Step 10: 커밋**

```bash
git add src/layouts/BaseLayout.astro src/styles/global.css
git commit -m "fix(ui): 사이드바 접힘/펼침 재배열 제거 (고정 폭 내부+클립+opacity 페이드)"
```

---

## 최종 검증 (육안)

- [ ] `npm run build` 성공.
- [ ] 데스크톱: 레일에 호버하면 폭만 커지며 라벨·카테고리가 **페이드로** 나타나고, **카테고리 재배열/튐이 없다**. 접힘 상태엔 아이콘만 보이고 카테고리 텍스트 슬라이버가 새지 않는다.
- [ ] pin 고정/해제 정상. 본문은 `--main-gap`만 따르므로 호버로 밀리지 않는다.
- [ ] 모바일(≤768px): 드로어에 라벨·카테고리·태그 모두 보인다.
- [ ] `prefers-reduced-motion`에서 애니메이션 없이 즉시 전환.

## Self-Review 결과

- **Spec 커버리지:** 고정 폭 내부(Step 2,4)·클립(Step 4 overflow 유지)·opacity 페이드(Step 5)·모바일(Step 6)·reduced-motion(Step 7) 모두 대응.
- **Placeholder:** 없음. 모든 스텝에 실제 코드/명령 포함.
- **타입/이름 일관성:** `.sidebar-inner`, `--rail-expanded`가 마크업·CSS·모바일에서 일관 사용. 기존 `.rail-txt`/`.rail-expand-only` 클래스명 유지(마크업 무변경).
