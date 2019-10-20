from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException        
import time
import sys

import platforms.platform_utilities as platform_utilities

class FacebookPlatform:
    def enter_string(self, driver, element, string):
        element.clear()
        element.send_keys(string)

    def get_options(self):
        options = Options()

        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 2
        })

        return options

    def wait_for_element(self, driver, element_css_selector):
        try:
            element = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, element_css_selector))
            )
            if (element):
                return True
            else:
                return False
        except Exception as e:
            print("exception: " + str(e))
            return False

    def check_element_exists(self, driver, css_selector):
        try:
            driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return False
        return True

    def send_message(self, credentials, config, message):
        driver = webdriver.Chrome(options = self.get_options())
        driver.get(credentials['url'])
        title = driver.title
        if (credentials['name'] not in title):
            self.enter_string(driver,driver.find_element_by_css_selector("input[name='email']"), credentials['email'])
            self.enter_string(driver, driver.find_element_by_css_selector("input[name='pass']"), credentials['password'])

            if (self.check_element_exists(driver, "input[value='Log In']")):
                log_in_button = driver.find_element_by_css_selector("input[value='Log In']")
                log_in_button.click()
            elif (self.check_element_exists(driver, "button[name='login']")):
                log_in_button = driver.find_element_by_css_selector("button[name='login']")
                log_in_button.click()

        if (not self.wait_for_element(driver, "a[aria-label='Options']")):
            driver.close()
            return {"status": "failed", "message": "Couldn't find the options on the chat popup before continuing", "timestamp": platform_utilities.get_timestamp()}

        post = driver.find_element_by_css_selector("textarea[name='xhpc_message']")
        post.click()

        if (not self.wait_for_element(driver, "button[label='Show background options']")):
            driver.close()
            return {"status": "failed", "message": "Couldn't find the post popup options", "timestamp": platform_utilities.get_timestamp()}
        if (not self.wait_for_element(driver, "a[data-tooltip-content='Insert an emoji']")):
            driver.close()
            return {"status": "failed", "message": "Couldn't find the post emoji options", "timestamp": platform_utilities.get_timestamp()}

        self.enter_string(driver, driver.find_element_by_css_selector("div[data-testid='status-attachment-mentions-input']"), message['body'])

        post_button = driver.find_element_by_css_selector("button[data-testid='react-composer-post-button']")
        post_button.click()

        self.wait_for_element(driver, "p:contains('" + message['body'] + "')")

        driver.close()
        return {"status": "succeeded", "message": "Message posted successfully", "timestamp": platform_utilities.get_timestamp()}

    def get_platform_name(self):
        return "facebook"
