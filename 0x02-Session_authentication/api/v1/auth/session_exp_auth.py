#!/usr/bin/env python3
"""Session expiry"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration class"""

    def __init__(self) -> None:
        self.session_duration = 0
        duration = os.getenv('SESSION_DURATION')
        if duration is not None and duration.isnumeric():
            self.session_duration = int(duration)

    def create_session(self, user_id=None):
        """Creates a session"""
        sessionID = super().create_session(user_id)
        if sessionID is None:
            return None
        if user_id is None:
            return None
        self.user_id_by_session_id[sessionID] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """User id from session id"""
        if session_id is None:
            return None
        user = self.user_id_by_session_id.get(session_id)
        if user is None:
            return None
        if self.session_duration == 0:
            return user.get('user_id')
        if user.get('created_at') is None:
            return None
        created_at = user.get('created_at')
        deltatime = timedelta(seconds=self.session_duration)
        expires_at = created_at + deltatime
        current_time = datetime.now()
        if current_time > expires_at:
            return None
        return user.get('user_id')
