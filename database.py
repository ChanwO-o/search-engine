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