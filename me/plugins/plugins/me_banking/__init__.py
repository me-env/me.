from typing import List

from me.logger import MeLogger, DEFAULT
from me.plugins import IDataSource, IService
from me.storage.data_config import DataType, DataAction, DataAccess

from .datasource import BanksManager
from .service import BankingAPI

from multiprocessing import Process


class MeBankingDataSource(IDataSource):
    def __init__(self):
        self._banks_manager = BanksManager()

    def getData(self, columns, check, convert):
        """
        """
        return self._banks_manager.getAllTransactions(columns, check, convert)

    def getAccessAuth(self):
        """
        Get information about who can access data
        """
        raise NotImplementedError

    def getStorageDetails(self):
        """
        Get information about how to store data, such as the type of database needed and where to store it
        """
        return {
            'db_engine': 'psql',
            'db': 'me',
            'schema': 'me_banking',
            'table': 'transactions',
            'type': DataType.TXs
        }


def startAPI(data):
    api = BankingAPI(data)
    api.run()


class MeBankingService(IService):
    def __init__(self):
        self.log = MeLogger(name=__name__)
        self._data = None
        self._subproc = None
        self.api = None

    def setNeededData(self, data):
        """
        This is name data, but it is the tool to access the data, not the raw data itself.
        """
        if data and not self._data:
            self._data = data

    def neededDataDetails(self) -> List[DataAccess]:
        return [DataAccess(DataType.TXs, [DataAction.READ, DataAction.UPDATE, DataAction.CREATE])]

    def run(self, data=None) -> None:
        """
        Run the service with the necessary data
        """
        self.setNeededData(data)
        if not self._data:
            self.log.warn('Service not started because the needed data has to been provided')
            return
        if self._subproc:
            self.log.warn('Service already started')
            return

        api = BankingAPI(self._data)
        api.run()
        self.log.info('API started.')

    def __del__(self):
        if self._subproc and self._subproc.is_alive():
            self._subproc.terminate()
            if self._subproc.is_alive():
                self._subproc.kill()  # FIXME (send a message to stop it)
            self._subproc.join()

