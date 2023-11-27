import flask

app = flask.Flask(__name__)
app.config.from_object('scraps.config')
# app.config.from_envvar('INSTA485_SETTINGS', silent=True)
import scraps.api  # noqa: E402  pylint: disable=wrong-import-position
import scraps.views  # noqa: E402  pylint: disable=wrong-import-position
import scraps.model  # noqa: E402  pylint: disable=wrong-import-position
