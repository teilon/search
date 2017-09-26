from time import sleep

from common.beau import nice_display
from common.withmongo import collect_data
from mail.toemail import send

@nice_display
def main():

	while (True):
		message = collect_data()
		
		send(message)

		sleep(28800)

if __name__ == '__main__':
	main()