import pymysql
import pymysql.cursors
import urllib.request
import json
import socket
from re import search
import os
import requests
# from fp.fp import FreeProxy
import time
from datetime import datetime
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import subprocess
from fake_useragent import UserAgent
make = 'dell'
model_name = 'Inspiron 15 5370'
cpu_name = 'i5-8250U'
key_word = None
take_screen_shot = 'F'

def crawl(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id):
    # os.system('cls')
    ua = UserAgent()
    user_agent = ua.random
    now_time = datetime.now()
    date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
    image_file_name = file_name + '.png'
    date_time_file = str(now_time.strftime('%Y-%m-%d'))
    # client_ip = request.remote_addr
    PATH = r"chromedriver.exe"
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-notifications")
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    options.add_argument(f'user-agent={user_agent}')

    # options.headless = True
    # options.add_argument("--disable-geolocation")
    def word_count(txt):
        word_c = len(txt.split())
        return word_c
    if key_word:
        if word_count(key_word) >= 2 and len(key_word) > 4:
            pass
        else:
            result = 'Keyword length is not enoght!'
            crawl_status = 'F'
            # app.insert_log_spec(site_id, make, model_name, serial_num, key_word,
            #                     result, crawl_status, None, take_screen_shot, None, date_time, client_ip)
            return result
    else:
        key_word = make + ' ' + model_name
    address = 'https://www.gadgetsnow.com/pwafeeds/gnow/web/list/search/json?path=/search/gadgetKey/&category=laptop&key={}'.format(
        key_word)

    try:
        r = requests.get(address).json()

        def select_line(p, line_index):
            return p.splitlines()[line_index]

        # with open('my.json', 'a', encoding='utf-8') as f:
        #     json.dump(r, f, ensure_ascii=False, indent=4)
        # cpu = 'i7-8750H'
        length = len(r['jsonFeed']['data']['items'])
        num = 0
        crawl_url = ''
        while num < length:
            items = str(r['jsonFeed']['data']['items'][num]['uName'])
            cpu_name = cpu_name[:4]
            # return cpu_name
            if search(cpu_name, items):
                crawl_url += str(r['jsonFeed']['data']['items'][num]['url']
                                 ).replace('/laptop', 'https://www.gadgetsnow.com/laptops')
                # return crawl_url
            else:
                result = {'status': 'error', 'result': 'no match found'
                          }
                return result
            num += 1
        capacity = ''
        time.sleep(1)
        # print(capacity)
        driver = webdriver.Chrome(PATH, options=options)
        driver.get(crawl_url)
    except Exception as e:
        return str(e)
crawl(make, model_name, None, cpu_name, key_word, take_screen_shot, None, None)