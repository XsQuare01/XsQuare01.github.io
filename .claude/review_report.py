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


def serialize_report(*, target, generated_at, strict, findings, sources=()):
    rows = sorted(findings, key=finding_sort_key)
    header = [
        f"schema_version: {SCHEMA_VERSION}",
        f"target: {target or NOT_RECORDED}",
        f"generated_at: {generated_at or NOT_RECORDED}",
        f"strict: {_strict_text(strict)}",
    ]
    if sources:
        header.append("sources: " + ", ".join(sources))
    header.append(f"summary: {format_summary(summary_counts(rows))}")

    blocks = ["\n".join(header), FINDINGS_HEADING]
    blocks += [serialize_finding(row) for row in rows]
    return "\n\n".join(blocks) + "\n"


_HEADER_KEYS = ("schema_version", "target", "generated_at", "strict", "sources", "summary")
_HEADER_RE = re.compile(r"^(" + "|".join(_HEADER_KEYS) + r"): (.*)$")
_FIELD_RE = re.compile(
    r"^- \*{0,2}(" + "|".join(FINDING_FIELDS) + r")\*{0,2}: ?(.*)$"
)


def _clean_field_value(raw):
    text = raw.strip()
    if len(text) >= 2 and text[0] == "`" and text[-1] == "`":
        text = text[1:-1].strip()
    return text or NOT_RECORDED


def parse_report(text):
    header = {}
    findings = []
    current = None
    in_findings = False

    for line in text.splitlines():
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

        if line.startswith("### "):
            if current:
                findings.append(current)
            current = {}
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
