from me.plugins import IService, IDataSource


class Photo(IDataSource, IService):
    ### IDataSource ###
    def getData(self):
        """
        Get data from the datasource.
        Done in a thread to let the data source run
        """

    def getSchema(self):
        """
        Get schema to know how to store the data in me.
        """

    def getAccessAuth(self):
        """
        Get information about who can access data
        """

    def getStorageDetails(self):
        """
        Get information about how to store data, such as the type of database needed and where to store it
        """

    ### IService ###

    def neededDataDetails(self):
        """
        Get information on what data is needed and under what format
        """

    def run(self, data):
        """
        Run the service with the necessary data
        """