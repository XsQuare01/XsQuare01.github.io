# Search Feature Design

**Date:** 2026-03-25
**Status:** Approved

## Summary

Fuse.js 기반 클라이언트 사이드 퍼지 검색. 사이드바 버튼 또는 ⌘K/Ctrl+K 단축키로 모달을 열고 포스트를 검색한다.

---

## Architecture

### Data Flow

1. **Build time**: Astro API endpoint(`src/pages/search-index.json.ts`)가 모든 포스트를 수집해 JSON 인덱스 생성
2. **Runtime**: 모달 최초 오픈 시 `/search-index.json` lazy fetch → Fuse.js 인스턴스 생성
3. **Search**: 입력마다 Fuse.js 검색 → 결과 렌더링 (debounce 불필요, 인덱스가 메모리에 있음)

### Search Index Schema

```ts
{
  id: string;        // post.id (URL slug)
  title: string;
  description: string;
  tags: string[];
  category: string;
}
```

### Fuse.js Config

```js
{
  keys: [
    { name: 'title',       weight: 0.5 },
    { name: 'description', weight: 0.25 },
    { name: 'tags',        weight: 0.15 },
    { name: 'category',    weight: 0.10 },
  ],
  threshold: 0.4,   // 퍼지 허용 범위 (0=완전일치, 1=모두매칭)
  minMatchCharLength: 2,
}
```

---

## Components

### `src/pages/search-index.json.ts`

- Astro API Route (GET)
- `getCollection('posts')`로 전체 포스트 수집
- `id`, `title`, `description`, `tags`, `category` 필드만 추출해 JSON 반환
- 빌드 시 정적 파일로 생성됨 (`/search-index.json`)

### Modal HTML (BaseLayout.astro에 추가)

```
#search-modal          — 전체 오버레이 (기본 display:none)
  .search-modal-box    — 중앙 박스
    .search-modal-input-row
      input#search-input
    #search-results    — 결과 목록
      .search-result-item  (반복)
        .search-result-title
        .search-result-badge  (카테고리)
```

### Sidebar Button (BaseLayout.astro에 추가)

사이드바 카테고리 섹션 위에 배치:
```html
<button id="search-btn">🔍 검색 <kbd>⌘K</kbd></button>
```

### JavaScript (BaseLayout.astro `<script>`)

**모달 열기/닫기:**
- `#search-btn` 클릭
- `Ctrl+K` / `⌘K` keydown
- `Esc` keydown으로 닫기
- 오버레이 클릭으로 닫기
- 열릴 때 `#search-input` focus

**검색 인덱스 로딩:**
- 모달 최초 오픈 시 `/search-index.json` fetch (이후 캐시)
- Fuse 인스턴스 생성 후 재사용

**결과 렌더링:**
- `input` 이벤트마다 `fuse.search(query)` 실행
- 최대 8개 결과 표시
- 빈 쿼리면 결과 초기화
- 각 결과: `<a href="/blog/{id}">` 클릭 시 페이지 이동

**키보드 내비게이션:**
- `↑` / `↓`: `.search-result-item` 간 포커스 이동
- `Enter`: 포커스된 결과 페이지 이동

### CSS (global.css에 추가)

- `#search-modal`: `position:fixed; inset:0; z-index:200; background:rgba(0,0,0,0.6)`
- `.search-modal-box`: 중앙 정렬, `max-width:520px`, `border-radius:12px`
- 다크/라이트 모드 모두 CSS 변수로 대응
- `.search-result-item:hover` / `.search-result-item.focused`: accent 하이라이트

---

## Dependencies

```bash
npm install fuse.js
```

Fuse.js는 ESM 지원. Astro 클라이언트 스크립트에서 `import Fuse from 'fuse.js'` 가능.

---

## File Changes

| 파일 | 변경 유형 |
|------|---------|
| `src/pages/search-index.json.ts` | 신규 생성 |
| `src/layouts/BaseLayout.astro` | 사이드바 버튼 + 모달 HTML + script 추가 |
| `src/styles/global.css` | 검색 모달 스타일 추가 |
| `package.json` | `fuse.js` 의존성 추가 |

---

## Out of Scope

- 한국어 형태소 분석 (Fuse.js 퍼지 매칭으로 충분)
- 검색 결과 URL 공유 (`/search?q=...`)
- 검색어 하이라이팅 (결과 내 매칭 텍스트 강조)
