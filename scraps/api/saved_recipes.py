"""REST API for likes."""
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth


@scraps.app.route('/api/v1/saved_recipes/', methods=['POST'])
def api_saved_recipes():
    
    logname = check_auth()

    # postid = flask.request.args.get("postid", type=int)

    # connection = scraps.model.get_db()
   
    context = {
        "saved_recipes": "omg hi im a recipe",
        "logname": logname
    }
    # redirect to user page or saved recipes screen
    return flask.jsonify(**context)


