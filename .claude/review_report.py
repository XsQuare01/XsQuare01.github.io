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


def serialize_report(*, target, generated_at, strict, findings, sources=(), migrated_from=None):
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
    text = raw.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        text = text[1:-1].strip()
    return text or NOT_RECORDED


def parse_report(text):
    """리포트를 헤더와 finding으로 읽는다.

    입력에는 관대하다. `## Findings` 헤딩이 없어도 첫 `### ` 줄부터 finding으로
    보고, 굵게 표기(`- **severity**:`)도 필드로 인정한다. 과거 리포트를 근거
    손실 없이 되읽기 위해서다. 출력은 언제나 정본 형식 하나뿐이다.

    각 finding의 `_heading` 키에는 `### ` 뒤 원문을 그대로 담는다. 스키마 필드가
    아니라 마이그레이션이 설명형 제목을 되살릴 때만 쓰는 내부 값이다.
    """
    header = {}
    findings = []
    current = None
    in_findings = False

    for line in text.splitlines():
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
            current[match.group(1)] = _clean_field_value(match.group(2))

    if current:
        findings.append(current)
    return {"header": header, "findings": findings}


def validate_report(text, *, state="complete"):
    errors = []
    parsed = parse_report(text)
    header, findings = parsed["header"], parsed["findings"]

    if header.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    for key in ("target", "generated_at", "strict", "summary"):
        if not header.get(key):
            errors.append(f"missing required header field: {key}")
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

    expected = format_summary(summary_counts(findings))
    if header.get("summary") and header["summary"] != expected:
        errors.append(f"summary is stale: header={header['summary']} computed={expected}")

    return errors
