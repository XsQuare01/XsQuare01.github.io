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

Astro 템플릿 표현식을 사용해 연도를 동적으로 처리한다:

```astro
<footer class="site-footer">
  <div class="site-footer-top">
    <span class="site-footer-name">XsQuare01</span>
    <span class="site-footer-bio">기록하는 개발자</span>
  </div>
  <div class="site-footer-bottom">
    <span>© {new Date().getFullYear()} XsQuare01</span>
    <a href="https://github.com/XsQuare01" target="_blank" rel="noopener noreferrer">GitHub</a>
    <a href="mailto:mystic6113@naver.com">이메일</a>
  </div>
</footer>
```

---

## 스타일 (CSS)

`src/styles/global.css`에 `.site-footer` 관련 클래스 추가.
`border-top` 라인은 `.main-wrap`의 전체 너비에 걸쳐 표시된다.

### `.site-footer`
| 속성 | 값 | 비고 |
|------|-----|------|
| border-top | `1px solid var(--border)` | 콘텐츠와 시각적 구분 |
| padding | `2.5rem 0` | 상하 여유 |
| margin-top | `3rem` | 콘텐츠와 간격 |

### `.site-footer-top`
| 속성 | 값 | 비고 |
|------|-----|------|
| display | `flex` | |
| flex-direction | `row` | 이름과 소개를 한 줄로 표시 |
| align-items | `center` | |
| gap | `0.5rem` | |

### `.site-footer-name`
| 속성 | 값 |
|------|-----|
| font-weight | `700` |
| color | `var(--text)` |

### `.site-footer-bio`
| 속성 | 값 |
|------|-----|
| color | `var(--text-muted)` |
| font-size | `0.85rem` |

### `.site-footer-bottom`
| 속성 | 값 | 비고 |
|------|-----|------|
| display | `flex` | |
| flex-direction | `row` | |
| flex-wrap | `wrap` | 좁은 화면에서 줄바꿈 허용 |
| align-items | `center` | |
| gap | `0.5rem 1rem` | 세로 0.5rem, 가로 1rem |
| font-size | `0.8rem` | |
| color | `var(--text-dim)` | copyright 텍스트 색상 |
| margin-top | `0.5rem` | top과의 간격 |

### 링크 색상
| 상태 | 값 |
|------|-----|
| 기본 | `var(--accent-2)` (#38bdf8) |
| hover | `var(--accent)` (#f97316) |

---

## 변경 파일

1. `src/layouts/BaseLayout.astro` — `<slot />` 아래에 `<footer>` 마크업 추가
2. `src/styles/global.css` — `.site-footer` 관련 스타일 추가

---

## 비변경 범위

- 사이드바 구조 및 기존 `sidebar-footer` 유지
- 모바일 레이아웃의 `body` 구조 변경 없음

---

## 구현 전 확인 사항

- `PostLayout.astro`가 `BaseLayout.astro`를 내부적으로 사용하는지 확인 필요.
  사용한다면 footer가 자동으로 포스트 페이지에도 적용됨.
  사용하지 않는다면 `PostLayout.astro`에도 동일하게 footer 추가 필요.
