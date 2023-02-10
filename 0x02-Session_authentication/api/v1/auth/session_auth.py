#!/usr/bin/env python3
"""Session authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4
import os


class SessionAuth(Auth):
    """ Sessions Authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        sessionID = str(uuid4())
        SessionAuth.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Gets user id for a session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ Returns current user """
        sessionID = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sessionID)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Logout mechanism"""
        if request is None:
            return False
        sessionID = self.session_cookie(request)
        if sessionID is None:
            return False
        user = self.user_id_for_session_id(sessionID)
        if user is None:
            return False
        del self.user_id_by_session_id[sessionID]
        return True
