from Models.InitDatabase import db
from Models import HealthData


class Vaccines(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    name = db.Column(db.VARCHAR(100))
    health_id = db.Column(db.ForeignKey('healthData.id'))