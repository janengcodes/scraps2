"""REST API for likes."""
import flask
import scraps
import json

from scraps.api.exceptions import AuthException
from scraps.api.user import check_login


@scraps.app.route('/api/v1/saved_recipes/', methods=['POST'])
def api_saved_recipes():
    # Ensure that the user is logged in 
    check_login()

    # Parse the incoming JSON data
    json_string = flask.request.form['json_data']
    data_dict = json.loads(json_string)


    serialized_instructions = json.dumps(data_dict['instructions'])

    # Prepare the context for the response
    context = {
        "name": data_dict["name"],
        "ingredients": data_dict["ingredients"],
        "instructions": data_dict["instructions"],
        "measurements": data_dict["measurements"],
        "items": data_dict["ingredients_list"]  # Ensure this is JSON serializable
    }

    # Insert data into the database
    connection = scraps.model.get_db()
    cursor = connection.execute('''
        INSERT INTO recipes(name, instructions)
        VALUES (?, ?)
    ''', (data_dict['name'], serialized_instructions))
    
    # Fetch the auto-generated recipe ID
    recipe_id = cursor.lastrowid

    # Add the recipe ID to the context
    context["recipe_id"] = recipe_id

    # Commit the changes to the database
    connection.commit()

    # Return the JSON response
    # Current endpoint: http://localhost:8000/api/v1/saved_recipes/
    # Want the endpoint to be in users/saved_recipes or smth
    
    return flask.jsonify(**context), 201
