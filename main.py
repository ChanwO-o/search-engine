import requests
import sys
import os
import json
import fileIO
import bs4
import re
import math
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
		if int(k[0]) < 1:
			num_doc += 1
			y = []
			fol, fil = k.split('/')
			
			try:
				file = open(rootdir + '\\' + fol + "\\" + fil, 'r', encoding = 'utf-8')
				tokens , freq_ = tokenize(file)
				totaldocumentwords += len(tokens)
			except:
				continue
				
			finally:
				print('number of words in doc:', totaldocumentwords)
				print(fol + '/' + fil)

				for token in tokens:
					freq = freq_[token]
					tf = freq / totaldocumentwords
					if token not in result:
						result[token] = dict()
					if (fol, fil) not in result[token]:		# if document is not included in term's subdictionary
						result[token][(fol,fil)] = (freq, tf)	# store freq and tf values
		else:
			break;
			
			
	return (result, num_doc)

	
if __name__ == '__main__':
		index = None # the inverted index dictionary
		num_doc = None # number of documents
		
		if fileIO.index_file_exists():	# read prebuilt index from final.txt
			print('Reading index from file...')
			index = fileIO.read_index_from_file()
			num_doc = fileIO.read_num_doc_from_file()
			num_uniq = len(index)
		else:	# create a new index structure from scratch (takes approx. 20 minutes)
			print('Creating index...')
			index, num_doc = create_index()
			num_uniq = len(index)
			fileIO.write_index_to_file(index)
			size = os.path.getsize("final.txt")
			fileIO.write_num_to_file(num_doc)
			fileIO.write_result_to_file(num_uniq, size)
		
		# calculate tf-idf values for each term in completed index (and store them in each subdictionary)
		for k,v in index.items(): # k: term	v: term's subdictionary
			idf = 0
			if len(index[k]) != 0: # avoid divide by 0 error
				idf += math.log(num_doc / len(index[k]))
			print('Calculated idf as:', idf)
			
			# store idf value as first key in term's subdictionary, under the key 'idf'
			index['idf'] = idf
		
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
			
