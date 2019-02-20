from pymongo import MongoClient


def createDatabase():
	client = MongoClient()
	database = client["worddatabase"]
	collection = database["wordcollection"]
	
	mydict = { "Roman": [1, 2, 3, 4] }
	x = collection.insert_one(mydict)