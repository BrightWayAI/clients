#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx>=1.1,<2"]
# ///
"""Derive a format spec, section skeleton, and section text from a sample SOW."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from docx import Document
    from docx.oxml.ns import qn
except ModuleNotFoundError as exc:  # pragma: no cover - runtime preflight
    raise SystemExit(
        "python-docx is required. Run this script with `uv run scripts/sow_extract.py ...` "
        "or install the dependency from scripts/requirements-sow.txt."
    ) from exc


def _pt(value: Any) -> float | None:
    return round(value.pt, 1) if value is not None else None


def _emu_in(value: Any) -> float | None:
    return round(value / 914400, 2) if value is not None else None


def _first(*values: Any) -> Any:
    return next((value for value in values if value is not None), None)


def font_role(paragraph: Any) -> str:
    """Best-effort semantic role from the paragraph style."""
    style = (paragraph.style.name or "").lower()
    text = paragraph.text.strip()
    if "draft" in text.lower() and "review" in text.lower():
        return "draft_banner"
    if "subtitle" in style:
        return "title"
    if "title" in style:
        return "doc_title"
    if "heading 1" in style or "heading1" in style:
        return "section_heading"
    if "heading" in style:
        return "sub_heading"
    if re.match(r"^\d+[.)]\s+", text) and paragraph.runs and paragraph.runs[0].bold:
        return "section_heading"
    return "body"


def _effective_font(run: Any, paragraph: Any, document: Any) -> dict[str, Any]:
    """Resolve direct formatting through paragraph/character styles and Normal."""
    direct = run.font
    run_style = run.style.font if run.style is not None else None
    para_style = paragraph.style.font if paragraph.style is not None else None
    normal = document.styles["Normal"].font
    color = None
    for font in (direct, run_style, para_style, normal):
        if font is not None and font.color is not None and font.color.rgb is not None:
            color = str(font.color.rgb)
            break
    return {
        "name": _first(
            direct.name,
            run_style.name if run_style is not None else None,
            para_style.name if para_style is not None else None,
            normal.name,
            "Calibri",
        ),
        "size_pt": _pt(
            _first(
                direct.size,
                run_style.size if run_style is not None else None,
                para_style.size if para_style is not None else None,
                normal.size,
            )
        ),
        "bold": bool(
            _first(
                direct.bold,
                run_style.bold if run_style is not None else None,
                para_style.bold if para_style is not None else None,
                normal.bold,
                False,
            )
        ),
        "italic": bool(
            _first(
                direct.italic,
                run_style.italic if run_style is not None else None,
                para_style.italic if para_style is not None else None,
                normal.italic,
                False,
            )
        ),
        "color": color,
    }


def _paragraph_spec(paragraph: Any, document: Any) -> dict[str, Any]:
    run = next((candidate for candidate in paragraph.runs if candidate.text), paragraph.runs[0])
    result = _effective_font(run, paragraph, document)
    paragraph_format = paragraph.paragraph_format
    style_format = paragraph.style.paragraph_format if paragraph.style is not None else None
    result.update(
        {
            "space_before_pt": _pt(
                _first(
                    paragraph_format.space_before,
                    style_format.space_before if style_format is not None else None,
                )
            ),
            "space_after_pt": _pt(
                _first(
                    paragraph_format.space_after,
                    style_format.space_after if style_format is not None else None,
                )
            ),
            "line_spacing": _first(
                paragraph_format.line_spacing,
                style_format.line_spacing if style_format is not None else None,
            ),
            "alignment": int(paragraph.alignment) if paragraph.alignment is not None else None,
        }
    )
    return result


def _border_spec(table: Any) -> dict[str, Any] | None:
    borders = table._tbl.tblPr.find(qn("w:tblBorders"))
    if borders is None:
        return None
    values = []
    colors = []
    sizes = []
    for edge in borders:
        values.append(edge.get(qn("w:val")))
        colors.append(edge.get(qn("w:color")))
        sizes.append(edge.get(qn("w:sz")))
    active_values = [value for value in values if value]
    if active_values and all(value in {"none", "nil"} for value in active_values):
        return {"style": "none"}
    result: dict[str, Any] = {"style": _first(*active_values, "single")}
    if any(colors):
        result["color"] = _first(*colors)
    if any(sizes):
        result["size"] = int(_first(*sizes))
    return result


def _cell_margins(cell: Any) -> dict[str, float]:
    margins: dict[str, float] = {}
    tc_mar = cell._tc.get_or_add_tcPr().find(qn("w:tcMar"))
    if tc_mar is None:
        return margins
    for edge in ("top", "left", "bottom", "right"):
        node = tc_mar.find(qn(f"w:{edge}"))
        if node is not None and node.get(qn("w:w")):
            margins[edge] = round(int(node.get(qn("w:w"))) / 1440, 3)
    return margins


def _footer_pattern(paragraph: Any) -> str:
    """Preserve static footer text and replace a Word PAGE field with `{page}`."""
    parts: list[str] = []
    for element in paragraph._p.iter():
        if element.tag == qn("w:t") and element.text:
            parts.append(element.text)
        elif element.tag == qn("w:instrText") and "PAGE" in (element.text or "").upper():
            parts.append("{page}")
    return "".join(parts)


def extract(path: str | Path) -> dict[str, Any]:
    document = Document(path)
    section = document.sections[0]
    spec: dict[str, Any] = {
        "page": {
            "width_in": _emu_in(section.page_width),
            "height_in": _emu_in(section.page_height),
            "margin_top_in": _emu_in(section.top_margin),
            "margin_bottom_in": _emu_in(section.bottom_margin),
            "margin_left_in": _emu_in(section.left_margin),
            "margin_right_in": _emu_in(section.right_margin),
        },
        "roles": {},
        "sections": [],
        "tables": [],
        "footer_text": None,
        "footer_has_page_field": False,
        "signature_layout": None,
        "draft_banner": False,
        "colors": {},
    }

    seen_roles: dict[str, dict[str, Any]] = {}
    current_section: dict[str, Any] | None = None
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
        role = font_role(paragraph)
        if role not in seen_roles and paragraph.runs:
            seen_roles[role] = _paragraph_spec(paragraph, document)
        if role == "section_heading":
            heading = re.sub(r"^\d+[.)]\s+", "", text)
            current_section = {"heading": heading, "note": "", "body": []}
            spec["sections"].append(current_section)
        elif current_section is not None:
            current_section["body"].append(text)
        if "draft" in text.lower() and "review" in text.lower():
            spec["draft_banner"] = True
    spec["roles"] = seen_roles

    for table in document.tables:
        widths = [_emu_in(column.width) for column in table.columns]
        header_cells = table.rows[0].cells if table.rows else []
        header_fill = None
        header_font = None
        cell_margins: dict[str, float] = {}
        if header_cells:
            tc_pr = header_cells[0]._tc.tcPr
            if tc_pr is not None:
                shading = tc_pr.find(qn("w:shd"))
                if shading is not None:
                    header_fill = shading.get(qn("w:fill"))
            paragraph = header_cells[0].paragraphs[0] if header_cells[0].paragraphs else None
            if paragraph is not None and paragraph.runs:
                header_font = _paragraph_spec(paragraph, document)
            cell_margins = _cell_margins(header_cells[0])
        table_spec = {
            "col_widths_in": widths,
            "header_fill": header_fill,
            "header_font": header_font,
            "borders": _border_spec(table),
            "cell_margins_in": cell_margins,
        }
        spec["tables"].append(table_spec)
        if header_fill and "table_header_fill" not in spec["colors"]:
            spec["colors"]["table_header_fill"] = header_fill
        if header_font and "table_header" not in spec["roles"]:
            spec["roles"]["table_header"] = header_font

    footer_text_parts = []
    for paragraph in section.footer.paragraphs:
        footer_text_parts.append(_footer_pattern(paragraph))
        xml = paragraph._p.xml
        if "PAGE" in xml or "fldSimple" in xml:
            spec["footer_has_page_field"] = True
            if "footer" not in spec["roles"] and paragraph.runs:
                spec["roles"]["footer"] = _paragraph_spec(paragraph, document)
    spec["footer_text"] = " | ".join(value for value in footer_text_parts if value.strip())

    if document.tables:
        last = document.tables[-1]
        if len(last.columns) == 2:
            borders = _border_spec(last)
            borderless = borders is None or borders.get("style") == "none"
            spec["signature_layout"] = "two_column_borderless" if borderless else "two_column_bordered"
            spec["signature_col_widths_in"] = [_emu_in(column.width) for column in last.columns]

    return spec


def to_markdown_table(spec: dict[str, Any]) -> str:
    lines = ["| Element | Value |", "|---|---|"]
    page = spec["page"]
    lines.append(
        f"| Page | {page['width_in']}in x {page['height_in']}in, margins "
        f"T{page['margin_top_in']}/B{page['margin_bottom_in']}/"
        f"L{page['margin_left_in']}/R{page['margin_right_in']} |"
    )
    for role, values in spec["roles"].items():
        style = " bold" if values.get("bold") else ""
        color = f" color {values['color']}" if values.get("color") else ""
        lines.append(f"| Font - {role} | {values.get('name')} {values.get('size_pt')}pt{style}{color} |")
    for index, table in enumerate(spec["tables"]):
        lines.append(
            f"| Table {index + 1} | widths {table['col_widths_in']}, "
            f"header fill {table['header_fill']}, borders {table['borders']} |"
        )
    lines.append(
        f"| Footer | {spec['footer_text']} (page field: {spec['footer_has_page_field']}) |"
    )
    lines.append(f"| Signature block | {spec['signature_layout']} |")
    lines.append(f"| Draft banner used | {spec['draft_banner']} |")
    lines.append(f"| Sections found | {len(spec['sections'])} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx_path")
    parser.add_argument("--out", help="write JSON extraction to this path")
    args = parser.parse_args(argv)

    result = extract(args.docx_path)
    if args.out:
        destination = Path(args.out).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(to_markdown_table(result))
    print()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
