from beau import nice_display
from time import sleep
import kolesa
import auditor

@nice_display
def main():

	while(True):
		kolesa.parse_kolesa()
		auditor.collect()

		sleep(3600)
		# sleep(120)



if __name__ == '__main__':
	main()