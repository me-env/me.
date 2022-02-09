from me.logger import MeLogger, DEBUG, DEFAULT
from me.plugins.banks_manager.bank_account import BankAccountTink
from me.IDataSource import IDataSource


class PluginTink(IDataSource):
    def __init__(self):
        self._banks_manager = BanksManager

    def getData(self):
        """
        """
        # self._banks_manager.getAllTransactions()

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


class BanksManager:
    def __init__(self):
        self.log = MeLogger(name=__name__, level=DEFAULT)
        self.log.info('Setup Bank Accounts')
        self.accounts = {
            'cic': BankAccountTink('cic'),
            'boursorama': BankAccountTink('boursorama'),
        }

    def getTransactions(self, min_timestamp=None):
        """
        ((unused))
        Get transactions from all accounts
        :param min_timestamp: ((unused))
        :return: all fetched transactions
        """
        txs = []
        for account in self.accounts:
            txs_account = self.accounts[account].getTransactions(min_timestamp)
            self.log.debug('txs_account', txs_account)
            txs += txs_account
        return txs

    def getAllTransactions(self, columns, check, convert):
        """
        Get all transactions from all accounts
        :return: all fetched transactions
        """
        txs = []
        for account in self.accounts:
            self.log.debug("get transactions")
            txs_account = self.accounts[account].getAllTransactions(columns, check, convert)
            self.log.info('add', len(txs_account), 'transactions for account', account)
            self.log.debug('append', txs_account)
            txs += txs_account

        return txs


