import pymysql
import pymysql.cursors
import urllib.request
import json
import socket
from re import search
import os
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
import flask_app


# ---------------------------------- ASSETS ---------------------------------- #
# os.system('cls')
# category = 'laptop'
# make = 'dell'
# model = 'precision 3530'
# key_word = make + ' ' + model
# cpu = 'i7-8750'

def word_count(txt):
    word_c = len(txt.split())
    return word_c

# ----------------------------------------------------------------------------- GADGETS NOW ----------------------------------------------------------------------------- #

                                            # ---------------------------------- CRAWLER ---------------------------------- #
def crawl(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id):
    os.system('cls')
    now_time = datetime.now()
    date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
    image_file_name = file_name + '.png'
    date_time_file = str(now_time.strftime('%Y-%m-%d'))
    client_ip = socket.gethostbyname('google.com')
    PATH = r"chromedriver.exe"
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("'--disable-notifications'")

    # options.headless = True
    # options.add_argument("--disable-geolocation")
    if key_word:
        if word_count(key_word) >= 2 and len(key_word) > 4:
            pass
        else:
            result = 'Keyword length is not enoght!'
            crawl_status = 'F'
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
                                 result, crawl_status, None, take_screen_shot, None, date_time, client_ip)
            return result
    else:
        key_word = make + ' ' + model_name
    address = 'https://www.gadgetsnow.com/pwafeeds/gnow/web/list/search/json?path=/search/gadgetKey/&category=laptop&key={}'.format(
        key_word)

                                                                # ---------------- FUNCTION ---------------- #
    try:
        r = requests.get(address).json()

        def select_line(p, line_index):
            return p.splitlines()[line_index]

        # with open('my.json', 'a', encoding='utf-8') as f:
        #     json.dump(r, f, ensure_ascii=False, indent=4)
        cpu = 'i7-8750H'
        length = len(r['jsonFeed']['data']['items'])
        num = 0
        crawl_url = ''
        while num < length:
            items = str(r['jsonFeed']['data']['items'][num]['uName'])
            if search(cpu_name, items):
                crawl_url += str(r['jsonFeed']['data']['items'][num]['url']
                                 ).replace('/laptop', 'https://www.gadgetsnow.com/laptops')
            else:
                pass
            num += 1
        # print(crawl_url)
        p = subprocess.check_output(
            "pwsh -Executionpolicy byPass -Command Get-PortableBattery", shell=True, text=True)
        capacity = select_line(p, 3).replace(
            '\u001b[32;1mDesignCapacity : \u001b[0m', '') + ' mWh'
        time.sleep(1)
        # print(capacity)
        driver = webdriver.Chrome(PATH, options=options)
        driver.get(crawl_url)
        time.sleep(1)
        # wait = WebDriverWait(driver, timeout=15, poll_frequency=1)
        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div.FmaKN.mt24 > div._32DzD > h2")))
        # try:
        #     driver.find_element(By.ID, "no-results-message").text
        #     result = "Didn't find any results for the search" + ' ' + key_word
        #     crawl_status = 'T'
        #     keyword_found = 'F'
        #     flask_app.insert_log(make, model_name, serial_num, key_word, result, crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
        #     return result
        # except Exception:
        #     pass
        try:
            cpu = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div.FmaKN.mt24 > div.ekFqp > div > div:nth-child(3) > div._3NN-- > span._1R0sM").text
        except:
            cpu = 'not found'
        try:
            gpu = driver.find_element(
            By.CSS_SELECTOR, "//*[@id='app']/div[4]/div[2]/div/div/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div[2]/span[2]").text
        except:
            gpu = 'not found'
        try:
            display = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div.FmaKN.mt24 > div.ekFqp > div > div:nth-child(2) > div._3NN-- > span._1R0sM").text
        except:
            display = 'not found'
        try:
            storage = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div:nth-child(3) > div > div:nth-child(3) > div._1KhhP._3KOwP > div > div > table > tbody > tr:nth-child(1) > td").text
        except:
            storage = 'not found'
        try:
            ram_capacity = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div:nth-child(3) > div > div:nth-child(6) > div._1KhhP._3KOwP > div > div > table > tbody > tr:nth-child(1) > td").text
        except:
            ram_capacity = 'not found'
        try:
            ram_type = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div:nth-child(3) > div > div:nth-child(6) > div._1KhhP._3KOwP > div > div > table > tbody > tr:nth-child(2) > td").text
        except:
            ram_type = 'not found'
        try:
            ram_clock = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div:nth-child(3) > div > div:nth-child(6) > div._1KhhP._3KOwP > div > div > table > tbody > tr:nth-child(3) > td").text
        except:
            ram_clock = 'not found'
        try:
            weight = driver.find_element(
            By.CSS_SELECTOR, "#app > div:nth-child(5) > div.clearfix.rel.mb36 > div > div > div._1ZEBk > div._3jRrK > div._3kCJW > div > div:nth-child(3) > div > div:nth-child(2) > div._1KhhP._3KOwP > div > div > table > tbody > tr:nth-child(7) > td").text
        except:
            weight = 'not found'
        time.sleep(1)
        try:
            sc = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-catalog-specs.border-t-2.border-b-border-dashed.      text-lm-darkBlue.border-gray-300.pt-3.pb-10 > div.lm-ports-model.grid.grid-cols-1.gap-0.xl\\:grid-cols-2.xl\\:gap-5")
            if take_screen_shot == 'T':
                sc.screenshot('Screenshot/' + image_file_name)
            elif take_screen_shot == 'F':
                image_file_name = None
        except:
            pass
        time.sleep(1)
        driver.close()
        keyword_found = 'T'
        crawl_status = 'T'
        json_file = {
            'make': make, 'graphic': gpu, 'cpu': cpu, 'display': display, 'storage': storage, 'ram': {'ram_capacity': ram_capacity, 'ram_type': ram_type, 'ram_clock': ram_clock}, 'battery_capacity': capacity, 'weight': weight, 'screen_shot': take_screen_shot}

        with open('Json/' + file_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

        result = { 'status': 'success', 'result': json_file
        }
        flask_app.insert_log(site_id, make, model_name, serial_num, key_word, str(json_file), crawl_status, keyword_found, take_screen_shot, image_file_name, date_time, client_ip)
        return result

    except Exception as result:
        crawl_status = 'F'
        flask_app.insert_log(site_id, make, model_name, serial_num, key_word, str(result), crawl_status, None, take_screen_shot, None, date_time, client_ip)
        return result


# ----------------------------------------------------------------------------- GADGETS NOW ----------------------------------------------------------------------------- #

                                                            # ---------------- WEBSERVICE ---------------- #

def webservice(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id):
    # os.system('cls')
    now_time = datetime.now()
    date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
    date_time_file = str(now_time.strftime('%Y-%m-%d'))
    client_ip = socket.gethostbyname('google.com')
    take_screen_shot = 'N'
    crawl_status = 'N'
    if key_word:
        if word_count(key_word) >= 2 and len(key_word) > 4:
            pass
        else:
            result = { 'status': 'error', 'result': {'error_reason': 'keyword is too short', 'keyword': key_word, 'make': make, 'model': model_name, 'serial_number': serial_num}
            }
            crawl_status = 'F'
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
                                 str(result), crawl_status, None, take_screen_shot, None, date_time, client_ip)
            return result
    else:
        key_word = make + ' ' + model_name
    address = 'https://www.gadgetsnow.com/pwafeeds/gnow/web/list/search/json?path=/search/gadgetKey/&category=laptop&key={}'.format(
        key_word)
    try:
        def select_line(p, line_index):
            return p.splitlines()[line_index]
        cpu_name = cpu_name[0:4]
        # print(cpu_name)
        # -------------- BATTERY -------------- #
        pwsh_battery = subprocess.check_output(
            "pwsh -Executionpolicy byPass -Command Get-PortableBattery", shell=True, text=True)
        battery_capacity = select_line(pwsh_battery, 3).replace('\u001b[32;1mDesignCapacity : \u001b[0m', '') + ' mWh'
        # ------------------------------------- #
        r = requests.get(address).json()
        length = len(r['jsonFeed']['data']['items'])
        # print(length)
        if length:
            keyword_found = 'T'
        else:
            keyword_found = 'F'
            result = { 'status': 'error', 'result': {'error_reason': 'keyword not found', 'keyword': key_word, 'make': make, 'model': model_name, 'serial_number': serial_num}
            }
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
                                 str(result), crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
            return result
        num = 0
        uName = []
        # print(cpu_name)
        # r = str(r)
        # r['jsonFeed']['data'] = r['jsonFeed']['data'].replace('"item"', '"items"')
        # print(r)
        while num < length:
            items = str(r['jsonFeed']['data']['items'][num]['uName'])
            # print(items)
            if search(cpu_name, items):
                uName.append(items)
            else:
                pass
            num += 1
        # print(uName)
        # for i in uName
        
        if len(uName) == 0:
            result = { 'status': 'error', 'result': {'error_reason': 'exact cpu not matched', 'keyword': key_word, 'cpu': cpu_name, 'make': make, 'model': model_name, 'serial_number': serial_num}
            }
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
                                 str(result), crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
            return result

        try:
            s = requests.get('https://www.gadgetsnow.com/pwafeeds/gnow/web/show/gadgets/json?uName={}&category=laptop'.format(uName[0])).json()
            extra = s['jsonFeed']['data']['item']['specs']
            # print(extra)
        except Exception as result:
            # print(result)
            return str(result)
        try:
            extra.pop('general')
        except:
            pass
        # extra = str(extra)
        # print(type(extra))
        try:
            weight = extra['general_information']['weight']
        except:
            weight = 'not found'
        try:
            try:
                storage = extra['storage']['hdd_capacity']
            except:
                storage = extra['storage']['ssd_capacity']
        except:
            storage = 'not found'
        # print(storage)
        try:
            display_size = extra['display_details']['display_size']
        except:
            display_size = ''
        try:
            display_resolutions = extra['display_details']['display_resolution']
        except:
            display_resolutions = ''
        display = display_size + ' ' + display_resolutions
        try:
            cpu = extra['performance']['processor']
        except:
            cpu = 'not found'
        try:
            gpu = extra['performance']['graphic_processor']
        except:
            gpu = 'not found'
        try:
            ram_capacity = extra['memory']['capacity']
        except:
            ram_capacity = ''
        try:
            ram_type = extra['memory']['ram_type']
        except:
            ram_type = ''
        ram = ram_capacity + ' ' + ram_type

        # print('extract done')
        json_file = {
            'make': make, 'graphic': gpu, 'cpu': cpu, 'display': display, 'storage': storage, 'ram': ram, 'battery_capacity': battery_capacity, 'weight': weight, 'screen_shot': take_screen_shot, 'extra': extra
            }
        with open('Json/' + file_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
        # print('hi')
        result = { 'status': 'success', 'result': json_file
        }
        flask_app.insert_log(site_id, make, model_name, serial_num, key_word, str(result), crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
        return result

    except Exception as result:
        flask_app.insert_log(site_id, make, model_name, serial_num, key_word, str(result), None, None, take_screen_shot, None, date_time, client_ip)
        return result