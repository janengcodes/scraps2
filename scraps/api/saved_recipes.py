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
    json_data = clean_and_extract_text(json_string)
    data_dict = json.loads(json_data)

    print(json)

    context = {
        # "name": json_data
        # "ingredients": extracted["ingredients"],
        # "instructions": extracted["instructions"],
        # "meal_time": extracted["meal_time"]
        "name": data_dict["name"],
        "ingredients": data_dict["ingredients"],
        "instructions": data_dict["instructions"],
        "meal_time": data_dict["meal_time"]
    }
 
    return flask.jsonify(**context)



def clean_and_extract_text(input_text):
    # Remove newline (\n) and carriage return (\r) characters
    cleaned_text = input_text.replace('\n', '').replace('\r', '').replace('\\', '')

    # Find the start and end indices of the content within curly braces ({})
    start_index = cleaned_text.find('{')
    end_index = cleaned_text.rfind('}') + 1

    # Extract the text within curly braces
    extracted_text = cleaned_text[start_index:end_index].strip()

    return extracted_text


