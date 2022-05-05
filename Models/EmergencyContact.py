from Models.InitDatabase import db


class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    firstname = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.String(32), unique=False)
    birthdate = db.Column(db.String(64))
    phonenumber = db.Column(db.String(64))
    email = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
