# MATURITY — the 5-level ladder

> Where you are and what's next. `/statusreport` tells you your current level automatically.

The ladder maps to the few must-haves that every Claude Code user eventually builds — usually after learning the hard way. You don't need to climb fast. You need to climb **in order**. Skipping levels compounds complexity you don't understand yet.

---

## L0 — Vanilla CC

**What it looks like**
- Claude Code installed. No `CLAUDE.md`. Ad-hoc sessions.
- You re-explain your context in every session.
- Works fine for one-off lookups. Fails for anything recurring.

**Checklist**
- [x] You have Claude Code installed and can run `claude` in a terminal.

**Signal you're ready for L1**
You've opened CC more than three times this week and re-typed the same context.

**Common trap**
Thinking you don't need a `CLAUDE.md` because "my project is simple."

---

## L1 — Identity anchor

**What it looks like**
- A `CLAUDE.md` file exists (either in your project or at `~/.claude/CLAUDE.md`).
- It contains: who you are, how you want Claude to communicate (working style / tone), and any hard constraints.
- Claude stops drifting between sessions — you get consistent tone and depth without re-briefing.

**Checklist**
- [ ] `CLAUDE.md` exists
- [ ] It has an identity section (who you are, role, context)
- [ ] It has a working-style section (tone, verbosity, what to avoid)
- [ ] At least one hard constraint (e.g., "never hallucinate", "no sycophancy")

**Time to reach:** ~30 minutes

**Signal you're ready for L2**
You're delegating tasks to Claude and noticing yourself saying "oh that was supposed to be something I do myself, not Claude" — you need ownership tags.

**Common trap**
Writing a 500-line `CLAUDE.md`. Keep it under 200. Longer files get ignored.

---

## L2 — Task discipline

**What it looks like**
- A `TASKS.md` file at your project root.
- Every task is tagged with one of: `[ME]` / `[AGENT]` / `[TOGETHER]` / `[WIP]`.
- `[AGENT]` tasks include a 1–2 line acceptance criteria (AC) field.
- You stop wondering "did Claude do that task or am I supposed to?"

**Checklist**
- [ ] L1 passes
- [ ] `TASKS.md` exists at the project root
- [ ] At least 2 distinct ownership tags in use
- [ ] `[AGENT]` tasks have `| AC:` fields

**Time to reach:** ~1 hour

**Signal you're ready for L3**
Claude makes the same mistake twice across sessions. You need a mechanism that makes corrections stick.

**Common trap**
Writing `[AGENT]` tasks without acceptance criteria. Ambiguous done = ambiguous output. Claude marks `[x]` without actually finishing.

---

## L3 — Feedback loop

**What it looks like**
- A `feedback.md` file with open issues Claude reads at session start.
- Every time Claude makes a mistake you correct, you write the RULE (not the mistake) to `feedback.md`, same session.
- Over time, recurring patterns get promoted to `anti-patterns.md`.
- A third file — `learnings.md` — captures meta-observations about Claude Code itself (not project-specific mistakes, but how the tool behaves: "SessionStart hooks need `hookSpecificOutput` wrapper", "model X drifts on long prompts").
- Mistakes stop recurring across sessions. You can feel the drift stop.

**The three-tier knowledge loop:**
1. `feedback.md` — fresh corrections ("Always X BECAUSE Y") — intake
2. `anti-patterns.md` — recurring patterns, named — promoted
3. `learnings.md` — meta-knowledge about Claude Code as a tool — orthogonal

Without (3), you'll re-discover the same tool quirks in every project. See REPO-GUIDE for structure.

**Checklist**
- [ ] L2 passes
- [ ] `feedback.md` exists
- [ ] Has entries modified in the last 14 days (this is the hardest part — it's a habit, not a file)
- [ ] `anti-patterns.md` exists with at least one pattern
- [ ] `learnings.md` exists (even with 1–2 entries)

**Time to reach:** ~1 week to form the habit

**Signal you're ready for L4**
Your `CLAUDE.md` is bloating (> 200 lines). You're starting to need different contexts for different work modes. Or: you work across 3+ projects and keep copy-pasting rules.

**Common trap**
Writing descriptions of mistakes instead of rules. "Claude used the wrong file path" is a description. "Always run `ls config/` before assuming the config file location" is a rule. Rules prevent recurrence; descriptions just document regret.

---

## L4 — Protocols + context layers + methodology

**What it looks like**
- `CLAUDE.md` is split: core behavioral rules stay in `CLAUDE.md`, topic-specific rules move to `.claude/rules/*.md` files.
- Session tags like `[MORNING]` or `[PROJECT-X]` map to specific protocols + context loads.
- Sessions start with a single tag and Claude loads the right context automatically — no re-briefing.
- For non-trivial work, you follow the **brainstorm → spec → plan → implement → review** loop (see WORKFLOW.md).
- You start using the **3-agent loop** on complex builds: a planner agent, an implementer agent, a reviewer agent — each with isolated context and scoped tools. See WORKFLOW.md.

**Optional branch — if you work across 3+ projects:**
- Move cross-project rules (identity, working-style, hard constraints) to `~/.claude/rules/*.md`.
- Each project's `CLAUDE.md` becomes short (~50 lines) and project-specific.
- Skills you use everywhere move to `~/.claude/commands/`. See REPO-GUIDE — Global vs project.
- Skip this branch if you work in a single project. It adds complexity without payoff.

**Checklist**
- [ ] L3 passes
- [ ] `.claude/rules/*.md` exists with at least 1 file OR session tags defined in `CLAUDE.md`
- [ ] At least one session tag has a documented protocol
- [ ] You've used the plan → implement → review loop at least once (with subagents or manually)
- [ ] *If multi-project:* `~/.claude/rules/` populated, per-project `CLAUDE.md` short

**Time to reach:** ~1 day for protocols; another day for methodology habits.

**Signal you're ready for L5**
You're doing the same manual setup at the start of every session (reading files, checking state). Time to let hooks do it.

**Common trap**
Creating session tags with no protocol attached. A tag is only useful if it triggers deterministic behavior. Second trap: shipping complex work without the plan → implement → review split — generator and reviewer being the same model creates blind spots.

---

## L5 — Automation

**What it looks like**
- Hooks configured in `settings.json`: at minimum `SessionStart` (inject current date + state) and `Stop` (nudge Claude to keep going mid-task).
- Skills for repeated workflows (`/brief`, `/audit-X`, `/plan-milestone`).
- Subagents with `memory: project` for scoped expertise that accumulates knowledge across sessions.
- Your setup actively prevents mistakes — not just reminds you of rules.

**Checklist**
- [ ] L4 passes
- [ ] `settings.json` has hooks configured for at least one event
- [ ] At least one `.claude/agents/*.md` exists
- [ ] At least one skill you invoke more than once a week

**Time to reach:** ~2–3 days

**Signal you've "arrived"**
A new task you used to do manually now fits into an existing hook, skill, or subagent. You're no longer adding tools — you're refining them.

**Common trap**
Over-engineering L5 before L3 is solid. If your feedback loop isn't working, automating broken processes just automates the failures.

---

## What belongs at each level — index

Every concept in this kit has a home L-level. Use this index to skip sections that aren't relevant yet.

| Concept | Level | Doc |
|---|---|---|
| `CLAUDE.md` with identity + working-style | L1 | REPO-GUIDE |
| `TASKS.md` with 4 ownership tags + AC on [AGENT] | L2 | REPO-GUIDE, WORKFLOW |
| `feedback.md` intake loop (Always/Never BECAUSE) | L3 | REPO-GUIDE, `/log-feedback` |
| `anti-patterns.md` promoted patterns | L3 | REPO-GUIDE |
| `learnings.md` meta-knowledge about Claude Code | L3 | REPO-GUIDE |
| Role-specific context files | L4 | REPO-GUIDE |
| `.claude/rules/*.md` split when CLAUDE.md > 150 lines | L4 | REPO-GUIDE |
| Session tags + protocols | L4 | REPO-GUIDE |
| Brainstorm → spec → plan methodology | L4 | WORKFLOW |
| 3-agent loop (planner / implementer / reviewer) | L4 | WORKFLOW, `.claude/agents/` |
| Global vs project split (`~/.claude/rules/`) | L4 (optional) | REPO-GUIDE |
| Skills (`/slash-command`) | L4 | TOOLS |
| `SessionStart` hook (date + git state) | L5 | HOOKS |
| `Stop` nudge hook | L5 | HOOKS |
| `PreToolUse` / `PostToolUse` validators | L5 | HOOKS |
| PreCommit doc-gate (git hook) | L5 | HOOKS |
| Subagents with `memory: project` | L5 | TOOLS |

---

## The meta-rule

Don't climb faster than your habits. An L1 user with a great `CLAUDE.md` outperforms an L5 user with neglected `feedback.md`. The ladder's value is *the habits at each level*, not the artifacts.

*Run `/statusreport` to check your current level.*
