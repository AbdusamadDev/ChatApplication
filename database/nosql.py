from typing import Any, Optional, Sequence, Type, Union
from bson.codec_options import TypeRegistry
import pymongo


class NoSQLClientsManager(pymongo.MongoClient):
    def __init__(
        self,
        database_name: str,
        host: str | Sequence[str] | None = None,
        port: int | None = None,
        document_class: type | None = None,
        tz_aware: bool | None = None,
        connect: bool | None = None,
        type_registry: TypeRegistry | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            host, port, document_class, tz_aware, connect, type_registry, **kwargs
        )
        self.db = self[database_name]

    def create_group(self, table_name):
        name = self.db.create_collection(f"group_{table_name}")
        return name
