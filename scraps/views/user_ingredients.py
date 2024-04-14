import flask
from flask import redirect, render_template, Flask, request
import scraps
app = Flask(__name__)

@scraps.app.route('/ingredient_checkbox/', methods=['POST'])
def ingredient_selection():
    selected_ingredients = request.form.getlist('ingredient')
    print(selected_ingredients)

    # target = flask.request.args.get('target', '/produce')
    return flask.redirect('/recipe')
