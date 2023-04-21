import pytest
import pyxel
from typing import Callable
from app.kektris import App


@pytest.fixture(scope="function")
def mock_app(monkeypatch) -> Callable:
    """Mock user data
    """
    def mock_run(*args, **kwargs) -> Callable:
        return None

    monkeypatch.setattr(pyxel, "run", mock_run)


@pytest.fixture(scope="function")
def make_app(mock_app: Callable) -> App:
    """Make app
    """
    return App()
