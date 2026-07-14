## 결정적 검사: src/content/posts/convex-hull-5.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/convex-hull-5.md

검토 범위: 본문 전체 + 참조 SVG 3개(`hull-vertices.svg`, `antipodal.svg`, `calipers.svg`). L6은 이번 세션에서 가져온 노션 `Convex hull 2` 노트의 Farthest Point 섹션과 대조.

### 🟢 [L1] src/content/posts/convex-hull-5.md

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-5.md
- quote: "물체를 양쪽에서 재는 자(caliper) 두 짝을 벌려 돌리는 그림이라 Rotating Calipers다."
- message: 검토 완료, 이슈 없음. 줄표는 결정적 검사 임계치 내이고 경구식 마무리·대칭 반복 없음. "자를 양옆에 대는 느낌", caliper 비유는 개념을 돕는 평이한 수준이다. "시리즈를 마치며"도 마지막 편의 자연스러운 마무리다.
- recommendation: 현재 문체 유지.
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-5.md

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-5.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 1차원 워밍업 → 껍질 꼭짓점으로 후보 축소 → 대척점 쌍 → Rotating Calipers → 복잡도로 이어지는 흐름에 논리 도약이 없다.
- recommendation: 현재 순서 유지.
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-5.md

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-5.md
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 지름·껍질·꼭짓점·대척점 쌍·지지선·포인터·외적·CCW 용어가 1~4편과 일관되고 어체(~다)도 통일.
- recommendation: 현재 용어 체계 유지.
- gate_effect: info

### 🟢 [L4] SVG 3장 ↔ 본문

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-5/{hull-vertices,antipodal,calipers}.svg
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 세 도판이 동일 껍질 좌표를 공유. hull-vertices의 지름 쌍(120,190)-(560,300)과 내부 점 X 밀어내기, antipodal의 수평 지지선(y=100은 최상단 400,100·y=360은 최하단 350,360에만 접함)과 대척점 쌍, calipers의 두 포인터·전진 표시가 본문 서술과 대응한다. antipodal의 대척점 쌍이 hull-vertices의 지름과 다른 쌍이지만, 라벨을 "이 각도의 지름 후보"로 명시하고 본문이 "모든 대척점 쌍을 훑어 최대"라 밝혀 혼동이 없다(의도된 스냅샷).
- recommendation: 현행 유지.
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-5.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-5.md:2-4
- quote: "볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers"
- message: 검토 완료, 이슈 없음. 제목과 description(지름=껍질 꼭짓점, 평행선·대척점, Rotating Calipers로 O(N²)→O(N))이 실제 내용을 대표하고, description은 160자 이하(SEO 경고 없음).
- recommendation: 현재 frontmatter 유지.
- gate_effect: info

### 🟢 [L6] 노션 `Convex hull 2` (Farthest Point) 대조

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/convex-hull-5.md
- quote: "1차원은 min/max로 O(N) … 평행한 두 직선을 0°→180° 회전 … 대척점(antipodal pair) … 가장 먼 두 점은 반드시 convex hull 꼭짓점 … Rotating Calipers … 껍질 O(N log N)+순회 O(N)=O(N log N), 모든 쌍 O(N²)보다 빠르다" (노션 원본 요지)
- message: 노션 Farthest Point 섹션의 핵심(1D min/max, 껍질 꼭짓점, 평행선 회전·대척점 쌍, 더 작은 각도 쪽 포인터 전진, 복잡도)이 모두 반영됐고 누락 없음. 외적 기반 C++ 의사코드는 원본에 없는 **추가 구현 세부**이나, 시리즈의 의사코드 관례에 맞는 표준 rotating-calipers-diameter 알고리즘으로 정확하다(hallucination 아님).
- recommendation: 유지. 엣지 케이스는 예고대로 추가 설명 글로 분리.
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-5.md

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-5.md
- quote: "가장 먼 쌍 a, b를 잇는 선분에 수직인 방향으로 평행선을 대면 두 직선이 정확히 a와 b에 닿기 때문이다", "j는 while 문에서 전진하되 뒤로는 가지 않아 … H번을 넘지 못한다"
- message: 검토 완료, 이슈 없음. ① 지름 쌍이 대척점 쌍임(수직 지지선이 supporting line): c가 a의 수직선 밖이면 |cb|>|ab|가 되어 지름 가정과 모순 — 논증 타당. ② 내부 점이 최원 쌍이 될 수 없음(밀수록 멀어짐) 타당. ③ Rotating Calipers O(N): 외적으로 변에서 가장 먼 꼭짓점(대척점) 판정, j 단조 전진으로 총 O(H)=O(N), 전체 O(N log N) 정확. 의사코드의 strict `>` 비교로 생기는 평행/동거리 엣지 케이스는 본문이 명시적으로 추가 설명으로 미뤄 범위 밖.
- recommendation: 현재 논증·복잡도 유지.
- gate_effect: info

요약: 🔴 0 · 🟡 0 · 🟢 7
