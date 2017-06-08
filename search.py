import requests
from bs4 import BeautifulSoup

from writer import write_csv
from writer import write_console

# from selenium import webdriver

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

	# driver = webdriver.Firefox()
	# driver.get(url);
	
	# ajax = driver.find_element_by_xpath('//span[@class="action-link showPhonesLink"]')
	# ajax.click()
	# sleep(1)
	# html = driver.find_element_by_xpath('//*').get_attribute('outerHTML') 

	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	dl = soup.find('dl', {'class':'clearfix dl-horizontal description-params'}).find_all()
		
	values = []
	hastitle = False

	for elem in dl:
		classname = elem.get('class')[0]

		if classname == 'value-title':
			title = 'private_{}'.format(elem.text.strip())
			hastitle = True
			continue

		if classname == 'value' and hastitle:
			values.append({title:elem.text.strip()})
			hastitle = False

	return values

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
			'base_title':title,
			'base_price':price,
			'base_year':year,
			'base_region':region,
			'base_date':date,
			'base_link':host + link,
			'base_data_id':data_id
		}

		values = parse_element_page(host + link, data_id)

		
		for i in values:
			data.update(i)

		if not test:
			write_csv(data)
		else:
			write_console(data)
			break



def gen_url(brand = 'toyota', model = 'camry', region = 'almaty', price_from = '2000000', price_to = '4000000', year_from = '2008', page=0):
	
	query_part = '?auto-car-grbody=1&price[from]={}&price[to]={}&year[from]={}&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'.format(price_from, price_to, year_from)
	url = '{}/cars/{}/{}/{}/{}'.format(host, brand, model, region, query_part)

	if page != 0:
		page_part = '&page='
		url +=  page_part + str(page)

	return url

def parse_kolesa():
	
	url = gen_url()
	html = get_html(url)
	total_pages = get_total_pages(html)

	for i in range(1, total_pages + 1):

		url = gen_url(page=i)
		html = get_html(url)

		parse_selection_page(html)

		if test:
			break


def main():
	print('begin\n--------------------')

	parse_kolesa()

	print('--------------------\nbetti')



if __name__ == '__main__':
	main()