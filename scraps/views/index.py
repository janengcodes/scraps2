from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/')
def index():
    context = {
        'example_variable': 'Hello, World!'
    }
    # check if a user is logged in to display the dashboard

    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
