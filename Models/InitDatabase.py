from flask_sqlalchemy import SQLAlchemy
from Flask.BackendHelper import DBHelper

db = SQLAlchemy()

def create_database(app):
    try:
        DBHelper.connect()
        db.init_app(app)
        db.create_all(app=app)
        print('Connected and tables created!')
    except:
        DBHelper.createDB()
        DBHelper.connect()
        db.init_app(app)
        db.create_all(app=app)
        print('Database created and tables created!')

