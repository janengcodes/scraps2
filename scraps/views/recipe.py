from flask import Flask, render_template
import scraps
app = Flask(__name__)

'''

CREATE TABLE recipes(
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    filename VARCHAR(64) NOT NULL,
    ingredient_ids_json TEXT NOT NULL, /* JSON data */
    instructions TEXT NOT NULL,
    cook_time INT NOT NULL /* in minutes */
);

'''


@scraps.app.route('/recipe/')
def recipe():
    context = {
        'example_variable': 'Hello, World!'
    }
    return render_template('recipe.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
