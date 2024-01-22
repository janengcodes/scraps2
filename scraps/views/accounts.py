"""
Scraps accounts view.
"""
import pathlib
import uuid
import os
import hashlib
import flask
from flask import request, abort
import scraps


# HANDLE GET REQUESTS
@scraps.app.route("/accounts/login/", methods=["GET"])
def show_accounts_login():
    """Display /accounts/login/ route."""
    # Redirect to index if logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('index'))
    return flask.render_template("login-test.html", **{})


@scraps.app.route("/accounts/signup/", methods=["GET"])
def show_accounts_sign_up():
    """Display /accounts/login/ route."""
    # Redirect to index if logged in
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('index'))
    return flask.render_template("signup-test.html", **{})


# HANDLE POST REQUESTS
@scraps.app.route('/accounts/', methods=['POST'])
def post_accounts():
    """Process POST requests of type /accounts/<operation>/."""
    op_name = flask.request.form.get('operation')
    match op_name:
        case 'create':
            create()
        case 'login':
            login()
        case 'logout':
            logout()

    target = flask.request.args.get('target', '/')

    # Always redirects to target after above logic
    return flask.redirect(target)


def create():
    """Create an account."""
    # Connect to database
    connection = scraps.model.get_db()
    fullname = flask.request.form["fullname"]
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
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    # TODO: Do we need to set an upload folder?
    path = scraps.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    # Check if any of fields are empty --> abort 404
    if len(username) == 0 or len(password) == 0:
        abort(404)
    if len(fullname) == 0 or len(email) == 0 or not filename:
        abort(404)

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
        INSERT INTO users(username, password, fullname, email, filename)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password_db_string, fullname, email, uuid_basename))



def login():
    """Authenticate a login into an account."""
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    # authenticate with given username and password
    logname = scraps.model.http_authenticate(flask.model.get_db,
                                             username,
                                             password)

    # log user in
    flask.session['username'] = logname


def logout():
    """Logout and clear cookies from an account."""
    flask.session.clear()

