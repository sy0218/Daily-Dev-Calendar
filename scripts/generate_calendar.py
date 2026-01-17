import calendar
from datetime import datetime
from pathlib import Path

# 기본 경로
BASE_DIR = Path(__file__).resolve().parents[1]
HISTORY_DIR = BASE_DIR / "history"
README_PATH = BASE_DIR / "README.md"

HISTORY_DIR.mkdir(exist_ok=True)

today = datetime.today()
year, month, day = today.year, today.month, today.day
today_str = today.strftime("%Y-%m-%d")

# 날짜별 경로
YEAR_DIR = BASE_DIR / str(year)
MONTH_DIR = YEAR_DIR / f"{month:02d}"
DAY_FILE = MONTH_DIR / f"{today_str}.md"


def ym(y, m):
    return f"{y}-{m:02d}"


def prev_next(y, m):
    prev_y, prev_m = (y - 1, 12) if m == 1 else (y, m - 1)
    next_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
    return prev_y, prev_m, next_y, next_m


def render_month_calendar(year, month, today_str=None, base_path=""):
    cal = calendar.Calendar(firstweekday=0)
    prefix = f"{base_path}/" if base_path else ""

    lines = [
        "| Mon | Tue | Wed | Thu | Fri | Sat | Sun |",
        "|----|----|----|----|----|----|----|",
    ]

    for week in cal.monthdayscalendar(year, month):
        row = []
        for d in week:
            if d == 0:
                row.append(" ")
            else:
                date_str = f"{year}-{month:02d}-{d:02d}"
                link = f"[{d}]({prefix}{year}/{month:02d}/{date_str}.md)"
                if today_str and date_str == today_str:
                    row.append(f"**{link}**")
                else:
                    row.append(link)
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def last_n_months(year, month, n=3):
    result = []
    for i in range(n):
        y = year
        m = month - i
        while m <= 0:
            y -= 1
            m += 12
        result.append((y, m))
    return result


def summarize_month(y, m):
    month_dir = BASE_DIR / str(y) / f"{m:02d}"
    summary = {"algo": 0, "practice": 0, "theory": 0}

    if not month_dir.exists():
        return summary

    for md in month_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8")

        def count(section):
            if section not in text:
                return 0
            part = text.split(section, 1)[1]
            return part.count("\n- ")

        summary["algo"] += count("## 🛠 프로그래밍")
        summary["practice"] += count("## 📘 실습")
        summary["theory"] += count("## 📝 이론")

    return summary


# 연 / 월 디렉토리 및 일별 파일
MONTH_DIR.mkdir(parents=True, exist_ok=True)

if not DAY_FILE.exists():
    DAY_FILE.write_text(
        f"""# {today_str}

## 🛠 프로그래밍
- 

## 📘 실습
- 

## 📝 이론
- 
""",
        encoding="utf-8",
    )


# history 월별 파일
history_file = HISTORY_DIR / f"{ym(year, month)}.md"
py, pm, ny, nm = prev_next(year, month)

history_file.write_text(
    f"""# {year}년 {month}월

<p align="center">
<a href="./{ym(py, pm)}.md">⬅ {py}.{pm:02d}</a>
&nbsp;|&nbsp;
<a href="./{ym(ny, nm)}.md">{ny}.{nm:02d} ➡</a>
</p>

{render_month_calendar(year, month, base_path="..")}
""",
    encoding="utf-8",
)


# README 생성
lines = [
    "# 하루 한 줄 개발 기록",
    "",
    "---",
    "",
    "## Current Month",
    f"### {year}년 {month}월",
    "",
    f'<p align="center">'
    f'<a href="history/{ym(py, pm)}.md">⬅ {py}.{pm:02d}</a>'
    f' &nbsp;|&nbsp; '
    f'<a href="history/{ym(ny, nm)}.md">{ny}.{nm:02d} ➡</a>'
    f'</p>',
    "",
    render_month_calendar(year, month, today_str),
    "",
    "---",
    "",
    "## Monthly Summary (Last 3 Months)",
    "",
]

for y, m in last_n_months(year, month, 3):
    s = summarize_month(y, m)
    lines.append(
        f"- **{y}-{m:02d}** : 알고리즘 {s['algo']} / 실습 {s['practice']} / 이론 {s['theory']}"
    )

README_PATH.write_text("\n".join(lines), encoding="utf-8")
