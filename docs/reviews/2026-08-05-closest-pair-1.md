schema_version: review-report/v2
target: closest-pair-1
generated_at: 2026-08-05
strict: true
sources: src/content/posts/closest-pair-1.md
summary: 🔴 0 · 🟡 2 · 🟢 6

## Findings

### 🟡 [L7] src/content/posts/closest-pair-1.md:53

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-1.md:53
- quote: 정렬 없이 1차원 가장 가까운 쌍을 찾는 것은, 값들 사이에 일정 거리 이하인 두 값이 있는지 판별하는 것(uniqueness)과 계산 복잡도가 동등하다는 것이 알려져 있다.
- message: 2026-07-01 리포트의 L2 지적(당시 52행) 중 절반만 반영됐다. `uniqueness`를 괄호로 풀어 준 부분은 지금 문장에 있으나 두 가지가 남았다. 첫째, 괄호 안 설명("일정 거리 이하인 두 값이 있는지 판별")은 element uniqueness가 아니라 근접성 판별이다. element uniqueness는 "모든 값이 서로 다른가"이고 거리 문턱이 없다. 둘째, 이 하한은 대수적 결정 트리(algebraic decision tree) 모형에서 성립하는 결과인데 모형을 밝히지 않아 무조건적 하한으로 읽힌다. 하한을 인용하는 문장이라 모형이 빠지면 주장 범위가 실제보다 넓어진다.
- recommendation: 괄호 설명을 "모든 값이 서로 다른지 판별(element uniqueness)"로 바로잡고, "대수적 결정 트리 모형에서 $\Omega(n \log n)$이 알려져 있다"처럼 모형을 밝힌다. 환원 과정까지 싣지 않는다면 다루지 않는다고 한 줄 남긴다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/closest-pair-1.md:130

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-1.md:130
- quote: 좌표값이 클 때 오버플로를 막기 위해 `long long`을 사용한다.
- message: 2026-07-01 리포트의 같은 지적(당시 119행)이 반영되지 않았다. `long long`은 좌표 범위가 제한될 때만 제곱거리를 담는다. 본문은 입력 좌표 범위를 밝히지 않아 `dx * dx + dy * dy`가 언제나 안전하다는 인상을 준다. 2편은 이 지적을 반영해 "long long이 안전한 범위" 콜아웃(closest-pair-2.md:182-187)에서 좌표 범위와 제곱거리 상한, `__int128` 대안까지 적었다. 같은 코드 관용을 쓰는 두 편이 서로 다른 수준으로 설명하고 있다.
- recommendation: 2편의 콜아웃과 같은 내용을 1편에도 두거나, 1편에서 2편의 그 콜아웃을 가리킨다. 두 편의 설명 수준을 맞추는 편이 낫다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/closest-pair-1.md:1-283

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/closest-pair-1.md:1-283
- quote: not-recorded
- message: 검토 완료, 이슈 없음. ~다 평서체가 일관되고 경구식 마무리나 과한 비유가 없다. 줄표는 대부분 삽입구(39·61·78행)로 쓰여 기능이 분명하고 결정적 검사 D2·D3도 걸리지 않았다. 정의·보조정리·정리 조판이 들어온 뒤에도 문장 밀도가 고르다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/closest-pair-1.md:27-146

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/closest-pair-1.md:27-146
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 브루트포스에서 1차원 직관, 2차원 분할 정복, 밴드, 다음 7개, 복잡도로 이어지는 순서에 도약이 없다. 99행이 "밴드 안 점이 너무 많으면 어떻게 되는가"로 다음 절의 필요를 미리 세우고, 117행 콜아웃이 7의 근거를 요약한 뒤 별도 글로 넘긴다. 하한 논거의 정확성 문제는 별도 L7로 분리했다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/closest-pair-1.md:61-130

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/closest-pair-1.md:61-130
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 점·쌍·거리·밴드·Combine·분할 정복을 끝까지 같은 말로 쓴다. 거리를 제곱으로 다룬다는 규약을 123행과 130행에서 밝히고 코드 주석도 같은 규약을 쓴다. $D$(거리)와 $d$(거리 제곱)의 구분이 본문과 코드에서 어긋나지 않는다.
- recommendation: 현재 용어 규약을 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/closest-pair/band.svg:1-40

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/closest-pair/band.svg:1-40
- quote: Combine — 분할선 좌우 폭 D 밴드
- message: 검토 완료, 이슈 없음. band.svg의 분할선·좌우 영역·$D_L$·$D_R$·$D = \min(D_L, D_R)$ 표기가 본문 67-95행과 맞고, complexity.svg의 깊이 $\log n$·레벨별 $O(n \log n)$·전체 $O(n \log^2 n)$이 146행 증명과 맞는다. 밴드 폭을 19·268행은 "폭 $D$", 117행은 "폭 $2D$(좌우 각 $D$)"로 적어 표현이 갈리지만, 정의 1(91행)이 "분할선에서 x좌표 차이가 $D$ 이내"로 못 박고 SVG 레이블도 "좌우 폭 D"라 본문과 그림 사이에 충돌은 없다. 값을 정하는 자리가 정의 1이므로 별도 지적으로 올리지 않는다.
- recommendation: 밴드 폭을 다시 언급할 때는 정의 1의 표현을 따른다.
- gate_effect: info

### 🟢 [L5] src/content/posts/closest-pair-1.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/closest-pair-1.md:2-4
- quote: 가장 가까운 점 쌍 ① — 분할 정복과 O(n log²n)
- message: 검토 완료, 이슈 없음. 제목이 1편의 범위(분할 정복, $O(n \log^2 n)$)를 그대로 담고, description이 브루트포스 대비와 좌우 분할, 밴드 합치기, 복잡도 유도를 실제 본문 순서대로 요약한다. 41행이 2편에서 $O(n \log n)$으로 개선한다고 미리 밝혀 이 편의 경계도 분명하다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/closest-pair-1.md:59-146

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/closest-pair-1.md:59-146
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 노션 "Closest Pair"를 notion-fetch로 가져와 대조했다. 이전 리포트는 도구가 없어 대조하지 못했다고 기록했다. 원문 줄기가 모두 보존됐다 — x좌표 정렬 후 좌우 분할, `D = min(DL, DR)`, 기준선 좌우 `D` 밴드, 밴드 안 점만 비교, 밴드 점 y정렬 후 상수 개 비교, x 재정렬, 총 $O(N \log^2 N)$. 원문의 복잡도 유도(초기 정렬 1회 + 레벨당 약 $O(N \log N)$ + 깊이 $\log N$)도 146행 증명과 같은 구조다. 원문이 `j <= 5`를 쓴 자리에서 이 글은 7을 쓰는데, 그 차이는 117행이 가리키는 별도 글에서 다루므로 무표시 변경이 아니다.
- recommendation: 7과 원문 5의 차이를 다루는 별도 글 링크를 유지한다.
- gate_effect: info
