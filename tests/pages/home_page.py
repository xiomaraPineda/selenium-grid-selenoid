from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    URL = "https://the-internet.herokuapp.com/"
    HEADING = (By.TAG_NAME, "h1")
    LINK_LOGIN = (By.LINK_TEXT, "Form Authentication")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def heading_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.HEADING)).text

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LINK_LOGIN)).click()
        from tests.pages.login_page import LoginPage
        return LoginPage(self.driver)