from flask import Flask, render_template
import scraps
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import h5py
import keras

app = Flask(__name__)
# flask --app scraps --debug run --host 0.0.0.0 --port 80

file_path = '/Users/celin/Desktop/scraps2/scraps/ML/recipe_generation_rnn_raw_1.h5'


@scraps.app.route('/generate.html')
def generate():

    ingredient_list = ["milk", "sugar", "apple", "butter"]

    # keras version used in the model: 2.15.0

    
    print("Keras version:", keras.__version__)

    model = load_model(file_path)
    model = tf.saved_model.load('/Users/celin/Desktop/clubs/scraps/scraps2/scraps/views/recipe_generation_rnn_raw_1.h5')

    prediction = model.predict(np.array([ingredient_list]))


    context = {
        'ingredients': ingredient_list
        # 'prediction': prediction
    }
    return render_template('generate.html', **context) 

def access_model():

    # Open the model file
    with h5py.File(file_path, 'r') as f:
        # keras_version = f.attrs.get('keras_version')
        model_config = f.attrs.get('model_config')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

