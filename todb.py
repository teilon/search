# import pymongo
from pymongo import MongoClient

from bson.objectid import ObjectId

def start_mongo():
	client = MongoClient('localhost', 27017)

def add_to_mongo(data):
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']

	# if not adverts.find({advert_id:{$exists:data['advert_id']}}):
	advert = adverts.find_one({'advert_id':data['advert_id']})
	if advert is None:
		adverts.insert_one(data)
		return True
	return False





def test():
	pass
if __name__ == '__main__':
	test()