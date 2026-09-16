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
    "doc_title": {"name": "Calibri", "size_pt": 22, "bold": true, "color": "0B131C"},
    "title": {"name": "Calibri", "size_pt": 14, "bold": false, "color": "444444"},
    "byline": {"name": "Calibri", "size_pt": 11, "bold": false, "color": "444444"},
    "draft_banner": {"name": "Calibri", "size_pt": 10, "bold": true, "color": "B00020"},
    "section_heading": {"name": "Calibri", "size_pt": 13, "bold": true, "color": "0B131C"},
    "body": {"name": "Calibri", "size_pt": 11, "bold": false, "color": "000000"},
    "table_header": {"name": "Calibri", "size_pt": 10, "bold": true, "color": "FFFFFF"},
    "table_body": {"name": "Calibri", "size_pt": 10, "bold": false, "color": "000000"},
    "footer": {"name": "Calibri", "size_pt": 9, "bold": false, "color": "666666"}
  },
  "colors": {"rule": "444444", "table_header_fill": "444444"},
  "footer_text": "Confidential | {client} x {vendor}",
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
