import flask
import scraps

@scraps.app.route('/dashboard/<username>/')
def dashboard(username):
    context = {
        "test": "TEST"
    }
    return flask.render_template("dashboard.html", **context)
