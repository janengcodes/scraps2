"""REST API for Pantry."""
import hashlib
from flask import jsonify
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth

import requests

@scraps.app.route('/api/pantry/<username>', methods=['GET'])
def get_pantry(username):
    """Check if a user is logged in"""
    logname = check_auth()

    context = {
        'example_variable': 'Hello, World!'
    }
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    # Get all pantry ingredients and render into a JSON file 
    # 1. Get the pantry id
    connection = scraps.model.get_db()

    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()

    # 2. Get ingredients associated with the pantry id 


    print("PANTRY ID IS", pantry['pantry_id'])
    context = {
        "pantry_id": pantry['pantry_id']
    }

    return flask.render_template("pantry.html", **{})
    return flask.jsonify(context), 201


# @scraps.app.route('/api/v1/likes/', methods=['POST'])
# def api_likes():
#     """Likes."""
#     logname = check_auth()

#     postid = flask.request.args.get("postid", type=int)

#     connection = disaster_relief.model.get_db()
#     # Post IDs that are out of range should return a 404 error.
#     post_id_check = connection.execute('''
#         SELECT *
#         FROM posts
#         WHERE postid = ?
#     ''', (postid,)).fetchone()

#     if post_id_check is None:
#         raise AuthException('Not Found', status_code=404)
#     # If the like already exists, return the like object with a 200 response.
#     like_exists = connection.execute('''
#         SELECT likeid
#         FROM likes
#         WHERE owner = ?
#         AND postid = ?
#     ''', (logname, postid,)).fetchone()
#     # Check if the like already exists
#     already_exists = False
#     if like_exists:
#         already_exists = True
#         likeid = like_exists['likeid']
#     if not already_exists:
#         # Create one like for a specific post. Return 201 on success. Example:
#         connection.execute('''
#             INSERT INTO likes (owner, postid)
#             VALUES (?, ?)
#         ''', (logname, postid))
#         # get the likeid for newest like
#         new_likeid = connection.execute('''
#             SELECT likeid
#             FROM likes
#             WHERE owner = ?
#             AND postid = ?
#         ''', (logname, postid,)).fetchone()
#         likeid = new_likeid['likeid']
#     context = {
#         "likeid": likeid,
#         "url": "/api/v1/likes/" + str(likeid) + "/"
#     }
#     if already_exists:
#         return flask.jsonify(**context), 200
#     return flask.jsonify(**context), 201
