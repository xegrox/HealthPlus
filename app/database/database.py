import shelve
import threading
from typing import ValuesView, TypeVar, KeysView

T = TypeVar('T', bound='DatabaseObject')


class DatabaseInterface:
    def __init__(self, lock: threading.Lock, db: shelve.Shelf):
        self.__db = db
        self.__lock = lock

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def put(self, item: T):
        self.__db[item.key] = item

    def remove(self, key: str):
        del self.__db[key]

    def get(self, key: str) -> T:
        return self.__db[key]

    def keys(self) -> KeysView[str]:
        return self.__db.keys()

    def values(self) -> ValuesView[T]:
        return self.__db.values()

    def exists(self, key: str) -> bool:
        return key in self.__db

    def close(self):
        self.__db.close()
        self.__lock.release()


"""Wrapper around a shelve database to support concurrency

Flask handles each HTTP request in a separate thread, which might cause the database to be written simultaneously
However, shelve does not support concurrent writes, causing simultaneous write operations to fail
The wrapper solves this by managing each operations with a single lock
The lock delays each operation until the previous one has completed, preventing writes from colliding
"""


class Database:
    def __init__(self, name: str):
        self.__name = name
        self.__lock = threading.Lock()

    def open(self) -> DatabaseInterface:
        self.__lock.acquire()
        db = shelve.open(self.__name)
        return DatabaseInterface(self.__lock, db)
