# SETUP — what happens and what to read when

You've cloned the kit. Here's how to use it.

---

## The 3-step flow

```bash
git clone https://github.com/pavlovs/claude-code-starter-kit
cd claude-code-starter-kit
claude
```

Then:
```
/statusreport
```

That's the entire setup command. Everything else is Claude walking you through it.

---

## What `/statusreport` does

1. **Asks 4 questions:**
   - Which project directory to audit
   - How you use Claude Code (role signal)
   - Hours/day of use (intensity signal)
   - Biggest friction right now

2. **Scans two levels of your setup:**
   - Your target project directory (`CLAUDE.md`, `TASKS.md`, `feedback.md`, `.claude/`, etc.)
   - Your `~/.claude/` global setup (global CLAUDE.md, commands, skills, agents, hooks, settings)

3. **Scores you against the 5-level maturity ladder** (see `MATURITY.md`).

4. **Outputs a 30-line diagnosis:**
   - Current level
   - Pass/fail per level
   - 2–3 specific next steps to reach the next level
   - 3 rules from `TEN-RULES.md` most relevant to your current level
   - Personalized note based on your friction answer

5. **Offers to apply fixes — one at a time.** For each recommended fix, Claude asks: "Want me to copy this template? Walk you through filling it in? Or skip?" You approve each action individually. Read-only unless you say yes.

---

## What to read, in order

You don't need to read anything before running `/statusreport` — just clone and run. But once you have your diagnosis:

| Order | File | When to read it |
|---|---|---|
| 1 | `MATURITY.md` | Right after your first `/statusreport` — understand the 5 levels and where you're heading |
| 2 | `TEN-RULES.md` | This week — the 10 rules that prevent 80% of issues, each with an enforcement mechanism |
| 3 | `TOOLS.md` | When you hit L4–L5 and want to automate (hooks, skills, subagents) |
| 4 | `LINKS.md` | When you want to go deeper — 5 canonical sources, nothing else |

The templates in `templates/*.example` aren't meant to be read — they're meant to be **copied into your setup by `/statusreport`** with Claude walking you through customization.

---

## When to re-run `/statusreport`

- **Monthly** — tracks maturity drift (did you level up? regress?)
- **When setup feels off** — Claude is making mistakes you thought were solved
- **After a big workflow change** — new project, new tool, new team

Pull the latest kit anytime: `git pull` in the kit directory.

---

## Promote to global — run the skill from any project

Once you've run `/statusreport` once and trust it, copy the skills into your global skill directory so you don't need to `cd` into the kit each time:

```bash
# from the kit directory
mkdir -p ~/.claude/commands
cp .claude/commands/statusreport.md ~/.claude/commands/
cp .claude/commands/log-feedback.md ~/.claude/commands/
```

Now `/statusreport` runs from any project. The skill still asks which directory to audit — it no longer assumes the kit.

**To update later:**
```bash
cd claude-code-starter-kit && git pull && cp .claude/commands/*.md ~/.claude/commands/
```

**Why not symlink?** Symlinks work on Mac/Linux but not reliably on Windows. A plain `cp` + periodic re-pull is the simplest cross-platform pattern.

**Can I delete the kit repo after promoting?** Yes, but you'll lose the templates + examples that `/statusreport` copies from when applying fixes. Keep the kit repo around unless you're comfortable pointing Claude to template URLs manually.

---

## What this kit won't do

- Set up MCP servers (link to Anthropic docs in `LINKS.md`)
- Pick models for specific tasks (mention the tradeoff, don't prescribe)
- Give you role-specific workflows (too many variants — the kit is the generic core)
- Modify your files without explicit per-action approval

---

## Troubleshooting

**"`/statusreport` isn't showing up as a command."**
You need to open Claude Code *inside* the cloned kit directory (`cd claude-code-starter-kit && claude`). The skill is defined at `.claude/commands/statusreport.md` and only loads when CC runs with the kit as its working directory.

**"It scanned the wrong project directory."**
Re-run `/statusreport` and enter the correct absolute path when asked.

**"I already have a `CLAUDE.md` — will it overwrite?"**
No. The skill is idempotent. If a target file already exists, it shows you the diff against the template and lets you decide.

---

*Next: read `MATURITY.md` to understand the level your diagnosis puts you at.*
