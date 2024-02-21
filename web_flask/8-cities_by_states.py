#!/usr/bin/python3
"""Flask web application - List of states"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_storage(exception):
    """Remove the current SQLAlchemy session"""
    if storage is not None:
        storage.close()


@app.route("/cities_by_states")
def list_cities_by_states():
    """List all cities by states"""
    states = storage.all(cls=State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
