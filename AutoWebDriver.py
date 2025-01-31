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
#opts = Options()

from time import sleep
#print(profile.default_preferences)
from sys import argv
import os.path
import re
import traceback



class EverLastingProcess(Process):
    def join(self, *args, **kwargs):
        pass

    def __del__(self):
        pass

def checkdriver(driver, timeout):
    try:
        myElem = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((By.ID, 'IdOfMyElement')))
        driver.find_element(By.XPATH, "//")
    except TimeoutException:
        return True
    except Exception as e:
        return False
    return True

def daemon(idFile):
    opt = webdriver.FirefoxOptions()
    opt.set_preference("geo.enabled", False)
    opt.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/sla")
    try:
        driver = webdriver.Firefox( options=opt)  
    except:
        serv = webdriver.FirefoxService( executable_path='/snap/bin/geckodriver' )
        driver = webdriver.Firefox( options=opt, service=serv)  

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.alwaysOpenPanel", False)

    print("Daemon: started firefox")
    url = driver.command_executor._url  
    session_id = driver.session_id     
    print(url + " " + session_id, file = open(idFile, 'w'))
    while True:
        sleep(1)
        if (checkdriver(driver, 2) == False):
            exit()
    print("Daemon: exiting")

class AutoWebDriver:
    driver = False
    idFile = "/tmp/selenium." + os.path.basename(argv[0])
    startedServer = False
    default_timeout = 30


    def disableDownloadDialog():
        get("about:config")
        click('//button[@id="warningButton"]')
        click('//button[@id="show-all"]')
        keys('//input[@id="about-config-search"]', "alwaysOpenPanel")
        click('//button[@id="about-config-pref-toggle-button"]')
        waitPageLoaded()
        attempts = [300,] + list(range(200,450))
			
        for n in attempts:
            e = driver.find_element(By.XPATH, '/html/body/table/tr[%d]/th/span' % n)
            if (e.is_displayed()):
                e = driver.find_element(By.XPATH, '/html/body/table/tr[%d]/td[1]/span/span' % n)
                if e.text == "true":
                    if waitInteractable('/html/body/table/tr[%d]/td[2]/button' % n, 1) != False:
                        click('/html/body/table/tr[%d]/td[2]/button' % n)
                break

    def get(self, url):
        self.driver.get(url)

    def waitPageLoaded(self):
        WebDriverWait(self.driver, self.default_timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete') 

    def __init__(self):
        self.opendriver()
        self.driver.set_window_size("1200", "1000")

    def create_driver_session(self, session_id, executor_url):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': { 'sessionId' : session_id }, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute
        opt = webdriver.FirefoxOptions()
        try:
            new_driver = webdriver.Remote(command_executor=executor_url, options=opt)
            new_driver.session_id = session_id
        except Exception as e:
            print(traceback.format_exc())
            new_driver = None
        finally:
            RemoteWebDriver.execute = org_command_execute

        # Replace the patched function with original function
        return new_driver

    def opendriverNO(self):
        opt = webdriver.FirefoxOptions()
        serv = webdriver.FirefoxService( executable_path='/snap/bin/geckodriver' )
        opt.set_preference("geo.enabled", False)
        opt.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/sla")
        driver = webdriver.Firefox( options=opt, service=serv )  
        #rofile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.alwaysOpenPanel", False)
        self.driver = driver

    def opendriver(self):         
        self.driver = False
        try:
            line = open(self.idFile, "r").read()
            words = line.split()
            executor_url = words[0]
            session_id = words[1]
            print ("Initial attempt to connect to remote server " + self.idFile + " " + line)
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
            except Exception as e:
                print(e)
                self.driver = False
        print ("Connected to remote server " + self.idFile + " " + line)



    def waitInteractable(self, xpath, tmo=default_timeout):
        print("waitInteractable() " + xpath)
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

    def clear(self, xpath, tmo=default_timeout):
        print("Clear " + xpath)
        e = self.waitfor(xpath, tmo)
        e = self.waitInteractable(xpath, tmo)
        e.clear()

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

