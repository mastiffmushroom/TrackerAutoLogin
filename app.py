from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime
import requests
import numpy as np
from custom_logger import logging

def set_chrome_options() -> None:

    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    ## Hide images from the browser
    #chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options

def CheckConnection(url, timeout=10) -> bool:
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
        
def GetElementWait(driver, box, box_type):
    
    wait = WebDriverWait(driver, 10)
    if box_type.lower() == "id":
        return wait.until(EC.element_to_be_clickable((By.ID, box)))
    elif box_type.lower() in "class":
        return wait.until(EC.element_to_be_clickable((By.CLASS_NAME, box)))
    elif box_type.lower() == "css":
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, box)))
    elif box_type.lower() == "text":
        return wait.until(EC.element_to_be_clickable((By.LINK_TEXT, box)))  
    elif box_type.lower() == "tag":
        return wait.until(EC.element_to_be_clickable((By.TAG_NAME, box)))
    elif box_type.lower() == "name":
        return wait.until(EC.element_to_be_clickable((By.NAME, box)))        
    else:
        return wait.until(EC.element_to_be_clickable((By.XPATH, box)))
        
def GetElement(driver, box, box_type):
    if box_type.lower() == "id":
        return driver.find_element(By.ID, box)
    elif box_type.lower() in "class":
        return driver.find_element(By.CLASS_NAME, box)
    elif box_type.lower() == "css":
        return driver.find_element(By.CSS_SELECTOR, box)
    elif box_type.lower() == "text":
        return driver.find_element(By.LINK_TEXT, box)                
    elif box_type.lower() == "tag":
        return driver.find_element(By.TAG_NAME, box)
    elif box_type.lower() == "name":
        return driver.find_element(By.NAME, box)        
    else:
        return driver.find_element(By.XPATH, box)

        
def TrackerLogin(tracker, user_keys, tracker_keys):

        try:
            url = tracker_keys["url"]
            login_url = tracker_keys["login_url"]
            if url == login_url:
                login_title = tracker_keys["login_title"].lower()
            user = user_keys["user_login"]
            passwd = user_keys["pass_login"]
            
            driver = webdriver.Chrome(options=set_chrome_options())
            driver.get(url)
            
            wait = WebDriverWait(driver, 10)
            login_b = GetElementWait(driver, tracker_keys["login_box"],\
                                     tracker_keys["login_box_type"])
            
            pass_b = GetElementWait(driver, tracker_keys["password_box"],\
                                     tracker_keys["password_box_type"])
                                     
            submit_b = GetElementWait(driver, tracker_keys["submit_box"],\
                                     tracker_keys["submit_box_type"])
            
            login_b = GetElement(driver, tracker_keys["login_box"],\
                                 tracker_keys["login_box_type"])
                                 
            pass_b = GetElement(driver, tracker_keys["password_box"],\
                                tracker_keys["password_box_type"])
                                
            submit_b = GetElement(driver, tracker_keys["submit_box"],\
                                  tracker_keys["submit_box_type"])
            
            login_b.send_keys(user)
            pass_b.send_keys(passwd)
            submit_b.click()
            
            time.sleep(10)

            if url != login_url:
                fail_url = "LOGIN URL WAS \'" + driver.current_url + "\' instead of \'" + login_url + "'"
                assert(driver.current_url == login_url),fail_url
            else:
                fail_title = "LOGIN TITLE WAS \'" + driver.title.lower() + "\' instead of \'" + login_title + "'"
                assert(driver.title.lower() == login_title),fail_title
            
            driver.close()
            return True
        except TimeoutError:
            curr_time = str(datetime.datetime.now())
            failed = curr_time + " : Timeout error when trying to login to " + tracker + " will try again next loop"
            logging.error(failed)
            driver.close()
            return False
        except Exception as e:
            curr_time = str(datetime.datetime.now())
            failed = curr_time + " : Failed to login to " + tracker + " due to Error: " + str(e)
            logging.error(failed)
            driver.close()
            return False            




if __name__ == "__main__":

    with open("tracker_config.json", 'r') as f:
        tracker_config = json.load(f)

    with open("user_config.json", 'r') as f:
        user_config = json.load(f)
        
    hours_sleep = user_config["Hours_Rerun"]
    connection_url = user_config["CheckConnectionURL"]
    fail_connection = 0
    
    assert(hours_sleep > 20),"Hours_Rerun must be at least 20 hours in user_config.json"
    
    del user_config["Hours_Rerun"]
    del user_config["CheckConnectionURL"]
    del user_config["LogLevel"]
    
    while True:
        
        is_connected = CheckConnection(connection_url)
        loop_sleep = np.round(np.random.uniform(0.5, 1.0) * hours_sleep)
        curr_time = str(datetime.datetime.now())
        
        if is_connected == True:
            logging.debug(curr_time + " : " + "Successful connection to internet via " + connection_url)
            for t in user_config.keys():
                curr_time = str(datetime.datetime.now())
                print(curr_time, "Attempting " + t)
                logging.debug(curr_time + " : Attempting to login to " + t)
                tracker = tracker_config[t]
                successful = TrackerLogin(t, user_config[t], tracker)
                curr_time = str(datetime.datetime.now())
                if successful == True:
                    logging.debug(curr_time + " : Successful login to " + t)
                else:
                    logging.warning(curr_time + " : Failed to login to " + t)
                
        else:
            fail_connection += 1
            if fail_connection >= 3:
                logging.error(curr_time + " : Unable to connect to the internet for more than " + str(fail_connection) + " hours, skipping trackers and retrying in ~1 hour")
            else:
                logging.warning(curr_time + " : " + "Failed connection to internet via " + connection_url + ", skipping trackers and retrying in ~1 hour")
            loop_sleep = 1

        curr_time = str(datetime.datetime.now())    
        
        logging.debug(curr_time + " : Sleeping for " + str(loop_sleep) + " hours")
        time.sleep(loop_sleep * 60 * 60)
