# TOOLS — hooks, skills, subagents

> Three tools at Claude Code's core. Ignore them until L4. At L5, they become how you enforce the 10 rules deterministically instead of by habit.

---

## Hooks

**What it is**
Shell commands Claude Code runs automatically at lifecycle events. The harness executes them — not Claude. Deterministic.

**Lifecycle events**
- `SessionStart` — runs when you open Claude Code
- `PreCompact` — runs before the context window gets compressed
- `Stop` — runs when Claude stops mid-turn
- `PreToolUse` / `PostToolUse` — runs before/after tool calls (optionally filtered by tool name)
- `UserPromptSubmit` — runs when you submit a message

**When to use**
- Inject current date + git state at session start (so Claude never has stale date)
- Save session state before compaction (so nothing valuable gets lost)
- Nudge Claude to keep going when it stops mid-task ("did you actually finish?")
- Log all bash commands for audit trail on prod operations
- Validate file references in .md edits (warn, never block)

**When NOT to use**
- For anything the LLM should reason about — hooks are deterministic, use skills instead
- For anything that needs user interaction — hooks can't ask questions
- As a replacement for missing CLAUDE.md rules — hooks enforce, rules teach

**Minimal working example**
See `examples/hook-session-start.py` and `examples/hook-stop-nudge.json`.

**Canonical docs**
https://docs.claude.com/en/docs/claude-code/hooks

---

## Skills

**What it is**
Scoped procedures Claude invokes by name (slash commands like `/statusreport`, `/brief`, `/plan-milestone`). Each skill is a `.md` file with frontmatter and instructions Claude follows when you invoke it.

**Location** (all valid, Claude Code loads any of them)
- `.claude/commands/<name>.md` — single-file project skill (this kit uses this layout)
- `.claude/skills/<name>/SKILL.md` — folder-based project skill (supports assets in the same folder)
- `~/.claude/commands/<name>.md` — single-file global skill (available in every project)
- `~/.claude/skills/<name>/SKILL.md` — folder-based global skill

Start with single-file (`commands/<name>.md`). Move to folder-based (`skills/<name>/SKILL.md`) only when the skill needs companion files (templates, scripts, example data).

**When to use**
- Any workflow you execute more than once a week (morning brief, status report, code review)
- Anything that benefits from a checklist Claude follows step-by-step
- Anything you'd otherwise paste as a prompt every time

**When NOT to use**
- One-off tasks — just ask Claude directly
- Things that need to run automatically — use a hook
- Things requiring persistent state across sessions — use a subagent with `memory:`

**Minimal working example**
See `examples/skill-new-task.md` — a simple skill that prompts Claude to create a new structured task.
See `.claude/commands/statusreport.md` in this repo for a richer example.

**Canonical docs**
https://docs.claude.com/en/docs/claude-code/skills

---

## Subagents

**What it is**
Isolated Claude instances with scoped tools, scoped models, and optionally their own persistent memory. Invoked via the `Agent` tool. Don't share your conversation context unless you explicitly pass it.

**Location**
- Project-local: `.claude/agents/<name>.md`
- Global: `~/.claude/agents/<name>.md`

**When to use**
- Parallel work — run 3 independent agents on unrelated questions at once
- Specialized expertise — a code-reviewer agent that only does code review
- Review gates — a second agent reviews the first agent's output (generator/reviewer split)
- Tasks needing isolated context — so the main conversation doesn't bloat with research output
- Work with persistent state — `memory: project` frontmatter makes the agent accumulate knowledge across sessions

**When NOT to use**
- Simple edits you could do yourself — agents spawn a whole new context; wasteful for 3 Edit calls
- Tasks that depend heavily on main-conversation context — the agent won't see it unless you pre-extract into the prompt
- As a replacement for a skill — skills are cheaper and simpler

**Minimal working example**
See `examples/subagent-explorer.md` — a subagent scoped to read-only exploration with no write tools.

**Canonical docs**
https://docs.claude.com/en/docs/claude-code/sub-agents

---

## Decision tree — which tool do I need?

**"I want Claude to automatically do X at session start / before compaction / when it stops."**
→ **Hook.** Deterministic, no LLM reasoning needed.

**"I want to invoke X by name whenever I need it."**
→ **Skill.** Slash command. One prompt, repeatable.

**"I want a specialist that accumulates knowledge over time, or I want to run work in parallel without bloating my main context."**
→ **Subagent.** Possibly with `memory: project`.

**"I want X to happen automatically AND be context-aware."**
→ **Hook that invokes a skill.** Hook triggers, skill runs with LLM reasoning.

**"I want to enforce a rule deterministically."**
→ **Hook.** E.g., a `PostToolUse` hook that checks edit output.

**"I want to codify a workflow."**
→ **Skill.** A workflow is a procedure; a skill is the right shape.

**"I want a reviewer to check my work before I deliver."**
→ **Subagent.** Specifically, one with read-only tools.

---

## When to adopt each

- **Hooks — at L5.** Before L4, your protocols aren't stable enough to automate yet. Premature hooks calcify bad patterns.
- **Skills — at L3–L4.** As soon as you notice yourself repeating the same prompt, turn it into a skill.
- **Subagents — at L4+.** Mainly useful when your workflows are parallelizable or you need scoped memory.

**Don't adopt all three at once.** Start with one skill for your most-repeated workflow. Build the habit of using it. Add more later.

---

*Canonical references live in `LINKS.md`. Read those before building anything complex.*
