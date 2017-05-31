import csv

def write_csv(data):
	with open('kolesa.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow((
					data['title'],
					data['data_id'],
					data['price'],
					data['year'],
					data['region'],
					data['date'],
					data['link']
					))

def write_console(data):
	print('title: {}[{}]\t\tprice: {}\t\tyear: {}\t\tday: {}'.format(
		data['title'], 
		data['data_id'], 
		data['price'], 
		data['year'],
		data['date']
		))