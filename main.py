import requests
import sys
import os
import json
import fileIO
import bs4
import re
from multiprocessing import Pool
from collections import defaultdict

#rootdir = 'webpages'
rootdir = 'webpages\\WEBPAGES_RAW'

def tokenize(f):
	#pattern to ensure that word is only alphanumeric
	pattern = re.compile('[a-zA-Z]+')
	frequencies = defaultdict(int)
	tokens = []
	#going through all the lines in file
	for line in f:
		#making sure that all the characters in line are lowercase
		new_l = line.lower()
		
		#check which words fit the pattern and
		#using findall to combine into a list
		l = pattern.findall(new_l)

		#adding the elements of list l into actual list of tokens
		tokens.extend(l)

	#traversing through the list of tokens and adding to dictionary
	for i in tokens:
		#increment the word count by 1
		frequencies[i] += 1

	return tokens, frequencies
	
	
def search(index, searchterm) -> list:
	searchresult = index[searchterm]
	print("Number of URLs for '", searchterm, "':", len(searchresult))
	return searchresult

	
def create_index() -> (dict, int):

	result = dict()
	num_doc = 0


	with open(rootdir + '\\' + 'bookkeeping.json', 'r') as f:
		j_dict = json.load(f)

	for k, v in j_dict.items():
		tokens = []
		totaldocumentwords = 0
		freq_ = defaultdict()
		# if int(k[0]) < 1:
		num_doc += 1
		y = []
		fol, fil = k.split('/')
		# print(1)
		
		try:
			file = open(rootdir + '\\' + fol + "\\" + fil, 'r', encoding = 'utf-8')
			tokens , freq_ = tokenize(file)
			totaldocumentwords += len(tokens)
			# print(2)
		except:
			continue
			
		finally:
			print('number of words in doc:', totaldocumentwords)
			print(str(fol)+'/'+ str(fil))

			for token in tokens:
				freq = freq_[token]
				tfidf = freq / totaldocumentwords
				if token not in result:
					result[token] = dict()
					# print(3, end='')
				if (fol, fil) not in result[token]:
					# print(4, end='')
					result[token][(fol,fil)] = (freq, tfidf)	#.append((fol,fil, freq, tfidf))
			# print(5)
		# else:
			   # break;
			
			
	return (result, num_doc)

	
if __name__ == '__main__':
		index = None
		num_doc = None
		
		if fileIO.index_file_exists():
			print('Reading index from file...')
			index = fileIO.read_index_from_file()
			num_doc = fileIO.read_num_doc_from_file()
			num_uniq = len(index)
		else:
			print('Creating index...')
			index, num_doc = create_index()
			num_uniq = len(index)
			fileIO.write_index_to_file(index)
			size = os.path.getsize("final.txt")
			fileIO.write_num_to_file(num_doc)
			fileIO.write_result_to_file(num_uniq, size)
		
		
		print('Number of documents:', num_doc)
		
		print('Number of uniques:', num_uniq)
		print('Size of index on file:', os.path.getsize("final.txt"), 'bytes')

		with open(rootdir + '\\'+ 'bookkeeping.json', 'r') as f:
			j_dict = json.load(f)

		count = 0
		searchresult = search(index, 'mondego')
		mondego = open('mondego.txt', 'w')
		for i in searchresult:
			count += 1
			if (count < 21):
				mondego.write(j_dict[str(i[0]) + '/' + str(i[1])])
				print(j_dict[str(i[0]) + '/' + str(i[1])])
		mondego.close()

		count = 0;
		searchresult = search(index, 'informatics')
		in4 = open('informatics.txt', 'w')
		for i in searchresult:
			count += 1
			if (count < 21):
				in4.write(j_dict[str(i[0]) + '/' + str(i[1])])
				print(j_dict[str(i[0]) + '/' + str(i[1])])
		in4.close()

		count = 0;
		searchresult = search(index, 'irvine')
		irvine = open('irvine.txt', 'w')
		for i in searchresult:
			count += 1
			if (count < 21):
				irvine.write(j_dict[str(i[0]) + '/' + str(i[1])])
				print(j_dict[str(i[0]) + '/' + str(i[1])])
		irvine.close()
			
