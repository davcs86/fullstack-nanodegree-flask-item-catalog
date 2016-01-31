from .base import *


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    __table_args__ = (PrimaryKeyConstraint('id',
                                           name='_category_pk'),)
