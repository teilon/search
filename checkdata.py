from beau import nice_display
from pymongo import MongoClient

from datetime import datetime

# выводить результирующую выборку как
# count == 3
# где общее колличество может быть больше трех,
# но не по показателям 

count_of_days = 3
count_of_offers = 3


def check_by_price(**data):
	advert = data

	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	# set critical level
	ismutated = False
	isbetter = False
	
	# if isbetter or count < count_of_offers:
	count = offers.count()
	if count < count_of_offers:	
		offer = advert
		# offer['crit_level'] = count
		offers.insert_one(offer)
		# ismutated = True

	ofs = offers.find()
	for of in ofs:
		if of['price'] > advert['price']:
			offer = advert
			# offer['crit_level'] = -1
			# offers.insert_one(offer)
			no = max(list['price'])
			ofs.remove(no)
			offers.insert_one(offer)

def check_by_date():

	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	current_date = datetime.utcnow()

	for of in offers.find():
		if current_date - of['creation_date'] > count_of_days:
			pass

def get_new_offer():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']

	# current_date = datetime.utcnow()
	# true_ads = adverts.find({'old':{'$ne':'1'}})

	# for ad in true_ads:
	# 	if current_date - ad['creation_date'] > count_of_days:
	# 		ad['old'] = '1'


	# return min(true_ads.find({'$min':{'price':'inf'}}))
	# return true_ads({'$min':{'price':'inf'}})
	return adverts.find().min({'price':'2600000'})






	# if ismutated:
	# 	if count >= count_of_offers:
	# 		no = None
	# 		for of in offers.find():
	# 			if no is None:
	# 				no = of
	# 			if no['price'] < of['price']:
	# 				no = of
	# 		offers.remove(no)
		


# -------------------------




@nice_display
def test():

	data1 = {
		'title':'Totota Camry',
		'price':'3900000',
		'publication_date':'13',
		'link':'link',
		'advert_id':'36497165'
	}
	data2 = {
		'title':'Totota Camry',
		'price':'3800000',
		'publication_date':'13',
		'link':'link',
		'advert_id':'36044475'
	}
	data3 = {
		'title':'Totota Camry',
		'price':'4000000',
		'publication_date':'13',
		'link':'link',
		'advert_id':'36045175'
	}
	data4 = {
		'title':'Totota Camry',
		'price':'3750000',
		'publication_date':'13',
		'link':'link',
		'advert_id':'36074592'
	}
	data5 = {
		'title':'Totota Camry',
		'price':'3200000',
		'publication_date':'13',
		'link':'link',
		'advert_id':'36074592'
	}
	# check(**data1)
	# check(**data3)
	# check(**data2)
	# check(**data4)
	check(**data5)

def test_two():
	print(get_new_offer())
	# check_by_date();



if __name__ == '__main__':
	test_two()