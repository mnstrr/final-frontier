# imports
from crawler import Crawler
from pageRank import PageRank
from indexer import Indexer
import time


class Main:
    base_url = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/'
    seed_urls = ['d01.html', 'd06.html', 'd08.html']

    def __init__(self):
        crawler = Crawler(self.seed_urls, self.base_url)
        page_rank = PageRank(crawler.get_internal_url_structure())
        indexer = Indexer(crawler.get_document_soups())


start_time = time.time()
Main()
print("Execution time is %s seconds" % "%0.2f" % (time.time() - start_time))
