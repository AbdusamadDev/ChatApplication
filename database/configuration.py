from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# SQLite database creation
engine = create_engine("sqlite:///db.sqlite3")
# To create tables in models.py
Base = declarative_base()
# To execute operations
session = Session(engine)


# For MySQL or PostgreSQL, use something like:
# engine = create_engine('mysql://user:password@localhost/dbname')
# engine = create_engine('postgresql://user:password@localhost/dbname')
