# TOC (Table of Contents) 디자인 스펙

**날짜:** 2026-03-17
**프로젝트:** XsQuare01.github.io (Astro 기반 기술 블로그)

---

## 목표

글 상세 페이지에서 우측 스티키 패널에 h2 기반 목차(TOC)를 표시한다.
스크롤 위치에 따라 현재 읽고 있는 섹션이 목차에서 하이라이트된다.
다른 페이지(홈, 글 목록 등)에서는 우측 패널이 비어있는 상태를 유지한다.

---

## 데이터 흐름

```
[...slug].astro
  └─ render(post) → { Content, headings }
     └─ headings.filter(h => h.depth === 2) → PostLayout (prop)

PostLayout.astro
  └─ headings prop으로 TOC 마크업 생성
     └─ <Fragment slot="toc"> → BaseLayout의 toc 슬롯 주입
     └─ <script> IntersectionObserver 포함

BaseLayout.astro
  └─ .right-panel 안에 <slot name="toc" />
```

---

## 변경 파일

| 파일 | 작업 |
|------|------|
| `src/pages/blog/[...slug].astro` | `render(post)`에서 headings 추출, PostLayout에 전달 |
| `src/layouts/PostLayout.astro` | `headings` prop 추가, TOC 마크업 + IntersectionObserver 스크립트 |
| `src/layouts/BaseLayout.astro` | `.right-panel` 안에 `<slot name="toc" />` 추가 |
| `src/styles/global.css` | TOC 관련 스타일 추가 |

---

## 각 파일 상세

### `src/pages/blog/[...slug].astro`

`render(post)`가 반환하는 `headings`에서 `depth === 2`인 항목만 필터링해서 `PostLayout`에 prop으로 전달.

```astro
const { Content, headings } = await render(post);
const h2Headings = headings.filter((h) => h.depth === 2);
```

각 heading 객체 형태: `{ depth: number, slug: string, text: string }`
- `slug`: Astro가 자동 생성한 id (해당 h2 태그의 `id` 속성과 일치)
- 링크: `#${heading.slug}`

### `src/layouts/PostLayout.astro`

Props에 `headings` 추가:

```ts
interface Props {
  title: string;
  date: Date;
  description?: string;
  tags?: string[];
  headings?: { slug: string; text: string }[];
}
```

TOC 마크업을 `<Fragment slot="toc">`로 BaseLayout의 toc 슬롯에 주입:

```astro
<Fragment slot="toc">
  <div class="toc">
    <div class="toc-title">목차</div>
    <ul class="toc-list">
      {headings.map((h) => (
        <li>
          <a class="toc-link" href={`#${h.slug}`}>{h.text}</a>
        </li>
      ))}
    </ul>
  </div>
</Fragment>
```

headings가 비어있으면 Fragment를 렌더링하지 않는다.

**IntersectionObserver 스크립트** (`<script>` 태그, 클라이언트 실행):

- 본문의 모든 `h2` 요소를 관찰
- h2가 뷰포트 상단 20% 안에 들어오면 해당 slug의 `.toc-link`에 `.active` 클래스 추가
- 이전 active 항목의 `.active` 클래스 제거
- `rootMargin: '0px 0px -80% 0px'` 사용 (상단 20% 영역 기준)

### `src/layouts/BaseLayout.astro`

`.right-panel` 안에 slot 추가:

```astro
<aside class="right-panel">
  <slot name="toc" />
</aside>
```

### `src/styles/global.css`

```css
.toc { ... }
.toc-title { font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
             letter-spacing: 0.08em; color: var(--text-dim); margin-bottom: 0.75rem; }
.toc-list { list-style: none; display: flex; flex-direction: column; gap: 0.35rem; }
.toc-link { font-size: 0.82rem; color: var(--text-muted); transition: color 0.15s;
            display: block; line-height: 1.4; }
.toc-link:hover { color: var(--text); }
.toc-link.active { color: var(--accent); font-weight: 600; }
```

---

## 비변경 범위

- 홈, 글 목록, 카테고리, 태그 페이지 — toc 슬롯에 아무것도 주입하지 않으므로 `.right-panel`이 자동으로 빔
- 기존 `.right-panel` CSS 변경 없음
