from pathlib import Path
from app.scraping.utils import Crawler
from app.scraping.settings import ROOT_URL, DATA_PATH, METADATA_FILENAME

# Constants
SIDEMENU_CLASSNAME = 'devsite-nav-list'
CONTENT_SELECTOR = '.devsite-article'

# Get the starting URLs
def get_start_urls(root_url):
    side_menu_crawler = Crawler()
    side_menu_crawler.call_url(root_url)
    side_menu = side_menu_crawler.get_elements_by_class(SIDEMENU_CLASSNAME)[1]
    links = side_menu_crawler.get_all_links(side_menu)
    return links

if __name__ == '__main__':
    # First pass, fetch all the links
    start_urls = get_start_urls(ROOT_URL)

    # (Re)create the metadata file
    metadata_path = Path(f"{DATA_PATH}/{METADATA_FILENAME}.json")
    f = open(metadata_path, "w")
    f.write('[]')
    f.close()


    # Second pass - Crawl all the fetched links
    crawler = Crawler(start_urls)
    crawler.recursive_crawl_by_selector(CONTENT_SELECTOR, DATA_PATH)