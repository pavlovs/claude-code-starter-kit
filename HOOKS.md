# HOOKS — deterministic guardrails

> *Adopt at L5.* Before L4 your protocols aren't stable enough to automate — premature hooks calcify bad patterns. Finish the feedback loop (L3) and session protocols (L4) first.

Hooks are the only Claude Code mechanism that runs **outside** the model. The harness fires them at lifecycle events — before a tool call, after a file edit, on session start, on commit. They can't hallucinate. Use them for anything you want to be *always true*.

Five proven patterns below, each with: what it does, when it fires, why it's worth having, and when to adopt it.

---

## 1. SessionStart — inject date + git state

**Fires:** Every session start.
**Why:** Claude's internal date drifts. Branch/commit context saves 30 seconds of re-explaining each session.
**File:** `examples/hook-session-start.py` + settings snippet in the file header.

Output is injected as `additionalContext` via the documented `hookSpecificOutput` wrapper.

Extend it with:
- Last 3 commit messages (for recovering mid-work context)
- Detected session tag from prompt (regex the first 50 chars of user input)
- On-call / pager state (for engineering teams)

---

## 2. Stop — nudge to verify completeness

**Fires:** When Claude tries to end a turn.
**Why:** Claude often stops mid-task. A single re-prompt catches half-finished work without user intervention.
**File:** `examples/hook-stop-nudge.json`.

The `type: "prompt"` hook runs a nested Claude turn with a forced-reflection prompt. Its response decides whether to continue or end.

**Don't overuse this.** More than one Stop hook and you chain prompts users don't see. Start with one, tune the prompt, then decide if a second is worth it.

---

## 3. PreToolUse — block risky tool calls

**Fires:** Before any tool call.
**Why:** Deterministic veto of destructive operations. Catches `rm -rf /` before it runs.
**Shape:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 ~/.claude/hooks/block-dangerous-bash.py"
      }]
    }]
  }
}
```

Your script reads the tool input from stdin (JSON), greps for patterns like `rm -rf`, `git push --force`, `DROP TABLE`, and exits non-zero with a reason string to block. Exit 0 allows the call.

**Rule:** Don't block things the user might legitimately want. Block things that are almost never correct (force-pushing to main, dropping prod tables). Everything else → surface a warning, don't block.

---

## 4. PostToolUse — verify writes didn't introduce regressions

**Fires:** After a tool call (e.g., Write, Edit).
**Why:** Catches broken state immediately — a dead file reference, a syntax error, a missing doc update.
**Pattern:** After any `.md` write, run a link validator. After any code write, run the linter. Warn only — don't block.

Example: validate markdown links in a doc you just edited. If a link is dead, the hook prints a warning that Claude sees on its next message. Claude can then fix the reference or flag the issue.

Keep these **warn-only** unless the check is bulletproof. A noisy hook you've learned to ignore is worse than no hook.

---

## 5. PreCommit (user-side git hook, not Claude) — documentation gate

**Fires:** On `git commit`.
**Why:** "Docs before done" is Critical-10 rule #4. A pre-commit hook enforces it mechanically.

Pattern: if `.md` files are staged, require a `Doc-verified: true` trailer in the commit message. Block otherwise. Forces a conscious verification step: "Did I check that my doc changes actually reflect the code I'm committing?"

This lives outside Claude Code (it's a standard git hook in `.git/hooks/pre-commit` or via a framework like `pre-commit`), but it's how you enforce the one rule Claude's self-check can't reliably hit.

---

## What NOT to put in a hook

- **Anything that needs judgment.** Hooks are deterministic. If "should I block this?" is ambiguous, it's not a hook — it's a subagent review.
- **Anything that talks to the user.** Hooks run silently. For user interaction, use a skill.
- **Anything slow.** Hooks block the tool call. Keep under 500ms. If a check is slow, move it to CI.
- **Secrets lookup via network.** Hooks run on every tool call. Don't hit a remote service each time.

---

## Debugging hooks

- Hook not firing? Check `claude --debug` output. Matcher syntax is strict.
- Hook firing but nothing happens? Print to stderr (you'll see it in debug output) or write to a log file; stdout is consumed by the harness.
- Testing: invoke your script directly with a canned JSON input on stdin. Match the shape from `claude --debug`.

---

## When to adopt each

- **L2 → L3**: SessionStart (injects date/git — low effort, immediate value)
- **L3 → L4**: Stop nudge (catches half-finished work)
- **L4**: PreToolUse guards for dangerous Bash commands
- **L5**: PostToolUse doc/link validators + pre-commit doc gate

Don't adopt all five at once. Each hook you add is a new place something can go wrong — and Claude's behavior is hard to debug when a hook is misbehaving silently. Add one, run for a week, then consider the next.
