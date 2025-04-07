import flask
import scraps

@scraps.app.route('/accounts/edit/<username>', methods=['GET'])
def show_edit_profile(username):
    if 'username' not in flask.session:
        print("User is not logged in; redirecting to login page.")
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    username = flask.session.get('username')
    
#   connection to sqlite
    connection = scraps.model.get_db()

    # form data
    # email = flask.request.form.get('email')
    # first_name = flask.request.form.get('first_name')
    # last_name = flask.request.form.get('last_name')
    # password = flask.request.form.get('password')
    # username = flask.request.form.get('username')
    allergen_name = flask.request.form.get('allergen')
    dietary_pref = flask.request.form.get('dietary_pref')

#   get all updated allergens
    allergens_list = connection.execute('''
        SELECT username, allergen_id
        FROM user_allergens
        WHERE username = ?
    ''', (username,)).fetchall()
    
    allegen_ids = []
    allergens = []

    for allergen in allergens_list:
        allegen_ids.append(allergen['allergen_id'])

    for id in allegen_ids:
        allergen_name = connection.execute('''
            SELECT allergen_name
            FROM allergens
            WHERE allergen_id = ?
        ''', (id,)).fetchone()
        print(allergen_name)
        allergens.append(allergen_name)
        
    context = {
        "logname": username,
        "allergens": allergens,
        # "dietary_prefs": dietary_prefs,
    }

    return flask.render_template('edit-profile.html', **context)



@scraps.app.route('/accounts/edit/<username>', methods=['POST'])
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
    allergen_name = flask.request.form.get('allergen')
    dietary_pref = flask.request.form.get('dietary_pref')
   
#    # check if allergen is in allergens table
    check_allergens = connection.execute('''
        SELECT COUNT(*)
        FROM allergens
        WHERE allergens.allergen_name = ?
    ''', (allergen_name,)).fetchall()
    print("CHECK ALLERGENS")
    print(check_allergens)
    print(check_allergens[0])

    # check if form is empty 
    
    if not check_allergens[0]['COUNT(*)']:
        # insert allergens into database, for allergens table and user_allergies table
        connection.execute('''
            INSERT INTO allergens(allergen_name)
            VALUES (?)
        ''', (allergen_name,))
            # get allergen id
        allergen_dictionary = connection.execute(
            '''
            SELECT allergen_id
            FROM allergens
            WHERE allergens.allergen_name = ?
            ''', (allergen_name,)).fetchone()


        connection.execute('''
            INSERT INTO user_allergens(username, allergen_id)
            VALUES (?, ?)
        ''', (username, allergen_dictionary['allergen_id']))

        
    else:
        print("User trying to put in duplicate allergy")

# get all updated allergens
    allergens_list = connection.execute('''
        SELECT username, allergen_id
        FROM user_allergens
        WHERE username = ?
    ''', (username,)).fetchall()
    
    allegen_ids = []
    allergens = []

    for allergen in allergens_list:
        allegen_ids.append(allergen['allergen_id'])



    for id in allegen_ids:
        allergen_name = connection.execute('''
            SELECT allergen_name
            FROM allergens
            WHERE allergen_id = ?
        ''', (id,)).fetchone()
        print(allergen_name)
        allergens.append(allergen_name)

    context = {
        "logname": username,
        "allergens": allergens,
        # "dietary_prefs": dietary_prefs,
    }



    return flask.render_template('edit-profile.html', **context)
    # edited_user_info = flask.request.form.getlist('ingredient')

