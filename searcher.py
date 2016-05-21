import numpy as np

class Searcher:
    def __init__(self, index):
        self.__index = index

        print('Dummy Examples for token "document": ')
        print(self.__get_doc_freq('document'))
        print(self.__get_term_freq('document'))

        my_vector = np.array([1,2,3,4,5])
        print(self.__get_query_length(my_vector))

    # TODO: log10(N/DF), N=Anzahl der Dokumente, DF=get_doc_freq
    def __calc_token_idf(self, token):
        token_idf = 0.2041
        return token_idf

    # returns the magnitude of a vector, normalized
    # this method takes a vector => np.array([1,2,3,4,5])
    def __get_query_length(self, query_vector):
        return np.linalg.norm(query_vector)

    # 2) "_Represent each document as a weighted tf-idf vector" => TF-IDF für d04 berechnen
    # TODO: (1 +  log10(term_freq)) * token_idf
    def __calc_term_weight(self, token_or_term):
        return 0.2656

    # 3) Page Score
    # TODO: PAGE SCORE = IDF von 'tokens' aus Schritt 1 * TF-IDF aus Schritt 2 = 0.2041 * 0.2656 = 0.0542
    def __calc_page_score(self, ):
        return 0.0542


    def __get_doc_freq(self, key):
        return self.__index[key][0]

    def __get_term_freq(self, key):
        return self.__index[key][1][0]
