import pytest
from selenium.webdriver.common.keys import Keys
from tests.pages.add_remove_page import AddRemovePage
from tests.pages.key_presses_page import KeyPressesPage
from tests.pages.javascript_alerts_page import JavaScriptAlertsPage


@pytest.mark.interactions
def test_agregar_multiples_elementos(driver):
    page = AddRemovePage(driver).open()
    page.add_elements(5)
    assert page.count_added() == 5


@pytest.mark.interactions
def test_eliminar_elemento(driver):
    page = AddRemovePage(driver).open()
    page.add_elements(3)
    page.delete_first()
    assert page.count_added() == 2


@pytest.mark.interactions
@pytest.mark.parametrize("tecla,esperado", [
    (Keys.SPACE, "SPACE"),
    pytest.param(
        Keys.ENTER, "ENTER",
        marks=pytest.mark.xfail(
            reason=(
                "ENTER en un <input type='text'> dispara el submit implícito del "
                "formulario en Chrome antes de que el listener de #result capture el "
                "evento keyup. Es comportamiento nativo del navegador, no un bug de "
                "la aplicación ni de Selenium. Documentado como limitación conocida."
            ),
            strict=False,
        )
    ),
    (Keys.ESCAPE, "ESCAPE"),
    (Keys.TAB, "TAB"),
])
def test_key_press(driver, tecla, esperado):
    page = KeyPressesPage(driver).open()
    page.press_and_wait(tecla, esperado)
    assert esperado in page.result_text()


@pytest.mark.interactions
def test_js_alert(driver):
    page = JavaScriptAlertsPage(driver).open()
    page.trigger_alert_and_accept()
    assert "successfully clicked an alert" in page.result_text()


@pytest.mark.interactions
def test_js_confirm_cancelar(driver):
    page = JavaScriptAlertsPage(driver).open()
    page.trigger_confirm_and_dismiss()
    assert "You clicked: Cancel" in page.result_text()


@pytest.mark.interactions
def test_js_prompt(driver):
    page = JavaScriptAlertsPage(driver).open()
    page.trigger_prompt_and_send("Selenoid rocks")
    assert "You entered: Selenoid rocks" in page.result_text()
