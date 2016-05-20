
class Search:
    def __init__(self, dict_dfs, dict_occur):
        self.__occurrences = dict_occur
        self.__doc_freq = dict_dfs

        self.__print_occurrences()
        self.__print_dictionary(self.__doc_freq)

    def __print_dictionary(self, dictionary):
        for key, value in dictionary.items():
            if hasattr(value, '__iter__'):
                print(key + ': ' + ', '.join(value))
            else:
                print(key + ": " + str(value))
        print('--------------------')

    def __print_occurrences(self):
        for key, value in self.__occurrences.items():
            print(key + ": " + str(value))
        print('--------------------')
