from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

from flask_site import app

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String, 100)
    email = db.Column(db.String, 100)

    def __init__(self, name, email):
        self.name = name
        self.email = email