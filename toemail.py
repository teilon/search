import smtplib




def send(sender, subject, message, to):

	smtp_server = 'smtp.mail.ru'
	smtp_port = 465

	sender_password = 'password'

	server = smtplib.SMTP(host=smtp_server)	
	server.ehlo()
	server.starttls()
	server.login(sender, sender_password)

	msg = '\r\n'.join([
		'From: {}',
		'To: {}',
		'Subject: {}',
		'',
		'{}'
		])
	msg = msg.format(sender, to, subject, message)

	server.sendmail(sender, to, msg)
	server.quit()


def test():
	sep = '-'*15
	print('{0}{1}{0}'.format(sep, 'begin'))
	message = 'hello!'

	send('aspac@inbox.ru', 'the first!', message, 'aspac@inbox.ru')

	print('{0}{1}{0}'.format(sep, 'betti'))








if __name__ == '__main__':
	test()