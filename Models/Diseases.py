from Models.InitDatabase import db
from Models.HealthData import HealthData


class Diseases(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.VARCHAR(100))
    #health_id = db.Column(db.Integer, db.ForeignKey('healthData.id'))
