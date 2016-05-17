# imports
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString
from collections import OrderedDict
import urllib.request
import pdb


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

                #for string in soup.stripped_strings:
                #    print(repr(string))

                #print(soup.body.a.previous_sibling)

                #print(soup.find_all(self.is_link()))

                #print(soup.body.find_all(text=True))

                #for e in soup.findAll('br'):
                #    e.extract()

                unwanted_tags = ['br']
                for tag in unwanted_tags:
                    for match in soup.find_all(tag):
                        match.unwrap()

                for text in soup.body.find_all(text=True):
                    if (text.parent.name != "a"):

                        split_list = text.split()
                        if split_list:
                            print(text.split())


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
