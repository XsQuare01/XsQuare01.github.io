schema_version: review-report/v2
target: closest-pair-2
generated_at: 2026-08-05
strict: true
sources: src/content/posts/closest-pair-2.md
summary: 🔴 0 · 🟡 3 · 🟢 6

## Findings

### 🟡 [D12] not-recorded

- severity: 🟡
- source: D
- rule_id: D12
- location: not-recorded
- quote: not-recorded
- message: 시리즈 다음 편 링크 누락: /blog/closest-pair-3(`closest-pair-3.md` 존재)을 본문에서 참조하지 않음
- recommendation: 237행 "이어지는 글"에서 Plane Sweeping을 언급하므로 그 자리에 `/blog/closest-pair-3` 링크를 붙인다
- gate_effect: warn

### 🟡 [L6] src/content/posts/closest-pair-2.md:137

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/closest-pair-2.md:137
- quote: vector<P> band;
- message: 노션 "Closest Pair" 아이디어 3은 밴드 점을 따로 빼내는 방식을 인정하면서 대가를 함께 적었다. 원문: "이해가 안된다면, 한 번 쭉 탐색하고 밴드 안에 있는 점들만 따로 빼낸다고 생각해도 된다. 다만, 추가 메모리 할당 비용이 발생한다." 원문 코드는 그래서 별도 배열을 만들지 않고 `cnt < 5` 조건으로 밴드 밖 점을 건너뛴다. 이 글은 원문이 대가를 밝힌 쪽을 택했는데 그 대가를 옮기지 않았다. 재귀 호출마다 `vector`를 새로 할당하므로 상수 인자에 실제로 영향이 있다.
- recommendation: 밴드를 따로 담는 선택이 읽기 쉬운 대신 호출마다 할당이 생긴다는 단서를 한 줄 붙이거나, 원문처럼 건너뛰는 구현을 대안으로 언급한다. 복잡도 차수는 그대로다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/closest-pair-2.md:215

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-2.md:215
- quote: 정렬의 하한 $\Omega(n \log n)$과 같은 차수이므로 이 문제는 이론적 하한에 도달한다.
- message: 증명 블록 안에서 외부 하한을 근거 없이 끌어온다. 점화식 유도는 분할 정복 글을 가리키지만, 하한 주장에는 출처도 모형도 없다. 가장 가까운 점 쌍의 $\Omega(n \log n)$은 대수적 결정 트리 모형에서 element uniqueness로 환원해 얻는 결과이고, 비교 기반 정렬의 하한과 같은 논거가 아니다. 모형을 밝히지 않으면 "이론적으로 최적"(230행)이 계산 모형과 무관한 단정으로 읽힌다. 1편 53행의 같은 주장에도 모형이 빠져 있어 두 편이 함께 걸린다.
- recommendation: 하한 문장을 증명 밖 비고로 옮기고 "대수적 결정 트리 모형에서"라는 조건을 붙인다. 정렬 하한과 같은 차수라는 표현은 유지해도 되지만, 근거가 정렬이 아니라 element uniqueness 환원임을 밝힌다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/closest-pair-2.md:1-242

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/closest-pair-2.md:1-242
- quote: not-recorded
- message: 검토 완료, 이슈 없음. ~다 평서체가 일관되고 과한 강조나 경구식 마무리가 없다. 강조는 개선의 핵심 대비(정렬을 새로 하기와 물려주기)에 몰려 있어 기능이 분명하다. 결정적 검사 D2·D3도 걸리지 않았다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/closest-pair-2.md:27-81

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/closest-pair-2.md:27-81
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 1편의 비용을 항목으로 뜯어 여분의 $\log n$이 나온 자리를 짚고, merge sort의 재활용 아이디어로 넘어가는 순서가 곧바로 이어진다. 74-79행 콜아웃이 `midX`를 재귀 전에 읽어야 하는 이유를 "인덱스는 그대로지만 그 자리의 값이 변한다"로 설명해, 독자가 스스로 부딪힐 함정을 미리 막는다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/closest-pair-2.md:63-146

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/closest-pair-2.md:63-146
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 분할은 x, 순서는 y라는 축 구분을 본문·콜아웃·코드 주석·비교 표에서 같은 말로 유지한다. `midX`, `merge`, `밴드`, combine 단계 번호(①②③)가 본문과 코드에서 같은 대상을 가리킨다.
- recommendation: 현재 용어 규약을 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/closest-pair-2/merge.svg:1-40

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/closest-pair-2/merge.svg:1-40
- quote: 두 y정렬 절반을 O(n) merge로 합치기
- message: 검토 완료, 이슈 없음. merge.svg의 예시가 실제로 맞는다. 왼쪽 `y = 1, 4, 7`과 오른쪽 `y = 2, 3, 8`을 합친 결과가 `1, 2, 3, 4, 7, 8`로 정렬 순서와 일치한다. complexity.svg의 레벨별 $O(n)$·깊이 $\log n$·전체 $O(n \log n)$도 보조정리 1과 정리 1의 주장과 맞는다.
- recommendation: 현재 레이블과 예시 수치를 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/closest-pair-2.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/closest-pair-2.md:2-4
- quote: 가장 가까운 점 쌍 ② — 정렬을 유지해 O(n log n)으로
- message: 검토 완료, 이슈 없음. 제목이 개선의 방법(정렬 유지)과 결과($O(n \log n)$)를 함께 담고, description이 여분 $\log n$의 출처, merge 대체, 분할축과 순서축 분리를 실제 본문 범위대로 요약한다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/closest-pair-2.md:106-149

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-2.md:106-149
- quote: 함수 종료 시 pts[st..ed] 는 y좌표로 정렬됨.
- message: 검토 완료, 이슈 없음. 코드의 불변식이 닫힌다. 호출 시점에 구간이 x정렬이라는 전제는 최상위의 한 번 정렬로 성립하고, 왼쪽 재귀가 자기 구간만 y정렬로 바꾸므로 오른쪽 재귀가 시작될 때 그 구간은 아직 x정렬이다. 따라서 `midX`를 재귀 전에 읽는 것으로 분할선이 정확히 보존된다. base(`ed - st < 3`)도 직접 비교 후 y정렬을 남겨 같은 사후 조건을 지킨다. 밴드 추리기가 y정렬 배열을 순서대로 훑어 밴드도 y정렬을 유지하고, 다음 7개 비교는 `j <= i + 7`로 상한이 정확하다. 2026-07-01 리포트의 `long long` 오버플로 지적은 182-187행 콜아웃으로 반영됐다.
- recommendation: 현재 불변식 서술과 콜아웃을 유지한다.
- gate_effect: info
