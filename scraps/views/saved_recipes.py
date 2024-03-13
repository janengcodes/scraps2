import flask
from flask import redirect, render_template, Flask
import scraps
app = Flask(__name__)


@scraps.app.route('/saved_recipes/')
def saved_recipes():
    # breakfast = [
    #     {
    #         "name": "hashbrowns",
    #         "description": "potato"
    #     },
    #     {
    #         "name": "huevos rancheros",
    #         "description": "eggs and stuff"
    #     },
    #     {
    #         "name": "huevos rancheros",
    #         "description": "eggs and stuff"
    #     }
    # ]
        
    breakfast = [
        {
            "name": "burgers and fries",
            "description": "potato and meat"
        },
        {
            "name": "sandwich",
            "description": "peanut butter and jelly"
        },
        {
            "name": "poke",
            "description": "spicy tuna, mayo, edamame"
        }
    ]

    lunch = [
        {
            "name": "burgers and fries",
            "description": "potato and meat"
        },
        {
            "name": "sandwich",
            "description": "peanut butter and jelly"
        },
        {
            "name": "poke",
            "description": "spicy tuna, mayo, edamame"
        }
    ]

    dinner = [
        {
            "name": "lasagna",
            "description": "sskljafd"
        },
        {
            "name": "seasoned",
            "description": "yummy stuff"
        },
        {
            "name": "meat",
            "description": "stuff"
        }
    ]
    
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_accounts_login'))
    
    logname = flask.session.get('username')
    
    context = {
        "lunch": lunch,
        "breakfast:": breakfast,
        "dinner": dinner,
        "logname": logname
    }
    return render_template('saved_recipes.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
