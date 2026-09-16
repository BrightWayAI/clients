#!/usr/bin/env python3
"""Derive a FORMAT SPEC + SECTION SKELETON from a sample SOW .docx.

Usage: python3 sow_extract.py <sample.docx> [--out spec.json]

Reads run/paragraph/table properties with python-docx (not by eyeballing
rendered text) and prints a JSON spec that `clients.sow-template.md` is
built from. Also prints a markdown summary table for the setup confirmation
step.
"""
import json
import sys
import argparse
from docx import Document
from docx.shared import Pt, Emu


def _pt(v):
    return round(v.pt, 1) if v is not None else None


def _emu_in(v):
    return round(v / 914400, 2) if v is not None else None


def font_role(paragraph):
    """Best-effort role guess from style name + first run properties."""
    style = (paragraph.style.name or "").lower()
    text = paragraph.text.strip()
    if "title" in style:
        return "doc_title" if len(text) > 3 else "title"
    if "heading 1" in style or "heading1" in style:
        return "section_heading"
    if "heading" in style:
        return "sub_heading"
    return "body"


def run_spec(run):
    font = run.font
    return {
        "name": font.name,
        "size_pt": _pt(font.size),
        "bold": bool(font.bold),
        "italic": bool(font.italic),
        "color": str(font.color.rgb) if font.color and font.color.rgb else None,
    }


def extract(path):
    doc = Document(path)
    sec = doc.sections[0]
    spec = {
        "page": {
            "width_in": _emu_in(sec.page_width),
            "height_in": _emu_in(sec.page_height),
            "margin_top_in": _emu_in(sec.top_margin),
            "margin_bottom_in": _emu_in(sec.bottom_margin),
            "margin_left_in": _emu_in(sec.left_margin),
            "margin_right_in": _emu_in(sec.right_margin),
        },
        "roles": {},
        "sections": [],
        "tables": [],
        "footer_text": None,
        "signature_layout": None,
        "draft_banner": False,
        "colors": {},
    }

    seen_roles = {}
    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        role = font_role(p)
        if role not in seen_roles and p.runs:
            r = p.runs[0]
            seen_roles[role] = run_spec(r)
            pf = p.paragraph_format
            seen_roles[role]["space_before_pt"] = _pt(pf.space_before)
            seen_roles[role]["space_after_pt"] = _pt(pf.space_after)
            seen_roles[role]["alignment"] = str(pf.alignment) if pf.alignment else None
        if role == "section_heading":
            spec["sections"].append({"heading": p.text.strip(), "note": ""})
        if "draft" in p.text.lower() and "review" in p.text.lower():
            spec["draft_banner"] = True
    spec["roles"] = seen_roles

    for t in doc.tables:
        widths = [_emu_in(c.width) for c in t.columns]
        header_cells = t.rows[0].cells if t.rows else []
        header_fill = None
        header_font = None
        if header_cells:
            tc_pr = header_cells[0]._tc.tcPr
            if tc_pr is not None:
                shd = tc_pr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}shd")
                if shd is not None:
                    header_fill = shd.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fill")
            if header_cells[0].paragraphs and header_cells[0].paragraphs[0].runs:
                header_font = run_spec(header_cells[0].paragraphs[0].runs[0])
        spec["tables"].append({
            "col_widths_in": widths,
            "header_fill": header_fill,
            "header_font": header_font,
        })

    # Footer: page-number field position + static text pattern
    footer = sec.footer
    footer_text_parts = []
    has_page_field = False
    for p in footer.paragraphs:
        footer_text_parts.append(p.text)
        xml = p._p.xml
        if "PAGE" in xml or "fldSimple" in xml:
            has_page_field = True
    spec["footer_text"] = " | ".join(t for t in footer_text_parts if t.strip())
    spec["footer_has_page_field"] = has_page_field

    # Signature block: look for a table near the end with two columns, no borders
    if doc.tables:
        last = doc.tables[-1]
        if len(last.columns) == 2:
            tbl_pr = last._tbl.tblPr
            borderless = tbl_pr.find(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblBorders"
            ) is None
            spec["signature_layout"] = "two_column_borderless" if borderless else "two_column_bordered"

    return spec


def to_markdown_table(spec):
    lines = ["| Element | Value |", "|---|---|"]
    p = spec["page"]
    lines.append(f"| Page | {p['width_in']}in x {p['height_in']}in, margins T{p['margin_top_in']}/B{p['margin_bottom_in']}/L{p['margin_left_in']}/R{p['margin_right_in']} |")
    for role, r in spec["roles"].items():
        lines.append(f"| Font — {role} | {r['name']} {r['size_pt']}pt{' bold' if r['bold'] else ''}{' color ' + r['color'] if r['color'] else ''} |")
    for i, t in enumerate(spec["tables"]):
        lines.append(f"| Table {i+1} | widths {t['col_widths_in']}, header fill {t['header_fill']} |")
    lines.append(f"| Footer | {spec['footer_text']} (page field: {spec['footer_has_page_field']}) |")
    lines.append(f"| Signature block | {spec['signature_layout']} |")
    lines.append(f"| Draft banner used | {spec['draft_banner']} |")
    lines.append(f"| Sections found | {len(spec['sections'])} |")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("docx_path")
    ap.add_argument("--out", default=None, help="write JSON spec to this path")
    args = ap.parse_args()

    result = extract(args.docx_path)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, indent=2)
    print(to_markdown_table(result))
    print()
    print(json.dumps(result, indent=2))
