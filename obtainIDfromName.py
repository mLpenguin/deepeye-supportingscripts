from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import tkinter as tk

import os, time, random, re, configparser, csv

config = configparser.ConfigParser()
config.read(r'C:\Users\ntak\Desktop\USB\config.ini')

URL = str(config['main']['website'])

#has to be 20
moveDownRowEvery = 20

u = str(config['main']['user'])
p = str(config['main']['pass'])
BrowserTimeoutSeconds = 60
SkipTimeout = int(config['main']['SkipTimeout'])




def WaitUntilIDLoads(id):
    element = WebDriverWait(browser, BrowserTimeoutSeconds).until(EC.presence_of_element_located((By.ID, id)))

def WaitUntilNameLoads(n):
    element = WebDriverWait(browser, BrowserTimeoutSeconds).until(EC.presence_of_element_located((By.NAME, n)))


download_dir = str(config['main']['download_dir'])
fileList = []

#Overview
chrome_options = webdriver.ChromeOptions() 
prefs = {"download.default_directory": download_dir}

#chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_experimental_option("detach", True)
#chrome_options.binary_location = "chrome/ChromiumPortable/ChromiumPortable.exe"

browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)



def login():
    print ("Logging In")
    #browser = webdriver.Chrome()

    #browser.maximize_window()
    #browser.maximize_window()
    browser.get(URL)
    

    #Login
    WaitUntilIDLoads('txtUsername')
    username= browser.find_element_by_id('txtUsername')
    username.send_keys(u)

    password = browser.find_element_by_id('txtPassword')
    password.send_keys(p)

    #click login
    browser.find_element_by_id('btnLogin').click()

def getPatientIdFromRow(rowNum):
    #6 is id
    #5 is name
    
    return "gvStudyList_tccell"+str(rowNum)+"_6"

def getPatientNameFromRow(rowNum):
    #6 is id
    #5 is name

    return "gvStudyList_tccell"+str(rowNum)+"_5"

def getPerformedOnFromRow(rowNum):
    return "gvStudyList_tccell"+str(rowNum)+"_9"

namesArray = []
def readPatientNames():
    with open(r'C:\Users\ntak\Desktop\USB\DataSets\Dataset3\Macular Names Temp.txt') as my_file:
        for line in my_file:
            x = line.rstrip('\n')
            y = x.split(",")
            z = y[0] + " " + y[1]




            
            namesArray.append(z)



def scrambleNames(name):
    temp = []
    x = name.split(" ")
    numOfName = len(x)

    if numOfName == 2:
        temp.append(x[0] + " " + x[1])
        temp.append(x[1] + " " + x[0])
    elif numOfName == 3:
        temp.append(x[0] + " " + x[1]+" "+ x[2])
        temp.append(x[0] + " " + x[2]+" "+ x[1])

        temp.append(x[1] + " " + x[2]+" "+ x[0])
        temp.append(x[1] + " " + x[0]+" "+ x[2])

        temp.append(x[0] + " " + x[1])
        temp.append(x[0] + " " + x[2])
        temp.append(x[1] + " " + x[0])
        temp.append(x[1] + " " + x[2])
        temp.append(x[2] + " " + x[1])
        temp.append(x[2] + " " + x[0])

    else:
        temp.append(x[0] + x[numOfName-1])
        temp.append(x[numOfName-1] + x[0])

    return temp
        


login()
readPatientNames()
#print(namesArray)

#ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("gvStudyList_DXFREditorcol5_I")).click().perform()

for x in range(0,len(namesArray)):
    id_name = []
    print("ID: " + namesArray[x] + " :ID")
    splitNames = scrambleNames(str(namesArray[x]))
    for i in range(0, len(splitNames)):
        print("Trying: " +splitNames[i])
        time.sleep(2)
        browser.find_element_by_id('gvStudyList_DXFREditorcol5_I').clear()
        time.sleep(5)
        browser.find_element_by_id('gvStudyList_DXFREditorcol5_I').send_keys(str(splitNames[i]))
        time.sleep(2)
        browser.find_element_by_id('gvStudyList_DXFREditorcol5_I').send_keys(Keys.RETURN)
        time.sleep(1)
        
        for j in range(15):
            time.sleep(1)
            try:
                #print(bool(browser.find_element_by_id("gvStudyList_tccell0_9")))
                if (browser.find_element_by_id("gvStudyList_DXEmptyRow").text == "No data to display"):
                    #time.sleep(1)
                    break
            except:
                pass

            try:
                if (bool(browser.find_element_by_id("gvStudyList_tccell0_9"))):
                    time.sleep(1)
                    break
            except:
                pass


        rownum = 0
        while(True):
            try:
                id_name.append(browser.find_element_by_id(getPatientIdFromRow(rownum)).text)
                rownum += 1
            except:
                break

    

    beeop = list(set(id_name)) 
    
    #print(beeop)

    f = open(r"C:\Users\ntak\Desktop\USB\DataSets\Dataset3\Macular ID.txt", "a")
    f.write(str(beeop))
    f.write("\n")
    f.close()
    print("Saving: " + str(beeop))
    print("-------------------------------")





















"""


listExistingFiles()

login()

#time.sleep(2)

skipCounter = 0

row = 2099


#400-700

#850

skipped = False

#while (row <= 12):
while (True):
"""

"""
    if (skipCounter >= SkipTimeout):
        print ("Found " + str(SkipTimeout) + " skips in a row. Ending")
        break
"""

"""
    if (not skipped):
        for x in range(0, row//moveDownRowEvery):
            moveToRow = moveDownRowEvery * (x +1)
            print("Moving to row: " + str(moveToRow))
            while(True):
                try:
                    time.sleep(0.4)
                    element = browser.find_element_by_id(getPatientIdFromRow(moveToRow))
                    ActionChains(browser).move_to_element(element).perform()
                    break
                except:
                    pass
        
    time.sleep(1)
    
    #browser.refresh()

    #Move to desired element
    while(True):
        try:
            ActionChains(browser).move_to_element(browser.find_element_by_id(getPatientIdFromRow(row))).perform()
            break
        except:
            pass
    

    try:
        
        patientID = browser.find_element_by_id(getPatientIdFromRow(row)).text
        patientName = browser.find_element_by_id(getPatientNameFromRow(row)).text
        #time.sleep(0.1)
        performedOn = browser.find_element_by_id(getPerformedOnFromRow(row)).text
        
    except:
        print("Can't find next element (All done?): Exiting")
        break
    

    performedOn = re.sub('\:|\,' ,'', performedOn)

    #print (performedOn)


    print(row)
    

    imageFileName = patientID + "_" + patientName + "_" + "OD 1" + "_" + performedOn + ".jpg"

    #print (imageFileName)

    #If false then save. Otherwise skip
    if ((not checkIfExist(imageFileName)) and patientID != ""):
        skipCounter = 0
        skipped = True
        print ("Saving images from: " + "\"" + patientID + "\"")
        openById(getPatientIdFromRow(row))
        saveImages(patientID, performedOn, patientName)

        #Close Tab
        #browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 
        #browser.execute_script("window.history.go(-1)")
               

    else:
        print("Already Exists Skipping: " + "\"" + patientID + "\"")
        skipCounter += 1
        skipped = True

    row += 1



#Click Logout
ActionChains(browser).move_to_element(browser.find_element_by_id("divLogoffButton_imgSpan")).click().perform()

"""
print("*****DONE******")