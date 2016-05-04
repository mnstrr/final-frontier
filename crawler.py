import urllib.request
from bs4 import BeautifulSoup as bs

class Crawler:
    def __init__(self, seedList, baseUrl):
        self.__seedList = seedList
        self.__baseUrl = baseUrl
        self.__frontier = list()
        self.__visited = set()
        self.__crawl()

    def __crawl(self):
        for url in self.__seedList:

            self.__frontier.append(self.__baseUrl + url)

            while len(self.__frontier) > 0:
                currentURL = self.__frontier[0]
                page = urllib.request.urlopen(currentURL)
                soup = bs(page.read(), "html.parser")
                self.__visited.add(currentURL)
                self.__frontier.pop(0)

                for outURL in soup.find_all('a'):
                    currentOutURL = self.__baseUrl + outURL.get('href')
                    if currentOutURL not in self.__visited:
                        self.__frontier.append(currentOutURL)
                        self.__visited.add(currentOutURL)

    def printURLs(self):
        for ele in self.__visited:
            print(ele)
