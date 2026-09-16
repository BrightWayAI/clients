# SOW content schema

`scripts/sow_build.py` accepts a JSON object through `--content`. The content
file contains engagement facts and approved clause text; visual decisions stay
in `clients.sow-template.md`.

```json
{
  "title": "Statement of Work",
  "subtitle": "Client Inc. x Vendor LLC",
  "client": "Client Inc.",
  "vendor": "Vendor LLC",
  "draft": true,
  "sections": [
    {
      "heading": "Scope of Services",
      "level": 1,
      "page_break_before": false,
      "blocks": [
        {"type": "paragraph", "text": "Text with **optional bold spans**."},
        {"type": "bullets", "items": ["First deliverable", "Second deliverable"]},
        {
          "type": "table",
          "header": ["Phase", "Not-to-Exceed"],
          "rows": [["Phase 1", "$24,000"]],
          "widths": [3.5, 2.5]
        }
      ]
    }
  ],
  "signature": {"party_a": "Client Inc.", "party_b": "Vendor LLC"}
}
```

Supported block types are `paragraph`, `bullets`, `table`, and `page_break`.
Every table row must have the same number of cells as its header. Omit
`widths` to use compatible widths from the derived format spec. A document
without `signature` omits the signature block.
