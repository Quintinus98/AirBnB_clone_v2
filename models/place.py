#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from models import storage_type
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


# place_amenity = Table('place_amenity', Base.metadata,
#                       Column('place_id', String(60), ForeignKey('places.id'),
#                              primary_key=True, nullable=False),
#                       Column('amenity_id', String(60),
#                              ForeignKey('amenities.id'),
#                              primary_key=True, nullable=False)
#                       )


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_type == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        # amenities = relationship("Amenity", secondary="place_amenity",
        #                          backref="place_amenities", viewonly=False)
        reviews = relationship("Review", backref="place")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """ Initializes the basemodel class """
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def reviews(self):
            """ Returns the list of reviews in the filestorage """
            from models import storage
            all_review = storage.all(Review)
            all_review_match = []
            for review in all_review:
                if review.place_id == self.id:
                    all_review_match.append(review)
            return all_review_match

        @property
        def amenities(self):
            """ Returns the list of amenities in the filestorage """
            from models import storage
            all_amen = storage.all(Amenity)
            all_amen_match = []
            for amenity in all_amen:
                if amenity.place_id == self.id:
                    all_amen_match.append(amenity)
            return all_amen_match
