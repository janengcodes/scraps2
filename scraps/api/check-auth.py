"""REST API for likes."""
import hashlib
from flask import jsonify
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth


@scraps.app.route('/api/check-auth', methods=['POST'])
def check_login():
    logname = None
    """Check if a user is logged in"""
    logname = check_auth()

    connection = scraps.model.get_db()
    # Grab the name of the current user
    fullname =  connection.execute('''
        SELECT fullname
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()

    context = {
        "fullname": fullname,
    }
    return flask.jsonify(**context), 201