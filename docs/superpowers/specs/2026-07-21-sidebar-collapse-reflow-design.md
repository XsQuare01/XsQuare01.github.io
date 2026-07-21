# 사이드바 접힘/펼침 재배열(리플로우) 제거 설계

- 날짜: 2026-07-21
- 브랜치: `fix/sidebar-collapse-reflow`
- 관련: 이전 육안 리뷰 지적("왼쪽 사이드바가 전체 페이지와 볼 때 별로") 중 **접힘/펼침 시 카테고리 재배열** 부분

## 배경 / 문제

좌측 레일은 접힘(폭 `--rail-w` 3.9rem)에서 호버/포커스 또는 pin 시 14rem로 펼쳐진다. 이때 **카테고리 목록이 실시간으로 재배열되며 튀는** 현상이 거슬린다.

근본 원인 두 가지가 겹친다.

1. 레일 폭이 3.9rem→14rem로 **애니메이션되는 동안** 내부 flex 컬럼이 그 시점의 중간 폭으로 레이아웃된다. 콘텐츠가 8rem→…→14rem로 계속 다시 흐른다.
2. `.rail-txt`(라벨)와 `.rail-expand-only`(카테고리·태그)가 `display: none ↔ block/inline`으로 **즉시** 켜져, 애니메이션 중간에 삽입되며 재배열을 유발한다.

## 결정 (브레인스토밍 확정, 프로토타입 승인)

접힘/펼침 기능·항목 구성·아이콘·시각 스타일은 **유지**하고, 재배열만 제거한다. 프로토타입에서 동작 확인 완료.

## 상세 설계 — "고정 폭 내부 + 클립 + 페이드"

1. **고정 폭 내부 래퍼.** `.sidebar`의 자식들을 `.sidebar-inner`로 감싸고 `width: var(--rail-expanded)`(14rem)로 **고정**한다. 콘텐츠는 레일 실제 폭과 무관하게 항상 14rem 기준으로 레이아웃 → 폭이 변해도 재배열이 없다. 기존 `.sidebar`의 `padding`·flex 컬럼 배치는 `.sidebar-inner`로 옮긴다.
2. **클립으로 드러내기.** `.sidebar`는 이미 `overflow-x: hidden`. 접힘(3.9rem) 때 내부의 왼쪽(아이콘)만 보이고 나머지는 잘려 가려진다. 펼침은 폭만 커져 이미 완성된 레이아웃을 드러낼 뿐이다. 폭 트랜지션은 유지.
3. **display 토글 → opacity/visibility 페이드.** `.rail-txt`·`.rail-expand-only`(그리고 브랜드 텍스트·`kbd`·푸터)의 표시 전환을 `display` 대신 `opacity`/`visibility` 트랜지션으로 바꾼다. 접힘: `opacity: 0; visibility: hidden`(레이아웃은 그대로 점유하되 투명). 펼침(호버/포커스/pin): `opacity: 1; visibility: visible`. 레이아웃 불변이라 자리 이동 없이 페이드만 되고, 아이콘 옆 라벨이 반쯤 잘려 보이는 것도 방지된다.

### 접힘 상태의 카테고리 영역

프로토타입 승인대로, 접힘 때 카테고리/태그 영역은 **자리를 유지하되 투명**하다(완전히 접어 없애지 않음). 세로로 긴 레일(`min-height: 100vh`)에서 중간 빈 공간은 자연스럽다.

### 보존할 동작

- 호버/포커스 확장 오버레이(`box-shadow`), pin 고정(`html.rail-pinned`), 모바일 드로어(`@media`에서 `translateX`).
- 모바일 드로어는 항상 14rem로 펼쳐지므로, 기존 `@media`의 `display` 규칙을 **opacity/visibility 가시 상태**로 치환해 드로어 안 콘텐츠가 모두 보이게 한다.
- `prefers-reduced-motion`: 폭·opacity 트랜지션 모두 `none`.

## 파일 영향

- `src/layouts/BaseLayout.astro` — `.sidebar` 자식 전체를 `.sidebar-inner`로 래핑.
- `src/styles/global.css` — `.sidebar-inner` 규칙 추가(고정 폭·padding·flex), `.rail-txt`/`.rail-expand-only`의 display 토글 규칙(라인 118~125, 1165~1166 모바일 포함)을 opacity/visibility 방식으로 교체, `--rail-expanded` 토큰 추가, reduced-motion 갱신.

## 검증

정적 사이트(유닛 테스트 없음).

- `npm run build` 성공.
- 육안: 접힘→펼침 시 **카테고리 재배열/튐 없음**(폭 드러내기 + 페이드만). 접힘 상태엔 아이콘만 보이고 카테고리 텍스트 슬라이버가 새지 않음. pin 고정·해제 정상. 모바일 드로어에서 라벨·카테고리·태그 모두 보임.
- reduced-motion 환경에서 즉시 전환(애니메이션 없음).

## 범위 밖 (YAGNI)

- 사이드바 시각 스타일 전면 개편(색·아이콘·타이포), 내비 항목 재구성, 접힘/펼침 기능 자체 제거.
- 데스크톱 오버레이 vs 푸시 정책 변경.

## 리스크

- `display` 토글이 여러 셀렉터(기본·`rail-pinned`·`:hover`·`:focus-within`·모바일 `@media`)에 흩어져 있어, 전부 opacity/visibility로 일관 치환해야 한다(누락 시 접힘 상태 이상).
- `visibility: hidden` 요소가 포커스 순환에 남지 않도록 확인(접힘 시 키보드 포커스가 숨은 링크로 가지 않게 — 필요 시 `.sidebar:not(:hover):not(:focus-within):not(.pinned)`에서 pointer-events/inert 고려). 단, 현재도 `:focus-within`으로 펼쳐지므로 포커스 진입 시 보인다.
