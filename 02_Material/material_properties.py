from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_FILE = PROJECT_ROOT / "02_Material" / "material_report.txt"


# ---------------------------------------------------------
# DEMONSTRATION STRUCTURAL STEEL DATA
# ---------------------------------------------------------
# Replace these values with the actual material values
# from material_properties.pdf before claiming final FEA
# results.
# ---------------------------------------------------------

MATERIAL_NAME = "Structural Steel (Demo)"

YOUNGS_MODULUS_GPA = 200.0
POISSON_RATIO = 0.30
DENSITY_KG_M3 = 7850.0
YIELD_STRENGTH_MPA = 250.0
ULTIMATE_STRENGTH_MPA = 460.0


def calculate_factor_of_safety(von_mises_mpa):
    """Calculate simple yield-based factor of safety."""
    if von_mises_mpa <= 0:
        raise ValueError("Von Mises stress must be greater than zero.")

    return YIELD_STRENGTH_MPA / von_mises_mpa


def main():
    print("=" * 60)
    print("AUTOMOTIVE ENGINE MOUNT - MATERIAL DEFINITION")
    print("=" * 60)

    print("\nMaterial:")
    print(f"  Name                : {MATERIAL_NAME}")
    print(f"  Young's Modulus     : {YOUNGS_MODULUS_GPA} GPa")
    print(f"  Poisson Ratio       : {POISSON_RATIO}")
    print(f"  Density             : {DENSITY_KG_M3} kg/m^3")
    print(f"  Yield Strength      : {YIELD_STRENGTH_MPA} MPa")
    print(f"  Ultimate Strength   : {ULTIMATE_STRENGTH_MPA} MPa")

    timestamp = datetime.now(timezone.utc).isoformat()

    report = f"""
AUTOMOTIVE ENGINE MOUNT FEA
MATERIAL REPORT
==================================================

Generated UTC:
{timestamp}

Material:
{MATERIAL_NAME}

Properties:
--------------------------------------------------
Young's Modulus      : {YOUNGS_MODULUS_GPA} GPa
Poisson Ratio        : {POISSON_RATIO}
Density              : {DENSITY_KG_M3} kg/m^3
Yield Strength       : {YIELD_STRENGTH_MPA} MPa
Ultimate Strength    : {ULTIMATE_STRENGTH_MPA} MPa

IMPORTANT:
These are demonstration structural-steel values.
Verify and replace them using material_properties.pdf
before using them as final project data.

Factor of safety:
FoS = Yield Strength / Maximum Von Mises Stress

No solver stress result is assumed or fabricated by this script.
"""

    REPORT_FILE.write_text(
        report.strip() + "\n",
        encoding="utf-8"
    )

    print("\nMaterial report created:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()
