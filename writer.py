import csv

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
	print('title: {}[{}]\t\tprice: {}\t\tyear: {}\t\tday: {}'.format(
		data['title'], 
		data['data_id'], 
		data['price'], 
		data['year'],
		data['date']
		))