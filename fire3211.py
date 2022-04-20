#!/usr/bin/python3
from time import sleep
import re
from tkinter.ttk import Combobox
import eso
from eso import *
from datetime import date
from tkinter import *
from tkinter import simpledialog
from eso import Eso

date=date.today().strftime("%m%d%Y")
eso = Eso()

class MyDialog(simpledialog.Dialog):
    def __init__(self, master):
        self.okPressed = False
        simpledialog.Dialog.__init__(self, master,title="ESO Crusher")

    # returns (stringvar, entry) for the Entry 
    def addCheckbox(self, master, label, default):
        v = IntVar(root, value=default)
        Label(master, text=label).grid(sticky="w", column = 0, row = self.row)
        Checkbutton(master,variable=v, onvalue=1, offvalue=0).grid(sticky="w", column=1,row=self.row)
        self.row += 1
        return v


    def addTextEntry(self, master, prompt, default):
        sv = StringVar(root, value=default)
        Label(master, text=prompt).grid(sticky="w", column = 0, row = self.row)
        e = Entry(master,  textvar=sv)
        e.grid(sticky="w", column = 1, row = self.row)
        self.row += 1
        return (e, sv)


    def setCrib(self): 
        s = self.cb['values'][self.cb.current()].split('/')
        
        self.crib1.delete(0, END)
        self.crib1.insert(0, s[0])
        self.crib1.setvar()

        self.crib2.delete(0, END)
        self.crib2.insert(0, s[1])
        self.crib1.setvar()

        self.crib3.delete(0, END)
        self.crib3.insert(0, s[2])
        self.crib1.setvar()

    def body(self, master):
        #self.labels = Frame(master).pack()
        #self.entries = Frame(master).pack()
        self.row = 0;

        (dummy, self.name) = self.addTextEntry(master, "FF Name", "evans")
        (dummy, self.station) = self.addTextEntry(master, "Station", "54")
        (dummy, self.zip) = self.addTextEntry(master, "Zip", "98168")
        (self.crib1, self.pi) = self.addTextEntry(master, "Primary Impression", "alter")
        (self.crib2, self.ssc) = self.addTextEntry(master, "S&S Category", "cognit")
        (self.crib3, self.ssd) = self.addTextEntry(master, "S&S Detail", "intox")
        (dummy, self.hospital) = self.addTextEntry(master, "Hospital", "vall")
        self.male = self.addCheckbox(master, 'Male', 1)
        self.firstUnit = self.addCheckbox(master, 'First Unit', 1)
        
        
        Label(master).grid(column = 0, row=self.row)    
        self.row += 1

        cb = Combobox(master)
        cb['values'] = ('alt/cog/intox', 'face/inj/face', 'no complaint/no/no', 'shortness/resp/short')
        cb.current(0)
        cb.grid(column=0, row   =self.row) 
        self.cb = cb
        Button(master, text="SET", command=self.setCrib).grid(column = 1, row=self.row)
        self.setCrib()
        self.row += 1


    def apply(self):
        self.okPressed = True


def fireReport():
    global d
    global date
    global driver 
    eso.cl('//shelf-panel//button[text()="OK"]', tmo=1) 
    eso.cl('//label[text()="Basic"]')

    # simple ones
    eso.ss("INCIDENTTYPEID", "3211");
    eso.ss("STATIONID", d.station.get())
    eso.ss("ACTIONTAKEN1", "32")
    eso.ss("AIDGIVENORRECEIVEDID", "n")
    eso.ss("LOCATIONTYPEID", "address")
    eso.ss("PROPERTYUSEID", "000")
    eso.ss("OFFICERINCHARGEAGENCYPERSONID", d.name.get())
    eso.cl('//eso-yes-no[@field-ref="WORKINGFIRE"]//button[@data-val="false"]')
    eso.sk('//eso-text[@field-ref="ALARMS"]//input', "1\n")
    eso.sk('//eso-text[@field-ref="REPORTWRITERASSIGNMENT"]//input', "officer\n")

    if False:
        # complicated ones 
        if eso.exists('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]'):
            eso.cl('//eso-single-select[@field-ref="COVID19FACTORID"]//button[text()="No"]')
        else: 
            eso.cl('//eso-single-select[@field-ref="COVID19FACTORID"]')
            eso.sk('//input[@ng-model="searchString"]', "3\n")

    eso.cl('//eso-address-summary[@field-label="\'Address\'"]')
    eso.sk('//eso-zip-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
        d.zip.get() + "\n"])
    eso.cl('//shelf-panel//button[text()="OK"]')


    eso.cl('//eso-date[@field-ref="OFFICERINCHARGEDATE"]')
    eso.sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
        date + "\n"])
    eso.cl('//div[@class="filterbutton"]//button[text()="OK"]')

    eso.cl('//eso-date[@field-ref="REPORTWRITERDATE"]')
    eso.sk('//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
        date + "\n"])
    eso.cl('//div[@class="filterbutton"]//button[text()="OK"]')

    eso.sk('//eso-text[@field-ref="NARRATIVEREMARKS"]//textarea[@type="text"]', "See EMS report.\n")
    sleep(1)
    eso.cl('//label[text()="Basic"]')

    # Click on unit reports tab, wait for it to load 
    eso.cl('//label[text()="Unit Reports"]')
    eso.cl('//grid-cell[@class="unit-info-cell"]',tmo=20.0)
    eso.cl('//edit-unit-report-toast//button[text()="OK"]')

    for unit in range(1, 5):
        ugrid = '(//grid-cell[@class="unit-info-cell"])[' + str(unit) + ']'
        if eso.exists(ugrid):
            eso.cl(ugrid)
            eso.ss("UNITRESPONDINGFROMID", "in")
            eso.ss("UNITPRIORITYID", "emer")
            eso.ss("UNITACTIONTAKEN1", "32")
            eso.cl('//edit-unit-report-toast//button[text()="OK"]')

    eso.cl('//label[text()="Validation Issues"]')


def emsReport():
    global d
    global date
    global driver
 
    # Click out of any shelf trays that happen to be up 
    eso.cl('//shelf-panel//button[text()="OK"]', tmo=.5) 
    eso.cl('//shelf-panel//button[text()="OK"]', tmo=.5) 

    ###################################################33
    # INCIDENT tab
    eso.cl('//li[@class="incident incident-bg"]')
     

 
    eso.cl('//button[text()="CAD Import"]')
    eso.cl('//button[text()="Update data"]')
    eso.cl('//button[text()="Refresh with new data"]')

    eso.ssEms("incident.response.runTypeId", "911")
    eso.ssEms("incident.response.priorityId", "Emer")
    eso.ssEms("incident.response.stationId", d.station.get())
    eso.ssEms("incident.response.respondingFromZoneID", "In")
    eso.ssEms("incident.response.requestedByItemID", "Patient")

    if (len(d.hospital.get()) > 0): 
        eso.ssEms("incident.response.dispositionItemID", "Pt Care T")
        eso.ssEms("incident.disposition.dispositionItemID", "Patient Treated, Trans")
        eso.ssEms("incident.disposition.transportMethodID", "Ambulance")
        eso.ssEms("incident.disposition.transportDueToItemIDs", "Patient")
        eso.ssEms("incident.disposition.transferredToLocationTypeID", "Ground")
        eso.ssEms("incident.disposition.transferredToLocationID", "Tri")
        eso.ssEms("incident.destination.predefinedAddress.predefinedLocationID", d.hospital.get())
    else:
        eso.cl('//button[text()="Other"]')
        eso.ssEms("incident.response.dispositionItemID", "No Treatment")

    eso.ssEms("incident.scene.manualAddress.locationTypeID", "Home")

    eso.yesno("incident.response.isFirstUnitOnSceneID", "Yes" if d.firstUnit.get() else "No")
    eso.yesno("incident.scene.massCasualty", "No")

	# Pick 98168 zip code 
    x = '//eso-text[@name="incident.scene.manualAddress.zip"]//input'
    if eso.exists(x) and eso.waitfor(x).get_attribute("value") == '':
        if (eso.exists('//button[@class="btn icon-btn search-bg"]')):
            eso.cl('//button[@class="btn icon-btn search-bg"]')
            eso.cl('//td[text()="' + d.zip.get() + '"]')
    

#<button class="btn icon-btn search-bg" ng-class="{ searching: searching, 'search-bg': !isInternational, 'search-gray-bg': isInternational }" ng-click="search($event)" ng-disabled="isInternational"></button>

#/html/body/emr-app/div/emr-app-body/main/incident-tab/emr-main-view/main-viewport/field-set[2]/eso-location/div[2]/eso-address/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/button

    # Set PPE for people 
    for unit in range(1, 5):
        x = '(//incident-crew//grid-row//div[@class="name"])[' + str(unit) + ']'
        if (eso.exists(x)):
            eso.cl(x)
            eso.cl('//eso-multi-select[@field-config="incident.crew.personalProtectiveEquipment"]')
            eso.waitfor('//li//div[text()="Eye Protection"]')
            for ppe in ["Eye Protection", "Gloves", "Mask-N95"]: 
                x = '//li//div[text()="' + ppe + '"]/../..//check-mark[@class="check-white-bg"]';
                if (eso.exists(x)):
                    eso.cl(x)
            eso.cl('//shelf-panel//button[text()="OK"]') 
            eso.cl('//shelf-panel//button[text()="OK"]') 

            # TODO d.name.get() doesn't work, does it have a <CR>?
            # TODO blindly clicks, will deselect if a role is already selected 
            
            x = '(//incident-crew//grid-row//div[@class="name"])[' + str(unit) + '][contains(text(), "' + d.name.get() + '")]'
            #x = '(//incident-crew//grid-row//div[@class="name"])[' + str(unit) + '][contains(text(), "EVA")]'
            if (eso.exists(x)):
                row = 2
            else:
                row = 4
            if not eso.exists('((//incident-crew//grid-row)[' + str(unit) + ']//grid-cell)[' + str(row) + ']//label[@class="radio-btn selected"]'):
                eso.cl('((//incident-crew//grid-row)[' + str(unit) + ']//grid-cell)[' + str(row) + ']')


    # Handle missing "at-patient" time 
    if (eso.exists('//span[text()="At Patient"]/../span[text()="- -"]')):
        e = driver.find_element_by_xpath('(//span[text()="On Scene"]/../span)[2]')
        # Add 3 minutes to "On Scene" time 
        try: 
            t = e.text.split(':')
            t[1] = str(int(t[1]) + 3)
            if int(t[1]) >= 60:
                t[0] = str(int(t[0]) + 1)
            newTime = "".join(t)
            print ("No at patient time, setting to " + newTime)
            eso.cl('//button[text()="Set Times"]')
            eso.sk('//time-entry[@label="At Patient"]//eso-masked-input//input', [Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE, 
                newTime])
            eso.cl('//shelf-panel//button[text()="OK"]') 
        except Exception as e:
            print(e)

    ###################################################33
    # PATIENT tab
    eso.cl('//li[@class="patient patient-bg"]')
    sleep(1)
    #ssEms("patient.demographics.ethnicityId", "Not")
    eso.ssEms("patient.demographics.genderId", ("Male" if d.male.get() else "Female"))

    ###################################################33
    # NARRATIVE tab
    eso.cl('//li[@class="narrative narrative-bg"]')
    sleep(1)
    eso.ssEms("narrative.clinicalImpression.medicalTraumaId", "Trauma")
    eso.ssEms("narrative.clinicalImpression.primaryImpressionId", d.pi.get())

    # Add a sign/sympt if one doens't yet texist 
    ssBut = "((//narrative-signs-symptoms//grid-row)[1]/grid-cell)[1]/button"
    if eso.exists(ssBut):
        eso.cl(ssBut)
        eso.ssEms("narrative.supportingSignsAndSymptoms.signsAndSymptoms.supportPrimaryId", d.ssc.get())
        eso.ssEms("narrative.supportingSignsAndSymptoms.signsAndSymptoms.supportSignId", d.ssd.get())
        eso.cl('//shelf-panel//button[text()="OK"]', tmo=.5) 

    
    ###################################################33
    # SIGNATURES TAB tab
    # Make signature array with output from http://ramkulkarni.com/blog/record-and-playback-drawing-in-html5-canvas-part-ii/ 
    # and this: 
    # tr '}' '\n'  | perl -e 'while(<>){if(/"x":(\d+),"y":(\d+)/ && $count++ % 5 == 0) { $x=$1-$lx;$y=$2-$ly; $lx=$1;$ly=$2; print "[$x,$y],"; }}'
    # 

    eso.cl('//li[@class="signatures signatures-bg"]')
    sleep(1)
    eso.cl('//div[text()="Provider Signatures"]')
    if eso.exists('//div[@class="signing-area signature signed-bg"]'):
        print("ALREADY SIGNED")
    else:
        print("NOT SIGNED")
        eso.ssEms("signatures.standardSignatures.providerSignatures.leadProviderId", d.name.get())
        eso.cl('//eso-signature-pad//canvas')

        canvas = eso.driver.find_element_by_xpath('//div[@class="signing-area-container"]')
        #//eso-signature-pad//canvas')
        drawing = ActionChains(eso.driver)\
            .move_to_element_with_offset(canvas, 120, -482) \
            .click_and_hold()
        for p in (
            [-20,-32],[-8,-51],[4,-53],[19,-8],[16,118],[-20,58],[-31,32],[-8,-2],[77,-95],[19,-16],[5,-3],[-6,16],        
            ):
            drawing = drawing.move_by_offset(p[0], p[1])
        drawing.release()

        drawing.perform()
        eso.cl('//eso-signature-dialog//button[text()="OK"]') 
    eso.cl('//shelf-panel//button[text()="OK"]') 

    ###################################################33
    # VALIDATE button Experiental stuff messing with Validate button
    if 0:  
        eso.cl('//button[@class="validate check-circle-white-bg"]')
        eso.waitfor('//shelf-panel//button[text()="OK"]') 
        sleep(5)
        if eso.exists('//strong[text()="At Patient"]'):
            print ("AT PATIENT")

eso.driver.set_window_size("1200", "800")




#exit()

while True:
    if (not eso.exists('//button[@class="action-button hamburger-bg"]')) and (not eso.exists('//button[@class="more hamburger-bg"]')) and (not eso.exists('//button[@class="icons-hamburger"]')):
        eso.get("https://www.esosuite.net/")
        eso.waitPageLoaded()
        eso.cl('//input[@name="username"]')
        eso.sk('//input[@name="username"]', 'jevans')
        eso.cl('//input[@name="password"]')
        eso.sk('//input[@name="password"]', 'jevans2')
        eso.cl('//input[@name="agency"]')
        eso.sk('//input[@name="agency"]', 'tukwilafd')
        eso.cl('//button[@class="btn login-button"]')
        sleep(1)
        eso.waitPageLoaded()
        eso.get("https://www.esosuite.net/ehr")

    root = Tk()
    root.withdraw()
    d = MyDialog(root)
    if not d.okPressed: 
        exit()

    if eso.exists("//current-patient"):
        emsReport()
    elif eso.exists("//exposure-summary"):
        fireReport()

    #exit()

