# Scheduling Problem 1편 포스트 설계서

작성일: 2026-06-08
출처: Notion "Scheduling Problem 1" (페이지 ID `150cb27e-4930-80f1-8d86-e137f55056e0`, 부모: "알고리즘 수업 정리")

## 목표

Notion의 "Scheduling Problem 1" 노트를 Astro 블로그의 알고리즘 카테고리 포스트로 옮긴다. 기존 `greedy.md`·`mst.md`와 동일한 구조·문체·시각 양식을 따라, **데드라인 스케줄링 문제 → greedy 전략 → 정확성 증명 → 성능**을 모두 담는다.

## 작업 환경

- PR 워크플로 준수: 새 feature 브랜치에서 작업, main 직접 커밋 금지.
- 브랜치명: `feat/post-scheduling-1`

## 산출물

### 1. 포스트 파일

- 경로: `src/content/posts/scheduling-1.md` (기존 `dijkstra-1.md` 명명 규칙)
- 프론트매터 (`src/content/config.ts` 스키마 준수):
  - `title`: "데드라인 스케줄링 — 이익을 최대로 만드는 greedy 배치"
  - `date`: 2026-05-28T09:00:00 (greedy 05-18, MST 05-23 이후 흐름)
  - `description`: 문제·greedy·증명·성능을 요약한 2~3문장
  - `tags`: `["Algorithm", "Greedy", "Scheduling", "Exchange Argument"]`
  - `category`: `algorithm`
  - `difficulty`: `중급`

### 2. SVG 다이어그램

- 경로: `public/images/scheduling/timeline.svg`
- 내용: 예시 할 일 $\{(2,2),(1,3),(1,1)\}$에서 시간 슬롯 1·2에 $(1,3)$, $(2,2)$를 배치하고 $(1,1)$은 버려지는 greedy 배치 과정.
- 양식: 기존 `public/images/greedy/shortest-path.svg` 양식 그대로.
  - viewBox `0 0 720 360`, 다크 배경 `#0f1117`, rx 10
  - 제목/부제, 강조색(파랑 `#3b82f6`/`#93c5fd`, 주황 `#f97316`/`#fb923c`, 초록 `#22c55e`/`#4ade80`), 회색 보조 텍스트 `#64748b`
  - 하단 legend + 이탤릭 각주

## 본문 구조

`greedy.md` 스타일을 그대로 따른다: 도입 blockquote → 목차 callout → 본문 섹션 → 핵심 정리 callout → 다음 포스트 callout.

1. **도입 blockquote** — 마감 기한이 있는 여러 일 중 이익을 최대로 챙기는 문제 제기.
2. **목차 callout** (`이 포스트에서 다루는 내용`) — 4개 항목.
3. **## 데드라인 스케줄링 문제** — 조건($N$개의 일, $J_i=(D_i,P_i)$, 작업당 1시간), 예시 $\{(2,2),(1,3),(1,1)\}$와 최선의 해 $(1,3)\to(2,2)$.
4. **## Greedy 전략** — 직관적 가정 3가지(모든 $D_i \le N$, 이익 내림차순 정렬 가능, 최적 스케줄에서 모든 일은 마감을 지킴) + 실행 규칙(이익 큰 일부터, 가능하면 마감기한에 최대한 가깝게 배치). 이 자리에 SVG 삽입.
5. **## 정확성 증명** — Invariant 정의(상태 $A$가 $J_i$까지 본 시점에 대응하는 최적해 $S$가 존재하며 $j \le i$에 대해 등장 여부·위치가 일치) + 교환 논증.
   - Base: $i=0$, vacuously true.
   - Step: $J_{i+1}$ 처리 3경우.
     1. 놓을 수 없는 경우 ($D_{i+1}$ 전 빈자리 없음 → $S$에도 없음).
     2. $t$시간에 놓는 경우 — (a) $S$의 $t$가 비면 모순, (b) $S$의 $t$에 $J_x$($x>i+1$)면 $P_x \le P_{i+1}$이므로 교환, $P_x=P_{i+1}$.
     3. $S$의 $t'$에 $J_{i+1}$이 이미 있는 경우 — $t'=t$ 가능, $t'>t$ 불가, $t'<t$는 자리 교환으로 처리.
   - 증명 마무리는 callout으로 요약.
6. **## 성능** — naive $O(N^2)$(원소 $N$개 × 마감기한 $N$→0 선형 탐색) → Balanced Tree로 "$D_i$ 이하 최대값" 질의·삭제·재배열을 $O(\log N)$에 처리하여 전체 $O(N \log N)$.
7. **핵심 정리 callout** (`callout-key`).
8. **다음 포스트 callout** — Scheduling Problem 2편 예고.

## 수식 표기

기존 포스트와 동일하게 KaTeX 인라인 `$...$` / 블록 `$$...$$` 사용. Notion의 `` $`...` `` 표기는 `$...$`로 변환.

## 검증

- `npm run build`로 빌드 통과 확인 (content collection 스키마·KaTeX 렌더링 검증).
- 가능하면 review-post skill로 내용·문체·SVG 리뷰.

## 범위 밖 (Out of scope)

- Scheduling Problem 2편 작성 (별도 포스트).
- 기존 포스트 수정·리팩터링.
