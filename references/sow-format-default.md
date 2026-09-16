# SOW default format spec

Used by `scripts/sow_build.py` only when no user-derived
`<config-root>/plugins/clients.sow-template.md` exists (fresh install with no
sample yet, or the sample supplied was a PDF/content-only source). Generic,
unbranded styling — nothing here should be mistaken for a real firm's house
format. Once a real sample is captured via `/setup-projects`, this file is
never read again for that user.

```json
{
  "page": {"width_in": 8.5, "height_in": 11, "margin_top_in": 1, "margin_bottom_in": 1, "margin_left_in": 1, "margin_right_in": 1},
  "roles": {
    "doc_title": {"name": "Calibri", "size_pt": 22, "bold": true, "italic": false, "color": "0B131C", "space_after_pt": 6},
    "title": {"name": "Calibri", "size_pt": 14, "bold": false, "italic": false, "color": "444444", "space_after_pt": 12},
    "byline": {"name": "Calibri", "size_pt": 11, "bold": false, "italic": false, "color": "444444"},
    "draft_banner": {"name": "Calibri", "size_pt": 10, "bold": true, "italic": false, "color": "B00020", "space_after_pt": 6},
    "section_heading": {"name": "Calibri", "size_pt": 13, "bold": true, "italic": false, "color": "0B131C", "space_before_pt": 14, "space_after_pt": 6},
    "body": {"name": "Calibri", "size_pt": 11, "bold": false, "italic": false, "color": "000000", "space_after_pt": 6, "line_spacing": 1.08},
    "table_header": {"name": "Calibri", "size_pt": 10, "bold": true, "italic": false, "color": "FFFFFF", "space_after_pt": 0},
    "table_body": {"name": "Calibri", "size_pt": 10, "bold": false, "italic": false, "color": "000000", "space_after_pt": 0},
    "signature_caption": {"name": "Calibri", "size_pt": 10, "bold": false, "italic": false, "color": "000000"},
    "footer": {"name": "Calibri", "size_pt": 9, "bold": false, "italic": false, "color": "666666", "alignment": "center"}
  },
  "colors": {"rule": "444444", "table_header_fill": "444444"},
  "heading_number_format": "{n}.  {title}",
  "bullet_indent_in": 0.25,
  "tables": [{"col_widths_in": [3.5, 2.5], "borders": {"style": "single", "color": "B7B7B7", "size": 4}, "cell_margins_in": {"top": 0.06, "left": 0.08, "bottom": 0.06, "right": 0.08}}],
  "footer_text": "Confidential | {client} x {vendor} | Page {page}",
  "footer_has_page_field": true,
  "signature_layout": "two_column_borderless",
  "draft_banner": false
}
```

## Section skeleton (generic default)

Engagement-specific (fill from the proposal): Scope of Services, Phases &
Timeline, Deliverables, Pricing & Payment Terms, Assumptions, Out of Scope,
Change Requests, Acceptance Criteria, Client Inputs, Open Questions.

Boilerplate (adapt only party names / defined terms): Relationship of the
Parties, Representations & Warranties, Indemnification, Non-Solicitation,
Confidentiality, Termination, General Provisions, Governing Law, Signatures.
