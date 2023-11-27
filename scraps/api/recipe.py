"""REST API for recipes."""
import flask
app = flask.Flask(__name__)


@app.route('/api/v1/recipes/<int:recipeid_url_slug>/')
def get_recipe(recipeid_url_slug):
    """Return recipe on recipeid.
    """
    # connection = scraps2.model.get_db();
    # context = {
    #     "created": "2017-09-28 04:33:28",
    #     "owner": "awdeorio",
    #     "ownerShowUrl": "/users/awdeorio/",
    #     "postShowUrl": f"/posts/{recipeid_url_slug}/",
    #     "postid": recipeid_url_slug,
    #     "url": flask.request.path,
    # }
    context = {}
    return flask.jsonify(**context)
