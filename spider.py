import codecs
import ssl
from cosineSim import *
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from projectData import *

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # updates user display, fills queue, updates files and checks cosine similarity
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            with codecs.open(PROJECT_NAME + '/' + PROJECT_NAME + 'PL' + '.txt', 'a', 'utf-8-sig') as f:
                for link in Spider.gather_links(page_url):
                    f.write(page_url + ',' + link + '\n')
                    with codecs.open(PROJECT_NAME + '/' + PROJECT_NAME + 'WL' '.txt', 'a', 'utf-8-sig') as g:
                        g.write((get_domain_name(page_url)) + ',' + (get_domain_name(link)) + '\n')
                    if (get_domain_name(page_url)) != (get_domain_name(link)):
                        with codecs.open(PROJECT_NAME + '/' + PROJECT_NAME + 'WLC' '.txt', 'a', 'utf-8-sig') as h:
                            h.write((get_domain_name(page_url)) + ',' + (get_domain_name(link)) + '\n')
            if cosine_similarity(START_PAGE, page_url) > COSINE_SIM:
                Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url, context=ctx)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            with codecs.open(PROJECT_NAME + '/' + PROJECT_NAME + 'ER' + '.txt', 'a', 'utf-8-sig') as f:
                f.write(page_url + ',' + str(e) + '\n')
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            # if Spider.domain_name != get_domain_name(url):
            #     continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
