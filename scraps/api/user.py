"""REST API for user."""
import flask
import scraps


@scraps.app.route('/api/v1/user/<string:username>', methods=['GET'])
def get_user():
    connection = scraps.model.get_db()
    username = scraps.model.get_logname()

    cur = connection.execute(
        """
        SELECT fullname, filename, email, username
        FROM users
        WHERE username = ?
        """,
        (username, )
    )

    user = cur.fetchone()

    if not user:
        flask.abort(404)

    return flask.jsonify(**user)
# <string:usernameuser_calendarusername


@scraps.app.route('api/v1/<string:username', methods=['GET'])
def get_user_saved(username):
    connection = scraps.model.get_db()

    curr = connection.execute(
        """
        SELECT C.recipe_id, c.meal_time, R.name, R.filename, R.cook_time
        FROM calendar_events C
        LEFT JOIN recipes R ON C.recipe_id = R.recipe_id
        WHERE username = ?
        """,
        (username, )
    )

    rec = curr.fetchall()

    return flask.jsonify(**rec)