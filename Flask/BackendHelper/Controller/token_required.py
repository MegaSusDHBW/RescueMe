import os
from dotenv import load_dotenv
from Models import User
load_dotenv()
from functools import wraps
import jwt
from flask import request, jsonify


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'jwt' in request.headers:
            token = request.headers['jwt']
        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            data = jwt.decode(token, os.getenv('secret_key'), algorithms=['HS256'])
            print(data)
            current_user = User.User.query.filter_by(email=data['email']).first()
        except Exception as e:
            return jsonify({'message': 'token is invalid', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorator
