---
description: 모든 블로그 포스트의 내용·문체·SVG를 리뷰
allowed-tools: Write, Edit, Bash(python:*), Bash(git diff:*), Read, Grep, Glob
---

# 블로그 포스트 리뷰 (전체)

## 작성 가이드와 책임 경계

이 리뷰는 `docs/writing-rules.md`(작성 정본 가이드)와 `AGENTS.md`(원문 보존 규칙)를 기준으로 삼는다. 상세 체크리스트는 정본 가이드에 있으므로 여기서 복제하지 않는다.

작성자는 구조·문체·provenance 분류와 검증 근거 준비를 맡는다. 리뷰어는 원문 충실성·사실 및 기술 정확성·증명 타당성을 판정한다. 작성자가 준비한 근거로 리뷰어가 독립적으로 판정하며, 작성자의 자체 인증이 리뷰 판정을 대신하지 않는다.

## 대상 선정
`src/content/posts/*.md` 전체를 대상으로 한다. 모든 포스트를 처리해야 하며, 마지막에 전체 aggregate summary를 만든다. 글 수가 많으면 결정적 검사 리포트를 먼저 보이되, LLM 비평도 전체 포스트에 대해 완료한다.

## 1단계: 결정적 검사와 저장 scaffold
모든 대상 파일 경로를 인자로 다음을 실행한다. 이 Python 단계는 결정적 검사 결과와 저장 scaffold만 담당한다.

`python .claude/review_post.py --write-reports src/content/posts/*.md`

- stdout의 결정적 검사 결과는 리포트의 결정적 검사 섹션에 그대로 포함한다.
- `--write-reports`가 만든 포스트별 scaffold를 참고하되, `/review-post-all` 최종 산출물은 `docs/reviews/<오늘 날짜>-all.md` 한 파일이다.
- Python scaffold와 LLM 비평 행을 섞어 쓰지 않는다. LLM 비평은 아래 2단계 후 Write/Edit로 전체 리뷰 파일에 명시적으로 추가한다.

## 2단계: LLM 비평

루브릭 정본은 `docs/review-rubric.md`다. **그 파일을 Read로 읽고 L1~L7을 그대로 적용한다.** 범주와 문구를 이 파일에 복제하지 않는다. 두 리뷰 커맨드가 같은 정본을 쓰므로, 같은 글은 어느 진입점으로 시작해도 같은 범주로 판정된다.

대상 포스트의 본문과, 본문이 참조하는 모든 SVG(`/images/...svg`)를 Read로 읽는다. 문제는 가능한 한 **파일:줄 위치와 인용 문장**으로 구체적으로 지적한다.

## 출력 형식
`/review-post`와 동일하다. 포스트별로 묶어, 결정적 검사 결과와 LLM 비평을 합친다. 각 finding은 `docs/reviews/README.md`의 `review-report/v2` canonical fields를 모두 포함해야 한다.

- `severity`: `🔴`, `🟡`, `🟢` 중 하나
- `source`: LLM 비평은 `L`, 결정적 검사는 `D`
- `rule_id`: LLM 비평은 `L1`부터 `L7`까지, 결정적 검사는 `D1`처럼 기록
- `location`: `파일:줄` 형식. 알 수 없으면 `not-recorded`
- `quote`: 판단 근거가 되는 원문. 없으면 `not-recorded`
- `message`: 문제 설명
- `recommendation`: 권장 조치
- `gate_effect`: `fail`, `warn`, `info` 중 하나

각 항목은 사람이 읽을 수 있게 심각도(🔴 필수 / 🟡 권장 / 🟢 참고)와 출처 코드(`[Dn]` 결정적 / `[Ln]` 비평), 그리고 `파일:줄` 위치를 함께 표시한다. 포스트별 `요약: 🔴 n · 🟡 n · 🟢 n`을 둔 뒤, 전체 aggregate summary를 마지막에 둔다.

SVG와 L1-L7 범주 중 문제가 없는 범주는 생략하지 말고, 각 포스트마다 explicit coverage row를 남긴다. 문구는 `검토 완료, 이슈 없음`을 사용하고 `rule_id`는 해당 범주(`L1`~`L7`, SVG는 `L4`)로 기록한다. 이 coverage row는 `severity: 🟢`, `source: L`, `gate_effect: info`를 쓴다.

`location`에는 그 범주를 덮은 포스트 경로(`src/content/posts/<slug>.md:<줄>`)를 반드시 적는다. 여러 포스트가 한 파일에 들어가므로, `not-recorded`로 남기면 어느 포스트를 덮었는지 알 수 없어 게이트가 그 포스트를 미비평으로 판정한다.

**자동 수정 금지. 자동 수정은 하지 않는다.** 지적과 권고만 제시한다.

## 저장 (문서화): 필수
**리뷰가 끝나면 반드시 결과를 문서화해서 `docs/reviews/`에 저장한다. 이 단계는 건너뛰지 않는다.**

리포트를 대화에 출력한 뒤, 전체 결과를 하나의 파일로 남긴다. 규약은 `docs/reviews/README.md`를 따른다.
- 저장 경로: `docs/reviews/<오늘 날짜>-all.md` (전체 리뷰는 한 파일로 합침).
- `<오늘 날짜>`와 기본 저장 scaffold는 `python .claude/review_post.py --write-reports src/content/posts/*.md`가 결정적으로 처리한다. 필요하면 `--date YYYY-MM-DD`를 함께 쓴다.
- `docs/reviews/` 디렉터리가 없으면 Python scaffold가 만든다.
- 전체 리뷰 파일은 Write/Edit로 만든다. 모든 포스트의 LLM 비평 결과, `검토 완료, 이슈 없음` coverage row, 포스트별 요약, 전체 aggregate summary를 포함한다.
- finding 필드는 `- severity: 🔴`처럼 **굵게 표기 없이** 쓴다. `- **severity**:`는 정본 형식이 아니다. 각 finding은 `### <심각도> [<rule_id>] <위치>` 제목으로 시작한다.
- 비평 행을 모두 추가한 뒤 `python .claude/review_post.py --finalize --strict docs/reviews/<오늘 날짜>-all.md`를 실행한다. 이 단계가 `summary`를 다시 계산하고 finding을 정본 순서로 재정렬한 뒤 품질 게이트를 판정한다. 건너뛰면 리포트가 미완료 상태로 남는다.
- **리뷰 종료 조건은 이 명령의 exit code를 사용자에게 보고하는 것이다.** `gate_effect: fail`인 finding이 있으면 exit 1, 어느 한 포스트라도 L1–L7 coverage가 비거나 스키마가 어긋나면 exit 2다. 자세한 계약은 `docs/reviews/README.md`의 Gate 계약 절에 있다.
- `--strict` 없는 `--finalize`는 비평이 아직 끝나지 않은 중간 저장용이다. 최종 단계에서 `--strict`를 빼면 🔴가 남아 있어도 exit 0이 나오므로 종료 판정으로 쓰지 않는다.
- 저장이 끝나면 저장된 경로와 게이트 결과를 사용자에게 알린다.
