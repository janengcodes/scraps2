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
    print("PANTRY ID 2", pantry_id)

    seasonal_ingredients = connection.execute('''
        SELECT ingredient_name, season, food_group
        FROM ingredients
        WHERE season = 'winter'
    ''',).fetchall()

    # Converst ingredients into a list of dictionaries in order to jsonify the data
    ingredients_list = [
        {
            'ingredient_name': ingredient['ingredient_name'],
            'season': ingredient['season'],
            'food_group': ingredient['food_group']
        }
        for ingredient in seasonal_ingredients
    ]

    pantry_ingredients_list = []

    pantry_ingredients = connection.execute('''
        SELECT ingredient_id FROM pantry_ingredients WHERE pantry_id = ?
    ''', (pantry_id,)).fetchall()

    print("PANTRY INGREDIENTS CHECK 2", pantry_ingredients)
    # PANTRY INGREDIENTS CHECK 2 [{'ingredient_id': 2}, {'ingredient_id': 6}, {'ingredient_id': 9}, {'ingredient_id': 12}]

    pantry_ingredients_list = []

    # Get the ingredients associated with the ingredient ids
    for pantry_ingredient in pantry_ingredients:
        ingredient_id = pantry_ingredient['ingredient_id']
        ingredient = connection.execute('''
            SELECT ingredient_name, food_group
            FROM ingredients
            WHERE ingredient_id = ?
        ''', (ingredient_id,)).fetchone()

        # Append ingredient details as a dictionary
        if ingredient:  # Ensure ingredient is not None
            pantry_ingredients_list.append({
                'ingredient_name': ingredient['ingredient_name'],
                'food_group': ingredient['food_group']
            })
    print("PANTRY INGREDIENTS", pantry_ingredients_list)

    return flask.jsonify({'pantry_id': pantry_id, 'ingredients': ingredients_list, 'pantry_ingredients':pantry_ingredients_list}), 200
