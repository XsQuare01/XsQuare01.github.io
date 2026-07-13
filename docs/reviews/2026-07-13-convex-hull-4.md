## 결정적 검사: src/content/posts/convex-hull-4.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/convex-hull-4.md

### 🔴 [L4] public/images/convex-hull-4/dc-tangent.svg:16-17

- severity: 🔴
- source: L
- rule_id: L4
- location: public/images/convex-hull-4/dc-tangent.svg:16-17 (dc-walking.svg:23도 동일)
- quote: `<line x1="250" y1="315" x2="430" y2="320" stroke="#fbbf24" .../>` (하단 공통 접선)
- message: 하단 공통 접선을 왼쪽 껍질 (250,315)–오른쪽 껍질 (430,320)로 그렸는데, 왼쪽 껍질의 최하단 꼭짓점 (150,330)과 오른쪽 껍질의 최하단 꼭짓점 (540,335)이 이 접선을 연장한 직선보다 **아래**에 놓인다. 즉 두 껍질이 접선의 한쪽에 모이지 않아, 본문이 정의한 "두 껍질에 동시에 닿으면서 두 껍질을 모두 한쪽에 두는 직선"과 어긋난다. (250,315)/(430,320)은 실제 하단 접점이 아니다. dc-walking.svg의 최종 접선도 같은 좌표라 동일 문제.
- recommendation: 두 껍질의 최하단 바깥 꼭짓점을 접선 위로 올려 (250,315)/(430,320)이 실제 최하단 접점이 되게 한다. 예: 왼쪽 (150,330)→(150,300), 오른쪽 (540,335)→(540,300). 이러면 접선 위로 모든 점이 올라간다(검산: 직선 (250,315)-(430,320)에서 x=150일 때 y≈312 > 300, x=540일 때 y≈323 > 300). 네 도판(split·tangent·walking·binary-tangent)의 점 배치를 동일하게 갱신한다.
- gate_effect: fail

### 🟢 [L1] src/content/posts/convex-hull-4.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-4.md
- quote: "두 껍질을 합치는 이 접선 찾기가 바로 그 트리 기반 갱신의 심장이다."
- message: 검토 완료, 이슈 없음. 줄표는 결정적 검사 임계치 내이고 경구식 마무리·대칭 반복은 두드러지지 않는다. "다리처럼 잇는 변", "심장" 정도의 비유가 있으나 평이하고 설명을 돕는 수준이다.
- recommendation: 현재 문체 유지. 굳이 다듬는다면 "심장" 한 곳만 "핵심"으로 낮출 수 있다(선택).
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-4.md

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-4.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 나누기(merge sort 유비) → 공통 접선 정의 → 선형 워킹 O(N) → 전체 복잡도 → 이진 탐색 O(log²N)과 그 한계로 이어지는 흐름에 논리 도약이 없다.
- recommendation: 현재 설명 순서 유지.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-4.md

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-4.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. upper/lower hull, 사슬, 단조, 공통 접선, 최우점/최좌점, CCW 용어가 1~3편과 일관되게 쓰이고 어체(~다)도 통일돼 있다.
- recommendation: 현재 용어 체계 유지.
- gate_effect: info

### 🟢 [L4] SVG 전반 (split·binary-tangent 및 본문 대응)

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-4/dc-split.svg, dc-binary-tangent.svg
- quote: not-recorded
- message: 하단 접선 문제(위 🔴)를 제외하면 나머지 SVG↔본문 대응은 일치한다. dc-split의 좌/우 껍질과 x 중앙 분할, dc-tangent의 상단 접선·버려지는 안쪽 점(좌 최우점·우 최좌점), dc-walking의 시작 직선·전진 화살표, dc-binary-tangent의 고정점→접점 이진 탐색이 본문 서술과 대응한다.
- recommendation: 🔴 수정 시 네 도판 점 배치를 함께 맞춘다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-4.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-4.md:2-4
- quote: "볼록 껍질 ④ — 분할 정복과 공통 접선"
- message: 검토 완료, 이슈 없음. 제목과 description(선형 워킹 O(N), 이진 탐색 O(log²N), 복잡도의 진실)이 실제 내용을 대표한다.
- recommendation: 현재 frontmatter 유지.
- gate_effect: info

### 🟢 [L6] 노션 `Convex hull 2` 대조

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/convex-hull-4.md
- quote: "각 convex hull의 공통 접선을 다음과 같이 생성하면 된다 … 왼쪽 hull 점 1개당 O(log N), 오른쪽 점이 O(log N)개 → O(log²N) … merge O(N), height O(log N) → O(N log N). Merge sort와 시간이 동일." (노션 원본)
- message: 노션 원본(Divide and Conquer 섹션)을 notion-fetch로 가져와 대조했다. 원본의 핵심(최좌·최우 기준 upper/lower 분할, array 저장 merge O(N), 이진 탐색 공통 접선 O(log²N), 전체 O(N log N)=merge sort)이 모두 반영됐고 누락 없음. 원본의 O(log²N)이 총복잡도를 낮추지 못한다는 점("내보낼 점 찾고 merge O(N)")도 본문의 '복잡도의 진실' 문단으로 충실히 옮겼다. **선형 워킹 O(N) 접선 절은 노션 원본에 없는 추가분**이나, 이는 브레인스토밍에서 사용자가 "둘 다 본격적으로"로 명시 승인한 의도적 보강(hallucination 아님)이다.
- recommendation: 추가분(선형 워킹)이 원본 범위를 벗어남을 인지하되, 승인된 확장이므로 유지.
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-4.md

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-4.md
- quote: "$T(N) = 2T(N/2) + O(N) = O(N \\log N)$", "공통 접선 하나가 $O(\\log^2 N)$이다", "merge가 $O(N)$에서 내려오지 않으니 … 여전히 $O(N \\log N)$"
- message: 검토 완료, 이슈 없음. ① 분할 정복 재귀식 T(N)=2T(N/2)+O(N)=O(N log N) 정확. ② 선형 워킹의 O(N) 근거(각 포인터 단방향 전진, 총 전진 ≤ 점 수) 타당. ③ 이진 탐색 접선 O(log²N)(고정점 O(log N)개 × 접점 O(log N)) 및 그것이 총복잡도를 낮추지 못한다는 논증(배열 재구성 O(N) 지배)이 노션 원본과도 일치하며 옳다. 의사코드는 시리즈 관례상 pseudocode 수준으로 개념 서술과 부합.
- recommendation: 현재 복잡도·논증 유지.
- gate_effect: info

요약: 🔴 1 · 🟡 0 · 🟢 7

## 반영 결과 (2026-07-13)

- 🔴 [L4] 하단 공통 접선 기하 오류 — **반영 완료**. 네 도판(dc-split·dc-tangent·dc-walking·dc-binary-tangent)의 최하단 바깥 꼭짓점을 접선 위로 올렸다: 왼쪽 껍질 `(150,330)→(150,300)`, 오른쪽 껍질 `(540,335)→(540,300)`. 이제 하단 접선 (250,315)–(430,320)이 실제 최하단 접점이 되어 두 껍질의 모든 점이 접선 위에 놓인다(검산: 직선 (250,315)-(430,320)에서 x=150일 때 y≈312 > 300, x=540일 때 y≈323 > 300). 상단 접선도 새 배치에서 유효(모든 점이 접선 아래).
- 🟢 항목 — 조치 없음(현행 유지). "심장" 비유(L1 선택 제안)는 원문 의도가 분명해 유지.
- 재검증: `npm run build` 성공(106 pages), `python .claude/review_post.py` 재실행 "발견 사항 없음 ✅".
