import sys
import re
import datetime

if len(sys.argv) < 2:
    sys.exit(0)

filepath = sys.argv[1]

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # date: YYYY-MM-DD 형식에만 시간을 추가 (이미 시간이 있으면 그대로)
    new_content = re.sub(
        r'^(date:\s+)(\d{4}-\d{2}-\d{2})\s*$',
        lambda m: m.group(1) + now,
        content,
        flags=re.MULTILINE
    )

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
except Exception:
    pass
