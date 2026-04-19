# Claude Code Starter Kit

**Interactive Claude Code setup advisor.** Clone it, run `/statusreport`, get personalized suggestions based on your current maturity level. Claude does the analysis and offers to apply fixes — you approve each one.

Distilled from three weeks of intensive Claude Code use. Encodes the few must-haves every user eventually learns the hard way.

---

## Quickstart

**Prerequisites:** Claude Code installed + signed in. If not: https://docs.claude.com/en/docs/claude-code.

```bash
git clone https://github.com/pavlovs/claude-code-starter-kit
cd claude-code-starter-kit
claude
```

Then in Claude Code:

```
/statusreport
```

The audit scans *your current working directory* and `~/.claude/`. To audit a different project, either rerun Claude Code inside that project (after the global promotion step below) or give the skill an absolute path when it asks.

The skill will:

1. Ask which project directory you want to audit (and scan your `~/.claude/` global setup automatically)
2. Score your setup against a 5-level maturity ladder
3. Output your current level + 2–3 specific next actions
4. Offer to apply fixes (copy templates, walk you through filling CLAUDE.md, etc.) — you approve each one

It's read-only by default. Nothing gets written without your say-so.

### What the diagnosis looks like

```
## Your current level: L2

✅ L1 — Identity anchor: CLAUDE.md has identity + working-style sections
✅ L2 — Task discipline: TASKS.md has 8 tagged entries across [ME]/[AGENT]/[WIP]
❌ L3 — Feedback loop: feedback.md missing
❌ L4 — Protocols + context layers
❌ L5 — Automation

## Next steps to reach L3

1. Copy `templates/feedback.md.example` → `./feedback.md` — intake log for corrections
2. After the next mistake, log the RULE (not the description) that would have prevented it
3. Read rule #1 — "Write rules, not reminders"

## Rules most actionable at your level

- #3 Classify ownership on every task
- #4 Acceptance criteria on autonomous tasks
- #8 Never re-add deleted content

## Based on your answers

You said "Claude forgets rules between sessions" — that's exactly what L3 solves.
The feedback.md + same-session rule-writing discipline is the single highest-leverage
habit in this kit.
```

Claude then asks per fix: *"Want me to copy the feedback.md template and walk you through filling it in?"* — yes/no per action. No batch confirmations.

---

## What's in here

| File | What it is |
|---|---|
| `SETUP.md` | What happens when you run `/statusreport` + sequence for reading the other docs |
| `MATURITY.md` | Level 0 → 5 maturity ladder with binary checklists |
| `TEN-RULES.md` | 10 distilled rules + concrete enforcement for each |
| `REPO-GUIDE.md` | Repo infrastructure: what goes in CLAUDE.md vs. elsewhere, global vs. project boundary |
| `WORKFLOW.md` | Brainstorm → spec → plan → TDD → review. The loop that prevents rework |
| `HOOKS.md` | Hook pack: SessionStart, pre-commit doc verifier, dead-link checker, Stop nudge |
| `TOOLS.md` | Hooks, skills, subagents — what each is for and when |
| `LINKS.md` | 5 curated canonical sources for going deeper |
| `.claude/commands/statusreport.md` | The skill that runs the audit |
| `.claude/commands/log-feedback.md` | Skill for capturing corrections as rules (keeps feedback loop alive) |
| `.claude/rules/starter-rules.md.example` | Example modular rules file (when CLAUDE.md outgrows ~150 lines) |
| `.claude/agents/starter-reviewer.md.example` | Example generic reviewer subagent |
| `.claude/agents/planner.md.example` | Planner agent for the 3-agent loop (L4) — read-only, produces plan |
| `.claude/agents/implementer.md.example` | Implementer agent for the 3-agent loop — executes plan, writes code |
| `.claude/agents/plan-reviewer.md.example` | Reviewer agent for the 3-agent loop — reviews impl vs. spec + plan |
| `templates/*.example` | Starter CLAUDE.md, TASKS.md, feedback.md, anti-patterns.md, learnings.md |
| `examples/` | Working hooks, skills, subagents you can copy |

---

## Re-run monthly

Setup decays. Drop back into the kit dir and run `/statusreport` again — it'll tell you if you've drifted or leveled up.

Pull the latest kit anytime: `git pull`.

### Want to run `/statusreport` from any project?

After your first run, copy the skill into your global skill directory so you don't need the kit repo each time:

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/statusreport.md ~/.claude/commands/
cp .claude/commands/log-feedback.md ~/.claude/commands/
```

Now `/statusreport` and `/log-feedback` work from any project. Re-run `git pull && cp .claude/commands/*.md ~/.claude/commands/` to update.

---

## License

MIT. Use freely. Attribution appreciated but not required.
