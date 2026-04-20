from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DynamicLoadingPage:
    URL = "https://the-internet.herokuapp.com/dynamic_loading/2"
    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    FINISH = (By.ID, "finish")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)
        return self

    def start_loading(self):
        self.wait.until(EC.element_to_be_clickable(self.START_BUTTON)).click()
        return self

    def wait_for_finish_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.FINISH)).text
