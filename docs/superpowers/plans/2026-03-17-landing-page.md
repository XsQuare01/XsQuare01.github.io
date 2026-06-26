# 대문(Landing) 페이지 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** GitHub README 스타일 대문 페이지를 `/`에 만들고, 기존 글 목록을 `/blog`로 이동하며 사이드바를 업데이트한다.

**Architecture:** `index.astro`를 대문 페이지로 전면 교체하고, 기존 글 목록 로직은 `src/pages/blog/index.astro`에 새로 생성한다. `BaseLayout.astro`의 사이드바에 홈 링크를 추가하고 글 목록 링크를 `/blog`로 변경한다.

**Tech Stack:** Astro v6, CSS Variables (기존 global.css), shields.io (외부 이미지), github-readme-stats (외부 이미지)

---

## 파일 변경 목록

| 파일 | 작업 |
|------|------|
| `src/pages/blog/index.astro` | 신규 생성 — 글 목록 |
| `src/pages/index.astro` | 전면 교체 — 대문 페이지 |
| `src/layouts/BaseLayout.astro` | 사이드바 수정 |

---

### Task 1: 글 목록 페이지를 `/blog`로 이동

**Files:**
- Create: `src/pages/blog/index.astro`

- [ ] **Step 1: `src/pages/blog/index.astro` 생성**

기존 `src/pages/index.astro`의 글 목록 로직을 그대로 복사해 새 파일로 만든다:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

const posts = (await getCollection('posts')).sort(
  (a, b) => b.data.date.getTime() - a.data.date.getTime()
);
---

<BaseLayout title="글 목록">
  <ul class="post-list">
    {posts.map((post) => (
      <li class="post-item">
        <span class="post-item-date">
          {post.data.date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })}
        </span>
        <a href={`/blog/${post.id}`} class="post-item-title">
          {post.data.title}
        </a>
        {post.data.description && (
          <p class="post-item-desc">{post.data.description}</p>
        )}
        {post.data.tags.length > 0 && (
          <div class="tags">
            {post.data.tags.map((tag) => (
              <a href={`/tags/${tag}`} class="tag">{tag}</a>
            ))}
          </div>
        )}
      </li>
    ))}
  </ul>
</BaseLayout>
```

- [ ] **Step 2: 빌드 확인**

```bash
npm run build
```

Expected: `✓ Completed` — `/blog/index.html` 포함

- [ ] **Step 3: 커밋**

```bash
git add src/pages/blog/index.astro
git commit -m "feat: 글 목록 페이지 /blog로 이동"
```

---

### Task 2: 사이드바에 홈 링크 추가 및 글 목록 링크 수정

**Files:**
- Modify: `src/layouts/BaseLayout.astro` (사이드바 nav 부분, 약 44-55번째 줄)

- [ ] **Step 1: `BaseLayout.astro`의 사이드바 nav 수정**

기존:
```astro
<nav class="sidebar-nav">
  <div class="sidebar-nav-label">메뉴</div>
  <a href="/" class={currentPath === '/' ? 'active' : ''}>
    📝 &nbsp;글 목록
  </a>
  <a href="/categories" class={currentPath.startsWith('/categories') ? 'active' : ''}>
    📂 &nbsp;카테고리
  </a>
  <a href="/tags" class={currentPath.startsWith('/tags') ? 'active' : ''}>
    🏷️ &nbsp;태그
  </a>
</nav>
```

변경 후:
```astro
<nav class="sidebar-nav">
  <div class="sidebar-nav-label">메뉴</div>
  <a href="/" class={currentPath === '/' ? 'active' : ''}>
    🏠 &nbsp;홈
  </a>
  <a href="/blog" class={currentPath.startsWith('/blog') ? 'active' : ''}>
    📝 &nbsp;글 목록
  </a>
  <a href="/categories" class={currentPath.startsWith('/categories') ? 'active' : ''}>
    📂 &nbsp;카테고리
  </a>
  <a href="/tags" class={currentPath.startsWith('/tags') ? 'active' : ''}>
    🏷️ &nbsp;태그
  </a>
</nav>
```

- [ ] **Step 2: 빌드 확인**

```bash
npm run build
```

Expected: `✓ Completed`

- [ ] **Step 3: 커밋**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat: 사이드바에 홈 링크 추가, 글 목록 → /blog"
```

---

### Task 3: 대문 페이지로 `/` 교체

**Files:**
- Modify: `src/pages/index.astro` (전면 교체)

- [ ] **Step 1: `src/pages/index.astro` 전면 교체**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

const recentPosts = (await getCollection('posts'))
  .sort((a, b) => b.data.date.getTime() - a.data.date.getTime())
  .slice(0, 5);
---

<BaseLayout title="홈">
  <div class="prose">

    <!-- 섹션 1: 프로필 헤더 -->
    <section style="margin-bottom: 2.5rem;">
      <h1 style="font-size: 2rem; margin-bottom: 0.5rem;">XsQuare01</h1>
      <p style="color: var(--text-muted); font-size: 1rem; margin-bottom: 0.75rem;">기록하는 개발자</p>
      <p style="font-size: 0.9rem; color: var(--text-muted);">
        📍 Seoul &nbsp;·&nbsp;
        <a href="https://github.com/XsQuare01" target="_blank" rel="noopener noreferrer">GitHub</a>
        &nbsp;·&nbsp;
        <a href="mailto:mystic6113@naver.com">이메일</a>
      </p>
    </section>

    <!-- 섹션 2: 기술 스택 -->
    <section style="margin-bottom: 2.5rem;">
      <h2>🛠 Tech Stack</h2>
      <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem;">
        <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white" alt="Kotlin" />
        <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python" />
        <img src="https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white" alt="C++" />
        <img src="https://img.shields.io/badge/Astro-FF5D01?style=flat&logo=astro&logoColor=white" alt="Astro" />
        <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript" />
        <img src="https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white" alt="Git" />
      </div>
    </section>

    <!-- 섹션 3: GitHub Stats -->
    <section style="margin-bottom: 2.5rem;">
      <h2>📊 GitHub Stats</h2>
      <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem;">
        <img
          src="https://github-readme-stats.vercel.app/api?username=XsQuare01&show_icons=true&theme=dark&hide_border=true&bg_color=0f1117"
          alt="XsQuare01's GitHub Stats"
          loading="lazy"
          height="160"
        />
        <img
          src="https://github-readme-stats.vercel.app/api/top-langs/?username=XsQuare01&layout=compact&theme=dark&hide_border=true&bg_color=0f1117"
          alt="Top Languages"
          loading="lazy"
          height="160"
        />
      </div>
    </section>

    <!-- 섹션 4: 최근 포스트 -->
    <section style="margin-bottom: 2.5rem;">
      <h2>📝 Recent Posts</h2>
      <ul class="post-list" style="margin-top: 0.75rem;">
        {recentPosts.map((post) => (
          <li class="post-item">
            <span class="post-item-date">
              {post.data.date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })}
            </span>
            <a href={`/blog/${post.id}`} class="post-item-title">
              {post.data.title}
            </a>
            {post.data.description && (
              <p class="post-item-desc">{post.data.description}</p>
            )}
          </li>
        ))}
      </ul>
    </section>

    <!-- 섹션 5: 프로젝트 & 관심사 -->
    <section style="margin-bottom: 2.5rem;">
      <h2>🚀 Projects & Interests</h2>
      <ul style="margin-top: 0.75rem;">
        <li><strong>이 블로그</strong> — Astro로 만든 개인 기술 블로그</li>
        <li><strong>암호학</strong> — 수학적 기반의 암호 이론 공부</li>
        <li><strong>알고리즘</strong> — 문제 해결과 복잡도 이론</li>
      </ul>
    </section>

  </div>
</BaseLayout>
```

- [ ] **Step 2: 빌드 확인**

```bash
npm run build
```

Expected: `✓ Completed` — `/index.html` 포함

- [ ] **Step 3: 커밋**

```bash
git add src/pages/index.astro
git commit -m "feat: 대문 페이지 추가 (프로필, 스택, stats, 최근 글, 프로젝트)"
```
