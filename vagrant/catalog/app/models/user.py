from flask.ext.login import UserMixin
from .base import *

# Model for user info, composed by the UserMixin by the Flask-Login extension
# and the declarative base of sqlalchemy


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(32), nullable=False, unique=True)
    password = Column(String(128))
    google_id = Column(String(128))
    twitter_id = Column(String(128))
    github_id = Column(String(128))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'nickname': self.nickname
        }
