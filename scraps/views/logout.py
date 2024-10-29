"""
scraps logout view.

URLs include:
/login/
"""
import flask
from flask import render_template
import scraps


@scraps.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """
    Display Logout Route: Handles logout by clearing & redirect.
    Route URL: /accounts/logout/
    HTTP Methods: POST
    Parameters: None
    Returns: Redirection to the 'login' route.
    """
    context = {
            'logname': None,
    }

    flask.session.clear()
    # return render_template('index.html', **context)
    return flask.redirect(flask.url_for('show_accounts_login'))

