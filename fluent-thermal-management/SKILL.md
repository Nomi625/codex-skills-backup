---
name: fluent-thermal-management
description: "Use when Codex needs to plan, run, automate, or report Ansys Fluent simulations for thermal management and thermal design: electronics cooling, battery packs, PCM, heat sinks, forced/natural convection, liquid cooling, CHT, transient heat-up, thermal resistance, pressure drop, fan/pump operating points, or design comparison."
---

# Fluent Thermal Management

## Overview

Use Ansys Fluent as a verifiable heat-transfer solver for thermal design. This skill defines the engineering workflow; use `ansys-fluent-driver` for local Fluent 2026 launch, PyFluent, license, and sandbox details.

## Required Sub-Skill

Use `ansys-fluent-driver` before any real run:

```text
check paths -> check license -> PyFluent smoke test -> run thermal case
```

Do not claim a thermal result until Fluent actually ran and exported evidence.

## Workflow

1. Classify the case:
   - solid conduction only;
   - fluid convection only;
   - conjugate heat transfer (solid + fluid);
   - transient heat-up/cool-down;
   - PCM/phase change;
   - liquid cooling/cold plate;
   - fan/pump/pressure-drop design.
2. Confirm inputs: CAD/mesh/case path, units, materials, heat sources, boundary conditions, operating environment, and target metrics.
3. Prefer solver-only first if a mesh exists. Add Fluent Meshing only after the solver workflow is reliable.
4. Build the Fluent setup around energy conservation:
   - enable Energy equation;
   - use correct solid/fluid materials and thermal contact assumptions;
   - define heat generation as W, W/m3, heat flux, or source term with units explicit;
   - set convection inlet/outlet/wall/radiation conditions consistently.
5. Monitor engineering quantities, not only residuals: max temperature, average temperature, heat balance, pressure drop, mass flow, thermal resistance, and key surface heat fluxes.
6. Export reproducible artifacts: script/journal, case/data, monitor CSV, images from Fluent data, and Markdown report.

## Thermal Evidence Checklist

Every final answer must include:

- Fluent version, launch mode, and script/journal path.
- Input files and unit checks.
- Material properties used: density, Cp, k, viscosity where relevant.
- Heat source definition and total heat balance.
- Boundary conditions and reference ambient temperature.
- Mesh quality and boundary-layer/near-wall assumptions if convection is present.
- Residual history plus thermal metrics history.
- Maximum temperature location/value, pressure drop if fluid is present, and thermal resistance when meaningful.
- Exported result paths.
- Clear statement of what is real Fluent output versus generated visualization.

## Common Thermal Mistakes

- Forgetting Energy equation.
- Mixing W, W/m3, and W/m2 without checking total heat.
- Treating script-defined heat power as proof; verify integrated heat source in results.
- Ignoring contact resistance or assuming perfect bonding without saying so.
- Reporting residual convergence while max temperature or pressure drop is still drifting.
- Using arbitrary outlet/backflow temperatures that contaminate the solution.
- Comparing designs without identical mesh, BCs, materials, and convergence criteria.

## References

- Read `references/thermal-playbook.md` before a real simulation or design comparison.
- Read `references/prompt-templates.md` when drafting a user-facing prompt for Codex to run Fluent.
