from time import sleep

from common.beau import nice_display, logger
from kolesa.kolesa import parse_kolesa
from kolesa.auditor import collect

# @nice_display
@logger
def main():

	while(True):
		parse_kolesa()
		collect()

		# sleep(3600)
		sleep(60)

if __name__ == '__main__':
	main()