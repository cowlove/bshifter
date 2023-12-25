from sys import argv
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import AutoWebDriver 

class Eso(AutoWebDriver.AutoWebDriver):
    sleep_granularity = .3
    default_timeout = 2
    sleep_delay = .4
    driver = False

    def __init__(self):
        super().__init__()

    def yesno(self, fc, ans):
        print("Checking yes/no '" + fc + "'")
        if not self.exists('//*[@field-config="' + fc + '"]//button[@class="btn radio-btn selected"]'):
            self.cl('//*[@field-config="' + fc + '"]//span[text()="' + ans + '"]')

    def cl(self, xpath, tmo=default_timeout):
        for n in range(int(tmo/self.sleep_granularity)):
            try: 
                self.click(xpath, tmo)
                return
            except Exception as e:
                print(e) 
                sleep(self.sleep_granularity)


    def old_cl(self, xpath, tmo=default_timeout):
        sleep(self.sleep_delay)    
        print("Clicking on for " + xpath)
        for n in range(int(tmo/self.sleep_granularity)):
            try:
                e = self.driver.find_element("xpath", xpath)
                e.click()
                return
            except Exception as e:
                print("Click on " + xpath)
                print(e)
                sleep(self.sleep_granularity)


    def text(self, xpath, tmo = default_timeout):    
        for n in range(int(tmo/self.sleep_granularity)):
            try: 
                e = self.waitfor(xpath, tmo)
                return e.text
            except Exception as e:
                print(e) 
                sleep(self.sleep_granularity)
        

    def sk(self, xpath, keys, tmo = default_timeout):
        for n in range(int(tmo/self.sleep_granularity)):
            try: 
                e = self.waitInteractable(xpath)
                e.clear()
                self.keys(xpath, keys, tmo)
                return
            except Exception as e:
                print(e) 
                sleep(self.sleep_granularity)


    def old_sk(self, xpath, keys, tmo = default_timeout):
  
        sleep(self.sleep_delay)    
        for n in range(int(tmo/self.sleep_granularity)):
            try:
                e = self.driver.find_element("xpath", xpath)
                e.clear()
                #print(keys)
                e.send_keys(keys)
                return
            except Exception as e:
                print(xpath)
                print(e)
                sleep(self.sleep_granularity)

    def old_exists(self, xpath):
        return len(self.driver.find_elements("xpath", xpath)) > 0 

    def old_waitfor(self, xpath, tmo=default_timeout):
        print("Waiting for " + xpath)
        for n in range(int(tmo/self.sleep_granularity)):
            try:
                e = self.driver.find_element("xpath", xpath)
                return True
            except Exception as e:
                print(e)
                sleep(self.sleep_granularity)
        return False

    # single-select tweaked for EMS page, with horrible translate() hack for case insensitivity
    def ssEms(self, id, text, tmo=default_timeout):
        print("Checking single-select '" + id + "' => '" + text + "'")
        already = True

        # check if single-select box is empty
        if self.exists('//*[@field-config="' + id + '"]//div[@class="display-value"]'):
            t = self.text('//*[@field-config="' + id + '"]//div[@class="display-value"]')
            if t == "":
                print ("Empty display value on single-select")
                already = False

        # check if single-select box is quick-pick, with buttons showing (ie: nothing selected)
        if self.exists('//*[@field-config="' + id + '"]/div/div[@class=""]/div[@class="quick-picks"]/button'):
            print ("Visible pick buttons")
            self.cl('//*[@field-config="' + id + '"]//button', 2)     # click one button to select any value
            already = False

        if already:
            print ("Already filled, skipping")
        else:
            print ("single-select '" + id + "' found blank, setting value to '" + text + "'")
            self.cl('//*[@field-config="' + id + '"]', 2)      # click again to bring up the search pick menu 
            
            self.sk('//input[@ng-model="searchString"]', text, tmo)
            #sleep(1)
            if (self.exists("//eso-single-select-panel")): 
                self.cl('//eso-single-select-panel//li//div//mark[contains(' + 
                    'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),' +
                    'translate("' + text + '", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]', tmo)
                self.cl('//eso-single-select-shelf//button[text()="OK"]', tmo=.5) 
            else: 
                self.cl('//eso-multi-select-panel//li//div//mark[contains(' + 
                    'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),' +
                    'translate("' + text + '", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]', tmo)
                self.cl('//eso-multi-select-shelf//button[text()="OK"]', tmo=.5) 

            


    def ss(self, id, text, tmo=default_timeout):
        xp = '//*[@field-ref="' + id + '"]'
        self.cl(xp, tmo)
        self.sk('//input[@ng-model="searchString"]', text, tmo)
        
        if (self.exists("//eso-single-select-panel")): 
            self.cl('//eso-single-select-panel//li//div//mark[contains(' + 
                'translate(text(), "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789abcdefghijklmnopqrstuvwxyz"),' +
                'translate("' + text + '", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789abcdefghijklmnopqrstuvwxyz"))]', tmo)
            self.cl('//eso-single-select-shelf//button[text()="OK"]', tmo=.5) 
            self.cl('//eso-single-select-shelf//button[text()="Ok"]', tmo=.5) 
        else: 
            self.cl('//eso-multi-select-panel//li//div//mark[contains(' + 
                'translate(text(), "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789abcdefghijklmnopqrstuvwxyz"),' +
                'translate("' + text + '", "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789abcdefghijklmnopqrstuvwxyz"))]', tmo)
            self.cl('//eso-multi-select-shelf//button[text()="Ok"]', tmo=.5) 
            self.cl('//eso-multi-select-shelf//button[text()="OK"]', tmo=.5) 

