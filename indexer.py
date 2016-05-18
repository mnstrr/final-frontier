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
        self.__indexCount = {}
        self.__print_tokens()
        self.__count_in_document()

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







    def __count_in_document(self):
        token_list = {}
        # iterate over dict with all tokens
        for key, value in self.__document_tokens.items():
            # iterate over tokens in one document
            for token, token_val in enumerate(value):

                # if token is already existing:
                if token_val in token_list:
                    # get list:
                    valu = token_list[token_val]
                    # in same document:
                    if valu[1][0] == key:
                        valu[1] = (key, valu[1][1]+1)
                    # in other document:
                    else:
                        for i in range(1, len(valu)):
                            print('valu -1 ')
                            print(valu[-1])
                            print('len '+str(len(valu)))
                            if valu[i][0] == key:
                                # if other document is existing
                                valu[i] = (key, valu[i][1] + 1)
                                valu.pop(i + 1)
                                #break
                            elif valu[-1]:
                                print('elif, key:')
                                print(key)
                                print(valu)
                                if valu[i][0] == key:
                                    valu[i] = (key, valu[i][1] + 1)
                                    #break
                                elif valu[i][0] != key:
                                    # if other document is not existing yet
                                    valu.append((key, 1))
                                    valu[0] += 1  # increase df
                                    i += 1
                                    print('after')
                                    print(valu)


                else:
                    # first entry [df, tuple(page, ocurance in doc)]
                    token_list[token_val] = [1, (key, 1)]

        self.__print_tokens2(token_list)
        print('--------------------')






    def __count_tokens(self):
        print(self.__tokens)
        # for key, value in self.__soups.items():
            #self.__tokenize(value)

    def __print_tokens2(self, tokenlist):
        print('# TOKEN-LIST:')
        for key, value in tokenlist.items():
            print(str(key) + ': ')
            for idx, val in enumerate(value):
                if idx == 0:
                    print('df: ' + str(val))
            print(value)
        print('--------------------')

    def __print_tokens(self):
        print('# TOKENS:')
        for key, value in self.__document_tokens.items():
            print(key + ': ' + ', '.join(value))
        print('--------------------')


