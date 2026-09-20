#!/usr/bin/env python3
"""Create a project summary for the automotive engine mount FEA workflow."""

from pathlib import Path

root = Path(__file__).resolve().parent.parent

folders = [
    '01_Geometry',
    '02_Material',
    '03_Meshing',
    '04_Boundary_Conditions',
    '05_Static_Structural',
    '06_Topology_Optimization',
    '07_Validation',
    '08_Report',
    'docs',
    'scripts',
    'results',
    'templates',
]

for folder in folders:
    path = root / folder
    path.mkdir(exist_ok=True)

print(f"Project initialized at: {root}")
print(f"Folders created: {len(folders)}")
