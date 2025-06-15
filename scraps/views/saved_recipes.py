import flask
from flask import redirect, render_template, Flask
import scraps
app = Flask(__name__)
import json


@scraps.app.route('/saved_recipes/')
def saved_recipes():
    
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    logname = flask.session.get('username')

    connection = scraps.model.get_db()

    saved_recipes = connection.execute('''
        select r.recipe_name, i.ingredient_name, r.instructions
        from recipes r
        join recipe_ingredients ri on r.recipe_id = ri.recipe_id
        join ingredients i on i.ingredient_id = ri.ingredient_id
        where r.username = ?
    ''', (logname,)).fetchall()

    unique_results = []
    seen_names = set()
    recipe_counter = 0
    for entry in saved_recipes:
        instructions = entry['instructions']
        if isinstance(instructions, str):
            try:
                instructions = json.loads(instructions)
            except json.JSONDecodeError:
                instructions = [instructions]  # fallback if not valid JSON

        
        if entry['recipe_name'] not in seen_names:
            recipe_counter +=1
  
            unique_results.append({
                'recipe_name': entry['name'],
                'ingredients': [entry['ingredient_name']],
                'instructions': instructions 
            })
            seen_names.add(entry['recipe_name'])
        else:
            unique_results[recipe_counter - 1]['ingredients'].append(entry['ingredient_name'])

    print("unique results", unique_results)
    
    context = {
        "recipes": unique_results
    }
    return render_template('saved_recipes.html', **context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
