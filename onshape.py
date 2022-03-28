#!/usr/bin/python3 -u
import AutoWebDriver 
import time
import os

partStudio = "female test chip"
startPage = "https://cad.onshape.com/signin"


w = AutoWebDriver.AutoWebDriver()

if not w.exists('//element-name[@data-original-title="' + partStudio + '"]'):
    # Can't see partStudio tab, try logging in and reselecting first document  
    w.get(startPage)
    print ("Waiting for document to load")
    w.waitPageLoaded()
    print ("Document loaded")
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
w.keys('//input[@id="export-filename-input"]', "N001 " + partStudio)
w.click('//button[text()="OK"]')
            

        
