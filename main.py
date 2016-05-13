# imports
from crawler import Crawler
from pageRank import PageRank


class Main:
    base_url = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/'
    seed_urls = ['d01.html', 'd06.html', 'd08.html']

    def __init__(self):
        crawler = Crawler(self.seed_urls, self.base_url)
        crawler.print_internal_url_structure()

        page_rank = PageRank(crawler.get_internal_url_structure())
        page_rank.print_transition_prob_tmp()
        page_rank.print_transition_prob_matrix()

Main()
