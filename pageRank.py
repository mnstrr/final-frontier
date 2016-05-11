from collections import OrderedDict

class PageRank:
    def __init__(self, inURLs):
        self.__inURLs = inURLs
        self.__damping = 0.95
        self.__teleport = 1 - self.__damping
        self._delta = 0.04
        self.__pagecount = len(self.__inURLs)
        self.__transitionPorpabilities = self.__calculateTransition()

    def __calculateTransition(self):
        transitions = {}

        for url in self.__inURLs:
            outlinkCount = len(self.__inURLs[url])
            transitions[url] = []
            if outlinkCount > 0:
                for outlink in self.__inURLs[url]:
                    transitions[url].append(
                        [(outlink), (1.0 / outlinkCount) * self.__damping + (self.__teleport / self.__pagecount)])
            else:
                transitions[url].append(1 / self.__pagecount)
        transitions = self.__sortDictionary(transitions)
        return transitions

    def __sortDictionary(self, dict):
        sorteddict = OrderedDict(sorted(dict.items()))
        return sorteddict

    def printTransitions(self):
        for key, values in self.__transitionPorpabilities.items():
            print(key)
            print(values)
