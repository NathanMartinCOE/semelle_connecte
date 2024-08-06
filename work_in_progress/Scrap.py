import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import os
import shutil
import zipfile

def ReplaceSpecialCar(string, fill= "_"):
    string = string.replace("\\", fill)
    string = string.replace("/", fill)
    string = string.replace(":",fill)
    string = string.replace("*",fill)
    string = string.replace("?",fill)
    string = string.replace('"',fill)
    string = string.replace("<",fill)
    string = string.replace(">",fill)
    string = string.replace("|",fill)
    return string

url = "https://mobility.feetme.fr/dashboard/patients"

LocalDataBasePath = 'C:\\Users\\Nathan\\Desktop\\FeetMe_scrap'
LocalDownloadPath = 'C:\\Users\\Nathan\\Downloads'

driver = webdriver.Chrome()
driver.get(url)
updated_html = driver.page_source

# ====================================== Connection ==========================================
while True:
    try:
        button = driver.find_element(By.XPATH, '//*[@id="firebaseui-auth-container"]/div/div[1]/form/ul/li[2]/button')
        button.click()
        break
    except:
        pass

while True:
    try:
        field = driver.find_element(By.XPATH, '//*[@id="firebaseui-auth-container"]/div/form/div[2]/div/div[1]/input')
        field.send_keys("fabien.leboeuf@chu-nantes.fr")
        break
    except:
        pass

while True:
    try:
        button = driver.find_element(By.XPATH, '//*[@id="firebaseui-auth-container"]/div/form/div[3]/div/button[2]')
        button.click()
        break
    except:
        pass

while True:
    try:
        field = driver.find_element(By.XPATH, '//*[@id="firebaseui-auth-container"]/div/form/div[2]/div[3]/input')
        field.send_keys("feetme123") 
        break
    except:
        pass

while True:
    try:
        button = driver.find_element(By.XPATH, '//*[@id="firebaseui-auth-container"]/div/form/div[3]/div[2]/button')
        button.click()
        break
    except:
        pass


# =============================== Get patient name ==============================================

time.sleep(10)


tab_it = []
names = []
dobs = []

i = 1
while True:
    try:
        name = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[2]/table/tbody/tr[{i}]/td[1]')
        dob = driver.find_element(By.XPATH,f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[2]/table/tbody/tr[{i}]/td[2]')
        tab_it.append(i)
        names.append(ReplaceSpecialCar(name.text))
        dobs.append(dob.text)
        i += 1
    except:
        break

# =========================== Look for patient ===============================

for i, name, dob in zip(tab_it, names, dobs):

    path_ipp = os.path.join(LocalDataBasePath, str(name))
    try:
        os.mkdir(path_ipp)
    except:
        print(f"Patient {name} already exist")

    while True:
        try:
            Patient_button = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[2]/table/tbody/tr[{i}]/td[1]')
            Patient_button.click()
            break
        except:
            pass

    # ================================== Look for tests ========================

    time.sleep(10)


    tests = []
    iteration = []
    i = 1
    while True:
        try:
            TestName = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[2]/table/tbody/tr[{i}]/td[2]')
            Type = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[2]/table/tbody/tr[{i}]/td[3]')
            Date = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[2]/table/tbody/tr[{i}]/td[4]')
            Time = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[2]/table/tbody/tr[{i}]/td[5]')
            
            test = f"{TestName.text}_{Type.text}_{Date.text}_{Time.text}"
            tests.append(ReplaceSpecialCar(string= test, fill="-"))
            iteration.append(i)
            i += 1
        except:
            break

    
    # ============================= Download csv ==================
    for test, i in zip(tests, iteration):
        path_test = os.path.join(path_ipp, test)
        try:
            os.mkdir(path_test)

            while True:
                try:
                    TestName_Button = driver.find_element(By.XPATH, f'//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[2]/table/tbody/tr[{i}]/td[2]')
                    TestName = TestName_Button.text
                    TestName_Button.click()
                    break
                except:
                    pass
            
            
            while True:
                try:
                    Visualize_Button = driver.find_element(By.XPATH, '//*[@id="feetme-dial-app"]/div/div/main/div[3]/div[3]/div/div[1]/div/div[2]/div/div/a')
                    Visualize_Button.click()
                    break
                except:
                    pass
            
            if TestName != "Posturography" and TestName != "Imported record": # Because Posturography don't have metrics

                while True:
                    try:
                        StridesDataButton = driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/button')
                        StridesDataButton.click()
                        break
                    except:
                        pass

                while True:
                    try:
                        PressuresDataButton = driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[2]/div/button')
                        PressuresDataButton.click()
                        break
                    except:
                        pass
                
                while True:
                    try:
                        DownloadMetricsName = driver.find_element(By.XPATH, '//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/a')
                        StridesDataPath = os.path.join(LocalDownloadPath, DownloadMetricsName.get_attribute("download"))
                        shutil.move(StridesDataPath, path_test)
                        break
                    except:
                        pass

                while True:
                    try:
                        DownloadMetricsName = driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[2]/div/a')
                        PressuresDataPath = os.path.join(LocalDownloadPath, DownloadMetricsName.get_attribute("download"))
                        with zipfile.ZipFile(PressuresDataPath, 'r') as fichier_zip:
                            fichier_zip.extractall(path_test)
                        os.remove(PressuresDataPath)
                        break
                    except:
                        pass

            elif TestName == "Posturography": # Because Posturography don't have metrics

                while True:
                    try:
                        PressuresDataButton = driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/button')
                        PressuresDataButton.click()
                        break
                    except:
                        pass
                
                while True:
                    try:
                        DownloadMetricsName = driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/main/div[2]/div/div[2]/div/div[2]/div/div[1]/div/a')
                        PressuresDataPath = os.path.join(LocalDownloadPath, DownloadMetricsName.get_attribute("download"))
                        with zipfile.ZipFile(PressuresDataPath, 'r') as fichier_zip:
                            fichier_zip.extractall(path_test)
                        os.remove(PressuresDataPath)
                        break
                    except:
                        pass
                
            driver.back()

        except:
             print(f"Test {test} already exist")

    while True:
        try:
            retrun_patient_button =  driver.find_element(By.XPATH,'//*[@id="feetme-dial-app"]/div/div/div/nav/div[2]/div/div/div/ul/div/a[1]')
            retrun_patient_button.click()
            break
        except:
            pass
