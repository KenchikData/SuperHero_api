from sqlalchemy import Column, Integer, String
from .db import Base

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    intelligence = Column(Integer, nullable=True)
    strength = Column(Integer, nullable=True)
    speed = Column(Integer, nullable=True)
    power = Column(Integer, nullable=True)
