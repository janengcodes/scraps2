# """
# scraps accounts view.

# URLs include:
# /accounts/login/
# /accounts/auth/
# """
# import uuid
# import hashlib
# import pathlib
# import os
# import flask
# import scraps
# from scraps.views.index import check_login


# @scraps.app.route('/accounts/', methods=['POST'])
# def post_accounts():
#     """Process POST requests of type /accounts/<operation>/."""
#     op_name = flask.request.form.get('operation', 'create')
#     match op_name:
#         case 'login':
#             login()
#         case 'create':
#             create_account()
#         case 'delete':
#             delete_account()
#             return flask.redirect('/accounts/create/')
#         case 'edit_account':
#             edit_account()
#         case 'update_password':
#             update_password()
#             return flask.redirect('/accounts/edit/')

#     target = flask.request.args.get('target', '/')

#     # Always redirects to target after above logic
#     return flask.redirect(target)


# def login():
#     """Perform appropriate login checks."""
#     user = flask.request.form.get('username')
#     if user == '':
#         flask.abort(400)

#     entered_password = flask.request.form.get('password')
#     if entered_password == '':
#         flask.abort(400)
#     # First need to see if the inputted username is in the db
#     connection = scraps.model.get_db()
#     check_user = connection.execute(
#         ''' SELECT username, password
#             FROM users
#             WHERE username == ?
#         ''', (user,)
#     )
#     data = check_user.fetchone()

#     if data is None:
#         flask.abort(403)    # Not a valid username

#     # Retrieve the salt used in the password in the db
#     input_split = data["password"].split('$', 3)
#     salt = input_split[1]
#     # Hash the password the user submitted
#     algorithm = 'sha512'
#     hash_obj = hashlib.new(algorithm)
#     password_salted = salt + entered_password
#     hash_obj.update(password_salted.encode('utf-8'))
#     entered_password_hash = hash_obj.hexdigest()
#     entered_password_db_string = "$".join(
#        [algorithm, salt, entered_password_hash])

#     if not data["password"] == entered_password_db_string:
#         flask.abort(403)    # Password doesn't match

#     # This line officially logs the user in
#     flask.session['username'] = user


# @scraps.app.route('/accounts/login/')
# def show_login():
#     """Display /accounts/login/ route."""
#     if check_login():
#         return flask.redirect('/')

#     return '''
#         <!DOCTYPE html>
#         <head>
#             <title>scraps</title>
#         </head>
#         <body>
#             <span class = "insta_name"> <a href ="/">scraps</a></span>
#             <form action="/accounts/?target=/" method="post"
#                 enctype="multipart/form-data">
#                 <input type="text" name="username" required/>
#                 <input type="password" name="password" required/>
#                 <input type="submit" value="login"/>
#                 <input type="hidden" name="operation" value="login"/>
#             </form>
#             <a href="/accounts/create/">Don't have an account? Sign up</a>
#         </body>
#     '''


# @scraps.app.route('/accounts/logout/', methods=['POST'])
# def logout():
#     """Log user out."""
#     if check_login():
#         # print("DEBUG Logout:", flask.session['username'])
#         flask.session.clear()
#     return flask.redirect('/accounts/login/')


# @scraps.app.route('/accounts/auth/')
# def do_auth():
#     """Display /accounts/auth/ route."""
#     if 'username' in flask.session:
#         # User is logged in
#         return '', 200
#     flask.abort(403)


# @scraps.app.route('/accounts/create/')
# def get_create():
#     """Display /accounts/create/ route."""
#     if 'username' in flask.session:
#         return flask.redirect('/accounts/edit/')

#     return '''
#         <!DOCTYPE html>
#         <head>
#             <title>scraps</title>
#         </head>
#         <body>
#             <nav>
#             <a href ="/">scraps</a>
#             </nav>

#             <h1>Create Account</h1>
#             <form action="/accounts/?target=/" method="post"
#                 enctype="multipart/form-data">
#                 Photo <input type="file" name="file" required/><br>
#                 Full Name <input type="text" name="fullname" required/> <br>
#                 Username <input type="text" name="username" required/> <br>
#                 Email <input type="text" name="email" required/> <br>
#                 Password <input type="password" name="password" required/> <br>
#                 <input type="submit" name="signup" value="sign up"/><br>
#                 <input type="hidden" name="operation" value="create"/><br>
#         </form>
#         Have an account? <a href = "/accounts/login/"> Login </a>
#         </body>
#     '''


# def create_account():
#     """Add user into database."""
#     # Get user input from the POST request

#     user = flask.request.form.get('username')
#     password = flask.request.form.get('password')

#     # create unique filename
#     fileobj = flask.request.files["file"]
#     # print("heere:",fileobj)
#     if fileobj is not None:
#         profile_pic = fileobj.filename
#         stem = uuid.uuid4().hex
#         suffix = pathlib.Path(profile_pic).suffix.lower()
#         if suffix[1:] not in scraps.app.config["ALLOWED_EXTENSIONS"]:
#             flask.abort(400)
#         uuid_basename = f"{stem}{suffix}"
#         # save to disk
#         path = (os.path.join(scraps.app.config["UPLOAD_FOLDER"],
#                 uuid_basename))
#         fileobj.save(path)
#     else:
#         flask.abort(400)
#     # check if fields are empty
#     if (user == '' or password == ''
#             or flask.request.form.get('fullname') == '' or
#             flask.request.form.get('email') == ''):
#         flask.abort(400)

#     # compute hashed password
#     salt = uuid.uuid4().hex
#     hash_obj = hashlib.new('sha512')
#     password_salted = salt + password
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     password_db_string = "$".join(['sha512', salt, password_hash])

#     # check if username already exists in database
#     connection = scraps.model.get_db()
#     check_user = connection.execute(
#         ''' SELECT username
#             FROM users
#             WHERE username == ?
#         ''', (user,)
#     ).fetchone()

#     # print(check_user['username'])

#     # error check
#     if check_user:
#         flask.abort(409)

#     flask.session['username'] = user
#     connection.execute(
#         '''INSERT INTO users(username, fullname, email, filename, password)
#           VALUES(?, ?, ?, ?, ?)
#         ''', (user, flask.request.form.get('fullname'),
#               flask.request.form.get('email'),
#               uuid_basename, password_db_string,)
#     )


# def delete_account():
#     """Delete user from database."""
#     if not check_login():
#         flask.abort(403)
#     username = flask.session.get('username')
#     connection = scraps.model.get_db()

#     # all images related to user
#     post_images = connection.execute(
#         '''
#         SELECT
#         p.owner AS post_owner,
#         p.filename AS post_filename
#         FROM posts p
#         JOIN users u ON u.username = p.owner
#         WHERE p.owner = ?
#         ''', (username,)
#       ).fetchall()

#     # user profile pic
#     profile_pic = connection.execute(
#         '''
#         SELECT filename
#         FROM users
#         WHERE username = ?
#         ''', (username,)
#       ).fetchone()

#     # delete posts from file system
#     for image in post_images:
#         post_path = os.path.join(scraps.app.config['UPLOAD_FOLDER'],
#                                  image['post_filename'])
#         if os.path.exists(post_path):
#             os.remove(post_path)

#     # delete profile picture from file system
#     profile_path = os.path.join(scraps.app.config['UPLOAD_FOLDER'],
#                                 profile_pic['filename'])
#     if os.path.exists(profile_path):
#         os.remove(profile_path)

#     # update database
#     connection.execute(
#         ''' DELETE FROM users
#             WHERE username == ?
#         ''', (username, )
#     )
#     # reset flask session
#     flask.session.clear()


# @scraps.app.route('/accounts/delete/')
# def get_delete():
#     """Display /accounts/delete/ route."""
#     if 'username' not in flask.session:
#         return flask.redirect('/accounts/login/')

#     username = flask.session.get('username')
#     return f'''
#     <!DOCTYPE html>
#     <head>
#         <title>scraps</title>
#     </head>
#     <body>
#         <a href ="/">scraps</a>
#         <a href = "/explore/">explore</a>
#         <a href = "/users/{ username }/">{ username }</a>
#         <h1>{ username }</h1>
#         <form action="/accounts/?target=/accounts/create/"
#             method="post" enctype="multipart/form-data">
#             <input type="submit" name="delete" value="confirm delete account"/>
#             <input type="hidden" name="operation" value="delete"/>
#         </form>
#     </body>
#     '''


# @scraps.app.route('/accounts/edit/')
# def get_edit_account():
#     """Display /accounts/edit/ route."""
#     if not check_login():
#         return flask.redirect('/accounts/login/')

#     logname = flask.session['username']

#     connection = scraps.model.get_db()
#     # get user profile picture
#     user = connection.execute(
#         ''' SELECT u.username AS username,
#             u.filename AS owner_profile_picture,
#             u.email AS email,
#             u.fullname AS fullname
#             FROM users u
#             WHERE u.username == ?
#         ''', (logname,)
#     ).fetchone()

#     context = {
#         "user": user,
#         "logname": logname
#     }
#     return flask.render_template("edit.html", **context)


# def edit_account():
#     """Edit account."""
#     if not check_login():
#         flask.abort(403)
#     user = flask.session['username']

#     fullname = flask.request.form.get('fullname')
#     email = flask.request.form.get('email')

#     connection = scraps.model.get_db()

#     # convert filename
#     fileobj = flask.request.files["file"]

#     if fileobj:
#         profile_pic = fileobj.filename
#         stem = uuid.uuid4().hex
#         suffix = pathlib.Path(profile_pic).suffix.lower()
#         if suffix[1:] not in scraps.app.config["ALLOWED_EXTENSIONS"]:
#             flask.abort(400)
#         uuid_basename = f"{stem}{suffix}"
#         # save to disk
#         path = scraps.app.config["UPLOAD_FOLDER"]/uuid_basename
#         fileobj.save(path)
#     else:
#         connection.execute(
#             ''' UPDATE users
#             SET fullname = ?, email = ?
#             WHERE username == ?
#         ''', (fullname, email, user,)
#         )
#         return

#     # error check
#     if fullname == '' or email == '':
#         flask.abort(400)

#     # get old profile pic image
#     image = connection.execute(
#         '''
#         SELECT filename
#         FROM users
#         WHERE username = ?
#         ''', (user,)
#     ).fetchone()

#     # delete old profile picture from file system
#     if fileobj:
#         profile_path = os.path.join(scraps.app.config['UPLOAD_FOLDER'],
#                                     image['filename'])
#         if os.path.exists(profile_path):
#             os.remove(profile_path)

#     # update database
#     connection.execute(
#       ''' UPDATE users
#           SET fullname = ?, email = ?, filename = ?
#           WHERE username == ?
#       ''', (fullname, email, uuid_basename, user,)
#     )

#     return


# @scraps.app.route('/accounts/password/')
# def get_password():
#     """Show account/password page."""
#     if not check_login():
#         return flask.redirect('/accounts/login/')
#     username = flask.session['username']
#     return f'''<!DOCTYPE html>
#     <head><title>scraps</title></head>
#     <body>
#     <a href ="/">scraps</a>
#         <a href = "/explore/">explore</a>
#         <a href = "/users/{ username }/">{ username }</a>
#     <form action="/accounts/?target=/accounts/edit/"
#             method="post" enctype="multipart/form-data">
#             <input type="password" name="password" required/> Password
#             <input type="password" name="new_password1" required/> New Password
#             <input type="password" name="new_password2"
#             required/> Retype New Password
#             <input type="submit" name="update_password" value="submit"/>
#             <input type="hidden" name="operation" value="update_password"/>
#         </form>
#     </body>'''


# def update_password():
#     """Change the password in data base."""
#     if not check_login():
#         flask.abort(403)
#     user = flask.session['username']
#     password = flask.request.form['password']
#     new_password1 = flask.request.form.get('new_password1')
#     new_password2 = flask.request.form.get('new_password2')

#     if password == '' or new_password1 == '' or new_password2 == '':
#         flask.abort(400)

#     # check if password matches password in database
#     connection = scraps.model.get_db()
#     db_password = connection.execute(
#         ''' SELECT username, password
#             FROM users
#             WHERE username == ?
#         ''', (user,)
#     )
#     data = db_password.fetchone()

#     # Retrieve the salt used in the password in the db
#     old_salt = data["password"].split('$', 3)[1]
#     # Hash the password the user submitted
#     hash_obj = hashlib.new('sha512')
#     password_salted = old_salt + password
#     hash_obj.update(password_salted.encode('utf-8'))
#     entered_password_hash = hash_obj.hexdigest()
#     entered_password_db_string = "$".join(
#         ['sha512', old_salt, entered_password_hash])

#     if not data["password"] == entered_password_db_string:
#         flask.abort(403)    # Password doesn't match

#     # check if they match
#     if new_password1 != new_password2:
#         flask.abort(401)

#     # hash new password
#     salt = uuid.uuid4().hex
#     hash_obj = hashlib.new('sha512')
#     password_salted = salt + new_password1
#     hash_obj.update(password_salted.encode('utf-8'))
#     password_hash = hash_obj.hexdigest()
#     password_db_string = "$".join(['sha512', salt, password_hash])

#     # update passwords
#     connection.execute(
#         ''' UPDATE users
#             SET password = ?
#             WHERE username == ?
#         ''', (password_db_string, user,)
#         )
