"""REST API for retrieving saved recipes for React."""
import flask
from flask import redirect
import scraps
import json
import spacy
import re
import inflect

from scraps.api.exceptions import AuthException
from scraps.api.user import check_login

# load spacy model for ingredient extraction
nlp = spacy.load("en_core_web_sm")
p = inflect.engine()

@scraps.app.route('/api/saved_recipes/', methods=['GET'])
def get_saved_recipes():
    logname = flask.session.get('username')
    check_login()

    connection = scraps.model.get_db()

    query = ''' 
    SELECT recipe_id, recipe_name
    FROM recipes
    WHERE username = ?
    '''
    recipes = connection.execute(query, (logname,)).fetchall()

    recipe_list = [
        {"recipe_id": row["recipe_id"], "name": row["recipe_name"]}
        for row in recipes
    ]
    return flask.jsonify(recipe_list)

import re
import spacy
import inflect

nlp = spacy.load("en_core_web_sm")
p = inflect.engine()


# Extract the noun to compare against ingredients in the database 

def extract_noun(text):
    text = text.lower()
    text = re.sub(r'\([^)]*\)', '', text)
    text = text.replace(',', '')
    doc = nlp(text)

    ignore_words = {
        'cup', 'cups', 'tablespoon', 'tablespoons',
        'teaspoon', 'teaspoons', 'gram', 'grams',
        'ounce', 'ounces', 'optional', 'chopped', 'boneless',
        'sliced', 'diced', 'fresh', 'large', 'small'
    }

    ingredients = []

    for chunk in doc.noun_chunks:
        tokens = []
        for tok in chunk:
            if tok.like_num or tok.lower_ in ignore_words:
                continue
            if tok.pos_ in ['NOUN', 'PROPN', 'ADJ']:
                tokens.append(tok.text)
        if tokens:
            ingredients.append(' '.join(tokens))

    return ' '.join(ingredients)



# POST method for the saved recipes 
@scraps.app.route('/api/v1/saved_recipes/', methods=['POST'])
def api_saved_recipes():
    # Ensure that the user is logged in 
    check_login()
    logname = flask.session.get('username')

    # Parse the incoming JSON data
    json_string = flask.request.form['json_data']
    print("json_string api", json_string)
    
    # Safely parse JSON string to Python dict
    try:
        data_dict = json.loads(json_string)
    except json.JSONDecodeError:
        flask.abort(400, description="Invalid JSON data")
    
    print("data_dict api", data_dict)

    ''' 
    data_dict api {'name': 'Apricot and Fig Jam', 'ingredients': ['1 lb fresh apricots, pitted and chopped', '1 lb fresh figs, stemmed and chopped', '1 cup granulated sugar', '1/4 cup water', '1 tbsp lemon juice'], 'instructions': ['Combine the chopped apricots, figs, sugar, water, and lemon juice in a large pot over medium heat.', 'Bring the mixture to a boil, stirring constantly.', 'Reduce the heat to low and simmer for 45-60 minutes, or until the jam thickens, stirring occasionally.', 'Remove from heat and let cool slightly.', 'Transfer the jam to sterilized jars and seal tightly.', 'Process in a boiling water bath for 10 minutes to ensure proper sealing (optional).', 'Store in a cool, dark place.']}
    '''

    connection = scraps.model.get_db()

    serialized_instructions = json.dumps(data_dict['instructions'])

    # Save the recipe name and instruct ions into the database for the user
    cursor = connection.execute('''
        INSERT INTO recipes(username, recipe_name, instructions)
        VALUES (?, ?, ?)
    ''', (logname, data_dict['name'], serialized_instructions,))
    recipe_id = cursor.lastrowid

    # get pantry id
    cursor = connection.execute('''
        SELECT pantry_id FROM pantry WHERE username = ?
    ''', (logname,)).fetchone()


    ingredient_nouns = []
    # Save the ingredient measurements
    for item in data_dict['ingredients']:
        # First get the main ingredient name using spacy
        ingredient_noun = extract_noun(item)
        print(f"Ingredient: {item}, Ingredient Noun: {ingredient_noun}")
        ingredient_nouns.append(ingredient_nouns)
        # Save the main ingredient into the ingredients table 
        cursor = connection.execute('''
            INSERT INTO ingredients(ingredient_name)
            VALUES (?)
        ''', (ingredient_noun,))
        # Create an ingredient ID
        ingredient_id = cursor.lastrowid
        # Associate the ingredient name with the recipe 

        temp_cursor = connection.execute (
            '''
            INSERT INTO recipe_ingredients(recipe_id, ingredient_id)
            VALUES (?, ?)
            ''', (recipe_id, ingredient_id))

        # Save the ingredient measurement into the ingredient_measurements table 
        cursor = connection.execute('''
            INSERT INTO ingredient_measurements(ingredient_id, ingredient_measurement)
            VALUES (?, ?)
        ''', (ingredient_id, item,))

        # Associate the ingredient measurement with the recipe
        ingredient_measurement_id = cursor.lastrowid
        cursor = connection.execute('''
        INSERT INTO recipe_ingredient_measurements(recipe_id, ingredient_measurement_id)
        VALUES (?, ?)
        ''', (recipe_id, ingredient_measurement_id))
    # print(f"Ingredient nouns: {ingredient_nouns}")
    # Commit the changes to the database
    connection.commit()

    # Return the JSON response
    # Current endpoint: http://localhost:8000/api/v1/saved_recipes/
    # Want the endpoint to be in users/saved_recipes or smth

    # return flask.jsonify(**context), 201
    return flask.redirect(flask.url_for('saved_recipes'))
