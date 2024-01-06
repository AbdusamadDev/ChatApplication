from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()
sys_path = os.path.abspath(os.getenv("SYSTEM_PATH"))
# SQLite database creation
engine = create_engine("sqlite:///{}db.sqlite3".format(sys_path))


# To execute operations
metadata = MetaData()
session = Session(engine)
Base = declarative_base()

# For MySQL or PostgreSQL, use something like:
# engine = create_engine('mysql://user:password@localhost/dbname')
# engine = create_engine('postgresql://user:password@localhost/dbname')
