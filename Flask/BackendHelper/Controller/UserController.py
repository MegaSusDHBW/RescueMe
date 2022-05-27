import os
import re
from datetime import datetime, timezone, timedelta

import jwt
from flask import request, redirect, render_template, url_for, jsonify
from flask_cors import cross_origin
from flask_login import logout_user

from Flask.BackendHelper.Controller.token import token_required, generate_jwt, generate_pw_jwt, password_change
from Flask.BackendHelper.Cryptography.CryptoHelper import generateSalt, hashPassword
from Flask.BackendHelper.mail.mailhandler import pw_reset_mail, welcome_mail, sendEmergencyMail, mail_changed
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
            new_user = User.User(email=email, salt=salt, password=db_password, isAdmin=False)
            db.session.add(new_user)
            db.session.commit()

            welcome_mail(email, str(firstname) + " " + str(lastname))

            return redirect(url_for('login')), 201
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
                token = generate_jwt(email)
                print(token)
                return jsonify({'jwt': token}), 200
            else:
                return jsonify({'message': 'Check Credentials'}), 400
        return jsonify({'message': 'Bullshit'}), 400

    @staticmethod
    @cross_origin()
    def loginAdmin():
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
                isAdmin = user.isAdmin
            else:
                return jsonify({'message': 'Check Credentials'}), 400

            if user and key == new_key and isAdmin:
                # login_user(user)
                token = jwt.encode({'email': email, "exp": datetime.now(tz=timezone.utc) + timedelta(days=30)},
                                   os.getenv('secret_key'), algorithm='HS256')
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
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('login')), 200
        else:
            return redirect(url_for('sign_up')), 200



    @staticmethod
    @token_required
    def change_password(current_user):
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
    @cross_origin()
    @token_required
    def change_mail(current_user):
        email = current_user
        new_email = request.json["new_email"]
        new_email_confirm = request.json["new_email_confirm"]

        # Check if String is a Mail
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, new_email):
            return jsonify({"message": "Email is not valid"}), 400

        if new_email == new_email_confirm:
            user = User.User.query.filter_by(email=new_email).first()
            if user:
                return jsonify({'message': 'This mail is already registered'}), 400
            else:
                try:
                    db.session.query(User.User).filter(
                        User.User.email == email).update(
                        {
                            User.User.email: new_email,
                        },
                        synchronize_session=False)
                    db.session.commit()
                    token = generate_jwt(email)
                    print(token)
                    mail_changed(email, new_email)
                    return jsonify({'jwt': token}), 200
                except Exception as e:
                    return jsonify({'message': '{}'.format(e)}), 400
        else:
            return jsonify({'message': 'Email do not match'}), 400

    @staticmethod
    def forget_password_send_mail():
        email = request.json["email"]
        password = request.json["password"]

        user = User.User.query.filter_by(email=email).first()
        if user:
            jwt_pw = generate_pw_jwt(email, password)

            # TODO: Change Localhost to Server
            pw_reset_mail(email, "http://localhost:5000/change-password?jwt={}".format(jwt_pw))

        return jsonify(response="Email gesendet"), 200

    @staticmethod
    @password_change
    def forget_password(email, password):
        # email confirmed
        #email = request.args.get("email")
        #password = request.args.get("password").encode("utf-8")

        user = User.User.query.filter_by(email=email).first()
        if user:
            salt = user.salt
            pepper = os.getenv('pepper')
            pepper = bytes(pepper, 'utf-8')
            password = hashPassword(salt + pepper, password)
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
    def call_emergency_contact(current_user):
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
