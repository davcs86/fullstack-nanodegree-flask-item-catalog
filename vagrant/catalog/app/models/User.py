from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    google_token = db.Column(db.String)
    facebook_token = db.Column(db.String)
    twitter_token = db.Column(db.String)
