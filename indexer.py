import re
from collections import OrderedDict

class Indexer:
    def __init__(self, document_soups):
        self.__STOPWORDS = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08', 'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do', 'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so', 'that', 'the', 'this', 'to', 'we']
        self.__document_tokens = self.__tokenize_each_soup(document_soups)
        self.__print_tokens()
        self.__index = self.__create_index()
        self.__print_index()

    def __tokenize_each_soup(self, document_soups):
        document_tokens = {}
        for doc_ID, soup in document_soups.items():
            document_tokens[doc_ID] = self.__tokenize(soup)

        return document_tokens

    def __tokenize(self, soup):
        document_tokens = []

        # removes all line breaks
        strained_soup = self.__remove_tags(["br"], soup)

        # only iterate over text content, should be obvious, but what everest
        for text in strained_soup.body.find_all(text=True):

            # removes interpunction, in this case "." and ","
            text = self.__remove_interpunction(str(text))

            # splits into separate words
            token_list = text.split()

            # if list not empty
            if token_list:
                token_list = self.__normalize_tokens(token_list)

                #concatenate all lists
                document_tokens.extend(token_list)

        document_tokens = self.__remove_stopwords(document_tokens, self.__STOPWORDS)
        return document_tokens

    def __create_index(self):
        index = {}
        index = self.__count_term_freqs(index)
        index = self.__count_doc_freqs(index)
        index = self.__order_keys_in_dict(index)
        return index

    def __count_term_freqs(self, index_tmp):

        # iterate over dict {doc_id: [tokens]}
        for doc_id, tokens in self.__document_tokens.items():
            # iterate over tokens in one document
            for token in tokens:

                # if token is already existing:
                if token in index_tmp:
                    # get dict
                    doc_occurrences = index_tmp[token][0][0]
                else:
                    # make new dict
                    doc_occurrences = {}

                if doc_id in doc_occurrences:
                    doc_occurrences[doc_id] += 1
                else:
                    doc_occurrences[doc_id] = 1

                index_tmp[token] = [[doc_occurrences]]

        return index_tmp

    def __count_doc_freqs(self, index_tmp):

        for token, doc_occurrences in index_tmp.items():
            index_tmp[token][:0] = [len(index_tmp[token][0][0])]

        return index_tmp

    def __remove_tags(self, unwanted_tags, soup):
        for tag in unwanted_tags:
            for match in soup.find_all(tag):
                match.unwrap()
        return soup

    def __remove_interpunction(self, text):
        text_neu = re.sub(r'[:,\.]', '', text)
        return text_neu

    def __remove_stopwords(self, tokens, stopwords):
        intersection = [itm for itm in tokens if itm not in stopwords]
        return intersection

    def __normalize_tokens(self, token_list):
        token_list = [element.lower() for element in token_list]
        return token_list

    def __print_tokens(self):
        print('# TOKENS:')
        self.__print_dict(self.__document_tokens)

    def __print_index(self):
        print('# INDEX:')
        self.__print_dict(self.__index)

    def __print_dict(self, dict):
        for key, value in dict.items():
            print(key + ' -> ' + str(value))
        print('--------------------')

    def __order_keys_in_dict(self, dictionary):
        return OrderedDict(sorted(dictionary.items()))

    def get_index(self):
        return self.__index

    def get_document_tokens(self):
        return self.__document_tokens
