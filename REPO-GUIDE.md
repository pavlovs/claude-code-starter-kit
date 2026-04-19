# REPO-GUIDE — infrastructure best practices

How to structure files so Claude finds the right context at the right time without being told. The goal: *every piece of information lives in exactly one place, and the right session loads the right places automatically.*

---

## The seven file types

| File | Purpose | Adopt at | Lifespan | Who writes it |
|---|---|---|---|---|
| `CLAUDE.md` | Identity, hard constraints, session protocols | L1 | Changes ~monthly | You |
| `TASKS.md` | Active tasks with ownership tags | L2 | Changes daily | You + Claude |
| `feedback.md` | Intake log for corrections → rules | L3 | Grows continuously | Claude (triggered by your corrections) |
| `anti-patterns.md` | Named failure patterns with detection + fix | L3 | Grows slowly | Claude (promoted from feedback.md) |
| `learnings.md` | Meta-knowledge about Claude Code *as a tool* | L3 | Grows slowly | You + Claude |
| `.claude/rules/*.md` | Modular rule sets (when CLAUDE.md grows past ~150 lines) | L4 | Changes ~monthly | You |
| `Claude_Context/*.md` (or similar) | Role/domain context loaded on demand | L4 | Changes when domain changes | You |

Each has exactly one job. Don't mix.

---

## CLAUDE.md — what belongs

- **Identity.** Who you are, what you work on, how you think. 3–5 lines.
- **Working style.** Tone, verbosity, sycophancy tolerance, model defaults. 5–10 lines.
- **Hard constraints.** The ~10 rules that apply to every session. "Never hallucinate", "Surface contradictions", "Verify before claiming done".
- **Session protocols.** Tags like `[MORNING]` or `[REVIEW]` that trigger specific behavior.
- **Task classification.** `[ME]`/`[AGENT]`/`[TOGETHER]`/`[WIP]` definitions.
- **Connected tools.** MCP servers, API credentials, external services.

**Sizing rule:** Target ~150 lines. Hard ceiling ~250 lines. Beyond that, split into `.claude/rules/*.md`.

**Attention curve:** Items at the top and bottom of CLAUDE.md get the most attention. Middle items compete with everything else. Put the Critical N (your highest-leverage rules) at the top.

---

## CLAUDE.md — what does NOT belong

| Anti-pattern | Why it's wrong | Where it belongs |
|---|---|---|
| Task lists | Tasks are stateful and change daily — stale content poisons context | `TASKS.md` |
| Dated notes ("On 2026-04-12, I decided...") | One-off — burns tokens every session forever | `feedback.md` or git commit msgs |
| Deep role context ("For all M&A work, remember that...") | Not every session is M&A — load on demand | `Claude_Context/context-deals.md` |
| Full anti-pattern descriptions | Long-form explanations belong separate | `anti-patterns.md` |
| Project-specific setup for 5+ projects | Each project has its own CLAUDE.md | `<project>/CLAUDE.md` |
| A list of everything Claude has ever done | History belongs in git, not context | git log |
| Your resume | Yes, people do this. Don't. | About-me section (5 lines max) |

**The test:** Does every session I ever start need this info? If no, it doesn't belong in CLAUDE.md.

---

## Global vs. project split *(adopt at L4, optional)*

**When to adopt:** you work across 3+ projects and keep copy-pasting the same identity / working-style / hard constraints into each CLAUDE.md. Skip this entire section if you're in a single project — it adds complexity without payoff.

**The move:**
- Identity / working-style / hard constraints that are *true everywhere* → `~/.claude/rules/*.md`
- Project-specific stuff (TASKS, feedback, anti-patterns, role context) → stays in the project
- Cross-project skills you invoke weekly → `~/.claude/commands/*.md`
- Per-project skills → `<project>/.claude/commands/*.md`

After the move, each project's `CLAUDE.md` becomes ~30–50 lines: project identity + "hard constraints specific to this project" + a pointer to where global rules live. Claude Code loads both automatically.

**Decision test:** if the same rule is pasted into 3+ projects unchanged, it's global. If it changes per project, it's local.

**Trap:** moving everything global too early. Before you've run 3 projects with local CLAUDE.md, you don't know which rules actually generalize. You'll over-promote, then have to demote. Keep it local until the copy-paste pain is real.

---

## Directory layout reference

```
~/.claude/                     ← applies to ALL projects
├── CLAUDE.md                  ← or rules/ directory
├── rules/
│   ├── about-me.md            ← who you are (same everywhere)
│   ├── working-style.md       ← tone/style (same everywhere)
│   └── autonomy-rules.md      ← hard constraints (same everywhere)
├── commands/                  ← global skills
├── agents/                    ← global subagents
└── settings.json              ← global hooks

<project>/
├── CLAUDE.md                  ← project-specific identity + constraints
├── TASKS.md                   ← this project's active work
├── feedback.md                ← this project's correction log
├── anti-patterns.md           ← this project's failure patterns
├── .claude/
│   ├── rules/                 ← project-specific rules (modular)
│   ├── commands/              ← project-specific skills
│   ├── agents/                ← project-specific subagents
│   ├── hooks/                 ← project-specific hook scripts
│   └── settings.local.json    ← project-specific hooks + permissions
└── Claude_Context/            ← role/domain context loaded by session tags
    ├── context-dev.md
    ├── anti-patterns-dev.md
    └── ...
```

**Global** = stays the same across all your work. Identity, working style, hard constraints.
**Project** = specific to this codebase / workspace. Tasks, feedback, domain context, commit conventions.

If something applies to 80%+ of your projects, it's global. If it's specific to one, it's project.

---

## When to split CLAUDE.md into `.claude/rules/*.md`

**Trigger:** CLAUDE.md crosses ~150 lines.
**Goal:** each rules file focuses on one topic and stays under ~60 lines.

Typical split:
- `rules/about-me.md` — identity, role, context
- `rules/working-style.md` — response style, tone, model selection
- `rules/session-protocols.md` — session tags, task classification
- `rules/autonomy-rules.md` — execution behavior, hard constraints
- `rules/self-improvement.md` — feedback loop, anti-pattern logging

CLAUDE.md then becomes a short index that references each rule file.

Claude Code loads all `.claude/rules/*.md` automatically alongside `CLAUDE.md` — you don't need to import them manually.

---

## TASKS.md structure

```markdown
## What moves the needle today
- [ ] [ME] <task>
- [ ] [AGENT] <task> | AC: <acceptance criteria>

## Prio A — this week
- [ ] [TOGETHER] <task — waiting on my input>

## Prio B
- [ ] [ME] <task>
```

Four tag types (exactly four — resist inventing more):
- `[ME]` — only I can do this
- `[AGENT]` — Claude executes autonomously
- `[TOGETHER]` — needs my input first
- `[WIP]` — actively in progress, don't touch

**Every [AGENT] task needs an `| AC:` field.** Without AC, "done" is subjective. See `WORKFLOW.md` for AC patterns.

---

## The three-tier knowledge loop *(adopt at L3)*

Three files, one job each. Don't merge them.

**1. `feedback.md` — intake.**
Fresh corrections land here as rules. Format: "Always/Never X BECAUSE Y". Entry lifespan: days to weeks. Use `/log-feedback` to capture corrections without losing them.

**2. `anti-patterns.md` — promoted patterns.**
When the same failure recurs or represents a broader category, promote from feedback.md with a name (e.g., `ZOMBIE-CONTENT`, `STALE-DOCS`). Entry lifespan: months. These are the patterns you pattern-match *against* in every session.

**3. `learnings.md` — meta-knowledge about Claude Code.**
Orthogonal to the other two. Captures how the *tool itself* behaves:
- "SessionStart hooks require `hookSpecificOutput` wrapper — not top-level `additionalContext`"
- "Skills only load from `~/.claude/commands/` or cwd's `.claude/commands/` — not parent dirs"
- "Model X drifts on prompts over 4k tokens in the middle"

Without (3), you re-discover the same tool quirks in every new project. Most users scatter this knowledge across Notion, Slack, or their memory. Having it next to the rules makes it reloadable.

**What belongs in which:**

| If the mistake is about... | File |
|---|---|
| What Claude did wrong on *your project* | `feedback.md` (raw) → `anti-patterns.md` (promoted) |
| How Claude Code *the tool* behaves | `learnings.md` |
| A bug in your own code | git commit msg, not here |

**Example entries:**

```markdown
# learnings.md

## Hooks
- `SessionStart` hook output must be wrapped: `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}`. Top-level `additionalContext` is silently ignored. (2026-04-19)

## Skills
- Skills load from exactly two paths: `~/.claude/commands/<name>.md` (global) and `<cwd>/.claude/commands/<name>.md` (project). Nothing else is searched. (2026-04-18)

## Tools
- `Read` tool can't access paths outside the session's working directory. Use `/add-dir <path>` or restart from the target dir. (2026-04-17)
```

---

## feedback.md vs. anti-patterns.md

**feedback.md = intake**. Fresh corrections land here as rules ("Always X because Y").

**anti-patterns.md = promoted patterns**. When the same failure recurs or represents a broader category, move it from feedback.md to anti-patterns.md with a named pattern (e.g., `ZOMBIE-CONTENT`, `STALE-DOCS`, `PHANTOM-TASK`).

The loop:
1. You correct Claude
2. Claude writes the rule to `feedback.md` (same session)
3. If it's a recurring pattern, you or Claude promotes it to `anti-patterns.md` with a name
4. Next session start: both files get read; Claude applies the rules silently

**The `BECAUSE` clause is mandatory.** "Never re-add deleted content" is weak. "Never re-add content that's been deleted **because** deletions are intentional editorial choices — restoring them erodes trust" is strong. The `BECAUSE` clause is what generalizes the rule to novel situations.

---

## Role-specific context: when and how

If your work spans distinct domains (e.g., coding AND writing investor memos), don't stuff both into CLAUDE.md. Instead:

1. Define session tags in CLAUDE.md: `[DEV]`, `[WRITING]`, etc.
2. Create role-specific context files: `Claude_Context/context-dev.md`, `context-writing.md`
3. In CLAUDE.md's session protocol section: `[DEV] → read context-dev.md + anti-patterns-dev.md`
4. Start each session with the relevant tag

This keeps any individual session focused. Coding sessions don't read about writing style. Writing sessions don't read about git conventions. Load only what's relevant.

---

## Common mistakes when structuring the repo

1. **One giant CLAUDE.md with everything.** Grows until it's unreadable. Split once it crosses ~150 lines.
2. **Task state inside CLAUDE.md.** "Currently working on X, next is Y" — this changes daily. Move to `TASKS.md`.
3. **feedback.md with only descriptions, no rules.** "Claude used wrong calendar ID" ≠ "Always check all 3 calendar IDs because the primary excludes imports". Only rules prevent recurrence.
4. **No role separation.** A 400-line CLAUDE.md that has sections for every domain you work in. Split into role-specific context files loaded by session tag.
5. **Templates checked in as real files.** `CLAUDE.md.example` is a template; `CLAUDE.md` is your file. Keep the `.example` suffix on unmodified templates so they never accidentally get loaded by Claude Code.

---

## Minimum viable setup (for a new user)

If you do nothing else:

1. Create `CLAUDE.md` in your project root with: identity (3 lines) + working style (5 lines) + 3 hard constraints.
2. Create `TASKS.md` with the 4-tag convention.
3. Create an empty `feedback.md` (you'll fill it as Claude makes mistakes).

That's L2. Run `/statusreport` to find out what to add next.
