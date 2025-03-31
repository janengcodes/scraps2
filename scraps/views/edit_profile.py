import flask
import scraps

@scraps.app.route('/accounts/edit/<username>', methods=['GET'])
def edit(username):
    # Check if user is logged in
    if 'username' not in flask.session:
        print("User is not logged in; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Connect to the database
    connect = scraps.model.get_db()
    print(f"Route username: {username}")

    # Query the first_name of the user
    user_info = connect.execute(
        "SELECT f.first_name, f.last_name, f.email "
        "FROM users f "
        "WHERE f.username = ?",
        (username,),
    ).fetchall()

    if user_info is None:
        print(f"No user found with username: {username}; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Access the first name value
    print(user_info)

    # Render the user.html template
    context = {
        "logname": username,
        "first_name": user_info[0]['first_name'],
        "last_name": user_info[0]['last_name'],
        "email": user_info[0]['email'],
    }
    return flask.render_template('edit-profile.html', **context)


@scraps.app.route('/edit-user-info/', methods=['POST'])
def edit_user_info():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    username = flask.session.get('username')
    
#    connection to sqlite
    connection = scraps.model.get_db()

    # form data
    allergen = flask.request.form.get('allergen')
    dietary_pref = flask.request.form.get('dietary_pref')
   
   # check if allergen is in allergens table
    check_allergens = connection.execute('''
        SELECT COUNT(*)
        FROM allergens
        WHERE allergens.allergen_name = ?
    ''', (allergen,)).fetchall()
    
    # insert allergens into database, for allergens table and user_allergies table
    connection.execute('''
        INSERT INTO allergens(allergen_name)
        VALUES (?)
    ''', (allergen,))

    connection.execute('''
        INSERT INTO user_allergens(username, allergen_id)
        VALUES (?, ?)
    ''', (username, allergen))

    # get all updated allergens
    allergens = connection.execute('''
        SELECT allergen_name
        FROM allergens
    ''').fetchall()

    context = {
        "logname": username,
        "allergens": allergens,
        # "dietary_prefs": dietary_prefs,
    }



    return flask.render_template('edit-profile.html', **context)
    # edited_user_info = flask.request.form.getlist('ingredient')

