# Blog UI Improvements Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 메인 페이지 프로필 강조, 섹션 여백 확대, 카드 호버 포인트 라인, 사이드바 태그 가독성 개선

**Architecture:** 변경은 두 파일에 집중됨. `src/pages/index.astro`는 프로필 섹션 HTML 구조 변경, `src/styles/global.css`는 나머지 스타일 변경.

**Tech Stack:** Astro v6, CSS Variables

---

### Task 1: 메인 페이지 프로필 섹션 재구성

**Files:**
- Modify: `src/pages/index.astro` (섹션 1, 약 14~23행)

현재 구조:
```html
<section style="margin-bottom: 2.5rem;">
  <h1 style="font-size: 2rem; ...">XsQuare01</h1>
  <p style="color: var(--text-muted); ...">기록하는 개발자</p>
  <p style="font-size: 0.9rem; ...">
    Seoul · GitHub · 이메일
  </p>
</section>
```

목표 구조 — 아바타와 텍스트를 가로로 배치:
```html
<section style="margin-bottom: 3.5rem;">
  <div style="display: flex; align-items: center; gap: 1.5rem;">
    <img
      src="https://github.com/XsQuare01.png"
      alt="XsQuare01 프로필 사진"
      style="width: 88px; height: 88px; border-radius: 50%; border: 2px solid var(--accent); flex-shrink: 0;"
    />
    <div>
      <h1 style="font-size: 2.6rem; margin-bottom: 0.25rem; border: none;">XsQuare01</h1>
      <p style="color: var(--accent); font-size: 1rem; margin-bottom: 0.5rem;">기록하는 개발자</p>
      <p style="font-size: 0.9rem; color: var(--text-muted);">
        Seoul &nbsp;·&nbsp;
        <a href="https://github.com/XsQuare01" target="_blank" rel="noopener noreferrer">GitHub</a>
        &nbsp;·&nbsp;
        <a href="mailto:mystic6113@naver.com">이메일</a>
      </p>
    </div>
  </div>
</section>
```

- [ ] **Step 1: `src/pages/index.astro`의 섹션 1 교체**

위 목표 구조로 섹션 1 전체를 교체한다.

- [ ] **Step 2: 로컬에서 확인**

```bash
npm run dev
```

브라우저에서 `/` 접속 → 아바타와 이름이 가로로 나란히, 부제가 오렌지색인지 확인.

- [ ] **Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "Feat: 메인 페이지 프로필 섹션 아바타+강조 스타일 적용"
```

---

### Task 2: 섹션 여백 확대

**Files:**
- Modify: `src/pages/index.astro` (섹션 2~5의 `margin-bottom`)

섹션 1은 Task 1에서 이미 3.5rem으로 변경됨. 나머지 섹션들도 동일하게 적용.

- [ ] **Step 1: 섹션 2~5의 `margin-bottom: 2.5rem` → `3.5rem` 변경**

```html
<!-- 섹션 2: Tech Stack -->
<section style="margin-bottom: 3.5rem;">

<!-- 섹션 3: GitHub Stats -->
<section style="margin-bottom: 3.5rem;">

<!-- 섹션 4: Recent Posts -->
<section style="margin-bottom: 3.5rem;">

<!-- 섹션 5: Projects & Interests -->
<section style="margin-bottom: 3.5rem;">
```

- [ ] **Step 2: 로컬에서 확인**

각 섹션 사이 여백이 넓어졌는지 확인.

- [ ] **Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "Feat: 메인 페이지 섹션 여백 확대 (2.5rem → 3.5rem)"
```

---

### Task 3: Recent Posts 카드 호버 시 왼쪽 포인트 라인

**Files:**
- Modify: `src/styles/global.css` (`.post-item:hover` 블록)

현재:
```css
.post-item:hover {
  background: var(--bg-card);
  border-color: var(--border);
}
```

목표 — 호버 시 왼쪽 오렌지 라인:
```css
.post-item:hover {
  background: var(--bg-card);
  border-color: var(--border);
  border-left: 3px solid var(--accent);
  padding-left: calc(1.5rem - 3px); /* 기존 padding 1.5rem에서 추가 border 3px 보정 */
}
```

- [ ] **Step 1: `global.css`의 `.post-item:hover` 수정**

- [ ] **Step 2: 로컬에서 확인**

글 목록 카드에 마우스 올렸을 때 왼쪽에 오렌지 라인이 나타나는지 확인. 레이아웃 흔들림 없는지 확인.

- [ ] **Step 3: Commit**

```bash
git add src/styles/global.css
git commit -m "Feat: 포스트 카드 호버 시 왼쪽 오렌지 포인트 라인 추가"
```

---

### Task 4: 사이드바 태그 글자색 개선

**Files:**
- Modify: `src/styles/global.css` (`.sidebar-tags .tag`)

현재:
```css
.sidebar-tags .tag {
  font-size: 0.72rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: var(--bg-card);
  color: var(--text-muted);
  border: 1px solid var(--border);
  transition: all 0.15s;
}
```

목표 — 글자색을 흰색에 가깝게:
```css
.sidebar-tags .tag {
  font-size: 0.72rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: var(--bg-card);
  color: var(--text);
  border: 1px solid var(--border);
  transition: all 0.15s;
}
```

- [ ] **Step 1: `global.css`의 `.sidebar-tags .tag` color 변경**

`color: var(--text-muted)` → `color: var(--text)`

- [ ] **Step 2: 로컬에서 확인**

사이드바 태그 텍스트가 밝게 보이는지 확인.

- [ ] **Step 3: Commit**

```bash
git add src/styles/global.css
git commit -m "Feat: 사이드바 태그 글자색 가독성 개선"
```
