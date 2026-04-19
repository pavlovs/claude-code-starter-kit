# TEN RULES — the few that prevent 80% of issues

> Distilled from 3 weeks of intensive Claude Code use. Every rule has a concrete enforcement mechanism — not just a principle.

Read this once, end-to-end. Then re-read only the rules relevant to your current maturity level (`/statusreport` surfaces them for you).

---

## 1. Write rules, not reminders

**Why it fails without this**
Verbal corrections die with the session. You tell Claude "don't do X" in conversation, and next session Claude does X again. You've been "correcting" the same thing for weeks and nothing changed.

**Enforce**
After any correction, append the *rule that would have prevented the mistake* to `feedback.md` in the same session — before the next task. Not a description of the mistake. A rule.

**Example**
- BAD: `Claude used the wrong calendar ID in the morning brief`
- GOOD: `Always call gcal_list_events for all 3 calendar IDs (primary + imports). Querying only the primary misses imported calendars. BECAUSE imported calendars don't appear in the default list.`

---

## 2. Verify against code, not docs

**Why it fails without this**
Documentation drifts. `README.md` says the feature is "planned"; it shipped 3 commits ago. Claude recommends work based on stale docs and you end up with duplicate effort or conflicts with merged code.

**Enforce**
Before Claude recommends work or plans changes, it must read the actual current state: `git log`, the source files, live state. Not `ROADMAP.md`, not `PLAN.md`, not `ARCHITECTURE.md`. Those are drafts written by Claude in prior sessions.

**Example**
Before saying "next milestone should be X" — `git log --oneline | head -20` and read the last 3 commit messages. If the work is already done, update the plan doc instead.

---

## 3. Classify ownership on every task

**Why it fails without this**
You delegate a task. Claude sees it in `TASKS.md` but doesn't know if it's for Claude to execute or for you to do. Either Claude takes a task you meant to handle yourself, or "autonomous" tasks sit waiting for re-prompting.

**Enforce**
Every task in `TASKS.md` is tagged with exactly one of:
- `[ME]` — only you can do this (calls, decisions, signatures)
- `[AGENT]` — Claude executes autonomously
- `[TOGETHER]` — needs your input before Claude can proceed
- `[WIP]` — you're actively working on it; Claude doesn't touch

No tag = treat as `[ME]` by default.

**Example**
- `[ME] Call supplier about Q2 pricing`
- `[AGENT] Draft competitor comparison table | AC: 5 competitors, 4 axes, 1-paragraph summary`
- `[TOGETHER] Decide on feature X vs Y — need your preference`
- `[WIP] Finalize Q2 roadmap`

---

## 4. Acceptance criteria on autonomous tasks

**Why it fails without this**
You write `[AGENT] Research buyers for X` and Claude returns something you find unusable. Not Claude's fault — "research" and "usable" aren't defined. Ambiguous done = ambiguous output.

**Enforce**
Every `[AGENT]` task has a 1–2 line `| AC:` (acceptance criteria) field defining what "done" looks like. Claude self-verifies against it before marking `[x]`.

**Example**
- BAD: `[AGENT] Improve the dashboard`
- GOOD: `[AGENT] Add legend + source labels to pipeline dashboard | AC: legend visible on all 3 tabs, source label shows DB update timestamp`

---

## 5. Batch questions — never interrupt mid-task

**Why it fails without this**
You delegate a task. Claude starts, hits an ambiguity, asks one question. You answer. Claude hits another, asks. Repeat 5 times. Your flow is shredded. Feels "unagentic."

**Enforce**
At the start of any non-trivial task, Claude collects all ambiguities and blockers in ONE "Unblock me" section. You answer the whole block at once. Claude then works through without further interruption.

**Phrase for your `CLAUDE.md`:**
> Batch all questions into one ask. Never interrupt mid-task with single questions.

---

## 6. Session tags collapse context loading

**Why it fails without this**
Every session starts with "what are we working on today?" and 3–5 clarifying exchanges before Claude loads the right context. That's 10 minutes of ceremony per session.

**Enforce**
Define session tags in your `CLAUDE.md`, each mapped to:
- Which files to load
- What protocol to follow
- What to skip

Type the tag once, Claude loads the right context and follows the protocol. Zero-friction session start.

**Example**
```markdown
## Session tags

- [MORNING] — read TASKS.md, calendar for today, generate 1-page brief
- [REVIEW] — read-only mode, structured feedback, no writes
- [PROJECT-X] — load project-x/CLAUDE.md + project-x/TASKS.md
```

---

## 7. Documentation is a commit gate

**Why it fails without this**
Code ships but `ROADMAP.md` still says the feature is pending. Next session reads the stale doc, treats it as truth, recommends duplicate work. Rule #2 (verify against code) is the firefighter; this rule is the fire-prevention.

**Enforce**
Definition of done = code works + tests pass + docs updated + committed. Together, in one commit. Never ship code without the docs that describe it.

**Phrase for your `CLAUDE.md`:**
> Documentation is a commit gate. Before marking work complete: verify the relevant doc (roadmap, plan, architecture, learnings) reflects reality.

---

## 8. Never re-add deleted content

**Why it fails without this**
You edit a file, deliberately delete a section. Next session, Claude edits the same file and "helpfully" restores the deleted content — it read an earlier version from context. Deletions are intentional editorial choices; restoring them erodes trust fast.

**Enforce**
Before any edit to a file, Claude reads the current state of the file. Works only with what currently exists. If context suggests content that's not in the file, treat it as deliberately removed.

**Phrase for your `CLAUDE.md`:**
> Never re-add content that's been deleted. Read the current file state before any edit. Deletions are intentional.

---

## 9. Surface contradictions — never silently resolve

**Why it fails without this**
Two rules in your setup conflict. Claude picks one without telling you. Next session picks the other. Your behavior is unpredictable because you don't even know the rules contradict.

**Enforce**
When rules or instructions conflict, Claude names the contradiction explicitly and asks which wins. Never silent picks. The 10-second clarifying question saves the 10-minute debug later.

**Example**
> "Your CLAUDE.md says 'always use Sonnet for routine work' but your current task instruction says 'use Opus.' Which applies here?"

---

## 10. Self-check before delivering

**Why it fails without this**
Claude produces output. You read it. Obvious issue — wrong weekday, misaligned columns, a number that doesn't add up. You push back. Claude fixes it. You could have gotten the fixed version first time.

**Enforce**
Before presenting any output, Claude asks: *"Would the recipient push back on this?"* If yes, fix it first. The goal is correct output, not accepted output. Generator-and-reviewer being the same model has blind spots — but the question itself forces a second pass.

For high-stakes work, escalate: have a separate agent review the output before delivery. Generator and reviewer should be different instances.

---

## The meta-rule: apply rules at your level

At L1–L2: focus on rules 1, 3, 4, 8.
At L3: add rules 2, 9, 10.
At L4: add rules 5, 6, 7.
At L5: all ten, refined.

`/statusreport` surfaces the 3 most actionable rules for your current level.

---

*These rules come from accumulated mistakes. They're not principles — they're scar tissue.*
