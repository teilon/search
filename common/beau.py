import functools

def nice_display(func):

	@functools.wraps(func)
	def inner(*args, **kwargs):
		start = '+'*15
		end = '-'*15

		print('{1}{0}{1}'.format(func.__name__, start))

		result = func(*args, **kwargs)

		print('{1}{0}{1}'.format(func.__name__, end))
		return result
		
	return inner