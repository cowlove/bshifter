#!/usr/bin/python3 -u
import AutoWebDriver 
from selenium.webdriver.common.by import By
import time
import subprocess
from os import listdir
from os.path import isfile, join, expanduser
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

w = AutoWebDriver.AutoWebDriver()
if (w.exists('//a[@class="alert-link os-message-bubble-link"]')):
    w.click('//a[@class="alert-link os-message-bubble-link"]', 2)



if not w.exists('//tab-list-item[@class="os-tab-bar-tab active"]'):
    w.get("about:config")
    w.click('//button[@id="warningButton"]')
    w.click('//button[@id="show-all"]')
    w.keys('//input[@id="about-config-search"]', "alwaysOpenPanel")
    #w.click('//button[@id="about-config-pref-toggle-button"]')
    w.click('/html/body/table/tr[303]/td[2]/button')

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

w.waitPageLoaded()
e = w.waitInteractable('(//span[contains(@class, "os-tab-name")])[1]')
partStudio = e.text
ver = 1
for f in listdir(expanduser("~/Downloads/")):
    m = re.match("N(\d+) " + partStudio + ".stl", f)
    if (m):
        ver = max(ver, int(m.group(1)) + 1)
fname = expanduser("~/Downloads/N%04d %s.stl" % (ver, partStudio))
print("Downloading Part Studio '" +  partStudio + "' as file '" + fname + "'")


profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.alwaysOpenPanel", False)
opts = Options()
opts.set_preference("browser.download.alwaysOpenPanel", False)

time.sleep(2)
w.click('//element-name[@data-bs-original-title="' + partStudio + '"]')
w.click('//element-name[@data-bs-original-title="' + partStudio + '"]')
w.click('//element-name[@data-bs-original-title="' + partStudio + '"]')
w.rclick('//element-name[@data-bs-original-title="' + partStudio + '"]')
w.click('//span[text()="Export…"]')	
w.click('//input[@id="export-filename-input"]')	
w.clear('//input[@id="export-filename-input"]')	
w.keys('//input[@id="export-filename-input"]', "N%04d %s"  % (ver, partStudio))
w.click('//button[text()="Export"]')

# Wait for download to complete.  Use stl_bbox to check for complete file             
# stl_bbox from git clone https://github.com/AllwineDesigns/stl_cmd.git
while True:
    print ("Checking on download file '" + fname + "'...")
    time.sleep(2)
    completedProc = subprocess.run(('stl_bbox', fname))
    if completedProc.returncode == 0:
        print("File complete, success")
        break

w.click('//element-name[@data-bs-original-title="' + partStudio + '"]')
        
