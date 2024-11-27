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

    context = {
        "name": data_dict["name"],
        "ingredients": data_dict["ingredients"],
        "instructions": data_dict["instructions"],
        "measurements": data_dict["measurements"],
        "items": data_dict["ingredients_list"]
    }

    # NEED TO FIND RECIPE ID

    # insert into database 
    connection = scraps.model.get_db()

    # problem: when do we add a recipe into the database and how do we account for re-generated recipes to avoid duplicates

    connection.execute(
        '''
        INSERT INTO saved_recipes(username, recipe_id)
        VALUES ()
        ''', ()
    )

# connection.execute('''
#         INSERT INTO users(username, password, fullname, email, filename)
#         VALUES (?, ?, ?, ?, ?)
#     ''', (username, password_db_string, fullname, email, uuid_basename))
    # stay on recipe page 
 
    return flask.jsonify(**context)
