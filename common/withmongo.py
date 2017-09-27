from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import re

def get_mongo_connection(host='127.0.0.1',port=27017):

	conn = MongoClient(host=host, port=port)
	try:
		conn.admin.command('ismaster')
	except ConnectionFailure as msg:
		print('Could not connect to server: {}'.format(str(msg)))
		return None

	return conn

def read_config():

	host_pattern = '^host:[\d.]+$'
	host = '127.0.0.1'

	with open('common/mongo_conf', 'r') as f:
		for line in f:
			h = re.match(host_pattern, line)
			if h is not None:
				host = h.group(0).split(':')[1]
				break

	result = {
		'host':host
	}
	return result
						 

def save_to_mongodb(data, host='127.0.0.1'):

	conn = get_mongo_connection(host=host)
	if conn is None:
		return

	adverts = conn.kolesa.adverts

	advert = adverts.find_one({'advert_id':data['advert_id']})
	if advert is None:

		data.update({'creation_date':datetime.utcnow(), 'old':False})

		adverts.insert_one(data)

def collect_data():
	config = read_config()
	conn = get_mongo_connection(host=config['host'])
	if conn is None:
		return
	
	collect = conn.kolesa.collect;
	
	message = 'best prices\n'
	for c in collect.find().sort('value').limit(3):		
		message += 'auto#{} : {}\n'.format(c['_id']['title'], c['value']['price'])

	return message