schema_version: review-report/v2
target: floyd-warshall-memory
generated_at: 2026-08-12
strict: true
sources: src/content/posts/floyd-warshall-memory.md
summary: 🔴 0 · 🟡 1 · 🟢 7

## Findings

### 🟡 [L5] src/content/posts/floyd-warshall-memory.md:2

- severity: 🟡
- source: L
- rule_id: L5
- location: src/content/posts/floyd-warshall-memory.md:2
- quote: title: "플로이드·워셜의 메모리 줄이기 — 3층 배열을 한 층으로"
- message: 제목의 "3층"이 본문의 층 개념과 어긋난다. 이 글에서 층은 $k$ 축이고 배열 `D[n+1][n+1][n+1]`의 층은 $D^0$부터 $D^N$까지 $N+1$장이다. 3이라는 수가 나오는 자리는 차원 수뿐인데, 본편 :227이 이를 "3차원 배열"이라 부르고 이 글의 :16부터 :50까지는 같은 대상을 "층"으로 센다. 제목만 두 단위를 섞어 놓아, 처음 읽는 독자는 층이 원래 3장이었다가 1장이 된다고 읽게 된다. description 첫 문장이 "$N^3$칸을 쓴다"로 정확하므로 어긋남은 제목 한 줄에 한정된다. 직전 커밋 `0bf9983`이 "3차원 배열을 1차원으로"를 이 문구로 바꾸며 차원 대신 층 어휘를 택했는데, 수 3이 함께 옮겨 온 것으로 보인다.
- recommendation: 층 어휘를 유지하려면 수를 빼거나("층 배열을 한 장으로") 결과를 그대로 적는다("N³칸을 N²칸으로"). 뒤쪽은 description 첫 문장, 도입 :11, `layers.svg`의 세 단계 표기와 모두 같은 말이다. 제목은 직전 커밋이 의도적으로 고른 문구이므로 이번 리뷰에서 바꾸지 않았다. 사람 판정 대상이다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/floyd-warshall-memory.md:112

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/floyd-warshall-memory.md:112
- quote: ![k단계에서 k행과 k열은 값이 바뀌지 않으므로 덮어써도 안전하다.](/images/floyd-warshall-memory/overwrite-safe.svg)
- message: 반영 후 재판정. 줄표는 frontmatter 제목의 구조적 줄표 하나뿐이고 문장 내부에는 없다. 의존명사 '것' 10회, 접미사 '-들' 0회, 관형격 '의' 8회로 144행 분량 대비 남용이 아니다. 이 alt 문구만 "…바뀌지 않는다. 그래서 덮어써도 안전하다."로 문두 접속어를 썼는데, 인과가 이미 앞 절에 있어 접속어 없이 한 문장으로 붙였다. 절 제목 「그런데 왜 이걸 쓰는가」의 '그런데'는 그대로 두었다. 증명이 끝난 뒤 관점을 실행 시간으로 옮기는 전환 신호이고, 문두 접속어 최소화 규칙은 남발을 막는 것이지 전환에 꼭 필요한 하나까지 지우라는 뜻이 아니다.
- recommendation: 현재 문체를 유지한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/floyd-warshall-memory.md:81

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/floyd-warshall-memory.md:81
- quote: 위험이 남는 자리는 $D[i][k]$와 $D[k][j]$ 두 칸이다. 두 칸이 $k$ 단계에서 어떻게 변하는지만 확인하면 된다.
- message: 검토 완료, 이슈 없음. 2절이 위험을 막연히 말하지 않고 순서대로 좁힌다. 위험의 정체를 짚고(:75), 그 일이 벌어지는 정확한 시점을 $j$ 루프와 $i$ 루프에서 가리키고(:77), 안쪽 문장이 읽는 세 칸을 모두 세운 뒤 $D[i][j]$를 근거와 함께 후보에서 뺀다(:79). 남은 두 칸만 정리 1로 넘기므로 증명이 무엇을 갚아야 하는지가 미리 정해진다. 증명 뒤 :108이 그 빚을 명시적으로 갚고 :110이 얻은 것을 정리한다. 논리 도약이나 빠진 전제는 보이지 않는다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/floyd-warshall-memory.md:30

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/floyd-warshall-memory.md:30
- quote: 층을 두 장만 잡고 $k$의 홀짝에 따라 번갈아 쓰면 된다. 홀수 $k$에서는 0번 장을 읽어 1번 장에 쓰고, 짝수 $k$에서는 반대로 한다.
- message: 검토 완료, 이슈 없음. 층은 $k$ 축, 장은 층을 세는 단위, 칸은 배열 원소로 세 낱말의 역할이 끝까지 갈라져 있고 서로 자리를 바꾸지 않는다. 본편에서 물려받은 노드·간선·중간 노드·최단 거리 표기도 그대로이며 정점이나 엣지 같은 변형이 섞이지 않는다. $D^{k-1}[i][k]$ 수식 표기와 코드 `D[prev][i][k]`가 같은 대상을 가리키는 자리에서 층·행·열 순서가 어긋나지 않는다. 어체는 끝까지 ~다 평서체다.
- recommendation: 현재 용어 분담과 평서체를 유지한다.
- gate_effect: info

### 🟢 [L4] public/images/floyd-warshall-memory/layers.svg:7

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/floyd-warshall-memory/layers.svg:7
- quote: 0층 … N층
- message: 반영 후 재판정. 세 단계의 칸 수 표기 N³ 칸, 2N² 칸, N² 칸이 각각 도입 :11, :50, :110의 주장과 맞고, prev와 curr 두 장에 붙은 `D[k%2][i][j]`도 :41의 `prev`와 `curr` 계산과 같다. 하단 캡션 "k층은 k-1층만 참조한다"는 :16과 :26의 관찰 그대로다. 왼쪽 더미의 레이블이 원래 "1층 … N층"이라 기저 $D^0$이 빠져 있었는데, 본문 :38이 기저를 0층에 쓰므로 "0층 … N층"으로 고쳤다.
- recommendation: 조치 없음.
- gate_effect: info

### 🟢 [L4] public/images/floyd-warshall-memory/overwrite-safe.svg:81

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/floyd-warshall-memory/overwrite-safe.svg:81
- quote: D^k[i][k] = min(
- message: 검토 완료, 이슈 없음. 오른쪽 수식 상자가 :101의 식과 항까지 같고, 아래 결론 줄 D^k[i][k] = D^{k-1}[i][k]는 :104의 결론과 같다. 상자 머리말 "(k,k) 칸이 0이므로"는 :96이 두 방향 부등식으로 확정한 $D^{k-1}[k][k]=0$을 가리킨다. 왼쪽 격자는 k행 전체와 k열 전체를 앰버로 칠하고 교차점 (k,k)에만 0을 적어 정리 1의 진술 범위와 맞는다. 행과 열 머리글이 1, 2, 3, k, 5, 6이라 k가 네 번째 자리를 대신하지만, 도판이 특정 k를 고르지 않겠다는 표시이므로 본문과 어긋나지 않는다. 하단 캡션은 :108의 결론 문장과 같은 말이다.
- recommendation: 현재 SVG를 유지한다.
- gate_effect: info

### 🟢 [L6] src/content/posts/floyd-warshall-memory.md:94

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/floyd-warshall-memory.md:94
- quote: <span class="proof-lead">증명.</span> **정의로 보는 논증.** 두 값의 차이는 중간에 $k$를 쓸 수 있느냐뿐이다.
- message: Notion 원문을 이 환경에서 확보하지 못했으므로 원문 직접 대조는 수행하지 못했다. 대신 설계서 `docs/superpowers/specs/2026-08-11-all-pairs-shortest-path-design.md`와 대조했다. §2가 원문에서 오는 항목으로 적은 2층·1층 메모리 축소, $D^{k-1}[i][k] = D^k[i][k]$ 논증, 밀집 그래프에서 상수와 자료구조 때문에 실측이 빠르다는 관찰이 모두 본문에 있다. §6이 "원문이 서로 다른 두 각도를 제시하므로 둘 다 살린다"고 적은 대로 정의 논증과 점화식 대입 확인이 나란히 남아 있다. §8의 남은 불확실성대로 :124가 실측 우위를 단정하지 않고 이유를 밝히는 선에서 멈춘다. 설계서를 원문 자체로 간주하지 않았다. 본문에는 비공개 원천을 가리키는 서술이 없다.
- recommendation: 원문 확인이 필요하면 Notion 「All-Pairs Shortest Path」 페이지를 확보해 두 갈래 논증의 원래 서술과 대조한다.
- gate_effect: info

### 🟢 [L7] src/content/posts/floyd-warshall-memory.md:96

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/floyd-warshall-memory.md:96
- quote: 기저가 $D^0[k][k] = 0$이고, 허용 집합이 넓어져도 후보가 사라지지 않아 층이 올라갈수록 값이 늘지 않으므로($D^{k-1}[k][k] \le D^0[k][k]$) 이 값은 $0$ 이하다.
- message: 독립 재검증 결과 일치한다. 정리 1의 두 갈래가 각각 닫힌다. 정의 갈래는 $i \to k$에서 $k$가 끝점이므로 단순한 길에서 중간 노드가 될 수 없다는 논증이고, 대입 갈래는 $D^{k-1}[k][k]=0$을 위아래 부등식으로 먼저 확정한 뒤 $j=k$를 넣어 두 인자를 같게 만든다. 0 확정에 위 방향(층이 올라가도 값이 늘지 않음)과 아래 방향(비음수 가중치)을 모두 세운 점이 맞고, 순서도 대입보다 앞서 있어 이 글 안에서는 순환이 없다. $i=k$ 대입이 $k$행을 주는 것도 확인했다. 한 층 코드의 안전성은 $D[i][j]$가 같은 반복에서 한 번만 쓰이고 읽기가 그 쓰기보다 앞선다는 :79와, 나머지 두 칸이 어느 층이든 값이 같다는 정리 1로 세 칸이 모두 덮인다. 홀짝 인덱싱은 기저를 `D[0]`에 쓰고 $k=1$에서 prev=0, curr=1로 시작해 답이 `D[n % 2]`에 남는 것이 맞다. 칸 수 $2N^2$은 층당 $N^2$ 칸으로 세는 본문 기준의 값이며 1-based 패딩까지 세면 $2(N+1)^2$이나 본문이 패딩을 세는 자리는 없다. 복잡도는 밀집 그래프 $M \simeq N^2$에서 다익스트라 N번이 O(NM logN) = O(N³logN), 플로이드·워셜이 O(N³), 공간이 O(N³)에서 O(N²)로 내려가는 것이 모두 유도대로다. $N=1000$에서 $N^3$이 10억이고 $\log_2 N$이 10 안팎이라는 :11과 :120의 수치도 맞는다. 정의 갈래가 본편 정리 1에 기대므로, 본편 리포트의 🟡 항목이 판정되면 이 갈래도 함께 다시 본다.
- recommendation: 현재 논증과 복잡도 설명을 유지한다.
- gate_effect: info

## 반영 결과

이번 리뷰에서 고친 것은 SVG 한 장의 레이블과 본문의 이미지 alt 한 줄이다. 증명, 의사코드, 복잡도 주장은 건드리지 않았다.

- 🟢 [L4] `layers.svg:7` 기저 층이 빠진 레이블 → **반영 완료**. "1층 … N층"을 "0층 … N층"으로 바꿨다. 본문 :38이 기저를 `D[0]`에 쓰고 층을 $D^0$부터 세므로 1층에서 시작하는 표기는 기저를 도판 밖으로 밀어냈다. 반영 후 재판정해 🟢으로 남긴다.
- 🟢 [L1] `:112` 이미지 alt의 문두 접속어 → **반영 완료**. "값이 바뀌지 않는다. 그래서 덮어써도 안전하다."를 "값이 바뀌지 않으므로 덮어써도 안전하다."로 합쳤다. 인과는 그대로이고 접속어만 빠졌다. 반영 후 재판정해 🟢으로 남긴다.
- 🟡 [L5] `:2` 제목의 "3층" → **미반영**. 직전 커밋 `0bf9983`이 제목을 의도적으로 고른 결과이고, 대체 문구를 고르는 일은 사람 판단이 필요하다. 판정 대상으로 남긴다.

반영 후 검증: `python .claude/review_post.py`로 두 편 모두 발견 사항 없음, `npm run build` 성공, 빌드 산출물 본문에 raw 달러 기호 0개.
