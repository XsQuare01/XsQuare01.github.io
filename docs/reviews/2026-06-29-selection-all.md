# 리뷰 리포트 — 선택 문제 시리즈 3편 (2026-06-29)

대상: `selection.md`(메인), `selection-average.md`(추가설명 A), `selection-why-five.md`(추가설명 B) + 참조 SVG 4종
방식: 결정적 검사(`review_post.py`) + LLM 비평(L1~L7) + 노션 원문(L6) 대조
브랜치: `feat/post-selection`. 모든 지적은 동일 브랜치에서 반영 완료.

## selection.md

| severity | source | rule_id | location | message | 조치 |
|---|---|---|---|---|---|
| 🔴 | D | D1 | selection.md:10 | 깨진 굵게 `**선택 문제(selection problem)**다` (닫는 `**` 뒤 조사) | 굵게 범위를 "선택 문제"로 한정, 괄호·조사 밖으로 (fab71ef) |
| 🔴 | L | L7 | selection.md:110 | approximate median 점화식 `Q(n/4)+Q(3n/4)`를 "0.7n→3/4n 상한"으로 잘못 정당화 | `Q(n)=n+Q(0.3n)+Q(0.7n)`로 교체, "양쪽 모두 n의 상수배 → 깊이 O(log n)" 논거로 재서술 (fab71ef) |
| 🟡 | D | D2 | selection.md | 줄표(—) 18회 > 임계 16 | 문체 수정으로 14회로 감소 (fab71ef) |
| 🟡 | L | L1 | selection.md:10 | `봉인된다` 과한 수사 | `O(n log n)으로 묶인다`로 평이화 (fab71ef) |
| 🟡 | L | L1 | selection.md:77,85 | `**최선** —`/`**최악** —` 대칭 줄표 패턴 | 술어로 연결 (fab71ef) |
| 🟡 | L | L1 | selection.md:144 | `— 즉` 이중 전환 | 마침표로 분리 (fab71ef) |
| 🟡 | L | L3 | selection.md | `퀵소트`/`퀵 정렬` 혼용 | `퀵 정렬`로 통일 (fab71ef) |
| 🟢 | L | L2 | selection.md | 설명 흐름·명료성 | 검토 완료, 이슈 없음 |
| 🟢 | L | L4 | selection.md (SVG 3종) | SVG↔본문 수치·레이블 일치 | 검토 완료, 이슈 없음 |
| 🟢 | L | L5 | selection.md:2-4 | 제목·description 적합성 | 검토 완료, 이슈 없음 |

요약: 🔴 2 · 🟡 5 · 🟢 3 — 전부 반영

## selection-average.md

| severity | source | rule_id | location | message | 조치 |
|---|---|---|---|---|---|
| 🟡 | L | L5 | selection-average.md:82 | `median of medians` 링크가 `selection-why-five`를 가리킴(본체는 메인 글) | `/blog/selection`으로 수정 (fab71ef) |
| 🟡 | L | L2 | selection-average.md:57-60 | "항 수×평균=상한" 논거 부정확 | 등차수열 공식 + 명시적 ≤로 교체 (fab71ef) |
| 🟡 | L | L2 | selection-average.md:32 | 짝수 n 경계에서 max 우세 판별 설명 오류(공식은 맞음) | 경계 표현 정정 (fab71ef) |
| 🟡 | D/L | — | selection-average.md | quicksort 평균 섹션 앵커 `#평균은-왜-on-log-n인가` 깨짐(실제 id는 KaTeX로 변형됨) | 프래그먼트 제거, `/blog/quicksort`로 (fab71ef) |
| 🟡 | L | L3 | selection-average.md | `퀵소트` 표기 | `퀵 정렬`로 통일 (fab71ef, 47726f5) |
| 🟢 | L | L1/L6/L7 | selection-average.md | 문체·소스 충실성·E(n)≤4n 유도 정확성 | 검토 완료, 이슈 없음 |

요약: 🟡 5 · 🟢 3 — 전부 반영

## selection-why-five.md

| severity | source | rule_id | location | message | 조치 |
|---|---|---|---|---|---|
| 🟢 | L | L4 | group-size-compare.svg | g=7 비율 합 `≈0.86` vs 본문 `0.857` | SVG를 `≈0.857`로 통일 (fab71ef) |
| 🟢 | L | L1/L2/L3/L5/L6/L7 | selection-why-five.md | 문체·흐름·용어·제목·소스·논증(α+β<1 조건) | 검토 완료, 이슈 없음 |

요약: 🟢 7 — SVG 수치 통일 반영

## 추가 요구 반영 (사용자 지시)

- 추가 설명 글의 date는 메인 글보다 앞설 수 없음 → `selection.md` 09:00:00 < `selection-average.md` 09:01:00 < `selection-why-five.md` 09:02:00 (fab71ef)
- 참고: 블로그 목록은 날짜 내림차순 정렬(`b - a`)이므로, 늦은 시각의 추가설명이 목록 상단에 먼저 노출될 수 있음(메타데이터 선후 규칙은 지시대로 충족).

## Aggregate

| 파일 | 🔴 | 🟡 | 🟢 |
|---|---|---|---|
| selection.md | 2 | 5 | 3 |
| selection-average.md | 0 | 5 | 3 |
| selection-why-five.md | 0 | 0 | 7 |
| **합계** | **2** | **10** | **13** |

🔴/🟡 전 항목 반영 완료, 빌드 통과(89 pages), 줄표 임계 이하, 상호링크·날짜 순서 검증 완료.
