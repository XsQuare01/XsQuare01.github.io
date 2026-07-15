## 결정적 검사: src/content/posts/convex-hull-calipers-edge.md

🟡 권장 (1)
- [D2] src/content/posts/convex-hull-calipers-edge.md:15, src/content/posts/convex-hull-calipers-edge.md:17, src/content/posts/convex-hull-calipers-edge.md:18  줄표(—) 12회 — 임계치(10) 초과. AI 문체 신호 샘플 위치: src/content/posts/convex-hull-calipers-edge.md:15, src/content/posts/convex-hull-calipers-edge.md:17, src/content/posts/convex-hull-calipers-edge.md:18

schema_version: review-report/v2
target: convex-hull-calipers-edge
generated_at: 2026-07-15
strict: false
summary: 🔴 0 · 🟡 2 · 🟢 7

## Findings

### 🟡 [L1] src/content/posts/convex-hull-calipers-edge.md:15
- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-calipers-edge.md:15
- quote: `- 동률은 언제 생기나 — 변이 변과 **평행**할 때`
- message: 줄표(—)가 본문 전체 12회로 결정적 검사 D2 임계치(10)를 넘는다. 목차 리스트(15·17·18), 문장 중간(57 `하나 — 곧`, 67 `않는다 — 두`), 불릿 정의(71~73 `(i, j) —`, `(i, j+1) —`, `(ni, j+1) —`)에 반복 사용돼 AI 문체 신호로 읽힐 수 있다. 논증 자체는 문제없으나 밀도가 높다.
- recommendation: 목차 15·17·18의 `주제 — 설명`을 `주제: 설명` 콜론으로, 문장 중간 57·67의 줄표를 마침표나 쉼표로 바꾸면 임계치 아래로 내려간다. 불릿 71~73은 열거 리듬을 위해 유지해도 무방하다. 어체(~다 평서체)는 그대로.
- gate_effect: warn

### 🟢 [L2] src/content/posts/convex-hull-calipers-edge.md:57
- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-calipers-edge.md:57
- quote: `그 변을 $i \to ni$라 하면, 반대쪽 점 $v$는 그 변에서 가장 먼 꼭짓점 $j$이고, $u$는 그 변의 두 끝점 중 하나 — 곧 $i$ 아니면 $ni$다.`
- message: 검토 완료, 이슈 없음. 동률 정의 → 세 유형 → 지름 값 보존 → 열거는 별개 문제 → 코드 → 정리로 이어지는 흐름이 자연스럽고 논리 도약이 없다. 57행이 다소 길지만 문장이 절 단위로 끊겨 따라갈 수 있다.
- recommendation: 현재 구성을 유지한다. 굳이 다듬는다면 57행의 삽입구(괄호)를 별도 문장으로 떼어 호흡을 늘릴 수 있으나 필수는 아니다.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-calipers-edge.md:27
- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-calipers-edge.md:27
- quote: `지지선의 방향이 껍질의 어떤 **변과 나란해지는** 순간, 지지선은 그 변을 한 점이 아니라 **통째로** 떠받친다.`
- message: 검토 완료, 이슈 없음. `지지선`, `대척점 쌍`, `교차 쌍`, `동률`, `뼈대`, `단조성` 표기가 본문·코드·SVG에서 일관된다. 5편에서 쓴 `지지선`·`포인터 i/j`·`외적` 용어를 그대로 이어 시리즈 연속성이 유지된다.
- recommendation: 현재 용어 체계를 유지한다. `평행선`을 `지지선`과 혼용하지 않도록만 주의(현재는 문맥상 구분됨).
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-calipers-edge/contact-types.svg:1
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-calipers-edge/contact-types.svg:1
- quote: `<text ... >접촉의 세 유형 — 지지선이 변에 밀착하면 대척점 쌍이 늘어난다</text>`
- message: 검토 완료, 이슈 없음. 세 패널의 쌍 개수(꼭짓점–꼭짓점 1개, 꼭짓점–변 2개, 변–변 4개=2×2)가 본문 37~39행과 캡션 41행(`1개→2개→4개`)에 정확히 일치한다. 패널 B는 하단 꼭짓점에서 상단 변 두 끝으로 향하는 주황 선분 2개, 패널 C는 두 평행 변의 끝점 조합 4개(양 변+두 대각선)를 그려 개수가 시각적으로 맞다.
- recommendation: 변경 불필요.
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-calipers-edge/parallel-pairs.svg:1
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-calipers-edge/parallel-pairs.svg:1
- quote: `<text ... >변–변 동률에서 대척점 쌍 열거</text>`
- message: 검토 완료, 이슈 없음. 꼭짓점 라벨 i(160,340)·ni(520,340)·j(560,110)·j+1(200,110)과 색 구분이 본문 71~73행·코드와 일치한다. 초록 실선=(i,j)·(ni,j)[뼈대 기록], 주황 점선=(i,j+1)[동률 분기 추가], 회색 점선=(ni,j+1)[다음 변]. 포인터 j가 아래 변 i→ni에서 CCW로 먼저 닿는 top-right 꼭짓점에 멈춘다는 서술과 도판의 j 위치가 정합한다.
- recommendation: 변경 불필요.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-calipers-edge.md:2
- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-calipers-edge.md:2
- quote: `title: "추가 설명 — 평행한 변이 만드는 동률과 대척점 쌍 열거"`
- message: 검토 완료, 이슈 없음. 제목이 글의 두 축(동률의 출처=평행 변, 목표=대척점 쌍 열거)을 정확히 대표한다. description(109자, 160자 이하)도 "지름 값은 뼈대로 이미 옳고, 이 글은 열거라는 별개 문제를 다룬다"는 핵심 논지를 담아 실제 내용과 부합한다.
- recommendation: frontmatter 유지.
- gate_effect: info

### 🟢 [L6] not-recorded
- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음(단, 출처 관계 명시). 이 글의 엣지 케이스 내용(평행 변 동률, 대척점 쌍 완전 열거, `>` vs `>=`, Toussaint 시작 마커)은 노션 `Convex hull 2` 노트의 Farthest Point 섹션에 없다. 스펙에 기록된 대로 **승인된 표준 알고리즘 보강**(Toussaint 1983, Preparata–Shamos)이며, 5편 뼈대·대척점·외적 프레이밍은 노션 원본과 5편에 충실하다. 자의적 추가(hallucination)가 아니라 5편 L7이 명시적으로 후속 글에 위임한 범위를 채운 것.
- recommendation: Notion MCP 연결 세션에서 원본을 직접 대조하려면 별도로 검색·조회하되, 이 편은 원본에 없는 확장임이 스펙·5편 리뷰로 이미 문서화돼 있다.
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-calipers-edge.md:57
- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-calipers-edge.md:57
- quote: `뼈대는 $(i, j)$와 $(ni, j)$를 **둘 다** 재므로, $u$가 어느 끝이든 $(u, v)$를 반드시 검사한다.`
- message: 검토 완료, 이슈 없음(손으로 검증). ① 지름 값 보존 주장을 직접 검산: 직사각형 (0,0)(4,0)(4,1)(0,1)에서 뼈대가 i=0변에 dist2(A,C)=17, i=1변에 dist2(B,D)=17을 잡아 두 대각선 모두 후보로 오름. 정육각형(R=1)에서도 i=0변 처리 중 j가 대척 꼭짓점에 도달해 dist2=4(지름 2) 확보. ② 열거 완전성 검산: 일반 위치 볼록 오각형 (0,0)(4,0)(5,3)(2,5)(-1,3)에 코드를 손으로 돌려 보고 대척점 쌍 {0-2,0-3,1-3,1-4,2-4}를, 꼭짓점 법선 콘으로 독립 계산한 대척점 집합과 대조 → **정확히 5쌍, 빠짐·중복 없음**. ③ 변–변 동률에서 `cross(i,ni,j)==cross(i,ni,j+1)`로 `>`가 거짓이 되어 j가 j+1로 넘어가지 않음, 교차 쌍 (i,j+1)은 동률 분기로 추가·(ni,j+1)은 다음 변에서 회수됨을 확인. ④ `>`→`>=` 위험(경계 흐려짐·순회 횟수 어긋남) 서술 타당. ⑤ 과대주장 없음: 지름 값 정확성과 완전 열거(중복 없는 종료는 Toussaint 마커 필요)를 명확히 분리.
- recommendation: 논증·복잡도 주장 유지. 코드가 완전 dedup 버전이 아님을 113행에서 이미 정직하게 밝히고 있어 오해 소지 없음.
- gate_effect: info

요약: 🔴 0 · 🟡 2 · 🟢 7

## 반영 결과 (2026-07-15)

- 🟡 [D2/L1] 줄표(—) 12회로 임계치(10) 초과 — **반영 완료**. 목차 3곳(15·17·18)의 `주제 — 설명`을 `주제: 설명` 콜론으로, 문장 중간 2곳(57 `하나 — 곧`, 67 `않는다 — 두`)을 쉼표·마침표로 바꿔 5개를 제거. 불릿 정의(71~73)와 캡션·제목의 줄표는 열거 리듬·표기 관례로 유지. 재검사 결과 `python .claude/review_post.py` "발견 사항 없음 ✅".
- 🟢 나머지 항목은 이슈 없음(coverage). 특히 [L7] 논증은 직사각형·정육각형(지름 값 보존)과 일반 위치 오각형(대척점 쌍 5개 = 법선 콘 독립 계산과 일치, 빠짐·중복 없음)으로 손 검증을 마쳐 수정 불필요.
- 재검증: `npm run build` 성공.
