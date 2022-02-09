

class IDataSource:
    def getData(self):
        """
        Get data from the datasource.
        Done in a thread to let the data source run
        """
        raise NotImplementedError

    def getSchema(self):
        """
        Get schema to know how to store the data in me.
        """
        raise NotImplementedError

    def getAccessAuth(self):
        """
        Get information about who can access data
        """
        raise NotImplementedError

    def getStorageDetails(self):
        """
        Get information about how to store data, such as the type of database needed and where to store it
        """
        raise NotImplementedError
