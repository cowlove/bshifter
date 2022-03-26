#!/usr/bin/python3
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.firefox.options import Options
opts = Options()

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)

print(profile.default_preferences)
from time import sleep
from sys import argv
import re



def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute
    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    return new_driver


if len(argv) < 3 :
    driver = webdriver.Firefox()
    driver.get("https://cad.onshape.com/signin")
    url = driver.command_executor._url  
    session_id = driver.session_id      
    print("./onshape.py " + url + " " + session_id + "\n")
    if len(argv) == 2:
        while 1:
            sleep(1)
else:
    executor_url = argv[1]
    session_id = argv[2]
    driver = create_driver_session(session_id, executor_url)

wait = WebDriverWait(driver, 10)    

default_timeout = 20
sleep_granularity = .2

def waitforandclick(xpath, tmo=default_timeout):
    print("Waiting for " + xpath)
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.click()
            return e
        except Exception as e:
            print(e)
            sleep(sleep_granularity)
    return False

def waitfor(xpath, tmo=default_timeout):
    print("Waiting for " + xpath)
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            return e
        except Exception as e:
            print(e)
            sleep(sleep_granularity)
    return False

def waitforandkeys(xpath, keys, tmo=default_timeout):
    print("Waiting for " + xpath)
    for n in range(int(tmo/sleep_granularity)):
        try:
            e = driver.find_element_by_xpath(xpath)
            e.send_keys(keys)
            return e
        except Exception as e:
            print(e)
            sleep(sleep_granularity)
    return False


def exists(xpath):
    print("Looking for " + xpath)
    try:
        e = driver.find_element_by_xpath(xpath)
        print("Found it")
        return e
    except Exception as e:
        print(e)
    print("Didn't find it");
    return False




partStudio = "female test chip"

if 1:
    # Log in 
    e = exists('//input[@placeholder="Email"]')
    if e: 
        e.send_keys("jim@vheavy.com")
    e = exists('//input[@placeholder="Password"]')
    if e: 
        e.send_keys("tlatla53OS")
    e = exists('//button[text()="Sign in"]')
    if e:
        e.click()
		
    e = waitfor('//img[@class="navbar-onshape-logo"]')
    if e:
        e.click()
   
    # Open first document in recent documents list, if on documents page 
    waitforandclick('(//span[@class="os-document-display-name"])[1]')
    
    # Wait for the part studio 
    e = waitfor('//element-name[@data-original-title="' + partStudio + '"]')
    e = waitfor('//element-name[@data-original-title="' + partStudio + '"]')
    sleep(2)
    #e.click()
    try:
        ActionChains(driver).move_to_element(e).context_click().perform()
    except:
        e = waitfor('//element-name[@data-original-title="' + partStudio + '"]')
        e.click()
        ActionChains(driver).move_to_element(e).context_click().perform()
   

    e = waitfor('//span[text()="Export…"]')
    e.click()
	
    waitforandkeys('//input[@id="export-filename-input"]', "N001 " + partStudio)
    
    e = waitfor('//button[text()="OK"]')
    e.click()
    
    
    
	
print(profile.default_preferences)

