from pathlib import Path
from datetime import datetime, timezone
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "06_Topology_Optimization"

INPUT_FILE = OUTPUT_DIR / "optimization_results.csv"
OUTPUT_FILE = OUTPUT_DIR / "topology_optimization_report.csv"
REPORT_FILE = OUTPUT_DIR / "topology_optimization_report.txt"


# =========================================================
# OPTIMIZATION TARGETS
# =========================================================

TARGET_MASS_REDUCTION_PERCENT = 20.0

# Minimum acceptable factor of safety after optimization
REQUIRED_FOS = 1.50


def create_input_template():
    """
    Create a template for actual optimization results
    exported from ANSYS or HyperWorks/OptiStruct.
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
    print("AUTOMOTIVE ENGINE MOUNT - TOPOLOGY OPTIMIZATION")
    print("=" * 65)

    print("\nOptimization objective:")
    print(
        f"  Target mass reduction: "
        f"{TARGET_MASS_REDUCTION_PERCENT:.1f}%"
    )

    print(f"  Required minimum FoS : {REQUIRED_FOS:.2f}")

    print("\nRecommended optimization setup:")
    print("  Design variable  : Material distribution")
    print("  Objective        : Reduce structural mass")
    print("  Constraints      : Stress / displacement / FoS")
    print("  Non-design areas : Mounting and load-transfer regions")

    # -----------------------------------------------------
    # Create template
    # -----------------------------------------------------

    if not INPUT_FILE.exists():

        create_input_template()

        print("\nCreated optimization result template:")
        print(INPUT_FILE)

        print("\nNo solver optimization results are available yet.")

        print("\nThe actual optimization should be performed in:")
        print("  ANSYS Mechanical / Discovery")
        print("  or")
        print("  Altair OptiStruct")

        return

    # -----------------------------------------------------
    # Read actual solver output
    # -----------------------------------------------------

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("\nERROR: Optimization result file is empty.")
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

    # -----------------------------------------------------
    # Check whether actual results exist
    # -----------------------------------------------------

    missing = [
        field
        for field in required_fields
        if not row.get(field, "").strip()
    ]

    if missing:

        print("\nOptimization results are still pending.")

        print("\nMissing values:")
        for field in missing:
            print(f"  - {field}")

        print("\nNo optimization conclusion has been generated.")

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
        print("\nERROR: Optimization result values must be numeric.")
        return

    # -----------------------------------------------------
    # Validate inputs
    # -----------------------------------------------------

    if original_mass <= 0:
        print("\nERROR: Original mass must be greater than zero.")
        return

    if optimized_mass <= 0:
        print("\nERROR: Optimized mass must be greater than zero.")
        return

    # -----------------------------------------------------
    # Engineering calculations
    # -----------------------------------------------------

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

    target_achieved = (
        mass_reduction_percent
        >= TARGET_MASS_REDUCTION_PERCENT
    )

    fos_requirement_met = (
        optimized_fos >= REQUIRED_FOS
    )

    # This is a factual check against the user-defined
    # acceptance conditions, not a general claim that
    # the design is production-ready.

    if target_achieved and fos_requirement_met:
        status = "MEETS DEFINED OPTIMIZATION CHECK"
    else:
        status = "DOES NOT MEET DEFINED OPTIMIZATION CHECK"

    solver = row.get("Solver", "").strip()

    timestamp = datetime.now(timezone.utc).isoformat()

    # -----------------------------------------------------
    # Save results CSV
    # -----------------------------------------------------

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Parameter",
            "Value"
        ])

        writer.writerow([
            "Solver",
            solver
        ])

        writer.writerow([
            "Original Mass (kg)",
            f"{original_mass:.3f}"
        ])

        writer.writerow([
            "Optimized Mass (kg)",
            f"{optimized_mass:.3f}"
        ])

        writer.writerow([
            "Mass Reduction (%)",
            f"{mass_reduction_percent:.3f}"
        ])

        writer.writerow([
            "Original Von Mises Stress (MPa)",
            f"{original_stress:.3f}"
        ])

        writer.writerow([
            "Optimized Von Mises Stress (MPa)",
            f"{optimized_stress:.3f}"
        ])

        writer.writerow([
            "Stress Change (%)",
            f"{stress_change_percent:.3f}"
        ])

        writer.writerow([
            "Original Deformation (mm)",
            f"{original_deformation:.3f}"
        ])

        writer.writerow([
            "Optimized Deformation (mm)",
            f"{optimized_deformation:.3f}"
        ])

        writer.writerow([
            "Deformation Change (%)",
            f"{deformation_change_percent:.3f}"
        ])

        writer.writerow([
            "Original FoS",
            f"{original_fos:.3f}"
        ])

        writer.writerow([
            "Optimized FoS",
            f"{optimized_fos:.3f}"
        ])

        writer.writerow([
            "Target Mass Reduction (%)",
            f"{TARGET_MASS_REDUCTION_PERCENT:.3f}"
        ])

        writer.writerow([
            "Required FoS",
            f"{REQUIRED_FOS:.3f}"
        ])

        writer.writerow([
            "Status",
            status
        ])

    # -----------------------------------------------------
    # Save report
    # -----------------------------------------------------

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
TOPOLOGY OPTIMIZATION REPORT
==================================================

Generated UTC:
{timestamp}

Solver:
{solver}

OPTIMIZATION OBJECTIVE
--------------------------------------------------
Target mass reduction:
{TARGET_MASS_REDUCTION_PERCENT:.2f} %

Required minimum FoS:
{REQUIRED_FOS:.2f}

RESULTS
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

Original Deformation:
{original_deformation:.3f} mm

Optimized Deformation:
{optimized_deformation:.3f} mm

Deformation Change:
{deformation_change_percent:.3f} %

Original Factor of Safety:
{original_fos:.3f}

Optimized Factor of Safety:
{optimized_fos:.3f}

DEFINED CHECKS
--------------------------------------------------
Target mass reduction achieved:
{"YES" if target_achieved else "NO"}

Minimum FoS requirement met:
{"YES" if fos_requirement_met else "NO"}

Status:
{status}

IMPORTANT ENGINEERING NOTE
--------------------------------------------------
Topology optimization does not by itself establish that
a design is ready for manufacture or service.

The optimized geometry should be:
1. Reconstructed as manufacturable CAD.
2. Re-meshed.
3. Re-analyzed using the same relevant loading cases.
4. Checked for stress, deformation, stability and
   other required performance criteria.
5. Reviewed against manufacturing constraints.

This report only processes actual solver results.
It does not fabricate optimization results.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    print("\nOptimization post-processing completed.")

    print("\nResults:")
    print(f"  Mass reduction : {mass_reduction_percent:.2f}%")
    print(f"  Optimized stress : {optimized_stress:.2f} MPa")
    print(f"  Optimized deformation : {optimized_deformation:.2f} mm")
    print(f"  Optimized FoS : {optimized_fos:.2f}")
    print(f"  Status : {status}")

    print("\nGenerated:")
    print(OUTPUT_FILE)
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
