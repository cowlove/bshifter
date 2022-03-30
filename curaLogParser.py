#!/usr/bin/python3 -u
import re
import subprocess
from datetime import datetime
from os.path import expanduser
from os import chmod 

outDir = expanduser("~/tmp")

process = subprocess.Popen(['cura', ''], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
cmd = ""
while True:
    line = process.stderr.readline()
    line = line.decode('utf-8')
    if line == '' and process.poll() is not None:
        break
    if re.search("_backendLog", line):
        #print(line)
        if re.search(' -s date="', line):
            cmd = ""
        m = re.match('[^"]*\](.*)', line)
        if m:
            cmd += m.group(1)
        if re.search(' -l "0" ', line):
            cmd = cmd.replace(' -l "0" ', ' -l "$1" ')
            fname = outDir + datetime.now().strftime("/curaSlice-%Y%m%d-%H%M%S.sh")
            f = open(fname, "w")
            print('#!/bin/bash', file=f)
            print('CuraEngine slice -o "$1.gcode" ', end='', file=f)
            print(cmd, file=f)
            f.close()
            chmod(fname, 0o755)
            print("Wrote curaSlice script '" + fname + "'")
