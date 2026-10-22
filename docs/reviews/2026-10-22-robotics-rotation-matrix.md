schema_version: review-report/v2
target: robotics-rotation-matrix
generated_at: 2026-10-22
strict: true
sources: src/content/posts/robotics-rotation-matrix.md
summary: 🔴 0 · 🟡 0 · 🟢 12

## Findings

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:41

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:41
- quote: 그 정의는 모든 각도에서 성립하므로 $\theta$가 몇이든 맞는다.
- message: 정의는 '성립'하는 대상이 아니라 값을 정하는 약속이다. 사인과 코사인 글은 같은 내용을 "단위원 정의는 … 각도에도 값을 준다"로 적었다. 증명 의무(모든 θ)는 닫혀 있고 표현만 어긋난다.
- recommendation: "그 정의는 모든 각도에 값을 주므로 θ가 몇이든 맞는다."
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:49

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:49
- quote: 음수배는 방향을 반대로 하는 것까지 실수배에 들어 있으므로
- message: 주어와 서술이 엇갈린다. '음수배는 … 실수배에 들어 있다'에 '방향을 반대로 하는 것까지'가 끼어 문장이 어색하고, 의존명사 '것'도 불필요하다.
- recommendation: "방향을 반대로 바꾸는 음수배도 실수배이므로, a, b가 음수여도 이 식은 그대로 성립한다."
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:53

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:53
- quote: 처음 절에서는 $\mathbf e_x'$를 $90^\circ$ 돌린 단위벡터를 $\mathbf e_y'$로 정했다. 처음의 $\mathbf e_y$를 막대와 함께 $\theta$만큼 돌린 것도 이것과 같다.
- message: 1차 반영으로 다시 쓴 문단이다. '처음'이 두 문장에서 다른 뜻(첫 절, 처음 자세)으로 쓰였고, '것도 이것과'처럼 의존명사와 지시어가 겹친다. 같은 문단의 "θ를 먼저 돌리고 90°를 나중에 돌려도"는 각을 목적어로 삼아 무엇을 돌리는지가 빠졌다.
- recommendation: "1절에서는 … $\mathbf e_y'$로 정했다. 처음 자세의 $\mathbf e_y$를 막대와 함께 θ만큼 돌린 화살표도 $\mathbf e_y'$와 같다." 뒤 문장은 "$\mathbf e_x$를 θ만큼 먼저 돌리고 90°만큼 나중에 돌려도"로 고친다.
- gate_effect: info

### 🟢 [L1] src/content/posts/robotics-rotation-matrix.md:181

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/robotics-rotation-matrix.md:181
- quote: 나머지 $(-0.8,0.6)$은 $\mathbf e_y'$의 1배였다.
- message: 앞 글에는 $\mathbf e_y'$가 없었다. '1배였다'처럼 과거형으로 쓰면 앞 글에서 이미 그렇게 말한 것처럼 읽힌다. 1차 리뷰가 제안한 문구를 그대로 옮긴 결과다.
- recommendation: "앞 글에서 (1,3)을 레일에 정사영한 길이는 3이었고, 그 나머지 (−0.8, 0.6)은 $\mathbf e_y'$의 1배다."
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-rotation-matrix.md:69

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-rotation-matrix.md:69
- quote: 전제에 따라 $s_x\mathbf e_x$는 $s_x\mathbf e_x'$가 되고 $s_y\mathbf e_y$는 $s_y\mathbf e_y'$가 되며, 둘은 이어 붙은 채로 돈다.
- message: "$s_y\mathbf e_y$가 $s_y\mathbf e_y'$가 된다"는 전제만으로 나오지 않고, 53행에서 보인 "θ 돌린 $\mathbf e_y$ = $\mathbf e_y'$"가 함께 있어야 한다. 69행은 그 근거를 "전제에 따라"로만 적고, 53행도 이 사실을 어디에 쓰는지 밝히지 않아 다시 쓴 53행 문단이 왜 필요한지가 드러나지 않는다. 논증 자체는 닫혀 있고 순환도 없다.
- recommendation: 69행을 "앞 절에서 본 대로 $\mathbf e_x$는 $\mathbf e_x'$로, $\mathbf e_y$는 $\mathbf e_y'$로 가므로, 전제에 따라 $s_x\mathbf e_x$는 …"처럼 고친다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-rotation-matrix.md:107

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-rotation-matrix.md:107
- quote: 앞 절의 계산에 쓴 수는 $\mathbf e_x'$의 두 성분과 $\mathbf e_y'$의 두 성분, 모두 네 개다.
- message: 앞 절 계산에는 $s_x$, $s_y$(예에서는 3과 1)도 들어간다. "모두 네 개"는 각도가 정하는 수만 센 값이라, 세는 독자는 여섯 개를 얻는다.
- recommendation: "앞 절의 계산에서 θ가 정하는 수는 … 모두 네 개다"처럼 셀 대상을 밝힌다.
- gate_effect: info

### 🟢 [L2] src/content/posts/robotics-rotation-matrix.md:191

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/robotics-rotation-matrix.md:191
- quote: 막대를 $\theta$만큼 되돌리면 막대가 처음 자세로 돌아오고, 그 자세에서는 고정 좌표와 막대 좌표가 같다. 되돌린 점의 좌표가 막대 좌표인 이유다.
- message: 169행의 존재 논증을 거의 같은 말로 되풀이하고, 두 곳은 서로를 가리키지 않는다. 169행의 "거기서 다시 θ만큼 돌리면 … p = s_x e′_x + s_y e′_y"도 3절 결과를 쓰면서 출처를 적지 않는다. 존재 논증 자체는 맞고, 유일성은 175행의 내적 계산이 닫는다.
- recommendation: 169행 해당 문장에 3절을 가리키는 말을 넣는다. 191행 두 문장은 "앞에서 막대 좌표를 정할 때 물건을 θ만큼 되돌렸는데, $R(-\theta)$를 곱하는 일이 바로 그 되돌리기다"처럼 169행을 가리키는 한 문장으로 줄인다.
- gate_effect: info

### 🟢 [L3] src/content/posts/robotics-rotation-matrix.md:13

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/robotics-rotation-matrix.md:13
- quote: 그러려면 두 각을 더한 각의 코사인과 사인을 구하는 공식이 필요하다. … 두 각을 더하는 공식은 마지막에 덤으로 얻는다.
- message: 같은 공식을 다섯 가지 이름으로 부른다. 13행에 "두 각을 더한 각의 코사인과 사인을 구하는 공식"과 "두 각을 더하는 공식"이 나란히 놓였고, 195행 제목은 "각을 더하는 공식", 197행은 "두 각의 합에 대한 공식", 212행은 "덧셈정리"다. '각을 더하는 공식'은 각을 더하는 방법처럼 읽혀 공식의 내용과도 어긋난다.
- recommendation: 13행 두 번째 문장을 "그 공식은 마지막에 덤으로 얻는다"로 고친다. 195행 제목과 197행은 "두 각의 합 공식"처럼 한 이름으로 맞추고, 212행에서 "고교에서 배우는 덧셈정리"라고 이름을 붙인다.
- gate_effect: info

### 🟢 [L4] src/content/posts/robotics-rotation-matrix.md:61

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/robotics-rotation-matrix.md:61
- quote: not-recorded
- message: 검토 완료, 이슈 없음. SVG 다섯 장의 좌표를 수치로 대조했다. turned-axes(O=(230,300), 1단위 170px)의 노란 경로 `H332V164`는 O→(0.6,0)→(0.6,0.8), 초록 `V198H94`는 O→(0,0.6)→(−0.8,0.6)이라 노란 꼭짓점을 원점 중심으로 90° 돌린 상과 정확히 일치하고, 라벨 자리는 캡션·63행·aria-label과 맞는다. rod-frame(34px, 막대 4, 돌린 칸의 P (284,148) = 3e′+1e′), quarter-turn(44px, (3,1)→(−1,3), 호의 두 끝 방향), turned-point(64px, 3e′_x 끝 (1.8,2.4), P (1,3), 라벨과 범례 P), rotation-lab(40px, rotate(−30) 적용 후 P (2.098, 2.366), 읽기 값 2.1·2.37과 ≈, 첫째 열 앰버·둘째 열 초록)이 본문과 맞는다. 157행 설명은 입력 θ·s_x·s_y, 0.5 단위 스냅, 반올림 규칙을 실험 코드와 대조했다. resvg로 다시 래스터화했고 다섯 장 모두 겹침이 없다.
- recommendation: 없음
- gate_effect: info

### 🟢 [L5] src/content/posts/robotics-rotation-matrix.md:4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/robotics-rotation-matrix.md:4
- quote: 돌아간 점은 두 열을 막대 좌표만큼 더해 얻는다.
- message: 'A를 n만큼 더한다'는 보통 'A에 n을 더한다'로 읽힌다. 막대 좌표는 음수나 0.5일 수 있어 '그만큼 더한다'는 뜻이 흐리다. 본문은 113행에서 "첫째 열을 $s_x$배, 둘째 열을 $s_y$배 해서 더한"으로 정확히 정의한다. 핵심 정리(223행)의 "열을 성분만큼 더한 벡터"도 같은 표현이다. 제목과 description의 대표성은 문제없다.
- recommendation: "돌아간 점은 두 열에 막대 좌표를 곱해 더해 얻는다"로 고치고, 223행도 "열에 성분을 곱해 더한 벡터"로 맞춘다.
- gate_effect: info

### 🟢 [L6] src/content/posts/robotics-rotation-matrix.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/robotics-rotation-matrix.md:1
- quote: not-recorded
- message: `approved extension` (국소·핵심 불일치 없음). 이 글에는 Notion 원문이 없다. 승인 자료(스펙, 기구학 슬라이드 1·3·4·7·8·22–24, 선형대수 39–50쪽 추출본)와 실제로 대조했다. 원천 핵심과 본문 대응이 모두 보존됐다: 슬라이드 3 ↔ 27행(local 좌표는 일정하고 축 방향만 바뀐다), 슬라이드 1·4·8과 44쪽 ↔ 122행(R(θ)의 네 성분), 슬라이드 4 ↔ 133행(첫 행은 세계 x), 42쪽과 슬라이드 24 ↔ 131행(j번째 열은 e_j의 상), 40쪽 ↔ 107–111행(열벡터 동일시), 45–46쪽 ↔ 113–139행(곱 = 열의 일차결합 = 성분 식), 슬라이드 7 ↔ 186행(원점 이동 없이 초기 회전을 되돌림), 49쪽 ↔ 195–216행(덧셈정리). 1차 반영(첫 문장의 관절 원점 전제, '막대 끝' 삭제, 53행 논증 방향 전환)은 원천 구조와 논증을 바꾸지 않았고 스펙 provenance의 작성자 추가 범위 안이다. 스펙 11·23행은 아직 "막대 끝에 달린 집게"로 적혀 있어 본문·도판과 어긋나지만 스펙 문서 관리 사항이라 본문 판정에는 영향이 없다. 스펙 7절이 계획한 "(1,3)은 (3,1)의 각에 θ를 더한 방향"이라는 확인은 본문에 없으나 승인된 추가 예시의 생략이다. 본문에 비공개 원천을 가리키는 서술은 없다(검출 grep 0건).
- recommendation: 없음. 원하면 스펙 11·23행의 '막대 끝'을 본문에 맞춘다.
- gate_effect: info

### 🟢 [L7] src/content/posts/robotics-rotation-matrix.md:1

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/robotics-rotation-matrix.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 재계산이 모두 맞다: c²+s²=1, atan2(4,3)=53.1301°, e′x·e′y=0, 90° 규칙 (3,1)→(−1,3), 3(0.6,0.8)+(−0.8,0.6)=(1,3), 길이 √10, 행 계산 1·3, 되찾기 3·1, R(90°)·R(0°), 덧셈정리 30°+60°에서 0과 1, 실험 30°에서 (2.098, 2.366), 53°에서 (1.0068, 2.9977). θ·s·α 1000회 무작위로 ‖Rs‖=‖s‖, Rᵀ(Rs)=s, R(−θ)=R(θ)ᵀ, rot_θ(e_y)=rot_90(e′_x), cos(α+θ) 공식을 확인했다. 41·49·53·81·99·139·169/175·179·191·212행의 증명 의무(모든 θ, 모든 (a,b), 모든 s, 열 읽기 = 행 읽기, 존재·유일)가 닫혀 있다. 덧셈정리는 90° 규칙과 전제에서 나오고 그 앞 논증은 덧셈정리를 쓰지 않아 순환이 없다. 63행은 직관(그림)과 증명(90° 규칙)을 나눴다. 다시 쓴 53행은 33행 전제에서 나오는 회전각의 가법성만 쓴다. 169행 존재 논증은 −θ 되돌린 뒤 θ 돌리기가 항등이라는 점과 3절 결과로 닫히고, 유일성은 175행이 닫는다.
- recommendation: 없음
- gate_effect: info

## 후속 처리

이 판은 같은 날의 2차 리뷰다. 1차 리뷰(🔴 1 · 🟡 4 · 🟢 8)의 원래 판정, 작성자의 반영 내역, 실험 코드 리뷰(🔴 0 · 🟡 1 · 🟢 8)의 반영 내역은 이 파일의 앞 판에 그대로 있다(커밋 `e1d9249`). 2차 리뷰어는 반영한 글과 도판, 1차 리포트를 함께 읽고 L1–L7 전체를 다시 판정했다. 위 finding의 줄 번호는 2차 리뷰 시점의 글을 가리킨다.

### 1차 지적 해소 확인

2차 리뷰어가 1차 지적 10건을 하나씩 대조했고, 모두 해소로 판정했다.

- 🔴 [L4] turned-axes.svg의 초록 삼각형: 경로 `M230 300V198H94`의 꼭짓점이 노란 삼각형의 90° 회전 상과 일치하고, 라벨 자리와 63행 서술도 그림과 맞는다(래스터로 확인).
- 🟡 [L4] 11행 '막대 끝에 집게', 🟡 [L4] turned-point.svg의 P′, 🟡 [L4] 157행 '격자의 칸에 맞춰', 🟡 [L1] 65·181행 '남은 나머지': 해소.
- 🟢 [L2] 11행 원점 전제, 🟢 [L2] 53행 논증 방향, 🟢 [L1] 13행 '그 공식', 🟢 [L1] 25행 '앞의 것/뒤의 것', 🟢 [L3] '90° 규칙' 명명과 삼각형 이름: 해소. 이 가운데 181행 시제, 13행 이름, 53행 문체는 위 2차 finding으로 다시 적혔다.

### 2차 리뷰 반영

2026-10-22, 작성자가 같은 세션에서 반영했다.

- 🟢 [L2] 69행: "앞 절에서 본 대로 e_x는 e′_x로, e_y는 e′_y로 간다"를 먼저 적고, 그다음 문장에서 전제를 쓴다.
- 🟢 [L2] 191행: 두 문장을 "앞에서 막대 좌표를 정할 때 물건을 막대와 함께 θ만큼 되돌렸는데, R(−θ)를 곱하는 일이 바로 그 되돌리기다"로 줄였다. 169행에는 "돌아간 점의 식에 따라"를 넣어 3절 결과를 가리킨다.
- 🟢 [L2] 107행: "앞 절의 계산에서 θ가 정하는 수는"으로 셀 대상을 밝혔다.
- 🟢 [L1] 53행: "막대에 축을 붙일 때는 …로 정했다. 처음 자세의 e_y를 막대와 함께 θ만큼 돌린 화살표도 e′_y와 같다"로 고쳤다. 뒤 문장은 "e_x를 θ만큼 먼저 돌리고 90°만큼 나중에 돌려도"로 고쳤다.
- 🟢 [L1] 49행: "방향을 반대로 바꾸는 음수배도 실수배이므로"로 고쳤다.
- 🟢 [L1] 41행: "그 정의는 모든 각도에 값을 주므로"로 고쳤다.
- 🟢 [L1] 181행: "그 나머지 (−0.8, 0.6)은 e′_y의 1배다"로 시제를 고쳤다.
- 🟢 [L3] 13·195·197행: 13행 두 번째 이름을 "그 공식"으로, 절 제목을 "두 각의 합 공식"으로, 197행을 "두 각의 합 공식"으로 맞췄다. 212행의 "덧셈정리"는 고교에서 부르는 이름으로 남겼다.
- 🟢 [L5] 4·223행: description을 "두 열에 막대 좌표를 곱해 더해 얻는다"로, 핵심 정리를 "각 열에 성분을 곱해 더한 벡터"로 고쳤다.
- 🟢 [L6]의 권고: 스펙 11·23행의 '막대 끝'을 본문에 맞췄다. 스펙 7절의 절 이름도 "두 각의 합 공식"으로 맞췄다.

반영한 뒤 확인한 결과는 다음과 같다.

- 결정적 검사: 지적 0건
- `npm run test:js`: 79/79
- 빌드: dev 서버를 피해 격리된 복사본에서 실행. 153쪽 생성, 76개 글 본문 검사 통과, KaTeX 오류 0
