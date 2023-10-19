#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.base_model import Base


classes = {"City": City, "State": State, "User": User, "Place": Place,
           "Review": Review, "Amenity": Amenity}


class DBStorage:
    """This class manages storage of hbnb models in JSON a relational DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        dialect = "mysql"
        driver = "mysqldb"
        port = 3306
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db_name = os.getenv("HBNB_MYSQL_DB")

        db_uri = "{}+{}://{}:{}@{}:{}/{}".format(
            dialect, driver, user, passwd, host, port, db_name)

        self.__engine = create_engine(db_uri, pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        new_dict = {}
        if cls:
            if type(cls) == str:
                cls = classes[cls]

            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj
        else:
            for clas in classes.values():
                objs = self.__session.query(clas).all()

                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Adds new object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session """
        self.__session.commit()

    def reload(self):
        """
        create all tables in the database
        create the current database session from the engine
        """
        Base.metadata.create_all(self.__engine)
        sesn_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sesn_factory)
        self.__session = Session()

    def delete(self, obj=None):
        """
        Deletes objects from current database session and does nothing if obj
        is None
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        '''
        Close a session
        '''
        self.__session.close()
