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
    
    # #dietary pref stuff
    # if dietary_pref:
    #     dietary_record = connection.execute('''
    #         SELECT dietary_id FROM dietary_prefs WHERE dietary_name = ?
    #     ''', (dietary_pref,)).fetchone()

    #     if not dietary_record:
    #         connection.execute('''
    #             INSERT INTO dietary_prefs (dietary_name) VALUES (?)
    #         ''', (dietary_pref,))
    #         dietary_record = connection.execute('''
    #             SELECT dietary_id FROM dietary_prefs WHERE dietary_name = ?
    #         ''', (dietary_pref,)).fetchone()

    #     # Link user to dietary preference if not already linked
    #     exists = connection.execute('''
    #         SELECT COUNT(*) FROM user_dietary_prefs WHERE username = ? AND dietary_id = ?
    #     ''', (username, dietary_record['dietary_id'])).fetchone()

    #     if exists['COUNT(*)'] == 0:
    #         connection.execute('''
    #             INSERT INTO user_dietary_prefs (username, dietary_id) VALUES (?, ?)
    #         ''', (username, dietary_record['dietary_id']))

    # user_dietary_prefs = connection.execute('''
    #     SELECT d.dietary_name
    #     FROM dietary_prefs d
    #     JOIN user_dietary_prefs udp ON d.dietary_id = udp.dietary_id
    #     WHERE udp.username = ?
    # ''', (username,)).fetchall()
    # dietary_prefs = [row['dietary_name'] for row in user_dietary_prefs]

    
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
    dietary_prefs = flask.request.form.get('dietary_pref')
   
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

# check_dietary = connection.execute('''
#     SELECT COUNT(*)
#     FROM dietary_prefs
#     WHERE dietary_name = ?
# ''', (dietary_name,)).fetchone()

# if dietary_name and not check_dietary['COUNT(*)']:
#     # Insert new dietary preference
#     connection.execute('''
#         INSERT INTO dietary_prefs (dietary_name)
#         VALUES (?)
#     ''', (dietary_name,))
    
#     dietary_id = connection.execute('''
#         SELECT dietary_id
#         FROM dietary_prefs
#         WHERE dietary_name = ?
#     ''', (dietary_name,)).fetchone()['dietary_id']

#     connection.execute('''
#         INSERT INTO user_dietary_prefs (username, dietary_id)
#         VALUES (?, ?)
#     ''', (username, dietary_id))

#     user_dietary_prefs = connection.execute('''
#         SELECT d.dietary_name
#         FROM dietary_prefs d
#         JOIN user_dietary_prefs udp ON d.dietary_id = udp.dietary_id
#         WHERE udp.username = ?
#     ''', (username,)).fetchall()
#     dietary_prefs = [row['dietary_name'] for row in user_dietary_prefs]


    context = {
        "logname": username,
        "allergens": allergens,
        #"dietary_prefs": dietary_prefs,
    }

    return flask.render_template('edit-profile.html', **context)
    # edited_user_info = flask.request.form.getlist('ingredient')

# original is above, modified is below(modified should allow allergens across multiple users) 
# def edit_user_info():
#     if 'username' not in flask.session:
#         return flask.redirect(flask.url_for('show_accounts_login'))
    
#     username = flask.session.get('username')
#     connection = scraps.model.get_db()

#     # Get form data
#     allergen_name = flask.request.form.get('allergen')
#     dietary_pref = flask.request.form.get('dietary_pref')
   
#     # Skip processing if no allergen provided
#     if allergen_name:
#         # Check if allergen exists in the allergens table
#         allergen_record = connection.execute('''
#             SELECT allergen_id
#             FROM allergens
#             WHERE allergen_name = ?
#         ''', (allergen_name,)).fetchone()
        
#         # Get allergen_id (create allergen if it doesn't exist)
#         if allergen_record:
#             allergen_id = allergen_record['allergen_id']
#         else:
#             # Insert new allergen into database
#             connection.execute('''
#                 INSERT INTO allergens(allergen_name)
#                 VALUES (?)
#             ''', (allergen_name,))
            
#             # Get the ID of the newly created allergen
#             allergen_id = connection.execute('''
#                 SELECT allergen_id
#                 FROM allergens
#                 WHERE allergen_name = ?
#             ''', (allergen_name,)).fetchone()['allergen_id']
        
#         # Check if user already has this allergen
#         user_allergen = connection.execute('''
#             SELECT COUNT(*)
#             FROM user_allergens
#             WHERE username = ? AND allergen_id = ?
#         ''', (username, allergen_id)).fetchone()
        
#         # Only add if user doesn't already have this allergen
#         if user_allergen['COUNT(*)'] == 0:
#             connection.execute('''
#                 INSERT INTO user_allergens(username, allergen_id)
#                 VALUES (?, ?)
#             ''', (username, allergen_id))
#         else:
#             print(f"User {username} already has allergen {allergen_name}")

#     # Get all updated allergens for the user
#     allergens_list = connection.execute('''
#         SELECT a.allergen_name
#         FROM user_allergens ua
#         JOIN allergens a ON ua.allergen_id = a.allergen_id
#         WHERE ua.username = ?
#     ''', (username,)).fetchall()
    
#     context = {
#         "logname": username,
#         "allergens": allergens_list,
#         # "dietary_prefs": dietary_prefs,
#     }

#     return flask.render_template('edit-profile.html', **context)
