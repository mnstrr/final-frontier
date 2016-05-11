import urllib.request
from bs4 import BeautifulSoup as bs
import numpy as np
import re


class Crawler:
    def __init__(self, seedList, baseURL):
        self.__seedList = seedList
        self.__baseURL = baseURL
        self.__frontier = []
        self.__visited = []
        self.__inURLs = {}

        self.__crawl()

    def __crawl(self):
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

    def printURLs(self):
        for ele in self.__visited:
           print(ele)
        #print(self.__inURLs)

    def printInURLs(self):
        for key,values in self.__inURLs.items():
            print(key)
            print(values)

    def getPageCount(self):
        return len(self.__visited)

    def getInUrls(self):
        return self.__inURLs
