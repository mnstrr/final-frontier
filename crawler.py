# imports
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import urllib.request
import re

class Crawler:
    def __init__(self, seed_urls, base_url):
        self.__seed_urls = seed_urls
        self.__base_url = base_url
        self.__frontier = []
        self.__visited = []
        self.__internal_url_structure = {}
        self.__crawl()

    def __crawl(self):
        for url in self.__seed_urls:
            self.__frontier.append(self.__base_url + url)
            while len(self.__frontier) > 0:
                current_url = self.__frontier[0]
                page = urllib.request.urlopen(current_url)
                soup = bs(page.read(), "html.parser")
                self.__visited.append(current_url)
                self.__frontier.pop(0)
                key = self.__find_doc_title(current_url, '/', '.')
                self.__internal_url_structure[key] = []

                self.__tokenize(soup)

                for internal_url in soup.find_all('a'):
                    current_internal_url = self.__base_url + internal_url.get('href')
                    value = self.__find_doc_title(current_internal_url, '/', '.')
                    self.__internal_url_structure[key].append(value)
                    if current_internal_url not in self.__visited:
                        self.__frontier.append(current_internal_url)
                        self.__visited.append(current_internal_url)

        self.__internal_url_structure = self.__sort_dictionary(self.__internal_url_structure)

    def __sort_dictionary(self, dict):
        sorted_dict = OrderedDict(sorted(dict.items()))
        for key in sorted_dict:
            sorted_dict[key] = sorted(sorted_dict[key])
        return sorted_dict

    def __find_doc_title(self, s, first, last):
        start = s.rfind(first) + len(first)
        end = s.rfind(last)
        return s[start:end]

    def get_internal_url_structure(self):
        return self.__internal_url_structure

    def print_internal_url_structure(self):
        print('# INTERNAL URL STRUCTURE:')
        for key, value in self.__internal_url_structure.items():
            print(key+':' + ','.join(value))
        print('--------------------')


    def __tokenize(self, soup):
        document_tokens = []

        # removes all line breaks
        strained_soup = self.__remove_tags(["br"], soup)

        # only iterate over text content, should be obvious, but what everest
        for text in strained_soup.body.find_all(text=True):

            # ignore all links
            if (text.parent.name != "a"):

                # removes interpunction, in this case "." and ","
                text = self.__remove_interpunction(str(text))

                # splits into separate words
                token_list = text.split()

                # if list not empty
                if token_list:

                    #concatenate all lists
                    document_tokens.extend(token_list)

        print(document_tokens)
        return document_tokens

    def __remove_tags(self, unwanted_tags, soup):
        for tag in unwanted_tags:
            for match in soup.find_all(tag):
                match.unwrap()
        return soup

    def __remove_interpunction(self, text):
        text_neu = re.sub(r'[\,\.]', '', text)
        return text_neu