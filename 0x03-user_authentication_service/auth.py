#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

    def valid_login(self, email: str, password: str) -> bool:
        """Checks for credential validity"""
        if email is None or password is None:
            return False
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        ret = bcrypt.checkpw(password.encode(), user.hashed_password)
        if ret:
            return True
        return False

    def _generate_uuid(self) -> str:
        """Generates UUID"""
        return str(uuid4())

    def create_session(self, email: str) -> Union[str, None]:
        """Associates a session ID to a user"""
        if email is None:
            return
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get user from session_id"""
        if session_id is None:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return
        return user

    def destroy_session(self, used_id: int):
        """Destroys a session"""
        if used_id is None:
            return
        try:
            user = self._db.find_user_by(id=used_id)
        except NoResultFound:
            return
        user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        if email is None:
            return
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = self._generate_uuid()
        user.reset_token = token
        return token

    def update_password(self, reset_token: str, password: str):
        """Resets a password"""
        if reset_token is None or password is None:
            return
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        user.hashed_password = _hash_password(password)
        user.reset_token = None
