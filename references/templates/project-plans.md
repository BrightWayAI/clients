# Project Plan Templates

_Edit this file to match your firm's offerings. The starter ships with three example offerings; replace, remove, or add as needed._

Use the appropriate template for the active offering. Adjust week numbers based on the actual engagement timeline. If multiple offerings are active, combine phases into a single integrated plan.

This plan is project-zone content. Name deliverable phases after the SOW's actual
phase names at runtime (e.g., "Phase 1A — Marketplace Inventory"), not the generic
phase names below — these are starter defaults only. Never add cost, rate, or cap
figures to a populated plan; run the pricing-leak check before presenting it (see
`commands/project-setup.md` Step 6.3).

---

## AI Operating Model & Governance

**Engagement duration:** Typically 6–8 weeks

**Offering-specific interview questions:**
- How many stakeholder interviews planned? Which roles/levels?
- Any existing AI policies, governance attempts, or prior AI investments already in place?
- Is this org early in AI adoption, mid-journey, or trying to course-correct?

---

**Phase 1 — Assess**
_Goal: Understand the client's current AI landscape, readiness, and gaps_
- Send kickoff prep email; confirm logistics and pre-reads
- Run kickoff call; send recap within 24 hrs
- Schedule stakeholder interviews; send calendar invites
- Conduct all stakeholder interviews; save notes to 02_Discovery
- Complete AI tool and workflow inventory
- Synthesize findings → draft AI Readiness Report
- Share draft with client (3 business day review cycle)
- Deliver final AI Readiness Report

Owner: You (primary) / Client (interviews, review)
Timeline: Weeks 1–3

**Phase 2 — Design**
_Goal: Build the operating model — structure, governance, policies, and use case roadmap_
- Define AI governance structure and decision rights
- Assign AI-related roles and responsibilities
- Draft core policy templates (AI use policy, data governance, acceptable use)
- Define AI use case roadmap and prioritization framework
- Draft AI Operating Model document
- Share draft with client (5 business day review cycle)
- Incorporate feedback → finalize

Owner: You (primary) / Client (review and input)
Timeline: Weeks 3–6

**Phase 3 — Align**
_Goal: Activate leadership alignment and hand off a usable set of tools_
- Build executive presentation summarizing findings and recommendations
- Facilitate leadership alignment session
- Incorporate session outputs into final document set
- Package all final deliverables in 03_Deliverables
- Run close-out call
- Send engagement summary within 48 hrs

Owner: You (primary) / Client (alignment session)
Timeline: Weeks 6–8

---

## Custom Agent Systems

**Engagement duration:** Typically 8–12 weeks (varies by complexity)

**Offering-specific interview questions:**
- What workflow is being automated? Walk through the current manual process.
- What systems or data sources does the agent need to connect to?
- What does "done" look like — how will success be measured post-launch?
- Any known technical constraints (IT restrictions, data governance, security requirements)?
- Has the client done any AI/automation work before, or is this their first?

---

**Phase 1 — Scope & Design**
_Goal: Fully understand the target workflow and design the agent before writing a line of code_
- Send kickoff prep email; confirm logistics
- Run kickoff call; send recap within 24 hrs
- Map current workflow end-to-end (swim lanes, handoffs, decision points)
- Identify automation touchpoints and agent boundaries
- Draft Agent Design Document + Technical Spec
- Share design docs with client for sign-off
- ⚠️ NO BUILD WORK BEGINS until design is signed off

Owner: You + Client
Timeline: Weeks 1–2

**Phase 2 — Build**
_Goal: Build a working agent in a staged environment, iterating on client feedback_
- Set up dev environment; confirm all access and credentials received
- Build core agent functionality (alpha)
- Internal QA pass before sharing externally
- Share alpha with client — Loom walkthrough + written notes
- Incorporate feedback; build beta
- Second review cycle if needed

Owner: You (build) / Client (feedback)
Timeline: Weeks 2–7 (varies)

**Phase 3 — Integrate & Handoff**
_Goal: Deploy to production, train users, and hand off everything needed to maintain it_
- Connect agent to production systems
- Run user acceptance testing (UAT) — client signs off
- Production deployment (coordinate with client IT/ops timeline)
- Record user training walkthrough
- Deliver User Guide + Maintenance Notes to 03_Deliverables
- Run handoff call
- Close-out call + engagement summary

Owner: You + Client (UAT, deployment coordination)
Timeline: Weeks 7–10+

---

## Learning Production System

**Engagement duration:** Typically 8–12 weeks (scales with content volume)

**Offering-specific interview questions:**
- What type of content? (courses, microlearning, job aids, videos, assessments, etc.)
- Current production volume and desired future volume?
- What LMS or publishing platform do they use?
- Who reviews and approves content — what's the sign-off chain?
- Is the bottleneck writing speed, subject matter expert access, formatting, or something else?

---

**Phase 1 — Audit & Design**
_Goal: Understand the content library, current process, and where AI fits_
- Send kickoff prep email; confirm logistics
- Run kickoff call; send recap within 24 hrs
- Conduct content audit — catalog existing content, formats, quality levels
- Map current production workflow (who does what, where it breaks down)
- Design AI-assisted production workflow — where Claude/AI inserts
- Deliver Content Inventory + AI Workflow Map to 03_Deliverables

Owner: You (primary) / Client (content access, process walk-through)
Timeline: Weeks 1–2

**Phase 2 — Pilot**
_Goal: Prove the AI workflow works on real content before scaling_
- Select 2–3 pilot content pieces with client (representative of the full library)
- Build AI-assisted production pipeline for pilot pieces
- Produce pilot assets using new workflow
- Internal QA pass before sharing
- Share pilot assets with client (3–5 day review cycle)
- Incorporate feedback
- Finalize Production Playbook v1 based on pilot learnings

Owner: You (primary) / Client (pilot selection, review)
Timeline: Weeks 2–5

**Phase 3 — Scale**
_Goal: Run full production volume; deliver all assets and a self-sustaining playbook_
- Run full production batches per SOW volume targets
- QA each batch before client delivery
- Deliver assets in batches or all at once (per SOW)
- Refine Production Playbook based on full run learnings
- Deliver final content assets + QA Checklist + Production Playbook to 03_Deliverables
- Close-out call + engagement summary

Owner: You (primary) / Client (ongoing review and approval)
Timeline: Weeks 5–10+

---

## Immediate Next Step Logic

After presenting the project plan, always end with one specific next action. Use this decision tree:

1. **No kickoff call scheduled yet** → "Send the kickoff prep email to [Primary Contact Name]. Want me to draft it now?"
2. **Kickoff call scheduled but prep email not sent** → "Draft and send the kickoff prep email — it should go out 48 hrs before the call. Want me to write it?"
3. **Kickoff call done but recap not sent** → "Send the kickoff recap with action items while the call is fresh. Want me to draft it based on what you just shared?"
4. **Everything above is done** → "Log the engagement in your CRM and create the Drive folder structure. Then the first real delivery task is [first task from Phase 1]."

Always offer to execute the immediate next step if it's a communication, document, or planning task.

---

## Adding your own offerings

To add a new offering:

1. Add a new section above with: full name, short name, duration, offering-specific interview questions
2. Add 2–4 phases with name, goal, key tasks, owner, timeline
3. Update `references/templates/drive-structure.md` to add the offering's folder-02 layout
4. Update `references/user-context.md` to register the offering in your catalog

The starter ships with three example offerings — replace them with your own as needed.
