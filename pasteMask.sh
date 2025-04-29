#!/bin/bash -x
# For now needs an absolute path to the kicad project, openscad wants to open all files relative to the .scad file's dir
PROJ="$1"
TMP=/tmp/$(basename "${PROJ}")

kicad-cli pcb export dxf -l F.Paste "${PROJ}" -o "${TMP}-F_Paste.dxf"
kicad-cli pcb export dxf -l Edge.Cuts "${PROJ}" -o "${TMP}-Edge_Cuts.dxf"

openscad "$(dirname $0)/scadPasteMask.scad" -D proj=\"${TMP}\" --export-format binstl -o "${HOME}/Downloads/$(basename ${PROJ}.stl)"
"$(dirname $0)/printStl.sh" 

