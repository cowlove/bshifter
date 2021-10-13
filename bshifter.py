#!/usr/bin/python3
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from sys import argv
import re

#This example requires Selenium WebDriver 3.13 or newer


def playVideo(tag, tag2):
    print ("Playing video: " + tag)
    if len(driver.find_elements(By.ID, tag)) > 0:
        e = driver.find_element_by_id(tag)
        oh = e.get_attribute("outerHTML");
        #print(oh)
        if not re.match('.*display: none', oh):
            try:
                #sleep(2)
                #ActionChains(driver).move_to_element(e).click().perform()
                sleep(2)
                driver.find_element_by_id(tag2).click()  
                sleep(2)
                e.click()
                sleep(2)  
            except Exception as ex:
                print(ex)
            try:
                while 1:
                    oh = e.get_attribute("outerHTML");
                    #print(oh)
                    if not re.match('.*display: inline', oh):
                        break
                    sleep(1)
            except Exception as ex:
                print(ex)
    sleep(2)
    print("Video done")



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
    driver.get("https://bshifter.com/Loginpage.aspx")
    url = driver.command_executor._url  
    session_id = driver.session_id      
    print(url + " " + session_id + "\n")
    if len(argv) == 2:
        while 1:
            sleep(1)
else:
    executor_url = argv[1]
    session_id = argv[2]
    driver = create_driver_session(session_id, executor_url)

wait = WebDriverWait(driver, 10)    


while 1:
    try: 
        ps = str(driver.page_source)
        print(ps)
        print("\n\n")
        playVideo("radiobtnIncomplete", "radioBtn")
        playVideo("chiefbtnIncomplete", "chiefBtn")
    except Exception as ex:
        print(ex)

    try:
        #print (ps)
        pick3 = False
        for sa in range(15):
            s = '.*"studentAnswer' + str(sa) + '"[^}]+"isCorrect":true'
            m = re.compile(s, re.MULTILINE)
            #print(s)
            if m.search(ps):
                print ("Found correct studentAnswer " + str(sa))
                driver.find_element(By.ID, "studentAnswer" + str(sa)).click()
                pick3 = True
        if pick3:
            driver.find_element(By.ID, "submitRadioBtn").click()
            print("Found a submit button")
    except:
        print ("exception in pick3")

    #        
    try:
        driver.find_element_by_class_name("fv-answerOptionImage").click()
        sleep(1)
        driver.find_element_by_class_name("fv-answerOptionImage").click()
        print("Found multiple choice")
    except:
        0

    for sa in range(30):
        try:
            Select(driver.find_element_by_id("studentAnswer" + str(sa))).select_by_index(1)
        except:
            0

    try:
        if len(driver.find_elements(By.ID, "rdobuttonSize1")) > 0:
            for x in ("rdobuttonSize1", "rdobuttonHeight1", "rdobuttonSize1", "rdobuttonHeight1", "rdobuttonccupancy1", "rdobuttonSmoke1", 
                "chkboxLocationFloor1",
                "chkboxLocationSide1", "chkboxTasks1", "rdobuttonPlanLocationSide1", "rdobuttonPlanLocationFloor1", "chkboxObjectives2",
                "rdobuttonStrategy1", "rdobuttonResource1", "chkboxAssume"):
                try:
                    print(x)
                    e = driver.find_element_by_id(x);
                    if not e.is_selected():
                        driver.find_element_by_id(x).click()
                except Exception as ex:
                    print(ex)
            rb = driver.find_element(By.ID, "submitRadioBtn")
            if (rb.get_attribute("class") != "disabled checked"):
                rb.click() 
    except Exception as ex:
        print(ex)



    try:
        rb = driver.find_element(By.ID, "submitRadioBtn")
        if (rb.get_attribute("class") != "disabled checked"):
            print("Found large scenario quiz")
            rb.click() 
    except:
        0    

    # Check for next button 
    for x in range(20):
        try:
            if len(driver.find_elements(By.ID, "nextLinkNavItem")) > 0:
                nxt = driver.find_element(By.ID, "nextLinkNavItem")
                oh = nxt.get_attribute("outerHTML")
                if not re.match('.*class="disabled"', oh):
                    print("Found <NEXT> button, page complete.")
                    sleep(5)
                    nxt.click()
                    break
        except Exception as ex:
            print(ex)
        sleep(1)

    sleep(5)

