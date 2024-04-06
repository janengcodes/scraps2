# from flask import Flask, render_template, send_from_directory
# import scraps
# import tensorflow as tf
# import numpy as np
# import json
# app = Flask(__name__)
# # flask --app scraps --debug run --host 0.0.0.0 --port 8000

# file_path = '/Users/celin/Desktop/clubs/scraps/scraps2/scraps/ML/models/model.json'
# model_content = '{"format": "layers-model", "generatedBy": "keras v2.15.0", "convertedBy": "TensorFlow.js Converter v4.17.0", "modelTopology": {"keras_version": "2.15.0", "backend": "tensorflow", "model_config": {"class_name": "Sequential", "config": {"name": "sequential_1", "layers": [{"class_name": "InputLayer", "config": {"batch_input_shape": [64, None], "dtype": "float32", "sparse": False, "ragged": False, "name": "embedding_1_input"}}, {"class_name": "Embedding", "config": {"name": "embedding_1", "trainable": True, "dtype": "float32", "batch_input_shape": [64, None], "input_dim": 98, "output_dim": 256, "embeddings_initializer": {"module": "keras.initializers", "class_name": "RandomUniform", "config": {"minval": -0.05, "maxval": 0.05, "seed": None}, "registered_name": None}, "embeddings_regularizer": None, "activity_regularizer": None, "embeddings_constraint": None, "mask_zero": False, "input_length": None}}, {"class_name": "LSTM", "config": {"name": "lstm", "trainable": True, "dtype": "float32", "return_sequences": True, "return_state": False, "go_backwards": False, "stateful": True, "unroll": False, "time_major": False, "units": 1024, "activation": "tanh", "recurrent_activation": "sigmoid", "use_bias": True, "kernel_initializer": {"module": "keras.initializers", "class_name": "GlorotUniform", "config": {"seed": None}, "registered_name": None}, "recurrent_initializer": {"module": "keras.initializers", "class_name": "GlorotNormal", "config": {"seed": None}, "registered_name": None}, "bias_initializer": {"module": "keras.initializers", "class_name": "Zeros", "config": {}, "registered_name": None}, "unit_forget_bias": True, "kernel_regularizer": None, "recurrent_regularizer": None, "bias_regularizer": None, "activity_regularizer": None, "kernel_constraint": None, "recurrent_constraint": None, "bias_constraint": None, "dropout": 0.0, "recurrent_dropout": 0.0, "implementation": 2}}, {"class_name": "Dense", "config": {"name": "dense", "trainable": True, "dtype": "float32", "units": 98, "activation": "linear", "use_bias": True, "kernel_initializer": {"module": "keras.initializers", "class_name": "GlorotUniform", "config": {"seed": None}, "registered_name": None}, "bias_initializer": {"module": "keras.initializers", "class_name": "Zeros", "config": {}, "registered_name": None}, "kernel_regularizer": None, "bias_regularizer": None, "activity_regularizer": None, "kernel_constraint": None, "bias_constraint": None}}]}}, "training_config": {"loss": "loss", "metrics": None, "weighted_metrics": None, "loss_weights": None, "optimizer_config": {"class_name": "Custom>Adam", "config": {"name": "Adam", "weight_decay": None, "clipnorm": None, "global_clipnorm": None, "clipvalue": None, "use_ema": False, "ema_momentum": 0.99, "ema_overwrite_frequency": None, "jit_compile": False, "is_legacy_optimizer": False, "learning_rate": 0.0010000000474974513, "beta_1": 0.9, "beta_2": 0.999, "epsilon": 1e-07, "amsgrad": False}}}}, "weightsManifest": [{"paths": ["group1-shard1of6.bin", "group1-shard2of6.bin", "group1-shard3of6.bin", "group1-shard4of6.bin", "group1-shard5of6.bin", "group1-shard6of6.bin"], "weights": [{"name": "dense/kernel", "shape": [1024, 98], "dtype": "float32"}, {"name": "dense/bias", "shape": [98], "dtype": "float32"}, {"name": "embedding_1/embeddings", "shape": [98, 256], "dtype": "float32"}, {"name": "lstm/lstm_cell/kernel", "shape": [256, 4096], "dtype": "float32"}, {"name": "lstm/lstm_cell/recurrent_kernel", "shape": [1024, 4096], "dtype": "float32"}, {"name": "lstm/lstm_cell/bias", "shape": [4096], "dtype": "float32"}]}]}'


# @scraps.app.route('/generate.html')
# def generate():

#     ingredient_list = ["milk", "sugar", "apple", "butter"]

# #     model = sendModel(file_path)

# #     prediction = model.predict(np.array([ingredient_list]))


#     context = {
#         'ingredients': ingredient_list,
#     }
#     return render_template('generate.html', **context) 

# def sendModel(file_path):
#     # Load model content from file
#     with open(file_path) as f:
#         model_dict = json.load(f)
#         # model_content_json = f.read()

#     # Convert JSON string to dictionary
#     # model_content = json.load(model_content_json)

#     # Convert dictionary to JSON string
#     # model_content_json = json.dumps(model_content)

#     # Load model from JSON string
#     model = tf.keras.models.model_from_json(model_dict)
#     return model
# # def sendModel(file_path):
# #     # with open(file_path, 'r') as f:
# #     #         filestuff = f.read()

# #     # model_config = json.loads(filestuff)
# #     model_content_json = json.dumps(model_content)
# #     model = tf.keras.models.model_from_json(model_content_json)

# #     return model




# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
