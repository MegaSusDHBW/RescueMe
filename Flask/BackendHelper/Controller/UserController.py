import os
import re

import jwt
from flask import request, redirect, render_template, url_for, jsonify
from flask_cors import cross_origin
from flask_login import logout_user

from Flask.BackendHelper.Controller.token_required import token_required
from Flask.BackendHelper.Cryptography.CryptoHelper import generateSalt, hashPassword
from Flask.BackendHelper.mail.mailhandler import pw_reset_mail, welcome_mail, sendEmergencyMail
from Models import User
from Models.InitDatabase import db


class UserController:
    @staticmethod
    @cross_origin()
    def sign_up():
        if request.method == 'POST':
            json_data = request.get_json()
            email = json_data['email']
            firstname = json_data['firstName']
            lastname = json_data['lastName']
            password = json_data['password']
            passwordConfirm = json_data['passwordConfirm']

            # Check if String is a Mail
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.match(regex, email):
                return jsonify({"message": "Email is not valid"}), 400

            # Check if PASSWORD and PASSWORD_CONFIRM are the same
            if password != passwordConfirm:
                return jsonify({'message': 'Passwords do not match'}), 400

            # Check if EMAIL is already in use
            if User.User.query.filter_by(email=email).first() is not None:
                return jsonify({'message': 'Email already in use'}), 400

            salt = generateSalt()
            pepper = os.getenv('pepper')
            pepper = bytes(pepper, 'utf-8')
            db_password = hashPassword(salt + pepper, password)
            new_user = User.User(email=email, salt=salt, password=db_password)
            db.session.add(new_user)
            db.session.commit()

            welcome_mail(email, str(firstname) + " " + str(lastname))

            return redirect(url_for('login')), 200
        else:
            print('Error')
            return render_template('signUp.html'), 404

    @staticmethod
    @cross_origin()
    def login():
        if request.method == 'POST':
            json_data = request.get_json()
            email = json_data['email']
            password = json_data['password']

            # Check empty string fields
            if email == '' or password == '':
                return jsonify({'message': 'Check Credentials'}), 400
            elif not email or not password:
                return jsonify({'message': 'Check Credentials'}), 400

            user = User.User.query.filter_by(email=email).first()

            if user:
                salt = user.salt
                pepper = os.getenv('pepper')
                pepper = bytes(pepper, 'utf-8')
                key = user.password
                new_key = hashPassword(salt + pepper, password)
            else:
                return jsonify({'message': 'Check Credentials'}), 400

            if user and key == new_key:
                # login_user(user)
                token = jwt.encode({'email': email}, os.getenv('secret_key'), algorithm='HS256')
                print(token)
                return jsonify({'jwt': token}), 200
            else:
                return jsonify({'message': 'Check Credentials'}), 400
        return jsonify({'message': 'Bullshit'}), 400

    @staticmethod
    @cross_origin()
    @token_required
    def delete_user(current_user):
        email = current_user
        user = User.User.query.filter_by(email=email).first()
        if user:
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('login')), 200
        else:
            return redirect(url_for('sign_up')), 200

    @staticmethod
    @cross_origin
    @token_required
    def logout(current_user):
        logout_user()
        return redirect(url_for('login'))

    @staticmethod
    @token_required
    def changePassword(current_user):
        email = request.json["email"]
        password = request.json["password"]
        passwordConfirm = request.json["passwordConfirm"]

        user = User.User.query.filter_by(email=email).first()
        if user:
            db.session.query(User.User).filter(
                User.User.email == email).update(
                {
                    User.User.password: password,
                },
                synchronize_session=False)
            db.session.commit()
        else:
            print("Fehler beim Passwortändern"), 404

    @staticmethod
    def forgetPasswordSendMail():
        email = request.json["email"]
        password = request.json["password"]

        user = User.User.query.filter_by(email=email).first()
        if user:
            salt = user.salt
            pepper = os.getenv('pepper')
            pepper = bytes(pepper, 'utf-8')
            password = hashPassword(salt + pepper, password)
            # TODO
            pw_reset_mail(email,
                          "http://localhost:5000/change-password?email=" + str(email) + "&password=" + password.decode(
                              "iso8859_16"))

        return jsonify(response="Email gesendet"), 200

    @staticmethod
    def forgetPassword():
        # email confirmed
        email = request.args.get("email")
        password = request.args.get("password").encode("utf-8")

        user = User.User.query.filter_by(email=email).first()
        if user:
            db.session.query(User.User).filter(
                User.User.email == email).update(
                {
                    User.User.password: password,
                },
                synchronize_session=False)
            db.session.commit()

            return render_template("forgetPasswort.html"), 200
        else:
            return jsonify(response="Fehler"), 404

    @staticmethod
    @token_required
    def callEmergencyContact(current_user):
        email = request.json["email"]
        accidentplace = request.json["accidentplace"]
        hospital = request.json["hospital"]

        user = User.User.query.filter_by(email=email).first()
        if user:
            sendEmergencyMail(email, user.emergencyContact.firstname, user.emergencyContact.lastname,
                              user.healthData.firstname, user.healthData.lastname, accidentplace, hospital)

            return jsonify(response="Angehörige wurden informiert"), 200
        else:
            print("User nicht gefunden")
            return jsonify(response="Angehöriger konnte NICHT informiert werden"), 404
