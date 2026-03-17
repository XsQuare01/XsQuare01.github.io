# 대문(Landing) 페이지 디자인 스펙

**날짜:** 2026-03-17
**프로젝트:** XsQuare01.github.io (Astro 기반 기술 블로그)

---

## 목표

GitHub README 스타일의 대문 페이지를 `/`에 만든다.
기존 글 목록은 `/blog`로 이동한다.
사이드바에 "홈"과 "글 목록" 링크를 추가/수정한다.

---

## 라우팅 변경

| 경로 | 변경 전 | 변경 후 |
|------|---------|---------|
| `/` | 글 목록 | 대문 페이지 |
| `/blog` | 없음 | 글 목록 (기존 `/`의 내용) |

사이드바 "글 목록" 링크의 `href`를 `/blog`로 변경하고, "홈" 링크(`/`)를 추가한다.

---

## 페이지 구조 (세로 나열, GitHub README 스타일)

### 섹션 1: 프로필 헤더
- 이름: **XsQuare01**
- 한 줄 소개: `기록하는 개발자`
- 위치 + 링크: `📍 Seoul · GitHub(https://github.com/XsQuare01) · 이메일(mystic6113@naver.com)`
- 스타일: 큰 이름(`h1`), 소개는 subtitle, 링크는 accent-2 색상

### 섹션 2: 기술 스택
- 제목: `🛠 Tech Stack`
- 배지: `shields.io` 스타일 이미지 태그로 표현
- 데모 배지 목록: Kotlin, Python, C++, Astro, TypeScript, Git
- 스타일: `display: flex; flex-wrap: wrap; gap: 0.4rem`

### 섹션 3: GitHub Stats
- 제목: `📊 GitHub Stats`
- `github-readme-stats.vercel.app` 서비스의 이미지 두 개 embed:
  1. `https://github-readme-stats.vercel.app/api?username=XsQuare01&show_icons=true&theme=dark`
  2. `https://github-readme-stats.vercel.app/api/top-langs/?username=XsQuare01&layout=compact&theme=dark`
- `<img>` 태그로 삽입, `loading="lazy"`, `alt` 속성 포함

### 섹션 4: 최근 포스트
- 제목: `📝 Recent Posts`
- `getCollection('posts')`로 동적으로 가져와 날짜 기준 최신 5개 표시
- 각 항목: 날짜(mono font) + 제목(링크, `/blog/{id}`)
- 스타일: 기존 `.post-item` 스타일 재사용

### 섹션 5: 프로젝트 & 관심사
- 제목: `🚀 Projects & Interests`
- 데모 내용:
  - **이 블로그** — Astro로 만든 개인 기술 블로그
  - **암호학** — 수학적 기반의 암호 이론 공부
  - **알고리즘** — 문제 해결과 복잡도 이론
- 각 항목: 이름(굵게) + 대시 + 설명

---

## 섹션 공통 스타일

- 섹션 사이 구분: `<hr>` 또는 `margin: 2.5rem 0`
- 섹션 제목: `<h2>` (기존 `.prose h2` 스타일과 동일하게 적용)
- 전체 컨테이너: 기존 `.main-wrap` 사용 (별도 wrapper 불필요)

---

## 변경 파일

| 파일 | 작업 |
|------|------|
| `src/pages/index.astro` | 대문 페이지로 전면 교체 |
| `src/pages/blog/index.astro` | 신규 생성 — 기존 글 목록 내용 |
| `src/layouts/BaseLayout.astro` | 사이드바 "홈" 링크 추가, "글 목록" href → `/blog` |

---

## 비변경 범위

- 글 상세 페이지 (`/blog/[...slug]`) 변경 없음
- 카테고리, 태그 페이지 변경 없음
- CSS 변경 없음 (기존 스타일 재사용)
- footer 변경 없음
