# imports
from collections import OrderedDict
import numpy as np
import re

# Better printing options
np.set_printoptions(linewidth=1000, precision=4)

class PageRank:
    def __init__(self, internal_url_structure):
        self.__internal_url_structure = internal_url_structure
        self.__DAMPING_FACTOR = 0.95
        self.__TELEPORTATION_RATE = 1 - self.__DAMPING_FACTOR
        self.__DELTA = 0.04
        self.__COLLECTION_SIZE = len(self.__internal_url_structure)
        self.__transition_prob_tmp = self.__calc_transition_prob_tmp()
        self.__transition_prob = self.__make_transition_prob_matrix()
        self.__page_rank = self.__calc_page_rank()

    def __calc_transition_prob_tmp(self):
        transition_prob_tmp = {}

        for key in self.__internal_url_structure:
            internal_urls_size = len(self.__internal_url_structure[key])
            transition_prob_tmp[key] = []
            if internal_urls_size > 0:
                for internal_url in self.__internal_url_structure[key]:
                    transition_prob_tmp[key].append([(internal_url), (1.0 / internal_urls_size) * self.__DAMPING_FACTOR + (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)])
            else:
                transition_prob_tmp[key].append([(None), 1 / self.__COLLECTION_SIZE])
        transition_prob_tmp = self.__sort_url_structure(transition_prob_tmp)

        self.__print_transition_prob_tmp(transition_prob_tmp)
        return transition_prob_tmp

    def __make_transition_prob_matrix(self):
        matrix = np.zeros((self.__COLLECTION_SIZE, self.__COLLECTION_SIZE))
        matrix[:] = (self.__TELEPORTATION_RATE / self.__COLLECTION_SIZE)

        for row, row_val in self.__transition_prob_tmp.items():
            row_index = int(re.sub('[d0]', '', row))
            for col in row_val:
                # if URL doesn't contain internal URLS
                if col[0] is None:
                    col_val = col[1]
                    matrix[row_index - 1, :] = col_val
                    self.__print_transition_prob_matrix(matrix)
                    return matrix
                col_index = int(re.sub('[d0]', '', col[0]))
                col_val = col[1]
                matrix[row_index - 1, col_index - 1] = col_val

    def __calc_page_rank(self):
        step = 0
        initial_step = np.full((1, self.__COLLECTION_SIZE), 1/self.__COLLECTION_SIZE, dtype=np.float)
        prev_step = initial_step

        page_rank = []
        page_rank.append(initial_step)

        print('# PAGE RANK:')
        print('           d01     d02     d03     d04     d05     d06     d07     d08     diff')
        print('step: ' + str(step) + ' ' + str(initial_step[0]))

        # do...while loop
        while True:
            step += 1
            current_step = np.dot(prev_step, self.__transition_prob)
            current_delta = np.sum(abs(current_step - prev_step))
            print('step: ' + str(step) + ' ' + str(current_step[0]) + ' ' + str("%0.4f" % current_delta))

            page_rank.append(current_step)
            prev_step = current_step

            if (current_delta < self.__DELTA):
                break

        print('--------------------')
        return page_rank

    def __sort_url_structure(self, dict):
        sorted_dict = OrderedDict(sorted(dict.items()))
        return sorted_dict

    def __print_transition_prob_tmp(self, transition_prob_tmp):
        print('# TEMPORARY TRANSITION PROB: ')
        for key, values in transition_prob_tmp.items():
            s = ''
            for item in values:
                s +='[' + str(item[0]) +', ' + "%0.3f" % item[1] + ']; '
            print(key + ': ' + s)
        print('--------------------')

    def __print_transition_prob_matrix(self, transition_prob_matrix):
        print('# FINAL TRANSITION PROB MATRIX:')
        print(transition_prob_matrix)
        print('--------------------')

















