#!/usr/bin/python3
"""HBNB Filters"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_storage(exception):
    """Removes the current SQLAlchemy session"""
    storage.close()


@app.route("/hbnb_filters")
def hbnb_filters():
    """Load all cities of a State"""
    states = storage.all(cls=State).values()
    amenities = storage.all(cls=Amenity).values()
    places = storage.all(cls=Place).values()
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities,
                           places=places)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)
    storage.reload()
