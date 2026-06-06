# 블로그 포스트 리뷰 기록 (`docs/reviews/`)

`/review-post`·`/review-post-all` 커맨드가 생성한 리뷰 리포트를 보관하는 곳이다.

## 파일 이름 규약

- 변경분 리뷰(`/review-post`): `YYYY-MM-DD-<slug>.md` (포스트별 한 파일)
  - 예: `2026-06-03-dijkstra-2.md`
  - `<slug>`는 `src/content/posts/<slug>.md`의 파일명(확장자 제외)
- 전체 리뷰(`/review-post-all`): `YYYY-MM-DD-all.md` (한 파일로 합침)
- 같은 날 같은 대상을 다시 리뷰하면 덮어쓴다(최신 상태 유지). 이력을 남기고 싶으면 파일명 뒤에 `-2` 등을 붙인다.

## 리포트 형식

각 포스트 블록은 다음을 포함한다.

- 심각도: 🔴 필수 / 🟡 권장 / 🟢 참고
- 출처 코드: `[Dn]` 결정적 검사(`.claude/review_post.py`) / `[Ln]` LLM 비평
- 위치: `파일:줄`
- 블록 끝에 `요약: 🔴 n · 🟡 n · 🟢 n`

## 검사 항목 요약

결정적(D): D1 깨진 굵게 · D2 줄표 남발 · D3 강조 과다 · D4 SVG 유효성 · D5 에셋 경로 · D6 내부 링크 · D7 frontmatter · D8 수식 짝 · D9 이모지 금지 · D10 callout 순서 · D11 수식 블록 줄 분리 · D12 시리즈 인접 편 링크 · D13 SVG 세로 클리핑
LLM 비평(L): L1 문체(AI 신호) · L2 설명 흐름 · L3 용어·어체 일관성 · L4 SVG↔본문 일치 · L5 제목·description 적합성 · L6 소스 자료 충실성 · L7 논증·복잡도 정확성

자세한 설계는 `docs/superpowers/specs/2026-06-03-review-post-command-design.md` 참고.

## 비고

- 리포트는 **지적·권고만** 담는다. 자동 수정은 하지 않는다(수정은 사람이 판단).
- 이 디렉터리의 파일은 산출물이므로, 필요 없으면 지워도 된다.
