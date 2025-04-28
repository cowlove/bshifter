#!/bin/bash -x
# For now needs an absolute path to the kicad project, openscad wants to open all files relative to the .scad file's dir
PROJ="$1"

kicad-cli pcb export dxf -l F.Paste "${PROJ}.kicad_pcb" -o "${PROJ}-F_Paste.dxf"
kicad-cli pcb export dxf -l Edge.Cuts "${PROJ}.kicad_pcb" -o "${PROJ}-Edge_Cuts.dxf"

openscad "$(dirname $0)/pasteMask.scad" -D proj=\"${PROJ}\" --export-format binstl -o "${HOME}/Downloads/$(basename ${PROJ}.stl)"
"$(dirname $0)/printStl.sh" 

