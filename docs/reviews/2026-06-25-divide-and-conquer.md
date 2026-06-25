## 결정적 검사: src/content/posts/divide-and-conquer.md
발견 사항 없음 ✅

## LLM 비평

### src/content/posts/divide-and-conquer.md

#### 🟡 [L1] src/content/posts/divide-and-conquer.md:227
- severity: 🟡
- source: L
- rule_id: L1
- location: src/content/posts/divide-and-conquer.md:227
- quote: `<p>분할 정복의 점화식을 한 방에 푸는 <a href="/blog/recursion#마스터-정리">마스터 정리</a>, 그리고 병합·퀵 정렬의 동작과 올바름 증명을 다룬 <a href="/blog/sort">정렬 알고리즘</a> 포스트와 함께 읽으면 좋다. 분할 정복이 "나눠서" 정복한다면, <a href="/blog/greedy">그리디</a>는 "한 걸음씩" 정복한다 — 같은 문제도 전략에 따라 전혀 다른 모습으로 풀린다.</p>`
- message: 이어지는 글의 마무리가 줄표와 대칭 은유로 경구처럼 닫혀 L1의 AI 신호 기준에 걸린다.
- recommendation: 줄표를 마침표나 접속사로 바꾸고, “분할 정복과 그리디는 서로 다른 전략이므로 함께 읽으면 좋다.”처럼 평이하게 정리한다.
- gate_effect: warn

#### 🟡 [L2] src/content/posts/divide-and-conquer.md:131
- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/divide-and-conquer.md:131
- quote: `이론적 $O$-표기는 비교·이동 횟수만 센다. 그런데 실제로 돌려 보면, $n$ 이 크고 메모리가 빠듯할 때 이 할당 자체가 발목을 잡는다. 운영체제 입장에서 큰 배열을 확보하는 일은 공짜가 아니며, $n$ 이 커질수록 메모리 할당에 드는 시간이 무시할 수 없을 만큼 늘어난다. 같은 $O(n \log n)$ 이라도 추가 배열을 쓰지 않는 정렬보다 느려질 수 있다.`
- message: 한 문장 묶음 안에 복잡도 모델, 메모리 할당 비용, 실측 성능 비교가 함께 들어가 전제가 흐려진다.
- recommendation: 시간 복잡도 분석과 공간 복잡도/할당 비용 설명을 분리하고, “공간 복잡도는 별도로 $O(n)$으로 본다”는 전제를 먼저 둔다.
- gate_effect: warn

#### 🟢 [L3] not-recorded
- severity: 🟢
- source: L
- rule_id: L3
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 용어·어체는 현재처럼 분할/나누기, 풀기, 합치기, 비교 기반 정렬, 결정 트리 표현을 일관되게 유지한다.
- gate_effect: info

#### 🟢 [L4] not-recorded
- severity: 🟢
- source: L
- rule_id: L4
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: `/images/divide-and-conquer/dnc-framework.svg`와 `/images/divide-and-conquer/decision-tree.svg`의 레이블·수치·캡션은 본문 설명과 일치한다.
- gate_effect: info

#### 🟢 [L5] not-recorded
- severity: 🟢
- source: L
- rule_id: L5
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: 제목과 description은 분할 정복, 병합 정렬 점화식, 힙 정렬 대안, 비교 정렬 하한이라는 실제 내용을 잘 대표한다.
- gate_effect: info

#### 🟢 [L6] not-recorded
- severity: 🟢
- source: L
- rule_id: L6
- location: not-recorded
- quote: not-recorded
- message: Notion 원본 대조는 수행하지 못했다. 현재 도구 목록에 `notion-search`/`notion-fetch`가 없어 원문을 가져올 수 없었다.
- recommendation: Notion 원문 접근이 가능한 환경에서 원본의 핵심 누락과 원본에 없는 추가 내용을 재대조한다.
- gate_effect: info

#### 🟡 [L7] src/content/posts/divide-and-conquer.md:55
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/divide-and-conquer.md:55
- quote: `int b[n];`
- message: 코드 블록이 `cpp`로 표시되어 있지만, `int b[n]`은 ISO C++ 표준의 가변 길이 배열이 아니다. 일부 컴파일러 확장에서는 동작하지만 표준 C++ 예시로는 부정확하다.
- recommendation: 의사코드임을 명시하거나 `std::vector<int> b(n);`처럼 표준 C++ 형태로 바꿔 독자가 그대로 컴파일해도 혼동이 없게 한다.
- gate_effect: warn

#### 🟡 [L7] src/content/posts/divide-and-conquer.md:131
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/divide-and-conquer.md:131
- quote: `이론적 $O$-표기는 비교·이동 횟수만 센다.`
- message: Big-O 표기 자체가 비교·이동 횟수만 세는 것은 아니다. 분석 모델에 따라 시간, 공간, 비교 횟수, 메모리 접근 등을 각각 Big-O로 표현할 수 있으므로 개념 설명이 과하게 좁다.
- recommendation: “이 절의 단순 시간 분석에서는 비교·이동 같은 추상 연산에 집중하지만, 구현에서는 추가 공간과 할당 비용도 따로 보아야 한다.”처럼 분석 모델을 한정한다.
- gate_effect: warn

#### 🟡 [L7] src/content/posts/divide-and-conquer.md:151
- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/divide-and-conquer.md:151
- quote: `힙 정렬은 힙을 만들 때 한 번, 허물 때 한 번, 사실상 배열을 두 차례 훑는다.`
- message: 힙 구성은 $O(n)$으로 볼 수 있지만, 힙을 허무는 과정은 단순한 한 번의 선형 스캔이 아니라 최댓값 추출과 down-heap을 $n$번 반복하는 $O(n \log n)$ 단계다. “두 차례 훑는다”는 표현은 독자가 힙 정렬의 비용 구조를 선형 두 패스로 오해하게 할 수 있다.
- recommendation: “힙 구성 뒤에는 최댓값 추출과 재정렬을 반복하므로 접근 패턴과 상수 계수가 불리할 수 있다.”처럼 비용 구조를 정확히 말한다.
- gate_effect: warn

요약: 🔴 0 · 🟡 5 · 🟢 4

---

## 반영 결과 (2026-06-25)

| 항목 | 판단 | 조치 |
|---|---|---|
| 🟡 L1 (line 227) | 반영 | 줄표·대칭 은유 마무리를 평이한 평서문으로 교체. 사용자 문체 피드백(경구식 마무리 지양)과 일치. |
| 🟡 L2 (line 131) | 반영 | 시간 분석 모델과 메모리/할당 비용 설명을 분리. (L7 line 131과 통합 수정) |
| 🟡 L7 (line 55) | 반영 | `int b[n]` → `std::vector<int> b(n);` + `b.data()`. sort.md가 이미 채택한 표준 C++ 형태와 일관성 확보. |
| 🟡 L7 (line 131) | 반영 | "O-표기는 비교·이동 횟수만 센다"는 과한 단정 → "앞 절의 시간 분석은 추상 연산 횟수에 집중"으로 분석 모델을 한정. |
| 🟡 L7 (line 151) | 반영 | "두 차례 훑는다"(선형 2-pass 오해) 제거 → 최댓값 추출+재정렬을 n번 반복하며 접근이 흩어져 캐시 지역성이 나쁘다는 정확한 비용 구조로 수정. |
| 🟢 L6 | 보류(무효) | "Notion 대조 미수행" 지적은 본 세션에서 notion-fetch로 원본("Divide and Conquer", 151cb27e…)을 이미 대조했으므로 해당 없음. 포스트 수정 불필요. |

`npm run build` 재검증 통과 (78 페이지). 반영 후 🔴 0 · 🟡 0 (해소 5 / 무효 1).
