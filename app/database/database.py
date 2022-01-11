import shelve
import threading
from typing import ValuesView, TypeVar, KeysView

T = TypeVar('T', bound='DatabaseObject')


class DatabaseInterface:
    def __init__(self, db: shelve.Shelf):
        self.__db = db

    def __contains__(self, item):
        return self.__db.__contains__(item)

    def __getitem__(self, item):
        return self.__db[item]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def put(self, item: T):
        self.__db[item.key] = item

    def remove(self, key: str):
        del self.__db[key]

    def get(self, key: str) -> T:
        return self.__db.get(key)

    def keys(self) -> KeysView[str]:
        return self.__db.keys()

    def values(self) -> ValuesView[T]:
        return self.__db.values()

    def close(self):
        self.__db.close()


"""Wrapper around a shelve database to support concurrency

Flask handles each HTTP request in a separate thread, which might cause the database to be written simultaneously
However, shelve does not support concurrent writes, causing simultaneous write operations to fail
The wrapper solves this by managing each operations with a single lock
The lock delays each operation until the previous one has completed, preventing writes from colliding
"""


class BasicDatabase:
    def __init__(self, name: str):
        self.__name = name
        self.__lock = threading.Lock()

    def open(self):
        self.__lock.acquire()
        db = shelve.open(self.__name)

        def close(it):
            shelve.Shelf.close(it)
            if self.__lock.locked():
                self.__lock.release()

        db.close = close.__get__(db, shelve.Shelf)
        return db


class Database(BasicDatabase):
    def __init__(self, name: str):
        super().__init__(name)

    def open(self):
        db = super().open()
        return DatabaseInterface(db)
