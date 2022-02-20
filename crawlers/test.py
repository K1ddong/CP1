from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

geckodriver_loc = '/Users/dennis/projects/cp1/venv/geckodriver'
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options,executable_path='/Users/dennis/projects/cp1/venv/geckodriver')
driver.get("https://pythonbasics.org")