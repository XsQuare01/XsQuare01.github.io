# 블로그 포스트 리뷰 기록 (`docs/reviews/`)

`/review-post`·`/review-post-all` 커맨드가 생성한 리뷰 리포트를 보관하는 곳이다.

현재 리포트 스키마는 `review-report/v2`이다. 이 문서는 사람이 읽는 Markdown 리포트와 `--json` 기계 출력이 함께 따라야 할 기준 계약이다.

## 파일 이름 규약

- 변경분 리뷰(`/review-post`): `YYYY-MM-DD-<slug>.md` (포스트별 한 파일)
  - 예: `2026-06-03-dijkstra-2.md`
  - `<slug>`는 `src/content/posts/<slug>.md`의 파일명(확장자 제외)
- 전체 리뷰(`/review-post-all`): `YYYY-MM-DD-all.md` (한 파일로 합침)
- 같은 날짜와 같은 slug의 리포트는 항상 결정적으로 overwrite 한다. 파일명 suffix는 만들지 않는다.

## 리포트 형식

각 포스트 블록은 다음을 포함한다.

- 심각도: 🔴 필수 / 🟡 권장 / 🟢 참고
- 출처 코드: `[Dn]` 결정적 검사(`.claude/review_post.py`) / `[Ln]` LLM 비평
- 위치: `파일:줄`
- 블록 끝에 `요약: 🔴 n · 🟡 n · 🟢 n`

리뷰 산출물은 포스트 작성 가이드의 이모지 금지 규칙에서 예외다. 리포트는 판독성과 gate 판정을 위해 `🔴/🟡/🟢`를 사용할 수 있다.

## `review-report/v2` 스키마

리포트는 다음 역할을 나눈다.

- Markdown: 기본 human output이다. 사람이 읽는 리뷰 기록이며 JSON을 Markdown 안에 넣지 않는다.
- JSON: `--json`을 지정했을 때 stdout으로만 내보내는 machine-readable output이다.

상위 report 필드는 다음 값을 갖는다.

- `schema_version`: 항상 `review-report/v2`
- `target`: 리뷰 대상 slug 또는 `all`
- `generated_at`: 리포트 생성 시각. 알 수 없으면 `not-recorded`
- `strict`: strict mode 적용 여부
- `summary`: 심각도별 집계
- `findings`: finding 목록

각 finding은 다음 필드를 반드시 포함한다.

- `severity`: `🔴`, `🟡`, `🟢` 중 하나
- `source`: `D`, `L`, `MIGRATED` 중 하나
- `rule_id`: 예: `D1`, `L7`, `MIGRATED`
- `location`: `파일:줄` 형식. 알 수 없으면 `not-recorded`
- `quote`: 판단 근거가 되는 원문. 과거 리포트 마이그레이션에서 근거가 없으면 `not-recorded`
- `message`: 문제 설명
- `recommendation`: 권장 조치
- `gate_effect`: `fail`, `warn`, `info` 중 하나

finding 정렬은 항상 안정적이어야 한다. 정렬 순서는 severity(`🔴`, `🟡`, `🟢`) 다음 source(`D`, `L`, `MIGRATED`) 다음 rule id 다음 file path 다음 line이다.

마이그레이션 placeholder는 기존 리포트에 증거가 없을 때만 `not-recorded`를 쓴다. 없는 quote, 위치, 생성 시각을 새로 꾸며내지 않는다.

## Gate 계약

strict mode는 schema, 입력, deterministic 검사, LLM 비평 결과를 gate 판정에 맞춰 검증하는 모드다.

- exit code `0`: 통과
- exit code `1`: `🔴` finding 때문에 quality gate 실패
- exit code `2`: infrastructure, schema, input 실패

`🟡` finding은 권장 사항이며 gate를 실패시키지 않는다. `🔴`만 quality gate 실패로 이어진다.

## Frontmatter enum

`src/content/config.ts`의 현재 enum 값을 canonical 값으로 쓴다.

- category: `theory`, `cryptography`, `algorithm`, `os`, `unity`, `web-dev`
- difficulty: `입문`, `중급`, `심화`

## 검사 항목 요약

결정적(D): D1 깨진 굵게 · D2 줄표 남발 · D3 강조 과다 · D4 SVG 유효성 · D5 에셋 경로 · D6 내부 링크 · D7 frontmatter · D8 수식 짝 · D9 이모지 금지 · D10 callout 순서 · D11 수식 블록 줄 분리 · D12 시리즈 인접 편 링크 · D13 SVG 세로 클리핑
LLM 비평(L): L1 문체(AI 신호) · L2 설명 흐름 · L3 용어·어체 일관성 · L4 SVG↔본문 일치 · L5 제목·description 적합성 · L6 소스 자료 충실성 · L7 논증·복잡도 정확성

마이그레이션된 과거 finding은 원래 출처가 분명하지 않을 때 `MIGRATED` source를 쓴다. D/L taxonomy는 유지하며 새 구현은 기존 D/L rule id를 가능한 한 보존한다.

자세한 설계는 `docs/superpowers/specs/2026-06-03-review-post-command-design.md` 참고.

## 비고

- 리포트는 **지적·권고만** 담는다. 자동 수정은 하지 않는다(수정은 사람이 판단).
- 이 디렉터리의 파일은 산출물이므로, 필요 없으면 지워도 된다.
