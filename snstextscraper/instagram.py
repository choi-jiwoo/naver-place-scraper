# TO DO: Divide each flows by its functionality.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import yaml


# configuration
with open('../config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ID = config['instagram']['username']
PW = config['instagram']['password']

# flow 1: login
browser = webdriver.Chrome("/Users/cho2jiwoo/chromedriver")
browser.implicitly_wait(1)
browser.get('https://www.instagram.com/')
sleep(1)

username_input = browser.find_element_by_css_selector("input[name='username']")
password_input = browser.find_element_by_css_selector("input[name='password']")

username_input.send_keys("")
password_input.send_keys("")

login_button = browser.find_element_by_xpath("//button[@type='submit']")
login_button.click()

# flow 2: close pop-ups
for i in range(0, 2):
    not_not_button = browser.find_element_by_xpath("//button[text()='나중에 하기']")
    not_not_button.click()
    sleep(2)

# flow 3: search hashtag
search_input = browser.find_element_by_css_selector("input[placeholder='검색']")
search_input.send_keys("#애플망고1947")
search_input.send_keys(Keys.DOWN)
search_input.send_keys(Keys.RETURN)

# flow 4: close chrome webdriver
browser.close()
