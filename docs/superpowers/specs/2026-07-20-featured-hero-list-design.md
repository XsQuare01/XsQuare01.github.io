# 홈 '추천 글' 히어로 리스트 (N개 카테고리 대표) 설계

- 날짜: 2026-07-20
- 브랜치: `feat/featured-hero-list`
- 관련: #42/#47(UI 라벨·가독성)·#44/#43(홈 에디토리얼) 방향의 연장

## 배경

홈 첫 화면의 '추천 글'은 **2열 둥근 카드 + 왼쪽 액센트 바 + 카드 배경 채움 + 컬러 hover 글로우**(`box-shadow: -3px 0 0 accent, 0 0 0 1px rule` / `border-radius: 10px` / `background: var(--bg-card)` / hover `amber-soft`)를 쓴다. 이는 UI 리프레시(장식 절제·카드 남용 축소) 때 걷어낸 옛 카드 스타일이 남은 것으로, 지금 홈의 나머지(최근 글=테두리 없는 리스트, 카테고리=헤어라인 내비, 주제별 현황=막대)와 언어가 어긋나 featured만 겉돈다.

## 목표 / 결정 (브레인스토밍 확정)

- 단일 히어로가 아니라 **N편(수동 큐레이션) 대표 문건**을 헤어라인으로 구분한 세로 리스트로.
- 스타일은 채택안 **A(프레임 리드)**: 카드·바·글로우 제거, 헤어라인 규칙선 + 큰 세리프 제목으로 위상.
- 각 항목: **메타(카테고리[잉크블루 강조] · 날짜 · 난이도) + 큰 세리프 제목 + 2줄 설명**, 호버 시 제목이 잉크블루.
- 선택 = 기존 `FEATURED_IDS` 수동 목록을 N개로. 새 frontmatter·자동 추출 없음.
- 카테고리 토큰을 잉크블루로 강조해 "어느 큰 카테고리의 대표인지"가 먼저 읽히게 한다.

## 상세 설계

### 데이터

- `FEATURED_IDS` 배열(수동 큐레이션, N개)을 그대로 사용. 순서 = 표시 순서.
- 각 featured post에서 `title`, `description`, `date`, `category`, `difficulty` 사용.
- 카테고리 표기는 `getCategoryLabel(category)` (index.astro에 이미 import됨).
- 날짜 포맷: `YYYY.MM.DD` (예: `2026.03.25`), `tabular-nums`.
- `difficulty`·`description`은 **선택 필드** → 값이 있을 때만 렌더(없으면 해당 토큰·구분점 생략).

### 마크업 (index.astro의 featured 블록 교체)

섹션 헤딩은 **`.feed-head` + `.feed-label`을 재사용**해 '최근 글' 헤딩과 통일한다. 우측엔 '모두 보기' 링크 대신 작은 부제.

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

- `fmtDate(d)`: `${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}.${String(d.getDate()).padStart(2,'0')}` (프런트matter 스크립트에 헬퍼로 추가).
- 첫 토큰(카테고리)이 없을 수 있으면 구분점(`·`) 선행이 어색해질 수 있으므로, 카테고리 없는 글은 featured 대상에서 제외(현재 모든 후보에 category 존재). 구현 시 카테고리 유무에 따른 구분점 위치만 점검.

### 스타일 (index.astro scoped `<style>`)

제거: `.featured-grid`, `.featured`, `.featured-label`, `.featured-title`, `.featured-desc`, 그리고 반응형의 `.featured-grid` 규칙.

추가:

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

- 반응형 grid 규칙(`.featured-grid { grid-template-columns: 1fr }`) 삭제(리스트는 단일 열이라 불필요).
- `prefers-reduced-motion` 블록의 `.featured`·`.featured::after` 참조 제거. `.feat`는 색 전이만 있어 별도 처리 불필요(원하면 `.feat .feat-title { transition: none }` 추가 가능).

## 검증

정적 사이트(유닛 테스트 없음) → `npm run build` 성공 + 육안/grep.

- 빌드 성공.
- 홈 육안: '추천 글'이 헤어라인 구분 세로 리스트, 카드·바·글로우 없음, 카테고리 잉크블루, 호버 시 제목 잉크블루, 헤딩이 '최근 글'과 통일.
- `FEATURED_IDS`에 3번째 id를 임시로 추가해 항목이 늘어나는지 확인 후 원복(또는 사용자가 원하는 대표 목록으로 확정).
- 산출물 grep: `dist/index.html`에 `.featured`(옛 카드)·`old` 잔재 없음, `.feat-title` 존재.

## 범위 밖 (YAGNI)

- 카테고리별 자동 대표 추출, `featured: true` frontmatter 플래그.
- 카테고리별 그룹 헤더, '모두 보기' 링크, 난이도 별표(★☆☆) 표기.
- FEATURED_IDS 목록 내용 자체의 큐레이션(디자인이 아니라 편집 결정 — 사용자가 별도로 채움).

## 리스크

- difficulty 없는 글이 featured에 포함되면 메타 구분점 처리에 주의(값 유무로 토큰·`·` 동시 생략).
- `.feed-label` 재사용으로 '추천 글'과 '최근 글' 헤딩이 동일해짐 → 의도된 통일.
