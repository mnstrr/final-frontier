import numpy as np

class Pagerank:
    def __init__(self , urls ):
        self.__urls = urls
        print(len(self.__urls))

    def createMatix(self):
        matrix = np.zeros((len(self.__urls), len(self.__urls)))
        # print(matrix)
        for page in range(1, len(self.__urls)):
            # for page in self.__seedList:
            for linkedPage in range(1, len(self.__urls)):
                # for linkedPage in self.__visitedList:
                if page != self.__urls:
                    matrix[page, linkedPage] = 1
                # elif page == self.__seedList:
                    # go to next row
                else:
                    matrix[page, linkedPage] = 0
        print(matrix)
        # create matrix of len(self.__visitedList)
        # a = np.matrix('1 2; 3 4')
        # print(a)