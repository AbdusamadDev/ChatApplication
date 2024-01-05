from sqlalchemy import Column, Integer
from configuration import Base
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
