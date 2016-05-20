import re

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


