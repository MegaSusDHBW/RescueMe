import os

from flask import request, redirect, render_template, url_for
from flask_cors import cross_origin
from flask_login import login_user, login_required, logout_user

from Flask.BackendHelper.mail.mailhandler import pw_reset_mail, welcome_mail
from Models import User
from Models.InitDatabase import db
from Flask.BackendHelper.Cryptography.CryptoHelper import generateSalt, hashPassword


class UserController:
    @staticmethod
    @cross_origin()
    def sign_up():
        if request.method == 'POST':
            json_data = request.get_json()
            email = json_data['email']
            password = json_data['password']
            passwordConfirm = json_data['passwordConfirm']

            user = User.User.query.filter_by(email=email).first()

            if password == passwordConfirm and not user:
                salt = generateSalt()
                pepper = os.getenv('pepper')
                pepper = bytes(pepper, 'utf-8')
                db_password = hashPassword(salt + pepper, password)
                new_user = User.User(email=email, salt=salt, password=db_password)
                db.session.add(new_user)
                db.session.commit()

                welcome_mail(email, "Hans Peter")

                return redirect(url_for('login'))
            else:
                print('Error')
        return render_template('signUp.html')

    @staticmethod
    @cross_origin()
    def login():
        if request.method == 'POST':
            json_data = request.get_json()
            email = json_data['email']
            password = json_data['password']
            # email = request.form.get('email')
            # password = request.form.get('password')

            user = User.User.query.filter_by(email=email).first()

            if user:
                salt = user.salt
                pepper = os.getenv('pepper')
                pepper = bytes(pepper, 'utf-8')
                key = user.password
                new_key = hashPassword(salt + pepper, password)
            else:
                return redirect(url_for('sign_up'))

            if user and key == new_key:
                login_user(user)
                print('Logged In')
                return redirect(url_for('home'))
            else:
                print('Error')
        return render_template('login.html')

    @staticmethod
    @cross_origin()
    @login_required
    def delete_user():
        email = request.args['email']
        user = User.User.query.filter_by(email=email).first()
        if user:
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return redirect(url_for('sign_up'))

    @staticmethod
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @staticmethod
    def changePassword():
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
            print("Fehler beim Passwortändern")

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
            #TODO
            pw_reset_mail(email, "http://localhost:5000/change-password?email="+str(email)+"&password="+password.decode("utf-8"))
            #pw_reset_mail(email, 'http://web.de')
        return 200


    @staticmethod
    def forgetPassword():
        #email confirmed
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

            return render_template("Passwort zurückgesetzt")
        else:
            print("Fehler beim Passwortändern")


