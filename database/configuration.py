from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

# SQLite database creation
engine = create_engine("sqlite:///db.sqlite3")


# To create tables in models.py
def get_base():
    base = declarative_base()
    base.metadata.create_all(engine)
    return base


# To execute operations
metadata = MetaData()
session = Session(engine)
Base = get_base()

# For MySQL or PostgreSQL, use something like:
# engine = create_engine('mysql://user:password@localhost/dbname')
# engine = create_engine('postgresql://user:password@localhost/dbname')
