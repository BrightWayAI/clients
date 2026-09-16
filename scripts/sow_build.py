#!/usr/bin/env python3
"""Render a Statement of Work .docx from a derived format spec.

Reads FORMAT SPEC front-matter out of `clients.sow-template.md` (or, absent
one, `references/sow-format-default.md`) and exposes a small builder API used
by the `/sow` command:

    from sow_build import SOWDoc
    doc = SOWDoc(spec_path="<config-root>/plugins/clients.sow-template.md")
    doc.title_block("Statement of Work", "Acme Corp x BrightWay AI", draft=True)
    doc.heading(1, "Relationship of the Parties")
    doc.para("This Statement of Work (**SOW**) is entered into ...")
    doc.bullets(["Item one", "Item two"])
    doc.table(["Phase", "Not-to-Exceed"], [["Phase 1", "$24,000"]], widths=[3, 2])
    doc.signature("Acme Corp", "BrightWay AI")
    doc.save("Acme SOW.docx")

No visual defaults are hardcoded beyond `references/sow-format-default.md`,
used only when no user spec exists.
"""
import re
import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


DEFAULT_SPEC = {
    "page": {"width_in": 8.5, "height_in": 11, "margin_top_in": 1, "margin_bottom_in": 1, "margin_left_in": 1, "margin_right_in": 1},
    "roles": {
        "doc_title": {"name": "Calibri", "size_pt": 22, "bold": True, "color": "0B131C"},
        "title": {"name": "Calibri", "size_pt": 14, "bold": False, "color": "444444"},
        "section_heading": {"name": "Calibri", "size_pt": 13, "bold": True, "color": "0B131C"},
        "body": {"name": "Calibri", "size_pt": 11, "bold": False, "color": "000000"},
        "table_header": {"name": "Calibri", "size_pt": 10, "bold": True, "color": "FFFFFF"},
        "table_body": {"name": "Calibri", "size_pt": 10, "bold": False, "color": "000000"},
    },
    "colors": {"rule": "444444", "table_header_fill": "444444"},
    "footer_text": "Confidential | {client} x {vendor}",
    "footer_has_page_field": True,
    "signature_layout": "two_column_borderless",
    "draft_banner": False,
}


def _parse_spec_from_markdown(md_text):
    """Extract a fenced ```json spec block from clients.sow-template.md."""
    m = re.search(r"```json\s*\n(.*?)\n```", md_text, re.S)
    if not m:
        return None
    return json.loads(m.group(1))


def load_spec(spec_path=None, default_path=None):
    if spec_path:
        try:
            with open(spec_path) as f:
                text = f.read()
            parsed = _parse_spec_from_markdown(text)
            if parsed:
                return parsed
        except FileNotFoundError:
            pass
    if default_path:
        try:
            with open(default_path) as f:
                parsed = _parse_spec_from_markdown(f.read())
                if parsed:
                    return parsed
        except FileNotFoundError:
            pass
    return DEFAULT_SPEC


def _rgb(hexstr):
    if not hexstr:
        return None
    hexstr = hexstr.lstrip("#")
    return RGBColor.from_string(hexstr.upper())


def _set_cell_shading(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def _set_col_widths(table, widths_in):
    """Fixed layout — set tblGrid gridCol widths explicitly, per column and cell."""
    table.autofit = False
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    grid = tbl.find(qn("w:tblGrid"))
    for gridcol, w in zip(grid.findall(qn("w:gridCol")), widths_in):
        gridcol.set(qn("w:w"), str(int(w * 1440)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_in):
            cell.width = Inches(w)


def _add_page_field(paragraph):
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr)
    run._r.append(fld_char2)


class SOWDoc:
    def __init__(self, spec_path=None, default_path="references/sow-format-default.md"):
        self.spec = load_spec(spec_path, default_path)
        self.doc = Document()
        sec = self.doc.sections[0]
        p = self.spec["page"]
        sec.page_width = Inches(p["width_in"])
        sec.page_height = Inches(p["height_in"])
        sec.top_margin = Inches(p["margin_top_in"])
        sec.bottom_margin = Inches(p["margin_bottom_in"])
        sec.left_margin = Inches(p["margin_left_in"])
        sec.right_margin = Inches(p["margin_right_in"])
        self._section_num = 0
        self._setup_footer(sec)

    def _role(self, name):
        return self.spec["roles"].get(name, DEFAULT_SPEC["roles"].get(name, DEFAULT_SPEC["roles"]["body"]))

    def _apply_run_role(self, run, role_name):
        r = self._role(role_name)
        run.font.name = r.get("name", "Calibri")
        if r.get("size_pt"):
            run.font.size = Pt(r["size_pt"])
        run.font.bold = bool(r.get("bold"))
        run.font.italic = bool(r.get("italic"))
        if r.get("color"):
            run.font.color.rgb = _rgb(r["color"])

    def _setup_footer(self, sec):
        footer = sec.footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        text_pattern = self.spec.get("footer_text", "Confidential | {client} x {vendor}")
        run = p.add_run(text_pattern.split("{")[0].strip() + "  ")
        self._apply_run_role(run, "footer") if "footer" in self.spec["roles"] else self._apply_run_role(run, "table_body")
        if self.spec.get("footer_has_page_field", True):
            p.add_run("Page ")
            _add_page_field(p)

    def title_block(self, title, subtitle=None, draft=False):
        if draft or self.spec.get("draft_banner"):
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("DRAFT FOR REVIEW — NOT EXECUTED")
            self._apply_run_role(run, "draft_banner" if "draft_banner" in self.spec["roles"] else "title")
            run.font.bold = True
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        self._apply_run_role(run, "doc_title")
        if subtitle:
            p2 = self.doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run2 = p2.add_run(subtitle)
            self._apply_run_role(run2, "title")
        rule_color = self.spec.get("colors", {}).get("rule")
        if rule_color:
            self._add_horizontal_rule(rule_color)

    def _add_horizontal_rule(self, hex_color):
        p = self.doc.add_paragraph()
        p_pr = p._p.get_or_add_pPr()
        border = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "12")
        bottom.set(qn("w:color"), hex_color)
        border.append(bottom)
        p_pr.append(border)

    def heading(self, _unused_level, text):
        self._section_num += 1
        p = self.doc.add_paragraph()
        run = p.add_run(f"{self._section_num}.  {text}")
        self._apply_run_role(run, "section_heading")
        return self._section_num

    def _add_markdown_bold_runs(self, paragraph, text, role_name):
        parts = re.split(r"(\*\*.*?\*\*)", text)
        for part in parts:
            if not part:
                continue
            bold = part.startswith("**") and part.endswith("**")
            run = paragraph.add_run(part[2:-2] if bold else part)
            self._apply_run_role(run, role_name)
            if bold:
                run.font.bold = True

    def para(self, text):
        p = self.doc.add_paragraph()
        self._add_markdown_bold_runs(p, text, "body")
        return p

    def bullets(self, items):
        for item in items:
            p = self.doc.add_paragraph(style=None)
            p.paragraph_format.left_indent = Inches(0.25)
            run_bullet = p.add_run("•  ")
            self._apply_run_role(run_bullet, "body")
            self._add_markdown_bold_runs(p, item, "body")

    def table(self, header, rows, widths=None):
        n_cols = len(header)
        t = self.doc.add_table(rows=1, cols=n_cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        header_fill = self.spec.get("colors", {}).get("table_header_fill")
        for i, h in enumerate(header):
            cell = t.rows[0].cells[i]
            cell.paragraphs[0].text = ""
            run = cell.paragraphs[0].add_run(h)
            self._apply_run_role(run, "table_header")
            if header_fill:
                _set_cell_shading(cell, header_fill)
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                cells[i].paragraphs[0].text = ""
                run = cells[i].paragraphs[0].add_run(str(val))
                self._apply_run_role(run, "table_body")
        if widths:
            _set_col_widths(t, widths)
        return t

    def signature(self, party_a, party_b):
        t = self.doc.add_table(rows=3, cols=2)
        _set_col_widths(t, [3.25, 3.25])
        labels = [(party_a, party_b), ("Signature: _______________________", "Signature: _______________________"),
                  ("Name / Title / Date", "Name / Title / Date")]
        for r_idx, (left, right) in enumerate(labels):
            for c_idx, val in enumerate((left, right)):
                cell = t.rows[r_idx].cells[c_idx]
                cell.paragraphs[0].text = ""
                run = cell.paragraphs[0].add_run(val)
                self._apply_run_role(run, "table_body")
                if r_idx == 0:
                    run.font.bold = True
        return t

    def exhibit(self, title):
        self.doc.add_page_break()
        p = self.doc.add_paragraph()
        run = p.add_run(title)
        self._apply_run_role(run, "section_heading")
        return p

    def save(self, path):
        self.doc.save(path)
        return path


if __name__ == "__main__":
    import sys
    d = SOWDoc(spec_path=sys.argv[1] if len(sys.argv) > 1 else None)
    d.title_block("Statement of Work", "Sample Client x BrightWay AI", draft=True)
    d.heading(1, "Relationship of the Parties")
    d.para("This is a **smoke test** render of the SOW builder.")
    d.heading(2, "Compensation")
    d.table(["Phase", "Not-to-Exceed"], [["Phase 1", "$24,000"], ["Phase 2", "$50,000"]], widths=[3, 2.5])
    d.signature("Sample Client Inc.", "BrightWay AI")
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/sow_smoke_test.docx"
    d.save(out)
    print(f"wrote {out}")
