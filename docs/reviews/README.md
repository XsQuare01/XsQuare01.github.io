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

- Markdown: 기본 human output이다. 구조·필드 순서·공백은 `.claude/review_report.py`의 `serialize_report()`가 **단독으로** 결정한다. 손으로 형식을 맞추지 않는다.
- JSON: `--json`을 지정했을 때 stdout으로만 내보내는 machine-readable output이다. Markdown과 별도 산출물이지만 같은 필드 의미와 정렬 계약을 따른다.

### 최상위 필드 (이 순서로 출력한다)

| 필드 | 필수 | 값 |
|---|---|---|
| `schema_version` | 필수 | 항상 `review-report/v2` |
| `target` | 필수 | 리뷰 대상 slug 또는 `all` |
| `generated_at` | 필수 | 생성 날짜. 알 수 없으면 `not-recorded` |
| `strict` | 필수 | `true`, `false`, 또는 `not-recorded` |
| `sources` | 선택 | 검토한 포스트 경로 목록(쉼표 구분) |
| `migrated_from` | 선택 | 손실 있는 전환일 때만 `legacy-prose` |
| `summary` | 필수 | `🔴 n · 🟡 n · 🟢 n` — finding에서 계산한 값과 반드시 일치 |

헤더 다음에 빈 줄 하나, `Findings` 섹션 헤딩(h2), 빈 줄 하나, 그리고 finding 블록이 온다.

### finding 필드 (이 순서로, 굵게 표기 없이 출력한다)

`severity` · `source` · `rule_id` · `location` · `quote` · `message` · `recommendation` · `gate_effect`

- `severity`: `🔴`, `🟡`, `🟢` 중 하나
- `source`: `D`, `L`, `MIGRATED` 중 하나
- `rule_id`: 예: `D1`, `L7`, `MIGRATED`
- `location`: `파일:줄` 형식. 알 수 없으면 `not-recorded`
- `quote`: 판단 근거가 되는 원문. 없으면 `not-recorded`
- `message`: 문제 설명
- `recommendation`: 권장 조치
- `gate_effect`: `fail`, `warn`, `info` 중 하나

각 finding은 `### <severity> [<rule_id>] <location>` 제목으로 시작한다.

정렬은 severity(`🔴`, `🟡`, `🟢`) → source(`D`, `L`, `MIGRATED`) → rule id → file path → line 순이며 항상 안정적이다. 블록 사이 빈 줄은 하나, 파일은 개행 하나로 끝난다. 같은 입력은 항상 같은 바이트를 만든다.

### 두 가지 유효 상태

| 상태 | 만드는 명령 | finding 개수 | 검증 |
|---|---|---|---|
| scaffold | `--write-reports` | 0건 허용 | `validate_report(text, state="scaffold")` |
| complete | LLM 행 추가 후 `--finalize` | 1건 이상 필수 | `validate_report(text, state="complete")` |

`docs/reviews/`에 남는 최종 산출물은 complete 상태다. `--finalize`는 finding을 정본 순서로 재정렬하고 `summary`를 다시 계산한다. 멱등이므로 여러 번 실행해도 결과가 같다.

## 정본 강제 범위와 과거 리포트

**`2026-08-01` 이후 날짜의 리포트는 정본 계약을 반드시 지킨다.** 그 이전 리포트는 정본 serializer가 없던 시절 손으로 쓴 산물이라 형식이 최소 일곱 가지로 갈린다.

- 레거시 산문 불릿 (`- [L6] not-recorded · gate: info — …`)
- `### ` 제목 + 평문 필드 (`Findings` 섹션 헤딩 없음)
- `- 🟢 [L1] <위치>` 불릿 제목 + 들여쓴 필드
- 8열 마크다운 표
- 제목 없이 `- severity:`로 시작하는 블록
- `#### ` 제목 + 한글 라벨 (`- 심각도:`, `- 위치:`)
- 한 줄에 여러 필드 (`- severity: 🟢 · source: L · rule_id: L6`)

이 리포트들을 일괄 재작성하지 않는다. 형식을 하나라도 놓치면 finding이 조용히 사라지기 때문이다. 이미 정본을 선언한 과거 리포트는 되돌아가지 않도록 함께 검사한다.

### 마이그레이션

과거 리포트는 `python .claude/review_post.py --migrate <report.md>`로만 전환한다.

- 8개 필드가 이미 있는 리포트는 근거를 그대로 보존하고 표기만 정본화한다. `source`는 원래 값을 유지한다. 정본 제목에 자리가 없는 설명형 `###` 제목은 버리지 않고 `message` 앞으로 옮긴다.
- 산문 불릿만 있는 리포트는 `source: MIGRATED`로 전환하고, 확보할 수 없는 `location`·`quote`·`recommendation`은 `not-recorded`로 남긴다. 헤더에 `migrated_from: legacy-prose`를 붙여 손실 있는 전환임을 표시한다. 불릿에 박힌 위치와 들여쓴 하위 `- quote:`/`- message:` 줄은 되살린다.
- `generated_at`은 파일명의 날짜에서 가져온다. 없는 근거를 새로 만들어 내지 않는다.

**안전 장치:** `--migrate`는 원본이 스스로 밝힌 `요약: 🔴 n · 🟡 n · 🟢 n` 줄과 전환 결과의 총계를 대조한다. 총계가 어긋나거나 대조할 줄이 아예 없으면 **파일을 쓰지 않고 exit 2로 끝난다.** 파서가 형식 하나를 놓쳐 finding이 사라지는 일을 사람 검수에 맡기지 않기 위해서다. `요약(결정적):`처럼 일부만 센 줄은 대조 기준으로 쓰지 않는다.

마이그레이션 placeholder는 기존 리포트에 증거가 없을 때만 `not-recorded`를 쓴다. 없는 quote, 위치, 생성 시각을 새로 꾸며내지 않는다.

## Gate 계약

strict mode는 schema, 입력, deterministic 검사, LLM 비평 결과를 gate 판정에 맞춰 검증하는 모드다. 최종 판정은 두 단계가 **모두 끝난 뒤 한 번만** 내린다.

```
python .claude/review_post.py --finalize --strict <report.md>
```

- exit code `0`: 통과. `gate_effect: fail`인 finding이 없다.
- exit code `1`: 품질 실패. `gate_effect: fail`인 finding이 하나 이상 있다. 출처가 결정적 검사(`D`)든 LLM 비평(`L`)이든 같다.
- exit code `2`: infrastructure, schema, input 실패. 파싱 실패, 스키마 위반, severity와 gate_effect 불일치, LLM 비평 단계 누락을 포함한다.

`🟡` finding은 권장 사항이며 gate를 실패시키지 않는다. `🔴`만 quality gate 실패로 이어진다.

판정에 쓰는 finding 목록은 리포트를 직렬화할 때 쓴 목록과 같다. 보고서에 남은 실패 finding과 exit code가 어긋날 수 없다.

리포트는 판정 전에 먼저 저장한다. 게이트가 실패해도 근거가 남아야 하기 때문이다.

### 두 가지 strict 경로

| 명령 | 보는 것 | 쓰임 |
|---|---|---|
| `--strict <post.md>` | 결정적 검사만 | scaffold 단계의 조기 실패 검출 |
| `--finalize --strict <report.md>` | 결정적 + LLM 비평 | **최종 품질 게이트** |

앞쪽은 LLM 비평이 붙기 전에 끝나므로 최종 판정이 아니다. CI 게이트로 쓸 것은 뒤쪽이다.

### severity와 gate_effect 대응

| severity | gate_effect |
|---|---|
| `🔴` | `fail` |
| `🟡` | `warn` |
| `🟢` | `info` |

이 대응은 검증 대상이다. `🔴` finding에 `gate_effect: info`를 적어 게이트를 우회할 수 없다. 어긋나면 exit code `2`다.

### LLM 비평 coverage 누락

두 리뷰 커맨드는 문제가 없는 범주도 생략하지 말고 explicit coverage row를 남기도록 규정한다. 따라서 `source: L`인 finding이 L1–L7을 모두 덮지 않으면 비평 단계가 끝나지 않은 것이다.

strict는 이를 품질 통과로 처리하지 않고 exit code `2`로 끝낸다. LLM 단계의 인프라 실패나 출력 계약 위반이 조용히 통과하는 것을 막기 위해서다. 누락된 범주는 stderr에 나열된다.

## Frontmatter enum

`src/content/config.ts`의 현재 enum 값을 canonical 값으로 쓴다.

- category: `theory`, `cryptography`, `algorithm`, `os`, `unity`, `web-dev`
- difficulty: `입문`, `초급`, `중급`, `고급`, `심화`

## 검사 항목 요약

결정적(D): D1 깨진 굵게 · D2 줄표 남발 · D3 강조 과다 · D4 SVG 유효성 · D5 에셋 경로 · D6 내부 링크 · D7 frontmatter · D8 수식 짝 · D9 이모지 금지 · D10 callout 순서 · D11 수식 블록 줄 분리 · D12 시리즈 인접 편 링크 · D13 SVG 세로 클리핑
LLM 비평(L): L1 문체(AI 신호) · L2 설명 흐름 · L3 용어·어체 일관성 · L4 SVG↔본문 일치 · L5 제목·description 적합성 · L6 소스 자료 충실성 · L7 논증·복잡도 정확성

마이그레이션된 과거 finding은 원래 출처가 분명하지 않을 때 `MIGRATED` source를 쓴다. D/L taxonomy는 유지하며 새 구현은 기존 D/L rule id를 가능한 한 보존한다.

자세한 설계는 `docs/superpowers/specs/2026-06-03-review-post-command-design.md` 참고.

## 비고

- 리포트는 **지적·권고만** 담는다. 자동 수정은 하지 않는다(수정은 사람이 판단).
- 이 디렉터리의 파일은 산출물이므로, 필요 없으면 지워도 된다.
