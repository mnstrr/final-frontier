from collections import OrderedDict
import numpy as np
import re

class PageRank:
    def __init__(self, internal_urls):
        self.__internal_urls = internal_urls
        self.__DAMPING_FACTOR = 0.95
        self.__TELEPORTATION_RATE = 1 - self.__DAMPING_FACTOR
        self.__DELTA = 0.04
        self.__COLLECTION_SIZE = len(self.__internal_urls)
        self.__transition_prob = self.__calc_transition_prob()
        self.__transition_matrix = self.__create_matrix()


    def __calc_transition_prob(self):
        transitions = {}

        for url in self.__internal_urls:
            outlinkCount = len(self.__internal_urls[url])
            transitions[url] = []
            if outlinkCount > 0:
                for outlink in self.__internal_urls[url]:
                    transitions[url].append(
                        [(outlink), (1.0 / outlinkCount) * self.__DAMPING_FACTOR + (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)])
            else:
                transitions[url].append([('d00'), 1 / self.__COLLECTION_SIZE])
        transitions = self.__sort_url_structure(transitions)
        return transitions

    def __sort_url_structure(self, dict):
        sorteddict = OrderedDict(sorted(dict.items()))
        return sorteddict

    def print_transitions(self):
        for key, values in self.__transition_prob.items():
            print(key)
            print(values)


    def __create_matrix(self):
        #create empty matrix
        matrix = np.zeros((self.__COLLECTION_SIZE, self.__COLLECTION_SIZE))
        matrix[:] = (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)

        for row, rowVal in self.__transition_prob.items():
            rowNr = int(re.sub('[d0]', '', row))
            for col in rowVal:
                if rowNr == 8:
                    colVal = col[1]
                    matrix[rowNr - 1, :] = colVal
                    return matrix
                colNr = int(re.sub('[d0]', '', col[0]))
                colVal = col[1]
                matrix[rowNr - 1, colNr - 1] = colVal

    def print_matrix(self):
        print(self.__transition_matrix)

    def calc_page_rank(self):
        pageRankVal = []
        delta = 1
        #step0
        prev_step = np.zeros((1, self.__COLLECTION_SIZE))
        prev_step[:] = (1.0 / self.__COLLECTION_SIZE)

        pageRankVal.append(prev_step)
        print('Page Rank : '+str(pageRankVal))
        diff_V = []


        #delta_V = []

        # step0 mult with transition matrix
        betragV = np.zeros((1, self.__COLLECTION_SIZE))
        while (delta > 0.04):
            next_step = np.mat(prev_step) * np.mat(self.__transition_matrix)
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



