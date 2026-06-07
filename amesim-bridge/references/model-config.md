# AMESim Bridge Config Reference

Minimal config:

```json
{
  "amesim_root": "D:/Program Files/Simcenter/2021.1/Amesim",
  "model": "D:/path/to/model.ame",
  "work_dir": "runs/my-model",
  "parameters": {},
  "allowed_parameters": [],
  "outputs": ["smoke_status.csv", "*.log", "*.txt"],
  "timeout_seconds": 180,
  "runner_executable": "D:/Program Files/Simcenter/2021.1/Amesim/python.bat",
  "runner_args": [
    "C:/Users/Administrator/Documents/codex+amesim/scripts/amesim_quartercar_smoke.py",
    "D:/path/to/model.ame",
    "smoke_status.csv"
  ]
}
```

Notes:

- `work_dir` is resolved relative to the config file location by the current bridge.
- Real AMESim simulation should be run with escalation/sandbox bypass.
- For production model-specific work, create a model-specific runner script instead of mutating arbitrary `.ame` internals.
