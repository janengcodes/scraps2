"""
Scraps accounts view.
"""
import pathlib
import uuid
import os
import hashlib
import flask
from flask import request, abort, render_template
import scraps


# HANDLE GET REQUESTS
@scraps.app.route("/accounts/login/", methods=["GET"])
def show_accounts_login():
    """Display /accounts/login/ route."""
    # Redirect to index if logged in
    target = flask.request.args.get('target', '/dashboard/')
    if 'username' in flask.session:
        return flask.redirect(target)
    return flask.render_template("login.html", **{})

@scraps.app.route("/accounts/login_retry/", methods=["GET"])
def show_accounts_login_retry():
    """Display /accounts/login/ route."""
    # Redirect to index if logged in
    target = flask.request.args.get('target', '/dashboard/')
    if 'username' in flask.session:
        return flask.redirect(target)
    return flask.render_template("login_retry.html", **{})


@scraps.app.route("/accounts/signup/", methods=["GET"])
def show_accounts_sign_up():
    """Display /accounts/login/ route."""
    # Redirect to index if logged in
    if 'username' in flask.session:
        print("{} in session", flask.session['username'])
        return flask.redirect(flask.url_for('index'))
    return flask.render_template("sign-up.html", **{})


# HANDLE POST REQUESTS
@scraps.app.route('/accounts/', methods=['POST'])
def post_account():
    """Display /accounts/ route."""
    operation = request.form.get('operation')
    if operation == 'create':
        create()
    # elif operation == 'delete':
    #     delete()
    # elif operation == 'edit_account':
    #     edit_account()
    # elif operation == 'update_password':
    #     update_password()
    elif operation == 'login':
        login()
    target = flask.request.args.get('target', '/dashboard/')
    return flask.redirect(target)


def create():
    """Create an account."""
    # Connect to database
    connection = scraps.model.get_db()
    first_name = flask.request.form["first_name"]
    last_name = flask.request.form["last_name"]
    email = flask.request.form["email"]
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    # If any fields are empty, abort
    if not username or not password:
        flask.abort(400)

    # Check if username already exists in database
    check_username = connection.execute('''
        SELECT COUNT(*)
        FROM users
        WHERE users.username = ?
    ''', (username,)).fetchall()

    # Check if email already exists in database
    check_email = connection.execute('''
        SELECT COUNT(*)
        FROM users
        WHERE users.username = ?
    ''', (email,)).fetchall()

    if check_username[0]['COUNT(*)'] == 1 or check_email[0]['COUNT(*)'] == 1:
        abort(409)

    # Set up flask session and log the user in
    flask.session['username'] = username

  
    if len(username) == 0 or len(password) == 0:
        abort(404)
    if len(first_name) == 0 or len(last_name) == 0 or len(email) == 0:
        abort(404)

    # Generate password hash
    hash_obj = hashlib.new('sha512')
    password_salted = uuid.uuid4().hex + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join(['sha512',
                                  uuid.uuid4().hex, hash_obj.hexdigest()])

    # Generate password hash
    password_db_string = scraps.model.gen_password_hash(password)

    # Create user in database
    # TODO: add more values to database entry

    connection.execute('''
        INSERT INTO users(username, first_name, last_name, email, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, first_name, last_name, email, password_db_string))

    # create a pantry for new user
    connection.execute('''
        INSERT INTO pantry(username)
        VALUES (?)
    ''', (username,))

    # create a meal calendar for new user
    connection.execute('''
        INSERT INTO meal_calendar_users(username)
        VALUES (?)
    ''', (username,))



def login():
    """Login a user."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    connection = scraps.model.get_db()
    # Handle the login form submission
    username = request.form.get('username')
    password = request.form.get('password')

    # If the username or password fields are empty, abort(400).
    if len(username) == 0 or len(password) == 0:
        return flask.redirect('/accounts/login/')
        abort(400)

    # username authentification
    username_check = connection.execute('''
        SELECT COUNT(*)
        FROM users
        WHERE username = ?
    ''', (username,),).fetchone()
    # If username doesn't exist
    if username_check['COUNT(*)'] == 0:
        print("username check failed")
        return flask.redirect('/accounts/login/')
        abort(403)
    # grab salt
    real_password = connection.execute('''
        SELECT password
        FROM users
        WHERE username = ?
    ''', (username,),).fetchone()
    parts = real_password['password'].split('$')
    salt = parts[1]
    algorithm = 'sha512'
    # salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    if password_db_string != real_password['password']:
        print("password check failed")
        return flask.redirect('/accounts/login/')
        abort(400)


    # set a session cookie
    flask.session['username'] = username
    target = flask.request.args.get('target', '/dashboard/')

    return flask.redirect(target)




