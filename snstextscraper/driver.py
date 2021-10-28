from selenium import webdriver


class Driver:

    def __init__(self, path: str, headless: bool = 'False') -> None:
        self.path = path
        self.headless = headless

    def driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.headless = self.headless
        driver = webdriver.Chrome(self.path, options=options)

        return driver
