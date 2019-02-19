import requests
import sys
import os

import readfile


def printResult(result):
	for k, v in result.items():
		print k, v
		
def printList(node):
	print node.data + ' -> ',
	if node.next != None:
		printList(node.next)
	else:
		print 'END'

if __name__ == '__main__':
	rootdir = 'testwebpages'
	
	result = {}
	
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			path = os.path.join(subdir, file)
			filename = path.split('\\')[-1]
			file = readfile.read_file(path)
			readfile.tokenize_file(result, file, filename)
	
	printResult(result)