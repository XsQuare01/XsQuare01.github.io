## 결정적 검사: src/content/posts/convex-hull-calipers-edge.md
발견 사항 없음 ✅

schema_version: review-report/v2
target: convex-hull-calipers-edge
generated_at: 2026-07-15
strict: false
summary: 🔴 1 · 🟡 2 · 🟢 7

## Findings

### 🔴 [L7] src/content/posts/convex-hull-calipers-edge.md:122
- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-calipers-edge.md:122
- quote: `**중복 없이 딱 한 번씩** 뽑으려면 여기에 종료 관리를 더한다. 첫 대척점의 위치를 시작 마커로 기억해 두고, $j$가 그 마커로 되돌아오면 멈추는 방식이다(Toussaint의 고전적 열거법). 원리는 지금 뼈대와 같다. 평행한 변에서만 쌍을 하나 더 채우고, 한 바퀴에서 정확히 끊는다.`
- message: 중앙 주장인 중복 없는 완전 열거가 현재 코드와 설명만으로는 증명되지 않는다. 직사각형 $A(0,0)$, $B(4,0)$, $C(4,1)$, $D(0,1)$에서 본문에 제시된 전체 `for` 루프가 `report`를 단순히 목록에 append한다고 보면, 아래 변과 위 변을 각각 처리하면서 $(A,C)$와 $(C,A)$, $(B,D)$와 $(D,B)$처럼 같은 무순서 대척점 쌍을 방향만 바꿔 다시 낼 수 있다. $j$에 시작 마커를 둔다는 말만으로는 `i`의 진행, 쌍 정규화, event loop 종료 조건이 어떻게 맞물려 한 번만 출력되는지 보장하지 못하므로, “중복 없이 딱 한 번씩”이라는 핵심 열거 주장이 정당화되지 않는다.
- recommendation: 현재 글의 범위를 완전 열거 증명까지 확장하지 말고 completeness와 tie-branch illustration으로 좁히거나, 실제 Toussaint식 event loop, 무순서 pair normalization, 종료 규칙을 명시하고 그 규칙이 중복 출력 없이 모든 대척점 쌍을 한 번씩 낸다는 증명을 함께 제공한다.
- gate_effect: fail

### 🟡 [L7] src/content/posts/convex-hull-calipers-edge.md:89
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-calipers-edge.md:89
- quote: ``동률에서 $j$가 못 넘어가는 게 문제라면 비교를 `>=`로 풀어 $j$를 전진시키면 될 것 같다. 하지만 그러면 동률이 아닌 자리에서도 $j$가 한 칸 더 밀려, 어느 변의 대척점인지 경계가 흐려지고 $j$가 한 바퀴 도는 횟수가 어긋난다. 대척점을 중복해 세거나, 심하면 종료가 꼬인다. 그래서 표준 해법은 `>`를 그대로 두어 "변마다 대척점 하나"라는 단조성을 지키고, **넓이가 정확히 같은 동률만 따로 분기**해 빠진 교차 쌍을 채운다.``
- message: `>`를 `>=`로 바꾸면 달라지는 지점은 두 외적이 같은 equality case다. non-tie 위치에서는 `>`와 `>=`의 판정이 같으므로, “동률이 아닌 자리에서도 $j$가 한 칸 더 밀려”라는 설명은 비교 연산의 실제 차이를 잘못 말한다. 문제의 핵심은 equality case에서 어느 쪽 event를 소비했는지와 pair/report/termination을 어떻게 정의하느냐이지, non-tie 위치의 추가 전진이 아니다.
- recommendation: 이 문장을 “`>=`는 동률 위치에서 다음 꼭짓점을 즉시 소비하므로, 그 equality event에 속한 여러 대척점 쌍과 종료 조건을 별도로 정의하지 않으면 중복이나 누락이 생긴다”처럼 equality case 변화로 좁혀 설명한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-calipers-edge.md:121
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-calipers-edge.md:121
- quote: ``각 변에서 $(ni, j)$를 따로 `report`하지 않은 이유: 그 쌍은 `for`가 $ni$를 다음 $i$로 삼는 회차에서 $(i, j)$ 자리로 자연히 나온다. 한 바퀴를 다 돌면 모든 대척점 쌍이 모인다.``
- message: $(ni,j)$가 곧바로 다음 회차에서 같은 ordered form의 $(i,j)$로 나온다는 설명은 일반적으로 맞지 않는다. 직사각형 예시에서 bottom edge $(B,C)$는 다음 회차에 곧바로 같은 $(B,C)$로 반복되는 것이 아니라 $(B,D)$로 이어질 수 있다. $(B,C)$ 자체가 다시 나타나더라도 나중에 무순서로 보면 $(C,B)$ 형태가 되는 식이라, “다음 $i$ 회차에서 자연히 나온다”는 말은 ordered pair와 unordered pair를 섞는다.
- recommendation: 이 설명을 즉시 다음 회차 재출력으로 쓰지 말고, 어떤 쌍을 ordered로 볼지 unordered로 정규화할지 먼저 정한다. 그런 다음 직사각형처럼 평행 변이 있는 경우를 포함해 각 변 처리 순서에서 누락과 중복이 어떻게 관리되는지 별도 규칙으로 제시한다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-calipers-edge.md:10
- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-calipers-edge.md:10
- quote: `그 미뤄둔 조각을 마저 맞춘다. 다만 먼저 짚을 게 있다.`
- message: 검토 완료, 이슈 없음
- recommendation: 현재처럼 짧은 문장과 문제 범위 선언을 유지한다. 과장된 AI식 전환어보다 글의 기술적 목적을 바로 드러내는 문체라 읽기 흐름이 좋다.
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-calipers-edge.md:25
- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-calipers-edge.md:25
- quote: `## 동률은 어디서 오는가`
- message: 검토 완료, 이슈 없음
- recommendation: 동률의 원인, 접촉 유형, 지름 값과 열거 문제의 분리, 코드 예시 순서로 이어지는 큰 흐름은 자연스럽다. line 89, 121, 122의 정확성 지적을 제외하면 독자가 문제 범위를 따라가기 어렵게 만드는 구조적 비약은 없다.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-calipers-edge.md:16
- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-calipers-edge.md:16
- quote: `접촉의 세 유형: 꼭짓점–꼭짓점 · 꼭짓점–변 · 변–변`
- message: 검토 완료, 이슈 없음
- recommendation: `동률`, `대척점 쌍`, `지지선`, `strict >`, `report` 같은 핵심 용어가 본문과 코드 설명에서 일관되게 쓰인다. 한국어 용어 뒤에 필요한 코드 표기를 붙이는 현재 방식을 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-calipers-edge/contact-types.svg:14
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-calipers-edge/contact-types.svg:14
- quote: `<text x="120" y="290" text-anchor="middle" fill="#e2e8f0" font-size="12" font-weight="600">꼭짓점–꼭짓점</text>`
- message: 검토 완료, 이슈 없음
- recommendation: `contact-types.svg`는 본문 `src/content/posts/convex-hull-calipers-edge.md:35-43`의 꼭짓점, 꼭짓점과 변, 변과 변 접촉 분류를 시각적으로 잘 대응시킨다. 각 패널의 쌍 개수 라벨도 본문 설명과 충돌하지 않는다.
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-calipers-edge/parallel-pairs.svg:33
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-calipers-edge/parallel-pairs.svg:33
- quote: `<text x="248" y="396" fill="#6ee7b7">뼈대가 기록 — (i, j), (ni, j)</text>`
- message: 검토 완료, 이슈 없음
- recommendation: `parallel-pairs.svg`는 본문 `src/content/posts/convex-hull-calipers-edge.md:76-84`의 변과 변 동률 상황, 뼈대가 기록하는 쌍, 동률 분기로 추가하는 쌍, 다음 변에서 나오는 쌍의 구분을 같은 색상 범례로 보여 준다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-calipers-edge.md:4
- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-calipers-edge.md:4
- quote: `description: "볼록 껍질 ⑤의 Rotating Calipers 뼈대는 평행한 변이 있어도 지름 값이 옳다. 이 글은 대척점 쌍을 빠짐없이 열거하는 별개 문제와, 평행한 변이 만드는 동률·교차 쌍 처리를 다룬다."`
- message: 검토 완료, 이슈 없음
- recommendation: 제목과 description은 후속 보충 글의 범위, 지름 값과 열거 문제의 분리, 평행 변 동률과 교차 쌍 처리를 잘 대표한다. line 122의 실제 증명 공백은 본문 finding으로 다루면 되고, frontmatter의 주제 설정 자체는 유지 가능하다.
- gate_effect: info

### 🟢 [L6] docs/superpowers/specs/2026-07-15-convex-hull-calipers-edge-design.md:5
- severity: 🟢
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-07-15-convex-hull-calipers-edge-design.md:5
- quote: ``- 원본 자료: 노션 `Convex hull 2` 노트의 Farthest Point 섹션(엣지 케이스 상세는 노션에 없어 표준 알고리즘 지식 — Toussaint 1983, Preparata–Shamos — 으로 보강. 승인된 확장)``
- message: 검토 완료, 이슈 없음. 실제 source clue는 Notion `Convex hull 2` 노트의 Farthest Point 섹션이다. 평행 변 동률과 완전 열거 같은 edge-case details는 해당 노션에 없는 내용을 표준 알고리즘 지식에 근거해 보강한 승인된 확장으로 기록되어 있다. 다만 이번 검토 환경에서는 Notion URL/page ID나 notion-search/notion-fetch 접근이 제공되지 않아 source page comparison은 unavailable이다.
- recommendation: L6 근거는 이 post 전용 design spec의 source-extension statement로 유지한다. Notion 원문과 직접 대조하려면 별도 세션에서 실제 Notion URL/page ID 또는 notion-search/notion-fetch 접근 권한을 확보한 뒤 비교해야 하며, 접근 없이 URL이나 page ID를 새로 꾸며내지 않는다.
- gate_effect: info

요약: 🔴 1 · 🟡 2 · 🟢 7

## 반영 결과 (2026-07-15)

세 지적 모두 정당함. 직사각형 $A(0,0)B(4,0)C(4,1)D(0,1)$에 열거 코드를 손으로 돌려 검증한 결과, 실제로 $(A,C)$가 i=0(아래 변)과 i=2(위 변)에서, $(B,D)$가 i=1·i=3에서 각각 **두 번** 보고됨을 확인 → "중복 없이"는 거짓이었다.

- 🔴 [L7:122] 중복 없는 완전 열거가 코드·설명으로 증명되지 않음 — **반영 완료(범위 축소)**. 리뷰 권고의 옵션 1을 택함. 해당 bullet을 다시 써서 (a) 이 루프는 **빠짐없이 훑지만 딱 한 번씩 내지는 않음**을 명시하고, 아래 변이 $(A,C)$를 보고하면 위 변에서 $(C,A)$로 다시 나오는 직사각형 중복 예를 넣음. (b) 중복 제거·한 바퀴 종료는 Toussaint의 시작 마커가 **맞은편 변의 두 번째 순회 전에 끊어** 해결함을 원리로 설명. (c) 완전한 순회·무순서 정규화·종료 규칙 전체 이식은 글의 범위를 넘음을 밝히고, 이 글은 **동률 분기 필요성 + 열거 완전성**까지만 다룸을 명시.
- 🟡 [L7:89] `>=` 설명 오류(비교 차이가 non-tie에서도 나는 것처럼 서술) — **반영 완료**. "`>`와 `>=`가 갈리는 곳은 **오직 두 외적이 같은 동률 지점뿐**이고, 동률이 아니면 판정이 완전히 같다"로 정정. 문제의 핵심을 동률 지점에서 `>=`가 다음 꼭짓점을 즉시 삼켜 여러 쌍·종료를 따로 정의하지 않으면 중복·누락이 난다는 쪽으로 좁힘.
- 🟡 [L7:121] "$(ni,j)$가 다음 회차 $(i,j)$로 자연히 나온다"가 ordered/unordered 혼동 — **반영 완료**. 해당 문장을 삭제하고, "이 루프는 빠짐없이 훑되 한 쌍이 순서만 바뀌어 다시 나올 수 있다(무순서로 보면 중복)"는 정확한 서술로 대체(위 🔴 반영과 통합).
- 재검증: `npm run build` 성공, `python .claude/review_post.py convex-hull-calipers-edge` "발견 사항 없음 ✅". [L7] 완전성은 직사각형에서 무순서 6쌍(= 모든 꼭짓점 쌍) 모두 커버됨을 손으로 확인.
