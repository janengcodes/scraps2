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


@scraps.app.route('/api/add-to-meal-cal/<username>', methods=['POST'])
def add_to_meal_cal(username):
    """Add a recipe to the meal calendar."""
    # Ensure that the user is logged in 
    check_auth()
    logname = flask.session.get('username')

    # connection to the database
    connection = scraps.model.get_db()
    data = request.get_json()
    meal_day = data.get('day')
    meal_type = data.get('mealType')
    meal_name = data.get('mealName')
    recipe_name = data.get('selectedRecipe')  # assuming this is the recipe name


    # find the meal calendar id
    meal_cal = connection.execute('''
        SELECT meal_calendar_id
        FROM meal_calendar_users
        WHERE username = ?
    ''', (username,)).fetchone()

    if meal_cal is None:
        return flask.jsonify({"error": "Meal calendar not found"}), 404
    
    meal_cal_id = meal_cal['meal_calendar_id']
    # find the recipe id
    recipe = connection.execute(
        '''
        SELECT recipe_id
        FROM recipes
        WHERE name = ?
        ''', (recipe_name,)
    ).fetchone()
    if recipe is None:
        return flask.jsonify({"error": "Recipe not found"}), 404
    # insert into meal_calendar_item
    connection.execute('''
        INSERT INTO meal_calendar_items (meal_calendar_id, recipe_id, meal_day, meal_type)
        VALUES (?, ?, ?, ?)
    ''', (meal_cal_id, recipe['recipe_id'], meal_day, meal_type))

    connection.commit()
    return flask.jsonify({"success": True}), 200


