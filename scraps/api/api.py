"""This module provides the API functionality for the scraps project.

This module contains classes and functions for interacting
with the API of the scraps
application. It handles various API endpoints and provides
exceptions for error handling.

"""

import flask
import scraps


@scraps.app.route('/api/v1/')
def get_services():
    """Return list of services."""
    context = {
        "saved_recipes": "/api/v1/saved_recipes/",
        "url": "/api/v1",
        "pantry": "api/v1/pantry"
    }
    return flask.jsonify(**context)