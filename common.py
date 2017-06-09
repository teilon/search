import requests

def get_html(url, useragent=None, proxy=None):
	
	r = requests.get(url, headers=useragent, proxies=proxy)
	return r.text