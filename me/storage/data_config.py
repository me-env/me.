from enum import Enum, auto
from dataclasses import dataclass

from typing import List


class DataType(Enum):
    TXs = 'transaction'


class DataAction(Enum):
    READ = 'read'
    UPDATE = 'update'
    CREATE = 'create'
    DELETE = 'delete'


@dataclass(frozen=True)
class DataAccess:
    data_type: DataType
    actions: List[DataAction]

    def __le__(self, other):
        """
        Used to check if other data is same type and has at least the access rights that 'self' has
        """
        return other.data_type == self.data_type and all([a in other.actions for a in self.actions])

    def __ge__(self, other):
        return other.data_type == self.data_type and all([a in self.actions for a in other.actions])


