import os
import json
import time
from datetime import datetime
# from pyvirtualdisplay.display import Display
from re import search
import socket
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask, request
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime
from fake_useragent import UserAgent
import flask_app

# REMAINED
# serial_num = "5CG0321N1N"
# model_num = "1C8P4UT"

# EXPIRED
# serial_n = "8CG938632C"
# model_num = "7XV55UA"


def warranty(serial_num, model_num, make):
    # make = "HP"
    os.system('cls')
    ua = UserAgent()
    user_agent = ua.random
    # PROXY = "20.121.184.238:443"
    PROXY = "20.121.184.238:443"
    now_time = datetime.now()   # type: ignore
    date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
    client_ip = request.remote_addr
    PATH = r"chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1080,900")
    # options.add_argument("--disable-gpu")
    options.add_argument(f'user-agent={ua}')
    options.add_argument(f"--proxy-server={PROXY}")

    print(user_agent)
    print(ua)
    driver = webdriver.Chrome(PATH, options=options)
    try:
        # driver.get('https://support.hp.com/gb-en/unknownwarranty')
        driver.get('https://support.hp.com/de-de/checkwarranty')
        time.sleep(1)
        # COOKIE REJECT
        # driver.find_element(By.XPATH, "//*[@id='onetrust-reject-all-handler']").click()
        time.sleep(1)
        input_sn = driver.find_element(By.XPATH, "//*[@id='wFormSerialNumber']")
        input_mn = driver.find_element(By.XPATH, "//*[@id='wFormProductNum']")
        input_sn.send_keys(serial_num)
        input_mn.send_keys(model_num)
        driver.find_element(By.CSS_SELECTOR, '#onetrust-reject-all-handler').click()
        driver.find_element(By.XPATH, '//*[@id="btnWFormSubmit"]').click()
        # input_mn.send_keys(Keys.RETURN)
        # NECCESARY INFOS
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor > div.recaptcha-checkbox-border').click()
        except:
            pass
        # a = driver.title
        # driver.close()
        # return a
        wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='w-details']/div[1]/div[1]/h2/span")))
        try:
            service_status = driver.find_element(By.XPATH, "//*[@id='w-details']/div[1]/div[1]/h2/span").text
        except:
            service_status = 'not found'
        # return service_status
        start_date = driver.find_element(By.XPATH, "//*[@id='warrantyResultBase']/div/div[1]/div[1]/div[4]/div[2]").text
        end_date = driver.find_element(By.XPATH, "//*[@id='warrantyResultBase']/div/div[1]/div[1]/div[5]/div[2]").text
        # EXTRA INFOS
        warranty_type = driver.find_element(By.XPATH, "//*[@id='warrantyResultBase']/div/div[1]/div[1]/div[2]/div[2]").text
        warranty_type = warranty_type.replace("Wty: ", "")
        driver.find_element(By.XPATH, "//*[@id='dismiss-notifications']").click()

        if "Expired" in service_status:
            warranty_status = False
        else:
            warranty_status = True
        time.sleep(2)
        try:
            sc = driver.find_element(By.XPATH, "//*[@id='warrantyResultBase']/div/div[1]")
            image_file_name = file_name + '.png'
            sc.screenshot('screenshots/' + image_file_name)
        except:
            image_file_name = None

        crawl_status = "T"
        json_file = {
            'status': warranty_status, 'crawl_status': crawl_status, 'support_service_status:': service_status, 'purchase': start_date, 'expire': end_date, 'extra_info': {'service_type': warranty_type}
        }
        # with open('jsons/' + file_name + '.json', 'w', encoding='utf-8') as f:
            # json.dump(json_file, f, ensure_ascii=False, indent=4)

        warranty_status_db = ""
        if warranty_status == True:
            warranty_status_db = "T"
        elif warranty_status == False:
            warranty_status_db = "F"


        # app.insert_log_warranty( make, serial_num, warranty_status_db, str(json_file), crawl_status, image_file_name, date_time, client_ip)
        result = { 'status': 'success', 'result': json_file
        }
        return result


    except Exception as e:
        crawl_status = "F"
        # app.insert_log_warranty( make, serial_num, None, str(e), crawl_status, None, date_time, client_ip)
        result = { 'status': 'success', 'result': str(e)
        }
        return result

    finally:
        driver.close()