from flask import Flask, render_template
import scraps
app = Flask(__name__)


@scraps.app.route('/grains/')
def grains():
    context = {
        'example_variable': 'Hello, World!'
    }
    return render_template('grains.html', **context)
    # take in form data 
    # save as a variable in order to send to the ML algo

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

