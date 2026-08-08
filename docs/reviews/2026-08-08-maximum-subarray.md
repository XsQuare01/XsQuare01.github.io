schema_version: review-report/v2
target: maximum-subarray
generated_at: 2026-08-08
strict: true
sources: src/content/posts/maximum-subarray.md
summary: 🔴 0 · 🟡 0 · 🟢 9

## Findings

### 🟢 [L1] src/content/posts/maximum-subarray.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/maximum-subarray.md:11
- quote: 배열의 원소가 전부 양수라면 답은 뻔하다. 무엇을 더 붙여도 합이 커지니 배열 전체가 답이다.
- message: 검토 완료, 이슈 없음
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/maximum-subarray.md:119

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/maximum-subarray.md:119
- quote: $k_i$ 에서 $k_{i+1}$ 로 넘어가는 규칙을 보자. $x = a_{i+1}$ 이라 하자. $a_1 \dots a_{i+1}$ 의 뒷조각은 두 종류다.
- message: 검토 완료, 이슈 없음
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/maximum-subarray.md:28

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/maximum-subarray.md:28
- quote: 아래에서는 연속 부분배열을 짧게 구간이라고도 부른다.
- message: 검토 완료, 이슈 없음
- recommendation: 현재 용어와 평서체를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/maximum-subarray/kadane-scan.svg:67

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/maximum-subarray/kadane-scan.svg:67
- quote: max(k₁ … k₈) = 9
- message: 검토 완료, 이슈 없음. 배열 값, k 수열, 끊기는 자리, 최댓값이 본문과 일치한다.
- recommendation: 현재 SVG를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/maximum-subarray/prefix-sum.svg:94

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/maximum-subarray/prefix-sum.svg:94
- quote: P₅ − P₂
- message: 검토 완료, 이슈 없음. 원소 값, 누적합 값, 경계 위치, 구간합 계산이 본문과 일치한다.
- recommendation: 현재 SVG를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/maximum-subarray/problem.svg:51

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/maximum-subarray/problem.svg:51
- quote: 중간의 −2 와 −6 은 통과한다. 앞의 2, 4 와 뒤의 8 을 한 구간에 함께 담으려면 연속이라는 조건 때문에 지나가야 한다.
- message: 반영 후 재판정. 통과 조건이 "앞의 2, 4 와 뒤의 8 을 한 구간에 함께 담으려면"으로 한정되어, $[8]$ 만 따로 고를 수 있다고 밝힌 본문 36행과 어긋나지 않는다. SVG의 구간 표시(a₃ … a₈ = 9)와 합계도 본문과 일치한다.
- recommendation: 조치 없음. 본문 36행과 이 주석의 한정 조건이 함께 유지되어야 한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/maximum-subarray.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/maximum-subarray.md:2
- quote: title: "최대 부분배열 — 자리마다 최선 하나만 들고 간다"
- message: 검토 완료, 이슈 없음
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/maximum-subarray.md:204

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/maximum-subarray.md:204
- quote: 여기서부터는 강의 노트 밖 확장이다.
- message: 검토 완료, 이슈 없음. 저장소 밖 Notion 원문은 이 환경에서 확보하지 못했으며, 현재 글은 강의 노트 밖 확장의 경계를 명시한다.
- recommendation: Notion 원문을 확보하면 현재 구조와 논지 및 확장 경계를 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/maximum-subarray.md:126

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/maximum-subarray.md:126
- quote: $k_0 = 0, \qquad k_{i+1} = \max(k_i + x,\; 0)$
- message: 검토 완료, 이슈 없음. 예시 합과 수열을 재계산했으며, 빈 뒷조각 포함 여부에 따른 두 점화식의 분류, 기저, 시간 및 공간 복잡도가 모두 타당하다.
- recommendation: 현재 논증과 복잡도 설명을 유지한다.
- gate_effect: info

## 후속 처리

🔴 1건을 반영했다. 본문은 고치지 않았고 SVG 주석만 바꿨다.

- 🔴 [L4] `problem.svg:51` 통과 조건 무한정 → **반영 완료**. "연속이라는 조건 때문에 뒤의 8 을 쓰려면 반드시 지나가야 한다"를 "앞의 2, 4 와 뒤의 8 을 한 구간에 함께 담으려면 연속이라는 조건 때문에 지나가야 한다"로 한정했다. 본문 36행이 이미 $[8]$ 만 따로 고를 수 있다고 밝히고 있었으므로 SVG만 본문에 맞춘 것이다. 해당 finding은 반영 후 재판정해 🟢으로 남긴다.

### 리포트 이후의 별도 수정 — 원문 언급 삭제

리뷰 반영과 무관하게, 정본 가이드에 새로 명시한 「원문을 본문에서 드러내지 않는다」를 적용했다.

- `:196` "강의 노트는 이 둘을 …이라 부른다" → "이 둘을 …이라 부르기도 한다". 귀속만 걷고 명칭과 이어지는 정밀화 설명은 그대로 두었다.
- `:204` "여기서부터는 강의 노트 밖 확장이다" → 삭제. 절 제목 「더 나가면」과 이어지는 "두 가지가 남았다"가 같은 역할을 하므로 논증에서 빠지는 것이 없다.

이 수정으로 위 🟢 [L6] finding이 인용한 204행이 사라졌다. 해당 판정은 그 문장이 있던 본문에 대한 것이므로 **L6(원문 충실성·확장 경계 표시)는 재리뷰 대상이다.** 확장 경계를 본문에서 걷어낸 뒤에도 추가 내용을 원문으로 오인할 여지가 없는지 판정이 필요하다. provenance 기록은 이 리포트와 포스트별 스펙에 남아 있다.

반영 후 검증: `npm run build` 성공, `python .claude/review_post.py --gate` 통과. 알고리즘·점화식·복잡도 주장은 바꾸지 않았다.
