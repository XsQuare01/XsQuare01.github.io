## 결정적 검사: src/content/posts/convex-hull-5.md
발견 사항 없음 ✅

schema_version: review-report/v2
target: convex-hull-5
generated_at: 2026-07-14
strict: false
summary: 🔴 0 · 🟡 2 · 🟢 7

## Findings

### 🟡 [L4] public/images/convex-hull-5/calipers.svg:12
- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/convex-hull-5/calipers.svg:12
- quote: `<line x1="470" y1="90" x2="650" y2="330" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>`
- message: `calipers.svg`의 두 지지선이 강조된 포인터 접점과 정확히 맞지 않는다. 위 지지선은 x=540에서 y≈183.3이어서 `포인터 i` 원의 중심 (540,180)을 지나지 않고, 아래 지지선은 x=150에서 y≈286.7이어서 `포인터 j` 원의 중심 (150,300)을 지나지 않는다. 본문 `src/content/posts/convex-hull-5.md:60`과 캡션은 두 포인터를 지지선의 접점처럼 설명하므로 시각적 기하가 텍스트와 어긋난다.
- recommendation: 지지선 좌표를 강조된 두 포인터 중심을 지나도록 조정하거나, 실제 지지선 위의 접점 위치로 포인터 원과 라벨을 옮긴다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/convex-hull-5.md:91
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-5.md:91
- quote: `평행한 두 **변**이 동시에 닿을 때(대척점 쌍이 여럿), 포인터가 언제 둘 다 움직여야 하는지, 대척점 쌍을 빠짐없이 세는 정확한 조건 등은 경우가 갈려 흐름을 끊는다.`
- message: 지름이 껍질 꼭짓점 쌍으로 줄어드는 논증과 외적 기반 면적 증가는 타당하지만, 현재 글은 `모든 대척점 쌍만 훑어` 지름을 얻는다고 설명하면서도 대척점 쌍의 정확한 열거 조건과 동률 처리(`둘 다 움직여야 하는지`)를 후속 글로 미룬다. 특히 `src/content/posts/convex-hull-5.md:77`의 strict `>` 조건은 같은 면적이 되는 vertex-edge/edge-edge 상황을 열거 관점에서 건너뛸 수 있으므로, “모든 대척점 쌍” 순회라는 주장과 현재 글 안의 알고리즘 설명 사이에 엄밀성 공백이 남는다.
- recommendation: 현재 글의 범위를 “지름 계산을 위한 rotating calipers의 기본 뼈대”로 좁혀 표현하거나, 동률일 때 양쪽 포인터 전진 및 중복 없는 종료 조건을 포함해 대척점 쌍 열거가 빠짐없이 닫힌다는 설명을 추가한다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-5.md:10
- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-5.md:10
- quote: `마지막 편은 방향을 바꾼다. 껍질을 **도구로 쓴다.**`
- message: 검토 완료, 이슈 없음
- recommendation: 현재처럼 한국어 평서체와 짧은 선언형 문장을 유지한다. 줄표와 비유가 과하지 않고, 강조도 핵심 용어 중심으로 제한되어 AI식 과장 신호가 두드러지지 않는다.
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-5.md:26
- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-5.md:26
- quote: `## 1차원에서 2차원으로`
- message: 검토 완료, 이슈 없음
- recommendation: 1차원 최솟값·최댓값 예시에서 2차원 모든 쌍, 껍질 꼭짓점, 대척점 쌍, rotating calipers로 이어지는 흐름이 자연스럽다. 문장 길이와 전환도 현재 수준을 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-5.md:17
- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-5.md:17
- quote: `평행선 회전과 **대척점 쌍(antipodal pair)**`
- message: 검토 완료, 이슈 없음
- recommendation: `껍질 꼭짓점`, `대척점 쌍(antipodal pair)`, `Rotating Calipers`, `외적(cross product)`의 표기가 본문과 코드 설명에서 일관된다. 혼용을 늘리지 말고 현재 용어 체계를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-5/hull-vertices.svg:9
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-5/hull-vertices.svg:9
- quote: `<text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">가장 먼 두 점은 껍질 꼭짓점이다</text>`
- message: 검토 완료, 이슈 없음
- recommendation: `hull-vertices.svg`는 본문 `src/content/posts/convex-hull-5.md:36-42`의 “가장 먼 두 점은 껍질 꼭짓점” 설명과 맞는다. 표시된 지름 후보 (120,190)–(560,300)는 그림의 다른 꼭짓점 쌍보다 제곱거리 205700으로 가장 길어 라벨도 타당하다.
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-5/antipodal.svg:4
- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-5/antipodal.svg:4
- quote: `<text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">평행선 회전과 대척점 쌍 (antipodal pair)</text>`
- message: 검토 완료, 이슈 없음
- recommendation: `antipodal.svg`는 본문 `src/content/posts/convex-hull-5.md:50-54`의 평행 지지선과 대척점 쌍 설명에 부합한다. 수평 지지선 y=100, y=360이 각각 꼭짓점 (400,100), (350,360)에 닿고, “이 각도의 지름 후보”라는 제한적 표현도 본문 주장과 충돌하지 않는다.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-5.md:2
- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-5.md:2
- quote: `title: "볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers"`
- message: 검토 완료, 이슈 없음
- recommendation: 제목과 description은 실제 범위인 볼록 껍질을 이용한 평면 지름 문제, 대척점 쌍, rotating calipers의 O(N) 순회를 잘 대표한다. 후속 글로 미룬 edge case는 본문 callout에서 별도 범위로 밝혀져 있으므로 frontmatter 자체는 유지 가능하다.
- gate_effect: info

### 🟢 [L6] not-recorded
- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 원문 대조 증거를 만들려면 Notion MCP가 연결된 세션에서 원본 페이지를 검색·조회한 뒤, 원문 누락이나 임의 추가 여부를 별도 확인한다. 이번 리포트에서는 Notion source-page evidence를 만들지 않는다.
- gate_effect: info

요약: 🔴 0 · 🟡 2 · 🟢 7

## 반영 결과 (2026-07-14)

- 🟡 [L4] `calipers.svg` 지지선-포인터 불일치 — **반영 완료**. 두 지지선을 강조 포인터 중심을 지나도록 재조정했다(기울기 4/3 유지). 위 지지선 `(470,90)-(650,330)` → `(470,87)-(650,327)`으로 x=540에서 y≈180(포인터 i), 아래 지지선 `(70,180)-(250,420)` → `(70,193)-(240,420)`으로 x=150에서 y≈300(포인터 j)을 지난다. 두 기울기는 각 꼭짓점의 인접 두 변 사이(유효 supporting line 범위)에 들어 접선으로도 타당.
- 🟡 [L7] "모든 대척점 쌍 훑기" 주장과 strict `>` 뼈대의 엄밀성 공백 — **반영 완료**. Rotating Calipers 의사코드 뒤 callout을 고쳐, 위 코드가 **일반 위치(동률 없는 경우)를 가정한 기본 뼈대**이며 `>`가 변마다 대척점을 하나로 고른다는 점, 평행 변으로 대척점 쌍이 동률이 되는 경우의 **완전한 열거·종료 조건**은 '추가 설명'에서 다룬다는 점을 명시했다. 글 범위를 "지름 계산 rotating calipers의 기본 뼈대"로 좁혀 표현.
- 재검증: `npm run build` 성공(109 pages), `python .claude/review_post.py` "발견 사항 없음 ✅", 지지선-포인터 통과 수치 확인(top@540≈180.3, bottom@150≈299.8).
