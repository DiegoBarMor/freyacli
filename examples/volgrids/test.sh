#!/bin/bash
set -uo pipefail

clear
items=(
    ""

    "smiffer"
    "smiffer prot" # err: missing required argument
    "smiffer rna" # err: missing required argument
    "smiffer ligand" # err: missing required argument

    "smutils"
    "smutils resids_nonbp" # err: missing required argument

    "apbs"

    "vgtools" # err: missing required argument
    "vgtools convert" # err: missing required argument
    "vgtools pack" # err: missing required argument
    "vgtools unpack" # err: missing required argument
    "vgtools fix_cmap" # err: missing required argument
    "vgtools average" # err: missing required argument
    "vgtools summary" # err: missing required argument
    "vgtools compare" # err: missing required argument
    "vgtools rotate" # err: missing required argument


    "unknown_command" # err: unrecognized command
    "smiffer prot fake_path.pdb" # err: file path doesn't exist
    "smiffer prot README.md"
)
for item in "${items[@]}"; do
    echo "========== TEST: $item =========="
    # shellcheck disable=SC2086
    python3 examples/volgrids/main.py $item
done
