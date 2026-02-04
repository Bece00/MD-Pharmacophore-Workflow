#!/bin/bash

# --- CONFIGURATION ---
INPUT_DIR="plip_inputs"
OUTPUT_DIR="plip_results"
DOCKER_IMAGE="pharmai/plip:latest"
MAX_THREADS=14 # Optimized for high-throughput processing

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"
HOST_PWD=$(pwd)

echo "🚀 Starting Batch PLIP Analysis (using $MAX_THREADS threads)..."

for f in "$INPUT_DIR"/*.pdb; do
    if [ -f "$f" ]; then
        base_name=$(basename -- "$f" .pdb)
        FRAME_OUT="$OUTPUT_DIR/${base_name}_plip"
        
        # Skip if report.xml already exists to save time (Resume capability)
        if [ -f "$FRAME_OUT/report.xml" ]; then
            echo "Skipping $base_name: Analysis already completed."
            continue
        fi

        echo "Processing snapshot: $base_name"
        mkdir -p "$FRAME_OUT"
        
        # --- DOCKER ORCHESTRATION ---
        # --xml: Generates XML reports for systematic data extraction
        # --nofix / --nohydro: Preserves original MD simulation coordinates
        docker run --rm -v "${HOST_PWD}":/data -w /data \
            "$DOCKER_IMAGE" \
            -f "$f" \
            -o "$FRAME_OUT" \
            --xml \
            --nofix \
            --nohydro \
            --maxthreads "$MAX_THREADS"
    fi
done

# Fix file permissions (Required for Docker-root generated files)
# As an IT Systems Support Assistant, I've automated this to ensure user-level access [cite: 108]
sudo chown -R $USER:$USER "$OUTPUT_DIR"

echo "--- BATCH ANALYSIS COMPLETE ---"