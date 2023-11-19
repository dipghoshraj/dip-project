

from flask import request, jsonify
from model import Account

def authenticate_user(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization

        username, password =  auth.username, auth.password
        user = Account.query.filter(auth_id = password, username = username).first()

        if user:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    return wrapper