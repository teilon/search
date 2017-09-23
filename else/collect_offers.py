from beau import nice_display
from pymongo import MongoClient
from datetime import datetime, timedelta

import re


count_of_days = 3
count_of_offers = 3

def check_advert(**data):
	ad = data
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']	
	ofcount = offers.count()
	if ofcount < count_of_offers:
		offers.insert_one(ad)
		print('add')
		ofcount = offers.count()
	else:
		ofs = offers.find()
		
		ismax = False
		maximus = ofs[0]

		for of in ofs:				
			if of['price'] >= maximus['price']:
				maximus = of

			if not ismax:
				if ad['price'] < of['price']:
						ismax = True
		cont = True
		if ismax:
			ofs = offers.find()
			for of in ofs:
				if of['price'] == maximus['price'] and cont:
					offers.delete_one({'advert_id':of['advert_id']})
					offers.insert_one(ad)
					print('readd')
					cont = False


def collect():

	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']
	offers = db['offers']

	ofcount = offers.count()
	ads = adverts.find({'old':False})	

	print('start')
	for ad in ads:
		if ofcount < count_of_offers:
			# ad['is_offer'] = True
			offers.insert_one(ad)
			print('add')
			ofcount = offers.count()
		else:
			ofs = offers.find()
			
			ismax = False
			maximus = ofs[0]

			for of in ofs:				
				if of['price'] >= maximus['price']:
					maximus = of

				if not ismax:
					if ad['price'] < of['price']:
						ismax = True
			cont = True
			if ismax:
				ofs = offers.find()
				for of in ofs:
					if of['price'] == maximus['price'] and cont:
						offers.delete_one({'advert_id':of['advert_id']})
						offers.insert_one(ad)
						print('readd')
						cont = False
						# of = ad
						


		




def adverts_correct():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']
	utc = datetime.utcnow()
	print(utc)

	border = timedelta(days=-count_of_days)
	border_date = utc + border

	ads = adverts.find({'old':False, 'creation_date':{'$lt':border_date}})
	for ad in ads:
		adverts.find_one_and_update(
			{'_id':ad['_id']}, 
			{'$set':{'old':True}}
		)
		


def offers_correct():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	utc = datetime.utcnow()
	
	border = timedelta(days=-count_of_days)
	border_date = utc + border

	offers.delete_many({'creation_date':{'$lt':border_date}})
			
def correct_by_data():
	adverts_correct()
	offers_correct()	

def for_test():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']
	utc = datetime.utcnow()
	print('utc: {}'.format(utc))

	ads = adverts.find()

	for ad in ads:
		if re.search('\d+', ad['publication_date']).group(0) == '16':
			border = timedelta(days=-3)
			border_date = utc + border			
			adverts.find_one_and_update(
				{'_id':ad['_id']}, 
				{'$set':{'creation_date':border_date}}
			)
		if re.search('\d+', ad['publication_date']).group(0) == '15':
			border = timedelta(days=-4)	
			border_date = utc + border
			adverts.find_one_and_update(
				{'_id':ad['_id']}, 
				{'$set':{'creation_date':border_date}}
			)
		if re.search('\d+', ad['publication_date']).group(0) == '14':
			border = timedelta(days=-5)	
			border_date = utc + border
			adverts.find_one_and_update(
				{'_id':ad['_id']}, 
				{'$set':{'creation_date':border_date}}
			)
		if re.search('\d+', ad['publication_date']).group(0) == '13':
			border = timedelta(days=-6)	
			border_date = utc + border
			adverts.find_one_and_update(
				{'_id':ad['_id']}, 
				{'$set':{'creation_date':border_date}}
			)
		if re.search('\d+', ad['publication_date']).group(0) == '12':
			border = timedelta(days=-7)	
			border_date = utc + border
			adverts.find_one_and_update(
				{'_id':ad['_id']}, 
				{'$set':{'creation_date':border_date}}
			)
		print('border_date: {}'.format(border_date))
	
	
	
		



@nice_display
def main():
	correct_by_data()
	collect()

if __name__ == '__main__':
	main()
	# for_test()