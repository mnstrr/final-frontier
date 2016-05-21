import math
import operator

class Searcher:
    def __init__(self, collection_size, index, document_tokens, search_terms):
        self.__COLLECTION_SIZE = collection_size
        self.__index = index
        self.__doc_lengths = self.__calc_doc_lengthes(document_tokens)
        self.__calc_cosine_scores(search_terms)

    def __calc_cosine_scores(self, search_terms):
        print('# COSINE SCORES: ')
        for term in search_terms:
            length_query = 0
            doc_scores = {}

            for splitted_term in term.split():
                idf_query = self.__calc_idf(splitted_term)
                length_query += idf_query ** 2

                for doc_id in self.__get_doc_occurrences(splitted_term):
                    tf_idf_token = self.__calc_tf_idf(splitted_term, doc_id, idf_query)
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = 0
                    doc_scores[doc_id] += idf_query * tf_idf_token

            length_query = math.sqrt(length_query)

            cosine_scores = {}
            for doc_id in doc_scores:
                cosine_score = doc_scores[doc_id]/self.__doc_lengths[doc_id]/length_query
                cosine_scores[doc_id] = cosine_score
                cosine_scores_sorted = self.__convert_dict_to_sorted_list(cosine_scores)

            print(term)
            print(cosine_scores_sorted)

    def __convert_dict_to_sorted_list(self, dict):
        list = sorted(dict.items(), key=operator.itemgetter(1))
        list.reverse()
        return list

    def __calc_idf(self, token):
        term_idf = math.log((self.__COLLECTION_SIZE/self.__get_doc_freq(token)), 10)
        return term_idf

    def __calc_tf_idf(self, term, doc_id, idf):
        tf_idf = (1+math.log(self.__get_term_freqs_in_doc(term, doc_id), 10)) * idf
        return tf_idf

    def __calc_doc_lengthes(self, document_tokens):
        doc_lengthes = {}
        for doc_id in document_tokens:
            result = 0
            for token in set(document_tokens[doc_id]):
                    idf = self.__calc_idf(token)
                    tf_idf = self.__calc_tf_idf(token, doc_id, idf)
                    result += tf_idf ** 2
            doc_lengthes[doc_id] = math.sqrt(result)
        return doc_lengthes

    def __get_doc_freq(self, key):
        return self.__index[key][0]

    def __get_doc_occurrences(self, key):
        return self.__index[key][1][0]

    def __get_term_freqs_in_doc(self, key, doc_id):
        return self.__index[key][1][0][doc_id]