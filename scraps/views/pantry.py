"""Rander pantry page."""
import scraps
import flask

# app = flask.Flask(__name__)


@scraps.app.route('/pantry/', methods=["GET"])
def pantry():

    protein = [
        {"name": "chicken",
         "id": 1},
        {"name": "beef",
         "id": 2},
        {"name": "pork",
         "id": 0},
        {"name": 'crab',
         "id": 3},
        {"name": "lamb",
         "id": 4}
        ]
    grains = [
        {"name": "cereal",
         "id": 5},
        {"name": "legume",
         "id": 6}
        ]

    dairy = [
        {"name": "milk",
         "id": 9},
        ]

    produce = [
        {"name": "apple",
         "id": 11},
        {"name": "onion",
         "id": 12},
        {"name": "garlic",
         "id": 10},
        {"name": 'mushroom',
         "id": 13},
        ]

    context = {
        "protein": protein,
        "grains": grains,
        "dairy": dairy,
        "produce": produce
        }
    return flask.render_template("pantry.html", **context)


@scraps.app.route('/pantry/', methods=["POST"])
def send_ingredients():
    ingredients = flask.forms.get('send_ingredients')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
