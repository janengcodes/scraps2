import flask
from flask import redirect, render_template, Flask
import scraps
app = Flask(__name__)



@scraps.app.route('/recipes/')
def get_recipes():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    logname = flask.session.get('username')
    
    context = {
        'example_variable': 'Hello, World!'
    }
    return render_template('recipes.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
