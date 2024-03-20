import flask
from flask import redirect, render_template, Flask, request
import scraps
app = Flask(__name__)


@scraps.app.route('/grains_checkbox/', methods=['POST'])
def grain():
    selected_grains = request.form.getlist('grain_ingredient')

@scraps.app.route('/produce_checkbox/', methodus=['POST'])
def produce():
    selected_produce = request.form.getlist('produce_ingredient')

@scraps.app.route('/dairy_checkbox/', methods=['POST'])
def dairy():
    selected_dairy = request.form.getlist('dairy_ingredient')

@scraps.app.route('/protein_checkbox/', methods=['POST'])
def protein():
    selected_protein = request.form.getlist('protein_ingredient')