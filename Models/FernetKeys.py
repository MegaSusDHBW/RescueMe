from flask_login import UserMixin

from Models.InitDatabase import db


class FernetKeys(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), primary_key=True, unique=True)
    fernet = db.Column(db.BLOB)
