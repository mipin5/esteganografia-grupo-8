from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    mediums = db.relationship('Medium')

class Medium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    mtype = db.Column(db.String(5))
    password = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))