from Models.InitDatabase import db


class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    firstname = db.Column(db.String(100), unique=False)
    lastname = db.Column(db.String(32), unique=False)
    organDonorState = db.Column(db.String(20))
    bloodGroup = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
