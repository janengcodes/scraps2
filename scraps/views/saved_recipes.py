from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/saved_recipes/')
def saved_recipes():
    breakfast = [

        ]
    
    lunch = [

        ]

    dinner = [

        ]


    context = {
        "breakfast:": breakfast,
        "lunch": lunch,
        "dinner": dinner
    }
    return render_template('saved_recipes.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
