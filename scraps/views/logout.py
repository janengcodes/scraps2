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
    if 'username' in flask.session:
        flask.session.clear()
    return flask.redirect(flask.url_for('show_accounts_login'))

