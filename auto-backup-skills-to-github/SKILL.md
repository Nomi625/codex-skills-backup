---
name: auto-backup-skills-to-github
description: Use when a Codex skill has just been created, edited, installed, or renamed and the user wants personal skills saved, backed up, synced, committed, pushed, or preserved in their GitHub skills repository.
---

# Auto Backup Skills to GitHub

## Overview

After creating or changing a personal skill, mirror it into the user's GitHub backup repository and push a commit. The default backup repo is:

```text
C:\Users\Administrator\Documents\codex-skills-backup
https://github.com/Nomi625/codex-skills-backup.git
```

## Trigger Rule

When this skill is active and a skill is created or updated, do not stop after writing `~\.codex\skills\<skill-name>`. Back it up to GitHub in the same turn unless the user explicitly says not to push.

## Workflow

1. Identify the source skill directory, usually:

   ```text
   C:\Users\Administrator\.codex\skills\<skill-name>
   ```

2. Confirm the backup repo is clean enough to modify:

   ```powershell
   git -C 'C:\Users\Administrator\Documents\codex-skills-backup' status --short --branch
   git -C 'C:\Users\Administrator\Documents\codex-skills-backup' remote -v
   ```

3. Copy the skill folder into the repo as a top-level directory named `<skill-name>`. Do not place independent skills inside another skill's `static/`, `references/`, or `scripts/` directory.

4. Add the skill name to `README.md` if the contents list does not already mention it.

5. Review the diff. Only commit the copied skill and intentional README changes.

6. Commit and push:

   ```powershell
   git add README.md <skill-name>
   git commit -m "Add <skill-name> skill"
   git push origin master
   ```

7. Report the commit hash and GitHub URL:

   ```text
   https://github.com/Nomi625/codex-skills-backup/tree/master/<skill-name>
   ```

## Script

Use `scripts/backup_skill_to_github.py` for the standard case:

```powershell
python scripts\backup_skill_to_github.py --skill-name zotero-paper-import --commit-message "Add Zotero paper import skill"
```

The script copies from `C:\Users\Administrator\.codex\skills`, updates the backup repo, and prints the git commands to run. Inspect `git diff` before committing when the repo already has unrelated changes.

## Safety Rules

- Never run `git reset --hard` or discard unrelated changes.
- If the backup repo has unrelated modifications, preserve them and commit only the target skill files.
- Do not back up `.codex\skills\.system`; system skills are intentionally excluded from this repository.
- Do not store secrets, API keys, cookies, Zotero databases, downloaded PDFs, or large generated files unless the user explicitly asks and the repo is intended for them.
- If `git push` fails for credentials or network, leave the local commit in place and tell the user the exact command to retry.
