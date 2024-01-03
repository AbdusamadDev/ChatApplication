from sqlalchemy import Column, Integer, String, Table
from configuration import metadata


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True),
    Column("email", String(120), unique=True),
)
