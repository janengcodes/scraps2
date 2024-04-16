from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/select_ingredients/')
def show_select_ingredients():
    context = {}
    return render_template('select_ingredients.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
