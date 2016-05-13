# imports
from collections import OrderedDict
import numpy as np
import re
import textwrap

# Better printing options
np.set_printoptions(linewidth=1000)

class PageRank:
    def __init__(self, internal_url_structure):
        self.__internal_url_structure = internal_url_structure
        self.__DAMPING_FACTOR = 0.95
        self.__TELEPORTATION_RATE = 1 - self.__DAMPING_FACTOR
        self.__DELTA = 0.04
        self.__COLLECTION_SIZE = len(self.__internal_url_structure)
        self.__transition_prob_tmp = self.__calc_transition_prob()
        self.__transition_prob_matrix = self.__create_matrix()
        self.__calc_page_rank()

    def __calc_transition_prob(self):
        transitions = {}

        for key in self.__internal_url_structure:
            internal_urls_size = len(self.__internal_url_structure[key])
            transitions[key] = []
            if internal_urls_size > 0:
                for internal_url in self.__internal_url_structure[key]:
                    transitions[key].append([(internal_url), (1.0 / internal_urls_size) * self.__DAMPING_FACTOR + (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)])
            else:
                transitions[key].append([(None), 1 / self.__COLLECTION_SIZE])
        transitions = self.__sort_url_structure(transitions)
        return transitions

    def __create_matrix(self):
        matrix = np.zeros((self.__COLLECTION_SIZE, self.__COLLECTION_SIZE))
        matrix[:] = (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)

        for row, row_val in self.__transition_prob_tmp.items():
            row_index = int(re.sub('[d0]', '', row))
            for col in row_val:
                # if URL doesn't contain internal URLS
                if col[0] is None:
                    col_val = col[1]
                    matrix[row_index - 1, :] = col_val
                    return matrix
                col_index = int(re.sub('[d0]', '', col[0]))
                col_val = col[1]
                matrix[row_index - 1, col_index - 1] = col_val

    def __calc_page_rank(self):
        pageRankVal = []
        delta = 1
        # step0
        prev_step = np.zeros((1, self.__COLLECTION_SIZE))
        prev_step[:] = (1.0 / self.__COLLECTION_SIZE)

        pageRankVal.append(prev_step)
        print('Page Rank : ' + str(pageRankVal))
        diff_V = []

        # delta_V = []

        # step0 mult with transition matrix
        betragV = np.zeros((1, self.__COLLECTION_SIZE))
        while (delta > 0.04):
            next_step = np.mat(prev_step) * np.mat(self.__transition_prob_matrix)
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

    def __sort_url_structure(self, dict):
        sorted_dict = OrderedDict(sorted(dict.items()))
        return sorted_dict

    def print_transition_prob_tmp(self):
        print('# TEMPORARY TRANSITION PROB: ')
        for key, values in self.__transition_prob_tmp.items():
            s = ''
            for item in values:
                s +='[' + str(item[0]) +', ' + "%0.3f" % item[1] + ']; '
            print(key + ': ' + s)
        print('--------------------')

    def print_transition_prob_matrix(self):
        print('# FINAL TRANSITION PROB MATRIX:')
        print(self.__transition_prob_matrix)
        print('--------------------')

















