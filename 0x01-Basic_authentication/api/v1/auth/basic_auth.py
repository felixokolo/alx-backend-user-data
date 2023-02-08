#!/usr/bin/env python3
"""Basic authentication class"""
from api.v1.auth.auth import Auth
from flask import request
import base64
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic Authentication class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """Decodes Base64 string to basic string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            dec = base64.b64decode(base64_authorization_header)
            return dec.decode('utf-8')
        except(Exception):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """Extracts user's credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        pos = decoded_base64_authorization_header.find(':')
        return (decoded_base64_authorization_header[:pos],
                decoded_base64_authorization_header[pos+1:])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns user object based on username and password"""
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        User.load_from_file()
        users = User.search({'email': user_email})
        if len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """GETS CURRENT USER"""
        auth = self.authorization_header(request)
        auth = self.extract_base64_authorization_header(auth)
        auth = self.decode_base64_authorization_header(auth)
        auth = self.extract_user_credentials(auth)
        user = self.user_object_from_credentials(*auth)
        return user
