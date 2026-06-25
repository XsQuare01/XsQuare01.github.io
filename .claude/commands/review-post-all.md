---
description: 모든 블로그 포스트의 내용·문체·SVG를 리뷰
allowed-tools: Write, Edit, Bash(python:*), Bash(git diff:*), Read, Grep, Glob
---

# 블로그 포스트 리뷰 (전체)

## 대상 선정
`src/content/posts/*.md` 전체를 대상으로 한다. 모든 포스트를 처리해야 하며, 마지막에 전체 aggregate summary를 만든다. 글 수가 많으면 결정적 검사 리포트를 먼저 보이되, LLM 비평도 전체 포스트에 대해 완료한다.

## 1단계: 결정적 검사와 저장 scaffold
모든 대상 파일 경로를 인자로 다음을 실행한다. 이 Python 단계는 결정적 검사 결과와 저장 scaffold만 담당한다.

`python .claude/review_post.py --write-reports src/content/posts/*.md`

- stdout의 결정적 검사 결과는 리포트의 결정적 검사 섹션에 그대로 포함한다.
- `--write-reports`가 만든 포스트별 scaffold를 참고하되, `/review-post-all` 최종 산출물은 `docs/reviews/<오늘 날짜>-all.md` 한 파일이다.
- Python scaffold와 LLM 비평 행을 섞어 쓰지 않는다. LLM 비평은 아래 2단계 후 Write/Edit로 전체 리뷰 파일에 명시적으로 추가한다.

## 2단계: LLM 비평
각 포스트와 참조 SVG를 읽고 아래의 **동일한 루브릭(L1~L7)** 으로 점검한다.

- **L1 문체(AI 신호):** 줄표(—) 남발, 경구식 섹션 마무리, 과한 비유·수사("형제처럼", "두 얼굴" 류), 대칭 문장 반복, 과한 굵게/기울임. 줄표는 마침표·접속사로, 비유는 평이하게 고치라고 제안. 어체는 ~다 평서체 유지.
- **L2 설명 흐름·명료성:** 논리 도약, 빠진 전제, 너무 길어 끊어야 할 문장.
- **L3 용어·어체 일관성:** 같은 개념을 다른 말로 섞어 쓰는지(예: 노드/정점, 엣지/간선), 어체 통일.
- **L4 SVG ↔ 본문 일치:** SVG의 레이블·수치·캡션이 본문 예제/주장과 맞는지(예: 그래프 가중치, 거리 값).
- **L5 제목·description 적합성:** 제목과 frontmatter description이 실제 내용을 잘 대표하는지.
- **L6 소스 자료 충실성:** 이 블로그 포스트는 사용자의 **노션** 자료를 바탕으로 쓴다(`CLAUDE.md` 참조). 가능하면 해당 노션 페이지를 `notion-search`→`notion-fetch`로 가져와 대조한다. 원본에 **없는 내용을 자의로 추가**(hallucination)했거나, 원본의 핵심을 **누락**했는지 점검한다. 원본을 구하지 못하면 그 사실을 리포트에 명시한다.
- **L7 논증·복잡도 정확성:** 수학·알고리즘 주장이 실제로 옳은지 따진다. ① 본문 예시가 주장한 값으로 실제 계산되는가(예: 총 이익, 거리), ② 시간/공간 복잡도(Big-O) 주장이 알고리즘과 맞는가, ③ 증명의 경우 분류가 **빠짐·겹침 없이(MECE)** 완결적인가, 불변식의 base·step이 닫히는가.

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

**자동 수정 금지. 자동 수정은 하지 않는다.** 지적과 권고만 제시한다.

## 저장 (문서화): 필수
**리뷰가 끝나면 반드시 결과를 문서화해서 `docs/reviews/`에 저장한다. 이 단계는 건너뛰지 않는다.**

리포트를 대화에 출력한 뒤, 전체 결과를 하나의 파일로 남긴다. 규약은 `docs/reviews/README.md`를 따른다.
- 저장 경로: `docs/reviews/<오늘 날짜>-all.md` (전체 리뷰는 한 파일로 합침).
- `<오늘 날짜>`와 기본 저장 scaffold는 `python .claude/review_post.py --write-reports src/content/posts/*.md`가 결정적으로 처리한다. 필요하면 `--date YYYY-MM-DD`를 함께 쓴다.
- `docs/reviews/` 디렉터리가 없으면 Python scaffold가 만든다.
- 전체 리뷰 파일은 Write/Edit로 만든다. 모든 포스트의 LLM 비평 결과, `검토 완료, 이슈 없음` coverage row, 포스트별 요약, 전체 aggregate summary를 포함한다.
- 저장이 끝나면 저장된 경로를 사용자에게 알린다.
