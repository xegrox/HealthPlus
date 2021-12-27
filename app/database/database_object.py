from abc import ABC, abstractmethod


class DatabaseObject(ABC):

    @property
    @abstractmethod
    def key(self) -> str:
        ...
