from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException        
import time
import sys

import utilities.config

def enter_string(element, string):
	element.clear()
	element.send_keys(string)

def get_options():
	options = Options()

	options.add_argument("--disable-infobars")
	options.add_argument("start-maximized")
	options.add_argument("--disable-extensions")

	# Pass the argument 1 to allow and 2 to block
	options.add_experimental_option("prefs", { 
	    "profile.default_content_setting_values.notifications": 2
	})

	return options

def wait_for_element(element_css_selector):
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CSS_SELECTOR, element_css_selector))
	    )
	    if (element):
	    	return True
	    else:
	    	return False
	except:
		return False

def check_element_exists(css_selector):
    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True


platform_config = utilities.config.get_config('.channels')
url = platform_config['facebook']['channels'][0]['config']['url']
name = platform_config['facebook']['channels'][0]['name']
email = platform_config['facebook']['channels'][0]['credentials']['email']
password = platform_config['facebook']['channels'][0]['credentials']['password']

driver = webdriver.Chrome(options = get_options())
driver.get(url)
title = driver.title
if (name not in title):
	enter_string(driver.find_element_by_css_selector("input[name='email']"), email)
	enter_string(driver.find_element_by_css_selector("input[name='pass']"), password)

	if (check_element_exists("input[value='Log In']")):
		log_in_button = driver.find_element_by_css_selector("input[value='Log In']")
		log_in_button.click()
	elif (check_element_exists("button[name='login']")):
		log_in_button = driver.find_element_by_css_selector("button[name='login']")
		log_in_button.click()

if (not wait_for_element("a[aria-label='Options']")):
	sys.exit()

post = driver.find_element_by_css_selector("textarea[name='xhpc_message']")
post.click()

if (not wait_for_element("button[label='Show background options']")):
	sys.exit()
if (not wait_for_element("a[data-tooltip-content='Insert an emoji']")):
	sys.exit()

enter_string(driver.find_element_by_css_selector("div[data-testid='status-attachment-mentions-input']"), "test")

post_button = driver.find_element_by_css_selector("button[data-testid='react-composer-post-button']")
post_button.click()


#driver.close()