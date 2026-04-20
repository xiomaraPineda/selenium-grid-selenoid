from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class DropdownPage:
    URL = "https://the-internet.herokuapp.com/dropdown"
    DROPDOWN = (By.ID, "dropdown")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def select_by_text(self, text: str):
        element = self.wait.until(EC.element_to_be_clickable(self.DROPDOWN))
        Select(element).select_by_visible_text(text)
        return self

    def get_selected(self) -> str:
        element = self.driver.find_element(*self.DROPDOWN)
        return Select(element).first_selected_option.text
