from time import sleep

from common.beau import nice_display
from kolesa.kolesa import parse_kolesa
from kolesa.auditor import collect

# @nice_display
def main():

	while(True):
		kolesa.parse_kolesa()
		auditor.collect()

		sleep(3600)
		# sleep(120)



if __name__ == '__main__':
	main()