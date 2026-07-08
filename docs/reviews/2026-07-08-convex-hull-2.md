## 결정적 검사: src/content/posts/convex-hull-2.md

🟡 권장 (1)
- [D2] src/content/posts/convex-hull-2.md:10, src/content/posts/convex-hull-2.md:15, src/content/posts/convex-hull-2.md:18  줄표(—) 23회 — 임계치(13) 초과. AI 문체 신호 샘플 위치: src/content/posts/convex-hull-2.md:10, src/content/posts/convex-hull-2.md:15, src/content/posts/convex-hull-2.md:18

요약: 🔴 0 · 🟡 1 · 🟢 0

## LLM 비평: src/content/posts/convex-hull-2.md

🟡 권장 (3)
- severity: 🟡 · source: L · rule_id: L1 · location: src/content/posts/convex-hull-2.md:10 · gate_effect: warn
  - quote: "결과는 $O(N \log N)$ — 그리고 그것이 사실상 한계라는 것까지"
  - message: 본문 문장 중간의 수사적 줄표가 8곳 안팎으로 많다(D2와 동일 사안). 제목·소제목·이미지 캡션의 구조적 줄표는 1편과 일관되므로 유지해도 되지만, 문장 내부 줄표는 AI 문체 신호다.
  - recommendation: 문장 중간 줄표를 마침표·접속사로 풀어 임계치 이하로 낮춘다.
- severity: 🟡 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-2.md:157 · gate_effect: warn
  - quote: "숫자를 원 위의 점으로 바꾸는 환원으로 **볼록 껍질 $\Rightarrow$ 정렬**이 성립하므로"
  - message: 화살표 표기가 환원 방향을 모호하게 만든다. 실제 논증은 "정렬이 볼록 껍질로 환원된다(볼록 껍질을 풀면 정렬이 풀린다)"이다.
  - recommendation: 기호 대신 "볼록 껍질을 풀 수 있으면 정렬도 풀린다"처럼 서술형으로 고친다.
- severity: 🟡 · source: L · rule_id: L2 · location: src/content/posts/convex-hull-2.md:31 · gate_effect: warn
  - quote: "1편에서 세 점의 회전 방향을 정수 연산만으로 판정하는 **CCW**를 만들었고"
  - message: 1편의 세 가지 가정(x·y좌표 서로 다름, 일직선 3점 없음)을 2편에서도 그대로 쓰는데 명시하지 않았다. 특히 CCW 비교자 정렬과 스캔의 `<0`/`>0` 판정은 일직선 배제 가정에 기댄다.
  - recommendation: 되짚어보기 절에 "1편의 세 가지 가정을 그대로 유지한다" 한 문장을 추가한다.

🟢 참고 (9)
- severity: 🟢 · source: L · rule_id: L6 · location: src/content/posts/convex-hull-2.md:135 · gate_effect: info
  - quote: "\theta_i = \frac{v_i}{M+1} \cdot 2\pi"
  - message: 노션 원본은 $v/\max \cdot 2\pi$로, 최댓값이 각도 $2\pi(=0)$와 겹치는 문제가 있다. 본문은 $M+1$로 나눠 정정했다. 원본에 없는 "비교 기반 모델" callout도 하한 주장의 정확성을 위해 추가한 것이다. 의도된 정정·보강으로 판단.
  - recommendation: 조치 불요. 노션 원본에 정정 사항을 남기고 싶다면 1편 때처럼 정정 토글 추가를 고려.
- severity: 🟢 · source: L · rule_id: L6 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 소스 대조 완료 — 노션 `Convex hull 1` 노트의 Graham Scan 섹션(스택 절차, 처음 두 점 보존, push/pop $O(N)$ 논증, 원 위 점 환원)이 모두 반영됨. 핵심 누락 없음.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L1 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 줄표 외 항목(경구식 마무리, 과한 비유, 대칭 반복) 검토 완료, 이슈 없음.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L2 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 가정 명시 건 외 흐름·명료성 검토 완료, 이슈 없음.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L3 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 용어(껍질/꼭짓점/좌회전/우회전/push/pop)와 ~다 평서체 일관.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L4 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. SVG 5장 모두 본문과 일치 — 도판 4장이 같은 점 배치(Y,1~7)를 공유하고, scan-pop의 4→5→6 우회전은 좌표상 실제 CCW 계산과 일치. lower-bound의 각도식 v·2π/5는 본문 예시(M=4)와 일치.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L5 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 제목·description이 Graham Scan과 하한이라는 실제 내용을 대표.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L6 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음 (위 정정·보강 참고 항목 외 자의적 추가 없음).
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L7 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 화살표 표기 건 외 논증·복잡도 검토 완료, 이슈 없음. 비교자 부호 해석, 스캔의 분할상환 $O(N)$, 환원의 $O(N)$ 전·후처리와 하한 이전 논리 모두 옳음.
  - recommendation: 조치 불요.

요약(전체): 🔴 0 · 🟡 4 · 🟢 9

## 반영 결과 (2026-07-08)

- [D2/L1] 문장 중간 줄표 10곳을 마침표·접속사·콤마로 정리. 재검사 결과 "발견 사항 없음 ✅".
- [L7] 핵심 정리의 "볼록 껍질 ⇒ 정렬" 표기를 "볼록 껍질을 풀 수 있으면 정렬도 풀린다"로 서술형 변경.
- [L2] 되짚어보기 절에 1편의 세 가지 가정 유지 문장 추가.
- 반영 후 `npm run build` 통과 (103 pages).
