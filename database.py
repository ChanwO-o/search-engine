from pymongo import MongoClient


def createDatabase():
	client = MongoClient()
	mydb = client["worddatabase"]
	print(client.list_database_names())