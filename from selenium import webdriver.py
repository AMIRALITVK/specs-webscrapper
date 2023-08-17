from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent

PATH = r"chromedriver.exe"
options = Options()
options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
ua = UserAgent()
a = ua.random
user_agent = ua.random
try:
    gpu_options_xpath = "//*[@id='gpu']/div/div/div[2]/div/div[{}]/div/label/span[1]".format(div_num)
    gpu_options += str(div_num) + '. ' + driver.find_element(By.XPATH, gpu_options_xpath).text + ' & '
    div_num += 1
            # print('error')
                # print(gpu_options)
except Exception as e:
    div_num = 'asdfasdfasdf'
    gpu_options = div_num.rstrip(div_num[-1])
# print(user_agent)
options.add_argument(f'user-agent={user_agent}')
d = webdriver.Chrome(executable_path=PATH, options=options)
# agent = d.execute_script("return navigator.userAgent")
# d.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"python 3.6", "platform":"Linux"})
# agent = d.execute_script("return navigator.userAgent")
# options.add_argument(agent)
d.get('https://laptopmedia.com/specs/')
# time.sleep(6)
wait = WebDriverWait(d, timeout=15, poll_frequency=1)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#search-input > div > input")))
title = d.find_element(By.CSS_SELECTOR, 'body > section > div.order-3.mx-auto.mx-auto.w-full.xl\:order-3.hidden.md\:block > div > div:nth-child(1) > h3').text
print(title)
d.close()