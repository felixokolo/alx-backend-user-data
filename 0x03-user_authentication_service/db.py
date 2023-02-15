#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves user to database"""
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """finds a user based on input keywords"""
        if kwargs is None:
            raise InvalidRequestError
        cols = User.__dict__.keys()
        ret = None
        for x in kwargs.keys():
            if x not in cols or kwargs[x] is None:
                raise(InvalidRequestError)
        try:
            ret = self._session.query(User).filter_by(**kwargs).first()
        except(InvalidRequestError):
            raise InvalidRequestError
        if ret is None:
            raise(NoResultFound)
        return ret

    def update_user(self, user_id: int, **kwargs):
        """Updates a user attribute"""
        if kwargs is None:
            raise ValueError
        attr = {'id': user_id}
        try:
            user = self.find_user_by(**attr)
        except(InvalidRequestError, NoResultFound):
            raise ValueError
        cols = User.__dict__.keys()
        for x in kwargs.keys():
            if x not in cols or kwargs[x] is None:
                raise(ValueError)
        for k, v in kwargs.items():
            setattr(user, k, v)
