---
name: statusreport
description: Interactive audit of the user's Claude Code setup. Scans their target project + ~/.claude/ global setup, scores against a 5-level maturity ladder, outputs personalized next-step suggestions, and offers to apply fixes with per-action user approval. Read-only by default.
---

# /statusreport — Claude Code Setup Advisor

You are running an interactive audit of the user's Claude Code setup. Your job is to:

1. Scan two levels (user's target project + their `~/.claude/` global setup)
2. Score against the 5-level maturity ladder
3. Output a scannable diagnosis with specific next steps
4. Offer to apply fixes — one at a time, user approves each

**Core rule:** Read-only by default. Never write or modify files without explicit per-action user approval via `AskUserQuestion`.

---

## Phase 1 — Scope gathering

Use `AskUserQuestion` to ask the following. Batch them into ONE question call with 4 questions:

1. **"Which project directory do you want to audit?"**
   - Default: user's `$HOME` (for auditing just global setup)
   - Options: provide 2–3 plausible paths if you can infer from the shell cwd's parent dir. Otherwise offer "Enter custom path" and let them type.

2. **"How are you using Claude Code today?"**
   - Options: `Software development` / `Product management` / `Data / analytics work` / `Other knowledge work`
   - Used to tailor the recommendation language (not the core diagnosis).

3. **"How many hours/day do you use Claude Code?"**
   - Options: `< 1` / `1–3` / `3–6` / `6+`
   - Used to gauge realistic target maturity level.

4. **"Biggest friction right now?"**
   - Options: `Claude forgets rules between sessions` / `Wastes time asking for context I already gave` / `Makes confident mistakes` / `I don't have a good workflow yet`
   - Used to surface the most relevant rules in Phase 4.

Store the answers — you'll use them in Phase 4.

---

## Phase 2 — Scan (both levels)

Do NOT ask the user what to look for. Scan deterministically.

### Global setup — `~/.claude/`

Use `Glob` / `Read` to check existence + extract key signals. Check both supported layouts for each kind of artifact — report whichever is present:

- `~/.claude/CLAUDE.md` — exists? Contains identity section? Contains working-style section?
- `~/.claude/rules/*.md` — any rules files?
- `~/.claude/commands/*.md` — count, list names (single-file skill layout)
- `~/.claude/skills/*/SKILL.md` — count, list names (folder-based skill layout)
- `~/.claude/agents/*.md` — count, list names
- `~/.claude/hooks/*` — any scripts?
- `~/.claude/settings.json` — exists? Contains `"hooks"` key with at least one event configured?

### Project setup — at the user-provided path

- `CLAUDE.md` — exists at project root? Also check `.claude/CLAUDE.md` (both are valid). Contains identity + working-style sections?
- `TASKS.md` — exists? Grep for `\[ME\]`, `\[AGENT\]`, `\[TOGETHER\]`, `\[WIP\]` — at least two tags present?
- `feedback.md` — exists? Has any entries (non-empty content section)? Has entries modified in last 14 days?
- `anti-patterns.md` — exists?
- `learnings.md` — exists? (Third tier of the knowledge loop — meta-knowledge about Claude Code as a tool.)
- `.claude/` — exists?
- `.claude/commands/*.md` + `.claude/skills/*/SKILL.md` — count files in each (both layouts valid)
- `.claude/agents/*.md`, `.claude/rules/*.md`, `.claude/hooks/*` — count files in each
- `.claude/agents/planner.md`, `implementer.md`, `plan-reviewer.md` — does the user have the 3-agent loop configured? (L4 signal.)
- `.claude/settings.json` AND `.claude/settings.local.json` — exists? Either has `"hooks"` configured?

> **Path access note:** If the user-provided audit target is outside the current Claude Code working directory, you may not be able to read it. If a Read/Glob fails due to path access, tell the user: "I can't read outside the current working directory. Either rerun Claude Code from the target project, or use `/add-dir <path>` to add it to this session." Then pause until they confirm.

Collect all findings into a mental map. Do NOT output them yet.

---

## Phase 3 — Score against maturity ladder

Binary checks. Each level requires ALL preceding levels to also pass.

### L1 — Identity anchor
- PASS if: `CLAUDE.md` exists (project OR global) AND contains an identity-style heading (e.g., `## About me`, `## Identity`, `## Who I am`) AND contains a working-style-style heading (e.g., `## Working style`, `## Tone`, `## Response style`).

### L2 — Task discipline
- PASS if: L1 passed AND `TASKS.md` exists in the project AND contains at least 2 distinct tags from `[ME]`, `[AGENT]`, `[TOGETHER]`, `[WIP]`.

### L3 — Feedback loop
- PASS if: L2 passed AND `feedback.md` exists AND has non-empty content (more than just headers) AND has been modified in the last 14 days (check mtime if possible; otherwise check for dated entries).
- **Bonus signal (note in evidence line):** `learnings.md` also exists — user has the full 3-tier knowledge loop.

### L4 — Protocols + context layers + methodology
- PASS if: L3 passed AND at least ONE of the following is true:
  - `.claude/rules/*.md` exists with at least 1 file (rules split)
  - `~/.claude/rules/*.md` exists with at least 1 file (global split — multi-project operator)
  - `CLAUDE.md` defines at least one session tag like `[MORNING]`, `[PROJECT-X]`, etc.
  - `.claude/agents/planner.md` AND `implementer.md` AND `plan-reviewer.md` (or equivalent reviewer) all exist (3-agent loop)
- **Bonus signals:**
  - Multi-project operator: `~/.claude/rules/` has 2+ files (note in evidence)
  - 3-agent loop active: all three agents present (note in evidence)

### L5 — Automation
- PASS if: L4 passed AND (`~/.claude/settings.json` OR `.claude/settings.json` OR `.claude/settings.local.json`) has `hooks` configured for at least one event AND at least one agent file exists in either `~/.claude/agents/*.md` or `.claude/agents/*.md`.

Determine the user's current level = highest level that passed. If all fail, they are L0.

---

## Phase 4 — Output diagnosis

Output in chat. Scannable, under 40 lines. Use this exact structure:

```
## Your current level: L<N>

✅ L1 — Identity anchor <one-line evidence: e.g., "global CLAUDE.md has identity + working-style sections">
✅ L2 — Task discipline <one-line evidence>
❌ L3 — Feedback loop <one-line gap: e.g., "missing: feedback.md in project dir">
❌ L4 — Protocols + context layers
❌ L5 — Automation

## Recommended next steps to reach L<N+1>

1. <Specific action with path reference>
2. <Specific action>
3. <Specific action>

## Relevant rules at your level (from TEN-RULES.md)

- #<X> <rule name> — https://github.com/pavlovs/claude-code-starter-kit/blob/main/TEN-RULES.md#<anchor>
- #<Y> <rule name> — https://github.com/pavlovs/claude-code-starter-kit/blob/main/TEN-RULES.md#<anchor>
- #<Z> <rule name> — https://github.com/pavlovs/claude-code-starter-kit/blob/main/TEN-RULES.md#<anchor>

## Based on your answers

<2-3 sentence personalized note. Use Phase 1 answers. Example: "You mentioned 'Claude forgets rules between sessions' as your top friction — that's exactly what L3 (feedback loop) solves. The feedback.md + same-session-write-the-rule discipline is the single highest-leverage habit.">
```

### Rules to surface per level — always exactly 3

- At L0 / L1: rules #1 (write rules, not reminders), #2 (verify against code), #10 (self-check before delivering)
- At L2: rules #3 (task ownership), #4 (acceptance criteria), #8 (never re-add deleted content)
- At L3: rules #1 (reinforces the loop), #9 (surface contradictions), #10 (self-check before delivering)
- At L4: rules #5 (batch questions), #6 (session tags), #7 (docs are a commit gate)
- At L5: rules #7 (docs commit gate), #9 (surface contradictions), #10 (self-check) — at automation level, the failure modes are subtle

### Tailor by friction answer (override the level defaults if a stronger match)
- "forgets rules between sessions" → #1 (write rules), #8 (never re-add deleted), #9 (surface contradictions)
- "wastes time asking for context I already gave" → #6 (session tags), #1 (write rules), #5 (batch questions)
- "makes confident mistakes" → #2 (verify against code), #10 (self-check), #9 (surface contradictions)
- "no good workflow yet" → #1 (write rules), #3 (task ownership), #4 (AC on autonomous tasks)

---

## Phase 5 — Offer to apply fixes

For EACH recommended next step that involves a file action, ask the user individually via `AskUserQuestion`. Do NOT batch "yes to all" — every fix gets its own explicit approval.

Format for each offer:

> "Want me to copy `templates/<file>.example` → `<project-dir>/<file>` now? I'll also walk you through filling in the `<CUSTOMIZE>` placeholders."
>
> Options:
> - `Yes, copy and walk me through`
> - `Yes, just copy it`
> - `No, I'll do it myself`
> - `Skip this — not relevant to me`

On user approval:
- **"Copy and walk through":** Copy the file from `templates/` to the target path, then read the placeholders and ask the user to fill each one, editing the file inline as they answer.
- **"Just copy":** Copy the file, print the path, move to next offer.
- **"No" / "Skip":** Note the decline, move to next offer.

### Rules for file actions
- **Idempotent:** If the target file already exists, do NOT overwrite. Instead, tell the user: "You already have `<path>`. Want me to show you the diff against the template?" — and use `Read` on both, display diff, let user decide.
- **Never edit files you weren't asked to edit.** Only the specific file in the current offer.
- **Confirm the path before every write.** E.g., "Copying to `C:/Users/You/myproject/feedback.md` — correct?"

---

## Phase 6 — Completion summary

After all offers have been processed, output a final summary:

```
## /statusreport complete

### Applied
- <path> (from templates/<file>.example)
- <path> (filled in sections: X, Y, Z)

### Declined or skipped
- <fix name>
- <fix name>

### Next audit
Re-run /statusreport in ~1 month or when setup feels off.

### Keep learning
- MATURITY.md — https://github.com/pavlovs/claude-code-starter-kit/blob/main/MATURITY.md
- TEN-RULES.md — https://github.com/pavlovs/claude-code-starter-kit/blob/main/TEN-RULES.md
- TOOLS.md (when you're ready for automation) — https://github.com/pavlovs/claude-code-starter-kit/blob/main/TOOLS.md
- LINKS.md (5 canonical sources) — https://github.com/pavlovs/claude-code-starter-kit/blob/main/LINKS.md
```

---

## Special modes

### Dry-run
If the user's initial invocation includes `--dry-run` or they ask "just show me the diagnosis, don't ask to apply fixes", skip Phase 5 entirely and go straight to Phase 6 with empty Applied/Declined sections.

### Re-audit
If the user re-runs `/statusreport` and their level is the same as before (detectable if `feedback.md` mentions a prior audit date), acknowledge it: "Still at L<N> — no regression. Here's what's relevant at your level:" and focus on the rules surfacing instead of the fixes.

---

## Failure modes to avoid

- **Don't ask questions before Phase 1.** You have everything you need to start.
- **Don't lecture the user.** Keep outputs scannable, not educational. Links carry the education.
- **Don't batch fixes.** Per-action confirmation is the rule.
- **Don't recommend L5 to an L1 user.** Focus on L(current + 1). Mention L(current + 2) as "after that" only.
- **Don't invent findings.** If you can't read a file, say so. Don't guess.
- **Don't write to a path the user didn't confirm.** Even if the path seems obvious.
