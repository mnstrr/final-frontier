from crawler import Crawler


class Main:
    baseURL = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/'
    seedList = ['http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d01.html',
                'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d06.html',
                'http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d08.html']

    def __init__(self):
        crawler = Crawler(self.seedList, self.baseURL)
        #crawler.printLinks()
        crawler.printLinkDict()

        pagerank = Pagerank()
        pagerank.makePagerank(crawler.getDictionary)

Main()