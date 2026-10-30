schema_version: review-report/v2
target: robotics-two-link-arm
generated_at: 2026-10-28
strict: true
sources: src/content/posts/robotics-two-link-arm.md
summary: 🔴 0 · 🟡 2 · 🟢 8

## Findings

### 🟡 [L2] src/content/posts/robotics-two-link-arm.md:147

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:147
- quote: 이 글에서는 거리가 $\theta_2$를 정하고 방향이 $\theta_1$을 정한다는 구조까지 본다.
- message: 앞에서는 일반 목표점에 θ2 후보가 두 개이고, 후보를 하나 고를 때마다 θ1이 정해진다고 올바르게 설명했다. 이 요약은 거리와 방향이 각각 관절각 하나를 정하는 것으로 읽혀 핵심인 다중 해를 흐린다. 실제 T=(2,1)에서는 같은 거리로 θ2=90°와 -90°가 나오고, 같은 목표 방향이어도 각각 θ1=0°와 약 53.13°가 필요하다. 식과 앞선 증명이 틀렸다는 뜻은 아니다.
- recommendation: “거리로 θ2의 후보를 찾고, 각 후보마다 θ1을 정해 손끝의 방향을 목표점에 맞춘다.”로 바꾼다. 원점 예외는 바로 앞 목록의 설명을 유지한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/robotics-two-link-arm.md:17

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/robotics-two-link-arm.md:17
- quote: 이 글의 예는 $L_1=2$, $L_2=1$이다.
- message: 고리 모양 작업 공간과 자세 0·1·2개라는 결론은 양의 링크 길이, 같은 평면의 회전 관절, 모든 방향을 허용하는 관절 범위, 충돌을 제외한 손끝 위치 문제에서 맞다. 본문은 기하로부터 그 모델을 추론할 수 있지만 관절 제한·충돌을 제외한다고 명시하지 않는다. 19행의 대표 각도는 같은 방향의 표기 규칙이며 실제 허용 범위와는 다르다. 예를 들어 둘째 관절을 0° 이상으로 제한하면 T=(2,1)의 두 후보 중 θ2=-90°인 자세는 허용되지 않는다. 식의 계산 오류보다는 실제 로봇까지 결론을 일반화하지 않도록 적용 전제를 밝힐 문제다.
- recommendation: 첫 절에 “이 글에서는 길이가 양수인 두 링크가 한 평면에서 움직이고, 두 관절은 모든 방향으로 돌 수 있다고 가정한다. 충돌은 고려하지 않고 손끝의 위치만 맞춘다.” 정도를 넣는다. 새로운 충돌 설명이나 관절 제한 계산을 추가할 필요는 없다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-two-link-arm.md:11

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-two-link-arm.md:11
- quote: 각도에서 손끝의 위치를 구하는 질문을 **순기구학**이라 한다.
- message: 검토 완료, 이슈 없음. 평서체와 구체적인 팔 예제를 유지하며 용어 정의·논증에 필요한 반복이 주를 이룬다. 과교정이 필요한 문체 문제는 찾지 못했다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-two-link-arm.md:117

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-two-link-arm.md:117
- quote: 거꾸로 이 범위 안의 목표점에는 항상 닿는다.
- message: 분량·난이도에 대한 선택적 개선이다. 이 한 문단에 c 정의, 단위원의 점 구성, θ2 선택, 길이 맞추기, θ1으로 방향 맞추기, d=0 예외가 들어 있어 입문 독자가 가장 멈추기 쉬운 곳이다. 논증은 맞고 필요한 단계도 빠지지 않았다. 원문 길이는 앞의 기초 3·4편보다 짧고, 순기구학에서 도달 여부·해 개수로 이어지는 구성도 승인 범위에 맞으므로 분량만으로 분리할 필요는 없다.
- recommendation: 내용을 삭제하거나 뒤로 넘기지 않고 “θ2로 거리를 맞춘다 → θ1으로 방향을 맞춘다 → 원점 예외” 세 덩어리로 문단을 나눈다. 필요하면 앞에 이 두 단계의 목적을 한 문장으로 예고한다. 역기구학 각도 계산식·야코비안은 지금 추가하지 않는다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-two-link-arm.md:19

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-two-link-arm.md:19
- quote: 두 관절 각의 한 쌍 $(\theta_1,\theta_2)$를 팔의 **자세**라 부르자.
- message: 검토 완료, 이슈 없음. 링크·관절각·자세·목표점·작업 공간을 정의하며, 앞 글의 막대 좌표와 고정 좌표를 이어 쓴다. T의 노름은 위치벡터의 길이로 풀어 설명했고, 거리 기호 d를 목표점 거리로 바꾸는 조건도 밝혔다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L4] src/content/posts/robotics-two-link-arm.md:23

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/robotics-two-link-arm.md:23
- quote: θ1은 x축에서 첫 링크까지, θ2는 첫 링크의 방향(점선)에서 둘째 링크까지 잰다.
- message: 검토 완료, 이슈 없음(위 모바일 수식 배열은 선택적 권고). 정적 SVG 5장과 실험 SVG 2장의 소스·브라우저 렌더를 본문과 대조했다. 링크 길이·상대각·호·거울상·도달 범위·수치 예제가 맞고 라벨의 유의미한 겹침을 발견하지 못했다. 순기구학 초기 (30°,60°)에서 P≈(1.73,2), d≈2.65이며 d²=7이다. 역기구학 T=(3,0),(1,0),(0,0.5),(3,1),(0,0),(2,1)에서 자세 수 1,1,0,0,0,2를 직접 확인했다. 닿지 않는 점에서 c를 cosθ2의 실제 값처럼 표시하지 않는다. 드래그·키보드·초기화·no-JS·print media의 정적 그림 전환도 확인했다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L4] src/content/posts/robotics-two-link-arm.md:40

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/robotics-two-link-arm.md:40
- quote: \mathbf b=R(\theta_1)
- message: 모바일 읽힘 개선(선택). 390px 뷰포트에서 이 한 줄 유도식은 표시 폭 345px, 내용 폭 644px로 거의 두 화면이다. 가로 스크롤은 정상 작동하고 페이지 자체가 넘치지는 않지만, 회전행렬을 곱한 결과와 덧셈정리 결과를 동시에 보기 어렵다. 48행 손끝 식도 513px다. 수학 오류나 잘림 버그로 판정하지 않는다.
- recommendation: 40행은 aligned 환경에서 등호마다 줄을 바꿔 회전행렬 적용·성분 전개·합각 결과를 세 줄로 보여 준다. 48행도 모바일 독해를 중시하면 x·y 성분을 두 줄로 놓는다. 증명 단계와 식의 내용은 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-two-link-arm.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-two-link-arm.md:2
- quote: 평면 2관절 팔 — 각도에서 손끝으로, 손끝에서 각도로
- message: 검토 완료, 이슈 없음. 제목이 순·역기구학 두 질문을 대표하고 도입에서 역기구학 범위를 도달 여부와 자세 개수로 명시한다. description에도 길이가 다른 경우라는 조건이 반영되어 있다. 빌드의 description 189자 SEO 경고는 품질 실패가 아니며 수학·난이도 판정에 영향을 주지 않는다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-two-link-arm.md:13

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-two-link-arm.md:13
- quote: 역기구학은 목표점에 닿는지와 닿는 자세가 몇 개인지까지 답한다.
- message: approved extension. 승인 자료인 2026-10-27-robotics-two-link-arm-design.md의 독자·목적·사용자 확정 범위·provenance·증명 의무를 본문 및 앞의 기초 1–4편과 대조했다. 순기구학 유도, 존재 조건과 자세 개수, 각도 계산식 유보, 두 실험이 스펙의 범위와 일치한다. 링크 예제와 회전 길이 보존으로 세운 거리 논증은 작성자 추가로 명시돼 있다. 비공개 PPT·공업수학 PDF 자체를 이번에는 다시 대조하지 않았으며, 승인 스펙을 원천 충실성 판정에 사용했다. 공개 근거는 Modern Robotics 저자 서버의 2017년 2-up 판 6장 도입부(인쇄 219–220쪽, 식 6.1)와 OpenStax 10.2를 직접 확인했다. 본문의 MR-v2.pdf URL은 웹 도구에서 시간 초과되어 같은 저자의 2-up 판으로 대조했다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-two-link-arm.md:92

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-two-link-arm.md:92
- quote: d^2=L_1^2+L_2^2+2L_1L_2\cos\theta_2
- message: 위 모델 전제 명시 권고 외에 수식·개수 증명의 오류는 찾지 못했다. b의 방향 θ1+θ2, P=a+b, 회전의 길이 보존을 이용한 거리 식, 도달 조건의 필요성과 충분성, 단위원 교점 수와 θ2마다 θ1의 유일성(d>0), L1=L2·T=O에서 무수히 많은 자세가 모두 타당하다. 예 (30°,60°)→(√3,2), T=(2,1)의 두 자세와 팔꿈치 (2,0)/(1.2,1.6), d=1·3 경계도 재계산했다. 모든 양의 링크 길이를 고려할 때 L1<L2에서도 접힌 팔의 s가 음의 x축을 가리킬 뿐 방향 맞추기와 개수 논증은 유지된다. 코사인 법칙의 부호는 안쪽 각 180°-θ2를 사용하므로 맞다. 원점 예외를 포함한 129–133행 분류가 전체 경우를 덮는다.
- recommendation: 없음
- gate_effect: info

## 후속 처리

### PR #250 독립 검토 — 2026-10-28

- 검토 head: c8c6bedc4779a3184d525e1d80f297e41dfa9534. GitHub PR head와 로컬 HEAD가 일치함을 확인했다.
- 기준: AGENTS.md, docs/writing-rules.md, docs/readability-guide.md, docs/review-rubric.md, .claude/commands/review-post.md, docs/reviews/README.md, 포스트별 설계 스펙, docs/design/SVG_LABS.md. 앞선 2026-10-27 리뷰의 권고와 반영 내역도 대조했다. 그 리뷰 파일은 수정하지 않았다.
- 판정: 🔴 0 · 🟡 2 · 🟢 8. 두 권고는 모델 적용 전제와 147행의 후보 선택 요약이다. 입문 난이도는 앞의 네 편을 읽었다는 조건에서 적절하다. 117행 증명의 문단 분리와 긴 수식의 여러 줄 배열은 선택적 읽힘 개선이다.
- 분량 판단: frontmatter 제외 원문(수식·링크·마크업 포함)의 글자 수는 기초 3 12,885자, 기초 4 12,859자, 기초 5 10,508자다. 기초 5에는 독립 수식 블록 9개, 정적 도판 5장, 실험 2개가 있다. 이 수치는 비교 보조이며 길이만으로 분리 여부를 판단하지 않았다. 순기구학 → 거리 → 도달 조건 → 해 개수라는 중심 흐름과 필요 증명은 한 편에 남기는 것이 적절하다.
- 결정적 검사: 지적 0건. npm run test:js: 97/97 통과. 순기구학 360² 상태와 역기구학 13² 목표점 검사 포함. 변이 시험은 작성자 주장으로만 읽었고 이번에 재실행하지 않았다.
- 격리 worktree 빌드: exit 0, 154쪽 생성, 77개 글 본문 검사 통과. 해당 글의 브라우저 KaTeX 오류 0, pageerror 0.
- Chromium 1100px/390px 화면 확인: 정적 그림 5장과 실험 2개, 읽기 값, 범례를 확인했다. 모바일 문서 폭 390px/scrollWidth 390px. 긴 수식은 자체 가로 스크롤을 사용한다.
- 포인터·키보드: 어깨 손잡이를 중심에서 비껴 잡아 30°→120° 회전할 때 θ2=60°와 거리 유지. 손끝만 끌어 (30°,60°)→(30°,-30°), 팔꿈치 중심 6 SVG px 안에서 각 유지, 드래그 중 Enter 초기화 후 포인터를 움직여도 (30°,60°) 유지. 목표점은 중심에서 비껴 잡아 (2,1)→(0,0.5)로 옮겼고 자세 0개·빨간 표시 및 초기화를 확인했다.
- fallback: JavaScript 차단 시 두 실험의 정적 이미지가 실제로 로드되고 보인다. print media에서는 live가 숨고 static이 보인다. 실제 터치 기기·다른 브라우저·인쇄물의 페이지 나눔은 검증하지 않았다.
- 화면 근거: [모바일 회전행렬 유도식](../review-prep/2026-10-28-pr250-forward-math-mobile.png), [모바일 역기구학 실험](../review-prep/2026-10-28-pr250-inverse-mobile.png), [모바일 읽기 값](../review-prep/2026-10-28-pr250-inverse-readouts-mobile.png).
- 공개 대조: [Modern Robotics 저자 공개 2-up 판](https://hades.mech.northwestern.edu/images/b/b2/MR-2up.pdf#page=119), [OpenStax 코사인 법칙](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-2-non-right-triangles-law-of-cosines). 공식의 재유도·경계 검토와 함께 사용했다.
- 리뷰 보고서와 화면 근거만 작성했다. 본문·실험 코드·SVG 수정, GitHub 댓글·리뷰 제출, 커밋·푸시는 하지 않았다.

### 독립 검토 반영 — 2026-10-28

- 🟡 [L7] 17행: 바로 뒤에 모델 가정 문단을 넣었다. "이 글에서는 길이가 양수인 두 링크가 한 평면에서 움직이고, 두 관절은 어느 방향으로든 돌 수 있다고 가정한다. 실제 관절에는 돌 수 있는 범위가 있고 링크끼리 부딪히기도 하지만, 여기서는 그런 제한과 충돌을 따지지 않고 손끝의 위치만 맞춘다." 관절 제한 계산이나 충돌 설명은 더하지 않았다. 스펙의 「두 관절과 두 각」 항목에도 같은 가정을 적었다.
- 🟡 [L2] 147행: "이 글에서는 거리로 $\theta_2$의 후보를 찾고, 각 후보마다 $\theta_1$을 정해 손끝의 방향을 목표점에 맞추는 구조까지 본다."로 바꿨다.
- 🟢 [L2] 117행: 증명 내용은 그대로 두고 네 문단으로 나눴다. 두 단계를 예고하는 문장("$\theta_2$로 손끝까지의 거리를 맞추고, $\theta_1$로 손끝의 방향을 맞추는 두 단계로 그런 자세를 만들어 보자"), 거리 맞추기("거리부터 맞춘다."), 방향 맞추기("방향은 첫 관절로 맞춘다."), 원점 예외("$d=0$이면 맞출 방향이 없다.") 순이다.
- 🟢 [L4] 40행: `aligned`로 등호마다 줄을 바꿔 회전행렬 적용, 성분 전개, 두 각의 합 결과를 세 줄로 놓았다. 48행 손끝 식도 $x$ 성분과 $y$ 성분을 두 줄로 놓았다. 점을 괄호 안 순서쌍으로 적는 표기는 유지했다.
- 나머지 🟢 여섯 건([L1] 11행, [L3] 19행, [L4] 23행, [L5] 2행, [L6] 13행, [L7] 92행): 이슈 없음 판정이라 조치하지 않았다.
- 확인: 결정적 글 검사 지적 0건. 격리 빌드 154쪽, 이 글의 KaTeX 오류 0(`aligned` 블록 3개 렌더). 줄을 바꾼 두 식의 모바일 표시 폭은 브라우저로 다시 재지 않았다.
