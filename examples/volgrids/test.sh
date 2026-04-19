#!/bin/bash
set -uo pipefail

clear
items=(
    ""

    "smiffer"
    "smiffer prot"
    "smiffer rna"
    "smiffer ligand"

    "smutils"
    "smutils resids_nonbp"

    "apbs"

    "vgtools"
    "vgtools convert"
    "vgtools pack"
    "vgtools unpack"
    "vgtools fix_cmap"
    "vgtools average"
    "vgtools summary"
    "vgtools compare"
    "vgtools rotate"

    ### Should trigger errors:
    "unknown_command"
)
for item in "${items[@]}"; do
    echo "========== TEST: $item =========="
    # shellcheck disable=SC2086
    python3 examples/volgrids/main.py $item
done
