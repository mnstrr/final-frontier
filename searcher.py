import math
import operator
import re
from collections import OrderedDict


class Searcher:
    def __init__(self, collection_size, index, document_tokens, search_terms, page_rank):
        self.__COLLECTION_SIZE = collection_size
        self.__index = index
        self.__page_rank = page_rank
        self.__doc_lengths = self.__calc_doc_lengths(document_tokens)
        self.__calc_cosine_scores(search_terms, False)
        self.__calc_cosine_scores(search_terms, True)

    def __calc_cosine_scores(self, search_terms, combine_with_page_rank=False):
        if combine_with_page_rank:
            print('--------------------')
            print('# COSINE SCORES WITH PAGERANK: ')
        else:
            print('# COSINE SCORES: ')

        for search_term in search_terms:
            length_query = 0
            doc_scores = {}

            for token in search_term.split():
                idf_query = self.__calc_idf(token)
                length_query += idf_query ** 2

                for doc_id in self.__get_doc_occurrences(token):
                    tf_idf_token = self.__calc_tf_idf(token, doc_id, idf_query)
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = 0
                    doc_scores[doc_id] += idf_query * tf_idf_token

            length_query = math.sqrt(length_query)

            cosine_scores = {}
            for doc_id in doc_scores:
                cosine_score = doc_scores[doc_id] / self.__doc_lengths[doc_id] / length_query
                cosine_scores[doc_id] = cosine_score

            if combine_with_page_rank:
                for doc_id in cosine_scores:
                    doc_index = int(re.sub('[d0]', '', doc_id))
                    cosine_score = cosine_scores[doc_id]
                    page_rank = self.__page_rank[len(self.__page_rank) - 1][0][doc_index - 1]
                    cosine_scores[doc_id] = 2 * (cosine_score  * page_rank) / (cosine_score + page_rank)
            cosine_scores_sorted = self.__convert_dict_to_sorted_list(cosine_scores)

            print('"' + search_term+'":')
            for cosine_score in cosine_scores_sorted:
                print(str(cosine_score[0])+': ' + str("%0.6f" % cosine_score[1]))

    def __convert_dict_to_sorted_list(self, dict):
        list = sorted(dict.items(), key=operator.itemgetter(1))
        list.reverse()
        return list

    def __calc_idf(self, token):
        term_idf = math.log((self.__COLLECTION_SIZE / self.__get_doc_freq(token)), 10)
        return term_idf

    def __calc_tf_idf(self, term, doc_id, idf):
        tf_idf = (1 + math.log(self.__get_term_freqs_in_doc(term, doc_id), 10)) * idf
        return tf_idf

    def __calc_doc_lengths(self, document_tokens):
        doc_lengths = {}
        for doc_id in document_tokens:
            result = 0
            for token in set(document_tokens[doc_id]):
                idf = self.__calc_idf(token)
                tf_idf = self.__calc_tf_idf(token, doc_id, idf)
                result += tf_idf ** 2
            doc_lengths[doc_id] = math.sqrt(result)

        print('--------------------')
        print('# DOC LENGTHS:')
        ordered_lengths = self.__order_keys_in_dict(doc_lengths)
        for key, value in ordered_lengths.items():
            print(key + ": " + str(value))
        print('--------------------')
        return doc_lengths

    def __get_doc_freq(self, key):
        return self.__index[key][0]

    def __get_doc_occurrences(self, key):
        return self.__index[key][1][0]

    def __get_term_freqs_in_doc(self, key, doc_id):
        return self.__index[key][1][0][doc_id]

    def __order_keys_in_dict(self, dictionary):
        return OrderedDict(sorted(dictionary.items()))
