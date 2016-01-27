from sqlalchemy import Column, ForeignKey, Integer, \
                       String, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base
from .category import Category
from .user import User


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
        secondary='item_category'
    )

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
