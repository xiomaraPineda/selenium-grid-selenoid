import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

REMOTE_URL = os.getenv("REMOTE_URL")
BROWSER = os.getenv("BROWSER", "chrome").lower()
ENABLE_VIDEO = os.getenv("ENABLE_VIDEO", "false").lower() == "true"
ENABLE_VNC = os.getenv("ENABLE_VNC", "true").lower() == "true"


def build_driver(test_name: str = "test"):
    if BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    elif BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
    else:
        raise ValueError(f"Navegador no soportado: {BROWSER}")

    if REMOTE_URL:
        options.set_capability("browserName", BROWSER)
        selenoid_opts = {
            "enableVNC": ENABLE_VNC,
            "enableVideo": ENABLE_VIDEO,
            "name": test_name,
            "screenResolution": "1920x1080x24",
        }
        options.set_capability("selenoid:options", selenoid_opts)
        driver = webdriver.Remote(command_executor=REMOTE_URL, options=options)
    else:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    driver.set_window_size(1366, 768)
    return driver
