import threading
import time
import os

from app.database.database import Database, DatabaseObject, DatabaseInterface
import unittest


class Propagate(threading.Thread):
    def __init__(self, cls):
        super().__init__(target=cls.run)
        self._target = cls.run
        self.ex = None

    def run(self):
        try:
            self._target()
        except BaseException as e:
            self.ex = e

    def join(self, timeout=None):
        super().join(timeout=timeout)
        if self.ex is not None:
            raise self.ex


class TestObject(DatabaseObject):
    def __init__(self, key: str, value):
        self.__key = key
        self.value = value

    @property
    def key(self) -> str:
        return self.__key


class TestDatabaseCRUDConcurrency(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database('test_db')

    def tearDown(self) -> None:
        os.remove('test_db')

    def test_add(self):
        def operation(interface: DatabaseInterface, value: str, sleep: float):
            item = TestObject('key', value)
            time.sleep(sleep)
            interface.put(item)

        t1 = self.db.dispatch(lambda x: operation(x, 'first', 1))
        t2 = self.db.dispatch(lambda x: operation(x, 'second', 0.5))
        t1.join()
        t2.join()
        result = self.db.dispatch(lambda x: self.assertEqual(x.get('key').value, 'second'), autostart=False)
        propagate = Propagate(result)  # Propagate error from 'result' thread to main thread
        propagate.start()
        propagate.join()
