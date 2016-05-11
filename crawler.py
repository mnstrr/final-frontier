import urllib.request
from bs4 import BeautifulSoup as bs
import numpy as np


class Crawler:
    def __init__(self, seedList, baseUrl):
        self.__seedList = seedList
        self.__baseUrl = baseUrl
        self.__frontierList = []
        self.__visitedList = set()
        self.__crawl()

    def __crawl(self):
        for url in self.__seedList:

            self.__frontierList.append(url)

            while len(self.__frontierList) > 0:
                currenturl = self.__frontierList[0]
                page = urllib.request.urlopen(currenturl)
                soup = bs(page.read(), "html.parser")
                self.__visitedList.add(currenturl)
                self.__frontierList.pop(0)

                for link in soup.find_all('a'):
                    url1 = self.__baseUrl + link.get('href')
                    if url1 not in self.__visitedList:
                        self.__frontierList.append(url1)
                        self.__visitedList.add(url1)

    def printLinks(self):
        for ele in self.__visitedList:
            print(ele)

    def createMatix(self):
        matrix = np.zeros((len(self.__visitedList), len(self.__visitedList)))
        #print(matrix)
        for page in range(1 , len(self.__seedList)):
        #for page in self.__seedList:
            for linkedPage in range(1 , len(self.__visitedList)):
            #for linkedPage in self.__visitedList:
                if page != self.__visitedList:
                    matrix[page, linkedPage] = 1
               # elif page == self.__seedList:
                    # go to next row
                else:
                    matrix[page, linkedPage] = 0

        print(matrix)
# create matrix of len(self.__visitedList)
#a = np.matrix('1 2; 3 4')
#print(a)