# TOC (Table of Contents) 디자인 스펙

**날짜:** 2026-03-17
**프로젝트:** XsQuare01.github.io (Astro 기반 기술 블로그)

---

## 목표

글 상세 페이지에서 우측 스티키 패널에 h2 기반 목차(TOC)를 표시한다.
스크롤 위치에 따라 현재 읽고 있는 섹션이 목차에서 하이라이트된다.
다른 페이지(홈, 글 목록 등)에서는 우측 패널이 비어있는 상태를 유지한다.

---

## 데이터 흐름 (prop 방식으로 통일)

```
[...slug].astro
  └─ render(post) → { Content, headings }
  └─ h2Headings = headings.filter(h => h.depth === 2)
  └─ <PostLayout headings={h2Headings} ...>

PostLayout.astro
  └─ headings prop 수신
  └─ <BaseLayout ...>
       └─ <Fragment slot="toc"> TOC 마크업 </Fragment>  ← PostLayout이 직접 생성
     </BaseLayout>
  └─ <script> IntersectionObserver 포함

BaseLayout.astro
  └─ <aside class="right-panel">
       <slot name="toc" />   ← PostLayout의 Fragment가 여기 주입됨
     </aside>
```

PostLayout이 headings를 받아 TOC 마크업을 직접 만들어 BaseLayout의 `toc` 슬롯에 주입한다. `[...slug].astro`는 named slot을 직접 다루지 않는다.

---

## 변경 파일

| 파일 | 작업 |
|------|------|
| `src/pages/blog/[...slug].astro` | `render(post)`에서 headings 추출, h2만 필터해서 PostLayout prop으로 전달 |
| `src/layouts/PostLayout.astro` | `headings` prop 추가, `<Fragment slot="toc">` 로 TOC 마크업 생성, IntersectionObserver 스크립트 |
| `src/layouts/BaseLayout.astro` | `.right-panel` 안에 `<slot name="toc" />` 추가 |
| `src/styles/global.css` | TOC 관련 스타일 추가 |

---

## 각 파일 상세

### `src/pages/blog/[...slug].astro`

```astro
const { Content, headings } = await render(post);
const h2Headings = headings.filter((h) => h.depth === 2);
```

`h2Headings`를 PostLayout에 prop으로 전달:

```astro
<PostLayout
  title={post.data.title}
  date={post.data.date}
  description={post.data.description}
  tags={post.data.tags}
  headings={h2Headings}
>
  <Content />
</PostLayout>
```

각 heading 객체: `{ depth: number, slug: string, text: string }`
- `slug`: Astro가 자동 생성한 id (본문 h2 태그의 `id` 속성과 일치)
- 링크: `#${heading.slug}`

---

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
const { title, date, description, tags = [], headings = [] } = Astro.props;
```

`<BaseLayout>` 호출 시 `<Fragment slot="toc">`로 TOC 마크업을 toc 슬롯에 주입.
headings가 비어있으면 Fragment를 렌더링하지 않는다:

```astro
<BaseLayout title={title} description={description}>
  {headings.length > 0 && (
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
  )}
  <article>
    ...
  </article>
</BaseLayout>
```

**IntersectionObserver 스크립트** (PostLayout의 `<script>` 태그, 클라이언트에서 실행):

- 본문의 모든 `h2[id]` 요소를 관찰
- `rootMargin: '0px 0px -80% 0px'` — 화면 상단 20% 영역에 h2가 진입할 때 active
- h2 진입 시 해당 `#${id}`의 `.toc-link`에 `.active` 추가, 기존 active 제거

---

### `src/layouts/BaseLayout.astro`

`.right-panel`의 빈 주석을 `<slot name="toc" />`로 교체:

```astro
<aside class="right-panel">
  <slot name="toc" />
</aside>
```

---

### `src/styles/global.css`

```css
/* ── TOC ── */
.toc { padding-top: 0.5rem; }

.toc-title {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-dim);
  margin-bottom: 0.75rem;
}

.toc-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.toc-link {
  font-size: 0.82rem;
  color: var(--text-muted);
  display: block;
  line-height: 1.4;
  transition: color 0.15s;
}

.toc-link:hover { color: var(--text); }
.toc-link.active { color: var(--accent); font-weight: 600; }
```

---

## 비변경 범위

- 홈, 글 목록, 카테고리, 태그 페이지: toc 슬롯에 아무것도 주입하지 않으므로 `.right-panel`이 자동으로 빔
- 기존 `.right-panel` CSS (width, sticky 등) 변경 없음
