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

필드 값은 **한 줄에 담는다.** 값이 다음 줄로 이어진 리포트는 정본화하지 않고 exit code `2`로 끝난다. 이어진 줄을 조용히 버리면 근거가 사라지고, 말없이 이어 붙이면 원문과 다른 바이트가 되기 때문이다. 값을 한 줄로 합친 뒤 다시 실행한다.

값 전체를 감싼 백틱은 **한 쌍뿐일 때만** 벗긴다(`` `a.md:73` `` → `a.md:73`). 표기 정규화이므로 한 번만 일어나고 그 뒤로는 값을 손대지 않는다. `` `A` / `B` ``처럼 code span이 여러 개면 벗기지 않는다. 양 끝만 벗기면 남은 백틱이 가운데를 감싸 인용이 반대로 렌더된다.

### 감사 섹션 — 지적을 어떻게 처리했는지

finding 뒤에 `## 후속 처리`, `## 반영 상태`, `## 반영 결과` 중 하나로 시작하는 섹션을 둘 수 있다. 어느 지적을 어느 커밋에서 고쳤는지, 재검증을 했는지가 여기 남는다. 정본화는 이 섹션을 **원문 그대로** 옮긴다.

- 위치는 파일 맨 끝이다. 이 섹션부터는 finding으로 읽지 않는다. 안에 쓰인 `- 🟡 [L7] …` 불릿이 finding 제목과 같은 꼴이라, 읽으면 필드 없는 finding이 유령처럼 생긴다.
- 그래서 감사 섹션 **뒤에 finding을 두면 안 된다.** 두면 판정에서 빠지므로 exit code `2`다.
- finding에 자리가 없다는 이유로 이 기록을 버리면, 이미 해결한 지적이 미해결로 남아 리포트가 현재 상태를 반대로 전달한다.

`--migrate`는 위 세 제목과 `결정적 검사`·`LLM 비평`·`Findings` 밖의 `##` 섹션을 만나면 **전환하지 않는다.** 정본 모델에 담을 자리가 없어 사라질 내용이기 때문이다. 감사 섹션으로 옮기거나 손으로 정본화한다.

### 두 가지 유효 상태

| 상태 | 만드는 명령 | finding 개수 | 검증 |
|---|---|---|---|
| scaffold | `--write-reports` | 0건 허용 | `validate_report(text, state="scaffold")` |
| complete | LLM 행 추가 후 `--finalize` | 1건 이상 필수 | `validate_report(text, state="complete")` |

상태 이름은 이 둘뿐이다. 다른 값을 주면 `ValueError`로 즉시 터진다. 오타를 검증 오류 목록에 담으면 호출자가 그것을 데이터 결함으로 읽고 넘어가, 검사하지 않은 리포트가 검사한 것처럼 통과한다.

`schema_version` 선언은 **첫 줄**이어야 한다. 아래쪽에 묻힌 선언은 리포트를 여는 사람도, 첫 줄로 정본 여부를 가리는 게이트도 보지 못한다. `strict` 값은 `true`·`false`·`not-recorded` 셋뿐이다.

정본 형식이 담는 섹션은 `Findings` 섹션 헤딩(h2)과 감사 섹션뿐이다. **`--finalize`는 그 밖의 h1·h2 섹션을 만나면 쓰지 않고 exit code `2`로 끝난다.** `## 결정적 검사`, `## LLM 비평`, `# 리뷰 리포트` 같은 진행용 제목도 마찬가지다. 결정적 검사 결과는 이미 `D` 출처 finding 행에 들어 있으므로 산문 섹션을 따로 만들지 않는다.

`--migrate`만 진행용 제목을 허용한다. 과거 리포트가 그 형식으로 쓰여 있어서, 거부하면 전환 자체를 할 수 없다. **정본화와 전환의 허용 범위를 같게 두면 안 된다.** 같게 두면 진행용 제목 아래 적은 산문이 정본화에서 성공 코드와 함께 사라진다.

`--finalize`는 정본화가 **고치지 않는** 입력 결함을 쓰기 전에 거부한다. `strict` 값과 선언 위치가 그렇다. 요약 갱신·정렬·공백은 정본화가 맡아 고치는 항목이라 거부 대상이 아니다. `--strict`는 `strict` 값을 덮어쓰므로, 원본을 먼저 보지 않으면 잘못된 값이 지워진 채 통과한다.

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

**총계만으로는 부족하다.** 개수가 같아도 인용이 잘리거나 감사 기록이 빠지면 리포트는 다른 사실을 말한다. 그래서 전환 결과를 되읽어 **finding의 8개 필드 값과 감사 섹션을 하나씩 원본과 대조한다.** 하나라도 다르면 무손실을 확인할 수 없으므로 쓰지 않는다. 비교 기준은 직렬화에 넘긴 값이며, 없는 근거를 `not-recorded`로 채우는 것은 손실이 아니라 표시이므로 걸리지 않는다.

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

`--finalize`와 `--migrate`는 함께 쓸 수 없다. 함께 주면 파일을 쓰기 전에 exit code `2`로 끝난다. 조용히 한쪽을 고르면 `--migrate`가 총계 불일치로 거부한 입력을 `--finalize`가 덮어써 안전 장치가 무력해지기 때문이다.

### 검증 → 저장 → 판정

순서는 이 셋으로 고정한다.

1. **검증(저장 전)**: 원본 finding의 8개 필드 존재와 제목↔필드 일치를 본다. 정본화는 빠진 필드를 `not-recorded`로 채우고 제목을 필드 값으로 다시 만들기 때문에, 저장한 뒤에 보면 원본의 결함이 이미 덮인 뒤다. `### 🔴 [L7]` 제목에 `severity: 🟢` 필드가 붙은 리포트는 정본화하면 빨간 제목이 사라진 채 통과한다. 어긋나면 파일을 쓰지 않고 exit code `2`다.
2. **저장**: 정본화한 내용을 쓴다. `--strict`를 붙였다고 정본화를 건너뛰지 않는다.
3. **판정**: coverage 누락과 `gate_effect: fail`을 본다. 게이트가 실패해도 근거가 남아야 하므로 판정은 저장 뒤에 한다.

### 저장은 원자적으로 — 파일별 원자성

리포트를 덮어쓰는 경로(`--finalize`, `--migrate`, `--write-reports`)는 대상 파일에 직접 쓰지 않는다. 같은 디렉터리의 **임시 파일**에 UTF-8로 쓰고 flush·fsync한 뒤, 되읽어 내용을 대조하고 나서 `os.replace()`로 교체한다.

대상 파일을 먼저 비우고 쓰면 디스크 부족·권한 오류·프로세스 중단이 쓰는 도중에 일어날 때 원본 대신 잘린 파일이 남는다. 리포트는 리뷰 근거의 유일한 기록이므로 부분 파일은 원본보다 나쁘다. 실패하면 임시 파일을 지우고 대상은 **byte-identical**하게 남긴다.

줄 끝은 기존 파일 스타일을 따른다. 저장소 리포트는 LF와 CRLF가 섞여 있어서, 플랫폼 기본으로 쓰면 정본화만 해도 파일 전체가 바뀐 것처럼 보인다. 근거를 읽는 사람에게 diff는 신호여야 한다.

**정책은 파일별 원자성이다. batch all-or-nothing이 아니다.** 리포트 여러 개를 한 번에 처리하면 파일마다 독립적으로 교체되므로, 뒤 파일이 실패해도 이미 교체된 앞 파일은 그대로 남는다. 리포트는 포스트별로 독립된 산출물이고 `--finalize`·`--migrate`가 멱등이라 실패한 파일만 다시 돌리면 복구된다. 전체 되돌리기를 하려면 모든 원본의 사본을 따로 들고 있다가 실패 시 복원해야 하는데, 그 복원 자체가 다시 실패할 수 있어 잃을 것이 더 많다. 실패한 파일 경로는 stderr에 남고 exit code는 `2`다.

### 저장소 게이트 — CI가 부르는 진입점

`--finalize --strict`는 리포트 하나를 정본화하며 판정한다. CI는 리포트 하나가 아니라 저장소 전체를 봐야 하고, 남의 파일을 고쳐서도 안 된다. 그 자리가 `--gate`다.

```
python .claude/review_post.py --gate [--reports-dir docs/reviews]
npm run review:gate
```

- **읽기 전용이다.** 어떤 리포트도 고치지 않는다. `--finalize`·`--migrate`와 함께 쓰면 exit code `2`다.
- **판정 단위는 대상별 최신 리포트 하나다.** 리포트는 날짜가 박힌 스냅샷이라 글을 고쳐도 과거 파일의 🔴은 그대로 남는다. 전체 파일을 판정하면 과거 리포트를 고치지 않는 한 영원히 초록이 될 수 없으므로, 대상마다 가장 최근 날짜의 리포트만 본다. 과거 스냅샷은 이력으로 남긴다.
- **정본화 여부도 검사한다.** 파일 내용이 재직렬화 결과와 한 바이트라도 다르면 `--finalize --strict`를 돌리지 않은 것으로 보고 exit code `2`다. 요약과 판정이 어긋난 리포트를 통과시키지 않기 위해서다.
- **면제분을 조용히 넘기지 않는다.** 아래 면제 규칙에 걸린 리포트는 개수와 파일명을 stdout에 나열한다.
- **검사한 것이 없으면 통과가 아니다.** `--reports-dir`가 가리키는 디렉터리가 없거나 날짜가 붙은 리포트가 하나도 없으면 exit code `2`다. 0개 검사를 통과로 돌려주면 경로 오타나 디렉터리 이동이 "검사했고 문제없다"로 읽힌다. 리포트가 모두 면제 대상인 것은 정상이므로 통과다.

모르는 옵션은 경로가 아니라 오류다. 어떤 파일도 읽거나 쓰기 전에 exit code `2`로 끝난다. 오타가 조용히 기능을 끄면 안 된다. `--finalize --strcit <report.md>`는 예전에 읽기 실패 하나만 남기고 나머지 리포트를 판정 없이 정본화했다.

exit code는 `--finalize --strict`와 같다. `0` 통과, `1` 🔴 남음, `2` 스키마·정본화·coverage 실패.

이 게이트는 `.github/workflows/review-gate.yml`에서 PR과 main push마다, `deploy.yml`에서는 빌드 **전에** 돈다. 두 곳에 배선한 이유는 역할이 다르기 때문이다. 앞쪽은 머지를 막고, 뒤쪽은 배포를 막는다.

#### 면제 규칙

| 리포트 | coverage 요구 | 🔴 판정 |
|---|---|---|
| `2026-08-01` 이후 생성분 | 강제 | 강제 |
| 그 이전이지만 `schema_version: review-report/v2`를 선언한 리포트 | 강제 | 강제 |
| 그 이전의 비정본 리포트 | 면제 | 면제 |
| `migrated_from`이 붙은 리포트 | **면제** | 강제 |

기준일 이전 비정본 리포트를 면제하는 이유는 serializer가 없던 시절 손으로 쓴 산물이라 형식이 여러 가지로 갈리고, 일괄 재작성이 근거 손실을 부르기 때문이다(#84). 정본을 한 번 선언한 리포트는 날짜와 무관하게 강제해 되돌아가지 못하게 한다.

`migrated_from`이 붙은 리포트에서 coverage만 면제하는 이유는 레거시 산문을 옮긴 결과라 `source: MIGRATED` finding만 있고 L 비평 행이 애초에 없기 때문이다. 여기에 L1–L7을 요구하면 과거 글 전체의 재리뷰를 강제하게 된다. 🔴 판정은 면제하지 않는다.

L6 상태 규약은 2026-08-18 이후 생성된 리포트에 적용한다. 그 이전 리포트의 L6 행을 고쳐 쓰지 않는다. 판정은 그 시점의 근거로 남기며, 소급 수정은 위 「감사 섹션」 규약과 어긋난다.

### 두 가지 strict 경로

| 명령 | 보는 것 | 쓰임 |
|---|---|---|
| `--strict <post.md>` | 결정적 검사만 | scaffold 단계의 조기 실패 검출 |
| `--finalize --strict <report.md>` | 결정적 + LLM 비평 | 리포트 하나의 최종 판정 |
| `--gate` | 대상별 최신 리포트 전부 | **CI 게이트** |

앞쪽은 LLM 비평이 붙기 전에 끝나므로 최종 판정이 아니다. CI 게이트로 쓸 것은 뒤쪽이다.

헤더의 `strict: true`는 **실행 모드 표시이지 게이트 결과가 아니다.** 두 경로 모두 같은 값을 남기고, 게이트가 실패한 리포트에도 붙는다. 판정 결과는 exit code와 stderr로만 읽는다.

### severity와 gate_effect 대응

| severity | gate_effect |
|---|---|
| `🔴` | `fail` |
| `🟡` | `warn` |
| `🟢` | `info` |

이 대응은 검증 대상이다. `🔴` finding에 `gate_effect: info`를 적어 게이트를 우회할 수 없다. 어긋나면 exit code `2`다.

#### L6 상태가 severity를 정한다

위 3단 매핑은 그대로다. L6만 판정 상태가 severity를 먼저 정하고, 그 severity가 매핑에 따라 `gate_effect`를 정한다. 원문 대조에 실패한 상태는 "이슈 없음"이 아니라 "검증 미완료"이므로 coverage row라도 🟢을 쓰지 않는다. 상태 목록과 매핑의 정본은 `docs/review-rubric.md`의 L6 절이다.

검증을 마치지 못한 경우.

```
### 🟡 [L6] src/content/posts/any-mst.md:1

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/any-mst.md:1
- quote: not-recorded
- message: source unavailable — 대조할 노션 원문이나 승인된 자료에 접근할 수 없어 충실도를 검증하지 못했다. 현재 저장소 글의 구조와 논지만 보존 기준으로 삼았다.
- recommendation: 원문 접근이 가능해지면 핵심 구조, 논증 흐름, 누락, 자의적 추가를 대조한다.
- gate_effect: warn
```

대조를 마친 경우.

```
### 🟢 [L6] src/content/posts/all-pairs-shortest-path.md:25

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/all-pairs-shortest-path.md:25
- quote: 무엇을 구하는가
- message: verified fidelity — 승인된 설계 스펙과 대조해 문제 정의, 경유 제약, 점화식 증명, 의사코드의 핵심 줄기가 보존됨을 확인했다.
- recommendation: not-recorded
- gate_effect: info
```

### LLM 비평 coverage 누락

L1–L7 범주의 정본은 `docs/review-rubric.md` 하나다. 두 리뷰 커맨드가 그 문서를 읽어 적용하므로 같은 글은 어느 진입점으로 시작해도 같은 범주로 판정된다. `.claude/review_post.py`의 `REQUIRED_LLM_RULES`도 그 문서와 일치해야 하고, 계약 테스트가 둘을 대조한다.

두 리뷰 커맨드는 문제가 없는 범주도 생략하지 말고 explicit coverage row를 남기도록 규정한다. 따라서 `source: L`인 finding이 L1–L7을 모두 덮지 않으면 비평 단계가 끝나지 않은 것이다.

strict는 이를 품질 통과로 처리하지 않고 exit code `2`로 끝낸다. LLM 단계의 인프라 실패나 출력 계약 위반이 조용히 통과하는 것을 막기 위해서다. 누락된 범주는 stderr에 나열된다.

**판정 단위는 포스트다.** `/review-post-all`은 포스트 여럿을 한 파일에 담으므로, 리포트 전체를 한 묶음으로 세면 한 포스트의 coverage가 나머지를 대신한다. 비평하지 않은 포스트가 그대로 통과하는 구멍이다. 그래서 대상이 둘 이상이면 포스트별로 나눠 L1–L7을 확인한다.

- 대상은 finding의 `location`에 나온 `src/content/posts/*.md` 경로에서 모은다. L4가 가리키는 SVG 경로는 포스트가 아니므로 대상이 아니다.
- 따라서 `-all` 리포트의 coverage row는 `location`에 해당 포스트 경로를 반드시 적는다. `not-recorded`로 남기면 어느 포스트를 덮었는지 알 수 없어 그 포스트는 미비평으로 판정된다.
- 포스트가 하나인 `/review-post` 리포트는 리포트 전체가 곧 그 포스트이므로 리포트 단위로 본다. coverage row의 `location`이 `not-recorded`여도 판정이 달라지지 않는다.
- finding이 한 줄도 가리키지 않는 포스트는 리포트만 보고 알 수 없다. 대상 목록 자체의 누락은 이 게이트가 잡지 못한다.

## Frontmatter enum

`src/content/config.ts`의 현재 enum 값을 canonical 값으로 쓴다.

- category: `theory`, `cryptography`, `algorithm`, `os`, `unity`, `web-dev`
- difficulty: `입문`, `초급`, `중급`, `고급`, `심화`

## 검사 항목 요약

결정적(D): D1 깨진 굵게 · D2 줄표 남발 · D3 강조 과다 · D4 SVG 유효성 · D5 에셋 경로 · D6 내부 링크 · D7 frontmatter · D8 수식 짝 · D9 이모지 금지 · D10 callout 순서 · D11 수식 블록 줄 분리 · D12 시리즈 인접 편 링크 · D13 SVG 세로 클리핑
LLM 비평(L): L1 문체(AI 신호 + 바른 문장) · L2 설명 흐름·명료성 · L3 용어·어체 일관성 · L4 표현 정렬 — SVG·의사코드·수식·계산 예시 ↔ 본문 · L5 제목·description 적합성 · L6 소스 자료 충실성 · L7 논증·복잡도 정확성

각 범주의 정의와 문구는 `docs/review-rubric.md`가 정본이다. 위 목록은 이름만 훑는 색인이므로, 판정 기준이 필요하면 정본을 본다.

마이그레이션된 과거 finding은 원래 출처가 분명하지 않을 때 `MIGRATED` source를 쓴다. D/L taxonomy는 유지하며 새 구현은 기존 D/L rule id를 가능한 한 보존한다.

`docs/superpowers/specs/2026-06-03-review-post-command-design.md`는 커맨드를 처음 만들 때의 **v1 설계 기록**이다. 현재 계약이 아니다. 그 문서의 루브릭은 L1–L5까지만 정의하고 수학 정확성을 적극 판정하지 않는다고 적어 두었는데, 지금은 L6·L7이 더해지고 L7이 증명·복잡도를 직접 판정한다. 현재 기준은 이 README와 `docs/review-rubric.md`다.

## 비고

- 리포트는 **지적·권고만** 담는다. 자동 수정은 하지 않는다(수정은 사람이 판단).
- 이 디렉터리의 파일은 산출물이므로, 필요 없으면 지워도 된다.
