from flask_login import UserMixin

from Models.InitDatabase import db


class FernetData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.VARCHAR(5000))
    fernet = db.Column(db.VARBINARY(255), primary_key=True)
