#!/usr/bin/python3 -u
import AutoWebDriver 
import time
from os import listdir
from os.path import isfile, join, expanduser
import re
partStudio = "female test chip"

ver = 1
for f in listdir(expanduser("~/Downloads/")):
    m = re.match("N(\d+) " + partStudio + ".stl", f)
    if (m):
        ver = max(ver, int(m.group(1)) + 1)

w = AutoWebDriver.AutoWebDriver()

if not w.exists('//element-name[@data-original-title="' + partStudio + '"]'):
    # Can't see partStudio tab, try logging in and reselecting first document  
    w.get("https://cad.onshape.com/signin")
    w.waitPageLoaded()
    time.sleep(2)
    e = w.exists('//input[@placeholder="Email"]')
    if e: 
        w.keys('//input[@placeholder="Email"]', "jim@vheavy.com")
        w.keys('//input[@placeholder="Password"]', "tlatla53OS")
        w.click('//button[text()="Sign in"]')
    w.click('//img[@class="navbar-onshape-logo"]')
    w.click('(//span[@class="os-document-display-name"])[1]') # First document in list

w.click('//element-name[@data-original-title="' + partStudio + '"]')
w.rclick('//element-name[@data-original-title="' + partStudio + '"]')
w.click('//span[text()="Export…"]')	
w.keys('//input[@id="export-filename-input"]', "N%04d %s"  % (ver, partStudio))
w.click('//button[text()="OK"]')
            

        
