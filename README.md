# Claude Code Starter Kit

**Interactive Claude Code setup advisor.** Clone it, run `/statusreport`, get personalized suggestions based on your current maturity level. Claude does the analysis and offers to apply fixes — you approve each one.

Distilled from three weeks of intensive Claude Code use. Encodes the few must-haves every user eventually learns the hard way.

---

## Quickstart

```bash
git clone https://github.com/pavlovs/claude-code-starter-kit
cd claude-code-starter-kit
claude
```

Then in Claude Code:

```
/statusreport
```

The skill will:

1. Ask which project directory you want to audit (and scan your `~/.claude/` global setup automatically)
2. Score your setup against a 5-level maturity ladder
3. Output your current level + 2–3 specific next actions
4. Offer to apply fixes (copy templates, walk you through filling CLAUDE.md, etc.) — you approve each one

It's read-only by default. Nothing gets written without your say-so.

---

## What's in here

| File | What it is |
|---|---|
| `SETUP.md` | What happens when you run `/statusreport` + sequence for reading the other docs |
| `MATURITY.md` | Level 0 → 5 maturity ladder with binary checklists |
| `TEN-RULES.md` | 10 distilled rules + concrete enforcement for each |
| `TOOLS.md` | Hooks, skills, subagents — what each is for and when |
| `LINKS.md` | 5 curated canonical sources for going deeper |
| `.claude/commands/statusreport.md` | The skill |
| `templates/*.example` | Starter CLAUDE.md, TASKS.md, feedback.md, anti-patterns.md |
| `examples/` | Working hooks, skills, subagents you can copy |

---

## Re-run monthly

Setup decays. Drop back into the kit dir and run `/statusreport` again — it'll tell you if you've drifted or leveled up.

Pull the latest kit anytime: `git pull`.

---

## License

MIT. Use freely. Attribution appreciated but not required.
