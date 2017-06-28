from pymongo import MongoClient

def add_to_mongo(data):
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	adverts = db['adverts']

	advert = adverts.find_one({'advert_id':data['advert_id']})
	if advert is None:
		adverts.insert_one(data)
		return True
	return False


from toemail import send
def test():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	offers_ = offers.find({})
	messages = '';

	for of in offers_:
		message = '\ntitle:\t{}\n\tadvert:\t{}\n\tdate:\t{}\n\tprice:\t{}\n\tlink:\t{}\n'.format(
			of['title'], 
			of['advert_id'], 
			of['publication_date'],
			of['price'],
			of['link'])
		print(message)
		messages += message

	send(messages)




if __name__ == '__main__':
	test()