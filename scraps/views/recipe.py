import flask
from flask import redirect, render_template, Flask, jsonify
import scraps
import json
import google.generativeai as genai
app = Flask(__name__)

# flask --app scraps --debug run --host 0.0.0.0 --port 8000
GOOGLE_API_KEY = 'AIzaSyCGu2PKA-ly-HGgkuiyswIPoVIUo64M9b4'

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
    json = []
    if (len(ingredients) != 0):
        response = model.generate_content("generate a recipe around these specific ingredients: "+ str(ingredients))
        print(response)
        output = response.text
        # generate a json object based 
        if response:
            db_json = model.generate_content("generate JSON object based on this recipe: " + str(response) + ". the keys are 'name', 'instructions', and 'ingredients' . do not add any extra characters that are '*', '#'. do not shorten or summarize the instructions ")
            # classify the meal 
            json = db_json.text
            json = model.generate_content("add a new key called 'meal_time' to this existing json: " + json +" and the value will be either be 'breakfast', 'lunch', or 'dinner' and assign a value based on this recipe " + str(response))
            # jsonify in api 
            json_data = json.text
            # clean text and pass relevant information into context
            print(json_data)
            

    context = {
        'recipe': output,
        'json': json_data
    }
    return render_template('recipe.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
