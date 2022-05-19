import json
import pickle
from functools import wraps

import jwt
from flask_login import LoginManager

from Flask.BackendHelper.Controller.UserController import UserController
from Flask.BackendHelper.Controller.DataController import DataController
from Flask.BackendHelper.Controller.QRCodeController import QRCodeController
from Flask.BackendHelper.Controller.ViewController import ViewController
from Flask.BackendHelper.Cryptography.CryptoHelper import generateFernet
from Flask.BackendHelper.DB.DBHelper import *
from Models import User
from Models.InitDatabase import *
from flask import Flask, request, jsonify

app = Flask(__name__, template_folder="../templates")
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
create_database(app=app)

'''ViewController'''
# @app.route("/")
app.add_url_rule("/", view_func=ViewController.main, methods=['GET', 'POST'])
# @app.route("/home", methods=['GET', 'POST'])
app.add_url_rule("/home", view_func=ViewController.home, methods=['GET', 'POST'])

'''DataController'''
# /encrypt/notfallkontakt
app.add_url_rule("/set-emergencycontact", view_func=DataController.setEmergencyContact, methods=['POST'])
# /encrypt/gesundheitsdaten
app.add_url_rule("/set-healthdata", view_func=DataController.setHealthData, methods=['POST'])
# /getGeodata
app.add_url_rule("/get-geodata", view_func=DataController.getGeodata, methods=['POST'])
# /getHospitals
app.add_url_rule("/get-hospitals", view_func=DataController.getHospitals, methods=['POST'])
# getHealthData
app.add_url_rule("/get-healthdata", view_func=DataController.getHealthData, methods=['GET'])
# getEmergencyContact
app.add_url_rule("/get-emergencycontact", view_func=DataController.getEmergencyContact, methods=['GET'])

'''QRCodeController'''
# /encrypt/qrcode"
app.add_url_rule("/create-qrcode", view_func=QRCodeController.generateQRCode, methods=['GET'])
# @app.route("/decrypt", methods=['POST'])
app.add_url_rule("/read-qrcode", view_func=QRCodeController.readQRCode, methods=['POST'])

'''UserController'''
# @app.route("/sign-up", methods=['GET', 'POST'])
app.add_url_rule("/sign-up", view_func=UserController.sign_up, methods=['GET', 'POST'])
# @app.route("/login", methods=['GET', 'POST'])
app.add_url_rule("/login", view_func=UserController.login, methods=['GET', 'POST'])
# @app.route("/delete-user", methods=['GET', 'POST'])
app.add_url_rule("/delete-user", view_func=UserController.delete_user, methods=['GET', 'POST'])
# @app.route("/logout")
app.add_url_rule("/logout", view_func=UserController.logout, methods=['GET', 'POST'])
# change PW
app.add_url_rule("/change-password", view_func=UserController.changePassword, methods=['POST'])
# forget PW
app.add_url_rule("/forget-password", view_func=UserController.forgetPasswordSendMail, methods=['POST'])
# confirm email
app.add_url_rule("/change-password", view_func=UserController.forgetPassword, methods=['GET'])

if __name__ == "__main__":
    # Opening JSON file
    with open('../globalFernetFile.json', 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    print(json_object["fernet"])
    if json_object["fernet"] == "":
        globalFernet = generateFernet()
        dictionary = {
            "fernet": pickle.dumps(globalFernet).decode("iso8859_16")
        }
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        # Writing to sample.json
        with open("../globalFernetFile.json", "w") as outfile:
            outfile.write(json_object)

    app.run()

