import datetime
import os
from dotenv import load_dotenv
from Models import User

load_dotenv()
from functools import wraps
import jwt
from flask import request, jsonify

'''
The following is for our Authentication
'''


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
            user = User.User.query.filter_by(email=data['email']).first()
            if user:
                current_user = data['email']
            else:
                return jsonify({'message': 'Token seems to have non existent User'}), 401
        except Exception as e:
            return jsonify({'message': 'token is invalid', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorator


def param_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'jwt' in request.args:
            token = request.args.get('jwt')

        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            data = jwt.decode(token, os.getenv('secret_key'), algorithms=['HS256'])
            user = User.User.query.filter_by(email=data['email']).first()
            if user:
                current_user = data['email']
            else:
                return jsonify({'message': 'Token seems to have non existent User'}), 401
        except Exception as e:
            return jsonify({'message': 'token is invalid', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorator


def generate_jwt(mail):
    token = jwt.encode({'email': mail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)},
                       os.getenv('secret_key'), algorithm='HS256')
    return token


'''
The following is for our ResetPassword Function
'''


def generate_pw_jwt(mail, password):
    token = jwt.encode({'mail': mail, 'password': password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       os.getenv('secret_key'), algorithm='HS256')
    return token


def password_change(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'jwt' in request.args:
            token = request.args.get('jwt')

        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401

        try:
            data = jwt.decode(token, os.getenv('secret_key'), algorithms=['HS256'])
            password = data['password']
            mail = data['mail']
        except Exception as e:
            return jsonify({'message': 'token is invalid', 'error': str(e)}), 401

        return f(mail, password, *args, **kwargs)

    return decorator
