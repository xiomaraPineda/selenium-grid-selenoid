from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JavaScriptAlertsPage:
    URL = "https://the-internet.herokuapp.com/javascript_alerts"
    BTN_ALERT = (By.XPATH, "//button[text()='Click for JS Alert']")
    BTN_CONFIRM = (By.XPATH, "//button[text()='Click for JS Confirm']")
    BTN_PROMPT = (By.XPATH, "//button[text()='Click for JS Prompt']")
    RESULT = (By.ID, "result")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def trigger_alert_and_accept(self):
        self.driver.find_element(*self.BTN_ALERT).click()
        self.wait.until(EC.alert_is_present()).accept()
        return self

    def trigger_confirm_and_dismiss(self):
        self.driver.find_element(*self.BTN_CONFIRM).click()
        self.wait.until(EC.alert_is_present()).dismiss()
        return self

    def trigger_prompt_and_send(self, text: str):
        self.driver.find_element(*self.BTN_PROMPT).click()
        alert = self.wait.until(EC.alert_is_present())
        alert.send_keys(text)
        alert.accept()
        return self

    def result_text(self) -> str:
        return self.driver.find_element(*self.RESULT).text
