from flask_login import UserMixin

from Models.InitDatabase import db


class GlobalFernet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fernet = db.Column(db.VARBINARY(255), primary_key=True, unique=True)
