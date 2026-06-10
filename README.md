# Codex Skills Backup

This repository stores user-installed Codex skills for reuse across machines.

## Contents

- `find-skills`
- `gstack`
- `superpowers` skills from `obra/superpowers`
- Nature workflow skills
- `zotero-paper-import`
- `auto-backup-skills-to-github`
- `interactive-learning`
- `ansys-fluent-driver`
- `fluent-thermal-management`
- Shared reference files in `_shared`

System skills from `.codex/skills/.system` are intentionally excluded because Codex provides them.

## Restore On Windows

From this repository root:

```powershell
.\install.ps1
```

This copies every skill folder in this repository into:

```text
$HOME\.codex\skills
```

Restart Codex after installing or updating skills.

## Restore Manually

Copy all folders except `.git` and files such as `README.md` / `install.ps1` into:

```text
~/.codex/skills
```

On Windows that is usually:

```text
C:\Users\<username>\.codex\skills
```

