from time import sleep

from common.beau import nice_display
import kolesa.kolesa
import kolesa.auditor

# @nice_display
def main():

	while(True):
		kolesa.parse_kolesa()
		auditor.collect()

		sleep(3600)
		# sleep(120)



if __name__ == '__main__':
	main()