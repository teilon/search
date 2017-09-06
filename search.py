from beau import nice_display
from time import sleep
import kolesa

@nice_display
def main():

	while(True):
		kolesa.parse_kolesa()

		sleep(36000)
		# sleep(120)



if __name__ == '__main__':
	main()