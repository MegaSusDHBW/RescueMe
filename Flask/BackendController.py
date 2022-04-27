import json

import what3words as what3words
import rsa
from flask import render_template, Flask, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from Flask.BackendHelper.DBHelper import *
from Flask.BackendHelper.QRCode import generateQRCode
from Flask.BackendHelper.crypt import generateKeypair, encryptData, decryptData
from Flask.BackendHelper.hash import hashPassword, generateSalt
from Models.InitDatabase import *
from Models import User

# Für lokales Windows template_folder=templates
app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
create_database(app=app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

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
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

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
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.User.query.filter_by(email=email).first()
        salt = user.salt
        pepper = os.getenv('pepper')
        pepper = bytes(pepper, 'utf-8')
        key = user.password
        new_key = hashPassword(salt + pepper, password)

        if user and key == new_key:
            login_user(user)
            print('Logged In')
            return redirect(url_for('home'))
        else:
            print('Error')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/encrypt", methods=['GET', 'POST'])
def encrypt():
    data = '{"name": "Hans", "alter": 50}'
    data = json.dumps(data).encode('utf-8')

    fernet = generateKeypair(publicKey)
    encryptedJSON = encryptData(data, fernet)
    print(encryptedJSON)

    generateQRCode(encryptedJSON)
    return encryptedJSON


@app.route("/decrypt", methods=['GET', 'POST'])
def decrypt():
    encryptedJSON = b'gAAAAABiYsjMXQL5n4ubzAYdf82PRcBXVTT2cfrPGvMUvt4y-Grv3vM4gXh8x7JhpLEIf2A6oCcNFGZ_RwTHKgoQ4hxTqXx72fHctYbBA0wrIZwoHEVCOJvtvraaJx8sclq2jSV79h7F'

    with open('BackendHelper/Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    decryptedJSON = decryptData(encryptedJSON, key)
    data = json.loads(decryptedJSON)
    print(data)
    return 'Decryption success'


@app.route("/getGeodata", methods=['GET', 'POST'])
def getGeodata():
    # public
    geocoder = what3words.Geocoder("what3words-api-key")

    # eigener Server
    # geocoder = what3words.Geocoder("what3words-api-key", end_point='http://localhost:8080/v3')

    X = 51.484463
    Y = -0.195405

    res = geocoder.convert_to_3wa(what3words.Coordinates(X, Y))
    print(res)

    # Um Worte in Koordinaten umzuwandeln
    # res = geocoder.convert_to_coordinates('prom.cape.pump')
    # print(res)


# Pfusch aber lassen wir mal so
if __name__ == "__main__":
    app.run()
