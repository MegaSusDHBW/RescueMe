from Models.InitDatabase import db


class GlobalFernet(db.Model):
    __tablename__ = 'globalfernet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fernet = db.Column(db.VARBINARY(255), primary_key=True, unique=True)
