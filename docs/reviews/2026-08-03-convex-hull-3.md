schema_version: review-report/v2
target: convex-hull-3
generated_at: 2026-08-03
strict: true
sources: src/content/posts/convex-hull-3.md
summary: 🔴 0 · 🟡 1 · 🟢 6

## Findings

### 🟡 [L6] docs/superpowers/specs/2026-07-09-convex-hull-3-design.md:55

- severity: 🟡
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-07-09-convex-hull-3-design.md:55
- quote: "매 걸음 껍질을 다 훑는 낭비 → 껍질 점을 균형 이진 트리에 y좌표 순 저장."
- message: 본문은 고쳐졌는데 설계 문서에 원인이 그대로 남아 있다. 노션 원문(🎿 Convex hull 2)은 껍질을 두 가지 방식으로 자를 수 있다고 밝힌 뒤 "다음 설명은 right hull만 고려한다"로 못박고, 그 전제 위에서 "convex hull 위의 점이 Balanced binary tree에 y좌표 순으로 저장되어 있어야 한다"고 쓴다. right hull은 최상단·최하단 점으로 가른 사슬이라 y에 단조롭기 때문에 원문 안에서는 일관된다. 이 글은 대신 최좌·최우 점으로 가른 upper/lower hull을 택했고, 그 사슬은 x에 단조롭다. 그래서 저장 순서도 x여야 하는데, 스펙 45행은 upper/lower 분해를 적어 놓고 55행은 원문의 y좌표 순을 그대로 옮겨 두 줄이 서로 어긋난다. 앞선 리포트(2026-07-09)의 🔴이 정확히 이 불일치였고 본문과 `bst-idea.svg`는 x좌표 순으로 고쳐졌지만, 스펙은 갱신되지 않아 다음 개정 때 같은 오류가 되살아날 자리가 남아 있다.
- recommendation: 스펙 55행을 "x좌표 순 저장"으로 고치고, 원문이 right hull 기준이어서 y좌표 순이었다는 사실을 한 줄로 덧붙여 왜 달라졌는지 남긴다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-3.md:1-123

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-3.md:1-123
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/convex-hull-3.md:1-123

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-3.md:1-123
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-3.md:1-123

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-3.md:1-123
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-3/bst-idea.svg:10

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-3/bst-idea.svg:10
- quote: "사슬(예: upper hull)을 x좌표 순으로 저장 → 새 점의 접점을 O(log N)에 찾는다"
- message: 참조 SVG 다섯 개를 본문과 대조했다. 앞선 리포트가 지적한 `bst-idea.svg`의 "y좌표 순으로 저장" 레이블은 본문 73행과 함께 x좌표 순으로 이미 고쳐졌다. `upper-lower.svg`의 "최좌측 점 L과 최우측 점 R이 껍질을 위아래 두 사슬로 가른다"는 본문 30행과 같고, 덧붙은 "각 사슬은 x좌표에 대해 단조롭다"도 34행과 맞는다. `sweep-tangent.svg`의 "새 점 p(가장 오른쪽)에서 위·아래 접선을 긋고 사이 점을 버린다", `sweep-result.svg`의 갱신 결과, `dynamic.svg`의 안쪽·바깥쪽 두 분기도 각각 본문 42-46행, 100행 서술과 일치한다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-3.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-3.md:2-4
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-3.md:52-102

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-3.md:52-102
- quote: not-recorded
- message: 논증과 복잡도를 확인했다. 접점 탐색 코드는 `ccw(p, hull[up], hull[i]) > 0`이면 `up`을 갱신해 p에서 봤을 때 나머지 점이 모두 한쪽에 오는 극점을 남기므로, 볼록 다각형 밖의 점에서 접점을 찾는 선형 훑기로 옳다. `i == up`일 때 ccw가 0이라 자기 자신으로 갱신되지 않는 점도 같다. upper/lower 사슬이 x에 단조라는 성질은 1편의 "모든 x좌표가 다르다" 가정 위에서 성립하고, 22행이 그 가정을 다시 밝힌다. 삭제 총비용 논증도 맞다. 각 점은 한 번 삽입되고 최대 한 번 삭제되므로 삭제 횟수 합이 $N$ 이하이고, 삭제 하나가 $O(\log N)$이라 총 $O(N \log N)$이다. Plane Sweeping $O(N^2)$, 정렬 $O(N \log N)$이 묻힌다는 서술, Dynamic Case의 내부 판정(x범위 밖이면 즉시 외부, 안이면 두 사슬에 각각 CCW)도 원문과 같고 논리에 빈 곳이 없다.
- recommendation: not-recorded
- gate_effect: info
