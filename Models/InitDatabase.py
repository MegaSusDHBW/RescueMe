from flask_sqlalchemy import SQLAlchemy
from Flask.BackendHelper import DBHelper

db = SQLAlchemy()

def create_database(app):
    DBHelper.connect()
    db.init_app(app)
    db.create_all(app=app)
    print('Connected and tables created!')

