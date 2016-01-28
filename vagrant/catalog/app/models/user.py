from sqlalchemy import Column, Integer, String, UniqueConstraint
from flask.ext.login import UserMixin
from .base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(32), nullable=False, unique=True)
    password = Column(String(128))
    google_id = Column(String(64))
    facebook_id = Column(String(64))
    twitter_id = Column(String(64))
    github_id = Column(String(64))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'nickname': self.nickname
        }
