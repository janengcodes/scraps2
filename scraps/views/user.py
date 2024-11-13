import flask
import scraps


@scraps.app.route('/user/')
def show_user():
    # create a connection to the database in order to access the info
    # add some sql queries here 
    # username = flask.session['username']

    context = {
        "logname": "jane"
    }
    return flask.render_template('user.html', **context)
