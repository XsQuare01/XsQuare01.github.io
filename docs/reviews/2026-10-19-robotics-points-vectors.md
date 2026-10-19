schema_version: review-report/v2
target: robotics-points-vectors
generated_at: 2026-10-19
strict: true
sources: src/content/posts/robotics-points-vectors.md
summary: 🔴 0 · 🟡 4 · 🟢 7

## Findings

### 🟡 [L2] src/content/posts/robotics-points-vectors.md:59

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-points-vectors.md:59
- quote: 시작점과 끝점이 같아도 경로에 따라 이동한 길이는 달라질 수 있다. 변위는 그 경로를 모두 기록하지 않는다.
- message: "시작점과 끝점이 같아도"는 "두 경로의 양 끝점이 같아도"로 의도했겠지만, 한국어로는 "시작점과 끝점이 서로 같아도", 곧 제자리로 돌아오는 경로로 먼저 읽힌다. 바로 뒤 문장의 "모두 기록하지 않는다"도 변위가 경로의 일부는 기록한다는 뜻으로 읽힐 수 있다. 변위에 남는 것은 두 끝점의 차이뿐이고 경로 정보는 전혀 없다.
- recommendation: "같은 두 점을 잇더라도 경로에 따라 이동한 길이는 달라진다. 변위에는 두 끝점의 차이만 남고 어떤 경로로 갔는지는 남지 않는다."처럼 쓴다.
- gate_effect: warn

### 🟡 [L2] src/content/posts/robotics-points-vectors.md:107

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/robotics-points-vectors.md:107
- quote: 이제 한 막대를 원점에 붙이고 돌린다고 생각해 보자.
- message: 저장소 글 72편 중 69편이 `callout-key` 핵심 정리를 두고, 블로그 관례는 도입 뒤 「이 포스트에서 다루는 내용」 목차 callout과 끝의 핵심 정리·이어지는 글 callout이다. 이 글에는 셋 다 없고, 스펙에 구조 기본값에서 벗어난 사유가 적혀 있지 않다(작성 정본 2단계는 예외 범위와 사유를 스펙에 기록하라고 한다). 입문 독자에게는 "점의 좌표는 원점에 따라 바뀐다 / 변위는 원점 이동에 따라 바뀌지 않는다 / 축 회전은 별개"를 한곳에 모은 정리가 특히 쓸모 있다.
- recommendation: 끝에 핵심 정리 callout을 두고, 107행의 다음 질문을 「이어지는 글」 callout로 옮긴다(미발행이므로 링크 없이 텍스트로). 시리즈 전체에서 이 구조를 쓰지 않기로 했다면 그 결정을 스펙에 적는다.
- gate_effect: warn

### 🟡 [L3] src/content/posts/robotics-points-vectors.md:21

- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/robotics-points-vectors.md:21
- quote: 괄호 안에서는 가로 성분 $x$를 먼저, 세로 성분 $y$를 나중에 쓴다.
- message: 이 글은 35행에서 "$(3,4)$의 두 수는 벡터의 성분"이라 하고 101행에서 "점의 좌표와 벡터의 성분이 비슷하게 보인다"고 써서, 점에는 '좌표', 벡터에는 '성분'이라는 말을 갈라 쓰는 것을 논지의 일부로 삼는다. 그런데 21행은 점 $(4,5)$의 두 수를 '가로 성분·세로 성분'이라 부르고, 23행 도판 캡션도 "점선은 B의 가로·세로 성분을 보여 준다"고 점 B에 '성분'을 쓴다. 독자가 두 말을 구별하기 시작하는 첫 절에서 용어가 섞인다.
- recommendation: 21행은 "가로 좌표 $x$를 먼저, 세로 좌표 $y$를 나중에", 23행 캡션은 "점선은 B의 가로·세로 좌표를 보여 준다"로 바꾼다. 원점에서 B까지의 화살표를 뜻하려는 것이라면 그렇게 밝힌다.
- gate_effect: warn

### 🟡 [L4] public/images/robotics-points-vectors/displacement-lab.svg:13

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/robotics-points-vectors/displacement-lab.svg:13
- quote: <text x="30" y="375">−1</text> … <text data-part="label-o" x="42" y="378" … >O</text> … <text x="52" y="397">−1</text>
- message: 원점 모서리에 글자 셋이 몰린다. 가로 눈금 "−1"(가운데 정렬, 20px, 대략 x 19–41)과 원점 이름 "O"(24px, 대략 x 42–59)가 같은 줄에서 1px 정도만 떨어져 있어 "−1O"로 이어 읽히고, 그 바로 아래 세로 눈금 "−1"이 붙는다. 작성자 인계의 390px 스크린샷(docs/review-prep/robotics-points-vectors-mobile.jpg)에서도 "-1O"가 붙어 보인다. 같은 파일 33행의 "A" 이름(125, 294)은 변위 화살표가 지나는 자리(x=125에서 y≈290)에 겹친다. 정적 그림은 JS가 없는 환경과 인쇄본에 그대로 나가는 그림이다. 리뷰어는 브라우저로 직접 보지 않았고, 좌표 계산과 작성자 스크린샷으로 판단했다.
- recommendation: 원점 모서리의 −1 눈금 둘을 빼거나 "O"를 세 번째 사분면 안쪽으로 옮겨 눈금과 떨어뜨린다. "A"는 화살표 반대쪽(A의 왼쪽 위나 오른쪽 아래)에 둔다. 실험 코드가 같은 자리에 라벨을 다시 그리는지도 함께 맞춘다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/robotics-points-vectors.md:65

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-points-vectors.md:65
- quote: **축의 방향과 한 칸의 길이는 그대로 유지한다.**
- message: 문두 접속어 0회, '-들' 0회, 줄표는 제목에만 있다. 의존명사 '것'은 41행("빼는 것이다")과 107행("구하는 것이")에 두 번이다. 굵게는 13곳인데 용어 도입(원점·좌표·변위벡터·벡터의 성분·자유벡터·영벡터·위치벡터)이 아닌 강조가 11·65·87·91행에 다섯 곳이고, 65행과 87행은 문장 전체를 굵게 했다. 강조가 용어 도입과 섞여 무엇이 새 용어인지 흐려진다.
- recommendation: 65·87행은 굵게를 풀거나 조건 부분("축의 방향과 한 칸의 길이")만 남긴다. 41행은 "순서는 끝점에서 시작점을 뺀다."로 줄일 수 있다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-points-vectors.md:103

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-points-vectors.md:103
- quote: 앞 절에서 두 종류의 숫자가 다르게 바뀐 이유다.
- message: 앞 절에서 점의 좌표는 바뀌고 변위는 바뀌지 않았다. "다르게 바뀐"은 둘 다 바뀌었는데 바뀐 방식이 달랐다는 뜻으로도 읽힌다.
- recommendation: "앞 절에서 좌표는 바뀌고 변위는 그대로였던 이유다."
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-points-vectors.md:32

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-points-vectors.md:32
- quote: \overrightarrow{AB}=(4-1,\;5-1)=(3,4).
- message: 점 $A=(1,1)$과 변위 $\overrightarrow{AB}=(3,4)$를 같은 괄호로 적는다. 선형대수 원자료(5쪽)도 $\mathbb{R}^n$의 벡터를 같은 괄호로 쓰므로 틀린 표기는 아니다. 다만 본문이 인용한 OpenStax §10.8은 벡터를 $\langle a, b\rangle$로 적어 점과 갈라 쓰고, 이 글의 주제가 바로 그 구별이다. 이후 편(프레임, 회전행렬)은 열벡터를 쓸 것이므로 시리즈의 표기 결정이 지금 필요하다.
- recommendation: 같은 괄호를 유지한다면 "이 글은 점의 좌표와 벡터의 성분을 같은 괄호로 쓰고, 이름($A$, $\overrightarrow{AB}$)으로 구별한다"는 한 문장을 둔다. 기초 4에서 열벡터로 넘어갈 때의 표기 전환도 시리즈 스펙에 적어 둔다.
- gate_effect: info

### 🟢 [L4] public/images/robotics-points-vectors/coordinates.svg:7

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/robotics-points-vectors/coordinates.svg:7
- quote: <circle cx="110" cy="230" r="7" fill="#e2e8f0"/><circle cx="230" cy="70" r="8" fill="#93c5fd"/>
- message: 나머지 세 도판(length, origin-shift, displacement-lab)은 A를 파란 원, B를 파란 마름모, 원점을 사각형으로 그려 스펙의 "점과 원점은 모양과 문자로도 구별한다"를 따른다. 첫 도판만 A가 흰 원, B가 파란 원이다. 위치 값은 네 도판 모두 한 칸 40px 기준으로 맞는다(리뷰에서 픽셀 좌표를 환산해 확인).
- recommendation: coordinates.svg의 B를 마름모로 바꾸고, A의 색을 다른 도판과 맞추거나 B만 강조하려는 의도라면 그대로 두되 모양은 맞춘다.
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-points-vectors.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-points-vectors.md:2
- quote: 점과 벡터 — 위치와 변위를 구분하기
- message: 검토 완료, 이슈 없음. 제목과 description이 글의 질문(위치와 변위의 구분)과 결론(원점 이동에 따른 좌표 변화와 변위 불변), 실험을 그대로 대표한다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-points-vectors.md:63

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-points-vectors.md:63
- quote: 원점만 옮기면 무엇이 바뀌는가
- message: approved extension. 승인 자료를 실제로 대조했다. 기구학 PPT 4장(점의 세계 좌표 = 원점 위치 + 회전한 local 좌표), 8장(방향 벡터에는 원점 위치를 더하지 않는다), 9장(원점을 옮긴 효과와 local 좌표를 바꾼 효과가 상쇄된다), 레일 HTML 도입(frame = 원점 + 축, 두 원점을 잇는 변위 벡터), 선형대수 PDF 2쪽(벡터는 크기와 방향을 가진 화살표)·5쪽(좌표 성분의 덧셈과 상수배)이 글의 핵심 줄기와 맞는다. 회전을 빼고 원점 평행이동만 다루는 범위 축소, A=(1,1)·B=(4,5)·O′=(1,2) 예시, 경로 길이와 영벡터는 스펙이 승인된 추가로 적었고 원자료의 의도(점과 방향의 변환 차이)를 해치지 않는다. 한 가지 기록 불일치가 있다. 스펙의 provenance는 선형대수 PDF 20–24쪽(일차결합)을 원문으로 적었지만 본문은 일차결합을 쓰지 않는다.
- recommendation: 스펙 provenance에서 20–24쪽을 빼거나 "기초 3에서 사용"으로 옮긴다.
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-points-vectors.md:79

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-points-vectors.md:79
- quote: 이 결과가 이번 숫자에만 해당하는지 확인해 보자.
- message: 검토 완료, 이슈 없음. 리뷰에서 다시 계산했다. $\overrightarrow{AB}=(3,4)$, 역방향 $(-3,-4)$, 길이 $\sqrt{9+16}=5$, 꺾인 경로 $3+4=7$, 새 원점 $(1,2)$에서 $A=(0,-1)$, $B=(3,3)$, 새 좌표의 차 $(3,4)$. "변위와 거리는 그대로"라는 강한 주장은 79–85행의 일반식(임의의 $(c_x,c_y)$에 대해 원점 이동량이 상쇄)으로 평행이동 전체에 대해 닫혔고, 87행이 회전으로 확대하지 않도록 범위를 막았다. 영벡터의 방향 미정(61행)과 위치벡터가 원점에 따라 달라진다는 서술(101–103행)도 옳다. 공개 대조 문헌 OpenStax §10.8의 정의(크기와 방향, 끝점 좌표의 차, 위치벡터, 크기 공식)와도 맞는다. SVG 4장의 점 위치는 모두 한 칸 40px로 환산해 본문 값과 일치한다.
- recommendation: 없음
- gate_effect: info

## 후속 처리

2026-10-19, 같은 세션에서 🟡 4건을 반영했다. PR #242가 이 수정 전 상태로 머지되어, 수정은 후속 브랜치 `fix/robotics-points-vectors-review`의 PR로 올렸다. 🟢 항목은 반영하지 않았다.

- 🟡 [L3] 21·23행: 점의 두 수를 '가로 좌표·세로 좌표'로 바꿨다. 캡션도 "B의 가로·세로 좌표"로 바꿨다.
- 🟡 [L2] 59행: "같은 두 점을 잇더라도 경로에 따라 이동한 길이는 달라진다. 변위에는 두 끝점의 차이만 남고, 어떤 경로로 갔는지는 남지 않는다."로 바꿨다.
- 🟡 [L2] 107행: 끝에 핵심 정리 callout을 더하고, 다음 질문 문단을 「이어지는 글」 callout로 옮겼다(미발행 편이라 링크 없음). 핵심 정리는 회전으로 확대하지 않도록 "원점 이동에 대한 것", "달라질 수 있다"로 범위를 적었다.
- 🟡 [L4] displacement-lab.svg 원점 모서리와 A 라벨: 라벨 위치를 모델의 `labelPositions`가 계산하게 바꿨다. A 라벨은 화살표 뒤쪽에, B 라벨은 화살표 머리 너머에 놓이고, O 라벨은 세로축의 0 눈금 자리(원점 왼쪽 위)로 옮겨 두 −1 눈금과 떨어졌다. 정적 SVG의 라벨·세로 눈금을 같은 계산값으로 고쳤고, 실험 눈금과 표시값의 음수도 U+2212로 맞췄다. `test/point-vector.test.mjs`가 정적 SVG와 실험 첫 화면의 점·라벨 위치가 같은지, 라벨이 화살표 위에 놓이지 않는지 검사한다.

같은 PR의 코드 리뷰 지적 두 건도 함께 처리했다.

- 터치 드래그: 브라우저는 SVG 안쪽 요소가 아니라 바깥 `<svg>`에서 `touch-action`을 판정한다는 명세 논의(W3C public-pointer-events 2014, Rick Byers)와 웹 플랫폼 테스트의 구성에 따라, 손잡이에서 시작한 `touchstart`만 기본 동작을 막도록 바꿨다(`passive: false`). 실기기 터치는 확인하지 못했다.
- 테스트 공백: 로더 fallback 테스트(`test/lab-loader.test.mjs`: 미등록, 불러오기 실패, 초기화 도중 실패 후 원복, 실패가 다음 실험을 막지 않음), 드래그 변환 테스트, 디렉터리 연결로 public 밖을 가리키는 경로 테스트를 더했다. 마지막 테스트는 경로 검사 줄을 끄면 실패하는 것을 확인했다.

재검증: `npm run test:js` 40/40, `python .claude/review_post.py` 결정적 지적 0건, `.claude` unittest 220/220, `npm run build` 146쪽·본문 검사 통과. 빌드 결과물 HTML에서 새 라벨 좌표, 고친 문장, 핵심 정리, 터치 처리가 반영된 것을 확인했다. 브라우저 렌더는 보지 못했다.
