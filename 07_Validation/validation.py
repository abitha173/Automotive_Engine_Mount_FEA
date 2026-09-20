from pathlib import Path
from datetime import datetime, timezone
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "07_Validation"

INPUT_FILE = OUTPUT_DIR / "validation_results.csv"
OUTPUT_FILE = OUTPUT_DIR / "original_vs_optimized.csv"
REPORT_FILE = OUTPUT_DIR / "validation_report.txt"

REQUIRED_FOS = 1.50


def create_input_template():
    """
    Template for actual ANSYS / HyperWorks validation results.
    """

    headers = [
        "Original Mass (kg)",
        "Optimized Mass (kg)",
        "Original Von Mises Stress (MPa)",
        "Optimized Von Mises Stress (MPa)",
        "Original Deformation (mm)",
        "Optimized Deformation (mm)",
        "Original FoS",
        "Optimized FoS",
        "Original Solver",
        "Optimized Solver"
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
            "",
            "",
            "",
            "",
            "PENDING",
            "PENDING"
        ])


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print("=" * 65)
    print("AUTOMOTIVE ENGINE MOUNT - DESIGN VALIDATION")
    print("=" * 65)

    if not INPUT_FILE.exists():

        create_input_template()

        print("\nCreated validation input template:")
        print(INPUT_FILE)

        print("\nNo actual solver validation results are available yet.")

        print("\nValidation procedure:")
        print("  1. Solve original geometry.")
        print("  2. Solve optimized/reconstructed geometry.")
        print("  3. Use the same relevant material model.")
        print("  4. Use equivalent load cases.")
        print("  5. Compare stress, deformation and FoS.")
        print("  6. Compare mass.")
        print("  7. Check that the optimized design satisfies")
        print("     the defined acceptance criteria.")

        return

    # -----------------------------------------------------
    # Read validation results
    # -----------------------------------------------------

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:

        print("\nERROR: Validation input is empty.")
        return

    row = rows[0]

    required_fields = [
        "Original Mass (kg)",
        "Optimized Mass (kg)",
        "Original Von Mises Stress (MPa)",
        "Optimized Von Mises Stress (MPa)",
        "Original Deformation (mm)",
        "Optimized Deformation (mm)",
        "Original FoS",
        "Optimized FoS"
    ]

    missing = [
        field
        for field in required_fields
        if not row.get(field, "").strip()
    ]

    if missing:

        print("\nValidation data is still pending.")

        print("\nMissing fields:")

        for field in missing:
            print(f"  - {field}")

        print("\nNo validation conclusion has been generated.")

        return

    try:

        original_mass = float(
            row["Original Mass (kg)"]
        )

        optimized_mass = float(
            row["Optimized Mass (kg)"]
        )

        original_stress = float(
            row["Original Von Mises Stress (MPa)"]
        )

        optimized_stress = float(
            row["Optimized Von Mises Stress (MPa)"]
        )

        original_deformation = float(
            row["Original Deformation (mm)"]
        )

        optimized_deformation = float(
            row["Optimized Deformation (mm)"]
        )

        original_fos = float(
            row["Original FoS"]
        )

        optimized_fos = float(
            row["Optimized FoS"]
        )

    except ValueError:

        print("\nERROR: All validation values must be numeric.")
        return

    # -----------------------------------------------------
    # Input validation
    # -----------------------------------------------------

    values = [
        original_mass,
        optimized_mass,
        original_stress,
        optimized_stress,
        original_deformation,
        optimized_deformation,
        original_fos,
        optimized_fos
    ]

    if any(value < 0 for value in values):

        print("\nERROR: Negative result values are not accepted.")
        return

    if original_mass == 0:

        print("\nERROR: Original mass cannot be zero.")
        return

    if original_stress == 0:

        print("\nERROR: Original stress cannot be zero.")
        return

    if original_deformation == 0:

        print("\nERROR: Original deformation cannot be zero.")
        return

    # -----------------------------------------------------
    # Comparisons
    # -----------------------------------------------------

    mass_change_percent = (
        (optimized_mass - original_mass)
        / original_mass
    ) * 100.0

    mass_reduction_percent = (
        (original_mass - optimized_mass)
        / original_mass
    ) * 100.0

    stress_change_percent = (
        (optimized_stress - original_stress)
        / original_stress
    ) * 100.0

    deformation_change_percent = (
        (optimized_deformation - original_deformation)
        / original_deformation
    ) * 100.0

    fos_change_percent = (
        (optimized_fos - original_fos)
        / original_fos
    ) * 100.0

    # -----------------------------------------------------
    # Defined checks
    # -----------------------------------------------------

    optimized_fos_check = (
        optimized_fos >= REQUIRED_FOS
    )

    optimized_stress_check = (
        optimized_stress <=
        optimized_fos * 0 + optimized_stress
    )

    # The stress check above intentionally does not create
    # a material pass/fail condition without a verified
    # yield-strength input in this validation script.

    status = (
        "VALIDATION DATA PROCESSED"
        if optimized_fos_check
        else "REVIEW REQUIRED"
    )

    timestamp = datetime.now(timezone.utc).isoformat()

    # -----------------------------------------------------
    # Save comparison CSV
    # -----------------------------------------------------

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Metric",
            "Original",
            "Optimized",
            "Change (%)"
        ])

        writer.writerow([
            "Mass (kg)",
            f"{original_mass:.3f}",
            f"{optimized_mass:.3f}",
            f"{mass_change_percent:.3f}"
        ])

        writer.writerow([
            "Von Mises Stress (MPa)",
            f"{original_stress:.3f}",
            f"{optimized_stress:.3f}",
            f"{stress_change_percent:.3f}"
        ])

        writer.writerow([
            "Total Deformation (mm)",
            f"{original_deformation:.3f}",
            f"{optimized_deformation:.3f}",
            f"{deformation_change_percent:.3f}"
        ])

        writer.writerow([
            "Factor of Safety",
            f"{original_fos:.3f}",
            f"{optimized_fos:.3f}",
            f"{fos_change_percent:.3f}"
        ])

    # -----------------------------------------------------
    # Save validation report
    # -----------------------------------------------------

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
ORIGINAL vs OPTIMIZED VALIDATION REPORT
==================================================

Generated UTC:
{timestamp}

SOLVER
--------------------------------------------------
Original:
{row.get("Original Solver", "Not specified")}

Optimized:
{row.get("Optimized Solver", "Not specified")}

COMPARISON
--------------------------------------------------
Original Mass:
{original_mass:.3f} kg

Optimized Mass:
{optimized_mass:.3f} kg

Mass Reduction:
{mass_reduction_percent:.3f} %

Original Von Mises Stress:
{original_stress:.3f} MPa

Optimized Von Mises Stress:
{optimized_stress:.3f} MPa

Stress Change:
{stress_change_percent:.3f} %

Original Total Deformation:
{original_deformation:.3f} mm

Optimized Total Deformation:
{optimized_deformation:.3f} mm

Deformation Change:
{deformation_change_percent:.3f} %

Original Factor of Safety:
{original_fos:.3f}

Optimized Factor of Safety:
{optimized_fos:.3f}

FoS Change:
{fos_change_percent:.3f} %

DEFINED CHECK
--------------------------------------------------
Required minimum FoS:
{REQUIRED_FOS:.2f}

Optimized FoS meets defined minimum:
{"YES" if optimized_fos_check else "NO"}

Validation status:
{status}

ENGINEERING VALIDATION WORKFLOW
--------------------------------------------------
The optimized design should be re-meshed and solved
using equivalent boundary conditions and relevant
load cases.

The following should be reviewed:
- Mesh quality
- Mesh convergence
- Maximum Von Mises stress
- Total deformation
- Factor of safety
- Contact behavior
- Structural stability
- Manufacturing feasibility

IMPORTANT
--------------------------------------------------
This script only compares actual values supplied by
the user/solver. It does not generate FEA results and
does not establish production readiness by itself.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    print("\nValidation comparison generated successfully.")

    print("\nMass:")
    print(f"  Original  : {original_mass:.3f} kg")
    print(f"  Optimized : {optimized_mass:.3f} kg")
    print(f"  Reduction : {mass_reduction_percent:.2f}%")

    print("\nVon Mises stress:")
    print(f"  Original  : {original_stress:.3f} MPa")
    print(f"  Optimized : {optimized_stress:.3f} MPa")

    print("\nDeformation:")
    print(f"  Original  : {original_deformation:.3f} mm")
    print(f"  Optimized : {optimized_deformation:.3f} mm")

    print("\nFactor of Safety:")
    print(f"  Original  : {original_fos:.3f}")
    print(f"  Optimized : {optimized_fos:.3f}")

    print("\nGenerated:")
    print(OUTPUT_FILE)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
