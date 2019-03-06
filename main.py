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
import search
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QLineEdit

#rootdir = 'webpages'
rootdir = 'webpages\\WEBPAGES_RAW'
searchresults = None

def gui():
	app = QApplication([])
	
	# gui widgets
	window = QWidget()
	textbox = QLineEdit()
	textbox.move(20, 20)
	textbox.resize(280,40)
	searchbutton = QPushButton('Search')
	searchbutton.clicked.connect(onClickSearch)
	global searchresults
	searchresults = QLabel('')
	
	# define layout
	layout = QVBoxLayout()
	layout.addWidget(textbox)
	layout.addWidget(searchbutton)
	layout.addWidget(searchresults)
	
	# set layout to window
	window.setLayout(layout)
	window.setGeometry(500, 500, 500, 500)
	window.show()
	app.exec_()
	
def onClickSearch():
	global searchresults
	
	# get search results
	search.search()
	# set searchresults lable as results
	searchresults.setText('search button clicked')
	
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
			index, num_doc = search.create_index()
			num_uniq = len(index)
			fileIO.write_index_to_file(index)
			size = os.path.getsize("final.json")
			fileIO.write_num_to_file(num_doc)
			fileIO.write_result_to_file(num_uniq, size)
		
			# calculate tf-idf values for each term in completed index (and store them in each subdictionary)
			# ONLY CALCULATE IDF VALUES RIGHT AFTER INDEX CREATION; reading from final.json may already have idf values
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

		# start GUI
		gui()

		
'''
user_input = input('Enter a word (q to quit):')
while(user_input != 'q'):
	count = 0
	searchresult = []
	try:
		usr_sp = user_input.split(' ')
		if(len(usr_sp) > 1):
			num = 0
			for i in usr_sp:
				print(i)
				if (num == 0):
					searchresult = search.search(index, i)
				else:
					searchresult = list(set(searchresult) & set(search.search(index, i)))
				num = num + 1
		else:
			searchresult = search.search(index, user_input)
		print("Number of URLs for '", user_input, "':", len(searchresult))
		for i in searchresult:
			count += 1 # return top 20 links
			if count < 21 and i != 'idf': # skip key 'idf' cuz that's a float
				print(j_dict[i])
	except:
		print("Cannot find word in indexer. Please try again")
	user_input = input('Enter a word (q to quit):')
'''