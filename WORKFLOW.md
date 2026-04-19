# WORKFLOW — the loop that prevents rework

Freestyling with Claude Code produces plausible-looking output with hidden defects. The fix isn't "try harder" — it's **structure**. This doc describes the loop.

```
Brainstorm → Spec → Plan → Implement (TDD) → Review → Ship
```

Each step has an artifact. Each artifact unblocks the next step. Skipping a step causes the same categories of failure, every time.

---

## 1. Brainstorm — understand what you're actually building

**Input:** A loose idea from your head.
**Output:** A short design doc with: goal, constraints, 2–3 approach options with tradeoffs, chosen approach.
**Artifact:** `docs/specs/YYYY-MM-DD-<topic>-design.md`

**What breaks if you skip this:**
You write code that solves the wrong problem. The user asked for X, you built X-but-more-general, now they need to figure out how to use it. Brainstorming forces *one question at a time* so the real constraint surfaces — often it's not what the first message implied.

**Do:** Ask multiple-choice questions when possible (easier to answer). Propose 2–3 approaches before settling. Write the chosen design down before coding.

**Don't:** Jump to code because "it's obvious." If it's obvious, writing the 3-bullet design takes 30 seconds.

---

## 2. Spec — make it specific enough to build from

**Input:** Design doc.
**Output:** A spec with concrete requirements, API contracts, input/output formats, edge cases.
**Artifact:** The design doc expanded with **Input Data** / **Output Data** / **Acceptance Criteria** sections.

### Why input/output data matters

Most "it doesn't work" failures trace to inputs Claude *assumed* about. Writing them down forces surfacing:
- Exact shape of every input (types, units, required vs. optional)
- Exact shape of every output (including error cases)
- What happens at the boundaries: empty input, oversized input, malformed input

If you can't describe the I/O contracts in 10 lines, the spec isn't ready.

### Acceptance criteria — what "done" actually means

Every [AGENT] task needs AC. Every feature needs AC. Rule: *if you can't write a test that checks AC, the AC isn't precise enough.*

Bad AC: "Dashboard is clear and usable."
Good AC: "Dashboard shows 3 tabs (Pipeline, Deals, Contacts). Each tab loads in <2s. Legend visible on all tabs. Filter bar state persists across tab switches."

**What breaks if you skip this:**
You'll ship something, the user tries it, finds a case you didn't handle, you fix it, they find another case, repeat. AC upfront = one round of debugging, not five.

---

## 3. Plan — sequence the work

**Input:** Spec.
**Output:** Ordered list of steps, each small enough to implement + test in under ~30 minutes.
**Artifact:** `docs/specs/YYYY-MM-DD-<topic>-plan.md` with a numbered checklist.

**What breaks if you skip this:**
Mid-implementation, you realize step 4 depends on step 7 that you haven't designed. Now you're in a half-built state with no path forward. The plan makes these dependencies visible *before* the file edits start.

---

## 4. Implement — TDD where it pays

**Test-first for:** anything with a precise contract. Pure functions, data transformations, state machines, API parsers.

**Test-after (or skip tests) for:** anything highly visual or exploratory. UI styling, prototyping, one-off scripts.

**The rule:** if you'd fix a regression by running your eye over the output, tests won't help. If you'd fix it by running a function with new inputs, write the test.

**What breaks if you skip tests on contract-heavy code:**
You ship a "works for my one example" implementation. Six months later someone passes an empty array and the whole pipeline breaks. The test would have caught this on day one.

---

## 5. Review — independent second opinion

**Self-review is necessary but insufficient.** Generator and reviewer being the same model creates blind spots.

Before shipping non-trivial work:
- Ask a separate subagent (or `/codex-review` if you have GPT-5 access) to read the output
- Give it the spec + the artifact, ask it to find what's missing or broken
- If it flags something you didn't see, you had a blind spot — good.

**Rule:** If the reviewer finds nothing, either the work is genuinely tight or you gave the reviewer too little context. Feed it the spec + artifact + your own self-assessment. Ask it to challenge, not praise.

---

## 6. Ship — the commit gate

**Definition of done:**
1. Code works (you ran it)
2. Tests pass (if applicable)
3. Docs updated (plan, architecture, README reflect reality)
4. Reviewer (human or AI) has no blockers
5. You can state *how you verified* each of the above

Skip any of these and you're shipping on faith.

---

## Which step gets skipped most?

| Step | Skip rate | Cost of skipping |
|---|---|---|
| Brainstorm | High | Build the wrong thing |
| Spec (I/O + AC) | Very high | 3-5 rounds of rework |
| Plan | Medium | Get stuck mid-build |
| Review | Very high | Ship blind spots |
| Docs | Very high | Next session builds duplicate work on stale info |

Brainstorming feels slow. Spec feels pedantic. Docs feel like overhead. They all buy time later — measurably more than they cost.

---

## Minimum viable loop

For a 30-minute task, the full loop feels like overkill. Minimum viable:
1. Write 3 bullets: goal, inputs, expected output
2. Write the 1-line AC
3. Build
4. Check AC
5. Update any docs that now lie

5 minutes overhead. Saves 20 minutes of rework on average. That's the trade.
