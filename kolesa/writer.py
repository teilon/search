from common.withmongo import save_to_mongodb, read_config
# import csv

def write_csv(data):
	with open('kolesa.csv', 'a') as f:
		writer = csv.writer(f)

		output = []


		keys = sorted(list(data.keys()))
		for i in keys:
			output.append(data[i])		

		writer.writerow(output)

def write_console(data):
	keys = sorted(list(data.keys()))
	for i in keys:
		print('{}: {}'.format(i, data[i]))

def write_db(data):

	config = read_config()
	save_to_mongodb(data, config['host'])


