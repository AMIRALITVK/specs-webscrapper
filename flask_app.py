from datetime import datetime
import os
import pymysql
import pymysql.cursors
from flask import Flask, request
# import spec_laptopmedia
# import spec_gadgetsnow
# import spec_notebookcheck
# import warranty_asus
# import warranty_acer
# import warranty_dell
import warranty_hp
# import warranty_lenovo
# import warranty_toshiba


# ----- CONFIGS ----- #
app = Flask(__name__)

# app.debug = True

now_time = datetime.now()
date_time_file = str(now_time.strftime('%Y-%m-%d'))
date_time_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))

break_line = "\n\n" + "---------------------------------------------------------------------------------" + "\n\n"
db_host = 'localhost'
db_user = 'specref_usr'
db_pass = 'w*67Rp@(lwnk'
db_name = 'specref_db'

                                        # --------------------------  SPEC SQL INSERTION   -------------------------- #
def insert_log_spec(site_id, make, model_name, serial_num, key_word, result, crawl_status, keyword_found, take_screen_shot, image_name, date_time, client_ip):
    try:
        # print('insert')
        connection = pymysql.connect(host= db_host, user= db_user, password= db_pass,
                                 database= db_name, cursorclass=pymysql.cursors.DictCursor)
        request_status = ""
    except Exception as e:
        # return 'error'
        return str(e)
    try:
        # print('still ok!')
        with connection.cursor() as cursor:
            sql = "INSERT INTO `check_specs` (`site_id`, `make`, `model_name`, `serial_number`, `keywords`, `result`, `crawl_status`, `keyword_found`, `screen_shot`, `image`, `date_time`, `client_ip`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                sql, (site_id, make, model_name, serial_num, key_word, result, crawl_status, keyword_found, take_screen_shot, image_name, date_time, client_ip))
            connection.commit()
    except Exception as e:
        return str(e)
    finally:
        connection.close()
        if request_status == "":
            request_status = "T"
        else:
            request_status = "F"
        try:
            log_text = "new RQ @ " + date_time_time + ' from ' + client_ip + '\n' + "site_id : " + site_id + '\n' + "make : " + make + '\n' + 'model : ' + model_name + '\n' + 'serial_number : ' + serial_num + '\n' + 'crawl_status : ' + crawl_status + '\n' + 'request_status : ' + request_status + '\n' + 'result : ' + result + break_line

            log_file = open('logs/' + date_time_file + '.txt', 'a', encoding='utf-8')
            log_file.write(log_text)
            log_file.close()
        except Exception as e:
            return str(e)
# -----   LOG FILE RECORD   ----- #

                                        # --------------------------  WARRANTY SQL INSERTION   -------------------------- #
def insert_log_warranty(make, serial_num, warranty_status_db, result, crawl_status, file_name, date_time, client_ip):
    connection = pymysql.connect(host= db_host, user= db_user, password= db_pass, database= db_name, cursorclass=pymysql.cursors.DictCursor)
    request_status = ""
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `check_warranty` (`make`, `serial_number`, `warranty_status`, `result`, `status`, `image`, `date_time`, `client_ip`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(
                sql, (make, serial_num, warranty_status_db, result, crawl_status, file_name, date_time, client_ip))
            connection.commit()
    except (Exception, pymysql.Error) as e:
        return str(e)
    finally:
        if request_status == "":
            request_status = "T"
        else:
            request_status = "F"

        # ------- LOGGING RECORDS --------#
        if crawl_status == 'T' and request_status == 'T':
            check_result = 'success'
        elif crawl_status == 'T' and request_status == 'F':
            check_result = request_status
        elif crawl_status == 'F':
            check_result = str(result)
            result = ''
        else:
            check_result = "Can not determine the error!"
        if warranty_status_db == None:
            warranty_status_db = ''
            result = ''

        now_time = datetime.now()
        date_time_file = str(now_time.strftime('%Y-%m-%d'))
        date_time_time = str(now_time.strftime('%Y-%m-%d %H:%M:%S'))
        log_text = "new RQ @ " + date_time_time + ' from ' + client_ip + '\n' + "make : " + make + '\n' + 'serial_number : ' + serial_num + '\n' + 'warranty_status : ' + warranty_status_db + '\n' + 'crawl_status : ' + crawl_status + '\n' + 'request_status : ' + request_status + '\n' + 'result : ' + check_result + '\n' + 'warranty_info : ' + result + break_line
        try:
            log_file = open('logs/' + date_time_file + '.txt', 'a', encoding='utf-8')
            log_file.write(log_text)
            log_file.close()
        except Exception as e:
            return str(e)
        connection.close()

# ----- SPEC FUNCTION ----- #

@app.route("/spec", methods=['GET', 'POST'])    # type: ignore
def spec_req():
    os.system('clear')
    # return 'start'
    if request.method == 'POST':
        make = request.form.get('mk')
        model_name = request.form.get('mn')
        serial_num = request.form.get('sn')
        cpu_name = request.form.get('cp')
        key_word = request.form.get('kw')
        take_screen_shot = request.form.get('sc')
        method_id_user = request.form.get('mi')
        # IF SERIAL NUMBER IS SET
        if make and model_name and cpu_name:
            # print('done')
            connection = pymysql.connect(host= db_host, user= db_user, password= db_pass, database= db_name, cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = "SELECT `id`, `domain`, `method_id` FROM `sites` WHERE `status` = 'T' ORDER BY `priority` ASC"
                cursor.execute(sql)
                result = cursor.fetchall()
                # return str(result)
            try:
            # print(result)
                num = 0
                site = []
                while num < len(result):
                    site.append(result[num])
                    num += 1
                # print(site)
                for i in site:
                    method_id = i['method_id']
                    if method_id_user == '1' or method_id_user is None and method_id == 1:
                        # return('now in method func')
                        url = i['domain']
                        site_id = str(i['id'])
                        try:
                            output = spec_laptopmedia.crawl(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id)
                            return output
                        except Exception as e:
                            print(e)
                            return str(e)
                    else:
                        pass
                    if method_id_user == '2' or method_id_user is None and method_id == 2:
                        url = i['domain']
                        site_id = str(i['id'])
                        print(method_id)
                        try:
                            output = spec_gadgetsnow.crawl(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id)
                            return output
                        except Exception as e:
                            print(e)
                            return str(e)
                    else:
                        pass
                    if method_id_user == '3' or method_id_user is None and method_id == 3:
                        print(method_id)
                        url = i['domain']
                        site_id = str(i['id'])
                        try:
                            output = spec_gadgetsnow.webservice(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id)
                            return output
                        except Exception as e:
                            print(e)
                            return str(e)
                    else:
                        pass
                    if method_id_user == '4' or method_id_user is None and method_id == 4:    
                        url = i['domain']
                        site_id = str(i['id'])
                        print(method_id)
                        try:
                            output = spec_notebookcheck.webservice(make, model_name, serial_num, cpu_name, key_word, take_screen_shot, url, site_id)
                            return output
                        except Exception as e:
                            print(e)
                            return str(e)
                    else:
                        pass
            except Exception as sql_Error:
                print(sql_Error)
                return str(sql_Error)
            finally:
                connection.close()
        else:
            output = "There Is Not Enough Info!"
            return output
    else:
        output = "Method is not POST!"
        return output
# ---------------------- WARRANTY ---------------------- #

@app.route("/warranty", methods=['GET', 'POST'])  # type: ignore
def warranty():
    if request.method == 'POST':
        if request.form.get('mk') == 'asus':
            make = request.form.get('mk')
            serial_num = request.form.get('sn')
            if serial_num and make:
                try:
                    output = warranty_asus.warranty(serial_num, make)
                    return str(output)
                except Exception as e:
                    return str(e)
            else:
                output = "There Is No Serial Number!"
                return output
        elif request.form.get('mk') == 'acer':
            serial_num = request.form.get('sn')
            if serial_num:
                try:
                    output = warranty_acer.warranty(serial_num)
                    return output
                except Exception as e:
                    return str(e)
            else:
                output = "There Is No Serial Number!"
                return output
        elif request.form.get('mk') == 'dell':
            serial_num = request.form.get('sn')
            make = request.form.get('mk')
            if serial_num:
                try:
                    output = warranty_dell.warranty(serial_num, make)
                    return output
                except Exception as e:
                    return str(e)
            else:
                output = "There Is No Serial Number!"
                return output
        elif request.form.get('mk') == 'hp':
            serial_num = request.form.get('sn')
            model_num = request.form.get('mn')
            make = request.form.get('mk')
            if serial_num:
                try:
                    output = warranty_hp.warranty(serial_num, model_num, make)
                    return output
                except Exception as e:
                    return str(e)
            else:
                return "There Is No Serial Number!"
        elif request.form.get('mk') == 'lenovo':
            serial_num = request.form.get('sn')
            make = request.form.get('mk')
            if serial_num:
                try:
                    output = warranty_lenovo.warranty(serial_num, make)
                    return output
                except Exception as e:
                    return str(e)
            else:
                return "There Is No Serial Number!"
        elif request.form.get('mk') == 'toshiba':
            serial_num = request.form.get('sn')
            if serial_num:
                try:
                    output = warranty_toshiba.warranty(serial_num)
                    return output
                except Exception as e:
                    return str(e)
            else:
                return "There Is No Serial Number!"
    else:
        output = "Invalid request method!"
        return output