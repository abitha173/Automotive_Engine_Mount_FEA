from pathlib import Path
from datetime import datetime, timezone
import csv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "03_Meshing"
CSV_FILE = OUTPUT_DIR / "mesh_convergence_template.csv"
REPORT_FILE = OUTPUT_DIR / "mesh_setup_report.txt"


# ---------------------------------------------------------
# MESH STUDY PARAMETERS
# ---------------------------------------------------------
# These are mesh-study INPUTS, not solver results.
# Actual stress/deformation values must be obtained
# from ANSYS/HyperWorks.
# ---------------------------------------------------------

ELEMENT_TYPE = "3D solid"

ELEMENT_ORDER = "Quadratic"

MESH_METHOD = "Tetrahedral"

TARGET_SIZES_MM = [
    8.0,
    6.0,
    4.0,
    3.0,
    2.0,
]

CONVERGENCE_TOLERANCE_PERCENT = 5.0


def write_convergence_template():
    """Create a CSV template for actual solver results."""

    headers = [
        "Element Size (mm)",
        "Element Count",
        "Node Count",
        "Max Von Mises Stress (MPa)",
        "Total Deformation (mm)",
        "Factor of Safety",
        "Stress Change (%)",
        "Deformation Change (%)",
        "Converged?"
    ]

    rows = []

    for size in TARGET_SIZES_MM:
        rows.append([
            size,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "PENDING SOLVER RESULT"
        ])

    with CSV_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def create_report():
    timestamp = datetime.now(timezone.utc).isoformat()

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
MESH SETUP REPORT
==================================================

Generated UTC:
{timestamp}

Mesh Type:
{ELEMENT_TYPE}

Element Order:
{ELEMENT_ORDER}

Mesh Method:
{MESH_METHOD}

Target Element Sizes:
{", ".join(f"{x:.1f} mm" for x in TARGET_SIZES_MM)}

Convergence Tolerance:
{CONVERGENCE_TOLERANCE_PERCENT:.1f} %

Mesh Quality Parameters to Inspect:
--------------------------------------------------
1. Element aspect ratio
2. Skewness
3. Jacobian
4. Warpage
5. Minimum/maximum angles
6. Element quality
7. Local refinement around holes and fillets

Recommended Local Refinement:
--------------------------------------------------
- Bolt holes
- Fillets
- Sharp geometry transitions
- Load application regions
- Fixed-support regions
- Contact interfaces

Mesh Convergence Procedure:
--------------------------------------------------
1. Generate initial coarse mesh.
2. Solve the static structural model.
3. Record maximum Von Mises stress.
4. Record total deformation.
5. Reduce element size.
6. Solve again.
7. Compare the important result quantities.
8. Continue refinement until the selected output
   changes by less than the convergence tolerance.

IMPORTANT:
The convergence CSV contains empty solver-result fields.
No stress, deformation, element count, or FoS values are
invented by this script.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("AUTOMOTIVE ENGINE MOUNT - MESH SETUP")
    print("=" * 65)

    print("\nMesh configuration:")
    print(f"  Element type : {ELEMENT_TYPE}")
    print(f"  Order        : {ELEMENT_ORDER}")
    print(f"  Method       : {MESH_METHOD}")

    print("\nTarget element sizes:")
    for size in TARGET_SIZES_MM:
        print(f"  - {size:.1f} mm")

    print(
        f"\nConvergence tolerance: "
        f"{CONVERGENCE_TOLERANCE_PERCENT:.1f}%"
    )

    write_convergence_template()
    create_report()

    print("\nCreated:")
    print(f"  {CSV_FILE}")
    print(f"  {REPORT_FILE}")

    print("\nNo solver results were generated.")


if __name__ == "__main__":
    main()
