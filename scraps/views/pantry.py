from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/pantry')
def pantry():
    context = {
        'example_variable': 'Hello, World!'
    }
    return render_template('pantry.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
