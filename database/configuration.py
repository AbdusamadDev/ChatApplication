from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


path = os.getenv("BASE_DIR")
engine = create_engine(f"sqlite:///db.sqlite3")
Base = declarative_base()
metadata = MetaData()
metadata.reflect(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
print(path)
# For MySQL or PostgreSQL, use something like:
# engine = create_engine('mysql://user:password@192.168.100.39/dbname')
# engine = create_engine('postgresql://user:password@192.168.100.39/dbname')
