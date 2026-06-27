## 결정적 검사: src/content/posts/scheduling-2.md

🟡 권장 (1)
- [D12] not-recorded  시리즈 이전 편 링크 누락: /blog/scheduling-1(`scheduling-1.md` 존재)을 본문에서 참조하지 않음

요약(결정적): 🔴 0 · 🟡 1 · 🟢 0

---

## LLM 비평: src/content/posts/scheduling-2.md

🟡 권장 (1)
- [L_link] `src/content/posts/scheduling-2.md:31` quote: `[1편](/posts/scheduling-1)` — 사이트 라우트는 `/blog/<slug>`만 존재하고 `/posts/` 경로는 없다(`src/pages/blog`만 있음). `/posts/scheduling-1`, `/posts/greedy` 두 링크 모두 404다. 다수 포스트의 정상 컨벤션(`/blog/...`)과도 어긋난다. → `/blog/scheduling-1`, `/blog/greedy`로 수정. (gate_effect: warn)

🟢 참고 (3)
- [L6] `src/content/posts/scheduling-2.md` — 소스 충실성: Notion "Scheduling Problem 2"(`150cb27e-4930-80bf-bc26-dea5061b023f`)와 대조. 문제 정의·greedy(종료 시간 순)·교환 논증 구조 모두 일치. 원본 증명의 경우 2 부등식 슬립(서브케이스 라벨과 `T_y < S_x < S_{i+1}` 방향 모순) 및 "겹치는 일이 많아야 하나"라는 전제는 본문에서 정정·명시했다. 1편 리뷰에서 증명을 다듬은 것과 동일한 보정. 거짓 추가(hallucination) 없음. (gate_effect: info)
- [L7] `src/content/posts/scheduling-2.md:62-68` — 논증·정확성: 예시 A·C·E=3이 실제 최적(3)과 일치. 겹침 정의 $S_a<T_b \wedge S_b<T_a$ 정확. 증명 경우 분류(버림/채택, 채택 시 S 보유/미보유, $S_x\le S_{i+1}$/$S_x>S_{i+1}$) MECE, base·step 닫힘. 이상 없음. (gate_effect: info)
- [L4] SVG `public/images/scheduling/intervals.svg` — 레이블 A(1,3)·B(2,5)·C(4,7)·D(6,8)·E(8,10), 채택 A·C·E(3개), 버림 B·D가 본문 예시와 정확히 일치. 시간축·legend·각주 모두 정합. 이상 없음. (gate_effect: info)

### Coverage (이슈 없음)
- [L1] 문체(AI 신호): 줄표 사용 본문 톤은 1편과 동일 수준, 경구식 마무리 없음 — 검토 완료, 이슈 없음. (🟢/info)
- [L2] 설명 흐름·명료성: 논리 도약 없음 — 검토 완료, 이슈 없음. (🟢/info)
- [L3] 용어·어체 일관성: "고르다/채택" 혼용은 의미 충돌 없음, 평서체 통일 — 검토 완료, 이슈 없음. (🟢/info)
- [L5] 제목·description 적합성: 제목·description이 내용을 정확히 대표 — 검토 완료, 이슈 없음. (🟢/info)

### 인접 발견 (범위 밖, 참고)
- [L_link] `src/content/posts/scheduling-1.md` — 기존 `[그리디 알고리즘](/posts/greedy)` 링크도 동일하게 404다. 이번 작업에서 1편을 수정 중이므로 함께 `/blog/greedy`로 고치는 것을 권장. (gate_effect: info)

요약(전체): 🔴 0 · 🟡 2 · 🟢 7
