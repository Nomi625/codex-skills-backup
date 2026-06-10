# Fluent Simulation Playbook

Use this when the user wants Codex to run, plan, or report a real Fluent simulation rather than only check connectivity.

## Core Rule

Treat Codex as a CAE automation engineer, not a GUI clicker. Prefer:

```text
Codex -> PyFluent / journal / TUI -> Fluent -> exported files -> report
```

Do not rely on Chinese or English menu labels. UI language should not matter.

## Recommended Task Progression

1. **Connectivity smoke test**
   - Run `check_fluent.py`.
   - Run `check_fluent.py --launch` with sandbox escalation.
   - Continue only after `FLUENT_STARTED`, `Ansys Fluent 2026 R1`, `FLUENT_EXITED`.

2. **Solver-only case**
   - Start from an existing `.msh` or `.msh.h5`.
   - Import mesh, set materials/BCs/models, initialize, iterate, export case/data and monitors.

3. **Geometry + meshing case**
   - Use this only after solver-only workflow is reliable.
   - Audit geometry units, coordinate axes, enclosure, named boundaries, and mesh quality.

4. **Reusable automation**
   - Save scripts, input files, output files, and a Markdown report in a case folder.
   - Make every result reproducible from the saved script or journal.

## Prompt Template

```text
Use ansys-fluent-driver to drive Ansys Fluent 2026 for a real simulation.

First:
1. Run PyFluent/Fluent/license smoke test.
2. Confirm all input paths exist.
3. Decide whether this is solver-only, meshing+solver, or post-processing only.

Goal:
<engineering objective>

Inputs:
<mesh/geometry paths, units, case/data if any>

Physics:
<material, flow/thermal conditions, model, turbulence, compressibility, gravity if needed>

Boundary conditions:
<inlet, outlet, walls, symmetry, reference values>

Convergence:
<residual targets and engineering monitors such as pressure drop, temperature, Cl/Cd>

Outputs:
<case/data, CSV monitors, images, report, result directory>

Rules:
- Do not fabricate Fluent results.
- If Fluent does not really start, stop and report the failure.
- Record the exact script/journal and Fluent version.
- Distinguish real Fluent outputs from generated visualizations.
```

## Evidence Checklist

Every final report must include:

- Fluent version and launch method.
- Input file paths and existence checks.
- Actual PyFluent script or journal path.
- Mesh import status and mesh quality summary.
- Boundary conditions and solver model used.
- Iteration count and residual history.
- Engineering monitor history, not only residuals.
- Exported result file paths.
- Clear statement of what is real Fluent output.
- Failure point if the run did not complete.

## Aircraft / External Flow

Before meshing or solving, audit:

- geometry units and scale;
- nose/long-axis direction;
- freestream direction;
- lift and drag directions;
- reference area and reference length;
- named boundaries;
- enclosure size;
- AoA force vectors.

For AoA in the X-Z plane, use corrected force vectors consistently:

```text
drag direction = [cos(AoA), 0, sin(AoA)]
lift direction = [-sin(AoA), 0, cos(AoA)]
```

Do not stop when residuals hit the target if Cl/Cd are still drifting. Treat that as not converged.

## Post-Processing

Export machine-readable results, not only screenshots:

- `.cas.h5` / `.dat.h5` or legacy case/data when required;
- residual and monitor CSV files;
- force/pressure/temperature reports;
- contour/streamline images generated from Fluent data;
- optional JSON summary for browser viewers.

If a browser viewer is used, verify that its data was exported from the real Fluent run.
