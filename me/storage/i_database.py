from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def addRow(self, data_type, data):
        """
        Add data 'data' in database (should be one row)
        """

    @abstractmethod
    def addMultipleRows(self, data_type, data):
        """
        Add data 'data' in database (should be one a list of rows)
        """

    @abstractmethod
    def getAllRows(self, data_type):
        """
        """

    @abstractmethod
    def reset(self):
        """
        Reset database content
        """

    @abstractmethod
    def getScheme(self, data):
        """
        Get Schema to respect for data 'data'
        Return check and convert dictionary with for each field the convert function / check (type) function
        """

    @abstractmethod
    def connect(self):
        """
        Connect to database
        """