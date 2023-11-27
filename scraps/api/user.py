"""REST API for user."""
import flask
import scraps


@scraps.app.route('/api/v1/user/<string:username>', methods=['GET'])
def get_user(username):
    connection = scraps.model.get_db()

    cur = connection.execute(
        """
        SELECT fullname, filename, email, username, email
        FROM users
        WHERE username = ?
        """,
        (username, )
    )

    user = cur.fetchone()

    if not user:
        flask.abort(404)

    return flask.jsonify(**user)r<string:usernameuser_calendarusername
(
        """
        SELECT recipe_id, meal_time
        FROM calendar_events
        WHERE username = ?
        """,
        (username, )
    )

    temp = curr.fetchall()

    meals = []
    for i in temp:
        cur = connection.execute(
        "SELECT name, filename, cook_time "
        "FROM recipes "
        "WHERE recipe_id = ? ",
        (temp['recipe_id'], )
        )
        temp = cur.fetchall()
        comments.append(single_comment)

@scraps.app.route('api/v1/<string:username', methods=['GET'])
def get_user_saved(username):
    connection = scraps.model.get_db()
    
    curr = connection.execute(
        """
        SELECT recipe_id, meal_time
        FROM calendar_events
        WHERE username = ?
        """,
        (username, )
    )

    temp = curr.fetchall()

    meals = []
    for i in temp:
        cur = connection.execute(
        "SELECT name, filename, cook_time "
        "FROM recipes "
        "WHERE recipe_id = ? ",
        (temp['recipe_id'], )
        )
        temp = cur.fetchall()
        comments.append(single_comment)

