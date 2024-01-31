from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/proteins/')
def proteins():
    context = {
        'example_variable': 'Hello, World!'
    }
    return render_template('proteins.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
