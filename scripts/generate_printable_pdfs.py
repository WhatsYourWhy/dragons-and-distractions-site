from __future__ import annotations

from pathlib import Path
from typing import Iterable
try:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency 'fpdf2'. Install with `pip install -r requirements.txt` before generating PDFs."
    ) from exc
import re

ROOT = Path(__file__).resolve().parent.parent
PRINTABLES = [
    {
        "title": "Single-Task Oath",
        "source": ROOT / "site/printables/single-task-oath-card.md",
        "base": "single-task-oath-card",
        "image": ROOT / "TaskHydra.png",
    },
    {
        "title": "Tide Mark Calendar",
        "source": ROOT / "site/printables/tide-mark-calendar-card.md",
        "base": "tide-mark-calendar-card",
        "image": ROOT / "TheTemporalShark.png",
    },
    {
        "title": "Tide Marks Buddy Ping",
        "source": ROOT / "site/printables/tide-marks-buddy-ping.md",
        "base": "tide-marks-buddy-ping",
        "image": ROOT / "CaveBear.png",
    },
    {
        "title": "Wake Invocation Checklist",
        "source": ROOT / "site/printables/wake-invocation-checklist.md",
        "base": "wake-invocation-checklist",
        "image": ROOT / "SlumberTroll.png",
    },
]

NAV_MARKER = "🔗 Quick Navigation"


def cleaned_lines(path: Path) -> Iterable[str]:
    nav_seen = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        nav_heading = stripped.lstrip("#").strip()
        if stripped.startswith(NAV_MARKER) or nav_heading.startswith(NAV_MARKER):
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


def add_body(pdf: FPDF, lines: Iterable[str]):
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


def build_pdf(title: str, lines: Iterable[str], output: Path, image: Path | None):
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.add_page()
    top_margin = 10

    if image and image.exists():
        page_width = pdf.w - 20
        pdf.image(str(image), x=10, y=10, w=page_width)
        top_margin = 75

    pdf.set_y(top_margin)
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
        base = printable["base"]
        ink_output = output_dir / f"{base}-ink.pdf"
        art_output = output_dir / f"{base}-art.pdf"

        build_pdf(printable["title"] + " (Ink-Friendly)", lines, ink_output, None)
        build_pdf(printable["title"] + " (With Art)", lines, art_output, printable.get("image"))
        print(f"Generated {ink_output.name} and {art_output.name}")


if __name__ == "__main__":
    main()
