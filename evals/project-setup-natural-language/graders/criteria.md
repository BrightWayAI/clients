---
type: llm
weight: 1
---

The user reported a contract came back signed without typing `/project-setup`. A
successful response recognizes this as an explicit signed-contract signal and starts
the project-setup workflow (or asks a natural next question within that workflow,
such as locating the file), rather than asking the user to type the command
themselves. It must not write anything to Drive or any connector before presenting a
plan for confirmation. A failing response ignores the request, asks the user to type
`/project-setup`, or performs a write action without first showing a confirmable plan.
