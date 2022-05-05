from Models.InitDatabase import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    salt = db.Column(db.BINARY(32), unique=True)
    password = db.Column(db.BINARY(64))
    idHealthData = db.Column(db.ForeignKey)
    idEmergencyContact = db.Column(db.ForeignKey)
