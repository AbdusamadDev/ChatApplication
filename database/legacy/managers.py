from sqlalchemy.exc import OperationalError, PendingRollbackError, IntegrityError
from sqlalchemy import Table, inspect, desc, select, asc
import logging

from ..configuration import session, engine, Base, metadata
from .utils import to_dict
from ..models import User

from datetime import datetime
import time


class BaseManager:
    page_size = None

    def count(self) -> int:
        """Overridable .count() method"""
        pass

    def paginate(self, *args, **kwargs):
        """
        A paginate function which should be overriden later
        on when using this class
        """
        pass

    def get_paginated_response(self, page, url):
        start = time.time()
        count = self.count()
        response_body = {"total": count}
        if page in range(count - self.page_size, count):
            response_body["next_page"] = f"{url}?page={page + 1}"
        if page > 1:
            response_body["previous_page"] = f"{url}?page={page - 1}"
        end = time.time()
        response_body["elapsed_time"] = end - start
        response_body["data"] = self.paginate()
        return response_body


class BaseDeclarativeManager(BaseManager):
    meta: Base = None  # type: ignore
    page_size = 25

    def __init__(self) -> None:
        assert self.meta is not None, TypeError("Meta can not be None")

    def add(self, **kwargs):
        try:
            session.add(self.meta(**kwargs))
            session.commit()
        except OperationalError as error:
            raise error
        except PendingRollbackError:
            session.rollback()
            raise IntegrityError(
                statement="UNIQUE constraint failed", params=..., orig=...
            )

    def count(self) -> int:
        return session.query(self.meta).count()

    def all(self):
        records = session.query(self.meta).all()
        serialized_records = []
        for record in records:
            serialized_record = to_dict(record)
            # Convert datetime objects to string representation
            for key, value in serialized_record.items():
                if isinstance(value, datetime):
                    serialized_record[key] = value.isoformat()
            serialized_records.append(serialized_record)
        return serialized_records

    def get(self, **kwargs):
        assert len(kwargs) == 1, AttributeError("Only one keyword argument allowed")
        column, value = next(iter(kwargs.items()))
        try:
            query = (
                session.query(self.meta).filter(getattr(self.meta, column) == value)
            ).first()
        except AttributeError:
            raise ValueError(f"{column} is not a valid attribute of {self.meta}")

        if not query:
            return None
        return to_dict(query)

    def filter(self, **kwargs):
        try:
            query = session.query(self.meta)

            # Apply filters based on key-value pairs in kwargs
            for key, value in kwargs.items():
                column = getattr(self.meta, key, None)
                if column is not None:
                    query = query.filter(column == value)

            records = query.all()
            return [to_dict(record) for record in records]
        except OperationalError:
            return []

    def delete(self, pk):
        try:
            obj = session.query(self.meta).get(pk)
            if obj:
                session.delete(obj)
                session.commit()
        except OperationalError as error:
            raise error

    def update(self, pk, **kwargs):
        try:
            obj = session.query(self.meta).get(pk)
            if obj:
                for attr, value in kwargs.items():
                    setattr(obj, attr, value)
                session.commit()
        except OperationalError as error:
            raise error


class BaseTableClassManager(BaseManager):
    table: Table = None
    page_size: int = 40

    def __init__(self) -> None:
        assert self.table is not None, TypeError("Table is empty")

    @property
    def tables(self):
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        return table_names

    def count(self) -> int:
        return session.query(self.table).count()

    def create(self):
        try:
            self.table.create(bind=engine)
        except OperationalError:
            logging.warning(
                f"Table '{self.table.name}' already exists, so just skipping"
            )
            return

    def add(self, **kwargs):
        session.execute(self.table.insert().values(**kwargs))
        session.commit()
        session.close()

    def all(self):
        table_instance = Table(self.table, metadata, autoload_with=engine)
        select_stmt = table_instance.select()
        results = []
        for row in session.execute(select_stmt):
            results.append(dict(row._mapping))
        return results

    def filter(self, **kwargs):
        return session.execute(self.table.select().where(**kwargs))

    def get(self, pk):
        with engine.connect() as connection:
            # Select row by ID
            query = self.table.select().where(self.table.c.id == pk)
            result = connection.execute(query).fetchone()

            if result is None:
                return None
        return {per[0]: str(per[-1]) for per in zip(self.table.c.keys(), result)}

    def update(self, pk, **kwargs):
        try:
            obj = session.query(self.table).get(pk)
            if obj:
                for attr, value in kwargs.items():
                    setattr(obj, attr, value)
                session.commit()
        except OperationalError as error:
            raise error

    def delete(self, pk):
        try:
            # Construct the delete statement
            stmt = self.table.delete().where(self.table.c.id == pk)
            # Execute the delete statement
            session.execute(stmt)
            # Commit the transaction
            session.commit()
        except OperationalError as error:
            session.rollback()
            raise error
