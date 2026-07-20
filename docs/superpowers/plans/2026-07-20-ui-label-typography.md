# 작은 한글 UI 라벨 타이포그래피 정리 (#42) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 작은 한글 UI 라벨(사이드바·메타·배지·목차·콜아웃)의 폰트·자간·표기를 정리해 어색함을 제거한다.

**Architecture:** CSS 토큰 1곳(`--font-sans`)과 몇 개 셀렉터를 손보고, 홈 피드·검색 인덱스에서 카테고리 slug를 라벨로 매핑한다. 신규 파일·의존성 없음.

**Tech Stack:** Astro 정적 사이트, 순수 CSS, TypeScript(콘텐츠 API·검색 인덱스 엔드포인트).

## Global Constraints

- 유닛 테스트 없음 → 각 태스크 검증은 **`npm run build` 성공 + 산출물/소스 grep + 육안**.
- 커밋 메시지에 `Co-Authored-By` 트레일러를 넣지 않는다(블로그 저장소 관례).
- 브랜치: `feat/label-typography-42` (이미 생성됨). main 직접 커밋 금지.
- 콘텐츠 마크다운(`src/content/posts/**`)과 SVG는 변경하지 않는다.
- 폰트 시스템 스택(정확히): `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif`

---

### Task 1: A — 폰트 시스템 스택 전환

**Files:**
- Modify: `src/styles/global.css:57`

**Interfaces:**
- Consumes: 없음
- Produces: `--font-sans` 토큰(전 컴포넌트가 참조). 값만 바뀌고 이름·용법 불변.

- [ ] **Step 1: 현재 상태 확인**

Run: `grep -n "font-sans" src/styles/global.css | head -1`
Expected: `57:  --font-sans: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;`

- [ ] **Step 2: 토큰 교체**

`src/styles/global.css:57`을 아래로 바꾼다.

```css
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
```

- [ ] **Step 3: 빌드**

Run: `npm run build`
Expected: `Complete!` (에러 없음)

- [ ] **Step 4: 검증**

Run: `grep -c "Pretendard" src/styles/global.css`
Expected: `0`

- [ ] **Step 5: 커밋**

```bash
git add src/styles/global.css
git commit -m "fix(font): 한글 UI 라벨 sans를 시스템 스택으로 (Pretendard 미로딩 제거)"
```

---

### Task 2: B — 소형 라벨 uppercase·자간 정리

한글 라벨에서 `text-transform: uppercase`와 넓은 자간을 제거한다. **영문 라벨 `.example-label`("Example")은 eyebrow를 유지**한다(공유 규칙에서 분리). `.toc-title`은 mono→sans도 겸한다.

**Files:**
- Modify: `src/styles/global.css` — 188(`.sidebar-nav-label`), 625–633(`.toc-title`), 730–738(`.callout-title`), 877–893(`.example-label,.section-label` 공유 규칙 + `.example-label` 블록), 1112–1126(`.post-category-badge`)

**Interfaces:**
- Consumes: Task 1의 `--font-sans`
- Produces: 없음(스타일만)

- [ ] **Step 1: 현재 uppercase 사용처 확인 (기준선)**

Run: `grep -c "text-transform: uppercase" src/styles/global.css`
Expected: `5`

- [ ] **Step 2: `.sidebar-nav-label` (188행) 교체**

```css
.sidebar-nav-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0; color: var(--ink-faint); margin: 1rem 0 0.4rem 0.55rem; }
```

- [ ] **Step 3: `.toc-title` (625–633행) 교체 — sans + uppercase/자간 제거**

```css
.toc-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0;
  color: var(--ink-soft);
  font-family: var(--font-sans);
  margin-bottom: 0.85rem;
}
```

- [ ] **Step 4: `.callout-title` (730–738행) 교체**

```css
.callout-title {
  font-family: var(--font-sans);
  font-size: 0.64rem;
  font-weight: 700;
  letter-spacing: 0;
  color: var(--accent);
  margin-bottom: 0.4rem;
}
```

- [ ] **Step 5: 공유 규칙(877–887)에서 uppercase·자간 제거하고 영문 라벨로 이관**

`.example-label, .section-label { ... }` 공유 블록을 아래로 바꾼다(‑ `text-transform`·`letter-spacing` 제거).

```css
.example-label,
.section-label {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}
```

이어서 `.example-label` 전용 블록(889–893)에 영문 eyebrow 규칙을 추가한다.

```css
.example-label {
  color: var(--amber);
  background: var(--amber-soft);
  border: 1px solid var(--amber);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

> 참고: `.section-label`은 홈에서 `index.astro`의 스코프 스타일(1.2rem, uppercase 없음)이 우선하므로 홈은 영향 없음. 이 변경은 포스트 본문의 `증명`·`심화` 같은 한글 섹션 라벨에 적용된다. `.section-label-deep`는 자체 `letter-spacing: 0.04em`를 유지한다(그대로 둠).

- [ ] **Step 6: `.post-category-badge` (1112–1126행)에서 uppercase·자간 제거**

블록에서 `text-transform: uppercase;`와 `letter-spacing: 0.07em;` 두 줄을 삭제한다. 결과:

```css
.post-category-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  border: 1px solid;
  position: relative;
  z-index: 1;
  transition: opacity 0.2s;
  text-decoration: none;
}
```

- [ ] **Step 7: 빌드**

Run: `npm run build`
Expected: `Complete!`

- [ ] **Step 8: 검증 — uppercase는 영문 `.example-label`만 남는다**

Run: `grep -n "text-transform: uppercase" src/styles/global.css`
Expected: 정확히 **1줄**, `.example-label` 블록 내부.

- [ ] **Step 9: 커밋**

```bash
git add src/styles/global.css
git commit -m "fix(ui): 한글 소형 라벨 uppercase·자간 정리, 목차 제목 sans화 (영문 Example만 eyebrow 유지)"
```

---

### Task 3: C — 메타 폰트 mono→sans

글 상세 breadcrumb와 읽기 시간의 한글이 mono를 상속하는 문제를 sans로 바꾼다. 숫자 정렬감은 `tabular-nums`로 유지.

**Files:**
- Modify: `src/styles/global.css` — 371–379(`.post-breadcrumb`), 712–716(`.reading-time`)

**Interfaces:**
- Consumes: Task 1의 `--font-sans`
- Produces: 없음

- [ ] **Step 1: `.post-breadcrumb` (371–379행) — mono→sans**

블록의 `font-family: var(--font-mono);`를 아래로 바꾼다.

```css
  font-family: var(--font-sans);
```

- [ ] **Step 2: `.reading-time` (712–716행) 교체 — sans + tabular-nums**

```css
.reading-time {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  color: var(--text-dim);
  font-variant-numeric: tabular-nums;
}
```

- [ ] **Step 3: `.post-meta` 하위 다른 mono 상속 확인**

Run: `sed -n '411,430p' src/styles/global.css`
확인: 날짜 등 다른 메타 요소가 `var(--font-mono)`를 쓰고 그 안에 한글이 섞이면 동일하게 sans로 바꾼다. (없으면 조치 불필요.)

- [ ] **Step 4: 빌드**

Run: `npm run build`
Expected: `Complete!`

- [ ] **Step 5: 검증**

Run: `grep -A2 "^.post-breadcrumb {" src/styles/global.css | grep font-family; grep -A1 "^.reading-time {" src/styles/global.css | grep font-family`
Expected: 두 줄 모두 `var(--font-sans)`.

- [ ] **Step 6: 커밋**

```bash
git add src/styles/global.css
git commit -m "fix(ui): 글 상세 breadcrumb·읽기시간 한글을 mono에서 sans로 (숫자는 tabular-nums)"
```

---

### Task 4: D — 카테고리 slug→label 매핑

홈 피드와 검색 결과가 slug(`algorithm`)를 노출하는 문제를 `getCategoryLabel()`로 라벨(`알고리즘`) 표기로 통일한다.

**Files:**
- Modify: `src/pages/index.astro:116`
- Modify: `src/pages/search-index.json.ts` (import 추가 + `category` emit)

**Interfaces:**
- Consumes: `getCategoryLabel(slug: string): string` — `src/data/categories.ts` (미매칭 slug는 slug 그대로 반환)
- Produces: 검색 인덱스 JSON의 `category` 필드가 라벨 문자열이 됨 → `BaseLayout.astro:348`의 배지가 자동으로 라벨 표시(코드 변경 없음)

- [ ] **Step 1: 홈 피드 (index.astro:116) 교체**

현재:
```astro
          <span class="feed-cat">{post.data.category ?? '—'}</span>
```
로 바꾼다:
```astro
          <span class="feed-cat">{post.data.category ? getCategoryLabel(post.data.category) : '—'}</span>
```
(`getCategoryLabel`는 `index.astro`에 이미 import되어 있음 — `import { categories, getCategoryLabel } from '../data/categories';`)

- [ ] **Step 2: 검색 인덱스 import 추가**

`src/pages/search-index.json.ts` 상단 import 구역에 추가:
```ts
import { getCategoryLabel } from '../data/categories';
```

- [ ] **Step 3: 검색 인덱스 category emit 교체**

`index` 매핑에서
```ts
    category: post.data.category ?? '',
```
을
```ts
    category: post.data.category ? getCategoryLabel(post.data.category) : '',
```
로 바꾼다.

- [ ] **Step 4: 빌드**

Run: `npm run build`
Expected: `Complete!`

- [ ] **Step 5: 검증 — 홈/검색 인덱스에 라벨 표기**

Run: `grep -oE 'feed-cat">[^<]*' dist/index.html | sort -u`
Expected: `알고리즘`·`웹 개발` 등 한글 라벨(‘algorithm’ 같은 slug 없음).

Run: `grep -oE '"category":"[^"]*"' dist/search-index.json | sort -u`
Expected: 값이 한글 라벨(‘algorithm’ 등 slug 없음).

- [ ] **Step 6: 커밋**

```bash
git add src/pages/index.astro src/pages/search-index.json.ts
git commit -m "fix(ui): 홈 피드·검색 카테고리 표기를 slug에서 라벨로 (getCategoryLabel)"
```

---

## 최종 통합 검증 (전 태스크 후)

- [ ] `npm run build` 성공.
- [ ] 홈(`/`) 피드 배지가 라벨로 표시.
- [ ] 글 상세: breadcrumb·읽기시간 sans 렌더, `목차` 제목 sans·자연 자간.
- [ ] 사이드바 `카테고리` 라벨 자간 정상, 포스트 `증명`·`심화` 섹션 라벨 uppercase 없음, 콜아웃 제목 자연스러움.
- [ ] `Example` 라벨은 대문자 eyebrow 유지.
- [ ] 검색 모달에서 `알고리즘` 검색 시 결과 매칭 + 배지 라벨 표시.

## Self-Review 결과

- **Spec 커버리지:** A(Task 1)·B(Task 2)·C(Task 3)·D(Task 4) 전부 대응. 스펙의 `.section-label` "중복 정리"는 조사로 명확화됨 — 홈은 스코프 스타일로 이미 정상, global 규칙은 `.example-label`(영문 유지)과 포스트 `.section-label`(한글 정리)로 분리. 스펙보다 정밀해짐.
- **Placeholder:** 없음. 모든 스텝에 실제 코드/명령 포함.
- **타입 일관성:** `getCategoryLabel(string): string` 시그니처가 Task 4 두 사용처에서 일치.
