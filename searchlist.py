from bs4 import BeautifulSoup
from datetime import datetime

from beau import nice_display
from proxy_jumping import get_sleeply_html
from checkdata import check
from todb import add_to_mongo

host = 'https://kolesa.kz'

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = len(soup.find('div', class_='pager').find_all('li'))	
	return pages

def gen_url(brand = 'toyota', model = 'camry', region = 'almaty', price_from = '2000000', price_to = '4000000', year_from = '2008', page=0):
	
	query_part = '?auto-car-grbody=1&price[from]={}&price[to]={}&year[from]={}&_sys-hasphoto=2&auto-emergency=1&auto-car-order=1'.format(price_from, price_to, year_from)
	url = '{}/cars/{}/{}/{}/{}'.format(host, brand, model, region, query_part)

	if page != 0:
		page_part = '&page='
		url +=  page_part + str(page)

	return url

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
			'advert_id':advert_id,
			'creation_date':datetime.utcnow()
		}
		
		# for i in data:
		# 	print('{}\t{}'.format(i, data[i]))
		# print('*'*15)

		write_db(data)

@nice_display
def write_db(data):
	isadd = add_to_mongo(data)
	if isadd:
		check(**data)
		return

@nice_display
def main():
	url = gen_url()
	html = get_sleeply_html(url)
	total_pages = get_total_pages(html)

	for i in range(1, total_pages + 1):

		url = gen_url(page=i)
		html = get_sleeply_html(url)

		parse_selection_page(html)





if __name__ == '__main__':
	main()