from pathlib import Path

from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.IFSelect import IFSelect_ReturnStatus
from OCP.BRepCheck import BRepCheck_Analyzer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "01_Geometry" / "engine_mount_bracket.step"


def fuse(shape_a, shape_b):
    """Fuse two OpenCascade solids."""
    result = BRepAlgoAPI_Fuse(shape_a, shape_b)
    result.Build()

    if not result.IsDone():
        raise RuntimeError("Boolean fuse operation failed.")

    return result.Shape()


def cut(shape_a, shape_b):
    """Cut shape_b from shape_a."""
    result = BRepAlgoAPI_Cut(shape_a, shape_b)
    result.Build()

    if not result.IsDone():
        raise RuntimeError("Boolean cut operation failed.")

    return result.Shape()


def box(x, y, z, dx, dy, dz):
    """Create a rectangular solid."""
    return BRepPrimAPI_MakeBox(
        gp_Pnt(x, y, z),
        dx,
        dy,
        dz
    ).Shape()


def cylinder_y(x, y, z, radius, length):
    """Create cylinder along +Y direction."""
    axis = gp_Ax2(
        gp_Pnt(x, y, z),
        gp_Dir(0, 1, 0)
    )

    return BRepPrimAPI_MakeCylinder(
        axis,
        radius,
        length
    ).Shape()


def cylinder_z(x, y, z, radius, length):
    """Create cylinder along +Z direction."""
    axis = gp_Ax2(
        gp_Pnt(x, y, z),
        gp_Dir(0, 0, 1)
    )

    return BRepPrimAPI_MakeCylinder(
        axis,
        radius,
        length
    ).Shape()


def main():
    print("=" * 65)
    print("AUTOMOTIVE ENGINE MOUNT BRACKET - STEP GENERATOR")
    print("=" * 65)

    print("\nCreating demonstration engine-mount bracket...")

    # ---------------------------------------------------------
    # Overall design dimensions (mm)
    # ---------------------------------------------------------

    base_length = 140.0
    base_width = 100.0
    base_thickness = 12.0

    # ---------------------------------------------------------
    # 1. Base plate
    # ---------------------------------------------------------

    shape = box(
        0,
        0,
        0,
        base_length,
        base_width,
        base_thickness
    )

    # ---------------------------------------------------------
    # 2. Left and right vertical mounting ears
    # ---------------------------------------------------------

    left_ear = box(
        15,
        15,
        12,
        18,
        70,
        65
    )

    right_ear = box(
        107,
        15,
        12,
        18,
        70,
        65
    )

    shape = fuse(shape, left_ear)
    shape = fuse(shape, right_ear)

    # ---------------------------------------------------------
    # 3. Cylindrical bosses at top of mounting ears
    # ---------------------------------------------------------

    left_boss = cylinder_y(
        24,
        15,
        77,
        18,
        70
    )

    right_boss = cylinder_y(
        116,
        15,
        77,
        18,
        70
    )

    shape = fuse(shape, left_boss)
    shape = fuse(shape, right_boss)

    # ---------------------------------------------------------
    # 4. Bolt holes through the two vertical ears
    # ---------------------------------------------------------

    left_hole = cylinder_y(
        24,
        14,
        77,
        8,
        72
    )

    right_hole = cylinder_y(
        116,
        14,
        77,
        8,
        72
    )

    shape = cut(shape, left_hole)
    shape = cut(shape, right_hole)

    # ---------------------------------------------------------
    # 5. Four mounting holes through base plate
    # ---------------------------------------------------------

    base_hole_positions = [
        (20, 20),
        (120, 20),
        (20, 80),
        (120, 80),
    ]

    for x, y in base_hole_positions:
        hole = cylinder_z(
            x,
            y,
            -1,
            7,
            base_thickness + 2
        )

        shape = cut(shape, hole)

    # ---------------------------------------------------------
    # 6. Geometry validity check
    # ---------------------------------------------------------

    analyzer = BRepCheck_Analyzer(shape)

    if not analyzer.IsValid():
        raise RuntimeError(
            "Generated CAD geometry failed the OpenCascade validity check."
        )

    if shape.IsNull():
        raise RuntimeError("Generated CAD shape is null.")

    # ---------------------------------------------------------
    # 7. Export STEP
    # ---------------------------------------------------------

    writer = STEPControl_Writer()

    writer.Transfer(shape, STEPControl_AsIs)

    status = writer.Write(str(OUTPUT_FILE))

    if status != IFSelect_ReturnStatus.IFSelect_RetDone:
        raise RuntimeError(
            f"STEP export failed. Status: {status}"
        )

    print("\nSTEP generation completed successfully.")
    print(f"\nOutput:")
    print(OUTPUT_FILE)

    print("\nApproximate design dimensions:")
    print("  Base      : 140 x 100 x 12 mm")
    print("  Ear height: 65 mm")
    print("  Ear hole  : 16 mm diameter")
    print("  Base holes: 14 mm diameter")

    print("\nGeometry validity: VALID")
    print("\nThe STEP file is ready for geometry import.")


if __name__ == "__main__":
    main()
