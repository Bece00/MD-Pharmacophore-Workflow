#!/bin/bash

# Directory containing the PDB files
IN_DIR="frames"

echo "--- Renaming Files: .pdb.X -> _X.pdb ---"

# Navigate into the target directory
if cd "$IN_DIR"; then
    count=0
    
    # Loop through all files matching the pattern run*_frame.pdb.*
    # This handles run1, run2, run3, etc., automatically
    for f in run*_frame.pdb.*; do
        # Ensure the file exists before processing
        [ -e "$f" ] || continue
        
        # Extract the frame number (the part after the last dot)
        num="${f##*.}"
        
        # Extract the base name (the part before .pdb.)
        base_name="${f%.pdb.*}"
        
        # Construct the new filename: e.g., run1_frame_45.pdb
        new_name="${base_name}_${num}.pdb"
        
        # Perform the rename
        mv "$f" "$new_name"
        ((count++))
    done
    
    cd ..
    echo "--- PROCESS COMPLETE ---"
    echo "$count files have been successfully renamed."
else
    echo "Error: Directory '$IN_DIR' not found!"
    exit 1
fi