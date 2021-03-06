# imports
from crawler import Crawler
from pageRank import PageRank
from indexer import Indexer
from searcher import Searcher
import time


class Main:
    base_url = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/'
    seed_urls = ['d01.html', 'd06.html', 'd08.html']
    search_terms = ['tokens', 'index', 'classification', 'tokens classification']

    def __init__(self):
        crawler = Crawler(self.seed_urls, self.base_url)
        page_rank = PageRank(crawler.get_internal_url_structure(), crawler.get_collection_size())
        indexer = Indexer(crawler.get_document_soups())
        searcher = Searcher(crawler.get_collection_size(), indexer.get_index(), indexer.get_document_terms(), self.search_terms, page_rank.get_page_rank())


start_time = time.time()
Main()
print('--------------------')
print("Execution time is %s seconds" % "%0.2f" % (time.time() - start_time))
