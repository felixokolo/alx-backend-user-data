#!/usr/bin/env python3
"""Simple flask app"""

from flask import Flask, jsonify, request, abort, redirect
from flask import url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """Basic app"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """creates a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return

    try:
        AUTH.register_user(email, password)
    except(ValueError):
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Carries out login process"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(401)
    valid = AUTH.valid_login(email, password)
    if valid:
        session_id = AUTH.create_session(email)
        ret = jsonify({"email": email, "message": "logged in"})
        ret.set_cookie('session_id', session_id)
        return ret
    abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Implements the logout process"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route("/profile", methods=['GET'])
def profile():
    """Gets profile of a user"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    email = request.form.get('email')
    if email is None:
        return
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token}), 200


@app.route("/reset_password", methods=["PUT"])
def update_password():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')
    if ((email is None or
         new_password is None or
         reset_token is None)):
        return
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
