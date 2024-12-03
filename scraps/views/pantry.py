import flask
from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/pantry/<username>/')
def pantry(username):
    context = {
        'example_variable': 'Hello, World!'
    }
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    

    
    return render_template('pantry.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
