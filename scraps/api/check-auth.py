"""REST API for likes."""
import hashlib
from flask import jsonify
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth


@scraps.app.route('/api/v1/likes/', methods=['POST'])
def check_login():
    """Likes."""
    logname = check_auth()

    postid = flask.request.args.get("postid", type=int)

    connection = scraps.model.get_db()
    # Post IDs that are out of range should return a 404 error.
    connection.execute('''
        SELECT *
        FROM posts
        WHERE postid = ?
    ''', (postid,)).fetchone()

    if postid is None:
        raise AuthException('Not Found', status_code=404)

    # If the like already exists, return the like object with a 200 response.
    like_exists = connection.execute('''
        SELECT likeid
        FROM likes
        WHERE owner = ?
        AND postid = ?
    ''', (logname, postid,)).fetchone()
    # Check if the like already exists
    already_exists = False
    if like_exists:
        already_exists = True
        likeid = like_exists['likeid']
    if not already_exists:
        # Create one like for a specific post. Return 201 on success. Example:
        connection.execute('''
            INSERT INTO likes (owner, postid)
            VALUES (?, ?)
        ''', (logname, postid))
        # get the likeid for newest like
        new_likeid = connection.execute('''
            SELECT likeid
            FROM likes
            WHERE owner = ?
            AND postid = ?
        ''', (logname, postid,)).fetchone()
        likeid = new_likeid['likeid']
    context = {
        "likeid": likeid,
        "url": "/api/v1/likes/" + str(likeid) + "/"
    }
    if already_exists:
        return flask.jsonify(**context), 200
    return flask.jsonify(**context), 201