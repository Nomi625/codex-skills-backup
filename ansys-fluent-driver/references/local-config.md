# Local Ansys Fluent 2026 Configuration

## Verified on 2026-06-10

- Workbench shortcut target: `D:\ANSYS2026\ANSYS Inc\v261\Framework\bin\Win64\RunWB2.exe`
- Fluent executable: `D:\ANSYS2026\ANSYS Inc\v261\fluent\ntbin\win64\fluent.exe`
- Fluent product version: `26.1.0`
- PyFluent venv: `C:\Users\Administrator\Documents\codex+obsidian\.venv-pyfluent`
- PyFluent version installed during setup: `0.39.0`
- License service: `Ansys PLE Licensing 2026 R1`
- License path: `1055@localhost`

## Important Finding

The license server can issue Fluent 2026 features. A manual launch checked out `cfd_base`, `cfd_solve_level1`, and `cfd_solve_level2`.

Sandboxed Codex launches can fail because Ansys Desktop Licensing cannot write:

`C:\Users\Administrator\AppData\Roaming\Ansys\ansyscl.<host>.<pid>.<port>`

Use escalated sandbox permissions for PyFluent launches.

## Useful Commands

```powershell
& 'D:\ANSYS2026\ANSYS Inc\v261\licensingclient\winx64\lmutil.exe' lmstat -a -c 1055@localhost
```

```powershell
Get-ChildItem 'C:\Users\Administrator\AppData\Local\Temp\.ansys' -Filter 'ansyscl*.log' |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 3
```

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'cx2610|fluent|mpiexec|ansyslmd|lmgrd' }
```
