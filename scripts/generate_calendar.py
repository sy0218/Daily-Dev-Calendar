import calendar
from pathlib import Path
from datetime import date

YEAR = date.today().year
BASE = Path("history")
BASE.mkdir(exist_ok=True)

cal = calendar.Calendar(firstweekday=0)  # Monday

for month in range(1, 13):
    prev_y, prev_m = (YEAR, month - 1) if month > 1 else (YEAR - 1, 12)
    next_y, next_m = (YEAR, month + 1) if month < 12 else (YEAR + 1, 1)

    lines = []
    lines.append(f"# 📆 {YEAR}년 {month}월\n")
    lines.append(
        f'<p align="center">'
        f'<a href="./{prev_y}-{prev_m:02d}.md">⬅ {prev_y}.{prev_m:02d}</a>'
        f' &nbsp;|&nbsp; '
        f'<a href="./{next_y}-{next_m:02d}.md">{next_y}.{next_m:02d} ➡</a>'
        f'</p>\n\n'
    )

    lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
    lines.append("|----|----|----|----|----|----|----|")

    for week in cal.monthdayscalendar(YEAR, month):
        row = []
        for day in week:
            if day == 0:
                row.append(" ")
            else:
                path = f"../{YEAR}/{month:02d}/{YEAR}-{month:02d}-{day:02d}.md"
                row.append(f"[{day}]({path})")
        lines.append("| " + " | ".join(row) + " |")

    (BASE / f"{YEAR}-{month:02d}.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
