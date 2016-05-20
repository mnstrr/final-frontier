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
        self.__print_tokens()
        self.__count_occurrences()

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

    def __count_occurrences(self):
        occurrences = {}

        # iterate over dict {doc_id: [tokens]}
        for doc_id, tokens in self.__document_tokens.items():
            # iterate over tokens in one document
            for i, token in enumerate(tokens):

                # if token is already existing:
                if token in occurrences:
                    # get dict
                    doc_occurrences = occurrences[token]
                else:
                    # make new dict
                    doc_occurrences = {}

                if doc_id in doc_occurrences:
                    doc_occurrences[doc_id] += 1
                else:
                    doc_occurrences[doc_id] = 1

                occurrences[token] = doc_occurrences

        ordered_occurrences = OrderedDict(sorted(occurrences.items()))

        doc_freq = {}
        for key, value in ordered_occurrences.items():
            doc_freq[key] = len(value)

        ordered_doc_freq = OrderedDict(sorted(doc_freq.items()))

        self.__print_dictionary(ordered_occurrences)
        self.__print_dictionary(ordered_doc_freq)

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


