# import csv

from withmongo import add_to_mongo

# from checkdata import check

def write_csv(data):
	with open('kolesa.csv', 'a') as f:
		writer = csv.writer(f)

		output = []


		keys = sorted(list(data.keys()))
		for i in keys:
			output.append(data[i])		

		writer.writerow(output)



		# writer.writerow((
		# 			data['base_title'],
		# 			data['base_data_id'],
		# 			data['base_price'],
		# 			data['base_year'],
		# 			data['base_region'],
		# 			data['base_date'],
		# 			data['base_link']
		# 			))

def write_console(data):
	keys = sorted(list(data.keys()))
	for i in keys:
		print('{}: {}'.format(i, data[i]))


	# print('title: {}[{}]\t\tprice: {}\t\tyear: {}\t\tday: {}'.format(
	# 	data['title'], 
	# 	data['data_id'], 
	# 	data['price'], 
	# 	data['year'],
	# 	data['date']
	# 	))

def write_db(data):

	pass

	# isadd = add_to_mongo(data)

	# if isadd:
	# 	print('saved')
	# else:
	# 	print('NOT saved')

	# if isadd:
	# 	check(**data)
	# 	return
