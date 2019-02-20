from pymongo import MongoClient

client, database, collection = 0, 0, 0

def createDatabase():
	global client, database, collection
	client = MongoClient()
	database = client["worddatabase"]
	collection = database["wordcollection"]
	
def insertToDatabase(value):
	global collection
	x = collection.insert_one(value)
	
def insertNewWordToDatabase(word, index):
	global collection
	toadd = {word : [index]}
	collection.insert_one(toadd)
	
def insertExistingWordToDatabase(word, index):
	global collection
	for x in list(collection.find({"newword"})):
		print(x)
	# indexListOfTheWord = cursor[word]
	# print(indexListOfTheWord)