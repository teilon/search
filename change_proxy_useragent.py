import requests
from bs4 import BeautifulSoup

from random import choice
from random import uniform

from time import sleep
from datetime import datetime

import csv



def get_html(url, useragent=None, proxy=None):

	print('\tget_html')

	r = requests.get(url, headers=useragent, proxies=proxy)
	return r.text


def get_ip(html):
	print('\tget_ip')

	soup = BeautifulSoup(html, 'lxml')
	error = 'none'

	try:
		ip = soup.find('span', class_='ip').text.strip()
	except Exception as e:
		ip='none'
		error = 'error:{}\tip'.format(type(e))
		print('error:{}\tip'.format(type(e)))

	try:
		ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
	except Exception as e:
		ua='none'
		error = 'error:{}\tuser agent'.format(type(e))
		print('error:{}\tuser agent'.format(type(e)))

	print('{}\n{}\n---------------'.format(ip, ua))
	return {'error':error}


def write_csv(data):
	with open('change_proxy_useragent.csv', 'a') as f:
		writer = csv.writer(f)
		
		writer.writerow((
					data['proxy'],
					data['useragent'],
					data['error'],
					data['datetime']
					))

def to_log(data):
	write_csv(data)


def main():
	print('begin')

	url = 'http://sitespy.ru/my-ip'

	useragents = open('useragents.txt').read().split('\n')
	proxies = open('proxies.txt').read().split('\n')

	#print(proxies[-1])

	for i in range(100):

		sleeptime = uniform(3,5)
		sleep(sleeptime)

		proxy = {'http':'http://' + choice(proxies)}
		useragent = {'User-Agent':choice(useragents)}

		dt = datetime.now()


		print('#{} [{}]\n{}\n********\n{}\n{}\n********'.format(i, sleeptime, dt, proxy, useragent))

		try:
			html = get_html(url, useragent, proxy)
		except:
			to_log({
				'proxy':proxy,
				'useragent':useragent,
				'error':'continue',
				'datetime':dt
			})
			continue
		out = get_ip(html)

		to_log({
			'proxy':proxy,
			'useragent':useragent,
			'error':out['error'],
			'datetime':dt
		})


		# data = {
		# 	'proxy':proxy,
		# 	'useragent':useragent,
		# 	'error':out['error']
		# }

		# write_csv(data)

	print('betti')




if __name__ == '__main__':
	main()