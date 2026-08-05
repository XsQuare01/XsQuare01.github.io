schema_version: review-report/v2
target: closest-pair-five-points
generated_at: 2026-08-05
strict: true
sources: src/content/posts/closest-pair-five-points.md
summary: 🔴 0 · 🟡 4 · 🟢 4

## Findings

### 🟡 [L4] src/content/posts/closest-pair-five-points.md:26

- severity: 🟡
- source: L
- rule_id: L4
- location: src/content/posts/closest-pair-five-points.md:26
- quote: combine 단계에서 우리는 분할선 양옆 폭 $D$짜리 **밴드** 안의 점들을 살핀다.
- message: 같은 양을 본문은 "폭 $D$짜리 밴드", SVG는 `2D (밴드 폭)`(square-packing.svg:17)로 적어 배수가 어긋난다. 본문 53행이 "분할선 좌우 각 $D$"로 풀어 주기는 하지만, 26행만 읽으면 밴드 전체 폭이 $D$로 읽힌다. 이 값은 칸 개수를 정하는 양이라 오해가 결론까지 번진다. 폭을 $D$로 잡으면 가로 2칸 × 세로 2칸 = 4칸이 되어 후보가 3개로 줄고, 글의 결론인 7과 어긋난다.
- recommendation: 26행을 "분할선 좌우로 각각 $D$, 합쳐서 폭 $2D$인 밴드"처럼 총 폭이 드러나게 고친다. 노션 원문도 "기준선 좌우에 `D`만큼 밴드를 그린다"로 좌우 각각을 밝히므로 그 표현을 따르면 원문과도 맞는다.
- gate_effect: warn

### 🟡 [L6] src/content/posts/closest-pair-five-points.md:102

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/closest-pair-five-points.md:102
- quote: 맞은편을 눈대중으로 세면 "5개쯤"이라는 숫자가 나오기 쉽다.
- message: 노션 원문("Closest Pair", 아이디어 1·2)의 5는 눈대중이 아니라 근거를 밝힌 세기다. 원문은 "한 변의 길이가 `D`인 정사각형 내에서는 최대 3개의 점이 존재할 수 있다. 마찬가지로 한 변의 길이가 `D`인 정사각형이 2개 붙어있는 경우 최대 5개의 점이 존재할 수 있다"고 적고, 아이디어 2에서도 "정사각형 내에는 최대 3개" 근거를 달아 "자신 위에 있는 점 5개"를 말한다. 원문의 논거를 어림짐작으로 축소하면 provenance 기록이 원문보다 약하게 남는다.
- recommendation: "원문은 한 변 $D$인 정사각형에 최대 3점, 두 칸이면 최대 5점이라는 세기로 5를 얻는다"처럼 원문의 근거를 밝힌 뒤, 칸 크기를 $D/2$로 잘게 쪼개면 상한이 8점(후보 7개)으로 나온다는 차이로 설명한다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/closest-pair-five-points.md:68

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-five-points.md:68
- quote: 분할선이 칸 경계와 딱 맞아떨어지므로, 어떤 칸도 분할선을 걸치지 않는다. 즉 한 칸은 통째로 왼쪽 편이거나 통째로 오른쪽 편이다.
- message: 2026-06-30 리포트의 같은 지적이 아직 반영되지 않았다(그때는 55행). 보조정리 1의 증명은 "한 칸의 두 점은 같은 편 점"이라는 단계에 기대는데, 이 단계는 기하적 편(분할선 좌우)과 재귀가 배정한 편이 일치할 때만 성립한다. 구현은 x좌표로 정렬한 배열을 인덱스 중앙에서 가르므로, x가 분할선과 같은 점들이 서로 다른 재귀로 갈라질 수 있다. 그 두 점은 같은 칸에 있으면서 같은 재귀에 속하지 않아 거리 $\ge D$ 보장을 받지 못하고, 칸당 1점이 깨진다.
- recommendation: "분할선 위의 점은 한쪽(예: 왼쪽) 반열린 영역에 배정한다"처럼 경계·동률 배정 규약을 명시하거나, 일반 위치 가정(분할선 위에 점이 없다)을 전제로 밝힌다. 노션 원문의 코드도 인덱스로 가르므로, 규약을 적어 두면 원문 구현과의 간극도 함께 닫힌다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/closest-pair-five-points.md:103

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/closest-pair-five-points.md:103
- quote: 하지만 위처럼 칸으로 꼼꼼히 세면 안전하게 보장되는 값은 7이다. 5는 살짝 모자란 어림이었던 셈이다.
- message: 글이 증명한 것은 "7이면 충분하다"는 상한뿐이고, "5로는 부족하다"는 별개의 주장이다. 후자는 5개만 보면 최소 거리 쌍을 놓치는 배치를 제시해야 닫힌다. 상한 논거를 촘촘히 해서 7을 얻었다는 사실은 5의 반례가 되지 못한다. 노션 원문의 `j <= 5` 코드는 실행 결과에서 통과로 기록돼 있어, 근거 없이 "모자란다"고 단정하면 원문 구현을 잘못된 것으로 읽게 만든다.
- recommendation: "이 세기로 보장되는 값은 7이다. 5를 보장하려면 더 촘촘한 논거가 필요하다"처럼 상한 주장으로 좁힌다. 5가 실제로 부족함을 말하려면 반례 배치를 함께 싣는다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/closest-pair-five-points.md:1-140

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/closest-pair-five-points.md:1-140
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 평서체가 일관되고 과한 강조나 경구식 마무리가 없다. 줄표는 8개인데 제목의 시리즈 표기와 불릿 라벨 구분(53·54행)을 빼면 "주장 — 부연" 꼴이 세 곳(28·34·133행)이라 남발로 보기 어렵고, 결정적 검사 D2도 임계치 미달로 걸리지 않았다. 의자 비유(38행)는 장식이 아니라 최소 거리 제약을 설명하는 기능을 한다.
- recommendation: 현재 문체를 유지한다. 줄표가 더 늘어나면 28·34행처럼 마침표로 끊는 쪽을 먼저 고려한다.
- gate_effect: info

### 🟢 [L2] src/content/posts/closest-pair-five-points.md:24-98

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/closest-pair-five-points.md:24-98
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 왜 개수가 중요한가 → 같은 편 거리 제약 → 후보 직사각형 → 칸 쪼개기 → 다음 7개로 이어지는 순서에 도약이 없고, 각 단계가 앞 단계의 결론만 쓴다. 49행이 "각 점은 자기보다 위만 본다"와 그 이유(아래쪽 점은 위를 올려다볼 때 세어진다)를 함께 밝혀 중복 비교 의문을 미리 막는다. 밴드 폭 표기 문제는 별도 L4로 분리했다.
- recommendation: 현재 설명 순서를 유지한다.
- gate_effect: info

### 🟢 [L3] src/content/posts/closest-pair-five-points.md:34-94

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/closest-pair-five-points.md:34-94
- quote: not-recorded
- message: 검토 완료, 이슈 없음. $D$·$D_L$·$D_R$, 밴드, 칸, 같은 편/맞은편을 끝까지 같은 말로 쓴다. 이전 리포트가 쓰던 "셀"을 본문은 "칸"으로 통일했고 SVG 레이블도 "칸"이라 본문과 그림의 용어가 일치한다.
- recommendation: 현재 용어 규약을 유지한다.
- gate_effect: info

### 🟢 [L5] src/content/posts/closest-pair-five-points.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/closest-pair-five-points.md:2-4
- quote: title: "추가 설명 — 왜 다음 7개만 비교하면 되는가"
- message: 검토 완료, 이슈 없음. 제목이 글의 유일한 질문을 그대로 담고, description이 직관(가까운 점은 빽빽이 못 모인다)과 세기 방법(칸으로 쪼개기), 결론(상수 최대 7개)을 실제 본문 범위대로 요약한다. category `algorithm`과 difficulty `고급`도 허용 enum이며 내용 난이도와 맞는다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

## 후속 처리

🟡 4건을 모두 반영했다. 판정은 2026-08-05 시점 근거로 그대로 남긴다.

- 🟡 [L4] :26 밴드 폭 표기 → **반영 완료**. "분할선 좌우로 각각 $D$씩, 합쳐서 폭 $2D$인 밴드"로 총 폭을 드러냈다. SVG 레이블 `2D (밴드 폭)`과 배수가 맞는다. 노션 원문의 "기준선 좌우에 `D`만큼" 표현과도 일치한다.
- 🟡 [L7] :68 경계·동률 배정 규약 → **반영 완료**. 분할선이 어느 점도 지나지 않는다는 전제를 블록 인용에 명시하고, 그 전제가 필요한 이유(x좌표가 같은 점들이 양쪽으로 갈리면 한 칸의 두 점이 서로 다른 재귀에 속할 수 있다)를 함께 적었다. 2026-06-30 리포트에서 넘어온 지적이다.
- 🟡 [L6] :102 원문 근거 축소 → **반영 완료**. "눈대중" 표현을 걷고 노션 원문의 실제 세기(맞은편 한 변 $D$짜리 칸 두 개, 칸당 3개로 5)를 밝혔다. 두 숫자가 갈리는 이유를 세는 영역의 차이로 설명했다.
- 🟡 [L7] :103 "5 부족" 미증명 → **반영 완료**. 상한 주장으로 좁혔다. "여기서 보인 것은 7이면 충분하다는 상한이며, 5로는 부족하다는 것은 별개의 주장"이라고 적고 반례가 필요함을 명시했다.

반영 후 검증: 결정적 검사 재실행 "발견 사항 없음 ✅", `npm run build` 성공. 후보 직사각형 크기($2D \times D$), 칸 개수(8), 결론(다음 7개), SVG는 바꾸지 않았다.
