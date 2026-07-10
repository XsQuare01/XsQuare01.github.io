## 결정적 검사: src/content/posts/convex-hull-bst-tangent.md

🟡 권장 (1)
- [D2] src/content/posts/convex-hull-bst-tangent.md:10, src/content/posts/convex-hull-bst-tangent.md:27, src/content/posts/convex-hull-bst-tangent.md:41  줄표(—) 13회 — 임계치(9) 초과. AI 문체 신호 샘플 위치: src/content/posts/convex-hull-bst-tangent.md:10, src/content/posts/convex-hull-bst-tangent.md:27, src/content/posts/convex-hull-bst-tangent.md:41

요약: 🔴 0 · 🟡 1 · 🟢 0

## LLM 비평: src/content/posts/convex-hull-bst-tangent.md

🟡 권장 (1)
- severity: 🟡 · source: L · rule_id: L1 · location: src/content/posts/convex-hull-bst-tangent.md:20 · gate_effect: warn
  - quote: `하나는 **사슬 이웃** — x가 바로 작은 꼭짓점(prev)과 바로 큰 꼭짓점(next) — 이고, 다른 하나는 **트리 자식** — 작은 x 쪽(왼쪽)과 큰 x 쪽(오른쪽) — 이다.`
  - message: 문장 내부 줄표가 임계치(9)를 넘겨 13회. 특히 "다시, 무대" 절의 이 한 문장에 삽입구 줄표가 네 개 몰려 있고, 도입 blockquote에도 삽입구 줄표 한 쌍이 있다. 섹션 제목·이미지 alt·이어지는 글의 구조적 줄표는 시리즈와 일관되어 유지 가능.
  - recommendation: "다시, 무대"의 삽입구를 "즉/곧"으로 풀어 두 문장으로 나누고, blockquote 삽입구도 "즉"으로 풀어 임계치 이하로 낮춘다.

🟢 참고 (9)
- severity: 🟢 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-bst-tangent.md:33 · gate_effect: info
  - quote: `꼭짓점 $t$의 두 이웃(prev, next)이 **모두 직선 $p$–$t$ 아래**에 있으면, $t$가 접점이다.`
  - message: 접점의 국소 조건이 옳다. 볼록 다각형에서 외부 점 p의 접점은 두 인접 변이 직선 p–t의 같은 쪽(껍질 내부 쪽)에 있는 꼭짓점이며, 이는 전역 조건("사슬 전체가 직선 아래")과 동치다. figs의 점 배치(1~7, p=650,200)로 검증: 접점은 4번(직선 p–4 아래에 나머지 전부, 좌표로 확인).
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-bst-tangent.md:47 · gate_effect: info
  - quote: `오른쪽 이웃이 위로 삐져나옴 → 접점은 더 오른쪽(큰 x). 트리에서 **오른쪽 자식**으로.`
  - message: 방향 판정의 단조성·정확성 검증 완료. 7개 꼭짓점 전부에 대입 시 1·2·3→오른쪽, 4→종료(접점), 5·6·7→왼쪽으로 일관되게 나오며(각 꼭짓점에서 이웃의 위/아래를 직선 p–v로 계산), 접점 4에서 정확히 멈춘다. 트리 자식 하강이 x-절반을 소거하므로 O(log N). 알고리즘·복잡도 정확.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-bst-tangent.md:53 · gate_effect: info
  - quote: `위로 볼록한 사슬에서, 한 후보의 두 이웃이 동시에 직선 $p$–$v$ 위로 솟는 일은 없다.`
  - message: 세 갈래 판정의 MECE 근거가 옳다. 두 이웃이 동시에 직선 위면 v가 반사(reflex)/골짜기 꼭짓점이어야 하는데 볼록 껍질에는 그런 꼭짓점이 없다. 따라서 오른쪽/왼쪽/종료가 겹치지 않고 항상 하나로 정해진다.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L6 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 소스 대조 완료(노션 `Convex hull 2` 노트 O(N log N) 접선 절, 대화 내 fetch본). 노션의 "뚫고 들어감/나감 → 탐색 방향", CCW 판정, BST로 O(log N)이 모두 반영됨. 노션은 right hull+y좌표로 서술했으나 본 글은 3편과 정합을 위해 upper hull+x좌표 사슬로 번역(의도된 재프레이밍). "두 이웃 동시 위로 불가" MECE 근거는 rigor를 위한 추가로 타당.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L4 · location: src/content/posts/convex-hull-bst-tangent.md:78 · gate_effect: info
  - quote: `![왜 이진 탐색인가 — 후보는 트리의 한 노드이고, 오른쪽으로 판정되면...](/images/convex-hull-bst-tangent/halving.svg)`
  - message: SVG 3장 검토 완료. tangent-condition(접점 4가 초록선 위, pt5가 빨강선 위로 삐짐 — 좌표로 확인), direction-cases(후보 3→오른쪽, 6→왼쪽) 모두 본문과 일치. halving은 접점=루트=4인 실제 예와 달리 "오른쪽으로"를 그리지만, 부제·화살표에 "예:"로 명시한 일반 메커니즘 예시라 오해 소지 낮음.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L1 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 줄표 외 항목(경구식 마무리, 과한 비유, 대칭 반복) 검토 완료, 이슈 없음. ~다 평서체 일관.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L2 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 무대 재설정 → 접점 조건 → 방향 판정 → 이진 탐색 → 코드로 이어지는 흐름이 자연스럽고, 3편이 미룬 지점을 정확히 이어받는다.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L3 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 용어(사슬/이웃/접선/접점/prev·next/왼쪽·오른쪽 자식/CCW) 일관, 3편 용어와도 정합.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L5 · location: src/content/posts/convex-hull-bst-tangent.md:2 · gate_effect: info
  - quote: `title: "추가 설명 — 균형 트리에서 접선을 O(log N)에 찾기"`
  - message: 검토 완료, 이슈 없음. 제목·description이 실제 내용(접선 이진 탐색 방향 판정)을 대표하고, 기존 "추가 설명 —" 관례와 일치.
  - recommendation: 조치 불요.

요약(전체): 🔴 0 · 🟡 2 · 🟢 9

## 반영 결과 (2026-07-10)

- [D2/L1] 도입 blockquote와 "다시, 무대" 절의 삽입구 줄표를 "즉/곧"으로 풀어 문장을 나눔. 재검사 "발견 사항 없음 ✅".
- L6(소스 충실성)·L7(접점 국소 조건, 방향 판정 단조성·MECE, O(log N))은 검증 통과로 조치 없음.
- 반영 후 `npm run build` 통과 (105 pages).
