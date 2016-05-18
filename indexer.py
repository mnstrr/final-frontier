import re

class Indexer:
    def __init__(self, soups):
        self.__soups = soups
        self.__each_soup()
        self.__count_in_documents()
        self.__tokens = []

    def __each_soup(self):
        for key, value in self.__soups.items():
            self.__tokenize(value)

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

        print(document_tokens)
        self.__tokens = document_tokens
        return document_tokens

    def __remove_tags(self, unwanted_tags, soup):
        for tag in unwanted_tags:
            for match in soup.find_all(tag):
                match.unwrap()
        return soup

    def __remove_interpunction(self, text):
        text_neu = re.sub(r'[\,\.]', '', text)
        return text_neu

    def __normalize_tokens(self, token_list):
        token_list = [element.lower() for element in token_list]
        return token_list

    #(advance, df:1) -> [('d04', 1)]
    def __count_in_documents(self):
        #token dictionary
        document_tokens = {}
        print(self.__tokens)

    def __count_tokens(self):
        print(self.__tokens)
        #for key, value in self.__soups.items():
            #self.__tokenize(value)