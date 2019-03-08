import json
import re
from collections import defaultdict
import traceback

rootdir = 'webpages\\WEBPAGES_RAW'
STOPLIST = ['a', 'as', 'the', 'is', 'and', 'it', 'at', 'by', 'that', 'can', 'did', 'do', 'of', 'on', 'for', 'had', 'has', 'will', 'to', 'so']


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
	
	
def getSearchResults(index, user_input, j_dict):
	count = 0
	searchresults = []
	displayedresults = []
	try:
		tokens = user_input.split()
		if(len(tokens) > 1):
			num = 0
			for token in tokens:
				print(token)
				if len(token) >= 15:	# filter if token is ridiculously long word
					continue
				if token in STOPLIST:	# filter if token is a very common word
					continue
				if (num == 0):
					searchresults = search(index, token)
				else:
					searchresults = list(set(searchresults) | set(search(index, token)))
				num = num + 1
		else:
			searchresults = search(index, user_input)
		print("Number of URLs for '", user_input, "':", len(searchresults))
		for searchresult in searchresults:
			count += 1 # return top 20 links
			if count < 21 and searchresult != 'idf': # skip key 'idf' cuz that's a float
				displayedresults.append(j_dict[searchresult])
		if len(displayedresults) == 0:
			displayedresults.append('No results!')
	except:
		traceback.print_exc()
		displayedresults.append("Cannot find word in indexer. Please try again")
	return displayedresults
	
	
def search(index, searchterm) -> list:
	if searchterm not in index: # handle no results error
		return dict()
	searchresult = index[searchterm]
	sortresult = dict()
	#print(searchterm)
	#print(searchresult)
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
				file = open(rootdir + '\\' + fol + "\\" + fil, 'r', encoding = 'utf-8') # bs4?
				tokens , freq_ = tokenize(file)
				totaldocumentwords += len(tokens)
		except:
				continue
				
		finally:
				#print('number of words in doc:', totaldocumentwords)
				#print(fol + '/' + fil)

				for token in tokens:
						freq = freq_[token]
						tf = freq / totaldocumentwords
						if token not in result:
								result[token] = dict()
						if k not in result[token]:       # if document is not included in term's subdictionary
								result[token][k] = [freq, str(tf)]  # store freq and tf values

	
			
	return (result, num_doc)