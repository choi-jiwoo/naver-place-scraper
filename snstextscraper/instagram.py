# TO DO: Divide each flows by its functionality.
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class Instagram:

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    def login(self, id: str, pw: str, timeout: int = 5) -> None:
        self.driver.get("https://www.instagram.com/")

        username_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='username']")
            )
        )
        password_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='password']")
            )
        )

        username_input.send_keys(id)
        password_input.send_keys(pw)
        submit = self.driver.find_element_by_xpath("//button[@type='submit']")
        submit.click()

        try:
            for i in range(2):
                self.close_pop_up(timeout)
        except TimeoutException:
            print("Login failed. Try again.")

    def close_pop_up(self, timeout: int) -> None:
        not_now_button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), '나중에 하기')]")  # only works in korean
            )).click()

    def search(self, hashtag: str) -> None:
        self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        first_img_parent_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//img[@class='FFVAD']/parent::div[1]")  # class name could change
            )
        )
        first_post = first_img_parent_element.find_element_by_xpath(
            "./following-sibling::div[1]"
        )
        sleep(2)
        first_post.click()

    def get_contents(self) -> dict:
        contents = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@role='menuitem']"))
        )
        author = contents.find_elements_by_tag_name('span')[0].text
        content_text = contents.find_elements_by_tag_name('span')[1].text
        post = {author: content_text}

        return post

    def next_post(self) -> None:
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RIGHT)
        actions.perform()
