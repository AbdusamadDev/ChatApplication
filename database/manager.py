from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Column,
    Table,
    Text,
    func,
)

from .legacy.managers import BaseTableClassManager, BaseDeclarativeManager
from .models import User, UserJoinedGroups, Group
from .configuration import metadata

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
            Column("created_at", DateTime, default=func.now()),
            extend_existing=True,
        )

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


if __name__ == "__main__":
    table = GroupMessageManager(table_name="group_b76e2da7-ac49-4f5f-bfab-cc15ea366a8d")
    start = time.time()
    record = table.delete(pk=12)
    end = time.time()
    print("RECORD: ", record)