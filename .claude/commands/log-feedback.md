---
name: log-feedback
description: Capture a correction and turn it into a rule that prevents recurrence. Writes the rule to feedback.md (and anti-patterns.md if recurring). Keeps the self-improvement loop alive — rule #1 from TEN-RULES.md.
---

# /log-feedback — capture a correction as a rule

You are helping the user log a correction from a previous interaction (with you or another Claude session) as a persistent rule. Without this loop, the same mistakes recur indefinitely.

## Why this skill exists

Corrections are perishable. If a user tells you "stop doing X" and you don't write a rule that prevents X in future sessions, you will repeat the mistake next week. This skill forces the capture step.

The output is a rule in the format **"Always/Never X **because** Y"** — because the `because` clause is what lets the rule generalize to novel situations.

---

## Protocol

### Step 1 — understand the correction

Use `AskUserQuestion` with the following 3 questions batched:

1. **"What did Claude do wrong?"**
   - Options: `Hallucinated a fact/number/name` / `Re-added deleted content` / `Skipped verification` / `Wrong context loaded` / `Format/tone mismatch` / `Other`
   - Use "Other" for free-text if none fit.

2. **"Is this a one-off or a recurring pattern?"**
   - Options: `One-off (just log it)` / `Recurring (promote to anti-patterns)` / `Unsure — log to feedback.md for now`

3. **"Should this change CLAUDE.md or just feedback?"**
   - Options: `Just feedback/anti-patterns (behavioral rule)` / `Update CLAUDE.md too (structural change — new tag, protocol, constraint)` / `Unsure`

If the user chooses "Other" on Q1, ask a short free-text follow-up: *"In one sentence: what happened?"*

---

### Step 2 — draft the rule

Based on the answers, draft a rule in the format:

```
Always/Never <what> BECAUSE <why>.
```

**BAD examples (descriptions, not rules):**
- "Claude used the wrong date in the morning brief"
- "Claude re-added the section the user had deleted"

**GOOD examples (rules that prevent recurrence):**
- "Always cross-check the system date against live signals (recent email timestamps, git commit dates) BECAUSE the system clock can be stale and acting on a wrong date creates dated output errors."
- "Never re-add content that has been deleted BECAUSE deletions are intentional editorial choices — read the current file state before any edit."

**Key moves:**
- Use imperative phrasing (Always/Never), not descriptive ("Claude should...")
- The `BECAUSE` clause names the underlying principle, not the specific instance
- Make the rule general enough to apply to novel situations of the same type

Show the draft to the user in chat and ask: *"Does this capture it? Edit if not."*

Iterate until the user confirms.

---

### Step 3 — pick the target file

Based on Q2:

- **One-off** → append to `feedback.md` under an "Open Issues" section.
- **Recurring** → append to `anti-patterns.md` with a named pattern (ALL-CAPS-WITH-HYPHENS, e.g., `STALE-DATE`, `ZOMBIE-CONTENT`).
- **Unsure** → default to `feedback.md`; the user can promote later.

Ask the user: *"Confirm target: `<path>` — proceed?"*

If the target file doesn't exist yet, offer to create it from the template in `templates/feedback.md.example` or `templates/anti-patterns.md.example`.

---

### Step 4 — write the entry

**For feedback.md:**
```markdown
## Open Issues

### <YYYY-MM-DD> — <short label>
<rule in Always/Never BECAUSE format>

**Context:** <1-line summary of what triggered this>
```

**For anti-patterns.md:**
```markdown
## <NAME-OF-PATTERN>

**Detection:** <how to notice this failure mode>
**Rule:** <Always/Never BECAUSE>
**First logged:** <YYYY-MM-DD>
```

Append (don't overwrite). Read the file first, locate the right section, then `Edit` to add the new entry. Never use `Write` on an existing file — you'll lose content.

---

### Step 5 — update CLAUDE.md if structural

If the user said "structural change" in Q3:
- Ask which section of `CLAUDE.md` this changes (or if it's a new section)
- Show the proposed edit and confirm before writing
- Keep changes surgical — one section, no reformatting of adjacent content

Examples of structural changes:
- New session tag: add to the "Session tags" section
- New Critical rule: add to the top-N list
- New context file to load: update the session protocols

---

### Step 6 — confirm and close

Output a summary:

```
## Logged

**Rule:** <the rule>
**Target:** <file path>
**Also updated:** <CLAUDE.md section, or "none">

Next session will load this on start. To verify: `git diff <file>` before committing.
```

---

## Rules for this skill

- **Always use `AskUserQuestion`** for the 3 structured questions — don't let the user type them unstructured.
- **Never write without confirmation** of the final rule text AND target path.
- **Never overwrite** — always append. Read the current file first.
- **Never add the same rule twice** — if an existing entry covers this pattern, propose an update to that entry instead of a duplicate.
- **Keep the rule short.** 1–2 sentences. If it needs more, the user is probably trying to log two rules — split them.

---

## When NOT to use this skill

- Trivial typo corrections ("oh I meant X not Y") — don't log.
- User feedback about a one-conversation issue that can't recur — don't log.
- Praise or confirmation of good output — that's not a correction.

If you're unsure whether a correction is worth logging, default to logging — the cost of a stale entry is lower than the cost of repeating the mistake.
