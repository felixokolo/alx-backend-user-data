#!/usr/bin/env python3
""" Module of Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth() -> str:
    """ POST /auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    User.load_from_file()
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = None
    for usern in users:
        if usern.is_valid_password(password):
            user = usern
    if user is None:
        return jsonify({"error": "wrong password"}), 404
    from api.v1.app import auth
    sessionID = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie(os.getenv('SESSION_NAME'), sessionID)
    return out


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def remove_session() -> str:
    """ Remeoves session """
    from api.v1.app import auth
    ret = auth.destroy_session(request)
    if not ret:
        abort(404)
    return jsonify({}), 200
