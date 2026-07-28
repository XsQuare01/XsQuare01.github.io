## 결정적 검사: src/content/posts/matrix-multiplication.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/matrix-multiplication.md

🟡 권장 (3)

- severity: 🟡
  - source: L
  - rule_id: L3
  - location: src/content/posts/matrix-multiplication.md:222
  - quote: "나머지 행렬 덧셈·뺄셈은 $\Theta(N^2)$ 로, 점화식의 상수항에 흡수된다."
  - message: $\Theta(N^2)$는 입력 크기 $N$에 따라 변하므로 점화식의 상수항이 아니다. 여기서는 각 재귀 호출에서 드는 비재귀 작업 또는 결합 비용을 뜻한다. 현재 표현은 점화식 용어를 부정확하게 사용한다.
  - recommendation: `점화식의 비재귀 항` 또는 `각 호출의 결합 비용`으로 바꿔 $7T(N/2)$와 구분한다.
  - gate_effect: warn

- severity: 🟡
  - source: L
  - rule_id: L6
  - location: not-recorded
  - quote: not-recorded
  - message: 현재 세션에는 `notion-search`와 `notion-fetch`가 제공되지 않아 Notion 원문을 가져오지 못했다. 따라서 원문의 구조, 논증 흐름, 핵심 주장과 현재 글의 충실성은 완전히 검증할 수 없다.
  - recommendation: Notion 도구를 사용할 수 있는 세션에서 원문을 실제로 검색하고 가져온 뒤 현재 256줄 본문과 다시 대조한다.
  - gate_effect: warn

- severity: 🟡
  - source: L
  - rule_id: L7
  - location: src/content/posts/matrix-multiplication.md:35
  - quote: "덧셈도 그만큼 들지만, 앞으로 **곱셈 횟수만** 센다. 곱셈이 덧셈보다 비싸고, 재귀로 값이 커질 때 결국 곱셈 횟수가 복잡도를 지배하기 때문이다."
  - message: 표준 단위 비용 모델에서 나이브 곱의 스칼라 덧셈은 $N^2(N-1)$회로 곱셈과 같은 $\Theta(N^3)$이며, Strassen에서도 각 단계의 덧셈 비용은 전체 재귀 트리에서 $\Theta(N^{\log_2 7})$로 누적된다. 곱셈 수만 세어도 같은 점근 지수를 얻지만, 곱셈 횟수가 덧셈을 점근적으로 지배한다는 설명은 정확하지 않다. 이 문장을 제외하면 모든 블록은 $(N/2)\times(N/2)$로 차원이 맞고, 순서를 보존한 독립 전개에서 7개 곱의 네 재조합이 모두 표준 블록 곱과 일치했다. 준비 10회와 조립 8회로 덧셈과 뺄셈은 총 18회이며, $8T(N/2)+\Theta(N^2)=\Theta(N^3)$, $7T(N/2)+\Theta(N^2)=\Theta(N^{\log_2 7})$, $\log_2 7=2.8073549\ldots$도 검산했다. 전치, 역행렬, 저장 순서 변환은 사용하지 않아 관련 순서 함정은 없다.
  - recommendation: 곱셈이 덧셈보다 비싸서 지배한다고 설명하지 말고, 블록 곱의 재귀 호출 수가 점화식의 분기 수를 정하며 덧셈은 각 호출의 $\Theta(N^2)$ 비재귀 비용으로 함께 계산된다고 설명한다.
  - gate_effect: warn

🟢 참고 (4)

- severity: 🟢
  - source: L
  - rule_id: L1
  - location: src/content/posts/matrix-multiplication.md:11
  - quote: "두 행렬을 곱하는 데 정의대로면 $O(N^3)$이 든다. 분할 정복으로 이 벽을 넘을 수 있을까? 순진하게 나누면 실패한다."
  - message: 검토 완료, 이슈 없음. `docs/writing-rules.md`의 문두 접속어, 보조 용언, 불필요한 수식어와 복수 표지, 지시어, 중복 표현, 의존 명사와 관형격 조사 기준을 현재 256줄 전체에 문맥적으로 적용했다. 문두 접속어 남발, 경구식 마무리, 과한 비유나 강조는 없고, 줄표도 제목과 목록의 구획 또는 짧은 부연에 제한되어 기계적으로 고칠 수준이 아니다.
  - recommendation: 수정 불필요.
  - gate_effect: info

- severity: 🟢
  - source: L
  - rule_id: L2
  - location: src/content/posts/matrix-multiplication.md:27
  - quote: "나이브 곱은 왜 N³인가"
  - message: 검토 완료, 이슈 없음. 나이브 곱의 연산 수, 순진한 블록 분할의 한계, Strassen의 7개 곱, 재조합 증명, 점화식, 구현상 전환점과 후속 기록 순서가 자연스럽다. $N$이 2의 거듭제곱이라는 의사코드 전제와 $N=1$ 기저 조건도 명시되어 논리 흐름에 필요한 전제가 갖춰져 있다.
  - recommendation: 수정 불필요.
  - gate_effect: info

- severity: 🟢
  - source: L
  - rule_id: L4
  - location: src/content/posts/matrix-multiplication.md:66
  - quote: "![N×N 행렬을 2×2 블록으로 나누면, 블록을 원소처럼 다뤄 재귀적으로 곱할 수 있다. 하지만 블록 곱이 8번이라 T(N)=8T(N/2)로 여전히 Θ(N³)이다.](/images/matrix-multiplication/block-split.svg)"
  - message: 검토 완료, 이슈 없음. `block-split.svg`의 $A$, $B$, $C$ 배치, 네 $C_{ij}$ 식, $(N/2)\times(N/2)$ 크기, 블록 곱 8회와 $\Theta(N^3)$ 표기를 모든 레이블별로 확인했다. `seven-vs-eight.svg`의 왼쪽 8개와 오른쪽 7개 자식 노드, 각 $N/2$ 레이블, 두 점화식, $\log_2 8=3$, $\log_2 7=2.807\ldots$와 두 최종 복잡도도 본문 71행, 163행, 175행, 183행과 일치한다.
  - recommendation: 수정 불필요.
  - gate_effect: info

- severity: 🟢
  - source: L
  - rule_id: L5
  - location: src/content/posts/matrix-multiplication.md:4
  - quote: "N×N 행렬 곱은 정의대로면 O(N³)이다. 2×2 블록으로 나눠 재귀해도 곱셈이 8번이라 여전히 N³이다. Strassen은 곱셈을 7번으로 줄여 O(N^2.807)을 얻는다. 왜 지수가 바뀌는지, 7개의 곱이 답을 재구성하는지 검증한다."
  - message: 검토 완료, 이슈 없음. 제목은 순진한 분할 정복의 한계와 Strassen의 핵심 발상을 함께 나타내며, description은 나이브 복잡도, 8회와 7회 블록 곱, 지수 변화와 재조합 검증이라는 실제 범위를 정확히 대표한다.
  - recommendation: 수정 불필요.
  - gate_effect: info

요약: 🔴 0 · 🟡 3 · 🟢 4
