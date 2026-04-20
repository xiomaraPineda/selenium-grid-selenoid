from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AddRemovePage:
    URL = "https://the-internet.herokuapp.com/add_remove_elements/"
    ADD_BUTTON = (By.XPATH, "//button[text()='Add Element']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, ".added-manually")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def add_elements(self, n: int):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))
        for _ in range(n):
            btn.click()
        return self

    def delete_first(self):
        self.driver.find_elements(*self.DELETE_BUTTONS)[0].click()
        return self

    def count_added(self) -> int:
        return len(self.driver.find_elements(*self.DELETE_BUTTONS))
