from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

# SQLite database creation
engine = create_engine("sqlite:///../db.sqlite3")


# To execute operations
metadata = MetaData()
session = Session(engine)
Base = declarative_base()

# For MySQL or PostgreSQL, use something like:
# engine = create_engine('mysql://user:password@localhost/dbname')
# engine = create_engine('postgresql://user:password@localhost/dbname')
