## 결정적 검사: src/content/posts/convex-hull-4.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/convex-hull-4.md

검토 범위: `src/content/posts/convex-hull-4.md` 전체, `docs/reviews/README.md`, 기존 스캐폴드, 그리고 본문이 참조한 SVG 4개를 모두 읽었다. SVG는 `public/images/convex-hull-4/dc-split.svg`, `public/images/convex-hull-4/dc-tangent.svg`, `public/images/convex-hull-4/dc-walking.svg`, `public/images/convex-hull-4/dc-binary-tangent.svg`를 본문 캡션과 대조했다.

| severity | source | rule_id | location | quote | message | recommendation | gate_effect |
|---|---|---|---|---|---|---|---|
| 🔴 | L | L7 | `src/content/posts/convex-hull-4.md:76` | `while (below(R[b], L[a], L[nextDown(a)])) { a = nextDown(a); moved = true; }` | `below(a, b, c)`가 70행에서 방향선 `a→b` 기준으로 정의됐는데, 왼쪽 후보 검사만 `R[b]→L[a]`로 뒤집혀 있다. 방향선 기준 아래쪽 판정은 끝점을 바꾸면 부호가 반대가 되므로, 하단 접선 워킹 의사코드가 본문 설명과 달라질 수 있다. | 왼쪽 후보도 같은 기준선 `L[a]→R[b]`에 대해 검사하도록 고치거나, `below`가 무방향 직선 기준이라는 별도 정의와 CCW 부호 변환을 명시한다. | fail |
| 🟡 | L | L7 | `src/content/posts/convex-hull-4.md:107` | `먼저 왼쪽 껍질의 한 점 $a$를 고정하면, $a$에서 오른쪽 껍질로 긋는 접선의 접점은 하나로 정해진다.` | 외부 점에서 볼록 다각형으로 긋는 접선은 일반적으로 상·하 두 개다. 문맥상 특정 사슬 또는 특정 방향의 접선을 말하는 듯하지만, 이 문장만 보면 접점이 항상 하나라는 말로 읽힌다. | “상단 접선을 찾는다고 고정하면”, “하단 사슬에서 찾는 접점은”처럼 대상 접선과 사슬을 먼저 제한해 모호성을 줄인다. | warn |
| 🟢 | L | L1 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | Korean declarative tone is consistent, and no actionable AI-style filler or register break was found. | info |
| 🟢 | L | L2 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | The section order moves from split, merge by tangents, linear walking, recurrence, then faster tangent search without a blocking flow gap. | info |
| 🟢 | L | L3 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | Terms such as upper hull, lower hull, 상단 공통 접선, 하단 공통 접선, merge, and CCW are used consistently for this post's register. | info |
| 🟢 | L | L4 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | All four referenced SVGs were read. The split direction, highlighted tangent endpoints, walking arrows, binary-search labels, captions, and body claims match the prose aside from the separate L7 pseudocode issue. | info |
| 🟢 | L | L5 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | The title and description match the actual scope: divide and conquer convex hull merging, common tangents, linear walking, binary-search tangent finding, and complexity limits. | info |
| 🟢 | L | L6 | not-recorded | not-recorded | 검토 완료, 이슈 없음 | Notion tools are unavailable in this session, so original-source comparison could not be performed. The review only checks the repository version against its own prose, math, and SVGs. | info |

요약: 🔴 1 · 🟡 1 · 🟢 6

## 반영 결과 (2026-07-13, 2차 리뷰)

- 🔴 [L7] `convex-hull-4.md:76` 선형 워킹 의사코드 방향 불일치 — **반영 완료**. `below(a,b,c)`(방향선 a→b 기준)를 `belowLine(p,q,c)`(두 점 p,q를 지나는 **무방향 직선** 기준)로 바꾸고, 두 검사 모두 같은 기준선 `L[a]–R[b]`를 쓰도록 통일했다(`belowLine(L[a], R[b], ...)`). 끝점을 뒤집던 둘째 검사의 부호 반전 문제 제거. 본문 프로세 표기도 `직선 a→b`→`직선 ab`(무방향)로 맞추고, 기준선이 세로가 아니라 '아래'가 잘 정의됨을 주석에 명시.
- 🟡 [L7] `convex-hull-4.md:107` 접선 접점 모호성 — **반영 완료**. "상단 공통 접선을 찾는다고 하고 … 외부 점 $a$에서 오른쪽 껍질로는 위·아래 두 접선이 나오지만, 그중 **상단 접선의 접점**은 하나로 정해진다"로 대상 접선(상단)과 사슬을 먼저 제한해 모호성 제거.
- 재검증: `npm run build` 성공(106 pages), `python .claude/review_post.py` 재실행 "발견 사항 없음 ✅".
- 참고(L6): 2차 리뷰는 세션에서 Notion 도구 미가용으로 원본 대조를 못 했다고 기록했으나, 1차 리뷰에서 `notion-fetch`로 `Convex hull 2` 원본을 확보해 대조를 이미 수행했다(원본 핵심 반영·누락 없음, 선형 워킹은 승인된 보강).
