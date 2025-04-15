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

@scraps.app.route('/api/add-to-meal-cal/<username>', methods=['GET'])
def get_meal_cal(username):
    # Ensure that the user is logged in 
    check_auth()
    # connection to the database
    connection = scraps.model.get_db()
    # Get the meal calendar id
    meal_cal = connection.execute('''
        SELECT meal_calendar_id
        FROM meal_calendar_users
        WHERE username = ?
    ''', (username,)).fetchone()
    if meal_cal is None:
        return flask.jsonify({"error": "Meal calendar not found"}), 404
    meal_cal_id = meal_cal['meal_calendar_id']
    # Get all the recipes in the meal calendar
    meal_cal_items = connection.execute('''
        SELECT meal_day, meal_type, meal_name, recipe_name
        FROM meal_calendar_item
        WHERE meal_calendar_id = ?
    ''', (meal_cal_id,)).fetchall()
    # Convert into a list
    meal_cal_items_list = []
    for meal_cal_item in meal_cal_items:
        meal_cal_items_list.append({
            'meal_day': meal_cal_item['meal_day'],
            'meal_type': meal_cal_item['meal_type'],
            'meal_name': meal_cal_item['meal_name'],
            'recipe_name': meal_cal_item['recipe_name']
        })
    # Return the meal calendar items as JSON
    return flask.jsonify(meal_cal_items_list), 200



@scraps.app.route('/api/add-to-meal-cal/<username>', methods=['POST'])
def add_to_meal_cal(username):
    """Add a recipe to the meal calendar."""
    # Ensure that the user is logged in 
    check_auth()

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
        INSERT INTO meal_calendar_item (meal_calendar_id, recipe_id, meal_day, meal_type)
        VALUES (?, ?, ?, ?)
    ''', (meal_cal_id, recipe['recipe_id'], meal_day, meal_type))

    # check the meal calendar item
    meal_cal_item = connection.execute('''
        SELECT *
        FROM meal_calendar_item
        WHERE meal_calendar_id = ? AND recipe_id = ? AND meal_day = ? AND meal_type = ?
    ''', (meal_cal_id, recipe['recipe_id'], meal_day, meal_type)).fetchone()
    if meal_cal_item is None:
        return flask.jsonify({"error": "Failed to add recipe to meal calendar"}), 500
    else:
        print("Added recipe to meal calendar")
        print(meal_cal_item)

    connection.commit()
    return flask.jsonify({"success": True}), 200


