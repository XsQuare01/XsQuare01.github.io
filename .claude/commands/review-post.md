---
description: main 대비 변경된 블로그 포스트의 내용·문체·SVG를 리뷰 (인자로 slug 지정 가능)
allowed-tools: Write, Edit, Bash(python:*), Bash(git diff:*), Read, Grep, Glob
---

# 블로그 포스트 리뷰 (변경분)

## 작성 가이드와 책임 경계

이 리뷰는 `docs/writing-rules.md`(작성 정본 가이드)와 `AGENTS.md`(원문 보존 규칙)를 기준으로 삼는다. 상세 체크리스트는 정본 가이드에 있으므로 여기서 복제하지 않는다.

작성자는 구조·문체·provenance 분류와 검증 근거 준비를 맡는다. 리뷰어는 원문 충실성·사실 및 기술 정확성·증명 타당성을 판정한다. 작성자가 준비한 근거로 리뷰어가 독립적으로 판정하며, 작성자의 자체 인증이 리뷰 판정을 대신하지 않는다.

## 대상 선정
- 인자(`$ARGUMENTS`)가 있으면 `src/content/posts/<인자>.md` 하나만 대상으로 한다.
- 인자가 없으면 아래 두 결과를 합쳐 `src/content/posts/*.md`만 추린다.
  - `git diff --name-only main...HEAD`
  - `git diff --name-only`  (워킹트리 변경분)
- 대상이 하나도 없으면 "main 대비 변경된 포스트가 없습니다"라고 알리고 종료한다.

## 1단계: 결정적 검사와 저장 scaffold
대상 파일 경로들을 인자로 다음을 실행한다. 이 Python 단계는 결정적 검사 결과와 저장 scaffold만 담당한다.

`python .claude/review_post.py --write-reports <대상 파일들>`

- stdout의 결정적 검사 결과는 사용자에게 보고한다. **리포트에 `## 결정적 검사` 같은 산문 섹션을 만들지 않는다.** 발견 사항은 scaffold가 이미 `D` 출처 finding 행으로 담고 있고, 정본 형식에는 그 밖의 섹션이 없다. 만들면 `--finalize`가 exit 2로 거부한다.
- `--write-reports`가 만든 `docs/reviews/<오늘 날짜>-<slug>.md` 파일은 이후 LLM 비평 행을 추가할 저장 대상이다.
- Python scaffold와 LLM 비평 행을 섞어 쓰지 않는다. LLM 비평은 아래 2단계 후 Write/Edit로 명시적으로 추가한다.
- scaffold는 정본 헤더(`schema_version`·`target`·`generated_at`·`strict`·`sources`·`summary`)와 `## Findings` 섹션을 이미 포함한다. 헤더를 손으로 고치지 않는다.

## 2단계: LLM 비평

루브릭 정본은 `docs/review-rubric.md`다. **그 파일을 Read로 읽고 L1~L7을 그대로 적용한다.** 범주와 문구를 이 파일에 복제하지 않는다. 두 리뷰 커맨드가 같은 정본을 쓰므로, 같은 글은 어느 진입점으로 시작해도 같은 범주로 판정된다.

대상 포스트의 본문과, 본문이 참조하는 모든 SVG(`/images/...svg`)를 Read로 읽는다. 문제는 가능한 한 **파일:줄 위치와 인용 문장**으로 구체적으로 지적한다.

## 출력 형식
포스트별로 묶어, 결정적 검사 결과와 LLM 비평을 합친다. 각 finding은 `docs/reviews/README.md`의 `review-report/v2` canonical fields를 모두 포함해야 한다.

- `severity`: `🔴`, `🟡`, `🟢` 중 하나
- `source`: LLM 비평은 `L`, 결정적 검사는 `D`
- `rule_id`: LLM 비평은 `L1`부터 `L7`까지, 결정적 검사는 `D1`처럼 기록
- `location`: `파일:줄` 형식. 알 수 없으면 `not-recorded`
- `quote`: 판단 근거가 되는 원문. 없으면 `not-recorded`
- `message`: 문제 설명
- `recommendation`: 권장 조치
- `gate_effect`: `fail`, `warn`, `info` 중 하나

각 항목은 사람이 읽을 수 있게 심각도(🔴 필수 / 🟡 권장 / 🟢 참고)와 출처 코드(`[Dn]` 결정적 / `[Ln]` 비평), 그리고 `파일:줄` 위치를 함께 표시한다. 마지막에 `요약: 🔴 n · 🟡 n · 🟢 n`을 둔다.

SVG와 L1-L7 범주 중 문제가 없는 범주는 생략하지 말고, 각 포스트마다 explicit coverage row를 남긴다. 문구는 `검토 완료, 이슈 없음`을 사용하고 `rule_id`는 해당 범주(`L1`~`L7`, SVG는 `L4`)로 기록한다. 이 coverage row는 `severity: 🟢`, `source: L`, `gate_effect: info`를 쓴다.

**자동 수정 금지. 자동 수정은 하지 않는다.** 지적과 권고만 제시한다.

## 저장 (문서화): 필수
**리뷰가 끝나면 반드시 결과를 문서화해서 `docs/reviews/`에 저장한다. 이 단계는 건너뛰지 않는다.**

리포트를 대화에 출력한 뒤, 같은 내용을 파일로 남긴다. 규약은 `docs/reviews/README.md`를 따른다.
- 저장 경로: `docs/reviews/<오늘 날짜>-<slug>.md` (포스트별로 한 파일).
- `<오늘 날짜>`와 파일 생성은 `python .claude/review_post.py --write-reports <대상 파일들>`가 결정적으로 처리한다. 필요하면 `--date YYYY-MM-DD`를 함께 쓴다.
- `<slug>`는 리뷰한 포스트 파일명(확장자 제외).
- `docs/reviews/` 디렉터리가 없으면 Python scaffold가 만든다.
- LLM 비평 결과와 `검토 완료, 이슈 없음` coverage row는 scaffold 생성 뒤 Write/Edit로 같은 파일에 추가한다.
- finding 필드는 `- severity: 🔴`처럼 **굵게 표기 없이** 쓴다. `- **severity**:`는 정본 형식이 아니다. 각 finding은 `### <심각도> [<rule_id>] <위치>` 제목으로 시작한다.
- 비평 행을 모두 추가한 뒤 `python .claude/review_post.py --finalize --strict docs/reviews/<오늘 날짜>-<slug>.md`를 실행한다. 이 단계가 `summary`를 다시 계산하고 finding을 정본 순서로 재정렬한 뒤 품질 게이트를 판정한다. 건너뛰면 리포트가 미완료 상태로 남는다.
- **리뷰 종료 조건은 이 명령의 exit code를 사용자에게 보고하는 것이다.** `gate_effect: fail`인 finding이 있으면 exit 1, L1–L7 coverage가 비거나 스키마가 어긋나면 exit 2다. 자세한 계약은 `docs/reviews/README.md`의 Gate 계약 절에 있다.
- `--strict` 없는 `--finalize`는 비평이 아직 끝나지 않은 중간 저장용이다. 최종 단계에서 `--strict`를 빼면 🔴가 남아 있어도 exit 0이 나오므로 종료 판정으로 쓰지 않는다.
- 저장이 끝나면 저장된 경로와 게이트 결과를 사용자에게 알린다.
- 지적을 나중에 고쳤다면 finding 행을 고쳐 쓰지 않는다. 원래 판정은 그 시점의 근거로 남기고, 무엇을 어떻게 처리했는지는 리포트 끝 감사 섹션(`## 후속 처리`)에 적는다. 규약은 `docs/reviews/README.md`의 감사 섹션 절에 있다.
