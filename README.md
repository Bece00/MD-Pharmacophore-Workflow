MD-Pharmacophore-Workflow: Automated Snapshot Extraction & Interaction Profiling

Automated Interaction Profiling with Docker-PLIP: From Raw MD Trajectories to Interface Analysis.


## 🚀 Overview

Modern drug discovery requires understanding the dynamic nature of protein-ligand interactions. This workflow automates the transition from raw MD data to structured interaction profiles by:

    Equilibrium Extraction: Isolating the stable production phase of the simulation.

    Structural Standardization: Stripping solvents and performing RMS alignment.

    Automated Batch Processing: Renaming and organizing snapshots for high-throughput analysis.

    Reproducible Environment: Ensuring cross-platform compatibility via Docker.

## 🛠️ Technical Stack

    Molecular Dynamics: Amber/Cpptraj

    Interaction Analysis: PLIP (Protein-Ligand Interaction Profiler)

    Containerization: Docker

    Scripting: Python & Bash

  ##  📁 Project Structure
    MD-Pharmacophore-Workflow/
├── scripts/
│   ├── extract_last_1us.in   # Cpptraj script for trajectory processing
│   ├── rename_frames.sh      # Bash script for batch file renaming
│   └── extract_xml.py        # Python script to parse PLIP XML outputs
├── docker/
│   └── Dockerfile            # Container definition for reproducibility
└── README.md


## ⚙️ Methodology

### 1. Trajectory Processing

The workflow utilizes cpptraj to extract the final 1μs of the production run (Frames 4001-5000), ensuring that the analysis is performed on an equilibrated system. Solvent molecules and ions are stripped to optimize computational resources.
### 2. Snapshot Standardization

Individual snapshots are extracted and processed using rename_frames.sh. This script fixes naming conventions (e.g., converting .pdb.X to _X.pdb) to ensure compatibility with batch analysis tools.


### 3. Interaction Profiling

The extracted snapshots are subjected to batch PLIP analysis. The extract_xml.py script parses the resulting XML data to identify recurring interaction patterns (Hydrogen bonds, Hydrophobic contacts, etc.), which are then used to build dynamic pharmacophore models.

## 🐳 Running with Docker

This project is containerized to ensure a reproducible research environment. You don't need to install PLIP or its dependencies locally.

### 1. Build the Custom Image
Build the Docker image using the provided Dockerfile. This integrates our specialized BRAF analysis scripts into the PLIP environment:
```bash
docker build -t braf-workflow ./docker
```

### 2. Execute the Automated Pipeline

Run the high-throughput analysis script. It will automatically handle snapshot processing and interaction profiling using 14 threads:
./scripts/run_plip.sh