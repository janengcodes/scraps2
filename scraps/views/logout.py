"""
scraps logout view.

URLs include:
/login/
"""
import flask
from flask import render_template
import scraps


@scraps.app.route('/accounts/logout/', methods=['POST', 'GET'])
def logout():
    if flask.request.method == 'POST':
        if 'username' in flask.session:
            flask.session.clear()
        return flask.redirect(flask.url_for('show_accounts_login'))
    # Handle GET requests by redirecting to login
    return flask.redirect(flask.url_for('show_accounts_login'))


