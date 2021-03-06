#example from https://selenium-python.readthedocs.io/getting-started.html

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
import numpy as np
import pandas as pd
import csv
import sys


class SolarServerTest:
    
    def __init__(self):
        #need to avoid cache for accurate tests in some instances
        self.profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        self.profile.set_preference("browser.cache.disk.enable", False)
        self.profile.set_preference("browser.cache.memory.enable", False)
        self.profile.set_preference("browser.cache.offline.enable", False)
        self.profile.set_preference("network.http.use-cache", False) 
        self.driver = webdriver.Firefox(self.profile)
        
    def test_click(self, url):

        self.driver.get(url)

        assert "dropdown" in self.driver.title
        
        menu = self.driver.find_element_by_class_name("dropbtn")
        hidden_submenu = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
       
        actions.perform()

        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.close()
        #self.driver.quit()

def pingpongImage(path='data'):
    print("pingpong start")
    
    SERVER_IP = ""
    if (len(sys.argv) > 1):
        SERVER_IP = str(sys.argv[1])
        print(SERVER_IP)
    else:
        print("Error: no ip address given.")
        sys.exit()

    fileName = path+'/selenium-'+str(datetime.date.today())+'-'+str(int(time.time()))+'.csv' 
    print (fileName)
    print("")

    dataDF = pd.DataFrame(columns=['task','time'])

    """
    if (len(sys.argv) > 1):
        testTime = float(sys.argv[1])
    else: 
        testTime = 5 #default 5 seconds
    """
    testTime = 5

    bookendSleepTime = 60
    middleSleepTime = 30

    #bookendSleepTime = 5
    #middleSleepTime = 5

    #60 seconds idle
    time.sleep(bookendSleepTime)

    #open
    times = 4

    # run the whole thing i times to account for start up weirdness
    for i in list(range(times)):

        time.sleep(middleSleepTime)

        #Phase 1
        print ("Starting large test!")

        dataDF = dataDF.append({'task' : 'start v1 ' + str(i) , 'time': time.time()},ignore_index=True)
        SolarServer = SolarServerTest()

        tmCurrentTime = time.time()
        tmStartTime = time.time()
            
        while (tmCurrentTime - testTime < tmStartTime):
            # this could maybe be simplified in the future...
            dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
            SolarServer.test_click("http://" + SERVER_IP + "/dropdown/dropdown_dynamic_limageA.html")
            tmCurrentTime = time.time()
            dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
            SolarServer.test_click("http://" + SERVER_IP + "/dropdown/dropdown_dynamic_limageB.html")
            tmCurrentTime = time.time()

        SolarServer.tearDown()
        dataDF = dataDF.append({'task' : 'stop v1 ' + str(i) , 'time': time.time()},ignore_index=True)

        #chill out between tests
        time.sleep(middleSleepTime)

        # Phase 2

        print ("Starting small test!")

        dataDF = dataDF.append({'task' : 'start v2 '+ str(i), 'time': time.time()},ignore_index=True)
        SolarServer = SolarServerTest()

        tmCurrentTime = time.time()
        tmStartTime = time.time()
            
        while (tmCurrentTime - testTime < tmStartTime):
            dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
            SolarServer.test_click("http://" + SERVER_IP + "/dropdown/dropdown_dynamic_simageA.html")
            tmCurrentTime = time.time()
            dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
            SolarServer.test_click("http://" + SERVER_IP + "/dropdown/dropdown_dynamic_simageB.html")
            tmCurrentTime = time.time()

        SolarServer.tearDown()
        dataDF = dataDF.append({'task' : 'stop v2 '+ str(i) , 'time': time.time()},ignore_index=True)

    #save data to file
    # check if the file already exists
    try:
        with open(fileName) as csvfile:
            print("This file already exists!")
    except:
        dataDF.to_csv(fileName, sep=',',index=False)

    #print(dataDF)
    print("pingpong done")
    

if __name__ == "__main__":
    pingpongImage()