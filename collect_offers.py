from beau import nice_display
from pymongo import MongoClient
from datetime import datetime, timedelta


count_of_days = 3
count_of_offers = 3

def collect():

	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']
	offers = db['offers']

	ofcount = offers.count()

	ads = adverts.find()	

	print('start')
	for ad in ads:
		if ofcount < count_of_offers:
			ad['is_offer'] = True
			offers.insert_one(ad)
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

	ads = adverts.find({},{'old':0, 'creation_date':{'$lt':border_date}})
	for ad in ads:
		ad['old'] = 1


def offers_correct():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	utc = datetime.utcnow()
	print(utc)

	border = timedelta(days=-count_of_days)
	border_date = utc + border

	offers.delete_many({'creation_date':{'$lt':border_date}})
			
def correct_by_data():
	adverts_correct()
	offers_correct()
	
	
		



@nice_display
def main():
	correct_by_data()
	collect()

if __name__ == '__main__':
	main()