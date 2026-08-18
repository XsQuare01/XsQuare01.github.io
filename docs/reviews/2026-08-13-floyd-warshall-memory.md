schema_version: review-report/v2
target: floyd-warshall-memory
generated_at: 2026-08-13
strict: true
sources: src/content/posts/floyd-warshall-memory.md
summary: 🔴 0 · 🟡 0 · 🟢 7

## Findings

### 🟢 [L1] src/content/posts/floyd-warshall-memory.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/floyd-warshall-memory.md:11
- quote: 답은 나오지만 $N^3$칸을 들고 있다. $N$이 1000이면 10억 칸이다. 정말 다 필요한가.
- message: 검토 완료, 이슈 없음
- recommendation: 질문으로 문제를 열고 증명으로 답하는 현재 ~다 평서체를 유지한다. 과한 수사, 줄표 남발, 경구식 마무리나 불필요한 문두 접속어가 없다.
- gate_effect: info

### 🟢 [L2] src/content/posts/floyd-warshall-memory.md:24

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/floyd-warshall-memory.md:24
- quote: 2층이면 충분하다
- message: 검토 완료, 이슈 없음
- recommendation: 3차원 배열에서 2층으로 줄인 뒤 제자리 갱신의 위험을 특정하고 불변식으로 닫는 순서가 명료하므로 현재 설명 흐름을 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/floyd-warshall-memory.md:26

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/floyd-warshall-memory.md:26
- quote: 위첨자 $k$가 그 제한을 가리키므로, $k$를 하나 올릴 때마다 층이 한 장 쌓인다고 보면 된다.
- message: 검토 완료, 이슈 없음
- recommendation: 층, k단계, k행, k열, 덮어쓰기와 $D^k[i][j]$ 표기가 본편의 정의와 일관되므로 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/floyd-warshall-memory.md:60

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/floyd-warshall-memory.md:60
- quote: `layers.svg`, `overwrite-safe.svg`
- message: 검토 완료, 이슈 없음
- recommendation: 두 SVG를 각각 렌더링해 확인했다. `layers.svg`의 N³, 2N², N² 단계와 화살표, `overwrite-safe.svg`의 k행 및 k열 강조, `(k,k)=0`, 대입식이 본문과 일치하며 레이블, 값, 연결, 강조, 캡션에 잘림이 없다.
- gate_effect: info

### 🟢 [L5] src/content/posts/floyd-warshall-memory.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/floyd-warshall-memory.md:2
- quote: title: "플로이드·워셜의 메모리 줄이기 — N³칸에서 N²칸으로"
- message: 검토 완료, 이슈 없음
- recommendation: 제목은 최종 공간 축소를 정확히 드러내고 description은 2층과 1층 축소 및 덮어쓰기 증명을 실제 본문 범위대로 요약하므로 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/floyd-warshall-memory.md:24

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/floyd-warshall-memory.md:24
- quote: 2층이면 충분하다
- message: 검토 완료, 이슈 없음
- recommendation: 직접 Notion 비교는 현재 접근 수단이 없어 불가능하다. 매핑된 설계 스펙 `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md`와 대조하면 2층 축소, 1층 덮어쓰기 증명, 밀집 그래프 비교의 핵심 줄기와 두 갈래 증명이 보존되어 있으므로 현 상태를 유지한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/floyd-warshall-memory.md:28

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/floyd-warshall-memory.md:28
- quote: 점화식은 $D^k[i][j] = \min(D^{k-1}[i][j],\ D^{k-1}[i][k] + D^{k-1}[k][j])$였다.
- message: 검토 완료, 이슈 없음
- recommendation: 4노드 비음수 무방향 그래프 4096개를 전수 계산해 3차원, 두 버퍼, 제자리 구현의 결과가 같고 매 k단계의 k행과 k열이 보존됨을 확인했다. 2층 증명은 주점화식이 k층에서 k-1층만 읽는다는 사실에 직접 따르고, 1층 증명은 본편 정리 1로 단순 길만 겨뤄도 된다는 점과 비음수 전제에서 대각선이 0이라는 사실에 기대어 sound하게 닫힌다. 시간 O(N³), 공간 O(N²) 주장도 반복문과 배열 크기에 맞으므로 유지한다.
- gate_effect: info
