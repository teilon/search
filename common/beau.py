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

def logger(func):

	@functools.wraps(func)
	def inner(*args, **kwargs):
				
		to_log('start {}'.format(func.__name__))

		result = func(*args, **kwargs)

		to_log('end {}'.format(func.__name__))

		return result
		
	return inner

def to_log(log):
	with open('/tmp/data/log.txt', 'a') as f:
		f.write('{}\n'.format(log))