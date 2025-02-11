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
        "SELECT f.first_name, f.last_name, f.email "
        "FROM users f "
        "WHERE f.username = ?",
        (username,),
    ).fetchall()

    if first_name is None:
        print(f"No user found with username: {username}; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Access the first name value
    print(first_name)

    # Render the user.html template
    context = {
        "logname": username,
        "first_name": first_name[0]['first_name'],
        "last_name": first_name[0]['last_name'],
        "email": first_name[0]['email'],
    }
    return flask.render_template('user.html', **context)
