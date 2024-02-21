#!/usr/bin/python3
"""Flask web application - List of states"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session"""
    if storage is not None:
        storage.close()


@app.route("/states_list")
def list_states():
    """List all states"""
    from models.state import State
    states = storage.all(cls=State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
