from random import choice
from random import uniform
from time import sleep
import requests

def get_html(url, useragent=None, proxy=None):
	
	r = requests.get(url, headers=useragent, proxies=proxy)
	return r.text

def get_sleeply_html(url):
	sleeptime = uniform(3,5)
	sleep(sleeptime)
	
	while True:
		
		try:
			# proxy, useragent = get_new_proxies()
			# html = get_html(url, useragent, proxy)
			html = get_html(url)
		except Exception as e:
			# to_log(type(e))
			continue
		else:
			break
	
	return html

def get_new_proxies():
	useragents = open('useragents.txt').read().split('\n')
	proxies = open('proxies.txt').read().split('\n')

	proxy = {'http':'http://' + choice(proxies)}
	useragent = {'User-Agent':choice(useragents)}

	return proxy, useragent