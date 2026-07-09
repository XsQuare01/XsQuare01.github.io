# 볼록 껍질 ③ — Plane Sweeping과 동적 갱신 (포스트 설계)

- 날짜: 2026-07-09
- 상태: 승인됨 (사용자 확인)
- 원본 자료: 노션 `Convex hull 2` 노트의 Plane Sweeping·Dynamic Case 섹션
- 선행 포스트: `src/content/posts/convex-hull-2.md` (PR #29, 머지됨)

## 목표

볼록 껍질 시리즈 3편. 2편이 예고한 대로 Plane Sweeping($O(N^2)$에서 출발해 균형
이진 트리로 $O(N \log N)$)을 다루고, 점이 하나씩 추가되는 Dynamic Case를 글의
클라이맥스로 얹는다. 노션 `Convex hull 2` 노트의 Divide and Conquer는 4편,
Farthest Point(Rotating Calipers)는 5편으로 남긴다.

## 스코프 결정 (브레인스토밍 확정)

- $O(N \log N)$ BST 접선 찾기의 **이진 탐색 방향 판정(뚫고 들어감/나감 CCW
  케이스 분석)**은 본문에 넣지 않는다. 본문은 "BST면 이진 탐색으로 $O(\log N)$에
  접선을 찾을 수 있다"는 아이디어까지만. 상세는 별도 '추가 설명' 페이지로 분리
  (feedback-hard-topics-separate-page 방침).
- '추가 설명' 페이지는 **3편 이후 별도 작업**. 3편 본문은 죽은 링크 없이
  "다음 글에서 상세히 다룬다"는 예고 형태로 forward reference만 둔다.
- Dynamic Case는 **독립 섹션이자 글의 클라이맥스**. Plane Sweeping에서 만든
  BST/접선 도구의 재사용이 보상임을 강조한다.

## 파일 / 메타데이터

- 본문: `src/content/posts/convex-hull-3.md`
- 이미지: `public/images/convex-hull-3/*.svg` (1·2편 스타일 유지)
- frontmatter
  - title: "볼록 껍질 ③ — Plane Sweeping과 동적 갱신"
  - date: 2026-07-09T09:00:00 (실제 작성일 기준)
  - tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Plane Sweeping"]
  - category: algorithm
  - difficulty: 중급

## 본문 구성

1. **되짚어보기 & 새 질문**
   - 1·2편은 점을 전부 미리 알고 껍질을 한 번 구했다.
   - 이번 편의 두 관점: (가) 점을 x좌표 순으로 하나씩 삼키며 껍질을 키우는
     Plane Sweeping, (나) 다 구한 뒤에도 점이 계속 추가되는 Dynamic Case.
   - 1편의 세 가정(x·y좌표 서로 다름, 일직선 3점 없음) 유지 명시.
2. **껍질을 반으로 나누기**
   - 가장 왼쪽·오른쪽 점 기준으로 껍질을 **upper hull / lower hull** 두 사슬로
     분해하는 어휘 확립.
   - 이 분해가 스위핑·동적 갱신·(4편 분할정복)의 공통 토대임을 짧게.
3. **Plane Sweeping — $O(N^2)$**
   - 스위핑 라인 왼쪽→오른쪽(실제로는 점 이벤트마다 점프).
   - 새로 들어온 점은 항상 가장 오른쪽 → 현재 껍질에 위/아래 접선 긋고 두 접점
     사이 점을 버린 뒤 새 점을 붙인다.
   - 접선을 모든 껍질 점 훑어 찾으므로 걸음당 $O(N)$, 전체 $O(N^2)$.
   - 접선이 안 잡히는 경계 경우(새 점이 최상/최하단) 짧게.
4. **$O(N \log N)$으로 — 균형 BST 아이디어**
   - 매 걸음 껍질을 다 훑는 낭비 → 껍질 점을 균형 이진 트리에 y좌표 순 저장.
   - 접선을 이진 탐색으로 $O(\log N)$에.
   - 점 삽입 $O(\log N)$, 삭제 총합은 "각 점 한 번 삽입·최대 한 번 삭제"라
     $O(N)$ → 전체 $O(N \log N)$.
   - 이진 탐색 방향 판정 케이스 분석은 다음 '추가 설명' 글 예고(죽은 링크 아님).
5. **Dynamic Case — 클라이맥스**
   - 껍질을 다 구한 뒤에도 점이 하나씩 추가되면? 매번 재계산은 아깝다.
   - 껍질이 BST에 upper/lower 두 사슬로 있으니:
     - **안쪽 추가** → 껍질 불변. 점이 어느 사슬 위/아래인지 이진 탐색+CCW로 판정.
     - **바깥 추가** → 접선 2개 찾아 사이 잘라내고 붙임.
   - 3·4절 도구의 재사용이 곧 보상. 상세 접선 찾기는 추가 설명으로.
6. **핵심 정리 + 이어지는 글**
   - 4편 예고: Divide and Conquer(공통 접선으로 두 껍질 merge, $O(N \log N)$).

## SVG 도판 (5장)

1. upper/lower hull 분해 — 최좌·최우 점 기준 두 사슬.
2. $O(N^2)$ 접선 찾기 — 새 점(최우) + 위·아래 접선 + 버려지는 점.
3. 접선 후 새 껍질 — 갱신 결과.
4. BST 접선 아이디어 — 껍질 점이 트리에 저장되고 이진 탐색으로 접선(개념도).
5. Dynamic 안쪽/바깥쪽 추가 대비 — 안쪽(불변) vs 바깥(접선 2개 splice).

스타일: 1·2편 `public/images/convex-hull-{1,2}/*.svg`와 동일 팔레트(배경
`#0f1117`, 초록 `#34d399`, 파랑 `#93c5fd`/`#3b82f6`, 빨강 `#ef4444`/`#f87171`,
각주 `#94a3b8`)와 viewBox 규칙.

## 작업 절차 / 제약

- 모든 작업은 `feat/post-convex-hull-3` 브랜치에서. main 직접 커밋 금지.
- 코드는 실행 코드보다 의사코드 수준 C++, 컴파일 검증 불필요.
- 작성 후 `/review-post convex-hull-3`로 내용·문체·SVG 리뷰.
- 리뷰 반영 후 PR(Why 충분히, How 방법론 중심).

## 성공 기준

- 2편이 예고한 Plane Sweeping($O(N^2)$ → BST $O(N \log N)$)을 모두 전달.
- Dynamic Case가 도구 재사용의 보상으로 자연스럽게 이어진다.
- 어려운 이진 탐색 케이스 분석을 본문에 억지로 넣지 않고 예고로 남긴다.
- 1·2편과 문체·구성(callout, 핵심 정리, 이어지는 글)이 일관된다.
