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
    full_name_row = connection.execute('''
        SELECT first_name
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()

    if logname is None or full_name_row is None:
        print("logname is none")
        return flask.redirect('/accounts/login')

    context = {
        "username": logname,
    } 
    return flask.jsonify(**context), 201

