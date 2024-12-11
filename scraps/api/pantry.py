"""REST API for Pantry."""
import hashlib
from flask import request, jsonify
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
        SELECT ingredient_id, ingredient_name, season, food_group
        FROM ingredients
        WHERE season = 'winter'
    ''',).fetchall()

    # Converst ingredients into a list of dictionaries in order to jsonify the data
    ingredients_list = [
        {
            'ingredient_id': ingredient['ingredient_id'],
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
    return flask.jsonify({'pantry_id': pantry_id, 'ingredients': ingredients_list, 'pantry_ingredients':pantry_ingredients_list}), 200


@scraps.app.route('/api/add-to-pantry/<username>', methods=['POST'])
def add_to_pantry(username):
    logname = check_auth()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    try:

        data = request.get_json()
        ingredients = data.get('ingredients', [])  # Retrieve the 'ingredients' list from the JSON

        print(f"User {username} is adding the following ingredients: {ingredients}")

        connection = scraps.model.get_db()
        # Insert the ingredients into the pantry
        pantry = connection.execute('''
            SELECT pantry_id
            FROM pantry
            WHERE username = ?
        ''', (username,)).fetchone()
        pantry_id = pantry['pantry_id']
        pantry_ingredients_list = []

        for ingredient_id in ingredients:
            try:
                # Execute the insert statement
                cursor = connection.execute('''
                    INSERT INTO pantry_ingredients (pantry_id, ingredient_id)
                    VALUES (?, ?)
                ''', (pantry_id, ingredient_id))

                # Check if any row was inserted
                if cursor.rowcount > 0:
                    print(f"Added ingredient {ingredient_id} to pantry.")
                else:
                    print(f"Failed to add ingredient {ingredient_id} to pantry.")

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

            except Exception as e:
                print(f"Error inserting ingredient {ingredient}: {e}")

        # Check if ingredients are provided
        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        print(f"User {username} is adding the following ingredients: {ingredients}")

        # Respond with a success message
        return jsonify({
            "message": "Ingredients added successfully",
            'pantry_ingredients': pantry_ingredients_list,
            "pantry_id": pantry_id  # Optionally return pantry_id for confirmation
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500