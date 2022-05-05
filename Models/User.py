from Models.InitDatabase import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    email = db.Column(db.String(100), unique=True)
    salt = db.Column(db.BINARY(32), unique=True)
    password = db.Column(db.BINARY(64))
    idHealthData = db.relationship('HealthData', backref='user', uselist=False, primaryjoin='User.idHealthData==HealthData.id')
    idEmergencyContact = db.relationship('EmergencyContact', backref='user', uselist=False, primaryjoin='User.idEmergencyContact==EmergencyContact.id')
