## 결정적 검사: src/content/posts/selection-average.md
발견 사항 없음 ✅

## LLM 비평

- 🟡 [L1] src/content/posts/selection-average.md:80
  - severity: 🟡
  - source: L
  - rule_id: L1
  - location: src/content/posts/selection-average.md:80
  - quote: "이 절반 구간의 합은 등비수열처럼 줄어들어 $O(n)$에 수렴한다 — $\sum_{i=n/2}^{n-1} i \le \frac{3n^2}{8}$이 핵심 상한이다."
  - message: 핵심 정리 문장에서 줄표가 결론 연결부를 과하게 강조한다. 명령의 L1 기준상 AI식 마무리 신호로 보일 수 있다.
  - recommendation: 줄표 대신 마침표나 "이때" 같은 평이한 접속으로 나누는 편이 좋다.
  - gate_effect: warn

- 🟡 [L3] src/content/posts/selection-average.md:16
  - severity: 🟡
  - source: L
  - rule_id: L3
  - location: src/content/posts/selection-average.md:16
  - quote: "퀵 정렬는 왼쪽 $k-1$개와 오른쪽 $n-k$개 **양쪽 모두**를 재귀해야 한다."
  - message: 조사 오류가 있다. 문체와 어체의 신뢰도를 떨어뜨린다.
  - recommendation: "퀵 정렬은"으로 고친다.
  - gate_effect: warn

- 🔴 [L7] src/content/posts/selection-average.md:57
  - severity: 🔴
  - source: L
  - rule_id: L7
  - location: src/content/posts/selection-average.md:57
  - quote: "항의 개수는 $n - \lfloor n/2 \rfloor \le n/2$개이고"
  - message: 홀수 $n$에서 부등식이 거짓이다. 예를 들어 $n=5$이면 항의 개수는 $5-2=3$이고 $n/2=2.5$보다 크다. 이어지는 $\frac{3n^2}{8}$ 상계와 $E(n) \le 4n$ 귀납 단계가 모든 $n$에 대해 닫힌다는 증명이 성립하지 않는다.
  - recommendation: $n$을 짝수로 제한한 뒤 일반 $n$은 별도 처리하거나, 항의 개수를 $\lceil n/2 \rceil$로 두고 상수 여유를 다시 잡아 증명을 완결한다.
  - gate_effect: fail

- 🟢 [L2] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L2
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 현재 흐름을 유지한다.
  - gate_effect: info

- 🟢 [L4] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L4
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 이 포스트는 SVG를 참조하지 않는다.
  - gate_effect: info

- 🟢 [L5] not-recorded
  - severity: 🟢
  - source: L
  - rule_id: L5
  - location: not-recorded
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음
  - recommendation: 제목과 description이 quickselect 평균 시간 분석을 잘 대표한다.
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

요약: 🔴 1 · 🟡 2 · 🟢 4
