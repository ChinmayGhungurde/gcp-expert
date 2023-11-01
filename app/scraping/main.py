from app.scraping.utils import Crawler
from app.scraping.settings import ROOT_URL

# Constants
SIDEMENU_CLASSNAME = 'devsite-nav-list'
CONTENT_SELECTOR = '.devsite-article'
DIRPATH = './data'

# Get the starting URLs
def get_start_urls(root_url):
    side_menu_crawler = Crawler()
    side_menu_crawler.call_url(root_url)
    side_menu = side_menu_crawler.get_elements_by_class(SIDEMENU_CLASSNAME)[1]
    links = side_menu_crawler.get_all_links(side_menu)
    return links

if __name__ == '__main__':
    start_urls = get_start_urls(ROOT_URL)
    crawler = Crawler(start_urls)
    crawler.recursive_crawl_by_selector(CONTENT_SELECTOR, DIRPATH)