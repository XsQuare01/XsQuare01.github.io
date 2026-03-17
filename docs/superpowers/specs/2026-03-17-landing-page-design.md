# 대문(Landing) 페이지 디자인 스펙

**날짜:** 2026-03-17
**프로젝트:** XsQuare01.github.io (Astro 기반 기술 블로그)

---

## 목표

GitHub README 스타일의 대문 페이지를 `/`에 만든다.
기존 글 목록은 `/blog`로 이동한다.
사이드바에 "홈" 링크를 추가하고 "글 목록" 링크를 `/blog`로 변경한다.

---

## 라우팅 변경

| 경로 | 변경 전 | 변경 후 |
|------|---------|---------|
| `/` | 글 목록 | 대문 페이지 |
| `/blog` | 없음 | 글 목록 (신규) |
| `/blog/{id}` | 글 상세 | 글 상세 (변경 없음) |

**Post URL 참고:** Astro v6 Content Layer API에서 `post.id`는 파일 경로 기반 ID(`interesting-number-paradox`)이며, 글 상세 링크는 `/blog/{post.id}`로 이미 통일되어 있음. 신규 글 목록 페이지도 동일하게 사용.

---

## 변경 파일

| 파일 | 작업 |
|------|------|
| `src/pages/index.astro` | 대문 페이지로 전면 교체 |
| `src/pages/blog/index.astro` | 신규 생성 — 기존 `index.astro`의 글 목록 로직 이동 |
| `src/layouts/BaseLayout.astro` | 사이드바 항목 수정 |

`src/pages/blog/index.astro`는 기존 `src/pages/blog/[...slug].astro`와 동일 디렉터리에 공존하며, Astro가 `/blog`를 `index.astro`로, `/blog/{id}`를 `[...slug].astro`로 라우팅한다.

---

## 사이드바 변경 (`BaseLayout.astro`)

변경 후 사이드바 메뉴 항목 (순서대로):

| 텍스트 | href | 활성 조건 |
|--------|------|----------|
| 🏠 홈 | `/` | `currentPath === '/'` |
| 📝 글 목록 | `/blog` | `currentPath.startsWith('/blog')` |
| 📂 카테고리 | `/categories` | `currentPath.startsWith('/categories')` |
| 🏷️ 태그 | `/tags` | `currentPath.startsWith('/tags')` |

---

## 대문 페이지 구조 (`src/pages/index.astro`)

### 섹션 1: 프로필 헤더

```html
<section>
  <h1>XsQuare01</h1>
  <p>기록하는 개발자</p>
  <p>📍 Seoul &nbsp;·&nbsp;
    <a href="https://github.com/XsQuare01" target="_blank" rel="noopener noreferrer">GitHub</a>
    &nbsp;·&nbsp;
    <a href="mailto:mystic6113@naver.com">이메일</a>
  </p>
</section>
```

### 섹션 2: 기술 스택

제목: `🛠 Tech Stack`

shields.io 배지 목록 (실제 URL):

| 배지 | URL |
|------|-----|
| Kotlin | `https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white` |
| Python | `https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white` |
| C++ | `https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white` |
| Astro | `https://img.shields.io/badge/Astro-FF5D01?style=flat&logo=astro&logoColor=white` |
| TypeScript | `https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white` |
| Git | `https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white` |

스타일: `display: flex; flex-wrap: wrap; gap: 0.4rem`

### 섹션 3: GitHub Stats

제목: `📊 GitHub Stats`

`theme=dark`를 사용하며, 이는 블로그의 어두운 배경(`--bg: #0f1117`)과 시각적으로 어울리도록 의도된 선택이다.

이미지 두 개를 나란히 표시:
```html
<div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
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
```

`bg_color=0f1117`로 블로그 배경색과 일치시킨다.

### 섹션 4: 최근 포스트

제목: `📝 Recent Posts`

`getCollection('posts')`로 가져온 뒤 날짜 기준 내림차순 정렬, 최대 5개 표시.
날짜 포맷: `date.toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric' })` (기존 페이지와 동일)
링크: `/blog/{post.id}`
스타일: 기존 `.post-list`, `.post-item`, `.post-item-date`, `.post-item-title`, `.post-item-desc` 클래스 재사용.

### 섹션 5: 프로젝트 & 관심사 (데모)

제목: `🚀 Projects & Interests`

아래는 **데모 콘텐츠**이며 나중에 실제 내용으로 교체한다:

| 이름 | 설명 |
|------|------|
| 이 블로그 | Astro로 만든 개인 기술 블로그 |
| 암호학 | 수학적 기반의 암호 이론 공부 |
| 알고리즘 | 문제 해결과 복잡도 이론 |

각 항목: `<strong>이름</strong> — 설명` 형식, `<ul>` 목록으로 표현. 링크 없음.

---

## 섹션 공통 스타일

- 섹션 제목: `<h2>` — 기존 `.prose h2` 스타일이 적용되려면 `<div class="prose">` 안에 래핑하거나, 동일한 스타일을 직접 적용
- 섹션 간 간격: `margin-bottom: 2.5rem`
- 전체 컨테이너: 기존 `.main-wrap` 사용 (별도 wrapper 불필요)

**참고:** `.prose h2` 스타일은 `.prose` 클래스 하위에서만 동작한다. `index.astro`에서 `<div class="prose">` 전체를 감싸거나, 섹션 제목에 개별 스타일을 인라인으로 적용한다. **전체를 `.prose`로 감싸는 방식을 선택한다.**

---

## 비변경 범위

- `/blog/[...slug]` 글 상세 페이지 변경 없음
- 카테고리, 태그 페이지 변경 없음
- `global.css` 변경 없음 (기존 스타일 재사용)
- footer 변경 없음
