# TO DO: Divide each flows by its functionality.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import yaml


# configuration
with open('config.yml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

ID = config['instagram']['username']
PW = config['instagram']['password']

# flow 1: login
driver = webdriver.Chrome("/Users/cho2jiwoo/chromedriver")
driver.get('https://www.instagram.com/')

username_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
)
password_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
)

username_input.send_keys(ID)
password_input.send_keys(PW)

login_button = driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()

# flow 2: close pop-ups
for i in range(0, 2):
    not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), '나중에 하기')]")  # only works in korean
        )).click()

# flow 3: search hashtag
hashtag = "애플망고1947"
driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

# flow 4: click on the first post
first_img_parent_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//img[@class='FFVAD']/parent::div[1]")  # class name could change 
    )
)
first_post = first_img_parent_element.find_element_by_xpath(
    "./following-sibling::div[1]"
)
first_post.click()

# flow 5: get post content
content = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem']"))
)
content_item = content.find_elements_by_tag_name('span')[1]
content_text = content_item.text

# flow 6: click 'next' button
next_post = driver.find_element_by_xpath("//a[text()='다음']")  # only works in korean
next_post.click()

# loop between flow 5 and flow 6

# flow : close chrome webdriver
driver.quit()
