from bs4 import BeautifulSoup

# from common import get_html
from proxy_jumping import get_sleeply_html
# import common

from writer import write_csv
from writer import write_console
from writer import write_db

from datetime import datetime

host = 'https://kolesa.kz'
test = False

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = len(soup.find('div', class_='pager').find_all('li'))	
	return pages

def parse_element_page(url, id_element):

	html = get_sleeply_html(url)
	soup = BeautifulSoup(html, 'lxml')
	dl = soup.find('dl', {'class':'clearfix dl-horizontal description-params'}).find_all()
	
	titles = {
		'Город':'region', 
		'Кузов':'body', 
		'Объем двигателя, л':'engine_v', 
		'Пробег':'mileage', 
		'Коробка передач':'transmission', 
		'Руль':'steering_wheel', 
		'Цвет':'color', 
		'Привод':'drive_unit', 
		'Растаможен':'customs_cleared'
		}
	titles_number = 0

	values = []
	hastitle = False

	for elem in dl:
		classname = elem.get('class')[0]

		if classname == 'value-title':
			# title = '{}'.format(elem.text.strip())
			# print('elem: {}'.format(elem.text.strip()))
			# print()
			title = titles[elem.text.strip()]
			hastitle = True
			continue

		if classname == 'value' and hastitle:
			values.append({title:''.join(elem.text.strip().split('\xa0'))})
			hastitle = False

	return values

def parse_selection_page(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_='result-block col-sm-8').find_all('div', class_='row list-item')

	for ad in ads:
		# title, price, year, region

		try:
			advert_id = ad['data-id'].strip()
		except:
			continue

		try:
			title = ad.find('div', class_='list-title').find('a').text.strip()
			title = ''.join(title.split('\xa0'))
		except:
			title = 'none'

		try:
			price = ad.find('div', class_='list-title').find('span', class_='price').text.strip()
			price = ''.join(price.split('\xa0'))
		except:
			price = 'none'

		try:
			year_of_issue = ad.find('div', class_='list-extra-info').find('span', class_='year').text.strip()
			year_of_issue = ''.join(year_of_issue.split('\xa0'))
		except:
			year_of_issue = 'none'

		# try:
		# 	region = ad.find('div', class_='list-region').text.strip()
		# 	region = ''.join(region.split('\xa0'))
		# except:
		# 	region = 'none'

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
			'year':year_of_issue,
			# 'base_region':region,
			'publication_date':date,
			'link':host + link,
			'advert_id':advert_id,
			'creation_date':datetime.utcnow()
		}

		values = parse_element_page(host + link, advert_id)		
		for i in values:
			data.update(i)

		# if not test:
		# 	write_csv(data)
		# else:
		# 	write_console(data)
		# 	break
		write_db(data)



def gen_url(brand = 'toyota', model = 'camry', region = 'almaty', price_from = '2000000', price_to = '4000000', year_from = '2008', page=0):
	
	query_part = '?auto-car-grbody=1&price[from]={}&price[to]={}&year[from]={}&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'.format(price_from, price_to, year_from)
	url = '{}/cars/{}/{}/{}/{}'.format(host, brand, model, region, query_part)

	if page != 0:
		page_part = '&page='
		url +=  page_part + str(page)

	return url

def parse_kolesa():
	
	url = gen_url()
	html = get_sleeply_html(url)
	total_pages = get_total_pages(html)

	for i in range(1, total_pages + 1):

		url = gen_url(page=i)
		html = get_sleeply_html(url)

		parse_selection_page(html)

		if test:
			break