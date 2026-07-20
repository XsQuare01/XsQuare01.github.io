# 작은 한글 UI 라벨 타이포그래피 정리 (#42)

- 날짜: 2026-07-20
- 이슈: #42 — 아이콘·메타데이터 UI 라벨의 한글 타이포그래피 개선
- 브랜치: `feat/label-typography-42`

## 배경

제목·본문 폰트는 자연스러우나, 아이콘 주변·메타데이터 영역의 **작은 한글 라벨**이 어색하다. 원인은 별도 아이콘 폰트 문제가 아니라, 작은 UI 라벨에 서로 다른 폰트·크기·자간 규칙이 혼재한 것이다. 네 갈래로 정리한다.

- **A. 폰트 미로딩** — `--font-sans` 1순위가 `Pretendard`인데 웹폰트/로컬 폰트를 로드하지 않아, 방문자 OS마다 fallback이 달라진다.
- **B. 영문용 규칙의 한글 오용** — 작은 라벨에 `text-transform: uppercase` + 넓은 자간(0.07~0.12em)이 걸려, 한글에선 uppercase가 무의미하고 자간만 벌어져 어색하다.
- **C. mono 상속** — 글 상세 breadcrumb·읽기 시간의 한글이 `--font-mono`를 상속해 모노 폰트의 CJK fallback으로 찍힌다.
- **D. raw slug 노출** — 홈 피드·검색 결과가 카테고리 slug(`algorithm`)를 그대로 출력해, 다른 화면의 라벨(`알고리즘`)과 불일치한다.

## 결정 사항 (브레인스토밍 확정)

- **A: 시스템 스택** — 웹폰트를 도입하지 않고, 한글까지 커버하는 시스템 sans 스택으로 교체. 추가 네트워크 0, 모든 방문자에게 일관된 fallback.
- **B: 한글은 자연스럽게** — 한글 포함 라벨에서 uppercase 제거, 자간 0. 순수 영문 라벨이 남아 있으면 거기만 기존 eyebrow 유지. (조사 결과 대상 라벨은 모두 한글/혼합이라 일괄 적용한다.)
- **C: 한글 산문은 mono에서 제외** — 해당 컨테이너를 sans로 바꾸되 숫자는 `tabular-nums`로 정렬감 유지. 코드블록·인라인 코드 등 의도된 mono는 불변. 터미널 크롬 정체성은 유지.
- **D: slug → label 매핑** — 이미 존재하는 `getCategoryLabel()`로 표기 통일. 검색은 한글 매칭도 개선.

## 상세 설계

### A. 폰트 스택

`src/styles/global.css`의 `--font-sans` 토큰을 교체한다.

```
/* before */
--font-sans: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
/* after */
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
```

- Mac/iOS = Apple SD Gothic Neo, Windows = Malgun Gothic, 그 외 = Noto Sans KR(설치 시) → sans-serif 순으로 자연 fallback.
- 웹폰트 링크·@font-face 추가 없음.

### B. eyebrow / 소형 라벨

아래 5개 셀렉터에서 `text-transform: uppercase`를 제거하고 `letter-spacing`을 0으로 둔다. 현재 mono인 항목은 sans로 바꾼다. (이 5개가 저장소 내 uppercase 사용처 전부다.)

| 셀렉터 | 위치 | 텍스트(예) | 현재 | 조치 |
|---|---|---|---|---|
| `.sidebar-nav-label` | global.css:188 | 카테고리 | uppercase, ls .12em, sans | uppercase 제거, ls 0 |
| `.section-label` | index.astro(스코프) / global.css:878 | 주제별 현황 | uppercase, ls .1em | uppercase 제거, ls 0 (중복 정의 정리) |
| `.toc-title` | global.css:625 | 목차 | mono, uppercase, ls .08em | **sans**, uppercase 제거, ls 0 |
| `.callout-title` | global.css:730 | 이 포스트에서 다루는 내용 등(한글/혼합) | uppercase, ls .11em, sans | uppercase 제거, ls 0 |
| `.post-category-badge` | global.css:1112 | 알고리즘 | uppercase, ls .07em | uppercase 제거, ls 0 |

- `.section-label`이 index.astro 스코프와 global.css 양쪽에 정의돼 있으면 중복을 확인해 한쪽으로 정리한다(기능 변화 없이).
- `.callout-title`은 모든 포스트 콜아웃 제목의 인상을 바꾼다(대문자화된 라틴 용어가 저자 원래 대소문자로 복원됨). 의도된 변경으로 포함하되, 사용자 스펙 리뷰에서 확인 대상으로 명시한다.

### C. 메타 폰트(mono → sans)

| 셀렉터 | 위치 | 조치 |
|---|---|---|
| `.post-breadcrumb` | global.css:376 | `font-family`를 mono → `var(--font-sans)` |
| `.reading-time` | global.css:712 | mono → `var(--font-sans)`, `font-variant-numeric: tabular-nums` 유지/추가 |

- 구현 시 `.post-meta` 하위의 다른 요소(날짜 등)가 mono를 상속하는지 확인해, 한글이 섞이면 동일 처리.

### D. 카테고리 표기 매핑

1. **홈 피드** — `src/pages/index.astro:116`
   ```
   // before
   <span class="feed-cat">{post.data.category ?? '—'}</span>
   // after
   <span class="feed-cat">{post.data.category ? getCategoryLabel(post.data.category) : '—'}</span>
   ```
   (`getCategoryLabel`는 이미 import되어 있음.)

2. **검색 인덱스** — `src/pages/search-index.json.ts`
   - `category: post.data.category ?? ''` → `category: post.data.category ? getCategoryLabel(post.data.category) : ''`
   - 효과: 배지 표기가 라벨(`알고리즘`)로 바뀌고, Fuse의 `category` 필드 매칭이 한글 검색어에도 걸린다.
   - `getCategoryLabel`은 미매칭 slug에 대해 slug를 그대로 반환하므로 안전.

3. **검색 렌더러** — `src/layouts/BaseLayout.astro:348` `badge.textContent = item.category;` 는 인덱스가 라벨을 담으면 자동으로 라벨을 표시 → **코드 변경 없음**.

## 파일 영향 요약

- `src/styles/global.css` — A(토큰), B(5개 셀렉터), C(2개 셀렉터)
- `src/pages/index.astro` — B(`.section-label` 중복 정리), D(피드 라벨)
- `src/layouts/PostLayout.astro` — 변경 없음(스타일은 global.css에서 처리; 확인만)
- `src/pages/search-index.json.ts` — D(라벨 emit)

## 검증

정적 사이트로 유닛 테스트가 없다. 각 단계를 **빌드 성공 + 산출물/육안 확인**으로 게이트한다.

- `npm run build` 성공.
- 홈(`/`) — 피드 카테고리 배지가 `알고리즘`/`웹 개발` 등 라벨로 표시.
- 글 상세 — breadcrumb·읽기 시간이 sans로 렌더, 숫자 정렬 유지. 목차 제목 `목차`가 sans·정상 자간.
- 사이드바 — `카테고리` 라벨 자간 정상.
- 검색 모달 — 결과 배지가 라벨로 표시되고, `알고리즘` 검색 시 매칭.
- 산출물 grep — `dist`의 홈/검색 인덱스에 raw slug 배지 노출이 없음.

## 범위 밖 (YAGNI)

- 웹폰트 도입(A에서 시스템 스택 선택으로 불필요).
- 본문 세리프·터미널 팔레트·다이어그램 플레이트 변경.
- 아이콘 SVG 교체, 난이도 별표(`★☆☆`) 로직 변경.
- 블로그 목록·태그·글상세 카테고리 배지(이미 `getCategoryLabel` 사용 중).

## 리스크

- `.callout-title` 변경이 전 포스트 콜아웃 인상을 바꾼다 → 스펙 리뷰에서 확인.
- 시스템 스택은 OS별 자형이 미세하게 다르다(의도된 트레이드오프). Pretendard 미로딩 상태보다 오히려 일관적.
