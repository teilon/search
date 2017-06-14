import smtplib




def send(sender, subject, message, to):

	smtp_server = 'smtp.mail.ru'
	smtp_port = 465
	smtp_password = 'goezphstreet87'

	print('smtp')
	mail_lib = smtplib.SMTP(host=smtp_server)
	print('login')
	
	mail_lib.ehlo()
	mail_lib.starttls()
	mail_lib.login(sender, smtp_password)



	print('postlogin')
	# if isinstance(to, str):
	# 	to = ','.join(to)

	# msg = 'From: %s\r\nTo: %s\r\tContent-Type: text/html; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (sender, to, subject)
	# msg += message

	msg = '\r\n'.join([
		'From: {}',
		'To: {}',
		'Subject: {}',
		'',
		'{}'
		])
	msg = msg.format(sender, to, subject, message)


	print('send')
	mail_lib.sendmail(sender, to, msg)
	mail_lib.quit()


def test():
	sep = '-'*15
	print('{0}{1}{0}'.format(sep, 'begin'))
	message = 'hello!'

	send('aspac@inbox.ru', 'the first!', message, 'aspac@inbox.ru')

	print('{0}{1}{0}'.format(sep, 'betti'))








if __name__ == '__main__':
	test()