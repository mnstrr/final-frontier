from crawler import Crawler
from pagerank import Pagerank


class Main:
    baseURL = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/'
    seedList = ['d01.html', 'd06.html', 'd08.html']

    def __init__(self):
        crawler = Crawler(self.seedList, self.baseURL)
        crawler.printInURLs()
        pageRank = Pagerank(crawler.getInUrls())

Main()
