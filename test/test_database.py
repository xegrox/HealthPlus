import os
from concurrent.futures import ThreadPoolExecutor
from app.database import Database, DatabaseObject
import unittest


class TestObject(DatabaseObject):
    def __init__(self, key: str, value):
        self.__key = key
        self.value = value

    @property
    def key(self) -> str:
        return self.__key


class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database('test_db')

    def tearDown(self) -> None:
        os.remove('test_db')

    def test_concurrency(self):
        def worker():
            item = TestObject('key', 'value')
            with self.db.open() as db:
                db.put(item)

        with ThreadPoolExecutor(max_workers=2) as executor:
            # Execute writes in parallel
            t1 = executor.submit(worker)
            t2 = executor.submit(worker)
            t1.result()
            t2.result()  # No error is thrown because write in t2 waits for write in t1 to complete

