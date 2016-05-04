import urllib.request
from bs4 import BeautifulSoup as bs


class Crawler:
    def __init__(self, seedList, baseUrl):
        self.__seedList = seedList
        self.__baseUrl = baseUrl
        self.__frontierList = []
        self.__visitedList = set()
        self.__linkDict = {}  # dict containing title as key and href sites as values
        self.__crawl()

    def __crawl(self):
        for url in self.__seedList:

            self.__frontierList.append(url)
            self.__visitedList.add(url)

            while len(self.__frontierList) > 0:
                currenturl = self.__frontierList[0]
                page = urllib.request.urlopen(currenturl)
                soup = bs(page.read(), "html.parser")
                title = soup.title.string
                self.__frontierList.pop()[0]
                self.__linkDict[title] = []

                for link in soup.find_all('a'):
                    href = link.get('href')
                    url1 = self.__baseUrl + href
                    self.__linkDict[title].append(href)
                    if url1 not in self.__visitedList:
                        self.__frontierList.append(url1)
                        self.__visitedList.add(url1)

    def printLinks(self):
        for ele in self.__visitedList:
            print(ele)

    def printLinkDict(self):
        for x in self.__linkDict:
            print(x)
            for y in self.__linkDict[x]:
                print(y, ':', self.__linkDict[x][y])