#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str):
    """Encrypts a password"""
    salt = b'$2b$12$18CJg2MFbrookabjkMl/DO'
    if password is None:
        return
    return bcrypt.hashpw(password.encode(), salt)


class Auth():
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialization function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""

        if email is None or password is None:
            return
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email=email,
                                     hashed_password=_hash_password(password))
            user
            return user
        raise ValueError("{} already exists".format(email))
