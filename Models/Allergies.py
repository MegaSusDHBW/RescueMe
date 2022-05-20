from Models.InitDatabase import db


class Allergies(db.Model):
    __tablename__ = 'allergies'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.VARCHAR(100))
    health_id = db.Column(db.Integer, db.ForeignKey('healthdata.id'))
