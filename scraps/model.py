"""scraps model (database) API."""
import hashlib
import sqlite3
import flask
import scraps
import uuid


def http_authenticate(connection, input_password, input_username):
    """Authenticate for Rest API."""
    # check cookie
    cookie_login = False
    logname = ""
    if flask.session.get('username') is None:
        cookie_login = False
    else:
        cookie_login = True
        logname = flask.session['username']
    # check http header
    http_login = False
    if input_username is not None and input_password is not None:
        # get user password from database
        temp = get_pass(connection, input_username)
        if temp is not None:
            password_has = temp['password']
            password_part = password_has.split("$")
            algorithm = password_part[0]
            salt = password_part[1]
            hash_ob = hashlib.new(algorithm)
            input_password_salted = salt + input_password
            hash_ob.update(input_password_salted.encode('utf-8'))
            input_password_hash = hash_ob.hexdigest()

            if input_password_hash == password_part[2]:
                http_login = True
                logname = input_username

    if not cookie_login and not http_login:
        flask.abort(403)
    return logname


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = scraps.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory

        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")

    return flask.g.sqlite_db


@scraps.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


def get_pass(connection, input_username):
    """Get password."""
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (input_username, )
    )
    return cur.fetchone()


def get_logname():
    """Get logname."""
    if flask.request.authorization is not None:
        username = ""
        password = ""
    else:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
    connection = get_db()
    logname = http_authenticate(connection, password, username)
    return logname


def gen_password_hash(password):
    """Generate a salted SHA-512 hash given a password string."""
    salt = uuid.uuid4().hex
    sha_hash = hashlib.sha512()
    salted_password = salt + password
    sha_hash.update(salted_password.encode('utf-8'))
    password_hash = sha_hash.hexdigest()

    return "$".join(["sha512", salt, password_hash])
