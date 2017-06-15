def nice_display(func):
	def inner(*args, **kwargs):
		sep = '-'*15
		print('{0}{1}{0}'.format(sep, 'begin'))
		func()
		print('{0}{1}{0}'.format(sep, 'betti'))
	return inner