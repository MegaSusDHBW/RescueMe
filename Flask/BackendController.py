import json

import rsa
import what3words as what3words
from flask import render_template, Flask, request, redirect, url_for, jsonify, send_file
from flask_cors import cross_origin
from flask_login import login_user, login_required, logout_user, LoginManager

from Flask.BackendHelper.DBHelper import *
from Flask.BackendHelper.QRCode import generateQRCode
from Flask.BackendHelper.crypt import decryptData
from Flask.BackendHelper.hash import hashPassword, generateSalt
from Models import EmergencyContact
from Models import HealthData
from Models import User
from Models.InitDatabase import *

# Für lokales Windows template_folder=templates
app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
create_database(app=app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

dict_emergencycontact = {}
dict_healthdata = {}


@login_manager.user_loader
def load_user(id):
    return User.User.query.get(int(id))


publicKey, privateKey = rsa.newkeys(512)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        return redirect(url_for('logout'))
    return render_template('home.html')


@app.route("/sign-up", methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
        else:
            print('Error')
    return render_template('signUp.html')


@app.route("/login", methods=['GET', 'POST'])
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


@app.route("/delete-user", methods=['GET', 'POST'])
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/encrypt/notfallkontakt", methods=['POST'])
def getEmergencyContact():
    global dict_emergencycontact

    contact_json = request.get_json()
    try:
        firstname = contact_json["firstName"]
        lastname = contact_json["lastName"]
        birthdate = contact_json["birthDate"]
        phonenumber = contact_json["phoneNumber"]
        email = contact_json["email"]
        user_mail = contact_json["userMail"]

        user = User.User.query.filter_by(email=user_mail).first()
        if user:
            new_emergencycontact = EmergencyContact.EmergencyContact(firstname=firstname, lastname=lastname,
                                                                     birthdate=birthdate,
                                                                     phonenumber=phonenumber, email=email,
                                                                     user_id=user.id)
            db.session.add(new_emergencycontact)
            db.session.commit()
        else:
            return jsonify(response="User nicht vorhanden"), 404

        return jsonify(response="Notfallkontakt angelegt"), 200
    except:
        return jsonify(response="Fehler beim Anlegen des Notfallkontakts"), 404


@app.route("/encrypt/gesundheitsdaten", methods=['POST'])
def getHealthData():
    global dict_healthdata
    healthdata_json = request.get_json()
    try:
        firstname = healthdata_json["firstName"]
        lastname = healthdata_json["lastName"]
        organDonorState = healthdata_json["organDonorState"]
        bloodGroup = healthdata_json["bloodGroup"]
        user_mail = healthdata_json["userMail"]

        user = User.User.query.filter_by(email=user_mail).first()
        if user:
            new_healthdata = HealthData.HealthData(firstname=firstname, lastname=lastname,
                                                   organDonorState=organDonorState,
                                                   bloodGroup=bloodGroup, user_id=user.id)
            db.session.add(new_healthdata)
            db.session.commit()
        else:
            return jsonify(response="User nicht vorhanden"), 404

        return jsonify(response="Gesundheitsdaten erhalten"), 200
    except:
        return jsonify(response="Fehler beim Anlegen der Gesundheitsdaten"), 404


@app.route("/encrypt/qrcode", methods=['GET'])
def encrypt():
    user_mail = request.args.get('email')
    date = request.args.get('date')
    user = User.User.query.filter_by(email=user_mail).first()

    qrcode_dict = {}

    q = db.session.query(
        User.User.email, HealthData.HealthData.firstname, HealthData.HealthData.lastname,
        HealthData.HealthData.organDonorState, HealthData.HealthData.bloodGroup,
        EmergencyContact.EmergencyContact.email, EmergencyContact.EmergencyContact.firstname,
        EmergencyContact.EmergencyContact.lastname, EmergencyContact.EmergencyContact.birthdate,
        EmergencyContact.EmergencyContact.phonenumber
    ).join(
        EmergencyContact.EmergencyContact
    ).join(
        HealthData.HealthData
    ).filter(user.email == user_mail)

    user_info = q[0]

    #Nicht hardcoden TODO
    qrcode_dict.update({"email": user_info[0]})
    qrcode_dict.update({"firstname": user_info[1]})
    qrcode_dict.update({"lastname": user_info[2]})
    qrcode_dict.update({"organDonorState": user_info[3]})
    qrcode_dict.update({"bloodGroup": user_info[4]})
    qrcode_dict.update({"emergencyEmail": user_info[5]})
    qrcode_dict.update({"emergencyFirstname": user_info[6]})
    qrcode_dict.update({"emergencyLastname": user_info[7]})
    qrcode_dict.update({"emergencyBirthday": user_info[8]})
    qrcode_dict.update({"emergencyPhone": user_info[9]})

    print(qrcode_dict)

    qrcode = generateQRCode(qrcode_dict)
    image = 'BackendHelper/QR/qrcode.png'

    return send_file(image, mimetype='image/png'), 200


@app.route("/decrypt", methods=['GET', 'POST'])
def decrypt():
    encryptedJSON = b'gAAAAABias2I9qSxvMH8eg7WT6f3-xrDLgMxIY5yhIQkUU0sy1v_R7-HDa_LdcBGd4v1Tkx27hBnDuwFuGYwjAvtTDSnQDujKiQ_n4GzDexjz08qZGKkBbqz9DFROmZzbBlFtOf1hNvK'

    with open('BackendHelper/Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    decryptedJSON = decryptData(encryptedJSON, key)
    data = json.loads(decryptedJSON)
    print(data)
    return 'Decryption success'


@app.route("/getGeodata", methods=['POST'])
def getGeodata():
    try:
        json_data = request.get_json()
        Y = json_data["coords"]["longitude"]
        X = json_data["coords"]["latitude"]

        print("X: " + str(X))
        print("Y:" + str(Y))

        geocoder = what3words.Geocoder("U7LVW2RA")

        res = geocoder.convert_to_3wa(what3words.Coordinates(X, Y))
        print(res["words"])

        return jsonify(words=res["words"]), 200
    except:
        return jsonify(words="Fehler beim Umwandeln der Koordinaten in What3Words"), 404


if __name__ == "__main__":
    app.run()
