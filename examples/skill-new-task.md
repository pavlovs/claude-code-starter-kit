---
name: new-task
description: Create a new structured task in TASKS.md with proper ownership tag and acceptance criteria. Use when adding a non-trivial task to the backlog.
---

# /new-task

You are helping the user add a new task to `TASKS.md` with proper structure — ownership tag and acceptance criteria where applicable.

## Steps

1. **Read the current `TASKS.md`** (at the project root) to understand existing structure.

2. **Ask the user** via `AskUserQuestion`:
   - "What's the task?" (free-text, use "Other")
   - "Who owns execution?" — options: `[ME]` / `[AGENT]` / `[TOGETHER]` / `[WIP]`
   - "Priority?" — options: `Prio A today` / `Prio A this week` / `Prio B`

3. **If the task is `[AGENT]`**: ask one more question:
   - "What's the acceptance criteria? (1–2 lines defining what 'done' looks like)" (free-text)

4. **Append** the new task to `TASKS.md` under the correct priority section:
   ```
   - [ ] [TAG] <task description> | AC: <acceptance criteria if AGENT>
   ```

5. **Confirm** by showing the user the new line + the section it was added to.

## Rules

- Don't overwrite existing tasks
- Don't re-order existing tasks
- Preserve all existing formatting in `TASKS.md`
- If the priority section doesn't exist yet, create it in the right place
- Never add a task without an ownership tag — always ask

## Example output

```
Added to "Prio A — today":
- [ ] [AGENT] Draft competitor comparison table | AC: 5 competitors, 4 axes, 1-paragraph summary
```
