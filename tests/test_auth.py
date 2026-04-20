import pytest
from tests.pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.auth
def test_home_carga_correctamente(driver):
    home = HomePage(driver).open()
    assert "Welcome to the-internet" in home.heading_text()


@pytest.mark.auth
@pytest.mark.parametrize("user,password,expected", [
    ("tomsmith", "SuperSecretPassword!", "You logged into a secure area"),
    ("foo", "bar", "Your username is invalid"),
    ("tomsmith", "claveMala", "Your password is invalid"),
    ("", "", "Your username is invalid"),
])
def test_login_escenarios(driver, user, password, expected):
    home = HomePage(driver).open()
    login = home.go_to_login()
    login.login(user, password)
    assert expected in login.flash_message()
