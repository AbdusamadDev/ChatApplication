from database.configuration import Base, engine, metadata, session
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy import String


class GlobalChat(Base):
    __tablename__ = "global_chat"
    id = Column(Integer, primary_key=True)
    message = Column(String(5000))


class GlobalChatManager:
    meta = GlobalChat

    def add(self, message):
        print("Adding message: ", message)
        session.add(self.meta(message=message))
        session.commit()


class Userqwe(Base):
    __tablename__ = "asdnoasdasdasdasdasdwer"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    emailsing = Column(Integer)
    password = Column(String(100))


class PrivateChatManager:
    def migrative_table(self, table_name) -> Base:
        class PrivateChat(Base):
            __tablename__ = table_name
            id = Column(Integer, primary_key=True, autoincrement=True)
            user_id = Column(String(50))
            messagesssss = Column(Integer)
            created_at = Column(DateTime, default=func.now())

        return PrivateChat

    def proceed_create(self):
        Base.metadata.create_all(engine)


def runner():
    for table in metadata.tables.keys():
        table = PrivateChatManager()
        table.migrative_table(table)


if __name__ == "__main__":
    # For migration purposes
    runner()
