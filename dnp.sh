#!/bin/bash -x
# Rough script to download latest file from onshape.com, slice it and print it 
ADHESION=none
ADHESION=brim
export LD_LIBRARY_PATH=~/opt/cura-5.2.1

octoprint-cli connection connect
octoprint-cli connection connect
octoprint-cli connection connect
octoprint-cli -v temp bed 50 
octoprint-cli -v temp extruder 200

./onshape.py
# TODO onshape.py should return this filename 
FILE="`ls -1tr ~/Downloads/*.stl | tail -1`"
FILEC="$FILE".centered.stl

stl_binary "$FILE" "$FILE".bin
stl_center "$FILE".bin "$FILEC"

sed 's/adhesion_type="brim"/adhesion_type="'${ADHESION}'"/g' curaslice.sh > go.sh
chmod 755 go.sh

./go.sh "$FILEC"  

octoprint-cli files upload "$FILEC.gcode"
octoprint-cli print select "`basename \"$FILEC.gcode"`"
octoprint-cli print start
#octoprint-cli continuous 


