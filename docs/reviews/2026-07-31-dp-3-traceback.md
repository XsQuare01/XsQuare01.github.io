schema_version: review-report/v2
target: dp-3-traceback
generated_at: 2026-07-31
strict: false
summary: 🔴 1 · 🟡 4 · 🟢 4

## Findings

## 결정적 검사: src/content/posts/dp-3-traceback.md
발견 사항 없음 ✅

## LLM 비평

### 🔴 [L7] src/content/posts/dp-3-traceback.md:106

- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/dp-3-traceback.md:106
- quote: 복원은 `split` 표를 요구한다. 비용값 `m[i][j]`만으로는 그 비용을 낸 분할점을 되짚을 수 없으므로, $O(n^2)$개 구간마다 분할점 하나씩을 따로 저장해 둬야 한다.
- message: 제시한 방법에서 `split`은 분할점을 상수 시간에 찾는 데 필요하지만, 복원 자체의 필수 조건은 아니다. `m`과 차원 배열 `d`가 있으면 방문한 각 구간에서 점화식을 만족하는 `k`를 다시 탐색할 수 있다. 따라서 $O(n^2)$ 추가 저장 공간은 필수 하한이 아니라 시간과 공간의 절충이다.
- recommendation: 주장을 한정하고, 저장 공간을 줄이는 대안으로 `m`과 `d`에서 `k`를 다시 계산할 수 있다고 설명한다.
- gate_effect: fail

### 🟡 [L1] src/content/posts/dp-3-traceback.md:73

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/dp-3-traceback.md:73
- quote: 먼저 **조각 A** — 분할점 기록이다.
- message: 강조 표기와 줄표를 결합한 문장이 설명의 흐름보다 형식적인 구획을 앞세운다.
- recommendation: 줄표 없이 조각 A가 분할점 기록 코드라는 사실을 평서문으로 쓴다.
- gate_effect: warn

### 🟡 [L1] src/content/posts/dp-3-traceback.md:88

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/dp-3-traceback.md:88
- quote: 다음은 **조각 B** — 재귀 복원이다.
- message: 앞 문장과 대칭인 강조 및 줄표 구성이 반복되어 문장이 도식적으로 들린다.
- recommendation: 줄표 없이 조각 B가 재귀 복원 코드라는 사실을 평서문으로 쓴다.
- gate_effect: warn

### 🟡 [L1] src/content/posts/dp-3-traceback.md:114

- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/dp-3-traceback.md:114
- quote: $m[1][3]=28$이라는 값 뒤에는 $(M_1(M_2M_3))$이라는 구체적인 구성이 항상 함께 있었다.
- message: 비유적이고 경구적인 표현이며, 비용값 자체에 구성이 본래 들어 있는 것처럼 과장한다. 앞서 설명했듯 `m`만 저장하면 그 구성을 바로 알 수 없다.
- recommendation: 저장한 분할점 정보로 해당 괄호화를 복원할 수 있다는 사실 중심의 문장으로 바꾼다.
- gate_effect: warn

### 🟡 [L2] src/content/posts/dp-3-traceback.md:29

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/dp-3-traceback.md:29
- quote: 표를 지우지만 않으면 그 정보는 그대로 남아 있다.
- message: 바로 앞에서 `m`은 비용만 저장한다고 설명했으므로 이 문장은 설명과 모순된다. 이긴 `k`는 따로 기록하지 않으면 비교가 끝날 때 사라진다.
- recommendation: 분할점은 계산 과정에서 결정되지만 별도 표에 기록해야 남는다고 명확히 쓴다.
- gate_effect: warn

### 🟢 [L3] src/content/posts/dp-3-traceback.md:43

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/dp-3-traceback.md:43
- quote: 분할점을 모두 적어 두면, 그 표를 따라 실제 괄호화를 거꾸로 짜맞출 수 있다. 구간 $[i,j]$에 대해 $build(i,j)$를 정의하자.
- message: 검토 완료, 이슈 없음
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L4] public/images/dp-3/traceback.svg:11

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/dp-3/traceback.svg:11
- quote: `split[1][3] = 1`, `split[2][3] = 2`, `(M₁(M₂M₃))  ·  cost 28`
- message: 검토 완료, 이슈 없음
- recommendation: 조치 없음. SVG의 분할값, 트리 경로, 괄호화, 비용 28이 본문과 일치한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/dp-3-traceback.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/dp-3-traceback.md:2
- quote: title: "추가 설명 — 어떤 순서로 곱했는지 되짚기"
- message: 검토 완료, 이슈 없음
- recommendation: 조치 없음. 제목과 description이 복원, 분할점 저장, 예시, 트리, 동점을 정확히 나타낸다.
- gate_effect: info

### 🟢 [L6] src/content/posts/dp-3-traceback.md:11

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/dp-3-traceback.md:11
- quote: 이 글은 강의 노트 밖 확장으로, 채운 표에 분할점을 함께 적어 그 순서까지 복원하는 방법을 다룬다.
- message: 검토 완료, 이슈 없음
- recommendation: 조치 없음. 글이 강의 노트 밖 확장임을 명시하고 저장소 설계 문서가 이 provenance를 승인한다. 이 확장에 대응하는 Notion 원문이 있다고 주장하지 않는다.
- gate_effect: info

요약: 🔴 1 · 🟡 4 · 🟢 4

---

## 후속 처리

- 🔴 [L7] :106 복원이 `split` 표를 요구한다는 과한 단정 → `split`은 분할점을 $O(1)$에 돌려주는 최적화일 뿐이며, `m`과 `d`에서 $m[i][k]+m[k+1][j]+d_{i-1}d_k d_j = m[i][j]$인 $k$를 재탐색해도 복원되므로 $O(n^2)$ 저장은 필수 하한이 아니라 시간·공간 절충임을 명시하도록 수정.
- 🟡 [L2] :29 "표를 지우지만 않으면 그 정보는 그대로 남아 있다"가 `m`은 비용만 담는다는 앞 설명과 모순 → 이긴 $k$는 표를 채우는 동안 정해지지만 `m`에 함께 저장되지 않으므로 따로 붙잡아 둬야 한다고 정정.
- 🟡 [L1] :114 마치며의 "값 뒤에는 구성이 항상 함께 있었다"는 경구·과장 → 표는 비용만 돌려주며, 저장한(또는 재계산한) 분할점으로 괄호 순서를 복원한다는 사실 중심 문장으로 교체.
- 🟡 [L1] :73·:88 조각 A·B 라벨의 `강조 + 줄표` 구획 → 줄표 없이 "조각 A는 분할점을 기록한다 / 조각 B는 재귀로 복원한다"는 평서문으로.
- 반영 후 `npm run build` 성공(130 페이지). 예시 수치(`split[1][3]=1`, `split[2][3]=2`, `(M₁(M₂M₃))`, 비용 28)·SVG 불변. 🟢 4(L3·L4·L5·L6)는 조치 없음.
