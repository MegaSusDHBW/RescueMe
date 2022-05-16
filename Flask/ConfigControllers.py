from flask import Flask
from flask_login import LoginManager

from Flask.BackendHelper.Controller.DataController import DataController
from Flask.BackendHelper.Controller.QRCodeController import QRCodeController
from Flask.BackendHelper.Controller.UserController import UserController
from Flask.BackendHelper.Controller.ViewController import ViewController
from Flask.BackendHelper.DB.DBHelper import *
from Models import User
from Models.InitDatabase import *

# Für lokales Windows template_folder=templates
project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'static/templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
create_database(app=app)

# LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.User.query.get(int(id))


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
    app.run()
