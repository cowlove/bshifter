#!/usr/bin/python3
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from multiprocessing import Process
import time
import os

from selenium.webdriver.firefox.options import Options
opts = Options()

#profile = webdriver.FirefoxProfile()
#profile.set_preference("browser.download.folderList", 2)

from time import sleep
#print(profile.default_preferences)
from sys import argv
import os.path
import re

class EverLastingProcess(Process):
    def join(self, *args, **kwargs):
        pass

    def __del__(self):
        pass

def checkdriver(driver, timeout):
    try:
        myElem = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((By.ID, 'IdOfMyElement')))
    except TimeoutException:
        return True
    except Exception as e:
        return False
    return True

def daemon(idFile):
    # Server daemon side of the fork()
    opt = webdriver.FirefoxOptions()
    opt.set_preference("geo.enabled", False)
    opt.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/sla")
    driver = webdriver.Firefox(options=opt)
    url = driver.command_executor._url  
    session_id = driver.session_id     
    print(url + " " + session_id, file = open(idFile, 'w'))
    while True:
        sleep(1)
        if (checkdriver(driver, 2) == False):
            exit()

class AutoWebDriver:
    driver = False
    idFile = "/tmp/selenium." + os.path.basename(argv[0])
    startedServer = False
    default_timeout = 30

    def get(self, url):
        self.driver.get(url)

    def waitPageLoaded(self):
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete') 


    def __init__(self):
        self.opendriver()
        self.driver.set_window_size("600", "400")

    def create_driver_session(self, session_id, executor_url):
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

    def opendriver(self):         
        self.driver = False
        try:
            line = open(self.idFile, "r").read()
            words = line.split()
            executor_url = words[0]
            session_id = words[1]
            print ("Trying to connect to remote server " + self.idFile + " " + line)
            self.driver = self.create_driver_session(session_id, executor_url)
        except:
            self.driver = False
        
        if checkdriver(self.driver, 1) == False:
            p = EverLastingProcess(target=daemon, args=(self.idFile,), daemon=False)
            p.start()
      
        while checkdriver(self.driver, 1) == False:
            sleep(1)
            try:
                line = open(self.idFile, "r").read()
                words = line.split()
                executor_url = words[0]
                session_id = words[1]
                print ("Trying to connect to remote server " + self.idFile + " " + line)
                self.driver = self.create_driver_session(session_id, executor_url)
            except:
                self.driver = False

        print ("Connected to remote server " + self.idFile + " " + line)




    def waitInteractable(self, xpath, tmo=default_timeout):
        for n in range(1, 3):
            try:
                e = WebDriverWait(self.driver, tmo).until(
                    expected_conditions.presence_of_element_located((By.XPATH, xpath)))
                e = WebDriverWait(self.driver, tmo).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
                e = self.driver.find_element(By.XPATH, xpath)
                return e
            except Exception as e:
                print(e)
        return False


    def keys(self, xpath, keys, tmo=default_timeout):
        print("Keys " + xpath)
        e = self.waitfor(xpath, tmo)
        e = self.waitInteractable(xpath, tmo)
        e.send_keys(keys)

    def click(self, xpath, tmo=default_timeout):
        print("Clicking " + xpath)
        e = self.waitfor(xpath, tmo)
        e = self.waitInteractable(xpath, tmo)
        if e:
            e.click()

    def rclick(self, xpath, tmo=default_timeout):
        print("RClicking " + xpath)
        e = self.waitInteractable(xpath, tmo)
        ActionChains(self.driver).move_to_element(e).context_click().perform()

    def waitfor(self, xpath, tmo=default_timeout):
        print("Waiting for " + xpath)
        try:
            e = WebDriverWait(self.driver, tmo).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath)))
            e = self.driver.find_element(By.XPATH, xpath)
            return e
        except Exception as e:
            print(e)
        return False

    def exists(self, xpath):
        print("Exists? " + xpath)
        try:
            e = self.driver.find_element(By.XPATH, xpath)
            print("Found it")
            return e
        except Exception as e:
            print(e)
        print("Didn't find it");
        return False

    def finish(self):
        if self.startedServer == True:
            print("Continuing to host selenium server, ^C to exit...")

