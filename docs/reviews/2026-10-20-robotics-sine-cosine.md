schema_version: review-report/v2
target: robotics-sine-cosine
generated_at: 2026-10-20
strict: true
sources: src/content/posts/robotics-sine-cosine.md
summary: 🔴 0 · 🟡 3 · 🟢 5

## Findings

### 🟡 [L2] src/content/posts/robotics-sine-cosine.md:43

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-sine-cosine.md:43
- quote: 그렇게 생긴 직각삼각형은 빗변이 1이고 한 각이 $30^\circ$이므로, 막대를 $30^\circ$ 돌렸을 때 생기는 직각삼각형과 모양과 크기가 같다.
- message: 정삼각형을 반으로 나누어 sin 30°와 cos 30°를 구하는 논증은 옳다. 다만 “고교 수학을 잊은 독자”는 정삼각형의 수선, 꼭짓점의 30°, 길이 1/2인 맞은편 변을 머릿속에 그린 뒤 앞의 막대 삼각형에 대응시켜야 한다. 현재 unit-circle.svg에는 이 보조 삼각형이 없어, 첫 정확한 삼각함수 값을 얻는 과정에 시각적 설명이 부족하다.
- recommendation: 한 변이 1인 정삼각형을 수선으로 나눈 작은 SVG를 보태고, 30°의 맞은편 변 1/2와 이웃한 직각변 √3/2를 표시한다. 옆에 같은 삼각형을 막대 그림의 방향으로 배치하면 두 정의와 예시를 바로 연결할 수 있다. 새 이론이나 긴 설명을 추가할 필요는 없다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-sine-cosine.md:41

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-sine-cosine.md:41
- quote: 직각삼각형의 한 예각 $\theta$에 대해 코사인은 $\dfrac{\text{밑변}}{\text{빗변}}$, 사인은 $\dfrac{\text{높이}}{\text{빗변}}$다.
- message: 현재 막대 그림처럼 θ가 가로 변과 빗변 사이에 있을 때는 맞지만, 임의의 예각에 대한 정의로는 θ의 위치 조건이 빠졌다. 같은 삼각형에서 다른 예각을 θ로 고르면 밑변과 높이의 역할이 바뀐다. 바로 다음 문단에서는 정삼각형 꼭짓점의 30°를 사용하므로, 입문자가 고정된 밑변·높이 이름으로 외우면 두 설명을 연결하기 어렵다.
- recommendation: 일반 정의를 “코사인은 θ에 이웃한 직각변의 길이/빗변의 길이, 사인은 θ의 맞은편 변의 길이/빗변의 길이”로 쓰고, 이어서 “지금 그림에서는 각각 가로 성분과 세로 성분이다”라고 연결한다. 현재 예제의 계산은 그대로 유지한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-sine-cosine.md:126

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-sine-cosine.md:126
- quote: 인자는 세로 좌표 $y$를 먼저 받고, $-180^\circ$보다 크고 $180^\circ$ 이하인 범위에서 각도를 돌려준다.
- message: (-180°, 180°]에서 대표 각도를 고르는 수학적 약속은 타당하다. 다만 현재 문장은 이를 atan2 자체의 보편적인 반환 규약처럼 읽히게 한다. 이 실험에서 사용하는 JavaScript Math.atan2는 라디안의 [-π, π]를 반환하며 Math.atan2(-0, -1)은 -π다. 모델은 도로 변환하고 wrap으로 -180°를 180°로 바꾸므로 실험 계산은 맞지만, 본문과 모델 첫 줄의 주석이 API의 결과와 글에서 선택한 표기를 구분하지 않는다. 또한 같은 방향의 θ와 θ+360°k 중 하나를 택한다는 설명을 보태면 “끝점에서 각도를 되찾는다”가 회전 횟수까지 복원한다는 오해를 막을 수 있다.
- recommendation: 본문에는 “같은 방향은 한 바퀴씩 더하거나 뺀 여러 각도로 나타낼 수 있다. 여기서는 (-180°, 180°] 안의 대표 각도를 쓴다”를 먼저 밝힌다. 구현 설명이나 짧은 주석에서 “Math.atan2의 라디안 결과를 도로 바꾸고 -180°를 180°로 통일한다”를 구분한다. src/labs/rod-angle-model.mjs:1의 “the range atan2 returns”도 실험이 사용하는 범위라는 표현으로 바꾸기를 권한다. 부호 있는 0의 상세 설명을 입문 본문에 길게 추가할 필요는 없다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-sine-cosine.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-sine-cosine.md:11
- quote: 각도와 길이를 좌표로 바꾸는 계산이 이 글의 질문이다.
- message: 검토 완료, 이슈 없음. 도입의 질문이 구체적이고, 평서체와 문장 길이가 대체로 안정적이다. 본문을 다시 구성해야 할 문체 문제는 발견하지 않았다.
- recommendation: 현재 질문 중심의 도입과 어체를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-sine-cosine.md:37

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-sine-cosine.md:37
- quote: 막대의 가로·세로 성분은 끝점의 두 좌표와 같은 숫자다.
- message: 검토 완료, 이슈 없음. 점의 좌표와 위치벡터의 성분을 구분하고, θ는 각도, L은 길이로 일관되게 사용한다. 단위원·라디안·사분면·탄젠트를 사용하는 자리에서 뜻을 설명한다. 삼각비의 변 이름에 필요한 조건은 L7의 41행 지적에 기록했다.
- recommendation: 좌표와 성분을 구분하는 현재 설명을 유지한다.
- gate_effect: info

### 🟢 [L4] src/content/posts/robotics-sine-cosine.md:39

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/robotics-sine-cosine.md:39
- quote: 노란 선이 가로 성분 cos θ, 초록 점선이 세로 성분 sin θ다.
- message: 검토 완료, 이슈 없음. 정적 SVG 네 장과 실험 SVG의 좌표·각도 호·부호·예시 수치를 본문 및 모델과 대조했다. 단위원의 (√3/2, 1/2), 두 배 확대, 120°의 (-1, √3), 반대 방향의 (3, 4)/(-3, -4)가 일치한다. 브라우저에서 도판을 렌더링하고 실험의 -90°·0°·90°·120°·180° 읽기 값과 초기화도 확인했다. atan2의 API 반환 규약과 실험의 정규화 구분은 L7의 126행 지적에 기록했다.
- recommendation: 현재 도판의 좌표와 부호 관계를 유지한다. 테스트의 3,960개 상태 확인은 모델의 경계 상자 계산이며 모든 상태를 브라우저에서 시각 검수한 것은 아니다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-sine-cosine.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-sine-cosine.md:2
- quote: 사인과 코사인 — 각도와 길이로 막대 끝을 찾기
- message: 검토 완료, 이슈 없음. 제목과 description이 단위원의 정의, 길이 L로의 확장, 끝점에서 방향을 구하는 역문제를 대표한다. 본문 범위를 넘어선 약속은 없다.
- recommendation: 제목을 유지한다. 대표 각도에 관한 L7 권고를 반영할 때 description의 “각도를 되찾을 때”도 “방향을 나타내는 각도를 구할 때”로 맞추면 더 분명하다.
- gate_effect: info

### 🟢 [L6] docs/superpowers/specs/2026-10-19-robotics-sine-cosine-design.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: docs/superpowers/specs/2026-10-19-robotics-sine-cosine-design.md:1
- quote: 로보틱스 기초 2 — 사인과 코사인으로 막대 끝을 찾기
- message: approved extension — 저장소의 포스트별 스펙을 실제로 읽고 본문의 목적·순서·예시·증명 의무와 대조했다. 30°·120°·-30° 및 (3, 4)/(-3, -4)는 추가 예시로 provenance에 밝혀져 있으며, 입문 독자를 위한 기초 설명이라는 의도와 부합한다. 공개 근거인 OpenStax 7.1·7.2·7.3도 확인했다. 이번 판정은 승인된 스펙과 공개 문헌에 대한 대조이며, 스펙에 적힌 비공개 PPT의 모든 원문 페이지를 재검증했다는 뜻은 아니다.
- recommendation: 현재 provenance 구분을 유지한다. 선형대수·미분방정식 PDF를 이 편에 사용하지 않았다는 스펙의 설명을 실제 활용으로 바꾸어 보고하지 않는다.
- gate_effect: info

## 후속 처리

- 검토 대상: [PR #245](https://github.com/XsQuare01/XsQuare01.github.io/pull/245), head `6c1c9c1695a1013860e84a09944f07d98c2d3585`. PR의 base는 `fix/robotics-points-vectors-review`이며 main이 아니다.
- 종합 판정: 핵심 공식과 논증, 수치 예시는 옳다. “질문 → 단위원의 정의 → 양수 L에 의한 확대 → 사분면 → 조작 실험 → 역문제”의 흐름도 자연스럽다. 필수 수정으로 분류할 핵심 수학 오류는 발견하지 않았고, 국소적인 정확성·명료성 보완 3건을 권고한다.
- 기본 등식 cos²θ + sin²θ = 1은 단위원과 거리 공식에서 나오며, L > 0에서 같은 반직선과 거리 L로 끝점의 유일성을 보이는 논증은 모든 각도에 적용된다. 원점에서 방향이 정해지지 않는 퇴화 사례도 본문에 있다.
- 실행한 검사: `npm run test:js` 50/50 통과. `.claude/review_post.py`의 결정적 검사에서 발견 사항 0건. Node에서 atan2(4, 3), atan2(-4, -3), atan2(-0, -1)의 값을 독립 재계산했고, 마지막 입력을 실험 모델에 넣으면 180°로 정규화됨을 확인했다.
- 브라우저 확인: PR head의 별도 worktree를 4325 포트로 실행하여 Chromium에서 확인했다. 정적 SVG 네 장을 로드한 뒤 렌더를 확인했다. 실험은 키보드 입력으로 -90°·0°·90°·120°·180°를 검사했고, 각각 끝점 (0, -2)·(2, 0)·(0, 2)·(-1, 1.73)·(-2, 0)이 표시됐다. 초기화는 30°로 돌아왔다. 데스크톱과 390px 폭의 초기 화면을 확인했으며, 390px 화면에서 문서 가로 넘침과 실행 중 JavaScript 예외는 없었다. 실기기 터치·인쇄·모든 상태의 시각 검수는 이번 확인 범위가 아니다.
- 수학적 근거: [OpenStax 7.1 Angles](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-1-angles)의 같은 방향을 나타내는 각도, [OpenStax 7.2 Right Triangle Trigonometry](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry)의 기준 각도에 대한 이웃변·맞은편 변, [OpenStax 7.3 Unit Circle](https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-3-unit-circle)의 좌표 정의를 대조했다.
- 구현 경계의 근거: [ECMAScript Math.atan2](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-math.atan2)는 라디안의 [-π, π] 반환과 음의 0에 대한 -π 반환을 명시한다. 수학적 대표 각도의 선택과 언어 API의 규약을 구분하는 근거다.
- 이번 작업에서는 리뷰 파일만 추가했다. 본문·도판·구현을 수정하거나 PR에 댓글을 게시하지 않았다.

작성자 반영 (2026-10-20):

- 🟡 [L7] 41행: 직각삼각형 정의를 "θ에 이웃한 직각변/빗변", "θ의 맞은편 변/빗변"으로 바꿨다. "어느 예각을 θ로 고르느냐에 따라 두 변의 역할이 바뀐다"를 더하고, 막대 그림에서는 각각 가로·세로 성분이라고 이었다. 30° 문단도 "30°에 이웃한 직각변"으로 맞추고 cos 30° = √3/2를 명시했다.
- 🟡 [L2] 43행: 도판 `thirty-degrees.svg`를 더했다. 세 칸(정삼각형 → 수선으로 자른 반쪽 → 막대 방향)으로 되어 있고, 이웃한 변은 노랑, 맞은편 변은 초록, 빗변은 파랑으로 둘째·셋째 칸을 잇는다. 기존 도판의 색 역할과 같다.
- 🟡 [L7] 126행:
  - 본문에 "30°, 390°, −330°는 같은 끝점을 준다. 이 글은 (−180°, 180°] 안의 하나를 대표로 쓴다"를 먼저 두고, atan2를 "이 대표 각도를 구하는 함수"로 바꿨다.
  - "프로그래밍 언어의 atan2는 라디안으로 돌려주고 경계에서 −π가 나오기도 하며, 실험은 도로 바꾼 뒤 −180°를 180°로 맞춘다"를 더했다. 핵심 정리 callout에도 대표 각도를 적었다.
  - 모델 첫 줄 주석을 "실험과 글이 쓰는 대표 범위, Math.atan2는 [−π, π]"로 고쳤다. `Math.atan2(-0, -2)`가 −π이고 실험이 180°로 맞춘다는 것을 테스트에 넣었다.
- 스펙: 정의 표현, 대표 각도와 API 규약의 구분, 새 도판 행을 기록했다.
- 재검증: `npm run test:js` 50/50, 결정적 검사 0건, 빌드(격리 복사본) 150쪽·본문 검사 통과, 이 글의 KaTeX 오류 0건, 빌드 결과에 새 도판과 바뀐 문장이 들어간 것을 확인했다.
- 미확인: 새 도판 `thirty-degrees.svg`의 브라우저 렌더는 작성자가 보지 못했다.
