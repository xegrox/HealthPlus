import shelve
import threading
from typing import Callable, ValuesView
from .database_object import DatabaseObject


class DatabaseInterface:
    def __init__(self, db: shelve.Shelf):
        self.__db = db

    def put(self, item: DatabaseObject):
        self.__db[item.key] = item

    def remove(self, key: str):
        del self.__db[key]

    def get(self, key: str) -> DatabaseObject:
        return self.__db[key]

    def values(self) -> ValuesView[DatabaseObject]:
        return self.__db.values()


"""Wrapper around a shelve database to support concurrency

Flask handles each HTTP request in a separate thread, which might cause the database to be written by multiple threads 
at the same time
However, shelve does not support concurrent writes, causing the write operations to fail
The wrapper solves this by propagating each write operation into different threads managed by a single lock
The lock delays each thread until the previous one has completed, preventing the risk of write operations colliding
"""


class Database:
    def __init__(self, name: str):
        self.__name = name
        self.__lock = threading.Lock()

    def dispatch(self, operation: Callable[[DatabaseInterface], None], autostart=True) -> threading.Thread:
        """Run crud operations on a lock managed thread

        Parameters
        ----------
        autostart : bool
            Starts operation immediately if True. Defaults to True
        operation : Callable[[DatabaseInterface], None]
            Callback with interface for crud operations

        Example
        -------
        The following inserts 'item' at 'item.key' into a database named 'example'
        >>> item = DatabaseObject()
        ... db = Database('example')
        ...
        ... def add_item(interface):
        ...    interface.put(item)
        ...
        ... db.dispatch(add_item)

        Returns
        -------
        Thread
            The thread that the dispatched operation is running on
        """
        def worker():
            self.__lock.acquire()  # Wait until lock has been released
            db = shelve.open(self.__name)
            interface = DatabaseInterface(db)
            operation(interface)
            db.close()
            self.__lock.release()  # Release lock once operation completed

        t = threading.Thread(target=worker)
        if autostart:
            t.start()
        return t
