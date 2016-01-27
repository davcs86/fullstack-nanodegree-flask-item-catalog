from sqlalchemy import Column, ForeignKey, Integer, String, \
                       PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    items = relationship(
        'Item',
        secondary='item_category'
    )
    __table_args__ = (PrimaryKeyConstraint('id',
                                           name='_category_pk'),)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'items': self.items
        }
