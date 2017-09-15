from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import re
# from toemail import send

HOST = '127.0.0.1'
PORT = 27017

def mongodb_conn():

	conn = MongoClient(host=HOST, port=PORT)
	try:
		conn.admin.command('ismaster')
	except ConnectionFailure as msg:
		print('Could not connect to server: {}'.format(str(msg)))
		return None

	return conn
						 

def save_to_mongodb(data):

	conn = mongodb_conn()
	if conn is None:
		return	

	print('its all right')

	db = conn['kolesa']
	adverts = db['adverts']

	advert = adverts.find_one({'advert_id':data['advert_id']})
	if advert is None:
		adverts.insert_one(data)	

def read_config():

	host_pattern = '^host:[\d.]+$'
	global HOST

	with open('mongo.conf', 'r') as f:
		for line in f:
			h = re.match(host_pattern, line)
			if h is not None:
				HOST = h.group(0).split(':')[1]
				break