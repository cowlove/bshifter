#!/usr/bin/python3 -u 
import sys
import re
import fileinput
import io 



def expandSeq(s): 
    openCount = 0
    closeCount = 0
    lastComma = 0
    ops = []
    for idx,char in enumerate(s):
        if char == '{':
            openCount += 1
        if char == '}':
            closeCount += 1
        if char == ',' and openCount == closeCount:
            ops += [s[lastComma:idx],]
            lastComma = idx + 1
    if lastComma > 0:
        ops += [s[lastComma:],]
    return ops


            
def process(accum, s):
    openCount = 0;
    closeCount = 0;

    firstOpen = 0;
    matchedClose = 0;
    for idx,char in enumerate(s):
        if char == '{':
            openCount += 1
            if openCount == 1:
                firstOpen = idx
        if char == '}':
            closeCount += 1
            if closeCount == openCount:
                matchedClose = idx
                break


    if (openCount):
        pre = s[:firstOpen]
        mid = s[firstOpen+1:matchedClose]
        post = s[matchedClose + 1:]
        for o in expandSeq(mid):
            process(accum + pre, o + post)
    else:
        print(accum + s)
   
   
 

txt = ""
for line in fileinput.input():

    txt += " " + line.strip()

process("", txt)
