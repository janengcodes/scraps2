"""REST API for likes."""
import hashlib
from flask import jsonify
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth

import requests

@scraps.app.route('/api/check-auth', methods=['GET'])
def check_login():
    """Check if a user is logged in"""
    logname = check_auth()

    connection = scraps.model.get_db()
    # Grab the name of the current user
    full_name_row2 = {}
    full_name_row = connection.execute('''
        SELECT fullname
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()

    if full_name_row is not None:
        full_name = full_name_row["fullname"]
    else:
        return flask.redirect('/accounts/login')


    context = {
        "fullname": full_name,
    } 
    return flask.jsonify(**context), 201

@scraps.app.route('/api/logout', methods=['POST'])
def api_logout():
    context = {
            'logname': None,
    }
    # Clear the session data
    if 'username' in flask.session:
        flask.session.clear()
    return flask.redirect(flask.url_for('show_accounts_login'))