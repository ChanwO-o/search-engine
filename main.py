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
import operator

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
	sortresult = dict()
	
	for k, v in searchresult.items():
		#print(v[1])
		if v[1] != '.': # catch error when float value is saved as '.'
			tf = float(v[1].strip())
			idf = float(searchresult['idf'].strip())
			tfidf = tf * idf
			v[1] = str(tfidf) # string-ify tfidf float and store back to list
		
	#print(searchresult)
	for k, v in sorted(searchresult.items(), key = lambda x : x[1][1], reverse = True): # sort dict by tf-idf from greatest to least
		sortresult[k] = v
	print("Number of URLs for '", searchterm, "':", len(searchresult))
	#print(sortresult)
	return sortresult

	
def create_index() -> (dict, int):

	result = dict()
	num_doc = 0


	with open(rootdir + '\\' + 'bookkeeping.json', 'r') as f:
		j_dict = json.load(f)

	for k, v in j_dict.items():
				tokens = []
				totaldocumentwords = 0
				freq_ = defaultdict()
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
								if k not in result[token]:	 # if document is not included in term's subdictionary
										result[token][k] = [freq, str(tf)]  # store freq and tf values
		
			
			
	return (result, num_doc)

	
if __name__ == '__main__':
		index = None # the inverted index dictionary
		num_doc = None # number of documents
		num_uniq = None
		
		if fileIO.index_file_exists():  # read prebuilt index from final.txt
			print('Reading index from file...')
			index = fileIO.read_index_from_file()
			num_doc = fileIO.read_num_doc_from_file()
			num_uniq = len(index)
			
		else:   # create a new index structure from scratch (takes approx. 20 minutes)
			print('Creating index...')
			index, num_doc = create_index()
			num_uniq = len(index)
			fileIO.write_index_to_file(index)
			size = os.path.getsize("final.json")
			fileIO.write_num_to_file(num_doc)
			fileIO.write_result_to_file(num_uniq, size)
		
		# calculate tf-idf values for each term in completed index (and store them in each subdictionary)
		for k,v in index.items(): # k: term v: term's subdictionary
			idf = 0
			if type(index[k]) == float:
				print(index[k])
			if len(index[k]) != 0: # avoid divide by 0 error
				idf += math.log(num_doc / len(index[k]))
			#print('Calculated idf as:', idf)
			
			# store idf value as first key in term's subdictionary, under the key 'idf'
			index[k]['idf'] = str(idf)
		
		print('Number of documents:', num_doc)
		
		print('Number of uniques:', num_uniq)
		print('Size of index on file:', os.path.getsize("final.json"), 'bytes')

		with open(rootdir + '\\'+ 'bookkeeping.json', 'r') as f:
			j_dict = json.load(f)

		count = 0
		searchresult = search(index, 'mondego')
		mondego = open('mondego.txt', 'w')
		for i in searchresult:
			count += 1 # return top 20 links
			if count < 21 and i != 'idf': # skip key 'idf' cuz that's a float
				
				mondego.write(j_dict[i])
				print(j_dict[i])
		mondego.close()

		count = 0;
		searchresult = search(index, 'informatics')
		in4 = open('informatics.txt', 'w')
		for i in searchresult:
			count += 1
			if (count < 21)and i != 'idf':
				in4.write(j_dict[i])
				print(j_dict[i])
		in4.close()

		count = 0;
		searchresult = search(index, 'irvine')
		irvine = open('irvine.txt', 'w')
		for i in searchresult:
			count += 1
			if (count < 21)and i != 'idf':
				irvine.write(j_dict[i])
				print(j_dict[i])
		irvine.close()
			
