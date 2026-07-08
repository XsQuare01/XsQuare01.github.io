# 볼록 껍질 ② — Graham Scan과 정렬 하한 (포스트 설계)

- 날짜: 2026-07-08
- 상태: 승인됨 (사용자 확인)
- 원본 자료: 노션 `Convex hull 1` 노트의 Graham Scan 섹션 (하한 논증 포함)
- 선행 포스트: `src/content/posts/convex-hull-1.md` (PR #28, 머지됨)

## 목표

볼록 껍질 시리즈 2편. 1편이 예고한 대로 Graham Scan($O(N \log N)$)과
"볼록 껍질은 정렬만큼 어렵다"는 $\Omega(N \log N)$ 하한 논증을 다룬다.
노션 `Convex hull 2` 노트(Plane Sweeping, Divide and Conquer, Dynamic,
Farthest Point)는 3편 이후 재료로 남긴다.

## 파일 / 메타데이터

- 본문: `src/content/posts/convex-hull-2.md`
- 이미지: `public/images/convex-hull-2/*.svg` (1편 스타일 유지)
- frontmatter
  - title: "볼록 껍질 ② — Graham Scan과 정렬 하한"
  - date: 2026-07-08 (실제 작성일 기준)
  - tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Graham Scan"]
  - category: algorithm
  - difficulty: 중급

## 본문 구성

1. **되짚어보기 — Package Wrapping의 한계**
   - 1편 요약: CCW, Package Wrapping $O(NH)$, 최악 $O(N^2)$.
   - 문제 제기: 걸음마다 나머지 전체를 다시 훑는 것이 낭비다.
2. **아이디어 — 각도 정렬을 한 번만**
   - 최하단 점 $Y$ 기준으로 나머지 점을 각도순으로 한 번만 정렬.
   - 각도(삼각함수) 대신 CCW 비교자로 정렬 — 1편의 "각도가 아니라 CCW" 원칙 재사용.
   - 정렬 후에는 점들을 순서대로 도는 것이 껍질 후보 순회가 된다.
3. **Graham Scan — 스택으로 좌회전만 남기기**
   - 절차: 처음 두 점 push → 새 점마다 좌회전이면 push, 우회전이면 좌회전이
     될 때까지 pop.
   - 단계별 그림으로 push/pop 장면 제시.
   - 처음 두 점이 제거되지 않는 근거(모든 점이 그 왼쪽에 있음).
   - 각 점은 최대 1번 push, 1번 pop → 스캔 $O(N)$, 전체는 정렬이 지배해
     $O(N \log N)$.
   - C++ 의사코드 수준 코드 (1편의 `ccw`, `struct P` 재사용).
4. **더 빠를 수는 없을까 — 정렬 하한**
   - 환원: 숫자들을 각도로 바꿔 원 위의 점으로 변환 → 볼록 껍질을 구하면
     껍질 위 인접 순서가 곧 정렬 결과.
   - 볼록 껍질이 $o(N \log N)$이면 정렬도 그보다 빨라져 모순.
   - "비교 기반(결정 트리) 모델에서의 하한"이라는 조건을 callout으로 한 줄
     정직하게 언급.
5. **핵심 정리 + 이어지는 글**
   - 3편 예고: Plane Sweeping (노션 `Convex hull 2` 노트).

## SVG 도판 (4~5장)

1. 각도 정렬 개념도 — $Y$ 기준 각도순 번호 매기기.
2. 스택 push 장면 — 좌회전이라 쌓이는 경우.
3. 스택 pop 장면 — 우회전 발생, 좌회전이 될 때까지 제거.
4. 하한 환원 — 숫자 → 원 위 점 → 껍질 순회 = 정렬 순서.
5. (선택) 완성된 껍질과 스캔 경로 전체 그림.

스타일: 1편 `public/images/convex-hull-1/*.svg`와 동일한 팔레트·선 굵기·
라벨 규칙.

## 작업 절차 / 제약

- 모든 작업은 `feat/post-convex-hull-2` 브랜치에서. main 직접 커밋 금지.
- 코드는 완전한 실행 코드보다 의사코드 수준 C++, 컴파일 검증 불필요.
- 작성 후 `/review-post convex-hull-2`로 내용·문체·SVG 리뷰.
- 리뷰 반영 후 PR 생성 (Why 충분히, How는 방법론 중심).

## 성공 기준

- 1편에서 예고한 두 주제(Graham Scan, 하한)를 모두 다룬다.
- 1편과 문체·구성(callout, 핵심 정리, 이어지는 글)이 일관된다.
- 하한 논증이 모델 조건을 과장 없이 서술한다.
