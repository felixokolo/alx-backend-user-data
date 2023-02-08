#!/usr/bin/env python3
"""
Authentication class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Requires authentication
        """

        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            if p is None:
                continue
            if '*' in p:
                pos = p.find('*')
                if p[:pos] == path[:pos]:
                    return False
            else:
                p = p.rstrip('/')
                if path.rstrip('/') == p:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Defines authorization header
        """
        if request is None:
            return None

        auths = request.headers.get('Authorization')
        if auths is None:
            return None
        return auths

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user
        """
        return None
