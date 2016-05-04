import urllib.request as ur
from bs4 import BeautifulSoup as bs
import numpy as np


class Crawler:
    def __init__(self, seedList, baseUrl):
        self.__seedList = seedList
        self.__baseUrl = baseUrl
        self.__frontierList = []
        self.__visitedList = set()
        self.__crawl()
        self.__test()

    def __crawl(self):
        for url in self.__seedList:

            self.__frontierList.append(url)

            while len(self.__frontierList) > 0:
                currenturl = self.__frontierList[0]
                page = ur.urlopen(currenturl)
                soup = bs(page.read(), "html.parser")
                self.__visitedList.add(currenturl)
                self.__frontierList.pop()[0]

                for link in soup.find_all('a'):
                    url1 = self.__baseUrl + link.get('href')
                    if url1 not in self.__visitedList:
                        self.__frontierList.append(url1)
                        self.__visitedList.add(url1)

    def __test(self):
        m = np.matrix('1 2; 3 4')
        print(m)

    def printLinks(self):
        for ele in self.__visitedList:
            print(ele)