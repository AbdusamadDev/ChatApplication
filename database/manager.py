from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Column,
    String,
    Table,
    Text,
    func,
    desc,
)

from .legacy.managers import BaseTableClassManager, BaseDeclarativeManager
from .models import User, UserJoinedGroups, Group
from .configuration import metadata, session

import time


class GroupMessageManager(BaseTableClassManager):
    def __init__(self, table_name: str | None = None) -> None:
        self.name = table_name

    def group_ids(self):
        return [group for group in metadata.tables.keys() if group.startswith("group_")]

    @property
    def table(self) -> Table:
        if self.name is None:
            raise TypeError("Database name cannot be None.")
        return Table(
            self.name,
            metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", ForeignKey("users.id")),
            Column("message", Text(length=5000)),
            Column("type", String(20)),
            Column("sent_at", String(50)),
            extend_existing=True,
        )

    def paginate(self, page: int = 1):
        offset = (page - 1) * self.page_size
        paginated_query = (
            session.query(self.table)
            .order_by(desc(self.table.c.id))  # Order by ID in descending order
            .offset(offset)
            .limit(self.page_size)
            .all()
        )
        messages = []
        for message in paginated_query:
            user_id = message.user_id
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                message_dict = {
                    "id": message.id,
                    "message": message.message,
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "sent_at": message.sent_at,
                }
                messages.append(message_dict)

        return messages[::-1]


class DirectMessagingManager(BaseTableClassManager):
    def __init__(self, table_name: str | None = None) -> None:
        self.name = table_name

    @property
    def table(self) -> Table:
        if self.name is None:
            raise TypeError("Database name cannot be None.")
        return Table(
            self.name,
            metadata,
            Column("id", Integer, primary_key=True),
            Column("user_id", ForeignKey("users.id")),
            Column("message", Text(length=5000)),
            Column("created_at", DateTime, default=func.now()),
            extend_existing=True,
        )


class UserManager(BaseDeclarativeManager):
    meta = User


class UserJoinedGroupsManager(BaseDeclarativeManager):
    meta = UserJoinedGroups


class GroupManager(BaseDeclarativeManager):
    meta = Group

    @staticmethod
    def to_dict(obj):
        """
        Convert SQLAlchemy object to dictionary with field names as keys.
        """
        if hasattr(obj, "__table__"):
            # If it's an SQLAlchemy ORM object
            return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        else:
            # If it's a regular Python object
            return {
                key: getattr(obj, key)
                for key in obj.__dict__.keys()
                if not key.startswith("_")
            }

    def paginate(self, page: int = 1):
        offset = (page - 1) * self.page_size
        paginated_query = (
            session.query(self.meta)
            .order_by(desc(self.meta.id))  # Order by ID in descending order
            .offset(offset)
            .limit(self.page_size)
            .all()
        )
        # Returning the paginated results
        response = [self.to_dict(data) for data in paginated_query]
        return response


def add_message_to_db(table_name, **data):
    table = metadata.tables[table_name]
    session.execute(table.insert(), data)
    session.commit()


if __name__ == "__main__":
    add_message_to_db(
        table_name="group_6f82b02a-bc8a-4999-a62d-c467bf2bbb1d",
        user_id=1,
        message="asdasd",
        type="asdasd",
        sent_at="now",
    )
