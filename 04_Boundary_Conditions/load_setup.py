from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "04_Boundary_Conditions"
REPORT_FILE = OUTPUT_DIR / "boundary_conditions_report.txt"


# =========================================================
# LOAD INPUT
# =========================================================
# This is a DEMONSTRATION / ASSUMED LOAD.
# Replace it with the actual design load before treating
# the FEA model as an engineering result.
# =========================================================

APPLIED_LOAD_N = 5000.0

# Global coordinate direction
LOAD_DIRECTION = (0.0, 0.0, -1.0)


def calculate_load_components(magnitude, direction):
    """Calculate Cartesian load components."""

    magnitude_of_direction = (
        direction[0] ** 2
        + direction[1] ** 2
        + direction[2] ** 2
    ) ** 0.5

    if magnitude_of_direction == 0:
        raise ValueError("Load direction cannot be zero.")

    unit_direction = tuple(
        component / magnitude_of_direction
        for component in direction
    )

    components = tuple(
        magnitude * component
        for component in unit_direction
    )

    return unit_direction, components


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("AUTOMOTIVE ENGINE MOUNT - BOUNDARY CONDITIONS")
    print("=" * 65)

    unit_direction, components = calculate_load_components(
        APPLIED_LOAD_N,
        LOAD_DIRECTION
    )

    fx, fy, fz = components

    print("\nBoundary-condition definition:")
    print("  Fixed support : Base mounting-hole regions")
    print("  Applied load  : Upper engine-mount region")
    print(f"  Load magnitude: {APPLIED_LOAD_N:.1f} N")

    print("\nGlobal load direction:")
    print(f"  X = {LOAD_DIRECTION[0]}")
    print(f"  Y = {LOAD_DIRECTION[1]}")
    print(f"  Z = {LOAD_DIRECTION[2]}")

    print("\nCalculated force components:")
    print(f"  Fx = {fx:.2f} N")
    print(f"  Fy = {fy:.2f} N")
    print(f"  Fz = {fz:.2f} N")

    timestamp = datetime.now(timezone.utc).isoformat()

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
BOUNDARY CONDITIONS REPORT
==================================================

Generated UTC:
{timestamp}

1. FIXED SUPPORT
--------------------------------------------------
Location:
Base mounting-hole regions

Description:
The base mounting regions are considered fixed in
the structural model to represent attachment of the
mount to the supporting structure.

Constraint:
UX = UY = UZ = 0

2. APPLIED LOAD
--------------------------------------------------
Location:
Upper engine-mount / boss region

Load magnitude:
{APPLIED_LOAD_N:.2f} N

Global direction:
X = {LOAD_DIRECTION[0]}
Y = {LOAD_DIRECTION[1]}
Z = {LOAD_DIRECTION[2]}

Unit direction:
X = {unit_direction[0]:.3f}
Y = {unit_direction[1]:.3f}
Z = {unit_direction[2]:.3f}

Force components:
Fx = {fx:.2f} N
Fy = {fy:.2f} N
Fz = {fz:.2f} N

3. UNITS
--------------------------------------------------
Length : mm
Force  : N
Stress : MPa

4. IMPORTANT ENGINEERING NOTE
--------------------------------------------------
The {APPLIED_LOAD_N:.0f} N load is a demonstration/
assumption for constructing the CAE workflow.

It must be replaced by the actual engine-load/design
requirement before final engineering conclusions are
made.

This script documents the intended boundary conditions.
It does NOT apply them to an ANSYS or HyperWorks solver
and does NOT generate FEA stress or deformation results.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    print("\nBoundary-condition report created:")
    print(REPORT_FILE)

    print("\nIMPORTANT:")
    print("This script documents the model inputs only.")
    print("No solver results were generated.")


if __name__ == "__main__":
    main()
