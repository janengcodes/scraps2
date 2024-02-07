"""This module provides the API functionality for the Insta485 project.

This module contains classes and functions for interacting
with the API of the Insta485
application. It handles various API endpoints and provides
exceptions for error handling.

"""
import hashlib
from flask import jsonify
import flask
import scraps


def check_logname_password(logname, password):
    """Check if logname and password are valid."""
    # Check if user exists
    connection = scraps.model.get_db()
    real_password = connection.execute('''
        SELECT password
        FROM users
        WHERE username = ?
    ''', (logname,),).fetchone()
    user = connection.execute('''
        SELECT *
        FROM users
        WHERE username = ?
    ''', (logname,)).fetchone()
    if user is None:
        print("user is none")
        raise AuthException('Forbidden', status_code=403)
    # Check if password matches
    # Use salt from old password and apply to current password
    parts = real_password['password'].split('$')
    salt = parts[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    print("print password db string", password_db_string)
    print("print real password", real_password['password'])
    if password_db_string != real_password['password']:
        raise AuthException('Forbidden', status_code=403)


def check_auth():
    """Check if user is authenticated."""
    if 'username' in flask.session:
        logname = flask.session.get('username')
        return logname
    # Otherwise, try get auth from http request
    if 'Authorization' in flask.request.headers:
        logname = flask.request.authorization['username']
        password = flask.request.authorization['password']
        check_logname_password(logname, password)
        return logname
        # password = flask.request.authorization['password']
        # do this: check password
    # Else redirect because you're not authenticated
    raise AuthException('Forbidden', status_code=403)


class AuthException(Exception):
    """Exception for authentication errors."""

    def __init__(self, message, status_code=None, payload=None):
        """Exception for authentication errors."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Doctring."""
        r_v = dict(())
        r_v['message'] = self.message
        r_v['status_code'] = self.status_code
        return r_v


@scraps.app.errorhandler(AuthException)
def handle_invalid_usage(error):
    """Doctring."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    # response.headers['Location'] = flask.url_for('login')
    return response
    # return response
    # flask.redirect(flask.url_for('login'))
