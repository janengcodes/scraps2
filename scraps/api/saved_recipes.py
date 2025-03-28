"""REST API for likes."""
import flask
from flask import redirect
import scraps
import json

from scraps.api.exceptions import AuthException
from scraps.api.user import check_login

# GET method for the saved recipes 
@scraps.app.route('/api/v1/saved/saved_recipes/', methods=['GET'])
def get_saved_recipes():
    print("Get saved recipes called")
    ''' 
    Get all recipes in the database that have the same user id as the user
    Get all ingredients associated with the recipe 
    '''


# POST method for the saved recipes 
@scraps.app.route('/api/v1/saved_recipes/', methods=['POST'])
def api_saved_recipes():
    # Ensure that the user is logged in 
    check_login()
    logname = flask.session.get('username')

    # Parse the incoming JSON data
    json_string = flask.request.form['json_data']
    data_dict = json.loads(json_string)

    serialized_instructions = json.dumps(data_dict['instructions'])
    ingredients_list = data_dict["ingredients_list"]

    # Prepare the context for the response
    context = {
        "name": data_dict["name"],
        "ingredients_readable": data_dict["ingredients"],
        "instructions": data_dict["instructions"],
        "measurements": data_dict["measurements"],
        "items": data_dict["ingredients_list"]  # Ensure this is JSON serializable
    }

    # Insert recipe into the database
    connection = scraps.model.get_db()
    # NEED TO RESET DB
    cursor = connection.execute('''
        INSERT INTO recipes(username, name, instructions)
        VALUES (?, ?, ?)
    ''', (logname, data_dict['name'], serialized_instructions,))
    recipe_id = cursor.lastrowid

    # get pantry id
    cursor = connection.execute('''
        SELECT pantry_id FROM pantry WHERE username = ?
    ''', (logname,)).fetchone()

    pantry_id = cursor["pantry_id"]

    # insert ingredients into DB
    for item in ingredients_list:
        cursor = connection.execute('''
            INSERT INTO ingredients(ingredient_name, pantry_id)
            VALUES (?, ?)
        ''', (item, pantry_id,))
        
        ingredient_id = cursor.lastrowid
        
        cursor = connection.execute('''
        INSERT INTO recipe_ingredients(recipe_id, ingredient_id)
        VALUES (?, ?)
    ''', (recipe_id, ingredient_id))

    # Commit the changes to the database
    connection.commit()

    # Return the JSON response
    # Current endpoint: http://localhost:8000/api/v1/saved_recipes/
    # Want the endpoint to be in users/saved_recipes or smth

    # return flask.jsonify(**context), 201
    return flask.redirect(flask.url_for('saved_recipes'))
