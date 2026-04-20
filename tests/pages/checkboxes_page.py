from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckboxesPage:
    URL = "https://the-internet.herokuapp.com/checkboxes"
    CHECKBOXES = (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def get_checkboxes(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.CHECKBOXES))

    def toggle(self, index: int):
        self.get_checkboxes()[index].click()
        return self

    def is_checked(self, index: int) -> bool:
        return self.get_checkboxes()[index].is_selected()
