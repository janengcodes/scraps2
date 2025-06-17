"""REST API for Pantry."""
from collections import defaultdict
import hashlib
from flask import request, jsonify
import flask
import scraps
from scraps.api.cuisine import train_model
from scraps.api.exceptions import AuthException
from scraps.api.exceptions import check_auth
import requests
import numpy as np
# from rapidfuzz import fuzz, process



model = train_model()

# def check_meal_cookable():

@scraps.app.route("/api/cookable-meals/<username>", methods=["GET"])
def cookable_meals(username):
    connection = scraps.model.get_db()

    # Get pantry_id for the given user
    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()
    print(f"Pantry record fetched: {pantry}")
    
    if pantry is None:
        return flask.jsonify({'error': 'No pantry found'}), 404

    pantry_id = pantry['pantry_id']

    # Get pantry ingredients
    pantry_ingredients = get_ingredients_from_pantry(pantry_id)

    # Get meal_calendar_id for the given user
    meal_calendar = connection.execute('''
        SELECT meal_calendar_id
        FROM meal_calendar_users
        WHERE username = ?
    ''', (username,)).fetchone()

    if meal_calendar is None:
        return flask.jsonify({'error': 'No meal calendar found'}), 404

    meal_calendar_id = meal_calendar["meal_calendar_id"]

    # Get all recipes from the meal calendar
    meals = connection.execute('''
        SELECT mci.meal_day, r.recipe_id, r.recipe_name AS recipe_name
        FROM meal_calendar_item mci
        JOIN recipes r ON mci.recipe_id = r.recipe_id
        WHERE mci.meal_calendar_id = ?
    ''', (meal_calendar_id,)).fetchall()

    cookable_map = {}

    for meal in meals:
        # Get ingredients for each recipe
        ingredient_rows = connection.execute('''
            SELECT i.ingredient_name
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.ingredient_id
            WHERE ri.recipe_id = ?
        ''', (meal["recipe_id"],)).fetchall()

        recipe_ingredient_names = [row["ingredient_name"] for row in ingredient_rows]
        
        # Use fuzzy matching to determine if all ingredients are in pantry
        missing = fuzzy_match_pantry(pantry_ingredients, recipe_ingredient_names)
        cookable_map[meal["recipe_name"]] = len(missing) == 0    
        # cookable_map[meal["recipe_name"]] = False

    print(f"Cookable map: {cookable_map}")
    return flask.jsonify(cookable_map), 200



# def fuzzy_match_pantry(pantry_items, meal_cal_items, threshold=80):
#     # Create a dictionary mapping pantry items to their split up words 
#     # Keep track of the highest scoring match for each pantry item
#     # If the score is below the threshold, add it to the non-matches
#     meal_cal_map = defaultdict(list)
#     scores_map = defaultdict(int)
#     pantry_items = [item.lower() for item in pantry_items]
#     meal_cal_items = [item.lower() for item in meal_cal_items]
#     print(f"Pantry items: {pantry_items}")
#     print(f"Meal calendar items: {meal_cal_items}")
#     non_matches = []
#     for meal_cal_item in meal_cal_items:
#         words = meal_cal_item.lower().replace(',', '').split()
#         meal_cal_map[meal_cal_item] = words
#     # initialize the scores_map
#     for meal_cal_item in meal_cal_items:
#         scores_map[meal_cal_item] = 0

#     for k, v in meal_cal_map.items():
#         for meal_cal_word in v:
#             for pantry_word in pantry_items:
#                 best_match, score, _ = process.extractOne(
#                     meal_cal_word, pantry_word, scorer=fuzz.token_set_ratio
#                 )
#             if score > scores_map[k]:
#                 scores_map[k] = score
#     for k, v in scores_map.items():
#         if v < threshold:
#             # threshold 

#             print("threshold not met", k)
#             pantry_item_found = False

#             # for p in pantry_items:
#             #     p_words = p.lower().replace(',', '').split()
#             #     for p_word in p_words:
#             #         if p_word in k:
#             #             pantry_item_found = True
            
#             if not pantry_item_found:
#                 non_matches.append(k)
            
#     print(f"Scores map: {scores_map}")
#     print(f"Non-matches: {non_matches}")
#     return non_matches


# def get_diff_ingredients(pantry_ingredients, meal_calendar_ingredients):
    
def get_ingredients_from_pantry(pantry_id):
    pantry_ingredients_list = []
    connection = scraps.model.get_db()
    # Get the list of pantry ids
    pantry_ingredients = connection.execute('''
        SELECT ingredient_id FROM pantry_ingredients WHERE pantry_id = ?
    ''', (pantry_id,)).fetchall()

    pantry_ingredients_list = []
    # Get the ingredient names 
    for pantry_ingredient in pantry_ingredients:
        ingredient_id = pantry_ingredient['ingredient_id']
        ingredient = connection.execute('''
            SELECT ingredient_name
            FROM ingredients
            WHERE ingredient_id = ?
        ''', (ingredient_id,)).fetchone()

        if ingredient: 
            pantry_ingredients_list.append(ingredient['ingredient_name'].lower())
    return pantry_ingredients_list

def get_ingredients_from_meal_calendar(meal_calendar_ingredient_ids):
    connection = scraps.model.get_db()
    # Get meal calendar ingredient names 
    meal_calendar_ingredients_names = connection.execute('''
        SELECT ingredient_name
        FROM ingredients WHERE ingredient_id IN ({})
    '''.format(','.join('?' * len(meal_calendar_ingredient_ids))), meal_calendar_ingredient_ids).fetchall()
    meal_calendar_ingredient_actual_names = [ingredient['ingredient_name'].lower() for ingredient in meal_calendar_ingredients_names]
    return meal_calendar_ingredient_actual_names

def get_shopping_list(pantry_id, meal_calendar_ingredient_ids):
    # Get meal calendar ingredients 
    meal_calendar_ingredients = get_ingredients_from_meal_calendar(meal_calendar_ingredient_ids)

    # Get pantry ingredients
    pantry_ingredients = get_ingredients_from_pantry(pantry_id)
    
    missing_ingredients = set(meal_calendar_ingredients) - set(pantry_ingredients)

    print(f"Missing ingredients: {missing_ingredients}")
    
    return missing_ingredients

    


@scraps.app.route('/api/currentPantry/<username>', methods=['GET'])
def current_pantry(username):
    print("Current pantry function called for user:", username)
    """Check if a user is logged in"""
    print(f"Request received for user: {username}")
    logname = check_auth()
    # # Get all pantry ingredients and render into a JSON file 
    connection = scraps.model.get_db()

    # Get pantry ID
    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()
    
    if pantry is None:
        print("No pantry found for user.")
        return flask.jsonify({'error': 'No pantry found'}), 404

    pantry_id = pantry['pantry_id']

    # Get the current meal calendar id
    meal_calendar_id = connection.execute('''
        SELECT meal_calendar_id
        FROM meal_calendar_users
        WHERE username = ?
    ''', (username,)).fetchone()


    if meal_calendar_id is None:
        print("No meal calendar found for user.")
        return flask.jsonify({'error': 'No meal calendar found'}), 404

    meal_calendar_id = meal_calendar_id['meal_calendar_id']
    print(f"Meal calendar ID: {meal_calendar_id}")

    # Get the recipes that are in the meal calendar
    meal_calendar_recipes = connection.execute('''
        SELECT recipe_id, meal_name
        FROM meal_calendar_item WHERE meal_calendar_id = ?
    ''', (meal_calendar_id,)).fetchall()

    meal_calendar_recipe_ids = [
        recipe['recipe_id'] for recipe in meal_calendar_recipes
    ]
    meal_calendar_recipe_ids = list(set(meal_calendar_recipe_ids))
    
    if not meal_calendar_recipe_ids:
        print("No recipes found in meal calendar.")
        return flask.jsonify({'ingredient_ids': []}), 200

    # get all the ingredients in the recipes that are in the meal calendar  
    meal_calendar_ingredients = connection.execute('''
        SELECT ingredient_id
        FROM recipe_ingredients WHERE recipe_id IN ({})
    '''.format(','.join('?' * len(meal_calendar_recipe_ids))), meal_calendar_recipe_ids).fetchall()
    # save all the ingredient ids
    meal_calendar_ingredient_ids = [ingredient['ingredient_id'] for ingredient in meal_calendar_ingredients]
    # get the ingredient names
    ingredient_names = get_shopping_list(pantry_id, meal_calendar_ingredient_ids)
    print(f"Ingredient names in shopping list: {ingredient_names}")
    return flask.jsonify({'ingredient_names': ingredient_names}), 200

    
    


  

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
    
@scraps.app.route('/api/add-to-pantry-check-box/<username>', methods=['POST'])
def add_to_pantry_check_box(username):
    logname = check_auth()
    data = request.get_json()
    ingredient_name = data.get('ingredient_name')
    if not ingredient_name:
        return jsonify({"error": "Ingredient name is None"}), 400
    connection = scraps.model.get_db()
        # Get pantry ID
    pantry = connection.execute('''
        SELECT pantry_id
        FROM pantry
        WHERE username = ?
    ''', (username,)).fetchone()

    
    if pantry is None:
        print("No pantry found for user.")
        return flask.jsonify({'error': 'No pantry found'}), 404

    pantry_id = pantry['pantry_id']
    ingredient = connection.execute('''
        SELECT ingredient_id FROM ingredients WHERE LOWER(ingredient_name) = LOWER(?)
    ''', (ingredient_name,)).fetchone()
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    ingredient_id = ingredient['ingredient_id']

    # Check if already in pantry
    exists = connection.execute('''
        SELECT 1 FROM pantry_ingredients WHERE pantry_id = ? AND ingredient_id = ?
    ''', (pantry_id, ingredient_id)).fetchone()

    if exists:
        return jsonify({'message': 'Ingredient already in pantry'}), 200

    # Add to pantry
    connection.execute('''
        INSERT INTO pantry_ingredients (pantry_id, ingredient_id) VALUES (?, ?)
    ''', (pantry_id, ingredient_id))
    connection.commit()

    return jsonify({'message': 'Ingredient added to pantry'}), 200

