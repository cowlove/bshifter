#!/bin/bash -x
# For now needs an absolute path to the kicad project, openscad wants to open all files relative to the .scad file's dir
PROJ="$1"

kicad-cli pcb export dxf -l F.Paste "${PROJ}" -o "/tmp" #-F_Paste.dxf"
kicad-cli pcb export dxf -l Edge.Cuts "${PROJ}" -o "/tmp" #-Edge_Cuts.dxf"

openscad "$(dirname $0)/scadPasteMask.scad" -D proj=\"/tmp/$(basename "$1" .kicad_pcb)\" --export-format binstl -o "${HOME}/Downloads/$(basename ${PROJ} .kicad_pcb).stl"
"$(dirname $0)/printStl.sh" 

