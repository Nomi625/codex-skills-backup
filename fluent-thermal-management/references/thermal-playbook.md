# Thermal Management Fluent Playbook

## Case Types

| Case | Fluent setup focus | Key outputs |
|---|---|---|
| Electronics heat sink | CHT, forced convection, turbulence, contact assumptions | Tmax, thermal resistance, pressure drop |
| Battery pack | volumetric heat, anisotropic/conductive paths, cooling channels | cell Tmax, Delta T, coolant pressure drop |
| PCM thermal buffer | transient, phase change material properties, latent heat | melt fraction, temperature delay, heat storage |
| Cold plate/liquid cooling | liquid material, channel pressure drop, wall heat transfer | thermal resistance, pump power, flow uniformity |
| Natural convection | gravity, buoyancy model, large domain | plume, Tmax, heat balance |
| Fan-cooled enclosure | fan curve or mass-flow inlet, vents, porous zones | component Tmax, airflow distribution |

## Minimum Input Contract

Ask for or infer:

- geometry/mesh/case path;
- length units and coordinate orientation;
- heat source type and total power;
- materials and temperature-dependent properties if needed;
- ambient/inlet temperature;
- flow rate, velocity, pressure, or fan/pump curve;
- wall assumptions: adiabatic, convection, radiation, symmetry, contact;
- steady or transient target;
- acceptance criteria: Tmax, Delta T, pressure drop, thermal resistance, warm-up time.

If these are missing, state assumptions explicitly and mark the result as preliminary.

## Setup Guidance

1. Enable Energy for any thermal result.
2. Use solid zones for conduction and fluid zones for convection. Check zone types after mesh import.
3. For CHT, verify wall/interface pairing and contact assumptions.
4. For electronics/batteries, prefer volumetric heat generation when heat is distributed through a solid volume.
5. For surface heaters, check that area-integrated heat flux equals intended power.
6. For transient thermal cases, define time step from thermal time scale and expected flow residence time; do not use arbitrary time steps without justification.
7. For radiation, specify emissivity and ambient/radiation temperature; otherwise state radiation is neglected.

## Convergence and Sanity Checks

- Residuals are necessary but insufficient.
- Track total heat input and heat leaving outlets/walls.
- Track max and average temperatures over iterations/time.
- Track pressure drop and mass imbalance for fluid cases.
- Compare expected order of magnitude using:
  - thermal resistance: `Rth = (Tmax - Tambient) / Q`;
  - heat balance: `Qin ~ Qout + dE/dt`;
  - pressure drop sign and magnitude.

## Design Comparison Rules

When comparing heat sink fins, PCM thickness, flow rates, coolant types, or geometry variants:

- keep material data, heat load, ambient, and convergence criteria identical;
- record mesh cell count and quality for each design;
- use the same monitor definitions;
- compare at the same physical time for transient runs;
- report tradeoffs: Tmax, Delta T, pressure drop, mass/volume, and required pumping/fan power.

## Reporting Structure

Use this structure:

1. Objective and model scope.
2. Inputs and assumptions.
3. Fluent execution evidence.
4. Mesh and physics setup.
5. Convergence and heat-balance evidence.
6. Results table.
7. Engineering interpretation.
8. Limitations and next simulation.
