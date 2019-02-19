import re
from listnode import ListNode
import bs4


def read_file(filepath):
	return open(filepath) # default mode is read
	
def tokenize_file(result, file, fileindex):
	for line in file: # O(n)
		soup = bs4.BeautifulSoup(line, 'html.parser')
		for child in soup:
			if isinstance(child, bs4.Tag):
				line = re.sub('[^a-zA-Z0-9]', ' ', child.text.lower())
				for word in line.split():
					if word in result:
						# addToIndexer(result, word, fileindex)
						if fileindex not in result[word]:
							result[word].append(fileindex)
					else:
						result[word] = [fileindex]
	return result
	
def addToIndexer(result, word, fileindex):
	temp = ListNode(fileindex)
	temp.next = result[word]
	result[word] = temp