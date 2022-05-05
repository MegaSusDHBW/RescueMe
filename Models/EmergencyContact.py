from Models.InitDatabase import db
from flask_login import UserMixin


class EmergencyContact(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.String(32), unique=False)
    birthdate = db.Column(db.String(64))
    phonenumber = db.Column(db.String(64))
    email = db.Column(db.String(100))

    user = db.relationship("User")
