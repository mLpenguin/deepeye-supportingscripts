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

import os, time, random, re, configparser

config = configparser.ConfigParser()
config.read(r'C:\Users\rcexam01\Desktop\OptoDownload\config.ini')

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

##chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920x1080")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_experimental_option("detach", True)
#chrome_options.binary_location = "chrome/ChromiumPortable/ChromiumPortable.exe"
openPatient = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def openById(id):
    
    
    #ActionChains(browser).move_to_element(browser.find_element_by_id(id)).context_click().perform()
    #ActionChains(browser).context_click(browser.find_element_by_id("gvStudyList_tccell0_6")).perform()
    ActionChains(browser).move_to_element(browser.find_element_by_id(id)).perform()
    time.sleep(0.5)
    ActionChains(browser).context_click().perform()
    """
    for x in range (0,5):
        ActionChains(browser).send_keys(Keys.ARROW_DOWN).perform()
        #time.sleep(0.2)
    ActionChains(browser).send_keys(Keys.RETURN).perform()
    
    """
    while(True):
        try:
            ActionChains(browser).move_to_element(browser.find_element_by_xpath("//a[text()='Copy Link']")).click().perform()
            break
        except:
            pass
    
    browser.find_element_by_id('copyLinkValue').send_keys(Keys.CONTROL + 'c')


    ActionChains(browser).move_to_element(browser.find_element_by_class_name("nilman-modal-dialog-title-close")).click().perform()
    

    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    #time.sleep(1)
    # read the clipboard
    
    while(True):
        try:
            imageUrl = root.clipboard_get()
            break
        except:
            pass

    #javaScript = "window.open(\"" + str(imageUrl) + "\",\"_blank\");"
    #print(javaScript)
    #browser.execute_script(javaScript)
    #browser.find_element_by_id('tagBody').send_keys(Keys.CONTROL + 't') 
    openPatient.get(imageUrl)

    #browser.find_element_by_id(id).context_click()

def saveImageToFile(patientId, side, PerformedOn, PatientName):
    #determmine number of images
    ##browser.refresh()
    #time.sleep(5)
    imageMax = 0

    try:
        imageMax = int(openPatient.find_element_by_id("imageSliderBar0").get_attribute('aria-valuemax'))
    except Exception:
        pass

    imageMax += 1
    ##print ("ValueMax: " + str(imageMax))
    

    for x in range(0,imageMax):
        imageFileName = patientId + "_" + patientName + "_" + side + " " + str(x+1) + "_" + PerformedOn


        #Save Button
        element = openPatient.find_element_by_id("saveMenuBtn")
        ActionChains(openPatient).move_to_element(element).click().perform()
        #browser.find_element_by_id('saveMenuBtn_imgSpan').click()
        openPatient.find_element_by_id('saveViewportImageButton_imgSpan').click()
        openPatient.find_element_by_id('saveImagePreviewTypeViewport').click()

        fileName = openPatient.find_element_by_id('txtSaveImagePreviewPanelFileName')
        fileName.clear()
        fileName.send_keys(imageFileName)
        openPatient.find_element_by_id('btnSaveImagePreviewPanelDownload').click()
        print("Saving File: " + imageFileName)
        time.sleep(1)
        #browser.find_element_by_id('btnSaveImagePreviewPanelClose').click()
        
        

        if (x < (imageMax -1)):
            ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("imagePagingNext0")).click().perform()

def clickSaveImagePrepare():
    time.sleep(0.2)
    ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("screenLayoutBtn")).click().perform()
    ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("Screen1x1Button_imgSpan")).click().perform()


def saveImages(PatientID, PerformedOn, PatientName):
    
    element = WebDriverWait(openPatient, BrowserTimeoutSeconds).until(EC.presence_of_element_located((By.ID, "protocolsParent")))
    
    #time.sleep(2)

    #Try till webpage is loaded
    while(True):
        try:
            clickSaveImagePrepare()
            break
        except:
            pass
    
    
    #SelectOD
    #ActionChains(browser).move_to_element(browser.find_element_by_id("optFilterODToggleButton_imgSpan")).click().perform()
    
    #delay to ensure that the webpage is fully loaded
    time.sleep(1)
    saveImageToFile(PatientID, "OD", PerformedOn, PatientName)


 
    

    #SelectOS
    ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("optFilterOSToggleButton_imgSpan")).click().perform()
    #Change Viewport
    ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("screenLayoutBtn")).click().perform()
    ActionChains(openPatient).move_to_element(openPatient.find_element_by_id("Screen1x1Button_imgSpan")).click().perform()
    
    #time.sleep(1)
    saveImageToFile(PatientID, "OS", PerformedOn, PatientName)

def listExistingFiles():
    print("Determining existing files")

    tempFileList = []

    for file in os.listdir(download_dir):
        filename = os.fsdecode(file)
        
        #x = filename.split("_")
        
        tempFileList.append(filename)

    fileList.extend(list(set(tempFileList)))
    print("DONE determining existing files list is: " + str(len(fileList)) + " elements long")
    #print(fileList)

def checkIfExist(patientID):
    exists = False

    for x in fileList:
        if patientID == x:
            exists = True
            break
    
    return exists

def login():
    print ("Logging In")
    #browser = webdriver.Chrome()

    browser.maximize_window()
    openPatient.maximize_window()
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
    if (skipCounter >= SkipTimeout):
        print ("Found " + str(SkipTimeout) + " skips in a row. Ending")
        break
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


print("*****DONE******")