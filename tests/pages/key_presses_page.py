from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class KeyPressesPage:
    URL = "https://the-internet.herokuapp.com/key_presses"
    INPUT = (By.ID, "target")
    RESULT = (By.ID, "result")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def press_and_wait(self, key, expected_token: str):
        field = self.wait.until(EC.element_to_be_clickable(self.INPUT))
        field.click()
        field.send_keys(key)
        self.wait.until(EC.text_to_be_present_in_element(self.RESULT, expected_token))
        return self

    def result_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.RESULT)).text
