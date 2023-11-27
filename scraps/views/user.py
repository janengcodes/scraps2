import flask
import scraps


@scraps.app.route('/user/')
def show_user():
    # create a connection to the database in order to access the info
    # add some sql queries here 
    context = {
        # fill this in with info from the database that will fill in the template
    }
    return flask.render_template('user.html', **context)
