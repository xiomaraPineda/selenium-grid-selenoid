import pytest
from tests.base.driver_factory import build_driver


@pytest.fixture
def driver(request):
    test_name = request.node.name.replace("[", "_").replace("]", "").replace("/", "_")
    drv = build_driver(test_name=test_name)
    yield drv
    drv.quit()
