"""REST API for Pantry."""
import hashlib
from flask import jsonify
import flask
import scraps

from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth

import requests

@scraps.app.route('/api/pantry/<username>', methods=['GET'])
def get_pantry(username):
    """Check if a user is logged in"""
    logname = check_auth()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    # Get all pantry ingredients and render into a JSON file 
    # 1. Get the pantry id
    connection = scraps.model.get_db()

    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()

    # 2. Get ingredients associated with the pantry id 

    pantry_id = pantry['pantry_id']
    print("PANTRY ID IS", pantry['pantry_id'])

    ingredients = connection.execute('''
        SELECT ingredient_name, season, food_group
        FROM ingredients
        WHERE season = 'winter'
    ''',).fetchall()

    print("INGREDIENTS ARE", ingredients)

    # Converst ingredients into a list of dictionaries in order to jsonify the data
    ingredients_list = [
        {
            'ingredient_name': ingredient['ingredient_name'],
            'season': ingredient['season'],
            'food_group': ingredient['food_group']
        }
        for ingredient in ingredients
    ]

    return flask.jsonify({'pantry_id': pantry_id, 'ingredients': ingredients_list}), 200
