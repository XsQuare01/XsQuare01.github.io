## 결정적 검사: src/content/posts/closest-pair-five-points.md

🔴 필수 (2)
- [D1] src/content/posts/closest-pair-five-points.md:35  깨진 굵게: '큰 쪽)**만' — 닫는 ** 앞 구두점 + 뒤 글자
- [D13] src/content/posts/closest-pair-five-points.md:43  SVG 세로 클리핑: 최상단 요소 y≈-45이 viewBox 시작 0보다 위에 있어 잘림 — /images/closest-pair-five-points/square-packing.svg

요약: 🔴 2 · 🟡 0 · 🟢 0

## LLM 비평

- 🟡 [L7] src/content/posts/closest-pair-five-points.md:55
  - severity: 🟡
  - source: L
  - rule_id: L7
  - location: src/content/posts/closest-pair-five-points.md:55
  - quote: "분할선은 셀 경계와 정확히 일치하므로, 어떤 셀도 분할선을 가로지르지 않는다. 즉 각 셀은 완전히 왼쪽 편이거나 완전히 오른쪽 편이다."
  - message: packing 증명은 분할선 위에 놓인 점이나 같은 x좌표 tie가 있을 때의 편 배정 규칙을 명시해야 완전히 닫힌다. 현재 문장은 기하적 셀 경계와 재귀의 왼쪽/오른쪽 편 배정이 항상 일치한다고 암묵적으로 가정한다.
  - recommendation: "분할선 위 점은 한쪽 반열린 영역에 배정한다" 같은 boundary/tie convention을 명시하거나, 일반 위치 가정(no point on divider)을 둔다.
  - gate_effect: warn

- 🟡 [L7] src/content/posts/closest-pair-five-points.md:108
  - severity: 🟡
  - source: L
  - rule_id: L7
  - location: src/content/posts/closest-pair-five-points.md:108
  - quote: "한 점당 비교 횟수는 $n$과 무관한 상수(≤ 7) → combine 선형 → 분할 정복 성립."
  - message: 1편의 구현에서는 Combine에 y정렬과 x재정렬이 포함되어 한 레벨 비용이 $O(n \log n)$이다. 여기서 선형이라고 할 수 있는 것은 7개 비교 스캔 부분이지, 1편 구현의 전체 Combine 단계가 아니다.
  - recommendation: "7개 비교 스캔은 선형"이라고 좁혀 쓰고, 전체 Combine 선형화는 y정렬을 유지하는 개선판에서 성립한다고 구분한다.
  - gate_effect: warn

- 🟢 [L1] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L1
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 현재 문체를 유지한다. 단, 결정적 검사 D1의 깨진 굵게는 별도로 수정 대상이다.
  - gate_effect: info

- 🟢 [L2] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L2
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 같은 편 거리 제약에서 후보 직사각형, 셀 분할, 다음 7개 결론으로 이어지는 설명 흐름을 유지한다.
  - gate_effect: info

- 🟢 [L3] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L3
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: $D$, $D_L$, $D_R$, $2D \times D$, $(D/2)$ 셀 용어를 현재처럼 일관되게 유지한다.
  - gate_effect: info

- 🟢 [L4] public/images/closest-pair-five-points/square-packing.svg:5
  - severity: 🟢
  - source: L
  - rule_id: L4
  - location: public/images/closest-pair-five-points/square-packing.svg:5
  - quote: "2D×D 직사각형을 (D/2) 셀로 나누기"
  - message: 검토 완료, 이슈 없음
  - recommendation: SVG의 4×2 셀, 셀 한 변 $D/2$, 최대 8점, 다음 7개 비교 설명은 본문과 일치한다. 다만 결정적 검사 D13의 세로 클리핑은 별도로 수정 대상이다.
  - gate_effect: info

- 🟢 [L5] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 제목과 description이 "다음 7개만 비교"의 기하적 근거를 잘 대표한다.
  - gate_effect: info

- 🟢 [L6] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L6
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 현재 세션에서 notion-search/notion-fetch 도구가 제공되지 않아 노션 원문 대조는 수행하지 못했다.
  - recommendation: 원문 대조가 필요하면 Notion MCP가 연결된 환경에서 재검토한다.
  - gate_effect: info

요약: 🔴 2 · 🟡 2 · 🟢 6

## 후속 처리

2026-08-05 재리뷰(`docs/reviews/2026-08-05-closest-pair-five-points.md`)에서 네 지적의 처리 상태를 확인했다. 이 리포트의 판정은 2026-06-30 시점 근거로 그대로 남긴다.

- 🔴 [D1] :35 깨진 굵게 → **반영 완료**. 결정적 검사 재실행 결과 "발견 사항 없음 ✅".
- 🔴 [D13] :43 SVG 세로 클리핑 → **반영 완료**. 같은 재실행에서 D13 미발생.
- 🟡 [L7] :108 combine 선형 과장 → **반영 완료**. "combine 선형" 단정을 걷어내고 "combine은 점 하나당 일정한 일만 하고"(현재 98행)로 범위를 좁혔다. 122행에 y 차이 재확인 구현도 점근이 같다는 단서를 달았다.
- 🟡 [L7] :55 경계·동률 배정 규약 누락 → **미반영**. 현재 68행이 같은 문장을 유지한다. 2026-08-05 리포트에 같은 지적을 다시 기록했다.

재리뷰가 새로 찾은 🟡 3건(밴드 폭 표기 L4, 원문 5의 근거 축소 L6, "5 부족" 미증명 L7)은 그 리포트에 있다.
