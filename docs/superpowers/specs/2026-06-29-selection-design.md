# Selection Problem 포스트 설계

작성일: 2026-06-29
브랜치: `feat/post-selection`
소스 오브 트루스: Notion "Selection Problem" 노트 (부모: 알고리즘 수업 정리 → 전공 과목 페이지)

## 배경과 목표

알고리즘 시리즈의 다음 글. 직전 글 `quicksort`(퀵 정렬 평균 분석)에 이어, 퀵소트의 partition을 재활용하는 **selection problem**($k$번째 작은 원소 찾기)을 다룬다.

노션 노트의 프레이밍을 충실히 따른다. 표준 교과서의 "median of medians(BFPRT)"와 결론은 같지만, 노트는 **approximate median = 가운데 40%**라는 독자적 프레이밍을 쓴다. 이를 유지한다.

## 산출물 (글 3개)

같은 `posts` 컬렉션. 공통: `category: algorithm`, `date: 2026-06-29T09:00:00`(작성일 기준 — 시리즈 순서 아님).

### ① 메인 글 — `src/content/posts/selection.md`
- slug: `selection`, difficulty: `심화`
- tags: `["Algorithm", "Selection", "Quickselect", "Median of Medians", "Linear Time"]`
- 구성:
  1. **동기** — 퀵소트 최악 $O(n^2)$ 복습 → best pivot을 $O(n)$에 찾으면 최악도 $O(n\log n)$ 보장 → 그것이 selection problem. (callout "이 포스트에서 다루는 내용")
  2. **정의** — $a_1,\ldots,a_n$ 중 $k$번째 수. max/min/median 모두 동일한 문제.
  3. **naive와 하한** — 정렬 후 인덱싱 $O(n\log n)$. "selection은 sorting보다 쉬운 문제"(정렬 = $n$개의 selection을 푼 것). 모든 수를 봐야 하므로 $\Omega(n)$. 다른 수들의 대소관계를 대부분 몰라야 함(다 알면 그건 정렬).
  4. **quickselect** — 아무 pivot이나 잡아 partition($O(n)$), $k$가 있는 **한쪽으로만** 재귀. 최선 $S(n)=n+S(n/2)=O(n)$(등비수열), 최악 $S(n)=n+S(n-1)=O(n^2)$. "대부분 $O(n)$이지만 worst case가 불안" → **추가설명 A 링크**(평균이 정말 $O(n)$인지).
  5. **approximate median** — 정확한 중앙값 불필요. $u+v=n$, 보통 $u=0.3n$ → 가운데 40% 안의 값이면 충분. $Q(n)=n+Q(n/4)+Q(3n/4)=O(n\log n)$ 직관(중앙 근처만 잡아도 $O(n\log n)$ 유지).
  6. **median of medians (5개씩)** — $n$개를 5개씩 그룹 → 각 정렬($O(n)$) → 그룹 중앙값 $X$ → $X$들의 중앙값 $X'$. $X'$은 최소 30%보다 크고 최소 30%보다 작음 보장(블루/퍼플 박스: 가로 $n/10$, 세로 3 → $0.3n$). → **추가설명 B 링크**(왜 하필 5개인지).
  7. **분석** — $S(n)=A(n)+n+S(0.7n)$, $A(n)=n+S(0.2n)$(5묶음 정렬 $O(n)$ + 중앙값들 $n/5=0.2n$개에서 재귀). 합쳐 $S(n)=2n+S(0.2n)+S(0.7n)=O(n)$. 귀납법으로 $S(n)=an+b$ 가정 → $a=10,b=0$ 증명.
  8. **결론 (callout "핵심 정리")** — 이론적으로 $O(n)$ 선택 가능. 그러나 상수와 메모리 때문에 실전에선 정렬 후 $k$번째 찾기가 더 빠름. selection만 떼서 푸는 경우는 드뭄($n$이 매우 크지 않은 한).

### ② 추가설명 A — `src/content/posts/selection-average.md`
- slug: `selection-average`, difficulty: `심화`
- 제목: "quickselect는 왜 평균 $O(n)$인가"
- tags: `["Algorithm", "Selection", "Quickselect", "Expected Value", "추가 설명"]`
- 노트가 "대부분 $O(n)$"으로 얼버무린 부분을 엄밀히 채움.
- 기댓값 점화식 $E(n)=n+\frac1n\sum_{k=1}^{n}\max\!\big(E(k-1),E(n-k)\big)$ — quicksort와 달리 **한쪽만** 재귀하므로 $\max$.
- 상계로 전개해 $E(n)\le 4n=O(n)$ 상수까지 유도.
- 퀵소트의 $E(n)$(양쪽 재귀 → $n\log n$, `quicksort` 글)과 대비 — "한쪽만 재귀"라는 한 끗이 $n\log n$을 $n$으로 바꾼다.

### ③ 추가설명 B — `src/content/posts/selection-why-five.md`
- slug: `selection-why-five`, difficulty: `심화`
- 제목: "왜 하필 5개로 나누는가"
- tags: `["Algorithm", "Selection", "Median of Medians", "추가 설명"]`
- 그룹 크기 $g$ 일반화 → 보장 영역 유도.
- 선형이 되려면 두 부분문제 비율의 합 < 1.
  - $g=5$: $S(0.2n)+S(0.7n)$, $0.2+0.7=0.9<1$ ✓
  - $g=3$: 비율 합이 1이 되어 선형 깨짐 ✗
  - $g=7$: 되지만 그룹 내 정렬 비용 증가, 이득 없음
- 그룹 크기가 홀수여야 중앙값이 명확.

## SVG 다이어그램

기존 패턴(`/images/<slug>/*.svg`, 직전 글들과 같은 시각 언어) 따라 신규 제작.
- 메인 `/images/selection/`:
  - `quickselect-one-side.svg` — partition 후 $k$가 속한 한쪽으로만 재귀
  - `approximate-median.svg` — 가운데 40%, 좌우 30%, 최악 $0.7n$ 설명
  - `median-of-medians.svg` — 5×$(n/5)$ 격자, 그룹 중앙값 행, $X'$과 보장 박스(블루/퍼플)
- B `/images/selection-why-five/`:
  - `group-size-compare.svg` — 그룹 3 vs 5 보장 영역 비교

## 상호 링크

- 메인 → `quicksort`, `divide-and-conquer`, `sort`(정렬 후 인덱싱), 추가설명 A·B
- 추가설명 A → 메인, `quicksort`(E(n) 대비)
- 추가설명 B → 메인
- 메인 글 끝 "이어지는 글" callout에서 A·B 안내

## 작업 방식

- 브랜치 `feat/post-selection`, main 직접 커밋 금지(PR 워크플로).
- 글 작성 후 `review-post` 스킬로 내용·문체·SVG 리뷰.
- 완료 시 PR 생성.

## 비목표 (YAGNI)

- 무작위화 quickselect의 고급 분석(꼬리 확률 등)은 다루지 않음 — 추가설명 A는 기댓값 상계까지만.
- "추가 설명"을 위한 새 컬렉션/레이아웃은 만들지 않음 — 기존 posts 컬렉션 + 태그로 충분.
