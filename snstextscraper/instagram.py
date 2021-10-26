# TO DO: Divide each flows by its functionality.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import yaml


# configuration
with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ID = config['instagram']['username']
PW = config['instagram']['password']

# flow 1: login
driver = webdriver.Chrome("/Users/cho2jiwoo/chromedriver")
driver.implicitly_wait(1)
driver.get('https://www.instagram.com/')
sleep(1)

username_input = driver.find_element_by_css_selector("input[name='username']")
password_input = driver.find_element_by_css_selector("input[name='password']")

username_input.send_keys(ID)
password_input.send_keys(PW)

login_button = driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()

# flow 2: close pop-ups
for i in range(0, 2):
    not_now_button = driver.find_element_by_xpath("//button[text()='나중에 하기']")
    not_now_button.click()
    sleep(2)

# flow 3: search hashtag
search_input = driver.find_element_by_css_selector("input[placeholder='검색']")
search_input.send_keys("#애플망고1947")
sleep(1)
search_input.send_keys(Keys.DOWN)
search_input.send_keys(Keys.RETURN)

# flow 4: click on the first post
imgs_parent = driver.find_element_by_xpath("//img[@class='FFVAD']/parent::div[1]")
first_post = imgs_parent.find_element_by_xpath("./following-sibling::div[1]")
first_post.click()

# flow 5: get post content
content = driver.find_element_by_xpath("//li[@role='menuitem']")
content_text = content.text

# flow 6: click 'next' button
next_post = driver.find_element_by_xpath("//a[text()='다음']")
next_post.click()

# loop between flow 5 and flow 6

# flow : close chrome webdriver
driver.quit()
