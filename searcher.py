
class Searcher:
    def __init__(self, index):
        self.__index = index

        print('Dummy Examples for token "document": ')
        print(self.get_doc_freq('document'))
        print(self.get_term_freq('document'))

    def get_doc_freq(self, key):
        return self.__index[key][0]

    def get_term_freq(self, key):
        return self.__index[key][1][0]
