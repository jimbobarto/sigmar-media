from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import utilities.config

platform_config = utilities.config.get_config('.channels')
url = platform_config['facebook']['channels'][0]['config']['url']
name = platform_config['facebook']['channels'][0]['name']

driver = webdriver.Chrome()
driver.get(url)
assert name in driver.title
#elem = driver.find_element_by_name("q")
post = driver.find_element_by_css_selector("div[aria-label='What\'s on your mind?']")
post.click()

#elem.clear()
#elem.send_keys("test message")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()