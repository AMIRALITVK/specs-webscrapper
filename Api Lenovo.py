import requests
from datetime import datetime
import json

now_time = datetime.now()
date_time_file = str(now_time.strftime('%Y-%m-%d'))
serial_num = str('PF2Z3MJM')
machine_type = str('20UC')


# payload = "{\"country\":\"gb\",\"channel\":\"APOS\",\"source\":null,\"couponNumber\":null,\"language\":\"en\",\"serialNumber\":\"PF2Z3MJM\",\"machineType\":\"20UC\",\"machineTypeModel\":\"\",\"brand\":\"TPG\"}"
url = "https://pcsupport.lenovo.com/gb/en/api/v4/upsell/redport/availableservices"
payload = {'country':'gb','channel':'APOS','source':'null','couponNumber':'null','language':'en','serialNumber':f'{serial_num}','machineType':f'{machine_type}','machineTypeModel':'null','brand':'TPG'}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'content-length': '166',
    'content-type': 'application/json',
    'Cookie': '_abck=22B64347A3C93B16D8A367CA49588CD0~-1~YAAQvofdWM+gMM+EAQAAInKP4gnGvhy3ssODZF/Tp9nZChGp6YV9YvemWEijEeqw14f6K4GzwklURwHdfKnpbzx4U/KVNkcbP7zbiA0lVKrotPxFoiLWnJi+Ju1iIUvonnZ0yXshI7bkvSRYu1fYYO69o1lyncPm1RDBfMeKLIutyM9zsngnskh7PtRalC9jNpzVW2C1z1l4PE7C/hBheiQ/rxXVlKrDt5duQr7sVojciUPtpxj1quRWy7kia1dyoEaPYeuDtUqtcUt93ytskTDUDL5EiDpZH5isAWjH+Xckbyy6uo+9ZnTqKvDKSzd7jxdGZ+5Xe3Fd1wI0yWF7/6rR/d1ojT9grw0cdfkqQjkXlr0MkG0PEy7T5HiipevkPYElVrybiLxT5+zIXoy6Jlmb30tBLWMc~0~-1~1668324760; ak_bmsc=2B15B3263319CCC91CE073A64990F987~000000000000000000000000000000~YAAQvofdWOJ8Mc+EAQAAdPyU4hK6N7HvqvZr9ya5hRvRFZs1ugVwQvPIrQIC9dAB0GNzCYm9X/GOMgiwO6+b9atUUHIXS3yXH9kN9Rnk7J5KMkUcHeZc5fUIVfF73iM5046v3c/batJRB7Ayp5mMi4UqZoC77F0O9eyo3xrHoR3joJ/AOc2zr0PtceZJszRRe9KfHIOgZtbdClPZWFIpAJJ8ijdg29zSKoOeEuJsIYYpcRnAaTKLvBkfHwbz1Sjt4GhJZpgb59k8BDo0QvqygEEHYrlZUT/vBOwtJ1KURjUMcJJqxuzAXCCKcZhagpiOVVhFvHGWu3T/lFKLOdWtOGBFrnp6l9rqst+Xh1Ckpfb16LhZz3yaZgffj8/QpyvM0mrZ2n13yzB7ekluEw==; bm_sv=CB7A5FB9C0C49AC2B81141F63FE50201~YAAQvofdWO1gM8+EAQAA0Weh4hJUQVM5Y+vxLU34pJgT6l3yVtpwaVvDxsFXSw4+BuDkqa3MRE6bKhuAMQG5uWP70JhDc9W7rR8RBI/dFFrkjNfIEG7oa/dsMUBGOz2O6l4PMJhCVR5N90LaHw9aim9D4HK/Ktt1J+uK7kriFA/BQda+MJ/naJiOXrmhnW3KUdoKr26QCHE1UAw47mBye+ap8JI5iA8lmc6F9K3VgDKk9LGyZw5JwWfbGVIh8EQRwg==~1; bm_sz=63C3D272B87A4F72A4CDAF2F94AB545E~YAAQvofdWFBsMc+EAQAAH5eU4hLtVxqBcP/YTdlXcmH/JFWbLm0qY934IACanOsw1gWwcnDDX1ndabFY8NYMpS7rsCLQxZMwwh54s65IN6xzTFbjZLaTj4qDi6YUhjIbsS1fpMXZxjYJ8DKMJgc8J0Jus7DQZK/hJ58YKJ4jrBLwMrV3osOKJ19in3tqwgXkCMtomue6vmdEMgaryhvmbhj8qxoyZGsloF5voFOST3m+soo1cX9HJFwL38495KSuRaTu7NyC+QTvdxWm1hYbS4PBgyugFKksFaOpi6n8J93DAFY=~3160373~3684658; esupport#lang1=en-gb'
}
try:
    response = requests.request("POST", url, headers=headers, json=payload).text
    response = json.loads(response)
    warranty = response['data']['ibaseInfo']['baseWarranties'][0]
    end_date = str(warranty['endDate'])
    check_status = end_date > date_time_file
# print(type(response))
# print(response)
    if check_status == True:
        warranty_status = 'Active'
    else:
        warranty_status = 'Expired'

    json_file = {
       'status': 'success', 'result': {'warranty': warranty_status, 'duration': str(warranty['duration']) + 'M', 'start_date': warranty['startDate'], 'end_date':   warranty['endDate'], 'description': warranty['description']}
    }
    with open(date_time_file + '.json', 'w', encoding='utf-8') as f:
                json.dump(json_file, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(str(e))