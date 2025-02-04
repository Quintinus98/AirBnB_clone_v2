#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
from sqlalchemy import MetaData, Column, String, DateTime
from models import storage_type
# from os import getenv


mymetadata = MetaData()

if storage_type == "db":
    Base = declarative_base(metadata=mymetadata)
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            self.create(**kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def create(self, **kwargs):
        """Creates a BaseModel from a dictionary"""
        for k, v in kwargs.items():
            if k != '__class__':
                setattr(self, k, v)
        if kwargs.get("updated_at", None) and type(self.updated_at) is str:
            self.updated_at = datetime.fromisoformat(kwargs["updated_at"])
        else:
            self.updated_at = datetime.utcnow()
        if kwargs.get("created_at", None) and type(self.created_at) is str:
            self.created_at = datetime.fromisoformat(kwargs["created_at"])
        else:
            self.created_at = datetime.utcnow()
        if kwargs.get("id", None) is None:
            self.id = str(uuid.uuid4())

    def delete(self):
        """ Deletes the current instance from storage """
        from models import storage
        storage.delete(self)
