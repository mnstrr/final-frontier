import urllib
from sets import Set
from bs4 import BeautifulSoup as bs
import collections

baseURL = 'http://home.htw-berlin.de/~iclassen/cmst/ue1/'

seedList = ['http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d01.html','http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d06.html','http://home.htw-berlin.de/~iclassen/cmst/ue1/docs/d08.html']
frontierList = []
visitedList = set()

def main ():
	for url in seedList:

		frontierList.append(url)

		while len(frontierList) > 0:
			currentURL = frontierList[0]
			page = urllib.urlopen(currentURL)
			soup = bs(page.read(), "html.parser")

			visitedList.add(currentURL)
			frontierList.pop()[0]

			for link in soup.find_all('a'):
				url1 = baseURL + link.get('href')
				if url1 not in visitedList:
					frontierList.append(url1)
					visitedList.add(url1)

	for ele in visitedList:
		print ele

main()
#commentt