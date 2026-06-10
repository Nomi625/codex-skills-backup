---
name: ansys-fluent-driver
description: Use when Codex needs to check, launch, automate, or troubleshoot local Ansys Fluent 2026 through PyFluent, especially for Fluent solver smoke tests, licensing errors, journal/API execution, CFD automation, or Codex driving Fluent from Windows.
---

# Ansys Fluent Driver

## Overview

Drive the local Ansys Fluent 2026 R1 installation through PyFluent, with explicit license and sandbox checks before claiming Fluent is usable.

## Local Defaults

Use these verified paths unless the user gives newer ones:

| Item | Path/value |
|---|---|
| Fluent 2026 | `D:\ANSYS2026\ANSYS Inc\v261\fluent\ntbin\win64\fluent.exe` |
| Workbench 2026 | `D:\ANSYS2026\ANSYS Inc\v261\Framework\bin\Win64\RunWB2.exe` |
| Ansys root | `D:\ANSYS2026\ANSYS Inc\v261` |
| License server | `1055@localhost` |
| PyFluent venv | `C:\Users\Administrator\Documents\codex+obsidian\.venv-pyfluent` |
| PyFluent package | `ansys-fluent-core` |

The working validated command must run outside the Codex sandbox because Ansys licensing writes port files under `C:\Users\Administrator\AppData\Roaming\Ansys`.

## Workflow

1. Check paths and package import first:
   ```powershell
   python C:\Users\Administrator\.codex\skills\ansys-fluent-driver\scripts\check_fluent.py
   ```
2. Check license visibility:
   ```powershell
   & 'D:\ANSYS2026\ANSYS Inc\v261\licensingclient\winx64\lmutil.exe' lmstat -a -c 1055@localhost
   ```
   Fluent-capable features include `cfd_base`, `cfd_solve_level1`, `cfd_solve_level2`, `acfd_fluent`, and `acfd_fluent_solver`.
3. Launch a PyFluent smoke test only with sandbox escalation:
   ```powershell
   python C:\Users\Administrator\.codex\skills\ansys-fluent-driver\scripts\check_fluent.py --launch
   ```
4. Report evidence, not assumptions: version printed, launch result, transcript errors, and whether Fluent exited cleanly.

## Sandbox Rule

If PyFluent fails in sandbox with:

```text
Cannot initialize ANSYS Licensing context
Unexpected license problem; exiting.
Unable to write port to C:\Users\Administrator\AppData\Roaming\Ansys\ansyscl...
```

rerun the same PyFluent launch with `sandbox_permissions="require_escalated"`. This is not a license entitlement failure if `lmstat` shows 2026 Fluent features and a non-sandbox run succeeds.

## Known Good Smoke Test

The validated result is:

```text
FLUENT_STARTED
Ansys Fluent 2026 R1
FLUENT_EXITED
```

Do not claim Codex can drive Fluent until this smoke test has passed in the current session or the user explicitly accepts prior evidence.

## Common Mistakes

- Treating a visible Fluent window as success. The Console may still show `Cannot initialize ANSYS Licensing context`.
- Running PyFluent only inside the sandbox. Licensing initialization can fail even when the license server is healthy.
- Letting user-level `ANSYS_ROOT` or `ANSYS_WB_EXE` point to Ansys 2022. Use explicit 2026 paths for automation.
- Depending on Chinese or English GUI labels. Prefer PyFluent, TUI, journal files, and logs; UI language should not matter.

## References

- Read `references/local-config.md` for current machine-specific facts and diagnostic commands.
