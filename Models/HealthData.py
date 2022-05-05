from Models.InitDatabase import db
from flask_login import UserMixin

class HealthData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.BINARY(32), unique=False)
    organDonorState = db.Column(db.String(20))
    bloodGroup = db.Column(db.String(64))
