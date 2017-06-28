def nice_display(func):
	def inner(*args, **kwargs):
		start = '+'*15
		end = '-'*15
		print('{0}{1}{0}'.format(start, func.__name__))
		func(*args, **kwargs)
		print('{0}{1}{0}'.format(end, func.__name__))
	return inner