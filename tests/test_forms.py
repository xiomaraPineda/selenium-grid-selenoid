import pytest
from tests.pages.checkboxes_page import CheckboxesPage
from tests.pages.dropdown_page import DropdownPage


@pytest.mark.forms
def test_checkbox_toggle(driver):
    page = CheckboxesPage(driver).open()
    estado_inicial = page.is_checked(0)
    page.toggle(0)
    assert page.is_checked(0) != estado_inicial


@pytest.mark.forms
def test_checkbox_ambos_marcados(driver):
    page = CheckboxesPage(driver).open()
    if not page.is_checked(0):
        page.toggle(0)
    assert page.is_checked(0) is True
    assert page.is_checked(1) is True


@pytest.mark.forms
@pytest.mark.parametrize("opcion", ["Option 1", "Option 2"])
def test_dropdown_seleccion(driver, opcion):
    page = DropdownPage(driver).open()
    page.select_by_text(opcion)
    assert page.get_selected() == opcion
