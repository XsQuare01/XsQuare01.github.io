schema_version: review-report/v2
target: all-pairs-shortest-path
generated_at: 2026-08-12
strict: true
sources: src/content/posts/all-pairs-shortest-path.md
summary: 🔴 0 · 🟡 1 · 🟢 10

## Findings

### 🟡 [L7] src/content/posts/all-pairs-shortest-path.md:143

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/all-pairs-shortest-path.md:143
- quote: 정리 1이 같은 노드를 두 번 지나지 않는 길만 겨루게 해도 최솟값이 그대로임을 보장하고, 그런 길은 유한 개라서 최솟값을 실제로 내는 길이 존재한다.
- message: 결론은 옳으나 두 문장의 의존 방향이 한 바퀴 돈다. 정리 1의 진술과 증명은 "제한 $S$ 아래 최단 거리를 내는 길 $Q$를 하나 잡는다"로 시작해 최솟값이 실제로 달성된다는 사실을 이미 전제한다(:123, :131). 이 줄은 반대로 그 달성 사실을 정리 1에서 끌어온다. 또한 정리 1은 "최단 거리를 내는 길 중에 단순한 것이 있다"를 말할 뿐이고, 이 줄이 실제로 쓰는 명제는 "임의의 길을 단순한 길로 바꿔도 길이가 늘지 않는다"라 진술 범위가 한 칸 넓다. 유한 그래프이므로 결론(최솟값 달성, 단순 경로로 제한해도 최솟값 불변)은 참이고 정리 1의 증명 기계도 그대로 쓸 수 있다. 증명 본문에서 최소성을 쓰는 곳은 마지막 한 문장뿐이고 잘라내기 논증 자체는 임의의 길에 적용되므로, 진술을 임의의 길로 넓히면 순환이 풀린다.
- recommendation: 정리 1의 진술을 "제한 $S$를 지키는 임의의 길은 같은 제한을 지키면서 같은 노드를 두 번 지나지 않고 길이도 늘지 않는 길로 바꿀 수 있다"로 넓히고, 최솟값 달성과 현재의 최단 경로 형태 진술을 그 따름정리로 둔다. 증명 문단은 마지막 문장만 손대면 되고 잘라내기 논증과 비음수 전제가 쓰이는 자리는 그대로 남는다. 증명 구조를 바꾸는 수정이므로 이번 리뷰에서는 반영하지 않았다. 사람 판정 대상이다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/all-pairs-shortest-path.md:147

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/all-pairs-shortest-path.md:147
- quote: $P$는 $k$번 노드를 중간에 지나거나 지나지 않는다. 둘 중 하나이고 둘 다일 수는 없다. 이 갈림이 그대로 점화식의 두 항이 된다.
- message: 검토 완료, 이슈 없음. 줄표는 frontmatter 제목의 구조적 줄표 하나뿐이고 문장 내부에는 없다. 문두 접속어 0회, 의존명사 '것' 10회, 접미사 '-들' 3회로 229행 분량 대비 남용이 아니다. 굵게는 두 경우의 이름표(:149, :157)와 반대 방향·유일성·동점 세 표지(:167, :179, :181)에만 붙어 역할이 일정하다. 경구식 절 마무리나 과한 비유는 없고 어체는 끝까지 ~다 평서체다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/all-pairs-shortest-path.md:118

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/all-pairs-shortest-path.md:118
- quote: 그 전에 정리 하나가 필요하다. 길을 두 조각으로 자르는 논증이 뒤에 나오는데, 같은 노드가 여러 번 등장하면 어디서 잘라야 할지가 정해지지 않는다.
- message: 검토 완료, 이슈 없음. 정리 1을 세우기 전에 그 정리가 왜 필요한지를 먼저 말해 도구가 불쑥 나오지 않는다. 점화식 절은 길이 없는 경우를 먼저 털고(:143), 유일성을 쓰지 않겠다고 예고한 뒤 길 하나를 고정하고(:145), 두 경우로 가른 다음(:147) 반대 방향으로 등호를 닫는(:167) 순서라 각 문단의 역할이 하나씩이다. 「새 알고리즘이 놓일 자리」 절은 그 눈금이 증명된 하한이 아니라고 스스로 한정한다(:57).
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/all-pairs-shortest-path.md:145

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/all-pairs-shortest-path.md:145
- quote: 최단 거리는 하나뿐이지만 그 거리를 내는 길은 여러 개일 수 있다. "그 최단 경로"라고 지목하면 있지도 않은 유일성을 슬쩍 빌려 쓰게 되니, 그런 길 중 **아무거나 하나를 골라** $P$라 한다.
- message: 검토 완료, 이슈 없음. 노드·간선·가중치·중간 노드·층으로 용어가 고정되어 있고 정점·엣지·레이어 같은 변형이 섞이지 않는다. '길'과 '최단 경로'가 함께 쓰이지만 무작위 혼용이 아니다. 낱개 대상은 '길'이고 유일성을 논하는 합성어 자리에서만 '최단 경로'다(:145, :181, :218). 이 줄이 그 구분을 직접 설명한다. $D^k[i][j]$ 표기와 의사코드 `D[k][i][j]`도 층·행·열 순서가 같다.
- recommendation: 현재 용어 분담과 평서체를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/all-pairs-shortest-path/k-meaning.svg:77

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/all-pairs-shortest-path/k-meaning.svg:77
- quote: 쓸 수 있다는 뜻이지 반드시 써야 한다는 뜻이 아니다
- message: 검토 완료, 이슈 없음. 세 패널의 허용 중간 노드 집합이 각각 공집합, {1}, {1,2}이고 초록 강조가 허용 노드에만 붙어 :65 정의와 맞는다. 세 패널의 간선 배치는 1-2, 1-3, 1-4, 2-4, 3-4 다섯 개로 :79와 :80의 목록과 같고 2-3 간선이 없다. 캡션은 :67의 "제한은 쓸 수 있다이지 반드시 써야 한다가 아니다"와 같은 말이다.
- recommendation: 현재 SVG를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/all-pairs-shortest-path/problem.svg:48

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/all-pairs-shortest-path/problem.svg:48
- quote: 아직 채우지 않은 빈 칸
- message: 반영 후 재판정. 그래프는 노드 4개와 간선 5개이고 각 가중치 배지가 1, 5, 7, 1, 10으로 :79와 :80의 간선 목록과 일치하며 2-3 간선이 없다. 오른쪽 4×4 격자는 빈 칸이고 부제 "답은 한 개가 아니라 N² 개다"는 :29와 맞는다. 원래 범례는 물음표 기호를 설명했으나 격자 안에 물음표 글리프가 하나도 그려지지 않아 없는 기호를 가리켰다. 범례 문구를 격자의 실제 모습에 맞췄다.
- recommendation: 조치 없음. 격자에 기호를 넣게 되면 범례도 함께 되돌린다.
- gate_effect: info

### 🟢 [L4] public/images/all-pairs-shortest-path/recurrence.svg:41

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/all-pairs-shortest-path/recurrence.svg:41
- quote: 고른 길에 같은 노드가 두 번 나오지 않으므로, k를 지난다면 정확히 한 번 지난다
- message: 반영 후 재판정. 위 갈래의 레이블 D^{k-1}[i][j]와 아래 갈래의 D^{k-1}[i][k], D^{k-1}[k][j]가 :152와 :160의 두 부등식 좌변과 정확히 대응하고, min으로 모여 D^k[i][j]가 되는 배선도 :176과 맞는다. 원래 캡션은 모든 최단 경로가 단순하다는 전칭 주장과 k를 언제나 지난다는 주장을 함께 담아 :145의 "고를 수 있다"와 :147의 두 경우 갈림보다 강했다. 고른 길로 한정하고 k를 지나는 갈래에 조건을 달았다.
- recommendation: 조치 없음. 본문 :145의 선택 논법과 이 캡션의 한정이 함께 유지되어야 한다.
- gate_effect: info

### 🟢 [L4] public/images/all-pairs-shortest-path/simulation.svg:173

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/all-pairs-shortest-path/simulation.svg:173
- quote: 3→4는 k=1에서 1번을 버렸지만 k=2에서 3→1→2→4 = 7로 되살아난다
- message: 검토 완료, 이슈 없음. 세 행렬을 칸 단위로 재계산해 대조했다. k=0은 인접 행렬이고 대각이 0, (2,3)과 (3,2)가 INF다. k=1은 (2,3)과 (3,2)만 6으로 바뀌며 초록 강조가 정확히 그 두 칸에 붙는다. k=2는 (1,4)와 (4,1)이 2, (3,4)와 (4,3)이 7이고 앰버 강조가 그 네 칸에만 붙는다. k=2 행렬은 :101부터 :106까지의 최종 행렬과 같은 값이다. 캡션의 5+1+1=7도 :93과 맞는다. 본문은 무한대 기호를, SVG는 INF를 쓰지만 의사코드의 `INF`와 같은 표기라 혼선이 없다.
- recommendation: 현재 SVG를 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/all-pairs-shortest-path.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/all-pairs-shortest-path.md:2
- quote: title: "모든 쌍 최단 거리 — 다익스트라 N번과 플로이드·워셜"
- message: 검토 완료, 이슈 없음. 제목이 기준선(다익스트라 N번)과 본론(플로이드·워셜)을 함께 걸어 글의 두 축을 그대로 가리킨다. description은 문제 정의, 기준선, 경유 제한 전략, 점화식과 양방향 증명까지 실제 절 구성을 순서대로 담고 있으며 글에 없는 내용을 약속하지 않는다. 경로 복원을 다루지 않는다는 한정은 본문 :31에 있고 description이 최단 거리라고 못박아 어긋나지 않는다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/all-pairs-shortest-path.md:27

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/all-pairs-shortest-path.md:27
- quote: 입력은 무방향 가중 그래프이고 노드 수를 $N$, 간선 수를 $M$이라 한다. 모든 간선의 가중치는 $0$ 이상이라고 둔다.
- message: Notion 원문을 이 환경에서 확보하지 못했으므로 원문 직접 대조는 수행하지 못했다. 대신 설계서 `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md` §2의 provenance 분류와 본문을 대조했다. 원문에서 온다고 분류된 항목(문제 정의, 다익스트라 N번과 복잡도, 범위 논증, 경유 제한 전략, k=0·1·2 시뮬레이션과 되살아나는 노드 관찰, 점화식 유도, 3차원 의사코드)이 모두 본문에 있고, 승인된 추가(4노드 예시, SVG, 유일성 약화)와 검토 대상 추가(비음수 전제와 사이클 제거의 연결)도 설계서가 적은 범위 안에 있다. 설계서를 원문 자체로 간주하지 않았다. 본문에는 비공개 원천을 가리키는 서술이 없다.
- recommendation: 원문 확인이 필요하면 Notion 「All-Pairs Shortest Path」 페이지를 확보해 핵심 줄기, 누락, 자의적 추가를 다시 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/all-pairs-shortest-path.md:176

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/all-pairs-shortest-path.md:176
- quote: D^k[i][j] = \min\!\left(D^{k-1}[i][j],\ D^{k-1}[i][k] + D^{k-1}[k][j]\right)
- message: 독립 재검산 결과 일치한다. 층별 행렬을 간선 목록에서 다시 계산해 k=1은 (2,3)과 (3,2)가 6, k=2는 (1,4)와 (4,1)이 2, (3,4)와 (4,3)이 7, k=3과 k=4는 변화 없음을 확인했고 최종 행렬도 :101부터 :106까지와 같다. k=1에서 3→1→4가 12로 직행 10보다 길다는 :86, k=2 후보 경로 다섯 가지 열거(:88), 동점 변형에서 두 갈래가 모두 7이라는 :181도 재계산으로 맞는다. 양방향 증명은 두 경우가 배타적이고 남김이 없으며(:147), 후보 논증으로 얻은 두 부등식과 반대 방향 두 부등식이 등호를 닫는다. 정리 1이 비음수 전제를 쓰는 자리는 잘라낸 구간의 길이가 0 이상이라는 문장 하나로 명시되어 있다. 복잡도는 다익스트라 한 번 O((M+N)logN)에서 N번 O(N(M+N)logN), 연결 그래프에서 M ≥ N-1이므로 O(NM logN), 밀집과 희소 극단값 O(N³logN)과 O(N²logN), 플로이드·워셜 시간과 공간 O(N³)이 모두 유도대로다. 의사코드에 `INF` 덧셈 오버플로를 막을 조건이 없었으므로 :189에 `INF`의 여유 조건을 한 문장으로 덧붙였다. 논증에 남은 우려는 별도 🟡 항목으로 분리했다.
- recommendation: 현재 논증과 복잡도 설명을 유지한다. 남은 판정은 :143 항목을 본다.
- gate_effect: info

## 반영 결과

이번 리뷰에서 고친 것은 SVG 두 장과 본문 한 문장이다. 증명, 점화식, 복잡도 주장은 건드리지 않았다.

- 🟢 [L4] `problem.svg:48` 없는 기호를 설명하는 범례 → **반영 완료**. "? — 아직 채우지 않은 칸"을 "아직 채우지 않은 빈 칸"으로 바꿨다. 격자 안에 물음표가 그려진 적이 없다. 반영 후 재판정해 🟢으로 남긴다.
- 🟢 [L4] `recurrence.svg:41` 캡션이 본문보다 강한 주장 → **반영 완료**. "최단 경로에 같은 노드가 두 번 나오지 않으므로 k는 정확히 한 번 지난다"를 "고른 길에 같은 노드가 두 번 나오지 않으므로, k를 지난다면 정확히 한 번 지난다"로 바꿨다. 본문 :145는 정리 1로 그런 길을 고를 수 있다고만 말하고 모든 최단 경로가 단순하다고 주장하지 않으며, k를 지나는지는 :147에서 갈리는 두 경우 중 하나다. 캡션만 본문에 맞춘 것이다. 반영 후 재판정해 🟢으로 남긴다.
- 🟢 [L7] `:189` `INF` 덧셈 오버플로 → **반영 완료**. "`INF`는 둘을 더해도 자료형을 넘지 않을 만큼 큰 값으로 잡는다. 이어지지 않는 두 조각을 더하는 자리가 있어서, 여유가 없으면 합이 넘쳐 엉뚱한 최솟값이 나온다."를 덧붙였다. 의사코드와 점화식은 그대로 두고 전제만 밝혔다.
- 🟡 [L7] `:143` 정리 1과 최솟값 달성의 순환 → **미반영**. 정리의 진술 범위를 넓히는 수정이라 증명 구조에 손이 간다. 결론은 참이고 유한 그래프에서 반례가 생기지 않으므로 게시를 막지 않되, 사람 판정 대상으로 남긴다.

이 리포트는 같은 날짜의 이전 산출물을 대체한다. 그 파일은 SVG 6장이 만들어지기 전에 생성되어 에셋 없음 판정으로 채워져 있었고, 현재 상태와 맞지 않아 이어 쓰지 않고 다시 만들었다.

반영 후 검증: `python .claude/review_post.py`로 두 편 모두 발견 사항 없음, `npm run build` 성공, 빌드 산출물 본문에 raw 달러 기호 0개.
