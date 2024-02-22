#!/usr/bin/python3
"""Hello flask"""
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


@app.route('/states')
def states():
    """Prints the list of all State objects present in storage"""
    states = storage.all(cls=State).values()
    return render_template("9-states.html", states=states)


@app.route('/states/<id>')
def state_with_id(id):
    """Prints If a State object is found with this id"""
    states = storage.all(cls=State).values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", states=[state])
    return render_template("9-states.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    storage.reload()
