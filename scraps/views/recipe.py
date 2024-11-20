import flask
from flask import redirect, render_template, Flask, jsonify
import scraps
import json
import google.generativeai as genai
app = Flask(__name__)

from google.api_core.exceptions import InternalServerError
import requests  # Assuming you're using requests for HTTP requests


# flask --app scraps --debug run --host 0.0.0.0 --port 8000
GOOGLE_API_KEY = 'AIzaSyDGLjSn7rKYIX_L990wAeMcYiWrmkzm3Mk'

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
    
    logname = flask.session.get('username')

    initialize_generative_model()
    # global ingredients 
    ingredients = flask.request.form.getlist('ingredient')
    print(ingredients)
    output = ""
    json_string = []
    if (len(ingredients) != 0):
        response = model.generate_content("generate a recipe around these specific ingredients: "+ str(ingredients))
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
                json_string = model.generate_content("Please add a two new keys called 'measurements' and 'ingredients_list' to this existing json: " + json_string +" Each measurement should match its respective ingredient at each index.")
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
    # Remove newline (\n) and carriage return (\r) characters
    cleaned_text = input_text.replace('\n', '').replace('\r', '').replace('\\', '')

    # Find the start and end indices of the content within curly braces ({})
    start_index = cleaned_text.find('{')
    end_index = cleaned_text.rfind('}') + 1

    # Extract the text within curly braces
    extracted_text = cleaned_text[start_index:end_index].strip()

    return extracted_text

'''
    clean algorithm pseudocode 

    based on output string 

    look for ** <text> ** 
        - make <text> the key
        - grab everything that follows and make that the value 

    then have the api write the html for each dictionary item?
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
