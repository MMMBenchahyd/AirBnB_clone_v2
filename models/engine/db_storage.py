#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


class DBStorage:
    """Represents a database storage engine."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        Ur=getenv("HBNB_MYSQL_USER")
        PWD=getenv("HBNB_MYSQL_PWD")
        H=getenv("HBNB_MYSQL_HOST")
        DB=getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(f"mysql+mysqldb://{Ur}:{PWD}@{H}/{DB}",
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class."""
        if cls is None:
            ob = self.__session.query(State).all()
            ob.extend(self.__session.query(City).all())
            ob.extend(self.__session.query(User).all())
            ob.extend(self.__session.query(Place).all())
            ob.extend(self.__session.query(Review).all())
            ob.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            ob = self.__session.query(cls)
        return {"{}.{}".format(type(oob).__name__, oob.id): oob for oob in ob}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove()"""
        self.__session.close()
