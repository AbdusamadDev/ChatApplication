from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()
