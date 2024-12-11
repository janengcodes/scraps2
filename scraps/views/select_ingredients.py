import flask
from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/select_ingredients/')
def show_select_ingredients():
    context = {}
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    connection = scraps.model.get_db()

    fruit = connection.execute('''
        SELECT ingredient_id, ingredient_name, food_group
        FROM ingredients
        WHERE food_group = 'fruit'
    ''',).fetchall()

    veggies = connection.execute('''
        SELECT ingredient_id, ingredient_name, food_group
        FROM ingredients
        WHERE food_group = 'veggies'
    ''',).fetchall()

    protein = connection.execute('''
        SELECT ingredient_id, ingredient_name, food_group
        FROM ingredients
        WHERE food_group = 'protein'
    ''',).fetchall()

    grains = connection.execute('''
        SELECT ingredient_id, ingredient_name, food_group
        FROM ingredients
        WHERE food_group = 'grains'
    ''',).fetchall()

    dairy = connection.execute('''
        SELECT ingredient_id, ingredient_name, food_group
        FROM ingredients
        WHERE food_group = 'dairy'
    ''',).fetchall()


    # Prepare the context for the response
    context = {
        "fruit": fruit,
        "veggies": veggies,
        "protein": protein,
        "grains": grains,
        "dairy": dairy
    }

    print(context)
    
    return render_template('select_ingredients.html', context=context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
