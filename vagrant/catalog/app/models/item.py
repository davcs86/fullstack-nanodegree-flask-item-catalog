from .base import *
import datetime
from .category import Category
from .user import User
from sqlalchemy_imageattach.entity import Image, image_attachment


class ItemPicture(Image, Base):
    """Item picture model."""
    __tablename__ = 'item_picture'
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship('Item')
    __tablename__ = 'item_picture'


class ItemCategory(Base):
    __tablename__ = 'item_category'
    item_id = Column(Integer, ForeignKey('item.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    __table_args__ = (PrimaryKeyConstraint('item_id',
                                           'category_id',
                                           name='_item_category_pk'),)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(1000), nullable=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship(User)
    categories = relationship(
        'Category',
        secondary='item_category',
        lazy='dynamic'
    )
    picture = image_attachment('ItemPicture')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = Column(DateTime,
                          default=datetime.datetime.utcnow,
                          onupdate=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'categories': self.categories,
            'author_id': self.author.id,
            'author': self.author.name
        }
