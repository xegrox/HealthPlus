from abc import ABC, abstractmethod


class DatabaseObject(ABC):

    @property
    @abstractmethod
    def key(self) -> str:
        ...


class BasicDatabaseObject(DatabaseObject):

    def __init__(self, key, value):
        self.__key = key
        self.value = value

    @property
    def key(self) -> str:
        return self.__key
