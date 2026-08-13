schema_version: review-report/v2
target: floyd-warshall-memory
generated_at: 2026-08-12
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
- message: 검토 완료, 이슈 없음. 도입의 질문형 문장과 이후 평서체가 자연스럽게 이어지고, 줄표·대칭 문장·강조·접속어·의존 명사 등도 의미를 흐릴 정도로 반복되지 않는다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/floyd-warshall-memory.md:24

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/floyd-warshall-memory.md:24
- quote: 2층이면 충분하다
- message: 검토 완료, 이슈 없음. $k-1$층만 읽는 관찰에서 2층 구현으로, 제자리 갱신의 위험에서 $k$행·$k$열 불변성 증명으로, 마지막에는 밀집 그래프 성능 비교로 진행해 전제와 결론의 이동이 명료하다.
- recommendation: 현재 설명 순서와 논증 연결을 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/floyd-warshall-memory.md:28

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/floyd-warshall-memory.md:28
- quote: 점화식은 $D^k[i][j] = \min(D^{k-1}[i][j],\ D^{k-1}[i][k] + D^{k-1}[k][j])$였다.
- message: 검토 완료, 이슈 없음. 층·단계·노드·간선·최단 거리와 $D^k$ 표기가 글 전체와 연결된 본편에서 같은 의미로 유지되며 어체도 ~다 평서체로 통일되어 있다.
- recommendation: 현재 용어와 표기를 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/floyd-warshall-memory.md:60

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/floyd-warshall-memory.md:60
- quote: ![N³칸을 두 층으로, 다시 한 층으로 줄인다.](/images/floyd-warshall-memory/layers.svg)
- message: 검토 완료, 이슈 없음. layers.svg를 텍스트와 렌더링으로 확인했으며 N³→2N²→N², prev/curr, D[k%2], 진행 화살표가 본문과 일치하고 클리핑이 없다. overwrite-safe.svg도 $k$행·$k$열 강조, $(k,k)=0$, 열 방향 등식과 덮어쓰기 결론이 본문 95–126행과 일치하며 경로·레이블·강조의 잘림이 없다. 행 방향 등식은 그림에서 대칭으로 암시되고 본문에서 명시된다.
- recommendation: 두 SVG의 현재 레이블, 화살표, 강조와 배치를 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/floyd-warshall-memory.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/floyd-warshall-memory.md:2
- quote: title: "플로이드·워셜의 메모리 줄이기 — N³칸에서 N²칸으로"
- message: 검토 완료, 이슈 없음. 제목은 3차원 DP를 2층과 1층으로 줄이는 중심 질문을 정확히 나타내고, description은 층 의존성·$k$행과 $k$열 불변성·덮어쓰기 안전성까지 실제 본문 범위를 충실히 요약한다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/floyd-warshall-memory.md:24

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/floyd-warshall-memory.md:24
- quote: 2층이면 충분하다
- message: 검토 완료, 이슈 없음. direct Notion comparison was unavailable. provenance handoff인 docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md만 대조했으며, 2층·1층 축소와 두 갈래 불변성 논증, 측정 없는 밀집 그래프 성능 서술을 조건부로 좁힌 범위가 handoff의 원천·승인 범위와 일치한다. Notion 원문 자체를 확인했다는 판정은 하지 않았다.
- recommendation: 직접 Notion 원문에 접근할 수 있을 때 핵심 구조·증명 흐름·누락 여부를 추가 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/floyd-warshall-memory.md:46

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/floyd-warshall-memory.md:46
- quote: for (int k = 1; k <= n; k++) {
- message: 검토 완료, 이슈 없음. D[0] 초기화 뒤 prev=(k-1)%2, curr=k%2인 두 층 인덱싱은 정확하다. 비음수 무방향 행렬 760개(n=1..4)를 전수 계산해 매 $k$에서 3차원 기준, 두 층, 제자리 결과와 $k$행·$k$열 불변성 및 대각선 0을 대조해 모두 일치했다. 제자리 문장은 대상 D[i][j]를 같은 문장에서 갱신 전에 읽고, 먼저 덮일 수 있는 D[i][k]·D[k][j]는 불변이므로 순서가 안전하다. 대각선 0 증명은 비음수 전제와 기저로 닫히며, 본편 정리 1은 제한을 지키는 길에서 반복 노드를 길이 증가 없이 제거하므로 끝점 $k$가 중간 노드로 재등장하지 않는다는 의존성도 타당하다. 공간 O(N³)→O(N²), 시간 O(N³), 밀집 그래프의 힙 O(N³ log N)·배열 O(N³) 비교와 실제 성능이 그래프·구현·기계에 달린다는 한정도 정확하다.
- recommendation: 현재 인덱싱, 증명 전제, 본편 정리 의존성과 복잡도·성능 한정을 유지한다.
- gate_effect: info

## 반영 결과 (2026-08-12, 2차)

- 본편 `all-pairs-shortest-path.md:243`의 🔴 [L7]을 고치며 본편 의사코드에 `INF` 검사가 들어갔다. 이 글의 두 의사코드(2층 :39–, 1층 :69–)에는 검사를 넣지 않고, 검사를 덜어냈다는 사실과 그 규칙이 층 수와 무관하게 그대로 필요하다는 점을 :36에 한 문장으로 밝혔다. 이 글의 주제가 메모리 축소여서 층 인덱스가 보여야 하고, 1층 코드의 결론인 "세 겹 `for`와 `min` 하나"라는 축소 논지를 검사 상용구가 덮지 않게 하기 위해서다.
- 검사는 셀 단위 판정이라 `prev`/`curr` 홀짝 배선이나 제자리 갱신 순서와 상호작용하지 않는다. 정리 1도 그대로 성립한다. $D^{k-1}[k][k] = 0$이 유한하므로 $j=k$·$i=k$ 대입에서 검사가 덧셈을 막지 않고, $D[i][k]$가 `INF`인 경우에는 양쪽 인자가 모두 `INF`라 최솟값이 `INF`로 같다.
- 위치 갱신: :32에 문단 하나가 들어가 이후 finding 위치를 L4 52→54, L7 40→42로 옮겼다.
- 재검증: `python .claude/review_post.py src/content/posts/floyd-warshall-memory.md` 발견 사항 없음, `python .claude/review_post.py --gate` exit 0, `npm run build` 성공.

## 반영 결과 (2026-08-13, 읽힘 패스)

- 판정을 바꾸는 수정은 없다. 정리 1과 그 증명, 두 층 홀짝 인덱싱, 두 의사코드, 복잡도 주장은 손대지 않았다. 산문의 문단 경계와 도입 문장만 다뤘다.
- `:120`(현재 `:134`)의 `$M \simeq N^2$`를 「간선 수 $M$이 대략 $N^2$개인 경우」로 풀었다. 이 글에서 설명 없이 쓰이던 `\simeq`가 사라졌다.
- 이 글만 읽는 독자를 위해 $D^k[i][j]$의 뜻과 위첨자 $k$가 층을 가리킨다는 풀이를 첫 등장 자리(`:26`)에 붙였다.
- `$O(M\log N) = O(N^2\log N)$`처럼 머릿속에서 대입하던 단계를 지면에 적었고, `$2N^2$`이 $O(N^2)$이 되는 근거(상수배를 세지 않음)도 함께 밝혔다. 「공간이 $O(N^3) \to O(N^2)$」이라는 화살표 조각문은 평서문으로 폈다.
- 정리 1 앞(`:99`)에 무엇을 보이면 끝나는지와 근거가 두 갈래라는 예고를 한 문단 넣었다. 증명 블록 바깥이며 증명 단계를 대신하지 않는다. 증명 내부는 한 글자도 고치지 않았다.
- 수식 5개 이상을 담던 긴 문단을 나눴다: 층 참조 관찰, 덮어쓰기 위험 진단, 읽는 칸 셋의 분석, 상수·메모리 접근 비교. 문장은 그대로 두고 문단 경계만 넣었다.
- 위치 갱신: L3 26→28, L4 54→60, L7 42→46. L4 message의 본문 범위도 83–112행→95–126행으로 옮겼다.
- 재검증: `python .claude/review_post.py src/content/posts/floyd-warshall-memory.md` 발견 사항 없음, `python .claude/review_post.py --gate` exit 0, `npm run build` 성공, 빌드 산출물의 raw `$` 0개.
