from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, name, run_strategy):
        self._name = name
        self._run_strategy = run_strategy


    @property
    def name(self):
        return self._name


class IDataSource(ABC):
    @abstractmethod
    def getData(self):
        """
        Get data from the datasource.
        Done in a thread to let the data source run
        """

    @abstractmethod
    def getSchema(self):
        """
        Get schema to know how to store the data in me.
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


class IService(ABC):
    @abstractmethod
    def neededDataDetails(self):
        """
        Get information on what data is needed and under what format
        """

    def run(self, data):
        """
        Run the service with the necessary data
        """