from abc import ABC, abstractmethod

from typing import List

from me.storage.data_config import DataType, DataAccess


class Plugin(ABC):
    def __init__(self, name, run_strategy):
        self._name = name
        self._run_strategy = run_strategy

    @property
    def name(self):
        return self._name


class IDataSource(ABC):
    @abstractmethod
    def getData(self, columns, check, convert):
        """
        Get data from the datasource.
        Done in a thread to let the data source run
        """

    @abstractmethod
    def getAccessAuth(self):
        """
        Get information about who can access data
        """

    @abstractmethod
    def getStorageDetails(self):
        """
        Get information about how to store data, such as the type of database needed and where to store it
        """
        # Example
        return {
            'db': 'psql',
            'schema': 'me_banking',
            'table': 'transactions',
            'type': DataType.TXs
        }


class IService(ABC):
    @abstractmethod
    def neededDataDetails(self) -> List[DataAccess]:
        """
        Get information on what data is needed and under what format
        """

    def run(self, data) -> None:
        """
        Run the service with the necessary data
        """