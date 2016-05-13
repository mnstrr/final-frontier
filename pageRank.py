from collections import OrderedDict
import numpy as np
#regular expression
import re

class PageRank:
    def __init__(self, inURLs):
        self.__inURLs = inURLs
        self.__damping = 0.95
        self.__teleport = 1 - self.__damping
        self.__delta = 0.04
        self.__pagecount = len(self.__inURLs)
        self.__transitionProbabilities = self.__calculateTransition()
        self.__transitionMatrix = self.__createMatix()


    def __calculateTransition(self):
        transitions = {}

        for url in self.__inURLs:
            outlinkCount = len(self.__inURLs[url])
            transitions[url] = []
            if outlinkCount > 0:
                for outlink in self.__inURLs[url]:
                    transitions[url].append(
                        [(outlink), (1.0 / outlinkCount) * self.__damping + (self.__teleport / self.__pagecount)])
            else:
                transitions[url].append([('d00'), 1 / self.__pagecount])
        transitions = self.__sortDictionary(transitions)
        return transitions

    def __sortDictionary(self, dict):
        sorteddict = OrderedDict(sorted(dict.items()))
        return sorteddict

    def printTransitions(self):
        for key, values in self.__transitionProbabilities.items():
            print(key)
            print(values)


    def __createMatix(self):
        #create empty matrix
        matrix = np.zeros((self.__pagecount, self.__pagecount))
        matrix[:] = (self.__teleport / self.__pagecount)

        for row, rowVal in self.__transitionProbabilities.items():
            rowNr = int(re.sub('[d0]', '', row))
            for col in rowVal:
                if rowNr == 8:
                    colVal = col[1]
                    matrix[rowNr - 1, :] = colVal
                    return matrix
                colNr = int(re.sub('[d0]', '', col[0]))
                colVal = col[1]
                matrix[rowNr - 1, colNr - 1] = colVal

    def printMatix(self):
        print(self.__transitionMatrix)

    def calcMatix(self):
        matrix = np.zeros((self.__pagecount, self.__pagecount))
        matrix[:] = (1.0 / self.__pagecount)

        product = np.mat(matrix)*np.mat(self.__transitionMatrix)
        print(product)


