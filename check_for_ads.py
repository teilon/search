from pymongo import MongoClient

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def check():
	client = MongoClient('localhost', 27017)

	db = client['kolesa']
	offers = db['offers']

	offers_ = offers.find({})
	messages = '';

	for of in offers_:
		message = '\ntitle:\t{}\n\tadvert:\t{}\n\tdate:\t{}\n\tprice:\t{}\n\tlink:\t{}\n'.format(
			of['title'], 
			of['advert_id'], 
			of['publication_date'],
			of['price'],
			of['link'])
		print(message)
		messages += message

	return messages

def send(message, sender='test_kolesa@mail.ru', subject='kolesa', to='aspac@inbox.ru'):

	smtp_server = 'smtp.mail.ru'
	smtp_port = 465

	sender_password = 'testirovanie'

	server = smtplib.SMTP(host=smtp_server)	
	server.ehlo()
	server.starttls()
	server.login(sender, sender_password)

	msg = MIMEMultipart('alternative')
	msg.set_charset('utf-8')

	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = to
	
	text = MIMEText(message, 'plain')

	msg.attach(text)

	server.sendmail(sender, to, msg.as_string())

	server.quit()

def main():
	result = check()
	send(result)

if __name__ == '__main__':
	main()