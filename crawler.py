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
        self.__tokens = {}
        self.__document_soups = self.__crawl()

    def __crawl(self):
        document_soups = {}
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

                document_soups[key] = soup

                for internal_url in soup.find_all('a'):
                    current_internal_url = self.__base_url + internal_url.get('href')
                    value = self.__find_doc_title(current_internal_url, '/', '.')
                    self.__internal_url_structure[key].append(value)
                    if current_internal_url not in self.__visited:
                        self.__frontier.append(current_internal_url)
                        self.__visited.append(current_internal_url)

        self.__tokens = self.__sort_keys_in_dict(self.__tokens)
        self.__internal_url_structure = self.__sort_values_in_dict(self.__sort_keys_in_dict(self.__internal_url_structure))

        self.__print_internal_url_structure()
        return document_soups

    def __sort_keys_in_dict(self, dict):
        return OrderedDict(sorted(dict.items()))

    def __sort_values_in_dict(self, dict):
        for key in dict:
            dict[key] = sorted(dict[key])
        return dict

    def __find_doc_title(self, s, first, last):
        start = s.rfind(first) + len(first)
        end = s.rfind(last)
        return s[start:end]

    def __print_internal_url_structure(self):
        print('# INTERNAL URL STRUCTURE:')
        for key, value in self.__internal_url_structure.items():
            print(key + ': ' + ','.join(value))
        print('--------------------')


    def get_internal_url_structure(self):
        return self.__internal_url_structure

    def get_document_soups(self):
        return self.__document_soups
