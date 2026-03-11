from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
PRINTABLES = [
    {
        "title": "Single-Task Oath",
        "source": ROOT / "site/printables/single-task-oath-card.md",
        "base": "single-task-oath-card",
    },
    {
        "title": "Tide Mark Calendar",
        "source": ROOT / "site/printables/tide-mark-calendar-card.md",
        "base": "tide-mark-calendar-card",
    },
    {
        "title": "Tide Marks Buddy Ping",
        "source": ROOT / "site/printables/tide-marks-buddy-ping.md",
        "base": "tide-marks-buddy-ping",
    },
    {
        "title": "Wake Invocation Checklist",
        "source": ROOT / "site/printables/wake-invocation-checklist.md",
        "base": "wake-invocation-checklist",
    },
    {
        "title": "Perfection Wyrm - Done Is Better",
        "source": ROOT / "site/printables/perfection-wyrm-done-is-better.md",
        "base": "perfection-wyrm-done-is-better",
    },
    {
        "title": "Rejection Wisp - Reply Scaffold",
        "source": ROOT / "site/printables/rejection-wisp-reply-scaffold.md",
        "base": "rejection-wisp-reply-scaffold",
    },
    {
        "title": "Sensory Storm - Sensory Reset Card",
        "source": ROOT / "site/printables/sensory-storm-reset-card.md",
        "base": "sensory-storm-reset-card",
    },
    {
        "title": "Burnout Dragon - Minimum Viable Day",
        "source": ROOT / "site/printables/burnout-dragon-minimum-viable-day.md",
        "base": "burnout-dragon-minimum-viable-day",
    },
]

NAV_MARKERS = ("Quick Navigation",)
SKIP_LINE_FRAGMENTS = ("Downloads:",)


def cleaned_lines(path: Path) -> Iterable[str]:
    nav_seen = False
    in_front_matter = False
    front_matter_finished = False

    for index, raw in enumerate(path.read_text(encoding="utf-8").splitlines()):
        stripped = raw.strip()

        if index == 0 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            if stripped == "---":
                in_front_matter = False
                front_matter_finished = True
            continue
        if front_matter_finished and not stripped:
            front_matter_finished = False
            continue

        nav_heading = stripped.lstrip("#").strip()
        if any(fragment in stripped for fragment in SKIP_LINE_FRAGMENTS):
            continue
        if any(marker in stripped for marker in NAV_MARKERS) or any(
            marker in nav_heading for marker in NAV_MARKERS
        ):
            nav_seen = True
            continue
        if nav_seen:
            continue

        line = stripped
        if not line:
            yield ""
            continue
        if line.startswith("#"):
            line = line.lstrip("# ")
        line = re.sub(r"^[>\-\*]\s*", "", line)
        line = re.sub(r"_+", lambda match: "_" * min(len(match.group()), 40), line)
        line = line.encode("ascii", "ignore").decode("ascii")
        if any(len(word) > 40 for word in line.split()):
            chunks = []
            for word in line.split():
                if len(word) > 40:
                    for start in range(0, len(word), 40):
                        chunks.append(word[start : start + 40])
                else:
                    chunks.append(word)
            line = " ".join(chunks)
        yield line


def get_fpdf_dependencies() -> tuple[Any, Any, Any]:
    try:
        from fpdf import FPDF
        from fpdf.enums import XPos, YPos
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency 'fpdf2'. Install with `pip install -r requirements.txt` before generating PDFs."
        ) from exc

    return FPDF, XPos, YPos


def add_body(pdf: Any, lines: Iterable[str]):
    pdf.set_font("Helvetica", size=11)
    width = pdf.w - pdf.l_margin - pdf.r_margin
    for line in lines:
        pdf.set_x(pdf.l_margin)
        if line == "---":
            pdf.ln(4)
            pdf.cell(0, 0, "")
            pdf.ln(2)
            continue
        pdf.multi_cell(width, 7, line if line else " ")
    pdf.ln(2)


def build_pdf(title: str, lines: Iterable[str], output: Path):
    FPDF, XPos, YPos = get_fpdf_dependencies()
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.add_page()
    pdf.set_y(12)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    add_body(pdf, lines)
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output))


def main():
    output_dir = ROOT / "site/printables/pdf"
    for printable in PRINTABLES:
        lines = list(cleaned_lines(printable["source"]))
        ink_output = output_dir / f"{printable['base']}-ink.pdf"
        build_pdf(printable["title"] + " (Ink-Friendly)", lines, ink_output)
        print(f"Generated {ink_output.name}")


if __name__ == "__main__":
    main()
