from beau import nice_display
from pymongo import MongoClient

# выводить результирующую выборку как
# count == 3
# где общее колличество может быть больше трех,
# но не по показателям 

def check(**data):
	advert = data

	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	ismutated = False
	isbetter = False

	count = offers.count()

	for of in offers.find():
		if advert['price'] < of['price']:
			isbetter = True
	
	if isbetter or count < 3:
		offers.insert_one(advert)
		ismutated = True

	if ismutated:
		if count >= 3:
			no = None
			for of in offers.find():
				if no is None:
					no = of
				if no['price'] < of['price']:
					no = of
			offers.remove(no)
		


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




if __name__ == '__main__':
	test()