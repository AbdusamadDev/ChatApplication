from database.configuration import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func,
    ForeignKey,
    String,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(80), unique=True)
    password = Column(String(70))
    joined_groups = relationship("UserJoinedGroups", back_populates="user")
    joined_at = Column(DateTime, default=func.now())


class UserJoinedGroups(Base):
    __tablename__ = "user_joined_groups"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_table_name = Column(String(100), unique=True)
    joined_at = Column(DateTime, default=func.now())

    # Define the relationship to the User table
    user = relationship("User", back_populates="joined_groups")


class Group(Base):
    __tablename__ = "Group"

    id = Column(Integer, autoincrement=True, primary_key=True)
    admin_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(70), unique=False)
    description = Column(String(200))
    table_name = Column(String(150))
    members_count = Column(Integer, default=0)
    link = Column(String(200))
    image = Column(String(300), default="")
    date_created = Column(DateTime, default=func.now())
