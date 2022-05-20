from Models.InitDatabase import db
from Models import User


class HealthData(db.Model):
    __tablename__ = 'healthData'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    firstname = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.String(32), unique=False)
    organDonorState = db.Column(db.String(20))
    bloodGroup = db.Column(db.String(64))
    birthdate = db.Column(db.DATE)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    allergies = db.relationship('Allergies', backref='healthData')
    diseases = db.relationship('Diseases', backref='healthData')
    vaccines = db.relationship('Vaccines', backref='healthData')
