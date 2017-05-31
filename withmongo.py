import pymongo
from pymongo import MongoClient
import datetime
import csv



def get_db(client):
	return client['lern']

def get_collection(client):
	db = get_db(client)
	return db['unicorns']

def check_data(obj, attr):
	try:
		result = obj[attr]
	except :
		result = 'none'
	return result

def write_csv(unicorn):
	with open('unicorns.csv', 'a') as f:
		writer = csv.writer(f)


		writer.writerow((
					check_data(unicorn, 'name'),
					check_data(unicorn, 'dob'),
					check_data(unicorn, 'loves'),
					check_data(unicorn, 'weight'),
					check_data(unicorn, 'gender'),
					check_data(unicorn, 'vampires'),
					))

def test():
	client = MongoClient('localhost', 27017)
	unicorns = get_collection(client)

	new_unicorn = {
		'name':'bridgit',
		'dob':datetime.datetime.utcnow(),
		'loves':['carrot'],
		'weight':'453',
		'gender':'f',
		'vampires':3
	}

	for unicorn in unicorns.find():
		write_csv(unicorn)




def main():
	print('begin')
	test()
	print('betti')



if __name__ == '__main__':
	main()