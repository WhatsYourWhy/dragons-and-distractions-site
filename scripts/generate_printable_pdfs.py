from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from pathlib import Path
import re
from typing import Iterable

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "site/printables/pdf"
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

PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 0.55 * inch
RIGHT_MARGIN = 0.55 * inch
TOP_MARGIN = 0.55 * inch
BOTTOM_MARGIN = 0.5 * inch
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

COLOR_INK = colors.HexColor("#1f1810")
COLOR_MUTED = colors.HexColor("#63594d")
COLOR_LINE = colors.HexColor("#8f877c")
COLOR_PANEL = colors.HexColor("#fbf9f4")
COLOR_PANEL_ALT = colors.HexColor("#f2ede3")
COLOR_BAND = colors.HexColor("#e5dccf")
COLOR_RULE = colors.HexColor("#b3a99b")


@dataclass
class Block:
    type: str
    text: str = ""
    level: int = 0
    items: list[str] = field(default_factory=list)


@dataclass
class Section:
    title: str
    blocks: list[Block] = field(default_factory=list)


@dataclass
class PrintableDoc:
    title: str
    hero_intro: str
    source: Path
    sections: list[Section]
    intro_blocks: list[Block]


def normalize_text(text: str) -> str:
    return text.replace("\t", " ").strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    front_matter = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return front_matter, body


def parse_blocks(lines: list[str]) -> list[Block]:
    blocks: list[Block] = []
    index = 0

    while index < len(lines):
        raw = lines[index]
        stripped = normalize_text(raw)

        if not stripped:
            index += 1
            continue

        if stripped == "---":
            blocks.append(Block(type="rule"))
            index += 1
            continue

        if stripped.startswith("```"):
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not normalize_text(lines[index]).startswith("```"):
                code_lines.append(lines[index].rstrip())
                index += 1
            index += 1
            blocks.append(Block(type="code", text="\n".join(code_lines).strip()))
            continue

        heading_match = re.match(r"^(#{2,3})\s+(.*)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            blocks.append(Block(type="heading", level=level, text=heading_match.group(2).strip()))
            index += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines):
                current = normalize_text(lines[index])
                if not current.startswith(">"):
                    break
                quote_lines.append(current.lstrip("> ").rstrip())
                index += 1
            blocks.append(Block(type="quote", text=" ".join(quote_lines).strip()))
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items: list[str] = []
            while index < len(lines):
                current = lines[index].rstrip()
                current_stripped = normalize_text(current)
                if not current_stripped:
                    index += 1
                    continue
                if re.match(r"^\d+\.\s+", current_stripped):
                    items.append(re.sub(r"^\d+\.\s+", "", current_stripped))
                    index += 1
                    continue
                if current.startswith("   - ") or current.startswith("  - "):
                    items.append(current_stripped)
                    index += 1
                    continue
                break
            blocks.append(Block(type="ordered_list", items=items))
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines):
                current_stripped = normalize_text(lines[index])
                if not current_stripped.startswith("- "):
                    break
                items.append(current_stripped[2:].strip())
                index += 1
            blocks.append(Block(type="bullet_list", items=items))
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            current = normalize_text(lines[index])
            if not current:
                break
            if current == "---" or current.startswith(">") or current.startswith("```"):
                break
            if re.match(r"^(#{2,3})\s+", current):
                break
            if re.match(r"^\d+\.\s+", current) or current.startswith("- "):
                break
            paragraph_lines.append(current)
            index += 1
        blocks.append(Block(type="paragraph", text=" ".join(paragraph_lines).strip()))

    return blocks


def parse_printable(path: Path) -> PrintableDoc:
    front_matter, body = split_front_matter(path.read_text(encoding="utf-8-sig"))
    parsed_blocks = parse_blocks(body.splitlines())

    intro_blocks: list[Block] = []
    sections: list[Section] = []
    current_section: Section | None = None

    for block in parsed_blocks:
        if block.type == "heading" and block.level == 2:
            current_section = Section(title=block.text)
            sections.append(current_section)
            continue

        if current_section is None:
            intro_blocks.append(block)
        else:
            current_section.blocks.append(block)

    return PrintableDoc(
        title=front_matter.get("title") or path.stem.replace("-", " ").title(),
        hero_intro=front_matter.get("hero_intro", ""),
        source=path,
        sections=sections,
        intro_blocks=intro_blocks,
    )


def build_styles():
    stylesheet = getSampleStyleSheet()
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow",
            parent=stylesheet["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=COLOR_MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "title",
            parent=stylesheet["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=19,
            leading=22,
            textColor=COLOR_INK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=stylesheet["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9.4,
            leading=12,
            textColor=COLOR_MUTED,
            alignment=TA_CENTER,
        ),
        "body": ParagraphStyle(
            "body",
            parent=stylesheet["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=12.2,
            textColor=COLOR_INK,
            spaceAfter=5,
        ),
        "body_compact": ParagraphStyle(
            "body_compact",
            parent=stylesheet["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=11.5,
            textColor=COLOR_INK,
            spaceAfter=4,
        ),
        "marker": ParagraphStyle(
            "marker",
            parent=stylesheet["BodyText"],
            fontName="Courier-Bold",
            fontSize=8.8,
            leading=10.5,
            textColor=COLOR_MUTED,
            spaceAfter=0,
        ),
        "section_title": ParagraphStyle(
            "section_title",
            parent=stylesheet["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.3,
            leading=13.3,
            textColor=COLOR_INK,
            spaceAfter=0,
        ),
        "subheading": ParagraphStyle(
            "subheading",
            parent=stylesheet["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=9.6,
            leading=11.3,
            textColor=COLOR_INK,
            spaceBefore=4,
            spaceAfter=3,
        ),
        "quote": ParagraphStyle(
            "quote",
            parent=stylesheet["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=12.0,
            textColor=COLOR_INK,
        ),
        "code": ParagraphStyle(
            "code",
            parent=stylesheet["Code"],
            fontName="Courier",
            fontSize=8.5,
            leading=10.4,
            textColor=COLOR_INK,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=stylesheet["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9,
            textColor=COLOR_MUTED,
        ),
    }


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def split_label_and_blank(text: str) -> tuple[str, str] | None:
    match = re.match(r"^(.*?:)\s+(_{6,})$", text)
    if not match:
        return None
    return match.group(1).strip(), match.group(2)


def make_fill_line(text: str, styles: dict[str, ParagraphStyle]) -> Table:
    match = split_label_and_blank(text)
    if not match:
        return Table(
            [[paragraph(text, styles["body_compact"])]],
            colWidths=[CONTENT_WIDTH - 20],
            style=TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 1),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ]
            ),
        )

    label, _ = match
    return Table(
        [[paragraph(label, styles["body_compact"]), ""]],
        colWidths=[2.35 * inch, CONTENT_WIDTH - 20 - 2.35 * inch],
        style=TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("LINEBELOW", (1, 0), (1, 0), 0.75, COLOR_LINE),
            ]
        ),
    )


def make_bullet_rows(
    items: list[str], styles: dict[str, ParagraphStyle], marker: str = "[ ]", indent: float = 0
) -> list:
    rows: list = []
    for item in items:
        text = item[2:].strip() if item.startswith("- ") else item
        content = make_fill_line(text, styles) if "____" in text else paragraph(text, styles["body_compact"])
        rows.append(
            Table(
                [[paragraph(marker, styles["marker"]), content]],
                colWidths=[0.42 * inch, CONTENT_WIDTH - 20 - indent - 0.42 * inch],
                style=TableStyle(
                    [
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 1),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                ),
            )
        )
    return rows


def make_ordered_list(items: list[str], styles: dict[str, ParagraphStyle]) -> list:
    flowables: list = []
    counter = 1

    for item in items:
        if item.startswith("- "):
            nested_rows = make_bullet_rows([item], styles, marker="-", indent=16)
            flowables.extend(
                [
                    Table(
                        [[nested_row]],
                        colWidths=[CONTENT_WIDTH - 30],
                        style=TableStyle(
                            [
                                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                ("TOPPADDING", (0, 0), (-1, -1), 0),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                            ]
                        ),
                    )
                    for nested_row in nested_rows
                ]
            )
            continue

        label = f"{counter}."
        content = make_fill_line(item, styles) if "____" in item else paragraph(item, styles["body_compact"])
        flowables.append(
            Table(
                [[paragraph(label, styles["body_compact"]), content]],
                colWidths=[0.28 * inch, CONTENT_WIDTH - 30 - 0.28 * inch],
                style=TableStyle(
                    [
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 1),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                ),
            )
        )
        counter += 1

    return flowables


def render_block(block: Block, styles: dict[str, ParagraphStyle]) -> list:
    if block.type == "paragraph":
        if "____" in block.text:
            return [make_fill_line(block.text, styles)]
        return [paragraph(block.text, styles["body"])]

    if block.type == "bullet_list":
        return [*make_bullet_rows(block.items, styles), Spacer(1, 3)]

    if block.type == "ordered_list":
        return [*make_ordered_list(block.items, styles), Spacer(1, 3)]

    if block.type == "quote":
        return [
            Table(
                [[paragraph(block.text, styles["quote"])]],
                colWidths=[CONTENT_WIDTH - 20],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PANEL_ALT),
                        ("BOX", (0, 0), (-1, -1), 0.75, COLOR_RULE),
                        ("LINEBEFORE", (0, 0), (0, 0), 2.2, COLOR_LINE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                ),
            ),
            Spacer(1, 5),
        ]

    if block.type == "code":
        return [
            Table(
                [[Preformatted(block.text, styles["code"])]],
                colWidths=[CONTENT_WIDTH - 20],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), COLOR_PANEL_ALT),
                        ("BOX", (0, 0), (-1, -1), 0.75, COLOR_RULE),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ]
                ),
            ),
            Spacer(1, 5),
        ]

    if block.type == "heading" and block.level == 3:
        return [paragraph(block.text, styles["subheading"])]

    if block.type == "rule":
        return [HRFlowable(width="100%", thickness=0.6, color=COLOR_RULE), Spacer(1, 6)]

    return []


def make_title_band(doc: PrintableDoc, styles: dict[str, ParagraphStyle]) -> Table:
    eyebrow = paragraph("Dragons & Distractions Printable", styles["eyebrow"])
    title = paragraph(doc.title, styles["title"])
    subtitle = paragraph(doc.hero_intro, styles["subtitle"]) if doc.hero_intro else Spacer(1, 0)
    return Table(
        [[[eyebrow, title, subtitle]]],
        colWidths=[CONTENT_WIDTH],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_BAND),
                ("BOX", (0, 0), (-1, -1), 1.0, COLOR_LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("RIGHTPADDING", (0, 0), (-1, -1), 16),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        ),
    )


def make_intro_panel(doc: PrintableDoc, styles: dict[str, ParagraphStyle]) -> Table | None:
    if not doc.intro_blocks:
        return None

    flowables: list = []
    for block in doc.intro_blocks:
        flowables.extend(render_block(block, styles))

    return Table(
        [[flowables]],
        colWidths=[CONTENT_WIDTH],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_PANEL),
                ("BOX", (0, 0), (-1, -1), 0.8, COLOR_RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        ),
    )


def make_section(section: Section, styles: dict[str, ParagraphStyle]) -> KeepTogether:
    body_flowables: list = []
    for block in section.blocks:
        body_flowables.extend(render_block(block, styles))

    table = Table(
        [
            [paragraph(section.title, styles["section_title"])],
            [body_flowables],
        ],
        colWidths=[CONTENT_WIDTH],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), COLOR_BAND),
                ("BACKGROUND", (0, 1), (-1, 1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.8, COLOR_LINE),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, COLOR_LINE),
                ("LEFTPADDING", (0, 0), (-1, 0), 12),
                ("RIGHTPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("LEFTPADDING", (0, 1), (-1, 1), 12),
                ("RIGHTPADDING", (0, 1), (-1, 1), 12),
                ("TOPPADDING", (0, 1), (-1, 1), 10),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        ),
    )
    return KeepTogether([table, Spacer(1, 9)])


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(COLOR_RULE)
    canvas.setLineWidth(0.6)
    canvas.line(LEFT_MARGIN, PAGE_HEIGHT - 20, PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 20)
    canvas.line(LEFT_MARGIN, 20, PAGE_WIDTH - RIGHT_MARGIN, 20)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(COLOR_MUTED)
    canvas.drawString(LEFT_MARGIN, 9, "Dragons & Distractions")
    canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, 9, f"Page {doc.page}")
    canvas.restoreState()


def build_story(doc: PrintableDoc) -> list:
    styles = build_styles()
    story: list = [make_title_band(doc, styles), Spacer(1, 10)]

    intro_panel = make_intro_panel(doc, styles)
    if intro_panel is not None:
        story.extend([intro_panel, Spacer(1, 10)])

    for section in doc.sections:
        story.append(make_section(section, styles))

    return story


def build_pdf(doc: PrintableDoc, output: Path):
    pdf = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=doc.title,
        author="Dragons & Distractions",
        subject="Ink-friendly printable",
    )
    pdf.build(build_story(doc), onFirstPage=on_page, onLaterPages=on_page)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for printable in PRINTABLES:
        parsed = parse_printable(printable["source"])
        output = OUTPUT_DIR / f"{printable['base']}-ink.pdf"
        build_pdf(parsed, output)
        print(f"Generated {output.name}")


if __name__ == "__main__":
    main()
