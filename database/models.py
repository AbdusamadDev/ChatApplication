from sqlalchemy import Column, Integer, Table
from database.configuration import Base, metadata
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    emailing = Column(Integer)
    password = Column(String(100))

class Userqwe(Base):
    __tablename__ = "asdnower"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    emailsing = Column(Integer)
    password = Column(String(100))


class ChatGroupManager:
    def __init__(self, name) -> None:
        self.name = name

    def create_new_table(self, table_name):
        my_table = Table(
            "my_table",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String),
        )
