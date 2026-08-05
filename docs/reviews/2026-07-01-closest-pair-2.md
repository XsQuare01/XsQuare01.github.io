schema_version: review-report/v2
target: closest-pair-2
generated_at: 2026-07-01
strict: not-recorded
summary: 🔴 0 · 🟡 1 · 🟢 6

## Findings

### 🟡 [L7] src/content/posts/closest-pair-2.md:95

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-2.md:95
- quote: "// 두 점 사이 거리의 제곱 (루트 회피, long long 사용)"
- message: `long long` 거리 제곱 계산은 좌표 범위가 충분히 작다는 전제가 있을 때만 안전하다. `dx * dx + dy * dy`는 임의의 `long long` 좌표 입력에서는 signed overflow가 날 수 있다.
- recommendation: 제곱거리가 `long long`에 들어가는 입력 범위를 명시하거나, 범위를 일반화하려면 `__int128` 계산으로 바꾼다고 설명한다.
- gate_effect: warn

### 🟢 [L1] not-recorded

- severity: 🟢
- source: L
- rule_id: L1
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 현재의 ~다 평서체와 강조 빈도를 유지한다.
- gate_effect: info

### 🟢 [L2] not-recorded

- severity: 🟢
- source: L
- rule_id: L2
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 1편의 병목에서 y정렬 유지 아이디어, midX 보존, 복잡도 개선으로 이어지는 흐름을 유지한다.
- gate_effect: info

### 🟢 [L3] not-recorded

- severity: 🟢
- source: L
- rule_id: L3
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: x좌표 분할, y정렬 유지, merge, Combine 용어를 현재처럼 일관되게 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/closest-pair-2/merge.svg:5

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/closest-pair-2/merge.svg:5
- quote: "두 y정렬 절반을 O(n) merge로 합치기"
- message: 검토 완료, 이슈 없음
- recommendation: merge.svg와 complexity.svg의 레이블·복잡도 표기는 본문 설명과 일치한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/closest-pair-2.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/closest-pair-2.md:2
- quote: "가장 가까운 점 쌍 ② — 정렬을 유지해 O(n log n)으로"
- message: 검토 완료, 이슈 없음
- recommendation: 제목과 description이 2편의 핵심인 y정렬 유지와 $O(n \log n)$ 개선을 잘 대표한다.
- gate_effect: info

### 🟢 [L6] not-recorded

- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 현재 세션에서 notion-search/notion-fetch 도구가 제공되지 않아 노션 원문 대조는 수행하지 못했다.
- recommendation: 원문 충실성 확인이 필요하면 Notion MCP가 연결된 환경에서 재검토한다.
- gate_effect: info

## 후속 처리

2026-08-05 재리뷰(`docs/reviews/2026-08-05-closest-pair-2.md`)에서 처리 상태를 확인했다. 이 리포트의 판정은 2026-07-01 시점 근거로 그대로 남긴다.

- 🟡 [L7] :95 `long long` 좌표 범위 전제 → **반영 완료**. "long long이 안전한 범위" 콜아웃(현재 182-187행)에서 좌표 범위, 제곱거리 상한, 범위를 넘길 때의 `__int128`·평행이동 대안까지 밝혔다. 권고보다 넓게 반영됐다.
- 🟢 [L6] 노션 원문 대조 미수행 → **해소**. 2026-08-05 재리뷰에서 `notion-fetch`로 원문을 가져와 대조했다. 그 대조에서 원문이 밴드 추출 방식의 메모리 대가를 밝혔다는 점을 새로 찾아 L6로 기록했다.

재리뷰가 새로 찾은 🟡 3건(시리즈 링크 D12, 원문 메모리 대가 L6, 하한 인용 모형 L7)은 그 리포트에 있다.
