# Automotive Engine Mount FEA

## Overview

This project presents a Computer-Aided Engineering (CAE) workflow for the structural study of an automotive engine mount bracket.

The project covers the major stages of a typical Finite Element Analysis (FEA) workflow:

**CAD Geometry → Material Definition → Meshing → Boundary Conditions → Static Structural Analysis → Topology Optimization → Validation**

Python scripts are used for geometry preparation, workflow documentation, engineering calculations, and result post-processing. OpenCascade is used to generate and inspect the STEP geometry.

> **Note:** Actual ANSYS/HyperWorks solver results are kept separate from the Python workflow. Placeholder fields are not presented as real FEA results.

---

## Project Objectives

- Develop a structured CAE workflow for an engine mount bracket.
- Import and validate STEP CAD geometry.
- Define material properties and engineering assumptions.
- Prepare a mesh strategy and mesh-convergence framework.
- Define structural boundary conditions and loading.
- Evaluate Von Mises stress, deformation, and factor of safety from actual solver results.
- Investigate topology optimization for potential mass reduction.
- Compare original and optimized designs through validation.

---

## Project Structure

```text
Automotive_Engine_Mount_FEA/
│
├── 01_Geometry/
│   ├── engine_mount_bracket.step
│   ├── create_engine_mount_step.py
│   ├── geometry_import.py
│   └── geometry_import_report.txt
│
├── 02_Material/
│   ├── material_properties.pdf
│   ├── material_properties.py
│   └── material_report.txt
│
├── 03_Meshing/
│   ├── mesh_setup.py
│   ├── mesh_convergence_template.csv
│   └── mesh_setup_report.txt
│
├── 04_Boundary_Conditions/
│   ├── load_setup.py
│   └── boundary_conditions_report.txt
│
├── 05_Static_Structural/
│   ├── static_structural_analysis.py
│   ├── solver_results.csv
│   └── static_structural_report.txt
│
├── 06_Topology_Optimization/
│   ├── topology_optimization.py
│   ├── optimization_results.csv
│   └── topology_optimization_report.txt
│
└── 07_Validation/
    ├── validation.py
    ├── validation_results.csv
    └── validation_report.txt

1. Geometry

The engine mount bracket geometry is represented as a STEP CAD model.

The geometry stage performs:

STEP generation
STEP import
OpenCascade validation
Solid, shell, face, edge, and vertex counting
Geometry import reporting
Tools
Python
OpenCascade
STEP format
2. Material Definition

The material stage stores the structural material parameters required for FEA.

Typical properties include:

Young's modulus
Poisson's ratio
Density
Yield strength
Ultimate tensile strength

Material values should be verified against the project's material specification before being used for final engineering conclusions.

3. Meshing

The model uses a 3D solid tetrahedral mesh strategy.

The mesh-study framework includes target element sizes:

8 mm
6 mm
4 mm
3 mm
2 mm

Important mesh-quality parameters include:

Aspect ratio
Skewness
Jacobian
Warpage
Element angles
Local refinement

Local refinement is particularly important around:

Bolt holes
Fillets
Sharp transitions
Load-transfer regions
Fixed-support regions
Contact interfaces
Mesh Convergence

Mesh convergence is evaluated by progressively refining the mesh and comparing important response quantities such as:

Maximum Von Mises stress
Total deformation

A convergence tolerance is defined for comparison between successive meshes.

4. Boundary Conditions

The demonstration structural model defines:

Fixed Support

The base mounting regions are treated as structural attachment regions.

Applied Load

A demonstration load is defined in the global coordinate system for constructing the workflow.

The load value is an input assumption and must be replaced with the actual engineering design load before using the model for final conclusions.

5. Static Structural Analysis

The static structural stage is designed to process actual solver outputs.

Important quantities include:

Von Mises Stress

Used as an equivalent stress measure for evaluating yielding of ductile materials.

Total Deformation

Used to evaluate the structural displacement response.

Factor of Safety

For a simple yield-based check:

Factor of Safety =
Yield Strength / Maximum Von Mises Stress

The Python post-processing script calculates these quantities from actual solver results entered into the project.

6. Topology Optimization

Topology optimization is used to investigate potential material reduction while maintaining structural requirements.

Typical setup:

Design variable:
Material distribution

Objective:
Reduce structural mass

Constraints:
Stress / deformation / factor of safety

Non-design regions:
Mounting and load-transfer regions

The optimized geometry should subsequently be reconstructed into manufacturable CAD, re-meshed, and re-analyzed.

7. Validation

The validation stage compares the original and optimized designs using:

Mass
Von Mises stress
Total deformation
Factor of safety

The purpose is to verify that optimization results are consistent with the defined structural requirements.

Engineering Workflow
          CAD GEOMETRY
               ↓
        Geometry Validation
               ↓
        Material Definition
               ↓
             Meshing
               ↓
      Boundary Conditions
               ↓
     Static Structural FEA
               ↓
      Stress / Deformation
               ↓
      Topology Optimization
               ↓
       Reconstructed CAD
               ↓
      Re-meshing & Re-analysis
               ↓
           Validation
Technologies Used
Python
OpenCascade (OCP)
STEP CAD
Finite Element Analysis
CAE methodology
ANSYS / HyperWorks workflow concepts
OptiStruct workflow concepts
CSV-based engineering data processing
Key CAE Concepts Demonstrated
Finite Element Method (FEM)
Finite Element Analysis (FEA)
CAD geometry preparation
Mesh generation
Mesh quality
Mesh convergence
Boundary conditions
Load application
Von Mises stress
Total deformation
Factor of safety
Topology optimization
Structural validation
Current Status
Geometry                     ✅
Material framework           ✅
Mesh framework               ✅
Boundary-condition framework ✅
Static-analysis framework    ✅
Topology-optimization        ✅
Validation framework         ✅

The project intentionally separates workflow automation from actual FEA solver output. Solver-derived values should only be added after running the corresponding ANSYS or HyperWorks/OptiStruct analysis.

Author

Abitha Chokka

Electronics & Communication Engineering

Areas of Interest
CAE / FEA
Structural Analysis
Automotive Engineering
Embedded Systems
Engineering Simulation
Python
