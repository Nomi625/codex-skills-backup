---
name: amesim-bridge
description: Use when the user wants Codex to run, validate, automate, smoke-test, or batch-drive a local Simcenter AMESim/Amesim model, especially with .ame files, QuarterCar smoke tests, STDSIMManager errors, or the C:\Users\Administrator\Documents\codex+amesim bridge.
---

# AMESim Bridge

## Overview

Use the local bridge at `C:\Users\Administrator\Documents\codex+amesim` to run AMESim models from Codex. Real AMESim simulation must run outside the default sandbox because `STDSIMManager` needs unrestricted process/IPC behavior.

## Standard Workflow

1. Work from `C:\Users\Administrator\Documents\codex+amesim`.
2. Set `PYTHONPATH=src`.
3. Run `discover` to confirm AMESim installations.
4. Create or update a JSON config for the target `.ame` model.
5. Run `validate`.
6. Run `run` with escalation/sandbox bypass for real simulation.
7. Read `run_summary.json` and result artifacts before claiming success.

## Commands

Development shell:

```powershell
cd C:\Users\Administrator\Documents\codex+amesim
$env:PYTHONPATH='src'
py -3.11 -m amesim_bridge.cli discover
```

Known working smoke test:

```powershell
$env:PYTHONPATH='src'
$env:AME='D:\Program Files\Simcenter\2021.1\Amesim'
$env:AME_STDSIM_WAIT_FOR_DAEMON='120'
py -3.11 -m amesim_bridge.cli run examples/quartercar_smoke_config.json
```

Run real AMESim simulations with `sandbox_permissions=require_escalated`. If run inside the sandbox, AMESim may fail with:

```text
Could not start local daemon manager: localhost.
No resource to perform the job.
```

## Using A User Model

When the user provides a `.ame` path:

1. Inspect whether the file exists.
2. Copy `examples/quartercar_smoke_config.json` to a new config such as `examples/user_model_config.json`.
3. Replace `model` with the user's `.ame` path.
4. Use a dedicated `work_dir`, usually under `examples/runs/<model-name>`.
5. Keep `runner_executable` as `D:/Program Files/Simcenter/2021.1/Amesim/python.bat` unless discovery shows a better runner.
6. If no model-specific script exists, adapt `scripts/amesim_quartercar_smoke.py` or create a minimal script that opens the model, runs `AMERunSimulation()`, writes a CSV status artifact, and closes AMESim.

See `references/model-config.md` for the config shape.

## Verification

Before telling the user it worked, verify all of:

- Bridge command exits `0`.
- `run_summary.json` has `"status": "success"` and `"returncode": 0`.
- Expected artifacts exist.
- No lingering `STDSIMManager`, `AMERun`, `AMESim`, or AMESim Python process remains.
- `py -3.11 -m pytest -v` still passes after code changes.

## Known Local Installations

- Batch/API target: `D:\Program Files\Simcenter\2021.1\Amesim`
- GUI target: `C:\Program Files\Simcenter\2404\Amesim\win64\AMESim.exe`
