#!/usr/bin/env python3
"""
SessionStart hook — injects current date + last git commit into Claude's context.

Wire it up in ~/.claude/settings.json:

  {
    "hooks": {
      "SessionStart": [{
        "hooks": [{
          "type": "command",
          "command": "python3 ~/.claude/hooks/session-start.py"
        }]
      }]
    }
  }

Windows: replace "python3 ~/.claude/hooks/session-start.py" with
"python %USERPROFILE%\\.claude\\hooks\\session-start.py" (or use `py -3`).

Why this matters:
- Claude's system date can be stale (especially in long-lived shells)
- You don't want to re-explain "we're at commit X, branch Y" every session
- Hooks are deterministic — the harness runs them, not Claude

Output shape per Claude Code docs:
  {"hookSpecificOutput": {"hookEventName": "SessionStart",
                          "additionalContext": "<text>"}}
"""

import json
import subprocess
from datetime import date


def get_git_state() -> dict:
    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
        last_commit = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%h %s"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
        return {"branch": branch, "last_commit": last_commit}
    except Exception:
        # Not a git repo or git not available — fine, skip git info
        return {}


def main():
    today = date.today().isoformat()
    git = get_git_state()

    context_lines = [f"Today's date is {today}."]
    if git.get("branch"):
        context_lines.append(f"Current branch: {git['branch']}")
    if git.get("last_commit"):
        context_lines.append(f"Last commit: {git['last_commit']}")

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(context_lines),
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
