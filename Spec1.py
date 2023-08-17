import json
import os
import socket
import time
from datetime import datetime
from re import search

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
import flask_app

# make = 'Lenovo'
# model_name = 'ThinkPad X1 Carbon'
# serial_num = 'C703673'
# cpu_name = 'i5-4300U'
# ram = '16GB'
# ---------------------------------- WORD COUNT CHECKER ---------------------------------- #
def word_count(txt):
    word_c = len(txt.split())
    return word_c

# ---------------------------------- FUNCTIONS ---------------------------------- #
# ---------------------- CRAWL ---------------------- #
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
    # options.headless = True
    # options.add_argument("--disable-geolocation")

    if key_word:
        if word_count(key_word) >= 2 and len(key_word) > 4:
            pass
        else:
            result = 'Keyword length is not enoght!'
            crawl_status = 'F'
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word, result, crawl_status, None, take_screen_shot, None, date_time, client_ip)
            return result
    else:
        key_word = make + ' ' + model_name + ' ' + cpu_name

    try:
        p = subprocess.check_output("pwsh -Executionpolicy byPass -Command Get-PortableBattery", shell=True, text=True)
        def select_line(p, line_index):
            return p.splitlines()[line_index]
        capacity = select_line(p,3).replace('\u001b[32;1mDesignCapacity : \u001b[0m', '') + ' mWh'
        time.sleep(1)
        driver = webdriver.Chrome(PATH, options=options)
        driver.get('https://laptopmedia.com/specs/')
        time.sleep(1)
        wait = WebDriverWait(driver, timeout=15, poll_frequency=1)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='search-input']/div/input")))
        search_bar = driver.find_element(
            By.XPATH, "//*[@id='search-input']/div/input")
        search_bar.send_keys(key_word)
        time.sleep(5)
        try:
            driver.find_element(By.ID, "no-results-message").text
            result = "Didn't find any results for the search" + ' ' + key_word
            crawl_status = 'T'
            keyword_found = 'F'
            flask_app.insert_log(site_id, make, model_name, serial_num, key_word, result, crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
            return result
        except Exception:
            pass
        div_num = 1
        gpu_options = ''
        while div_num > 0:
            try:
                gpu_options_xpath = "//*[@id='gpu']/div/div/div[2]/div/div[{}]/div/label/span[1]".format(div_num)
                gpu_options += str(div_num) + '. ' + driver.find_element(By.XPATH, gpu_options_xpath).text + ' & '
                div_num += 1
                # print(gpu_options)
            except Exception as e:
                div_num = 0
                gpu_options = gpu_options.removesuffix(' & ')
            continue
            # return gpu_options
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id='results_container']/div/div[1]/article/a[1]").click()
        time.sleep(2)
        cpu = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-model-laptop.grid.grid-cols-1.xl\\:grid-cols-2.items-start.gap-4 > div.lm-laptop-specs > ul.lm-specs-table.text-lm-darkBlue.w-full.border-t.border-lm-borderBlue > li.cpu-specs.relative.mb-0\\.5.h-12.pl-15.flex.items-center.gap-1.border-b.border-lm-borderBlue").text
        display = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-model-laptop.grid.grid-cols-1.xl\\:grid-cols-2.items-start.gap-4 > div.lm-laptop-specs > ul.lm-specs-table.text-lm-darkBlue.w-full.border-t.border-lm-borderBlue > li.display-specs.relative.mb-0\\.5.h-12.pl-15.flex.items-center.gap-1.border-b.border-lm-borderBlue").text
        storage = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-model-laptop.grid.grid-cols-1.xl\\:grid-cols-2.items-start.gap-4 > div.lm-laptop-specs > ul.lm-specs-table.text-lm-darkBlue.w-full.border-t.border-lm-borderBlue > li.storage-specs.relative.mb-0\\.5.h-12.pl-15.flex.items-center.gap-1.border-b.border-lm-borderBlue").text
        ram = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-model-laptop.grid.grid-cols-1.xl\\:grid-cols-2.items-start.gap-4 > div.lm-laptop-specs > ul.lm-specs-table.text-lm-darkBlue.w-full.border-t.border-lm-borderBlue > li.ram-specs.relative.mb-0\\.5.h-12.pl-15.flex.items-center.gap-1.border-b.border-lm-borderBlue").text
        weight = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-model-laptop.grid.grid-cols-1.xl\\:grid-cols-2.items-start.gap-4 > div.lm-laptop-specs > ul.lm-specs-table.text-lm-darkBlue.w-full.border-t.border-lm-borderBlue > li.weight-specs.relative.mb-0\\.5.h-12.pl-15.flex.items-center.gap-1.border-b.border-lm-borderBlue").text
        # dimensions = driver.find_element(By.XPATH, "/html/body/section/section/div[1]/div[5]/div[8]/ul/li[2]").text
        time.sleep(1)
        sc = driver.find_element(By.CSS_SELECTOR, "body > section > section > div.flex.flex-col.space-y-10 > div.lm-catalog-specs.border-t-2.border-b-2.border-dashed.text-lm-darkBlue.border-gray-300.pt-3.pb-10 > div.lm-ports-model.grid.grid-cols-1.gap-0.xl\\:grid-cols-2.xl\\:gap-5")
        # print(weight)
        if take_screen_shot == 'T':
            sc.screenshot('Screenshot/' + image_file_name)
        elif take_screen_shot == 'F':
            image_file_name = None
        time.sleep(1)
        driver.close()
        crawl_status = 'T'
        return '####'
        json_file = {
            'make': make, 'graphic': gpu_options, 'cpu': cpu, 'display': display, 'storage': storage, 'ram': ram, 'battery_capacity': capacity, 'weight': weight, 'screen_shot': take_screen_shot
            }
        with open('Json/' + file_name + '.json', 'w', encoding='utf-8') as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)
        keyword_found = 'T'
        result = str(json_file)
        flask_app.insert_log(make, model_name, serial_num, key_word, result, crawl_status, site_id, keyword_found, take_screen_shot, image_file_name, date_time, client_ip)
        return json_file
        

    except Exception as result:
        result = str(result)
        crawl_status = 'F'
        flask_app.insert_log(make, model_name, serial_num, key_word, result, crawl_status, site_id, None, take_screen_shot, None, date_time, client_ip)
        return result
