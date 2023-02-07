#!/usr/bin/env python3
"""Basic authentication class"""
from api.v1.auth.auth import Auth
from flask import request
import base64
from typing import Tuple


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
        except(Exception):
            return None
        return dec.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """Extracts user's credentials"""
        if decoded_base64_authorization_header is None:
            return None
        if type(decoded_base64_authorization_header) is not str:
            return None
        if ':' not in decoded_base64_authorization_header:
            return None
        return tuple(decoded_base64_authorization_header.split(':'))
