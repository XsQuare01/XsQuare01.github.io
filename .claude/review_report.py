#!/usr/bin/env python3
"""review-report/v2 정본 직렬화·파싱·검증. 표준 라이브러리만 사용한다.

Markdown 리포트의 구조와 필드 순서를 결정하는 유일한 모듈이다.
같은 입력은 항상 같은 Markdown을 만든다.
"""
import re

SCHEMA_VERSION = "review-report/v2"
NOT_RECORDED = "not-recorded"
FINDINGS_HEADING = "## Findings"

FINDING_FIELDS = (
    "severity",
    "source",
    "rule_id",
    "location",
    "quote",
    "message",
    "recommendation",
    "gate_effect",
)
SEVERITY_VALUES = ("🔴", "🟡", "🟢")
SOURCE_VALUES = ("D", "L", "MIGRATED")
GATE_EFFECT_VALUES = ("fail", "warn", "info")
STRICT_VALUES = ("true", "false", NOT_RECORDED)
# scaffold는 finding 0건을 허용하는 중간 상태, complete는 최종 산출물이다.
REPORT_STATES = ("scaffold", "complete")
# 정본 대응. 이 대응을 검증하지 않으면 🔴 finding에 gate_effect: info를 적어
# 품질 게이트를 우회할 수 있다.
CANONICAL_GATE_EFFECT = {"🔴": "fail", "🟡": "warn", "🟢": "info"}

_SEVERITY_RANK = {value: i for i, value in enumerate(SEVERITY_VALUES)}
_SOURCE_RANK = {value: i for i, value in enumerate(SOURCE_VALUES)}


def _value(finding, field):
    raw = finding.get(field, "")
    text = str(raw).strip() if raw is not None else ""
    return text or NOT_RECORDED


def summary_counts(findings):
    counts = {severity: 0 for severity in SEVERITY_VALUES}
    for finding in findings:
        severity = _value(finding, "severity")
        if severity in counts:
            counts[severity] += 1
    return counts


def format_summary(counts):
    return " · ".join(f"{severity} {counts.get(severity, 0)}" for severity in SEVERITY_VALUES)


def finding_sort_key(finding):
    location = _value(finding, "location")
    file_part, line_part = location, 0
    if ":" in location:
        head, tail = location.rsplit(":", 1)
        if tail.isdigit():
            file_part, line_part = head, int(tail)
    return (
        _SEVERITY_RANK.get(_value(finding, "severity"), len(SEVERITY_VALUES)),
        _SOURCE_RANK.get(_value(finding, "source"), len(SOURCE_VALUES)),
        _value(finding, "rule_id"),
        file_part,
        line_part,
    )


def serialize_finding(finding):
    heading = "### {} [{}] {}".format(
        _value(finding, "severity"),
        _value(finding, "rule_id"),
        _value(finding, "location"),
    )
    lines = [heading, ""]
    lines += [f"- {field}: {_value(finding, field)}" for field in FINDING_FIELDS]
    return "\n".join(lines)


def _strict_text(strict):
    if isinstance(strict, bool):
        return "true" if strict else "false"
    text = str(strict).strip()
    return text or NOT_RECORDED


def serialize_report(*, target, generated_at, strict, findings, sources=(),
                     migrated_from=None, audit=None):
    """정본 Markdown을 만든다. `audit`은 리포트 끝의 감사 섹션을 그대로 싣는다."""
    rows = sorted(findings, key=finding_sort_key)
    header = [
        f"schema_version: {SCHEMA_VERSION}",
        f"target: {target or NOT_RECORDED}",
        f"generated_at: {generated_at or NOT_RECORDED}",
        f"strict: {_strict_text(strict)}",
    ]
    if sources:
        header.append("sources: " + ", ".join(sources))
    if migrated_from:
        header.append(f"migrated_from: {migrated_from}")
    header.append(f"summary: {format_summary(summary_counts(rows))}")

    blocks = ["\n".join(header), FINDINGS_HEADING]
    blocks += [serialize_finding(row) for row in rows]
    if audit:
        blocks.append(audit.strip())
    return "\n\n".join(blocks) + "\n"


_HEADER_KEYS = ("schema_version", "target", "generated_at", "strict",
                "sources", "migrated_from", "summary")
_HEADER_RE = re.compile(r"^(" + "|".join(_HEADER_KEYS) + r"): (.*)$")
_FIELD_RE = re.compile(
    r"^\s*- \*{0,2}(" + "|".join(FINDING_FIELDS) + r")\*{0,2}: ?(.*)$"
)
# 과거 리포트 일부는 `### ` 대신 `- 🟢 [L1] <위치>` 불릿을 finding 제목으로 썼고
# 8개 필드를 그 아래 들여쓰기로 달았다. 근거가 온전하므로 제목으로 인정한다.
_BULLET_HEADING_RE = re.compile(r"^- ((?:🔴|🟡|🟢) \[(?:D\d+|L\d+)\].*)$")
# 제목 없이 `- severity:`부터 시작하는 블록도 있다.
_SEVERITY_START_RE = re.compile(r"^- \*{0,2}severity\*{0,2}: ?(.*)$")
# 8개 필드를 정본 순서 그대로 표 한 줄에 담은 리포트도 있다.
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
# 리포트 끝에는 지적을 어떻게 처리했는지 적은 감사 섹션이 붙는다. 어느 지적을 어느
# 커밋에서 고쳤는지, 재검증을 했는지가 여기 남는다. finding 모델에 자리가 없다는
# 이유로 버리면 리포트가 "경고만 있고 해결은 없는" 상태를 잘못 전달한다.
AUDIT_HEADINGS = ("후속 처리", "반영 상태", "반영 결과")
AUDIT_HEADING_RE = re.compile(r"^## (?:" + "|".join(AUDIT_HEADINGS) + r")\b.*$")
_FINDING_HEADING_LINE_RE = re.compile(r"(?m)^### (?:" + "|".join(SEVERITY_VALUES) + r") \[")


def _table_row_finding(line):
    """`| 🔴 | L | L7 | ... | fail |` 표 한 줄을 finding으로 읽는다."""
    match = _TABLE_ROW_RE.match(line)
    if not match:
        return None
    cells = [c.strip() for c in match.group(1).split("|")]
    if len(cells) != len(FINDING_FIELDS) or cells[0] not in SEVERITY_VALUES:
        return None
    if cells[1] not in SOURCE_VALUES or cells[-1] not in GATE_EFFECT_VALUES:
        return None
    return {field: _clean_field_value(cell) for field, cell in zip(FINDING_FIELDS, cells)}


def _clean_field_value(raw):
    """값을 감싼 백틱 한 쌍만 벗긴다. 값 안에 백틱이 더 있으면 벗기지 않는다.

    `` `A` / `B` ``처럼 code span이 여러 개인 값의 양 끝을 벗기면 남은 백틱이
    가운데를 감싸, 인용이 반대로 렌더된다. 근거를 바꾸는 것이라 하지 않는다.
    """
    text = raw.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`" and "`" not in text[1:-1]:
        text = text[1:-1].strip()
    return text or NOT_RECORDED


def parse_report(text):
    """리포트를 헤더와 finding으로 읽는다.

    입력에는 관대하다. `## Findings` 헤딩이 없어도 첫 `### ` 줄부터 finding으로
    보고, 굵게 표기(`- **severity**:`)도 필드로 인정한다. 과거 리포트를 근거
    손실 없이 되읽기 위해서다. 출력은 언제나 정본 형식 하나뿐이다.

    각 finding의 `_heading` 키에는 `### ` 뒤 원문을 그대로 담는다. 스키마 필드가
    아니라 마이그레이션이 설명형 제목을 되살릴 때만 쓰는 내부 값이다.

    감사 섹션(`## 후속 처리` 등)부터 끝까지는 `audit`에 원문 그대로 담고 finding으로
    읽지 않는다. 그 섹션의 `- 🟡 [L7] …` 불릿이 finding 제목 꼴이라, 읽으면 필드 없는
    finding이 유령처럼 생긴다.

    필드 값이 다음 줄로 이어진 리포트는 이어진 필드 이름을 `_continued`에 적어 둔다.
    정본은 필드 하나를 한 줄에 담으므로, 조용히 버리지 않고 검증에서 막기 위해서다.
    """
    header = {}
    findings = []
    current = None
    in_findings = False
    audit_lines = None
    last_field = None

    for line in text.splitlines():
        if audit_lines is not None:
            audit_lines.append(line)
            continue
        if AUDIT_HEADING_RE.match(line):
            if current:
                findings.append(current)
                current = None
            audit_lines = [line]
            continue

        heading = None
        if line.startswith("### "):
            heading = line[len("### "):].strip()
        else:
            bullet = _BULLET_HEADING_RE.match(line)
            if bullet:
                heading = bullet.group(1).strip()
        if heading is not None:
            in_findings = True
            if current:
                findings.append(current)
            current = {"_heading": heading}
            last_field = None
            continue

        row = _table_row_finding(line)
        if row is not None:
            in_findings = True
            if current:
                findings.append(current)
            findings.append(row)
            current = None
            continue

        # 제목 없이 `- severity:`로 시작하는 블록: 이미 severity를 채운 뒤라면 다음 finding이다.
        if _SEVERITY_START_RE.match(line) and (current is None or "severity" in current):
            in_findings = True
            if current:
                findings.append(current)
            current = {}
            last_field = None

        if not in_findings:
            match = _HEADER_RE.match(line)
            if match:
                key, value = match.group(1), match.group(2).strip()
                header[key] = [s.strip() for s in value.split(",") if s.strip()] \
                    if key == "sources" else value
                continue
            if line.strip() == FINDINGS_HEADING:
                in_findings = True
            continue

        if current is None:
            continue
        match = _FIELD_RE.match(line)
        if match:
            last_field = match.group(1)
            current[last_field] = _clean_field_value(match.group(2))
            continue
        # 들여쓴 비어 있지 않은 줄은 앞 필드의 연장이다. 중첩 목록(`  - 근거`)이든
        # 표든 모양으로 가리지 않는다. 정본 한 줄 형식에 담을 수 없는 내용이라는
        # 사실은 같고, 모양으로 걸러 내면 걸러진 모양만 조용히 사라진다.
        #
        # 들여쓰기 없는 줄은 finding 블록 밖의 산문(`요약:` 등)이라 연장이 아니다.
        # 들여쓴 하위 필드(`  - source: L`)는 위에서 필드로 먼저 읽는다.
        if last_field and line[:1].isspace() and line.strip():
            current.setdefault("_continued", []).append(last_field)

    if current:
        findings.append(current)
    audit = "\n".join(audit_lines).strip() if audit_lines else None
    return {"header": header, "findings": findings, "audit": audit}


_CANONICAL_HEADING_RE = re.compile(r"^(🔴|🟡|🟢) \[([^\]]+)\] ?(.*)$")


def validate_source_findings(findings):
    """정본화 **전** 원본 finding을 검사한다.

    serialize_report()는 빠진 필드를 not-recorded로 채우고 제목을 필드 값으로
    다시 만든다. 그래서 정본화한 텍스트만 검증하면 원본의 필드 누락과 제목↔필드
    불일치가 조용히 덮인다. `### 🔴 [L7]` 제목에 `severity: 🟢` 필드가 붙어도
    빨간 제목이 사라진 채 통과한다. 원본을 먼저 봐야 막을 수 있다.

    제목이 정본 꼴(`<심각도> [<규칙>] <위치>`)일 때만 대조한다. 레거시 리포트의
    설명형 제목은 마이그레이션이 message로 옮기므로 여기서 판정하지 않는다.
    """
    errors = []
    for index, finding in enumerate(findings):
        label = f"finding #{index + 1}"
        missing = [field for field in FINDING_FIELDS if field not in finding]
        if missing:
            errors.append(f"{label} missing fields: {', '.join(missing)}")

        continued = finding.get("_continued")
        if continued:
            errors.append(
                f"{label} {', '.join(sorted(set(continued)))} 값이 여러 줄이다. "
                "정본은 필드 하나를 한 줄에 담으므로 이어진 줄이 사라진다. "
                "값을 한 줄로 합친 뒤 다시 실행한다"
            )

        match = _CANONICAL_HEADING_RE.match((finding.get("_heading") or "").strip())
        if not match:
            continue
        heading_severity, heading_rule, heading_rest = match.groups()
        for name, in_heading, in_field in (
            ("severity", heading_severity, finding.get("severity")),
            ("rule_id", heading_rule, finding.get("rule_id")),
        ):
            if in_field is not None and in_heading != in_field:
                errors.append(
                    f"{label} 제목의 {name} {in_heading}가 필드 {in_field}와 다르다"
                )
        location = finding.get("location")
        # 제목에 위치 뒤로 사람이 쓴 요약이 더 붙는 리포트가 있어 접두 일치까지 인정한다.
        if location and heading_rest and not heading_rest.startswith(location):
            errors.append(
                f"{label} 제목의 위치 {heading_rest}가 필드 {location}와 다르다"
            )
    return errors


def validate_source_header(text, header):
    """정본화가 **고치지 않는** 헤더 계약을 원본에서 검사한다.

    요약 갱신, finding 정렬, 공백은 정본화가 맡아 고치는 항목이라 여기서 보지 않는다.
    반면 `strict` 값과 선언 위치는 고칠 대상이 아니라 입력 결함이다. 정본화가 조용히
    덮어쓰면 결함이 리포트에서 지워진 채 통과한다. `--strict`를 붙이면 `strict` 값을
    덮어쓰므로 특히 그렇다.
    """
    errors = []
    if header.get("strict") and header["strict"] not in STRICT_VALUES:
        errors.append(
            f"invalid strict: {header['strict']} (must be one of {', '.join(STRICT_VALUES)})"
        )
    if text.split("\n", 1)[0].strip() != f"schema_version: {SCHEMA_VERSION}":
        errors.append("schema_version must be the first line")
    return errors


def verify_round_trip(text, findings, audit=None):
    """정본화한 텍스트가 원본 근거를 그대로 담았는지 대조한다.

    심각도 개수만 세면 값이 바뀐 것을 놓친다. 개수가 같아도 인용이 잘리거나 감사
    섹션이 사라지면 리포트는 다른 사실을 말한다. 그래서 필드 값을 하나하나 비교한다.

    비교 기준은 직렬화에 실제로 넘긴 값이다. 마이그레이션이 없는 근거를 의도적으로
    `not-recorded`로 채우는 것은 손실이 아니라 표시이므로 여기서 걸리지 않는다.

    직렬화는 finding을 정본 순서로 재정렬하므로 같은 키로 정렬한 뒤 짝지어 본다.
    입력 순서로 비교하면 재정렬을 손실로 오인한다.
    """
    errors = []
    parsed = parse_report(text)
    if len(parsed["findings"]) != len(findings):
        return [f"finding 개수가 다르다: 원본 {len(findings)}건 정본 {len(parsed['findings'])}건"]

    canonical_order = sorted(findings, key=finding_sort_key)
    for index, (before, after) in enumerate(zip(canonical_order, parsed["findings"]), 1):
        for field in FINDING_FIELDS:
            expected = _value(before, field)
            if after.get(field) != expected:
                errors.append(
                    f"finding #{index} {field} 값이 정본화에서 바뀌었다: "
                    f"원본 {expected!r} → 정본 {after.get(field)!r}"
                )
    if (audit or None) != (parsed["audit"] or None):
        errors.append("감사 섹션이 정본화에서 바뀌었다")
    return errors


def validate_report(text, *, state="complete"):
    """저장 리포트가 정본 계약을 지키는지 본다. 오류 목록을 돌려준다.

    `state`가 `scaffold`·`complete`가 아니면 ValueError다. 오타를 오류 목록에 담으면
    호출자가 그것을 데이터 결함으로 읽고 넘어간다. 알 수 없는 상태는 데이터가 아니라
    호출 쪽 버그이므로 조용히 scaffold처럼 처리하지 않고 즉시 터뜨린다.
    """
    if state not in REPORT_STATES:
        raise ValueError(f"state must be one of {REPORT_STATES}: {state!r}")

    errors = []
    parsed = parse_report(text)
    header, findings = parsed["header"], parsed["findings"]

    if parsed["audit"] and _FINDING_HEADING_LINE_RE.search(parsed["audit"]):
        errors.append(
            "감사 섹션 뒤에 finding이 있다. 파서가 읽지 않아 판정에서 빠지므로 "
            "감사 섹션 앞으로 옮겨야 한다"
        )

    if header.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    # 선언은 첫 줄이어야 한다. 아래쪽에 묻힌 선언은 리포트를 여는 사람도, 첫 줄로
    # 정본 여부를 가리는 게이트도 보지 못한다.
    elif text.split("\n", 1)[0].strip() != f"schema_version: {SCHEMA_VERSION}":
        errors.append("schema_version must be the first line")
    for key in ("target", "generated_at", "strict", "summary"):
        if not header.get(key):
            errors.append(f"missing required header field: {key}")
    if header.get("strict") and header["strict"] not in STRICT_VALUES:
        errors.append(
            f"invalid strict: {header['strict']} (must be one of {', '.join(STRICT_VALUES)})"
        )
    if FINDINGS_HEADING not in text:
        errors.append(f"missing section: {FINDINGS_HEADING}")

    if state == "complete" and not findings:
        errors.append("complete report must contain at least one finding")

    for index, finding in enumerate(findings):
        missing = [f for f in FINDING_FIELDS if f not in finding]
        if missing:
            errors.append(f"finding #{index + 1} missing fields: {', '.join(missing)}")
            continue
        if finding["severity"] not in SEVERITY_VALUES:
            errors.append(f"finding #{index + 1} invalid severity: {finding['severity']}")
        if finding["source"] not in SOURCE_VALUES:
            errors.append(f"finding #{index + 1} invalid source: {finding['source']}")
        if finding["gate_effect"] not in GATE_EFFECT_VALUES:
            errors.append(f"finding #{index + 1} invalid gate_effect: {finding['gate_effect']}")
        expected_gate = CANONICAL_GATE_EFFECT.get(finding["severity"])
        if expected_gate and finding["gate_effect"] != expected_gate:
            errors.append(
                f"finding #{index + 1} severity {finding['severity']}는 "
                f"gate_effect {expected_gate}여야 하는데 {finding['gate_effect']}다"
            )

    expected = format_summary(summary_counts(findings))
    if header.get("summary") and header["summary"] != expected:
        errors.append(f"summary is stale: header={header['summary']} computed={expected}")

    return errors
