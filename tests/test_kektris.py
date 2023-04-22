import pytest
from kektris.kektris import App


@pytest.mark.skip('Is for test display')
def test(make_app: App):
    assert isinstance(make_app, App), 'wrong app'
