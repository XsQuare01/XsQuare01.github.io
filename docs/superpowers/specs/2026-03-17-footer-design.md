# Footer 디자인 스펙

**날짜:** 2026-03-17
**프로젝트:** XsQuare01.github.io (Astro 기반 기술 블로그)

---

## 목표

메인 콘텐츠 영역 하단에 2단 구조의 footer를 추가한다.
모바일에서는 페이지 맨 아래에 위치한다.

---

## 위치

- `BaseLayout.astro`의 `.main-wrap` 내부, `<slot />` 아래에 `<footer class="site-footer">` 삽입
- 사이드바 영역에는 영향 없음 (기존 `sidebar-footer`의 copyright 텍스트는 그대로 유지)
- 모바일(`max-width: 768px`)에서는 기존 `body { flex-direction: column }` 레이아웃 덕분에 자동으로 맨 아래에 위치

---

## 구조 (HTML)

```html
<footer class="site-footer">
  <div class="site-footer-top">
    <span class="site-footer-name">XsQuare01</span>
    <span class="site-footer-bio">기록하는 개발자</span>
  </div>
  <div class="site-footer-bottom">
    <span>© {연도} XsQuare01</span>
    <a href="https://github.com/XsQuare01" target="_blank" rel="noopener">GitHub</a>
    <a href="mailto:mystic6113@naver.com">이메일</a>
  </div>
</footer>
```

- `{연도}`는 Astro에서 `new Date().getFullYear()` 동적 처리

---

## 스타일 (CSS)

`src/styles/global.css`에 `.site-footer` 클래스 추가:

| 속성 | 값 | 비고 |
|------|-----|------|
| border-top | `1px solid var(--border)` | 콘텐츠와 시각적 구분 |
| padding | `2.5rem 0` | 상하 여유 |
| margin-top | `3rem` | 콘텐츠와 간격 |
| `.site-footer-top` | flexbox, gap 0.5rem | 이름 + 소개 한 줄 |
| `.site-footer-name` | `font-weight: 700`, `var(--text)` | 굵게 |
| `.site-footer-bio` | `var(--text-muted)`, `font-size: 0.85rem` | 흐리게 |
| `.site-footer-bottom` | flexbox, gap 1rem, `font-size: 0.8rem`, `var(--text-dim)` | copyright + 링크 |
| 링크 색상 | `var(--accent-2)` (기본), `var(--accent)` (hover) | 기존 링크 스타일 준수 |

---

## 변경 파일

1. `src/layouts/BaseLayout.astro` — `<slot />` 아래에 `<footer>` 마크업 추가
2. `src/styles/global.css` — `.site-footer` 관련 스타일 추가

---

## 비변경 범위

- 사이드바 구조 및 기존 `sidebar-footer` 유지
- 모바일 레이아웃 구조 변경 없음 (기존 CSS로 자동 대응)
- 다른 페이지 레이아웃(`PostLayout.astro` 등) 별도 수정 불필요 — `BaseLayout`을 상속하므로 자동 적용
