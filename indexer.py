import re
from collections import OrderedDict

class Indexer:
    def __init__(self, document_soups):
        self.__document_soups = document_soups
        self.__document_tokens = {}
        self.__STOPWORDS = [
            'd01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
            'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
            'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
            'that', 'the', 'this', 'to', 'we'
        ]
        self.__each_soup()
        self.__indexCount = {}
        self.__print_tokens()
        self.__index = self.__create_index()
        #self.__term_freqs = self.__count_term_freqs()
        #self.__doc_freqs = self.__count_doc_freqs(self.__term_freqs)
        #self.__print_term_freqs()
        #self.__print_dictionary(self.__doc_freqs)

    def __each_soup(self):
        for doc_ID, soup in self.__document_soups.items():
            self.__document_tokens[doc_ID] = self.__tokenize(soup)

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

    def __count_term_freqs(self, index):
        term_freqs = {}

        # iterate over dict {doc_id: [tokens]}
        for doc_id, tokens in self.__document_tokens.items():
            # iterate over tokens in one document
            for i, token in enumerate(tokens):

                # if token is already existing:
                if token in term_freqs:
                    # get dict
                    doc_occurrences = term_freqs[token]
                else:
                    # make new dict
                    doc_occurrences = {}

                if doc_id in doc_occurrences:
                    doc_occurrences[doc_id] += 1
                else:
                    doc_occurrences[doc_id] = 1

                #term_freqs[token] = doc_occurrences
                index[token] = [doc_occurrences]

        #ordered_occurrences = self.__get_ordered_dict(term_freqs)
        #return ordered_occurrences
        return index

    def __count_doc_freqs(self, term_freqs):
        doc_freq = {}

        for token, doc_occurrences in term_freqs.items():
            doc_freq[token] = len(doc_occurrences)

        #ordered_doc_freq = self.__get_ordered_dict(doc_freq)
        #return ordered_doc_freq
        return doc_freq

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
        self.__print_dictionary(self.__document_tokens)

    def __print_dictionary(self, dictionary):
        for key, value in dictionary.items():
            if hasattr(value, '__iter__'):
                print(key + ': ' + ', '.join(value))
            else:
                print(key + ": " + str(value))
        print('--------------------')

    def __print_term_freqs(self):
        for key, value in self.__term_freqs.items():
            print(key + ": " + str(value))
        print('--------------------')


    def __get_ordered_dict(self, dictionary):
        return OrderedDict(sorted(dictionary.items()))

    def get_df_dict(self):
        return self.__doc_freqs

    def get_occurrences_dict(self):
        return self.__term_freqs


    def __create_index(self):
        index = {}
        index = self.__count_term_freqs(index)
        #doc_freqs = self.__count_doc_freqs(term_freqs)
        print('')
