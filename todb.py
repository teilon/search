# import pymongo
from pymongo import MongoClient

def start_mongo():
	client = MongoClient('localhost', 27017)

def add_to_mongo(data):
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']

	# if not adverts.find({advert_id:{$exists:data['advert_id']}}):
	adverts.insert_one(data)