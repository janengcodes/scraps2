import flask
import scraps


@scraps.app.route('/user/<username>/')
def show_user(username):
    # create a connection to the database in order to access the info
    # add some sql queries here 
    # username = flask.session['username']
    
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    connect = scraps.model.get_db()
    fullname = connect.execute(
        "SELECT f.fullname "
        "FROM users f "
        "WHERE f.username = ?",
        (username,),).fetchall()

    context = {
        "logname": "username"
    }
    return flask.render_template('user.html', **context)
