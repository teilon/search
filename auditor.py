from pymongo import MongoClient
from datetime import datetime, timedelta

from bson.code import Code


def mongodb_conn(HOST = '127.0.0.1', PORT = 27017):

	conn = MongoClient(host=HOST, port=PORT)
	try:
		conn.admin.command('ismaster')
	except ConnectionFailure as msg:
		print('Could not connect to server: {}'.format(str(msg)))
		return None

	return conn

def get_notolds():
'''
get not olds
correct by date
set new old
return dict notolds
'''
	config = read_config()
	conn = mongodb_conn(HOST = config['host'])
	if conn is None:
		return

	db = conn['kolesa']
	adverts = db['adverts']

	# advert = adverts.find_one({'advert_id':data['advert_id']})	
	# if advert is None:
	# 	adverts.insert_one(data)

	threedays = timedelta(days=3)
	result = adverts.update_many({'old':{'$ne':True}, 'creation_date':{'$lt':datetime.utcnow() - threedays}}, {'$set': {'old':True}})

	# ads = adverts.find({'old':False})

	mapper = Code("""
		function(){
			this
		}
		""")




def get_best_by_price(notolds):
'''
get best adverts by price
return dict bests
'''
	pass


def read_config():

	host_pattern = '^host:[\d.]+$'
	global HOST

	with open('mongo.conf', 'r') as f:
		for line in f:
			h = re.match(host_pattern, line)
			if h is not None:
				HOST = h.group(0).split(':')[1]
				break

def read_config():

	host_pattern = '^host:[\d.]+$'
	host = 127.0.0.1

	with open('mongo.conf', 'r') as f:
		for line in f:
			h = re.match(host_pattern, line)
			if h is not None:
				host = h.group(0).split(':')[1]
				break

	result = {
		'host':host
	}
	return result