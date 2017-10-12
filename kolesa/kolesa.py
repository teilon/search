from bs4 import BeautifulSoup
from datetime import datetime

from common.beau import nice_display
from common.beau import logger
from kolesa.proxy_jumping import get_sleeply_html
from kolesa.writer import write_db

host = 'https://kolesa.kz'
test = False

# @nice_display
def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = len(soup.find('div', class_='pager').find_all('li'))	
	return pages

# @nice_display
# def parse_element_page(url, id_element):

# 	html = get_sleeply_html(url)
# 	soup = BeautifulSoup(html, 'lxml')
# 	try:
# 		dl = soup.find('dl', {'class':'clearfix dl-horizontal description-params'}).find_all()
# 	except AttributeError:
# 		print('url: {}'.format(url))
# 		raise AttributeError()

	
# 	titles = {
# 		'Город':'region', 
# 		'Кузов':'body', 
# 		'Объем двигателя, л':'engine_v', 
# 		'Пробег':'mileage', 
# 		'Коробка передач':'transmission', 
# 		'Руль':'steering_wheel', 
# 		'Цвет':'color', 
# 		'Привод':'drive_unit', 
# 		'Растаможен':'customs_cleared'
# 		}
# 	titles_number = 0

# 	values = []
# 	hastitle = False

# 	for elem in dl:
# 		classname = elem.get('class')[0]

# 		if classname == 'value-title':
# 			# title = '{}'.format(elem.text.strip())
# 			# print('elem: {}'.format(elem.text.strip()))
# 			# print()
# 			title = titles[elem.text.strip()]
# 			hastitle = True
# 			continue

# 		if classname == 'value' and hastitle:
# 			values.append({title:''.join(elem.text.strip().split('\xa0'))})
# 			hastitle = False

# 	return values

# @nice_display
@logger
def parse_selection_page(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_='result-block col-sm-8').find_all('div', class_='row list-item')

	for ad in ads:

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
			'publication_date':date,
			'link':host + link,
			'advert_id':advert_id
		}

		# values = parse_element_page(host + link, advert_id)		
		# for i in values:
		# 	data.update(i)

		# if not test:
		# 	write_csv(data)
		# else:
		# 	write_console(data)
		# 	break

		# print('{} : {} : {} : {} : {}'.format(data['title'],
		# 			   			    	   		data['price'],
		# 										data['publication_date'],
		# 										data['link'],
		# 										data['advert_id'],
		# 										))



		# print('save to db')
		write_db(data)


# @nice_display
def gen_url(brand = 'toyota', 
			model = 'camry', 
			region = 'almaty', 
			price_from = '2000000', 
			price_to = '4000000', 
			year_from = '2008', 
			page=0):
	
	query_part = '?auto-car-grbody=1&price[from]={}&price[to]={}&year[from]={}&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'.format(price_from, price_to, year_from)
	url = '{}/cars/{}/{}/{}/{}'.format(host, brand, model, region, query_part)

	if page != 0:
		page_part = '&page='
		url +=  page_part + str(page)
	
	return url

# @nice_display
@logger
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