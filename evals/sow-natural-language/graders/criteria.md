---
type: llm
weight: 1
---

The user asked in plain language for a Statement of Work without typing `/sow`.
A successful response recognizes and starts the SOW workflow, requests or resolves
the proposal and approved template/boilerplate inputs, keeps the output a draft,
and does not ask the user to invoke another command. A failing response ignores the
request, asks the user to type `/sow`, invents missing legal boilerplate, or claims
the document was visually reviewed without rendering it.
