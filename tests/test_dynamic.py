import pytest
from tests.pages.dynamic_loading_page import DynamicLoadingPage


@pytest.mark.dynamic
@pytest.mark.slow
def test_dynamic_loading_espera_explicita(driver):
    page = DynamicLoadingPage(driver).open()
    page.start_loading()
    assert "Hello World!" in page.wait_for_finish_text()
