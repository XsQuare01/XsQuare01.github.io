---
description: 모든 블로그 포스트의 내용·문체·SVG를 리뷰
allowed-tools: Bash(python .claude/review_post.py:*), Read, Grep, Glob
---

# 블로그 포스트 리뷰 (전체)

## 대상 선정
`src/content/posts/*.md` 전체를 대상으로 한다. 글 수가 많으면 결정적 검사 리포트를 먼저 보이고, LLM 비평은 🔴/🟡가 있는 포스트부터 우선 다룬다.

## 1단계 — 결정적 검사
모든 대상 파일 경로를 인자로 다음을 실행하고, 출력을 리포트에 그대로 포함한다.

`python .claude/review_post.py src/content/posts/*.md`

## 2단계 — LLM 비평
각 포스트와 참조 SVG를 읽고, `/review-post` 커맨드와 **동일한 루브릭(L1~L5)** 으로 점검한다. (문체 AI 신호, 설명 흐름, 용어·어체 일관성, SVG↔본문 일치, 제목·description 적합성)

## 출력 형식
`/review-post`와 동일하다. 포스트별로 심각도·출처 코드·위치를 붙이고, 전체 요약을 마지막에 둔다. 자동 수정은 하지 않는다.

## 저장 (문서화)
리포트를 대화에 출력한 뒤, 전체 결과를 하나의 파일로 남긴다. 규약은 `docs/reviews/README.md`를 따른다.
- 저장 경로: `docs/reviews/<오늘 날짜>-all.md` (전체 리뷰는 한 파일로 합침).
- `<오늘 날짜>`는 `date +%Y-%m-%d`로 확인한다. `docs/reviews/` 디렉터리가 없으면 만든다.
- 저장이 끝나면 저장된 경로를 사용자에게 알린다.
