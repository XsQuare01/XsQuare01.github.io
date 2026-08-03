schema_version: review-report/v2
target: convex-hull-1
generated_at: 2026-08-03
strict: true
sources: src/content/posts/convex-hull-1.md
summary: 🔴 0 · 🟡 2 · 🟢 6

## Findings

### 🟡 [D12] not-recorded

- severity: 🟡
- source: D
- rule_id: D12
- location: not-recorded
- quote: not-recorded
- message: 시리즈 다음 편 링크 누락: /blog/convex-hull-2(`convex-hull-2.md` 존재)을 본문에서 참조하지 않음
- recommendation: 메시지에 따라 원문을 검토하고 필요한 경우 수정
- gate_effect: warn

### 🟡 [L2] src/content/posts/convex-hull-1.md:104

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/convex-hull-1.md:104
- quote: "그 절댓값은 두 벡터가 만드는 **평행사변형의 넓이**(부호 있는 넓이의 2배)와 같다."
- message: 괄호 안 "부호 있는 넓이의 2배"가 무엇의 2배인지 밝히지 않아 두 가지로 읽힌다. 삼각형의 부호 있는 넓이를 기준으로 읽으면 맞지만, 바로 앞에서 ccw 값 자체를 부호 있는 양으로 소개했으므로 "ccw의 2배"로도 읽힌다. 후자로 읽으면 틀린 말이 된다. ccw는 그 자체가 평행사변형의 부호 있는 넓이이고, 삼각형 넓이의 2배다. 같은 내용을 담은 `ccw-area.svg`는 "평행사변형 넓이", "넓이 = |ccw(A, B, C)|"로 기준 도형을 분명히 적어 본문보다 정확하다.
- recommendation: 기준 도형을 밝혀 "삼각형 $ABC$ 넓이의 2배"로 쓰거나, 괄호를 지우고 "ccw는 평행사변형의 부호 있는 넓이"라고 한 문장으로 정리한다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/convex-hull-1.md:1-198

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/convex-hull-1.md:1-198
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/convex-hull-1.md:1-198

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/convex-hull-1.md:1-198
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] public/images/convex-hull-1/wrapping-full.svg:24-29

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/convex-hull-1/wrapping-full.svg:24-29
- quote: "시작점에서 반시계로 한 변씩 감싸며(나머지 점을 왼쪽에 두며) 돌아온다"
- message: 참조 SVG 일곱 개를 본문과 대조했다. 앞선 리포트(2026-07-07)가 지적한 `wrapping-full.svg`의 순회 방향은 이미 고쳐져 있다. 화살표 여섯 개의 끝점을 순서대로 따라가면 최하단 시작점에서 오른쪽 아래 변을 지나 위로 올라간 뒤 왼쪽을 거쳐 되돌아오는 반시계 순회이고(SVG 좌표계는 y가 아래로 증가하므로 화면상 아래쪽이 y 최소 지점이다), 부제도 "나머지 점을 왼쪽에 두며"로 코드 162행의 `ccw(...) < 0` 갱신 규칙과 맞는다. `wrapping-step.svg`의 "✗ 후보(오른쪽에 점이 남음)"도 같은 규약이다. `ccw-turn.svg`의 부호 대응, `brute-force.svg`의 한쪽 판정, `definition.svg`·`convex-vs-not.svg`의 정의 서술도 본문과 일치한다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/convex-hull-1.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/convex-hull-1.md:2-4
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] src/content/posts/convex-hull-1.md:25-183

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/convex-hull-1.md:25-183
- quote: not-recorded
- message: 노션 원문(🎰 Convex hull 1)과 대조했다. 정의의 "넓이 최소와 둘레 최소가 겹친다", 세 가정, 브루트포스 $O(N^3)$, CCW 기울기 비교에서 나오는 전개식은 원문을 그대로 따른다. 원문 Package Wrapping 절에는 "🔧 Claude 정정" 블록이 붙어 있어 복잡도를 $O(N^2 \log N)$에서 $O(NH)$로, "각도 정렬"을 선형 탐색으로, 누락된 반복 단계를 바로잡아 두었다. 이 글의 복잡도 서술과 "각도 정렬이 아니다" 콜아웃이 그 정정을 반영한 결과이므로 원문과 어긋나지 않는다. 원문 상단의 "블로그 쓸 때, Package wrapping이랑 Graham scan 나눠서 포스팅하기"라는 지시에 따라 Graham Scan을 다음 편으로 미룬 것도 원문 의도와 맞는다. 다만 그 분리 때문에 D12가 지적한 다음 편 링크 누락이 더 아쉬운 자리가 된다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/convex-hull-1.md:59-178

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/convex-hull-1.md:59-178
- quote: not-recorded
- message: 수식과 코드를 검산했다. 본문 90행의 전개식과 123행 코드 `(b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x)`를 전개하면 항이 정확히 일치한다. 81-85행의 기울기 비교 유도도 옳고, 분모 부호에 따라 부등호가 뒤집힐 수 있다는 단서를 87행이 이미 달아 두었다. `giftWrapping`은 `next`를 `(cur+1)%n`으로 시작해 `ccw < 0`인 점으로 갱신하므로 남은 점을 모두 왼쪽에 두는 반시계 순회를 만들고, `i == cur`일 때 ccw가 0이라 자기 자신으로 갱신되지 않는다. 복잡도 $O(NH)$와 최악 $O(N^2)$도 맞다. 앞선 리포트(2026-07-07)가 지적한 "오목하게 파고들면 둘레도 줄어든다"는 서술은 이미 삭제됐고, 현재 31행은 볼록 조건을 먼저 고정한 뒤 넓이 최소를 찾는다는 순서로 정리돼 있다. 104행 괄호의 모호함은 별도 L2 항목으로 남겼다.
- recommendation: not-recorded
- gate_effect: info
