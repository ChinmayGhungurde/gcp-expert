from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse
import json
import inspect

from app.scraping.settings import WHITELIST_URLS, METADATA_FILENAME

class Crawler:
    def __init__(self, urls=[]):
        self.urls = urls
        self.visited_urls = []

        # Configure the driver
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install()), options=options) 

    # Reset the current URLs queue, visited array and restart the driver
    def reset(self, urls):
        self.urls = urls
        self.visited_urls = []
        self.driver.quit()
        self.driver.start_client()

    # Return the driver
    def get_driver(self):
        return self.driver
    
    # Initialize the driver with given url
    def call_url(self, url):
        self.driver.get(url)

    def get_element_by_tag(self, tag, parent=None):
        try:
            if(parent):
                return parent.find_elements(By.TAG_NAME, tag)
            else:
                return self.driver.find_elements(By.TAG_NAME, tag)
        except Exception as e:
            frame = inspect.currentframe()
            print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

    def get_elements_by_class(self, class_name, parent=None):
        try:
            if(parent):
                return parent.find_elements(By.CLASS_NAME, class_name)
            else:
                return self.driver.find_elements(By.CLASS_NAME, class_name)
        except Exception as e:
            frame = inspect.currentframe()
            print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

    def get_elements_by_selector(self, selector, parent=None):
        try:
            if(parent):
                return parent.find_elements(By.CSS_SELECTOR, selector)
            else:
                return self.driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception as e:
            frame = inspect.currentframe()
            print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

    def get_all_links(self, parent):
        links = []
        parsed = urlparse(self.driver.current_url)
        domain = parsed.netloc
        protocol = parsed.scheme
        try:
            if(parent):
                soup = BeautifulSoup(parent.get_attribute('outerHTML'), features="html.parser")
                lnks = soup.find_all('a', href=True)
                # traverse list
                for lnk in lnks:
                    # get_attribute() to get all href
                    link = f"{protocol}://{domain}{lnk['href']}"
                    if (link == None):
                        continue
                    for wl_url in WHITELIST_URLS:
                        if(link.startswith(wl_url)):
                            links.append(link) 

            else:
                soup = BeautifulSoup(self.driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML'), features="html.parser")
                lnks = soup.find_all('a', href=True)
                # traverse list
                for lnk in lnks:
                    # get_attribute() to get all href
                    link = lnk['href']
                    for wl_url in WHITELIST_URLS:
                        if(link.startswith(wl_url)):
                            links.append(link)   
            return links
        except Exception as e:
            frame = inspect.currentframe()
            print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

    def recursive_crawl_by_selector(self, selector, dirpath):
        try:
            print(f"URLs count: {len(self.urls)}")
            if(len(self.urls) == 0):
                return
            url = self.urls.pop(0)
            self.visited_urls.append(url)
            self.driver.get(url)
            content = self.driver.find_element(By.CSS_SELECTOR, selector)

            # Search for additional links in the content
            links = self.get_all_links(content)

            # If the obtained URLs are not already visited, append them to our current URLs tree
            for link in links:
                if ((link not in self.visited_urls) and (link not in self.urls) and ('#' not in link)):
                    self.urls.append(link)
            
            # Extract text content from current content and write to a file in given path
            text = content.text
            filename = f"{dirpath}/{url.split('/')[-1]}.txt"
            Path(filename).write_bytes(bytes(text, 'utf-8'))

            print(f"Wrote {filename}")

            # Write the metadata
            try:
                with open(f"{dirpath}/{METADATA_FILENAME}.json", "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = []

            md_obj = {
                'path': filename,
                'url': url
            }
            data.append(md_obj)

            with open(f"{dirpath}/{METADATA_FILENAME}.json", 'w') as f:
                json.dump(data, f, indent=2)


            # Perform Depth-first Search on the remaining URL tree to scan the rest of the docs
            while(len(self.urls) != 0): 
                self.recursive_crawl_by_selector(selector, dirpath)

        except Exception as e:
            frame = inspect.currentframe()
            print(f"Error in {inspect.getframeinfo(frame).function}: {e}")
    