# 홈 '추천 글' 히어로 리스트 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 홈 '추천 글'을 옛 카드 스타일에서 헤어라인 구분 N개 히어로 리스트로 바꿔 종이+에디토리얼 홈과 통일한다.

**Architecture:** `src/pages/index.astro` 한 파일의 featured 마크업과 scoped 스타일을 함께 교체한다. 데이터 소스(`FEATURED_IDS` 수동 목록)와 `getCategoryLabel` import는 그대로 재사용, 날짜 포맷 헬퍼만 추가한다.

**Tech Stack:** Astro 정적 사이트, scoped CSS, TypeScript(frontmatter script).

## Global Constraints

- 유닛 테스트 없음 → 검증은 `npm run build` 성공 + 산출물 grep + 육안.
- 커밋에 `Co-Authored-By` 트레일러 금지(블로그 저장소 관례).
- 브랜치 `feat/featured-hero-list`(생성됨), main 직접 커밋 금지.
- 변경은 `src/pages/index.astro` 한 파일로 한정. 콘텐츠 마크다운·SVG 불변.
- 마크업/스타일은 스펙(`docs/superpowers/specs/2026-07-20-featured-hero-list-design.md`)의 코드를 그대로 사용.
- 날짜 포맷은 `YYYY.MM.DD`. 카테고리는 `getCategoryLabel()`(이미 import됨). `difficulty`·`description`은 값 있을 때만 렌더.

---

### Task 1: featured 섹션 → N개 히어로 리스트

**Files:**
- Modify: `src/pages/index.astro` (frontmatter 헬퍼 1개 추가 · featured 마크업 블록 교체 · scoped 스타일 교체 · reduced-motion/반응형 잔재 정리)

**Interfaces:**
- Consumes: `FEATURED_IDS`, `featuredPosts`, `getCategoryLabel(slug: string): string` (모두 이미 존재)
- Produces: 없음(홈 페이지 전용)

- [ ] **Step 1: 현재 상태 확인**

Run: `grep -n "featured-grid\|featured-label\|class=\"featured\"" src/pages/index.astro`
Expected: 옛 카드 마크업/스타일 라인들이 보임(교체 대상 확인).

- [ ] **Step 2: 날짜 포맷 헬퍼 추가**

frontmatter의 `const featuredPosts = ...` 줄 **바로 다음**에 추가:

```ts
const fmtDate = (d: Date) =>
  `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`;
```

- [ ] **Step 3: featured 마크업 블록 교체**

아래 옛 블록을
```astro
    {featuredPosts.length > 0 && (
      <div class="featured-grid">
        {featuredPosts.map((post) => (
          <a href={`/blog/${post!.id}`} class="featured">
            <span class="featured-label">추천 글</span>
            <div class="featured-title">{post!.data.title}</div>
            {post!.data.description && (
              <div class="featured-desc">{post!.data.description}</div>
            )}
          </a>
        ))}
      </div>
    )}
```
아래로 바꾼다:
```astro
    {featuredPosts.length > 0 && (
      <section class="featured-section">
        <div class="feed-head">
          <h2 class="feed-label">추천 글</h2>
          <span class="feat-sub">주요 카테고리 대표</span>
        </div>
        <div class="featured-list">
          {featuredPosts.map((post) => (
            <a href={`/blog/${post!.id}`} class="feat">
              <div class="feat-meta">
                {post!.data.category && <span class="cat">{getCategoryLabel(post!.data.category)}</span>}
                <span class="dot">·</span>
                <span class="tnum">{fmtDate(post!.data.date)}</span>
                {post!.data.difficulty && (<><span class="dot">·</span><span>{post!.data.difficulty}</span></>)}
              </div>
              <div class="feat-title">{post!.data.title}</div>
              {post!.data.description && <div class="feat-desc">{post!.data.description}</div>}
            </a>
          ))}
        </div>
      </section>
    )}
```

- [ ] **Step 4: scoped 스타일 교체**

옛 `.featured-grid` / `.featured` / `.featured:hover` / `.featured:focus-visible` / `.featured-label` / `.featured-title` / `.featured-desc` 블록 전체를 삭제하고, 그 자리에 아래를 넣는다:

```css
  .featured-section { margin-bottom: 1.75rem; }
  .feat-sub { font-size: 0.75rem; color: var(--text-dim); }

  .featured-list { border-bottom: 1px solid var(--rule); }
  .feat {
    display: block;
    text-decoration: none;
    border-top: 1px solid var(--rule);
    padding: 1.15rem 0;
  }
  .feat-meta {
    display: flex; flex-wrap: wrap; align-items: center; gap: 0.45rem;
    font-size: 0.76rem; color: var(--text-dim); margin-bottom: 0.45rem;
  }
  .feat-meta .cat { color: var(--accent); font-weight: 700; }
  .feat-meta .dot { color: var(--rule); }
  .feat-meta .tnum { font-variant-numeric: tabular-nums; }
  .feat-title {
    font-family: var(--font-serif);
    font-size: 1.5rem; font-weight: 700; line-height: 1.22;
    letter-spacing: -0.01em; color: var(--text);
    margin-bottom: 0.45rem; text-wrap: balance;
    transition: color 0.12s;
  }
  .feat:hover .feat-title { color: var(--accent); }
  .feat:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
  .feat-desc {
    font-size: 0.9rem; color: var(--text-muted); line-height: 1.6; text-wrap: pretty;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  }
```

- [ ] **Step 5: reduced-motion·반응형 잔재 정리**

`@media (prefers-reduced-motion: reduce)` 블록에서 `.featured` 관련 참조를 정리한다. 아래 세 줄에서 `.featured` 항목을 제거하고 `.featured::after` 줄은 통째로 삭제:
```css
    .cat-item, .featured, .feed-item, .feed-more { transition: none; }
    .cat-item:active, .featured:active, .feed-item:active { transform: none; }
    .cat-item:focus-visible, .featured:focus-visible, .feed-item:focus-visible, .feed-more:focus-visible {
```
→
```css
    .cat-item, .feed-item, .feed-more { transition: none; }
    .cat-item:active, .feed-item:active { transform: none; }
    .cat-item:focus-visible, .feed-item:focus-visible, .feed-more:focus-visible {
```
그리고 `.featured::after { transition: none; }` 줄 삭제.

반응형 미디어쿼리에서 `.featured-grid { grid-template-columns: 1fr; }` 줄을 삭제(리스트는 단일 열이라 불필요).

- [ ] **Step 6: 빌드**

Run: `npm run build`
Expected: `Complete!` (에러 없음)

- [ ] **Step 7: 검증 — 새 리스트만 남고 옛 카드 잔재 없음**

Run: `grep -c "featured-grid\|featured-label\|class=\"featured\"" src/pages/index.astro`
Expected: `0`

Run: `grep -o 'class="feat-title"' dist/index.html | wc -l`
Expected: featured 글 수(현재 `2`)와 일치.

Run: `grep -o 'feat-meta[^>]*>' dist/index.html | head -1`
Expected: 메타 컨테이너가 렌더됨(비어있지 않음).

- [ ] **Step 8: 커밋**

```bash
git add src/pages/index.astro
git commit -m "feat(ui): 홈 '추천 글'을 헤어라인 히어로 리스트로 (옛 카드 스타일 제거, N개 카테고리 대표)"
```

---

## 최종 검증

- [ ] `npm run build` 성공.
- [ ] 홈 육안: '추천 글'이 헤어라인 구분 세로 리스트, 카드·왼쪽 바·글로우 없음, 카테고리 잉크블루, 호버 시 제목 잉크블루, 헤딩이 '최근 글'과 통일.
- [ ] `FEATURED_IDS`에 임시로 3번째 id 추가 시 항목이 늘어나는지 확인(후 원복).

## Self-Review 결과

- **Spec 커버리지:** 데이터(헬퍼)·마크업·스타일·reduced-motion/반응형 정리·검증 모두 Task 1 스텝에 대응.
- **Placeholder:** 없음. 모든 스텝에 실제 코드/명령 포함.
- **타입 일관성:** `fmtDate(d: Date): string`, `getCategoryLabel(slug: string): string` 사용처와 일치. 새 클래스명(`.feat`, `.feat-meta`, `.feat-title`, `.feat-desc`, `.feat-sub`, `.featured-list`, `.featured-section`)이 마크업(Step 3)과 스타일(Step 4)에서 정확히 일치.
