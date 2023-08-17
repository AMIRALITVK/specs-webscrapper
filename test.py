from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PATH = r"chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome(executable_path=PATH, options=options)
d.get('https://www.google.com/')
print(d.title)
d.close()