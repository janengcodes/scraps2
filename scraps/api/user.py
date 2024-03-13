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
    full_name = connection.execute('''
        SELECT fullname
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()

    context = {
        "fullname": full_name["fullname"],
    } 
    return flask.jsonify(**context), 201
