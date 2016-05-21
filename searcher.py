import numpy as np
import math

class Searcher:
    def __init__(self, collection_size, index, document_tokens, search_terms):
        self.__COLLECTION_SIZE = collection_size
        self.__index = index
        self.__doc_lengthes = self.__calc_doc_lengthes(document_tokens)
        self.__search_terms = search_terms
        self.__analyze(self.__search_terms)

    def __analyze(self, search_terms):
        print('# COSINE SCORES: ')
        for term in search_terms:
            idf_query = self.__calc_idf(term)
            length_query = self.__get_query_length(idf_query)

            cosine_scores = {}
            for doc_id in self.__get_doc_ocurs(term):
                tf_idf_token = self.__calc_tf_idf(term, doc_id, idf_query)
                page_score = idf_query * tf_idf_token
                cosine_score = page_score/self.__doc_lengthes[doc_id]/length_query
                cosine_scores[doc_id] = cosine_score

            print(term)
            print(cosine_scores)

    def __calc_idf(self, token):
        term_idf = math.log((self.__COLLECTION_SIZE/self.__get_doc_freq(token)), 10)
        return term_idf

    def __get_query_length(self, query_vector):
        return np.linalg.norm(query_vector)

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

    def __get_doc_ocurs(self, key):
        return self.__index[key][1][0]

    def __get_term_freqs_in_doc(self, key, doc_id):
        return self.__index[key][1][0][doc_id]