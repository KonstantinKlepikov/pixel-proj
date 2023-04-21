from app.kektris import App


def test(make_app: App):
    assert isinstance(make_app, App), 'wrong app'
