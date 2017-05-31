import requests
from bs4 import BeautifulSoup

from writer import write_csv
from writer import write_console

from selenium import webdriver

from time import sleep

host = 'https://kolesa.kz'
test = True



def get_html(url):
	r = requests.get(url)
	return r.text


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = len(soup.find('div', class_='pager').find_all('li'))	
	return pages


def parse_element_page(url, id_element):

	driver = webdriver.Firefox()
	driver.get(url);
	
	ajax = driver.find_element_by_xpath('//span[@class="action-link showPhonesLink"]')
	ajax.click()

	sleep(1)

	print('***\t0\t***')

	html = driver.find_element_by_xpath('//*').get_attribute('outerHTML') 

	print(html)

	# phone_elements = driver.find_elements_by_xpath('//span[@class="a-phones phonesContainer phonesContainer_{}"]/ul'.format(id_element))
	# for li in phone_elements:
	# 	print('-----\n{}\n-----'.format(li.text))

def parse_selection_page(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_='result-block col-sm-8').find_all('div', class_='row list-item')

	for ad in ads:
		# title, price, year, region

		try:
			data_id = ad['data-id'].strip()
		except:
			continue

		try:
			title = ad.find('div', class_='list-title').find('a').text.strip()
		except:
			title = 'none'

		try:
			price = ad.find('div', class_='list-title').find('span', class_='price').text.strip()
			price = ''.join(price.split('\xa0'))
		except:
			price = 'none'

		try:
			year = ad.find('div', class_='list-extra-info').find('span', class_='year').text.strip()
			year = ''.join(year.split('\xa0'))
		except:
			year = 'none'

		try:
			region = ad.find('div', class_='list-region').text.strip()
			region = ''.join(region.split('\xa0'))
		except:
			region = 'none'

		try:
			date = ad.find('div', class_='list-views-comments').find('span', class_='date').text.strip()
			date = ''.join(date.split('\xa0'))
		except:
			date = 'none'

		try:
			link = ad.find('div', class_='list-title').find('a')['href']
		except:
			link = 'none'		

		data = {
			'title':title,
			'price':price,
			'year':year,
			'region':region,
			'date':date,
			'link':link,
			'data_id':data_id
		}

		parse_element_page(host + link, data_id)
		
		if not test:
			write_csv(data)
		else:
			write_console(data)

		break


def parse_test():

	with open('kolesa_test.html', 'r') as f:
		html = f.read()

	parse_selection_page(html)



def parse_kolesa(brand = 'toyota', model = 'camry', region = 'almaty', price_from = '2000000', price_to = '4000000', year_from = '2008'):
	#'https://kolesa.kz/cars/toyota/camry/almaty/?auto-car-grbody=1&price[from]=2000000&price[to]=4000000&year[from]=2008&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'
	
	query_part_of_url = '?auto-car-grbody=1&price[from]={}&price[to]={}&year[from]={}&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'.format(price_from, price_to, year_from)
	url = '{}/cars/{}/{}/{}/{}'.format(host, brand, model, region, query_part_of_url)	
	page_part = '&page='
	
	html = get_html(url)
	total_pages = get_total_pages(html)

	for i in range(1, total_pages + 1):
		url_gen = url + page_part + str(i)
		html = get_html(url_gen)

		parse_selection_page(html)
		break



def main():
	print('begin')

	parse_kolesa()

	#parse_test()

	print('betti')



if __name__ == '__main__':
	main()