## 결정적 검사: src/content/posts/selection.md
발견 사항 없음 ✅

## LLM 비평

- 🟢 [L1] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L1
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 현재 문체를 유지한다.
  - gate_effect: info

- 🟢 [L2] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L2
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 선택 문제 정의에서 quickselect, approximate median, median of medians로 이어지는 현재 흐름을 유지한다.
  - gate_effect: info

- 🟢 [L3] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L3
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: pivot, partition, approximate median, median of medians 표기를 현재처럼 일관되게 유지한다.
  - gate_effect: info

- 🟢 [L4] public/images/selection/quickselect-one-side.svg:5
  - severity: 🟢
  - source: L
  - rule_id: L4
  - location: public/images/selection/quickselect-one-side.svg:5
  - quote: "Quickselect — partition 후 한쪽만 재귀"
  - message: 검토 완료, 이슈 없음
  - recommendation: quickselect SVG의 pivot 등수, 왼쪽/오른쪽 재귀 조건이 본문 설명과 일치한다. approximate median 및 median-of-medians SVG도 본문의 30%/70%, 5개 그룹, 0.2+0.7=0.9 설명과 일치한다.
  - gate_effect: info

- 🟢 [L5] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 제목과 description이 선택 문제와 median of medians의 최악 O(n) 보장을 잘 대표한다.
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

- 🟢 [L7] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L7
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: quickselect 최선/최악, approximate median의 0.7n 상한, median of medians 점화식 $S(n)=2n+S(0.2n)+S(0.7n)$ 설명을 유지한다.
  - gate_effect: info

요약: 🔴 0 · 🟡 0 · 🟢 7
