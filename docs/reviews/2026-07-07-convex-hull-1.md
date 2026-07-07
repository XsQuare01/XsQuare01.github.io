## 결정적 검사: src/content/posts/convex-hull-1.md
발견 사항 없음 ✅

## LLM 비평

- 🟡 [L1] src/content/posts/convex-hull-1.md:193
  - severity: 🟡
  - source: L
  - rule_id: L1
  - location: src/content/posts/convex-hull-1.md:193
  - quote: "브루트포스는 모든 선분이 껍질의 변인지 검사한다 — $O(N^2)$개의 선분 × $O(N)$ 판정 $= O(N^3)$."
  - message: 핵심 정리 항목에서 문장을 끊어 강조하는 줄표(—). closest-pair가 동일 패턴으로 L1 warn을 받았다.
  - recommendation: "…검사한다. 선분 $O(N^2)$개 × 판정 $O(N)$ = $O(N^3)$." 처럼 마침표로 분리한다.
  - gate_effect: warn

- 🟢 [L6] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L6
  - location: not-recorded
  - quote: not-recorded
  - message: 노션 "Convex hull 1"(36acb27e...)과 대조 완료. 정의·가정(x/y 서로 다름, 3점 일직선 없음)·O(N^3) 브루트포스·CCW 행렬식·Package Wrapping 모두 원본과 일치. Package Wrapping 복잡도는 노션 본문의 O(N^2 log N)이 아니라 같은 페이지의 Claude 정정 노트가 제시한 O(NH)(worst O(N^2))를 따랐다(정확). '고무줄' 도입 비유는 원본에 없으나 convex hull의 표준 직관이라 허위 첨가 아님.
  - recommendation: 원본 대비 누락·왜곡 없음. 조치 불필요.
  - gate_effect: info

- 🟢 [L7] src/content/posts/convex-hull-1.md
  - severity: 🟢
  - source: L
  - rule_id: L7
  - location: src/content/posts/convex-hull-1.md
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. CCW 전개식(x_A y_B + x_B y_C + x_C y_A - x_A y_C - x_B y_A - x_C y_B)이 코드의 외적식 (b.x-a.x)(c.y-a.y)-(b.y-a.y)(c.x-a.x)과 대수적으로 동일함 확인. 부호 규약(>0 반시계) 일관. 브루트포스 O(N^2)선분 × O(N)판정 = O(N^3), Package Wrapping 한 걸음 O(N) × H걸음 = O(NH)(worst O(N^2)) 유도 정확. gift wrapping 코드(ccw<0이면 후보 갱신)가 본문·SVG와 정합.
  - recommendation: 현재 구성 유지.
  - gate_effect: info

- 🟢 [L2] src/content/posts/convex-hull-1.md
  - severity: 🟢
  - source: L
  - rule_id: L2
  - location: src/content/posts/convex-hull-1.md
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 정의→가정→브루트포스→CCW→Package Wrapping으로 이어지는 흐름이 자연스럽고, 브루트포스의 '한쪽에 있는가'를 CCW로 자연스럽게 넘긴다.
  - recommendation: 현재 흐름 유지.
  - gate_effect: info

- 🟢 [L3] src/content/posts/convex-hull-1.md
  - severity: 🟢
  - source: L
  - rule_id: L3
  - location: src/content/posts/convex-hull-1.md
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 껍질·변·점·CCW·반시계/시계 용어를 일관되게 사용. 어체 ~다 평서체 통일.
  - recommendation: 현재 용어 유지.
  - gate_effect: info

- 🟢 [L4] public/images/convex-hull-1/
  - severity: 🟢
  - source: L
  - rule_id: L4
  - location: public/images/convex-hull-1/
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. SVG 7개(definition, convex-vs-not, brute-force, ccw-turn, ccw-area, wrapping-step, wrapping-full)의 캡션·레이블이 본문과 일치. 좌/우회전 방향과 부호 규약, 평행사변형 꼭짓점(B+AC), 한쪽/양쪽 판정, 감싸기 단계 번호가 본문 서술과 정합.
  - recommendation: 현재 SVG 유지.
  - gate_effect: info

- 🟢 [L5] src/content/posts/convex-hull-1.md:2
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: src/content/posts/convex-hull-1.md:2
  - quote: "볼록 껍질 ① — 정의, CCW, 그리고 Package Wrapping"
  - message: 검토 완료, 이슈 없음. 제목·description이 실제 내용(정의·CCW·Package Wrapping, O(N^3)→O(NH))을 잘 대표한다.
  - recommendation: 현재 제목·description 유지.
  - gate_effect: info

요약: 🔴 0 · 🟡 1 · 🟢 6
