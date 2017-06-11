import requests
from bs4 import BeautifulSoup

from random import choice
from random import uniform

from time import sleep
from datetime import datetime

import csv


# def get_html(url, useragent=None, proxy=None):
def get_html(url):

	sleeptime = uniform(3,5)
	sleep(sleeptime)

	# print('\tget_html')
	proxy, useragent = get_url_data()

	r = requests.get(url, headers=useragent, proxies=proxy)
	return r.text


def get_ip(html):
	# print('\tget_ip')

	soup = BeautifulSoup(html, 'lxml')
	error = 'none'

	try:
		ip = soup.find('span', class_='ip').text.strip()
	except Exception as e:
		ip='none'
		error = 'error:{}\tip'.format(type(e))
		# print('error:{}\tip'.format(type(e)))

	try:
		ua = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
	except Exception as e:
		ua='none'
		error = 'error:{}\tuser agent'.format(type(e))
		# print('error:{}\tuser agent'.format(type(e)))

	# print('{}\n{}\n---------------'.format(ip, ua))
	return ip, error


def write_csv(data):
	with open('change_proxy_useragent.csv', 'a') as f:
		writer = csv.writer(f)
		
		writer.writerow((
					data['proxy'],
					data['useragent'],
					data['error'],
					data['datetime']
					))

def write_console(data, counter):
	# print('#{}\nproxy: {}\nuseragent: {}\nerror: {}\nip: {}\ndatetime: {}\n'.format(
	# 	counter,		
	# 	data['proxy'],
	# 	data['useragent'],
	# 	data['error'],
	# 	data['ip'],
	# 	data['datetime']
	# 	))
	print('#{}\nip: {}\n'.format(
		counter,	
		data['ip']
		))

def to_log(data, counter):
	#write_csv(data)
	write_console(data, counter)


def get_url_data():
	useragents = open('useragents.txt').read().split('\n')
	proxies = open('proxies.txt').read().split('\n')

	proxy = {'http':'http://' + choice(proxies)}
	useragent = {'User-Agent':choice(useragents)}

	return proxy, useragent

def main():
	print('begin\n--------------------')

	url = 'http://sitespy.ru/my-ip'

	# useragents = open('useragents.txt').read().split('\n')
	# proxies = open('proxies.txt').read().split('\n')

	#print(proxies[-1])

	for i in range(10):

		# sleeptime = uniform(3,5)
		# sleep(sleeptime)

		# proxy = {'http':'http://' + choice(proxies)}
		# useragent = {'User-Agent':choice(useragents)}
		proxy, useragent = get_url_data()

		dt = datetime.now()


		# print('#{} [{}]\n{}\n********\n{}\n{}\n********'.format(i, sleeptime, dt, proxy, useragent))

		try:
			html = get_html(url)
		except Exception as e:
			to_log({
				'proxy':proxy,
				'useragent':useragent,
				'error':type(e),
				'ip':'none',
				'datetime':dt
			}, i)
			continue
		ip, error = get_ip(html)

		to_log({
			'proxy':proxy,
			'useragent':useragent,
			'error':error,
			'ip':ip,
			'datetime':dt
		}, i)


		# data = {
		# 	'proxy':proxy,
		# 	'useragent':useragent,
		# 	'error':out['error']
		# }

		# write_csv(data)

	print('--------------------\nbetti')




if __name__ == '__main__':
	main()