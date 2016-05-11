from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import re
import urllib.request


class Crawler:
    def __init__(self, seedList, baseURL):
        self.__seedList = seedList
        self.__baseURL = baseURL
        self.__frontier = []
        self.__visited = []
        self.__inURLs = {}

    def crawl(self):
        for URL in self.__seedList:

            self.__frontier.append(self.__baseURL + URL)

            while len(self.__frontier) > 0:
                currentURL = self.__frontier[0]
                page = urllib.request.urlopen(currentURL)
                soup = bs(page.read(), "html.parser")
                self.__visited.append(currentURL)
                self.__frontier.pop(0)
                key = (re.search('(d[0-9]+)', currentURL)).group()
                self.__inURLs[key] = []

                for outURL in soup.find_all('a'):
                    currentOutURL = self.__baseURL + outURL.get('href')
                    value = (re.search('(d[0-9]+)', currentOutURL)).group()
                    self.__inURLs[key].append(value)
                    if currentOutURL not in self.__visited:
                        self.__frontier.append(currentOutURL)
                        self.__visited.append(currentOutURL)

        self.__inURLs = self.__sortDictionary(self.__inURLs)

    def __sortDictionary(self, dict):
        sorteddict = OrderedDict(sorted(dict.items()))
        for key in sorteddict:
            sorteddict[key] = sorted(sorteddict[key])
        return sorteddict

    def getInURLs(self):
        return self.__inURLs

    def printInURLs(self):
        for key, values in self.__inURLs.items():
            print(key)
            print(values)
