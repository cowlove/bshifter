#!/bin/bash -x

# Rough script to download latest file from onshape.com, slice it and print it 
octoprint-cli -v temp bed 60
octoprint-cli -v temp extruder 200

./onshape.py
# TODO onshape.py should return this filename 
FILE="`ls -1tr ~/Downloads/*.stl | tail -1`"

# TODO: curaslice.sh is manually made something like this:
# (echo '#!/bin/bash'; echo -n 'CuraEngine slice -o "$1.gcode" '; cat ~/tmp/cura.log2  | sed -e 's/[^"]*\]//' | sed -e 's/-l "0"/-l "$1"/' ) > curaslice.sh
# Write a script that constantly slurps the cura debugging output and makes scripts.  By default use
# the last one here 

FILEC="$FILE".centered.stl
stl_binary "$FILE" "$FILE".bin
stl_center "$FILE".bin "$FILEC"
#stl_ascii "$FILEC.bin" "$FILEC"
./curaslice.sh "$FILEC"  

octoprint-cli files upload "$FILEC.gcode"
octoprint-cli print select "`basename \"$FILEC.gcode"`"
octoprint-cli print start
#octoprint-cli continuous 


