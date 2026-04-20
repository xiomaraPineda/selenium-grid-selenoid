import pytest
from tests.base.driver_factory import build_driver

@pytest.fixture
def driver():
    drv = build_driver()
    yield drv
    drv.quit()