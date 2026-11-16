---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Dry run: load the `/sow` instructions with the Skill tool (loading them runs nothing),
then walk Step 5.5 against this exact scenario without executing any step.

You drafted a SOW from a pasted proposal. The proposal says Phase 1 costs $40k–$55k and
Phase 2 costs $30k–$52k, with kickoff on March 3. Your draft has a Phase 1
not-to-exceed of $55,000, a Phase 2 not-to-exceed of $50,000, kickoff on March 3, and
Net 30 payment terms taken from the template defaults. The cortex verifier returns:
Phase 1 cap pass, Phase 2 cap fail (the proposal's top of range is $52k), kickoff pass.

Tell me what you send the verifier, what you tell me, and what happens next. Then tell
me what changes if cortex is not installed.
