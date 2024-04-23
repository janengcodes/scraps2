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
    json_string = []
    if (len(ingredients) != 0):
        response = model.generate_content("generate a recipe around these specific ingredients: "+ str(ingredients))
        print(response)
        output = response.text
        # generate a json object based 
        if response:
            db_json = model.generate_content("based on this recipe: " + str(response) + " separate the recipe information into the format of a JSON object. the keys are 'name', 'instructions', and 'ingredients' . do not add any extra characters that are '*', '#' or quotes for the value ")
            # classify the meal 
            json_string = db_json.text
            json_string = model.generate_content("add a new key called 'meal_time' to this existing json: " + json_string +" and the value will be either be 'breakfast', 'lunch', or 'dinner' and assign a value based on this recipe " + str(response))
            # jsonify in api 
            json_data = json_string.text
            print(json_data)
            # clean text and pass relevant information into context
            json_data = clean(json_data)
            data_dict = json.loads(json_data)
            

            ingredients_list = clean_ingredients(data_dict["ingredients"])
            print("ingredients")
            print(ingredients_list)

            instructions_list = clean_instructions(data_dict["instructions"])
    

    
    context = {
        "name": data_dict["name"],
        "ingredients_list": ingredients_list,
        "instructions_list": instructions_list,
        "meal_time": data_dict["meal_time"],
        'json': json_data
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

def clean_ingredients(text):
    # Remove leading and trailing brackets [ ] and strip any extra whitespace
    cleaned_text = text.strip('[]').strip()

    # Initialize variables
    items_list = []
    current_item = ''

    # Iterate through each character in the cleaned text
    for char in cleaned_text:
        if char.isdigit():  # Check if the character is a digit (part of a number)
            if current_item:  # If there's an existing item, add it to the list
                items_list.append(current_item.strip())
            # Start a new item with the found digit as the delimiter
            current_item = char
        else:
            current_item += char  # Add character to the current item

    # Add the last item to the list
    if current_item:
        items_list.append(current_item.strip())

    return items_list

def clean_instructions(text):
    # Remove leading and trailing brackets [ ] and strip any extra whitespace
    cleaned_text = text.strip('[]').strip()

    # Split the cleaned text into individual items based on commas and trim whitespace
    items_list = [item.strip().strip("'") for item in cleaned_text.split('.')]

    return items_list
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
