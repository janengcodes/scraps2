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
    if logname is None:
        print("line 17")
        print("in check login, logname is none!!")
        return flask.redirect('/accounts/login_retry')\
    
    connection = scraps.model.get_db()
    # Grab the name of the current user
    full_name_check = connection.execute('''
        SELECT username
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()

    if logname is None or full_name_check is None:
        print("Full name check failed. Logname is:", logname)
        return flask.redirect('/accounts/login_retry')

    context = {
        "username": logname,
    } 
    return flask.jsonify(**context), 201

