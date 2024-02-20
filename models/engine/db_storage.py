#!/usr/bin/python3
""" DataBase storage class """
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
}

# Environment variables
HBNB_ENV = getenv('HBNB_ENV')
HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
HBNB_TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')


class DBStorage():
    """ Represents a DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes the DBStorage class """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@localhost:3306/{}"
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)

        # Session.configure(bind=self.__engine)
        if HBNB_ENV == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ Query all objects on the current database """
        obj_dict = {}
        if cls is None:
            for model in classes:
                all_obj = self.__session.query(classes[model]).all()
                for obj in all_obj:
                    key = '{}.{}'.format(model, obj.id)
                    obj_dict[key] = obj
        # if it's not None, filter by class.
        else:
            all_obj = self.__session.query(cls).all()
            for obj in all_obj:
                key = '{}.{}'.format(cls, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """ Adds a new obj to the db """
        self.__session.add(obj)

    def save(self):
        """ Save all changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database - reload """
        Base.metadata.create_all(self.__engine)
        our_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(our_session)
        self.__session = Session()

    def close(self):
        """Call remove() method"""
        self.__session.close()
