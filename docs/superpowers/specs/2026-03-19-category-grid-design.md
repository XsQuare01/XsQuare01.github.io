# Category Page Grid Card Redesign — Design Spec

## Goal
카테고리 목록 페이지를 텍스트 리스트에서 2열 그리드 카드 레이아웃으로 변경한다.

## Design Decision
- 아이콘 없음
- 각 카드: 카테고리명(굵게) + 한 줄 설명(muted) + 포스트 수(오렌지)
- 2열 그리드

## Files to Change

### `src/data/categories.ts`
- `description` 필드 추가

### `src/pages/categories/index.astro`
- `.category-list` (ul/li 리스트) → 2열 그리드 카드로 교체
- 카드 클릭 시 해당 카테고리 페이지로 이동

## Card Structure
```
┌─────────────────────────┐
│ 수학                     │
│ 알고리즘과 암호학의 기초… │
│                     3편  │
└─────────────────────────┘
```

## Category Descriptions
- 수학: 알고리즘과 암호학의 기초가 되는 수리적 개념들
- 알고리즘: 문제 해결과 자료구조, 복잡도 분석
- 게임 개발: 게임 설계 패턴과 구현 경험
- 웹 개발: 프론트엔드, 백엔드, 인프라 경험
