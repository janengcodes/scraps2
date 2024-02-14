"""REST API for likes."""
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth


@scraps.app.route('/api/v1/saved_recipes/', methods=['GET'])
def api_saved_recipes():
    
    logname = check_auth()

    # postid = flask.request.args.get("postid", type=int)

    # connection = scraps.model.get_db()
   
    context = {
        "saved_recipes": "omg hi im a recipe",
        "logname": logname
    }
   
    return flask.jsonify(**context)


