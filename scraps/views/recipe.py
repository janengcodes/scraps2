import flask
from flask import redirect, render_template, Flask, jsonify
import scraps
import json
import google.generativeai as genai
app = Flask(__name__)

from google.api_core.exceptions import InternalServerError
import requests  # Assuming you're using requests for HTTP requests


# flask --app scraps --debug run --host 0.0.0.0 --port 8000
GOOGLE_API_KEY = 'AIzaSyAVn-iA_a0wmmnNGs2sYKO8kfOw9odhc8o'

model = None

def initialize_generative_model():
    """Initialize the GenerativeModel with the specified character."""
    global model
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        "models/gemini-1.5-pro-latest"
    )

@scraps.app.route('/recipe/', methods=['POST'])
def recipe():
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))

    username = flask.session.get('username')

    initialize_generative_model()
    # global ingredients 
    ingredients = flask.request.form.getlist('ingredient')
    output = ""
    json_string = []
    # Put the ingredients into the user's pantry 
    # Create a connection to the database 

    connection = scraps.model.get_db()


    # INGREDIENTS ['Tomatoes', 'Arugula']
    user_pantry = connection.execute('''
        SELECT pantry_id FROM pantry WHERE username = ?
    ''', (username,)).fetchone()
    pantry_id = user_pantry['pantry_id']

    print("PANTRY ID", pantry_id)

    # Create an array of ingredient ids 
    ingredient_ids = []
    for ingredient in ingredients:
        ingredient_id = connection.execute('''
            SELECT ingredient_id FROM ingredients WHERE ingredient_name = ?
        ''', (ingredient,)).fetchone()
        ingredient_ids.append(ingredient_id['ingredient_id'])
    
    print("INGREDIENTS", ingredients)
    print("INGREDIENT IDS", ingredient_ids)

    # Insert the ingredients into the pantry
    for ingredient_id in ingredient_ids:
        connection.execute('''
            INSERT OR IGNORE INTO pantry_ingredients(pantry_id, ingredient_id)
            VALUES (?, ?)
        ''', (pantry_id, ingredient_id))

    
    
    # Check that the ingredients were added to the pantry
    pantry_ingredients = connection.execute('''
        SELECT ingredient_id FROM pantry_ingredients WHERE pantry_id = ?
    ''', (pantry_id,)).fetchall()


    #connor working on allergen stuff here:
    # Check allergens for the user
    user_allergens = connection.execute('''
        SELECT allergen_name FROM allergens
        JOIN user_allergens ON allergens.allergen_id = user_allergens.allergen_id
        WHERE user_allergens.username = ?
    ''', (username,)).fetchall()
    allergens = [row['allergen_name'] for row in user_allergens]



    if (len(ingredients) != 0):
        if allergens:
            response = model.generate_content("Please generate a recipe around these specific ingredients: "+ str(ingredients) + ". Avoid using any of these allergens: " + ', '.join(allergens) + ".")
        else:
            response = model.generate_content("Please generate a recipe around these specific ingredients: "+ str(ingredients) + ".")
        print(response)
        output = response.text
        # generate a json object based 
        if response:
            try: 
                db_json = model.generate_content("Based on this recipe: " + str(response) + ", separate the recipe information into the format of a JSON object. the keys are 'name', 'instructions', and 'ingredients'. the values for 'ingredients' and 'instructions' should be formatted as a python list. do not add any extra characters that are '*', '#' or quotes for the value ")
                # separate measurements from ingredients
                json_string = db_json.text
                print(json_string)
                json_string = model.generate_content("Please add a two new keys called 'measurements' and 'ingredients_list' to this existing json: " + json_string +" The measurement list should contain the numerical amount of each respective ingredient.")
                # jsonify in api 
                json_data = json_string.text
                print(json_data)
                # clean text and pass relevant information into context
                json_data = clean(json_data)
                data_dict = json.loads(json_data)
                print("dict")
                print(data_dict)

            except InternalServerError as e:
                db_json = model.generate_content("Based on this recipe: " + str(response) + ", separate the recipe information into the format of a JSON object. the keys are 'name', 'instructions', and 'ingredients'. the values for 'ingredients' and 'instructions' should be formatted as a python list. do not add any extra characters that are '*', '#' or quotes for the value ")
                # classify the meal 
                json_string = db_json.text
                json_string = model.generate_content("Please add a two new keys called 'measurements' and 'ingredients_list' to this existing json: " + json_string +" Each measurement and it's unit of measurement (if there is one) should match its respective ingredient at each index. the ingredients_list should not include any measurements or units of measurement.")
                # jsonify in api 
                json_data = json_string.text
                print(json_data)
                # clean text and pass relevant information into context
                json_data = clean(json_data)
                data_dict = json.loads(json_data)
                print("dict")
                print(data_dict)    
    
    context = {
        "name": data_dict["name"],
        "ingredients_list": data_dict["ingredients"],
        "instructions_list": data_dict["instructions"],
        'json': json_data,
        'output': output
    }
    return render_template('recipe.html', **context)
            
def clean(input_text):
    # remove newline (\n) and carriage return (\r) characters
    cleaned_text = input_text.replace('\n', '').replace('\r', '').replace('\\', '')

    # find the start and end indices of the content within curly braces ({})
    start_index = cleaned_text.find('{')
    end_index = cleaned_text.rfind('}') + 1

    # extract the text within curly braces
    extracted_text = cleaned_text[start_index:end_index].strip()

    return extracted_text

def show_recipe(json_data):
    context = {
        "json_data": json_data
    }
    return render_template('recipe.html', **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
