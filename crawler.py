import urllib.request
from bs4 import BeautifulSoup as bs


class Crawler:
    def __init__(self, seedList, baseUrl):
        self.__seedList = seedList
        self.__baseUrl = baseUrl
        self.__frontierList = []
        self.__visitedList = []
        self.__linkDict = {}
        self.__crawl()

    def __crawl(self):
        for url in self.__seedList:

            if url not in self.__visitedList:
                self.__frontierList.append(url)
                self.__visitedList.append(url)

            while len(self.__frontierList) > 0:
                currentUrl = self.__frontierList[0]
                page = urllib.request.urlopen(currentUrl)
                soup = bs(page.read(), "html.parser")
                tag = soup.title.string
                self.__linkDict[tag] = []
                self.__frontierList.remove(currentUrl)
                for link in soup.find_all('a'):
                    url1 = self.__baseUrl + link.get('href')
                    self.__linkDict[tag].append(link.get('href'))
                    if url1 not in self.__visitedList:
                        self.__frontierList.append(url1)
                        self.__visitedList.append(url1)

    def printLinks(self):
        for ele in self.__visitedList:
            print(ele)

    def printLinkDict(self):
        for key,values in self.__linkDict.items():
            print(key)
            print(values)
