---
type: llm
weight: 1
---

The user asked in plain language for weekly client status drafts, never typing `/client-status`. A successful response recognizes this as a request for the client-status workflow and attempts to draft status updates from available project/calendar/CRM/cortex evidence, without first asking the user to type the explicit command. A failing response ignores the request, asks the user to run `/client-status` themselves, or produces a generic non-status-shaped answer.
