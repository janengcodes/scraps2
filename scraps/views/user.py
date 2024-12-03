import flask
import scraps


@scraps.app.route('/user/<username>/')
def show_user(username):
    # Check if user is logged in
    if 'username' not in flask.session:
        print("User is not logged in; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Connect to the database
    connect = scraps.model.get_db()
    print(f"Route username: {username}")

    # Query the first_name of the user
    first_name = connect.execute(
        "SELECT f.first_name "
        "FROM users f "
        "WHERE f.username = ?",
        (username,),
    ).fetchone()

    if first_name is None:
        print(f"No user found with username: {username}; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Access the first name value
    first_name_value = first_name['first_name']

    # Render the user.html template
    context = {
        "logname": first_name_value
    }
    return flask.render_template('user.html', **context)
