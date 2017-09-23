from selenium import webdriver



class Bot:
	def __init__(self):
		self.driver = webdriver.Firefox()
		self.navigate()

	def take_screen_shot(self):
		self.driver.save_screenshot('screenshot.png')

	def navigate(self):
		self.driver.get('https://kolesa.kz/a/show/36181754');

		ajax = self.driver.find_element_by_xpath('//span[@class="action-link showPhonesLink"]')
		ajax.click()



def main():
	b = Bot()



if __name__ == '__main__':
	main() 