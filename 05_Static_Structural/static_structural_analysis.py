from pathlib import Path
from datetime import datetime, timezone
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "05_Static_Structural"

INPUT_FILE = OUTPUT_DIR / "solver_results.csv"
OUTPUT_FILE = OUTPUT_DIR / "static_structural_results.csv"
REPORT_FILE = OUTPUT_DIR / "static_structural_report.txt"


# =========================================================
# MATERIAL INPUT
# =========================================================
# Replace with the verified material value from your
# material_properties.pdf before final analysis.
# =========================================================

YIELD_STRENGTH_MPA = 250.0

# Minimum desired factor of safety
REQUIRED_FOS = 1.50


def calculate_factor_of_safety(yield_strength, von_mises):
    if von_mises <= 0:
        raise ValueError("Von Mises stress must be greater than zero.")

    return yield_strength / von_mises


def calculate_yield_utilization(von_mises, yield_strength):
    return von_mises / yield_strength


def create_input_template():
    """
    Create a template for values exported from ANSYS,
    HyperWorks, or another FEA solver.
    """

    headers = [
        "Maximum Von Mises Stress (MPa)",
        "Total Deformation (mm)",
        "Maximum Principal Stress (MPa)",
        "Minimum Principal Stress (MPa)",
        "Solver"
    ]

    with INPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(headers)

        writer.writerow([
            "",
            "",
            "",
            "",
            "PENDING"
        ])


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 65)
    print("AUTOMOTIVE ENGINE MOUNT - STATIC STRUCTURAL ANALYSIS")
    print("=" * 65)

    print("\nMaterial yield strength:")
    print(f"  {YIELD_STRENGTH_MPA:.1f} MPa")

    print("\nRequired factor of safety:")
    print(f"  {REQUIRED_FOS:.2f}")

    # -----------------------------------------------------
    # Create solver-result input template if absent
    # -----------------------------------------------------

    if not INPUT_FILE.exists():
        create_input_template()

        print("\nCreated solver result template:")
        print(INPUT_FILE)

        print("\nNo FEA solver results are available yet.")
        print("Run the model in ANSYS or HyperWorks and")
        print("enter/export the actual results into:")
        print(INPUT_FILE)

        return

    # -----------------------------------------------------
    # Read solver result
    # -----------------------------------------------------

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("\nERROR: Solver result file is empty.")
        return

    row = rows[0]

    stress_text = row.get(
        "Maximum Von Mises Stress (MPa)",
        ""
    ).strip()

    deformation_text = row.get(
        "Total Deformation (mm)",
        ""
    ).strip()

    solver = row.get(
        "Solver",
        ""
    ).strip()

    if not stress_text or not deformation_text:
        print("\nSolver results are still pending.")
        print("\nRequired values:")
        print("  Maximum Von Mises Stress")
        print("  Total Deformation")
        print("\nNo engineering conclusion has been generated.")
        return

    try:
        von_mises = float(stress_text)
        deformation = float(deformation_text)

    except ValueError:
        print("\nERROR: Solver result values must be numeric.")
        return

    if von_mises <= 0:
        print("\nERROR: Von Mises stress must be positive.")
        return

    if deformation < 0:
        print("\nERROR: Total deformation cannot be negative.")
        return

    # -----------------------------------------------------
    # Engineering calculations
    # -----------------------------------------------------

    fos = calculate_factor_of_safety(
        YIELD_STRENGTH_MPA,
        von_mises
    )

    utilization = calculate_yield_utilization(
        von_mises,
        YIELD_STRENGTH_MPA
    )

    passes_fos = fos >= REQUIRED_FOS
    below_yield = von_mises <= YIELD_STRENGTH_MPA

    if passes_fos and below_yield:
        status = "MEETS DEFINED CHECK"
    else:
        status = "DOES NOT MEET DEFINED CHECK"

    timestamp = datetime.now(timezone.utc).isoformat()

    # -----------------------------------------------------
    # Save CSV
    # -----------------------------------------------------

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Solver",
            "Von Mises Stress (MPa)",
            "Total Deformation (mm)",
            "Yield Strength (MPa)",
            "Factor of Safety",
            "Yield Utilization",
            "Status"
        ])

        writer.writerow([
            solver,
            f"{von_mises:.3f}",
            f"{deformation:.3f}",
            f"{YIELD_STRENGTH_MPA:.3f}",
            f"{fos:.3f}",
            f"{utilization:.3f}",
            status
        ])

    # -----------------------------------------------------
    # Save report
    # -----------------------------------------------------

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
STATIC STRUCTURAL ANALYSIS REPORT
==================================================

Generated UTC:
{timestamp}

Solver:
{solver}

RESULTS
--------------------------------------------------
Maximum Von Mises Stress : {von_mises:.3f} MPa
Total Deformation        : {deformation:.3f} mm

MATERIAL
--------------------------------------------------
Yield Strength           : {YIELD_STRENGTH_MPA:.3f} MPa

CALCULATIONS
--------------------------------------------------
Factor of Safety:
FoS = Yield Strength / Maximum Von Mises Stress

FoS = {fos:.3f}

Yield Utilization:
Maximum Von Mises Stress / Yield Strength

Utilization = {utilization:.3f}

DEFINED CHECK
--------------------------------------------------
Required FoS              : {REQUIRED_FOS:.2f}
Factor of Safety obtained : {fos:.3f}

Below yield strength      : {"YES" if below_yield else "NO"}

Result:
{status}

IMPORTANT
--------------------------------------------------
This report should only be generated after actual
solver results have been entered from ANSYS,
HyperWorks/OptiStruct, or another validated FEA solver.

The script does not generate or fabricate FEA stress
or deformation results.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    print("\nStatic structural calculation completed.")

    print("\nResults:")
    print(f"  Von Mises Stress : {von_mises:.3f} MPa")
    print(f"  Deformation      : {deformation:.3f} mm")
    print(f"  Factor of Safety : {fos:.3f}")
    print(f"  Status           : {status}")

    print("\nGenerated:")
    print(OUTPUT_FILE)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
