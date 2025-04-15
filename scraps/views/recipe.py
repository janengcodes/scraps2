import flask
from flask import redirect, render_template, Flask, jsonify
import scraps
import json
import google.generativeai as genai
app = Flask(__name__)
from dotenv import load_dotenv
import os
import re 

from google.api_core.exceptions import InternalServerError
import requests  # Assuming you're using requests for HTTP requests


load_dotenv()
GOOGLE_API_KEY = "AIzaSyBR6I4jWemlklfjrkbadGelz15GJWrlXDM"
# print(GOOGLE_API_KEY)

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

    # Create an array of ingredient ids 
    ingredient_ids = []
    for ingredient in ingredients:
        ingredient_id = connection.execute('''
            SELECT ingredient_id FROM ingredients WHERE ingredient_name = ?
        ''', (ingredient,)).fetchone()
        ingredient_ids.append(ingredient_id['ingredient_id'])
    

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


    if len(ingredients) != 0:
        # Base prompt for recipe generation
        base_prompt = f"""
        Your task is to generate a recipe using the following ingredients: {', '.join(ingredients)}.
        """

        if allergens:
            base_prompt += f"Avoid using any of these allergens: {', '.join(allergens)}.\n"

        base_prompt += """
        Your response must be a JSON object in **exactly** this format:

        {
            "name": "Recipe name here",
            "ingredients": ["ingredient 1", "ingredient 2", "..."],
            "instructions": ["step 1", "step 2", "..."]
        }

        - Use a valid JSON format, no markdown or extra characters.
        - Do not include '*', '#', or additional formatting in the ingredient or instruction values.
        """

        response = model.generate_content(base_prompt)
        output = response.text
        print(response)

        if response:
            try:
                cleaned_output = clean(output)
                data_dict = json.loads(cleaned_output)
                print("DATA DICTIONARY")
                print(data_dict)

            except InternalServerError:
                # Retry with a more detailed instruction in case of an error
                retry_output = model.generate_content(
                    f"Based on this recipe: {output}, separate the recipe information into the format of a JSON object. "
                    "The keys are 'name', 'instructions', and 'ingredients'. The values for 'ingredients' and 'instructions' "
                    "should be formatted as a Python list. Do not add any extra characters such as '*', '#' or quotes for the value."
                )         
                data_dict = json.loads(clean(retry_output))
                print("DATA DICTIONARY")
                print(data_dict)
  

        context = {
            "name": data_dict["name"],
            "ingredients_list": data_dict["ingredients"],
            "instructions_list": data_dict["instructions"],
            "json": json.dumps(data_dict),
            "output": output,
        }

        return render_template('recipe.html', **context)
            
def clean(text):
    # Remove markdown bullets or extra formatting
    text = re.sub(r'[*#`]', '', text)
    
    # Replace smart quotes with normal quotes
    text = text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    
    # Remove leading/trailing whitespace
    text = text.strip()

    # Make sure it starts and ends with braces
    if not text.startswith('{'):
        text = text[text.find('{'):]
    if not text.endswith('}'):
        text = text[:text.rfind('}') + 1]

    return text
def show_recipe(json_data):
    context = {
        "json_data": json_data
    }
    return render_template('recipe.html', **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
