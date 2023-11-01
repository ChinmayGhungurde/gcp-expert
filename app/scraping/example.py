from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

from app.scraping.settings import BLACKLIST_URLS
 
url = 'https://cloud.google.com/vertex-ai/docs/quotas' 
 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install())) 
 
driver.get(url)
content = driver.find_element(By.CLASS_NAME, 'devsite-article')
contentText = content.text

filename = f"./data/quotas.txt"
Path(filename).write_bytes(bytes(contentText, 'utf-8'))

# lnks=content.find_elements(By.TAG_NAME, "a")
# traverse list
# for lnk in lnks:
#    # get_attribute() to get all href
#    link = lnk.get_attribute("href")
#    if(link not in BLACKLIST_URLS):
#     print(link)
 