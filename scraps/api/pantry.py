"""REST API for Pantry."""
import hashlib
from flask import request, jsonify
import flask
import scraps
from scraps.api.cuisine import train_model
from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth
import requests
import numpy as np



model = train_model()

@scraps.app.route('/api/currentPantry/<username>', methods=['GET'])
def current_pantry(username):
    """Check if a user is logged in"""

    logname = check_auth()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))

    # Get all pantry ingredients and render into a JSON file 
    connection = scraps.model.get_db()

    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()
    pantry_id = pantry['pantry_id']

    # Get all the ingredients in the pantry
    pantry_ingredients = connection.execute('''
        SELECT ingredient_id, ingredient_name
        FROM ingredients WHERE pantry_id = ?
    ''', (pantry_id,)).fetchall()
    # Convert into a list 
    pantry_ingredients_list = []    
    for pantry_ingredient in pantry_ingredients:
        pantry_ingredients_list.append({
            'ingredient_id': pantry_ingredient['ingredient_id'],
            'ingredient_name': pantry_ingredient['ingredient_name']
        })

    
    


  

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

    for pantry_ingredient in pantry_ingredients:
        ingredient_id = pantry_ingredient['ingredient_id']
        ingredient = connection.execute('''
            SELECT ingredient_name, food_group
            FROM ingredients
            WHERE ingredient_id = ?
        ''', (ingredient_id,)).fetchone()

        if ingredient:  # Ensure ingredient is not None
            pantry_ingredients_list.append({
                'ingredient_name': ingredient['ingredient_name'],
                'food_group': ingredient['food_group']
            })

    top_cuisines = []

    try:

        new_ingredients = " ".join([ingredient['ingredient_name'] for ingredient in pantry_ingredients_list])
        
        probabilities = model.predict_proba([new_ingredients])
        class_labels = model.classes_

        top_n = 3
        prob_array = np.argsort(probabilities[0])[::-1]
        top_indices = prob_array[:top_n]

        top_cuisines = []
        for i in top_indices:
            top_cuisines.append({
                'cuisine': class_labels[i],
                'probability': round(probabilities[0][i], 2)
            })
    except Exception as e:
        print(f"Error getting top cuisines: {e}")
    

    recs = [{
        'cuisine': cuisine['cuisine'],
        'probability': cuisine['probability']
    } for cuisine in top_cuisines]

    # If pantry ingredients list is empty, make recs empty
    if not pantry_ingredients_list or not pantry_ingredients_list[0]['ingredient_name']:
        recs = []
    print(pantry_ingredients_list)
    return flask.jsonify({'pantry_id': pantry_id, 'ingredients': ingredients_list, 'pantry_ingredients':pantry_ingredients_list, 'recs':recs}), 200


@scraps.app.route('/api/add-to-pantry/<username>', methods=['POST'])
def add_to_pantry(username):
    logname = check_auth()

    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    try:

        data = request.get_json()
        ingredients = data.get('ingredients', []) 

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

                cursor = connection.execute('''
                    INSERT INTO pantry_ingredients (pantry_id, ingredient_id)
                    VALUES (?, ?)
                ''', (pantry_id, ingredient_id))

        
                if cursor.rowcount > 0:
                    print(f"Added ingredient {ingredient_id} to pantry.")
                else:
                    print(f"Failed to add ingredient {ingredient_id} to pantry.")

                ingredient = connection.execute('''
                    SELECT ingredient_name, food_group
                    FROM ingredients
                    WHERE ingredient_id = ?
                ''', (ingredient_id,)).fetchone()

       
                if ingredient:  
                    pantry_ingredients_list.append({
                        'ingredient_name': ingredient['ingredient_name'],
                        'food_group': ingredient['food_group']
                    })
                

            except Exception as e:
                print(f"Error inserting ingredient {ingredient}: {e}")

        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        print(f"User {username} is adding the following ingredients: {ingredients}")

        try:
            new_ingredients = " ".join([ingredient['ingredient_name'] for ingredient in pantry_ingredients_list])
            
            probabilities = model.predict_proba([new_ingredients])
            class_labels = model.classes_

            top_n = 3
            prob_array = np.argsort(probabilities[0])[::-1]
            top_indices = prob_array[:top_n]

            top_cuisines = []
            for i in top_indices:
                top_cuisines.append({
                    'cuisine': class_labels[i],
                    'probability': round(probabilities[0][i], 2)
                })
        except Exception as e:
            print(f"Error getting top cuisines: {e}")
        

        recs = [{
            'cuisine': cuisine['cuisine'],
            'probability': cuisine['probability']
        } for cuisine in top_cuisines]

        return jsonify({
            "message": "Ingredients added successfully",
            'pantry_ingredients': pantry_ingredients_list,
            "recs": recs
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500