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
# import subprocess
# import flask_app


def select_line(p, line_index):
    return p.splitlines()[line_index]

make = 'dell'
model = 'precision 3530'
cpu_name = 'i7-8750'

key_word = make + ' ' + model
os.system('cls')
now_time = datetime.now()
date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
date_time_file = str(now_time.strftime('%Y-%m-%d'))
client_ip = socket.gethostbyname('google.com')
take_screen_shot = 'N'
crawl_status = 'N'
address = 'https://www.gadgetsnow.com/pwafeeds/gnow/web/list/search/json?path=/search/gadgetKey/&category=laptop&key={}'.format(key_word)
r = requests.get(address).json()
lenght = len(r['jsonFeed']['data']['items'])
if lenght:
    keyword_found = 'T'
else:
    keyword_found = 'F'
num = 0
crawl_url = ''
while num < lenght:
    items = str(r['jsonFeed']['data']['items'][num]['uName'])
    if search(cpu_name, items):
        crawl_url += str(r['jsonFeed']['data']['items'][num]['uName'])
    else:
        pass
    num += 1
# print(crawl_url)
second_url = 'https://www.gadgetsnow.com/pwafeeds/gnow/web/show/gadgets/json?uName={}&category=laptop'.format(crawl_url)
# print(second_url)
s = requests.get('https://www.gadgetsnow.com/pwafeeds/gnow/web/show/gadgets/json?uName={}&category=laptop'.format(crawl_url)).json()
extra = s['jsonFeed']['data']['item']['specs']
print(extra)