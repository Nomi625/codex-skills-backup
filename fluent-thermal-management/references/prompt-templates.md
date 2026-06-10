# Prompt Templates

## Solver-Only Thermal Case

```text
Use fluent-thermal-management and ansys-fluent-driver to run a real Ansys Fluent 2026 thermal simulation.

Start with smoke test and license verification. Use sandbox escalation for Fluent launch.

Input mesh:
<path to .msh or .msh.h5>

Objective:
<thermal design goal, e.g. evaluate max temperature and pressure drop>

Physics:
- Energy equation: on
- Materials: <solid/fluid properties>
- Heat source: <W, W/m3, or W/m2 with total power>
- Flow: <velocity/mass flow/pressure/fan curve>
- Turbulence/laminar assumption: <...>
- Radiation/contact resistance: <included or neglected>

Acceptance criteria:
- residual targets: <...>
- max temperature monitor stable
- heat balance within <...>
- pressure drop stable if fluid is present

Outputs:
- case/data files
- monitor CSVs
- contour images from Fluent data
- Markdown report with evidence checklist

Rules:
- Do not fabricate Fluent results.
- If Fluent does not run, stop and report the exact failure.
- Distinguish real Fluent outputs from generated visualization.
```

## Design Comparison

```text
Use fluent-thermal-management to compare these thermal design variants:
<variant list>

Keep heat load, materials, ambient, mesh criteria, solver settings, and convergence criteria identical unless the variant explicitly changes them.

Report a table with:
- Tmax
- average target temperature
- Delta T
- pressure drop
- thermal resistance
- heat balance error
- notes on mesh quality and convergence

Choose the best design only after verifying all runs used comparable assumptions.
```

## Transient Heat-Up / PCM

```text
Use fluent-thermal-management for a transient heat-up simulation.

Define:
- initial temperature
- heat input over time
- time step and total simulated time
- PCM properties or temperature-dependent Cp/k if relevant
- melt fraction output if PCM is modeled

Report:
- Tmax(t)
- average temperature(t)
- stored heat / heat balance
- melt fraction(t), if applicable
- snapshots at meaningful times
```
