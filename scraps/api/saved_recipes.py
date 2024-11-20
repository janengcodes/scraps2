"""REST API for likes."""
import flask
import scraps
import json

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth


@scraps.app.route('/api/v1/saved_recipes/', methods=['POST'])
def api_saved_recipes():
    
    logname = check_auth()

    json_string = flask.request.form['json_data']
    data_dict = json.loads(json_string)

    # print(json)

    context = {
        "name": data_dict["name"],
        "ingredients": data_dict["ingredients"],
        "instructions": data_dict["instructions"],
        "measurements": data_dict["measurements"],
        "items": data_dict["ingredients_list"]
    }

    # insert into database 


    # stay on recipe page 
 
    return flask.jsonify(**context)
