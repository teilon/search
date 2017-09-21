from pymongo import MongoClient
import re
from toemail import send
from time import sleep

def get_mongo_connection(HOST = '127.0.0.1', PORT = 27017):

	conn = MongoClient(host=HOST, port=PORT)
	try:
		conn.admin.command('ismaster')
	except ConnectionFailure as msg:
		print('Could not connect to server: {}'.format(str(msg)))
		return None

	return conn

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


def collect_data():
	config = read_config()
	conn = get_mongo_connection(HOST = config['host'])
	if conn is None:
		return

	db = conn['kolesa']
	collect = db['collect']
	

	message = 'best prices\n'
	for c in collect.find().sort('value').limit(3):		
		message += 'auto#{} : {}\n'.format(c['_id']['title'], c['value']['price'])

	# print(message)
	send(message)



def main():
	collect_data()

	sleep(28800)

if __name__ == '__main__':
	main()