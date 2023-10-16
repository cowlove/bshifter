#!/usr/bin/python3 -u
import AutoWebDriver 
from selenium.webdriver.common.by import By
import time
import subprocess
from os import listdir
from os.path import isfile, join, expanduser
import re


w = AutoWebDriver.AutoWebDriver()
w.get('https://preply.com/en/login')


w.waitPageLoaded()
time.sleep(2)
e = w.exists('//input[@id="email"]')
if e: 
    w.keys('//input[@id="email"]', "jim3vans@gmail.com")
    w.keys('//input[@id="password"]', "fSr4AT9xVrGYNrh")
    #w.click('//button[@data-qa-id="finish-login-btn"]')
    w.click('//span[text()="Log in"]')
    w.waitPageLoaded()

w.get('https://preply.com/edu/spanish/learn/vocab')

time.sleep(2)
while w.exists('//div[text()="Show more"]'):
    w.click('//div[text()="Show more"]')
    w.waitPageLoaded()
    time.sleep(1)

