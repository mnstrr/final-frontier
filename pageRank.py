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

    def calcPageRank(self):
        pageRankVal = []
        delta = 1
        #step0
        prev_step = np.zeros((1, self.__pagecount))
        prev_step[:] = (1.0 / self.__pagecount)

        pageRankVal.append(prev_step)
        print('Page Rank : '+str(pageRankVal))
        diff_V = []


        #delta_V = []

        # step0 mult with transition matrix
        betragV = np.zeros((1, self.__pagecount))
        while (delta > 0.04):
            next_step = np.mat(prev_step) * np.mat(self.__transitionMatrix)
            print('next step : ' + str(next_step))
            pageRankVal.append(next_step)
            # add new diff
            tmp_diff = abs(next_step - prev_step)

            print('diff : ' + str(tmp_diff))
            diff_V.append(next_step - prev_step)

            for indx, val in enumerate(tmp_diff):
                betragV[indx] = abs(val)
            delta = np.sum(betragV)
            prev_step = next_step
            print('delta : ' + str(delta))



