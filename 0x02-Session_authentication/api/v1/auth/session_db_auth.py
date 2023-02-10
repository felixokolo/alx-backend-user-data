#!/usr/bin/env python3
"""Session DB authentication"""
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """Session DB Authentication class"""

    def create_session(self, user_id=None):
        """Create session overload"""

        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        sessionID = super().create_session(user_id)
        new_user = UserSession(user_id=user_id,
                               session_id=sessionID)
        new_user.save()
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """Gets user id for a session id"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        UserSession.load_from_file()
        users = UserSession.search({'session_id': session_id})
        if len(users) == 0:
            return None
        return users[0]

    def destroy_session(self, request=None):
        """Destroys session"""
        if request is None:
            return None
        cookieValue = self.session_cookie(request)
        if cookieValue is None:
            return None
        user_id = self.user_id_for_session_id(cookieValue)
        if user_id is None:
            return None
        user_id.remove()
