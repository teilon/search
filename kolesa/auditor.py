from pymongo import MongoClient
from datetime import datetime, timedelta
import re
from bson.code import Code

from common.beau import nice_display

def get_mongo_connection(HOST = '127.0.0.1', PORT = 27017):

	conn = MongoClient(host=HOST, port=PORT)
	try:
		conn.admin.command('ismaster')
	except ConnectionFailure as msg:
		print('Could not connect to server: {}'.format(str(msg)))
		return None

	return conn

@nice_display
def collect():
	config = read_config()
	conn = get_mongo_connection(HOST = config['host'])
	if conn is None:
		return

	db = conn['kolesa']
	adverts = db['adverts']

	threedays = timedelta(days=3)
	result = adverts.update_many({'old':{'$ne':True}, 'creation_date':{'$lt':datetime.utcnow() - threedays}}, {'$set': {'old':True}})

	mapper = Code("""
		function(){
			var key = {
				title: this.advert_id,
				price: this.price
			};
			emit(key, {price: this.price});
		}
		""")

	reducer = Code("""
		function(key, values){
			var result = 0;
			values.forEach(function(value){
				result += values['price']
			})
			return {price: result}
		}
		""")

	adverts.map_reduce(mapper, reducer, 'collect')

def read_config():

	host_pattern = '^host:[\d.]+$'
	host = '127.0.0.1'

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

# from beau import nice_display
# @nice_display
# def main():
# 	get_notolds()

# if __name__ == '__main__':
# 	main()