from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, ForeignKey, Integer, String,
                        PrimaryKeyConstraint, UniqueConstraint)
from sqlalchemy.orm import relationship

Base = declarative_base()
