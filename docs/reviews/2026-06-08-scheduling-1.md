## 결정적 검사: src/content/posts/scheduling-1.md

🟡 권장 (1)
- [D2] src/content/posts/scheduling-1.md:15, src/content/posts/scheduling-1.md:16, src/content/posts/scheduling-1.md:17  줄표(—) 15회 — 임계치(11) 초과. AI 문체 신호 샘플 위치: src/content/posts/scheduling-1.md:15, src/content/posts/scheduling-1.md:16, src/content/posts/scheduling-1.md:17

요약: 🔴 0 · 🟡 1 · 🟢 0

## LLM 비평: src/content/posts/scheduling-1.md

🔴 필수 (1)

- [L7] src/content/posts/scheduling-1.md:97
  - severity: 🔴
  - source: L
  - rule_id: L7
  - location: src/content/posts/scheduling-1.md:97
  - quote: "2-a. $S$ 의 $t$ 가 비어 있다면 — $S$ 에 $J_{i+1}$ 을 그냥 추가하면 이익이 $P_{i+1} > 0$ 만큼 늘어난다."
  - message: 증명의 경우 분류가 겹친다. $S$가 이미 $J_{i+1}$을 더 이른 슬롯 $t' < t$에 가지고 있으면서 슬롯 $t$가 비어 있는 경우에는, $S$에 $J_{i+1}$을 "그냥 추가"할 수 없고 모순도 아니다. 현재 2-a와 2-c가 서로 배타적이지 않아 Step 증명이 MECE하지 않다.
  - recommendation: 먼저 `$S$가 $J_{i+1}$을 이미 포함하는가`를 분기하고, 포함한다면 $t'=t$, $t'>t$ 불가, $t'<t$에서는 $J_{i+1}$을 $t$로 옮기거나 필요한 경우 자리 교환한다고 정리하라. 포함하지 않는 경우에만 `$t$가 비어 있으면 추가`, `$t$에 다른 일 $J_x$가 있으면 교환`으로 나누면 논증이 닫힌다.
  - gate_effect: fail

🟡 권장 (3)

- [L1] src/content/posts/scheduling-1.md:15
  - severity: 🟡
  - source: L
  - rule_id: L1
  - location: src/content/posts/scheduling-1.md:15
  - quote: "데드라인 스케줄링 문제의 정의 — 마감 기한과 이익을 가진 일들의 배치"
  - message: 결정적 검사 D2와 같은 문제다. 목차·정의·성능 제목 등에서 줄표(—)가 반복되어 글의 리듬이 다소 기계적으로 보인다.
  - recommendation: 목차 항목은 `:`, 괄호, 짧은 문장 분리로 바꾸고, 제목의 줄표는 꼭 필요한 곳에만 남겨라. 예: `데드라인 스케줄링 문제의 정의: 마감 기한과 이익을 가진 일들의 배치`.
  - gate_effect: warn

- [L2] src/content/posts/scheduling-1.md:119
  - severity: 🟡
  - source: L
  - rule_id: L2
  - location: src/content/posts/scheduling-1.md:119
  - quote: "각 일마다 마감 $D_i$ 에서 0 방향으로 한 칸씩 내려가며 빈 슬롯을 찾는다."
  - message: 앞에서는 시간 슬롯을 1, 2, 3, …로 정의했는데, 구현 설명에서는 `0 방향`이라고 해 슬롯 0까지 검사하는 것처럼 읽힐 수 있다.
  - recommendation: `마감 $D_i$에서 1까지 한 칸씩 내려가며` 또는 `마감 $D_i$ 이하의 슬롯을 큰 번호부터 작은 번호 순으로`처럼 실제 슬롯 범위를 명확히 써라.
  - gate_effect: warn

- [L3] src/content/posts/scheduling-1.md:59
  - severity: 🟡
  - source: L
  - rule_id: L3
  - location: src/content/posts/scheduling-1.md:59
  - quote: "마감 기한에 최대한 가까운 빈 자리"
  - message: 같은 개념이 `마감 기한`과 `마감기한`으로 섞여 나온다. 예를 들어 본문 line 59·140과 SVG footnote의 `마감기한` 표기가 line 30의 `마감 기한(deadline)`과 다르다.
  - recommendation: 본문과 SVG 모두 `마감 기한`으로 통일하라.
  - gate_effect: warn

🟢 참고 / coverage (3)

- [L4] src/content/posts/scheduling-1.md:61
  - severity: 🟢
  - source: L
  - rule_id: L4
  - location: src/content/posts/scheduling-1.md:61
  - quote: "(1,3)→슬롯1, (2,2)→슬롯2, (1,1)은 버려짐"
  - message: 검토 완료, 이슈 없음. SVG `public/images/scheduling/timeline.svg`는 예시 `{(2,2),(1,3),(1,1)}`, 슬롯 1의 `(1,3)`, 슬롯 2의 `(2,2)`, 버려진 `(1,1)`, 총 이익 5를 본문과 일치하게 표시한다.
  - recommendation: 유지.
  - gate_effect: info

- [L5] src/content/posts/scheduling-1.md:2
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: src/content/posts/scheduling-1.md:2
  - quote: "title: \"데드라인 스케줄링 — 이익을 최대로 만드는 greedy 배치\""
  - message: 검토 완료, 이슈 없음. 제목과 description이 문제 정의, greedy 전략, 교환 논증, $O(N \log N)$ 구현까지 실제 본문 범위를 잘 대표한다.
  - recommendation: 유지.
  - gate_effect: info

- [L6] docs/superpowers/specs/2026-06-08-scheduling-1-post-design.md:4
  - severity: 🟢
  - source: L
  - rule_id: L6
  - location: docs/superpowers/specs/2026-06-08-scheduling-1-post-design.md:4
  - quote: "출처: Notion \"Scheduling Problem 1\" (페이지 ID `150cb27e-4930-80f1-8d86-e137f55056e0`, 부모: \"알고리즘 수업 정리\")"
  - message: 검토 완료, 직접 Notion 원문은 현재 도구에서 가져오지 못했다. 대신 Notion 기반 설계서와 구현 계획을 대조했을 때, 포스트는 계획된 구조(문제 정의 → greedy 전략 → 정확성 증명 → 성능)와 예시/SVG 요구사항을 대체로 충실히 따른다.
  - recommendation: Notion 원문과의 1:1 대조가 필요하면 Notion fetch가 가능한 환경에서 한 번 더 확인하라. 현재 리뷰의 소스 충실성 평가는 로컬 설계서·계획 대비로 제한된다.
  - gate_effect: info

요약: 🔴 1 · 🟡 4 · 🟢 3
