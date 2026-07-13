# 볼록 껍질 ④ — 분할 정복과 공통 접선 (포스트 설계)

- 날짜: 2026-07-13
- 상태: 승인됨 (사용자 확인)
- 원본 자료: 노션 `Convex hull 2` 노트의 Divide and Conquer 섹션
- 선행 포스트: `src/content/posts/convex-hull-3.md` (PR #30, 머지됨) — 4편을 예고함
- 관련: `src/content/posts/convex-hull-bst-tangent.md` (PR #31, 추가 설명 — BST 접선)

## 목표

볼록 껍질 시리즈 4편. 3편이 예고한 대로 점들을 절반으로 갈라 각각의 껍질을
재귀로 구한 뒤, 두 껍질을 **공통 접선(common tangent)** 으로 잇는 **Divide and
Conquer**를 다룬다. 정렬에서 본 merge sort의 재귀 구조가 기하에서 어떻게 다시
나타나는지 보이는 것이 글의 뼈대다. 노션 `Convex hull 2` 노트의
Farthest Point(Rotating Calipers, 지름)는 5편으로 남긴다.

## 스코프 결정 (브레인스토밍 확정)

- 공통 접선 찾기를 **두 방법 모두 본문에서 본격적으로** 다룬다.
  1. **선형 워킹 O(N)**: 두 껍질의 포인터를 조금씩 전진시켜 상·하 공통 접선을
     찾는 고전적 방법. merge O(N) → 전체 O(N log N)이 merge sort의 선형 merge와
     정확히 대응한다는 점을 강조한다.
  2. **이진 탐색 O(log²N)**: 한 hull 점을 고정하고 다른 hull에서 접점을
     O(log N) 이진 탐색(3편 BST 접선과 같은 도구), 고정점을 O(log N)번 이동 →
     공통 접선 O(log²N).
- **핵심 단서**: 이진 탐색으로 접선을 O(log²N)에 찾아도, merge 배열 재구성이
  O(N)이라 D&C **총복잡도는 O(N log N)으로 그대로**다. 이진 탐색 접선이 값진
  경우는 껍질 배열을 새로 만들 필요가 없는 상황(3편 동적/BST 갱신)이며, 그쪽으로
  연결한다.
- difficulty는 **심화** (선형 워킹은 심화, 이진 탐색 접선은 고급 구간).
- upper/lower hull + x-단조 사슬 어휘는 3편에서 확립한 것을 그대로 재사용한다.

## 파일 / 메타데이터

- 본문: `src/content/posts/convex-hull-4.md`
- 이미지: `public/images/convex-hull-4/*.svg` (1~3편 스타일·팔레트 유지)
- frontmatter
  - title: "볼록 껍질 ④ — 분할 정복과 공통 접선"
  - date: 2026-07-13T09:00:00 (실제 작성일 기준)
  - tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Divide and Conquer"]
  - category: algorithm
  - difficulty: 심화

## 본문 구성

1. **되짚어보기 & 새 질문** (도입 blockquote)
   - 1·2편은 점을 전부 미리 늘어놓고 훑었고, 3편은 하나씩 더했다.
   - 4편은 **나눠서 각각 풀고 합친다.** 정렬의 merge sort 재귀가 기하에 다시.
   - 1편의 세 가정(x·y좌표 서로 다름, 일직선 3점 없음) 유지 명시.
2. **목차 callout** + 가정 재사용 문단.
3. **나누기 — merge sort의 기하 버전**
   - x좌표로 정렬 후 절반으로 split, 좌/우 부분 껍질을 재귀로 구한다.
   - base case(점 2~3개는 그 자체가 껍질).
   - `T(N) = 2T(N/2) + merge` 형태 예고. merge sort와 같은 뼈대.
   - upper/lower 사슬 어휘를 3편에서 이어받아 각 부분 껍질도 두 사슬로 본다.
4. **합치기의 핵심은 공통 접선**
   - 두 볼록 다각형을 함께 떠받치는 **상·하 공통 접선(upper/lower common
     tangent)** 정의.
   - 접선만 찾으면 merge가 왜 끝나는가: 상·하 접선의 바깥 사슬을 잇고, 두 접선
     사이에서 서로 마주 보는 점들은 새 경계 안쪽에 갇혀 버려진다.
5. **선형 워킹으로 공통 접선 — O(N)**
   - 왼 껍질 최우점 ↔ 오른 껍질 최좌점에서 시작.
   - 하단 공통 접선: 두 점을 잇는 직선이 양쪽 껍질을 모두 아래로 떠받칠 때까지,
     각 hull의 포인터를 CCW 판정으로 한 칸씩 전진. 상단 접선은 대칭.
   - C++ 의사코드(1편 `ccw`/`struct P` 재사용).
   - 전진 총횟수가 껍질 점 수에 선형이라 접선 찾기 O(N).
6. **merge와 전체 복잡도**
   - merge = 접선 찾기 O(N) + 바깥 사슬 이어붙이기 O(N) = O(N).
   - `T(N) = 2T(N/2) + O(N) = O(N log N)`. merge sort와 정확히 같은 재귀.
7. **접선을 더 빨리 — 이진 탐색 O(log²N)**
   - 한 hull 점을 고정하면, 다른 hull에서 그 점에 대한 접점은 사슬이 단조로우니
     O(log N) 이진 탐색으로 찾힌다(3편 BST 접선과 같은 도구).
   - 고정점 자체도 O(log N)번의 이진 탐색으로 옮기면 공통 접선 O(log²N).
   - **단, merge 배열 재구성이 O(N)이라 D&C 총복잡도는 O(N log N) 그대로.**
   - 이진 탐색 접선이 진짜 값진 경우: 껍질을 새로 안 만들어도 되는 상황
     (3편 동적/BST 갱신)으로 연결.
8. **핵심 정리** (callout-key, 4개 항목)
9. **이어지는 글** (callout)
   - 5편 예고: Farthest Point / 지름(Rotating Calipers) — 미발행이라 텍스트만.
   - closest-pair 시리즈 링크.

## SVG 도판 (4장)

1. `dc-split.svg` — 점을 x좌표 기준 절반으로 가르고 좌/우 부분 껍질.
2. `dc-tangent.svg` — 좌/우 껍질 + 상·하 공통 접선, 접선 바깥 유지·사이 안쪽 버림.
3. `dc-walking.svg` — 선형 워킹: 포인터가 전진하며 접선을 좁혀 가는 스냅샷.
4. `dc-binary-tangent.svg` — 고정점에서 다른 hull로 접점을 이진 탐색하는 방향 판정.

스타일: 1~3편 `public/images/convex-hull-{1,2,3}/*.svg`와 동일 팔레트(배경
`#0f1117`, 제목 `#e2e8f0`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`, 파랑
`#93c5fd`/`#3b82f6`(채움 `#1e3a5f`), 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`)와
viewBox ~680×420 규칙. 시리즈 도판과 같은 점 배치를 공유해 장면 연속성 유지.

## 작업 절차 / 제약

- 모든 작업은 `feat/post-convex-hull-4` 브랜치에서. main 직접 커밋 금지.
- 코드는 실행 코드보다 의사코드 수준 C++, 컴파일 검증 불필요.
- `npm run build`로 content collection 스키마 + KaTeX 파싱 검증.
- 작성 후 `/review-post convex-hull-4`로 내용·문체·SVG 리뷰, 반영 후 재빌드.
- 리뷰 반영 후 PR(Why 충분히, How 방법론 중심, 참조 코드 위치 섹션).

## 성공 기준

- 3편이 예고한 Divide and Conquer(공통 접선 merge, O(N log N))를 전달한다.
- 선형 워킹 O(N)과 이진 탐색 O(log²N) 두 방법을 모두 본격적으로 다루되, 총복잡도
  O(N log N)의 근거(merge O(N) 지배)를 정확히 밝힌다.
- merge sort 재귀 구조와의 대응이 독자에게 분명히 남는다.
- 1~3편과 문체·구성(callout, 핵심 정리, 이어지는 글)이 일관된다.
