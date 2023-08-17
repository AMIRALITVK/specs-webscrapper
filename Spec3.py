import pymysql
import pymysql.cursors
import json
import socket
from re import search
import os
import requests
import time
from datetime import datetime
import subprocess
import urllib.request
import flask_app

def word_count(txt):
    word_c = len(txt.split())
    return word_c
# ----------------------------------------------------------------------------- NOTEBOOK CHECK ----------------------------------------------------------------------------- #
def webservice(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id):
    os.system('cls')
    now_time = datetime.now()
    date_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    file_name = now_time.strftime('%Y-%m-%d %H-%M-%S')
    date_time_file = str(now_time.strftime('%Y-%m-%d'))
    client_ip = socket.gethostbyname('google.com')
    take_screen_shot = 'N'
    crawl_status = 'N'
    # if key_word:
    #     if word_count(key_word) >= 2 and len(key_word) > 4:
    #         pass
    #     else:
    #         result = { 'status': 'error', 'result': {'error_reason': 'keyword is too short', 'keyword': key_word, 'make': make, 'model': model_name, 'serial_number': serial_num}
    #         }
    #         crawl_status = 'F'
    #         flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
    #                              str(result), crawl_status, None, take_screen_shot, None, date_time, client_ip)
    #         return result
    # else:
    #     cpu_name = cpu_name[0:5]
    key_word = make + ' ' + model_name
    address = 'https://php7.torobika.com/goutte/nc.php?dev=false&keywords=dell%20precision%203530'
    try:
        # def select_line(p, line_index):
        #     return p.splitlines()[line_index]
        # print(cpu_name)
        # -------------- BATTERY -------------- #
        # pwsh_battery = subprocess.check_output(
        #     "pwsh -Executionpolicy byPass -Command Get-PortableBattery", shell=True, text=True)
        # battery_capacity = select_line(pwsh_battery, 3).replace('\u001b[32;1mDesignCapacity : \u001b[0m', '') + ' mWh'
        battery_capacity = 0
        # ------------------------------------- #
        print('hello')
        r = urllib.request.urlopen(address)
        # r = requests.get(address)
        # r = r.read()
        r_new = r.decode('utf-8')
        n = json.loads(r)
        print(type(r_new))
        return r_new
        print('bye')
        # exit()
        # length = len(r['jsonFeed']['data']['items'])
        # if length:
        #     keyword_found = 'T'
        # else:
        #     keyword_found = 'F'
        #     result = { 'status': 'error', 'result': {'error_reason': 'keyword not found', 'keyword': key_word, 'make': make, 'model': model_name, 'serial_number': serial_num}
        #     }
        #     flask_app.insert_log(site_id, make, model_name, serial_num, key_word,
        #                          str(result), crawl_status, keyword_found, take_screen_shot, None, date_time, client_ip)
        #     return result
        num = 0
        uName = []
        # print(cpu_name)
        # r = str(r)
        # r['jsonFeed']['data'] = r['jsonFeed']['data'].replace('"item"', '"items"')
        # print(r)
        length = 2
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
        keyword_found = 'T'
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
        extra = str(extra)
        print(type(extra))
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