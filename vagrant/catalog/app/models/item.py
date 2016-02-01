from .base import *
import datetime
from .category import Category
from .user import User
from sqlalchemy_imageattach.entity import Image, image_attachment

# Item-related models


class ItemPicture(Image, Base):
    """Item picture model, based on the sqlalchemy_imageattach extension
    http://sqlalchemy-imageattach.readthedocs.org/en/latest/guide/declare.html
    """
    __tablename__ = 'item_picture'
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    item = relationship('Item')


class ItemCategory(Base):
    """Item category model (many to many)."""
    __tablename__ = 'item_category'
    item_id = Column(Integer, ForeignKey('item.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    __table_args__ = (PrimaryKeyConstraint('item_id',
                                           'category_id',
                                           name='_item_category_pk'),)


class Item(Base):
    """Item model."""
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
    def default_picture_url(self):
        """ Returns the url for the first image associated the the item,
            or a placehold.it image """
        picture_url = 'https://placehold.it/256x256'
        first_picture = self.picture.first()
        if first_picture is not None:
            try:
                picture_url = first_picture.locate()
            except:
                # ignore it
                print sys.exc_info()[0]
        return picture_url

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'author': self.author.serialize,
            'categories': [g.serialize
                           for g in self.categories],
            'description': self.description,
            'id': self.id,
            'title': self.name,
            'updated': self.updated_date,
            'published': self.created_date,
            'images': [g.locate() for g in self.picture.all()]
        }
